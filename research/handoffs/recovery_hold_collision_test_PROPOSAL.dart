// ENGINEERING HANDOFF / PROPOSAL ONLY — not installed or executed in LogMate.
// Pinned product source: yhappcom/logmate main@5ad78167cb97d6846ed7b5f866151d2a080dcc88.
// Copy into test/repository/logbook/ after Engineering review.
// R03/R04 are intentionally RED against the pinned source: they encode the
// conservative FAIL-CLOSED remediation contract. A lineage-preserving fix
// requires a different, equally strong dual-evidence semantic oracle.
import 'package:flutter_test/flutter_test.dart';
import 'package:logmate/repository/logbook/local_owner_access.dart';
import 'package:logmate/repository/logbook/sembast_logbook_repository.dart';
import 'package:logmate/repository/logbook/whole_ledger_backup.dart';
import 'package:sembast/sembast_memory.dart';

const _uid = 'synthetic-recovery-owner';
const _cursorName = 'logmate_sync_applied_cursor_v1';
const _appliedName = 'logmate_sync_applied_identities_v1';
final _holds = StoreRef<String, Map<String, Object?>>(
  'logmate_sync_holds_v1',
);
final _cursor = StoreRef<String, Map<String, Object?>>(_cursorName);
final _applied = StoreRef<String, Map<String, Object?>>(_appliedName);
final _state = StoreRef<String, Map<String, Object?>>('logmate_sync_state_v1');

Map<String, Object?> _historicalHold(
  String sourceStore,
  String sourceKey,
  Map<String, Object?> evidence,
) => <String, Object?>{
  'classification': 'recoveryRequired',
  'sourceStore': sourceStore,
  'sourceKey': sourceKey,
  'sourceEvidence': evidence,
};

Future<void> _assertFailClosedCollision({
  required String sourceStore,
  required String sourceKey,
  required Map<String, Object?> liveEvidence,
}) async {
  final factory = newDatabaseFactoryMemory();
  final sourceDb = await factory.openDatabase('source-$sourceStore');
  addTearDown(sourceDb.close);
  final source = await SembastLogbookRepository.open(sourceDb);
  await source.createOwnedLedger(_uid);

  final live = StoreRef<String, Map<String, Object?>>(sourceStore);
  final collisionKey = 'restored:$sourceStore:$sourceKey';
  final historical = _historicalHold(sourceStore, sourceKey, {
    'generation': 'historical-A',
  });
  await _holds.record(collisionKey).put(sourceDb, historical);
  await live.record(sourceKey).put(sourceDb, liveEvidence);

  final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);
  final snapshot = WholeLedgerBackup.decode(encoded);
  expect(snapshot.manifest['backupFormatVersion'], 2);
  expect(snapshot.stores, hasLength(37));
  expect(snapshot.stores['logmate_sync_holds_v1'], hasLength(1));
  expect(snapshot.stores[sourceStore], hasLength(1));

  final destinationDb = await factory.openDatabase('destination-$sourceStore');
  addTearDown(destinationDb.close);
  final destination = await SembastLogbookRepository.open(destinationDb);
  final originalReplica = await destination.readLocalReplicaIdentity();

  // R03/R04 target: rejecting before commit is acceptable; silently
  // overwriting the older hold is not. This assertion FAILS on pinned main.
  await expectLater(
    destination.restoreWholeLedgerBackup(
      encoded,
      verifiedOwnerUid: _uid,
    ),
    throwsFormatException,
  );
  expect(await destination.readLocalReplicaIdentity(), originalReplica);
  expect(
    await destination.readOwnerAccess(),
    const LocalOwnerAccess.unbound(),
  );
  expect(await _holds.count(destinationDb), 0);
  expect(await live.count(destinationDb), 0);
  expect(await _holds.record(collisionKey).get(sourceDb), historical);
  expect(await live.record(sourceKey).get(sourceDb), liveEvidence);
}

void main() {
  test('R03 RED: existing cursor recovery hold must not be overwritten', () async {
    await _assertFailClosedCollision(
      sourceStore: _cursorName,
      sourceKey: 'stream',
      liveEvidence: {'sequence': '7'},
    );
  });

  test('R04 RED: existing applied-identity hold must not be overwritten', () async {
    await _assertFailClosedCollision(
      sourceStore: _appliedName,
      sourceKey: 'op-source',
      liveEvidence: {'operationId': 'op-source'},
    );
  });

  test('R05 control: distinct hold keys and new source evidence coexist', () async {
    final factory = newDatabaseFactoryMemory();
    final sourceDb = await factory.openDatabase('r05-source');
    addTearDown(sourceDb.close);
    final source = await SembastLogbookRepository.open(sourceDb);
    await source.createOwnedLedger(_uid);
    final oldHold = _historicalHold(_cursorName, 'previous', {
      'generation': 'historical-A',
    });
    await _holds.record('existing:previous').put(sourceDb, oldHold);
    await _cursor.record('stream').put(sourceDb, {'sequence': '7'});
    await _applied.record('op-source').put(sourceDb, {
      'operationId': 'op-source',
    });
    final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);

    final destinationDb = await factory.openDatabase('r05-destination');
    addTearDown(destinationDb.close);
    final destination = await SembastLogbookRepository.open(destinationDb);
    final destinationReplica = await destination.readLocalReplicaIdentity();
    await destination.restoreWholeLedgerBackup(
      encoded,
      verifiedOwnerUid: _uid,
    );

    expect(await _holds.count(destinationDb), 3);
    expect(await _holds.record('existing:previous').get(destinationDb), oldHold);
    expect(
      await _holds.record('restored:$_cursorName:stream').get(destinationDb),
      isNotNull,
    );
    expect(
      await _holds.record('restored:$_appliedName:op-source').get(destinationDb),
      isNotNull,
    );
    expect(await _cursor.count(destinationDb), 0);
    expect(await _applied.count(destinationDb), 0);
    expect(await destination.readLocalReplicaIdentity(), destinationReplica);
    final sync = await _state.record('current').get(destinationDb);
    expect(sync!['streamBindingStatus'], 'unbound');
    expect(sync['remoteBaselineStatus'], 'unverified');
    expect(sync['originReplicaId'], destinationReplica);
    expect((await destination.readOwnerAccess() as BoundLocalOwnerAccess).isUnlocked, isFalse);
  });

  test('R11 control: injected fault rolls back copied and transformed holds', () async {
    final factory = newDatabaseFactoryMemory();
    final sourceDb = await factory.openDatabase('r11-source');
    addTearDown(sourceDb.close);
    final source = await SembastLogbookRepository.open(sourceDb);
    await source.createOwnedLedger(_uid);
    final historicalKey = 'existing:r11-history';
    final oldHold = _historicalHold(_cursorName, 'previous', {
      'generation': 'historical-A',
    });
    await _holds.record(historicalKey).put(sourceDb, oldHold);
    await _cursor.record('stream').put(sourceDb, {'sequence': '7'});
    final encoded = await source.exportWholeLedgerBackup(verifiedOwnerUid: _uid);

    final destinationDb = await factory.openDatabase('r11-destination');
    addTearDown(destinationDb.close);
    final destination = await SembastLogbookRepository.open(destinationDb);
    final destinationReplica = await destination.readLocalReplicaIdentity();
    await expectLater(
      destination.restoreWholeLedgerBackup(
        encoded,
        verifiedOwnerUid: _uid,
        afterStoreWritesForTesting: () async => throw StateError('injected'),
      ),
      throwsA(isA<StateError>()),
    );
    expect(await destination.readLocalReplicaIdentity(), destinationReplica);
    expect(await destination.readOwnerAccess(), const LocalOwnerAccess.unbound());
    expect(await _holds.count(destinationDb), 0);
    expect(await _cursor.count(destinationDb), 0);
    expect(await _holds.record(historicalKey).get(sourceDb), oldHold);
  });
}
