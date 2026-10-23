// REVIEW-ONLY Engineering handoff. Browser-only; no dart:io.
// Source contract: yhappcom/logmate main@59cd171176c58b598a4db55d128ffd21d406e862.
// Requires Engineering compile/review; NOT a reported Chrome execution PASS.
import 'package:flutter_test/flutter_test.dart';
import 'package:logmate/domain/logbook/flight_record.dart';
import 'package:logmate/domain/logbook/ledger_page_projection.dart';
import 'package:logmate/domain/logbook/local_date.dart';
import 'package:logmate/domain/logbook/same_day_timeline_order.dart';
import 'package:logmate/repository/logbook/ledger_mutation_plan.dart';
import 'package:logmate/repository/logbook/ledger_projection_types.dart';
import 'package:logmate/repository/logbook/ledger_source_generation_types.dart';
import 'package:logmate/repository/logbook/ledger_structure_types.dart';
import 'package:logmate/repository/logbook/local_owner_access.dart';
import 'package:logmate/repository/logbook/repository_types.dart';
import 'package:logmate/repository/logbook/sembast_logbook_repository.dart';
import 'package:logmate/repository/logbook/whole_ledger_backup.dart';
import 'package:sembast/sembast.dart';
import 'package:sembast_web/sembast_web.dart';

const _uid = 'synthetic-b1-browser-owner';

void main() {
  test('B1 Chrome restores 30 stores across IndexedDB close reopen', () async {
    final prefix = _name('roundtrip');
    final sourceName = '$prefix-source';
    final destinationName = '$prefix-destination';
    Database? sourceDb;
    Database? destinationDb;
    try {
      sourceDb = await databaseFactoryWeb.openDatabase(sourceName);
      var source = await SembastLogbookRepository.open(sourceDb);
      await source.createOwnedLedger(_uid);
      await _createFlight(source);
      final sourceReplica = await source.readLocalReplicaIdentity();
      final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);
      final backup = WholeLedgerBackup.decode(encoded);
      expect(backup.stores.length, 30);
      expect(backup.stores['logmate_active_records_v1'], hasLength(1));
      expect(backup.stores['logmate_outbox_v1'], hasLength(1));

      await sourceDb.close();
      sourceDb = await databaseFactoryWeb.openDatabase(sourceName);
      source = await SembastLogbookRepository.open(sourceDb);
      expect(await source.readLocalReplicaIdentity(), sourceReplica);
      expect(await source.readPendingOperations(), hasLength(1));

      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      var destination = await SembastLogbookRepository.open(destinationDb);
      final destinationReplica = await destination.readLocalReplicaIdentity();
      expect(destinationReplica, isNot(sourceReplica));
      await destination.restoreWholeLedgerBackup(encoded, verifiedOwnerUid: _uid);
      expect(await destination.readLocalReplicaIdentity(), destinationReplica);
      final locked = await destination.readOwnerAccess();
      expect(locked, isA<BoundLocalOwnerAccess>());
      expect((locked as BoundLocalOwnerAccess).isUnlocked, isFalse);

      await destinationDb.close();
      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      destination = await SembastLogbookRepository.open(destinationDb);
      expect(await destination.readLocalReplicaIdentity(), destinationReplica);
      expect((await destination.readOwnerAccess() as BoundLocalOwnerAccess).isUnlocked, isFalse);
      await destination.unlockOwner(_uid);
      expect(await destination.readPendingOperations(), hasLength(1));
      final sourceStores = WholeLedgerBackup.decode(
        await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid),
      ).stores;
      final restoredStores = WholeLedgerBackup.decode(
        await destination.exportWholeLedgerBackup(verifiedOwnerUid: _uid),
      ).stores;
      sourceStores.remove('logmate_local_replica_v1');
      restoredStores.remove('logmate_local_replica_v1');
      expect(restoredStores, sourceStores);
    } finally {
      await sourceDb?.close();
      await destinationDb?.close();
      await databaseFactoryWeb.deleteDatabase(sourceName);
      await databaseFactoryWeb.deleteDatabase(destinationName);
    }
  });

  test('B1 Chrome rejects tamper and wrong owner without mutation', () async {
    final prefix = _name('reject');
    final sourceName = '$prefix-source';
    final destinationName = '$prefix-destination';
    Database? sourceDb;
    Database? destinationDb;
    try {
      sourceDb = await databaseFactoryWeb.openDatabase(sourceName);
      final source = await SembastLogbookRepository.open(sourceDb);
      await source.createOwnedLedger(_uid);
      await _createFlight(source);
      final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);
      final registry = WholeLedgerBackup.decode(encoded).stores.keys;

      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      final destination = await SembastLogbookRepository.open(destinationDb);
      final before = await _snapshot(destinationDb, registry);
      final replica = await destination.readLocalReplicaIdentity();
      await expectLater(
        destination.restoreWholeLedgerBackup('${encoded}x', verifiedOwnerUid: _uid),
        throwsFormatException,
      );
      await expectLater(
        destination.restoreWholeLedgerBackup(encoded, verifiedOwnerUid: 'different-owner'),
        throwsFormatException,
      );
      expect(await _snapshot(destinationDb, registry), before);
      expect(await destination.readLocalReplicaIdentity(), replica);
      expect(await destination.readOwnerAccess(), const LocalOwnerAccess.unbound());

      // A claimed but record-empty destination must not be overwritten.
      await destination.createOwnedLedger(_uid);
      final claimedBefore = await _snapshot(destinationDb, registry);
      await expectLater(
        destination.restoreWholeLedgerBackup(encoded, verifiedOwnerUid: _uid),
        throwsFormatException,
      );
      expect(await _snapshot(destinationDb, registry), claimedBefore);
    } finally {
      await sourceDb?.close();
      await destinationDb?.close();
      await databaseFactoryWeb.deleteDatabase(sourceName);
      await databaseFactoryWeb.deleteDatabase(destinationName);
    }
  });

  test('B1 Chrome rolls back injected failure and retries after reopen', () async {
    final prefix = _name('rollback');
    final sourceName = '$prefix-source';
    final destinationName = '$prefix-destination';
    Database? sourceDb;
    Database? destinationDb;
    try {
      sourceDb = await databaseFactoryWeb.openDatabase(sourceName);
      final source = await SembastLogbookRepository.open(sourceDb);
      await source.createOwnedLedger(_uid);
      await _createFlight(source);
      final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);
      final registry = WholeLedgerBackup.decode(encoded).stores.keys;

      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      var destination = await SembastLogbookRepository.open(destinationDb);
      final before = await _snapshot(destinationDb, registry);
      final replica = await destination.readLocalReplicaIdentity();
      await expectLater(
        destination.restoreWholeLedgerBackup(
          encoded,
          verifiedOwnerUid: _uid,
          afterStoreWritesForTesting: () async => throw StateError('synthetic rollback'),
        ),
        throwsA(isA<StateError>()),
      );
      expect(await _snapshot(destinationDb, registry), before);
      expect(await destination.readLocalReplicaIdentity(), replica);
      await destinationDb.close();
      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      destination = await SembastLogbookRepository.open(destinationDb);
      expect(await _snapshot(destinationDb, registry), before);
      await destination.restoreWholeLedgerBackup(encoded, verifiedOwnerUid: _uid);
      await destinationDb.close();
      destinationDb = await databaseFactoryWeb.openDatabase(destinationName);
      destination = await SembastLogbookRepository.open(destinationDb);
      expect(await destination.readLocalReplicaIdentity(), replica);
      await destination.unlockOwner(_uid);
      expect(await destination.readPendingOperations(), hasLength(1));
      final stores = WholeLedgerBackup.decode(
        await destination.exportWholeLedgerBackup(verifiedOwnerUid: _uid),
      ).stores;
      expect(stores.length, 30);
      expect(stores['logmate_active_records_v1'], hasLength(1));
    } finally {
      await sourceDb?.close();
      await destinationDb?.close();
      await databaseFactoryWeb.deleteDatabase(sourceName);
      await databaseFactoryWeb.deleteDatabase(destinationName);
    }
  });
}

String _name(String suffix) =>
    'logmate-b1-browser-$suffix-${DateTime.now().microsecondsSinceEpoch}';

Future<void> _createFlight(SembastLogbookRepository repository) async {
  final value = FlightLedgerRecordValue(FlightRecord(
    id: 'synthetic-b1-browser-flight',
    operationalDate: LocalDate(2026, 10, 23),
    remark: 'synthetic browser-only record',
  ));
  await repository.commitLedgerMutation(
    LedgerMutationPlan(
      recordMutation: PlannedRecordCreate(
        value: value,
        identity: LocalMutationIdentity(
          revisionId: RevisionId('synthetic-b1-browser-revision'),
          operationId: OperationId('synthetic-b1-browser-operation'),
          acceptedAtUtc: UtcEpochMicros(100),
        ),
      ),
      structureMutation: LedgerStructureMutation(
        expectedGeneration: LedgerStructureGeneration.initial,
        dayOrderChanges: [
          UpsertSameDayOrder(SameDayTimelineOrder(
            date: value.record.operationalDate,
            records: [value.ref],
            authority: SameDayTimelineOrderAuthority.initialEvidence,
          )),
        ],
        deletedSlotPolicyChanges: const [],
        projectionReplacement: LedgerProjectionTailReplacement(
          firstPageNumber: 1,
          pages: [
            LedgerPageProjection(
              pageNumber: 1,
              capacity: 15,
              status: LedgerPageStatus.active,
              occupiedSlots: [LedgerPageRecordSlot(value.ref)],
            ),
          ],
        ),
      ),
    ),
  );
}

Future<Map<String, List<Map<String, Object?>>>> _snapshot(
  Database db,
  Iterable<String> names,
) async => {
  for (final name in names)
    name: [
      for (final row in await StoreRef<dynamic, Map<String, Object?>>(
        name,
      ).find(db))
        {'key': row.key, 'value': Map<String, Object?>.from(row.value)},
    ],
};
