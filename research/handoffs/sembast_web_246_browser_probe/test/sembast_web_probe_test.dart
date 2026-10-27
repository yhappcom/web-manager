import 'package:sembast_web/sembast_web.dart';
import 'package:test/test.dart';

// Research-only synthetic stores. No LogMate source, flight records or secrets.
final _flights = stringMapStoreFactory.store('flights');
final _revisions = stringMapStoreFactory.store('revisions');
final _outbox = stringMapStoreFactory.store('outbox');
int _sequence = 0;

String _newDbName() =>
    'stage8_sembast_246_${DateTime.now().microsecondsSinceEpoch}_${_sequence++}';

Future<String> _applyStableOperation(
  Database db,
  String operationId,
  String digest,
) async {
  return db.transaction((txn) async {
    final existing = await _outbox.record(operationId).get(txn);
    if (existing != null) {
      if (existing['digest'] != digest) {
        throw StateError('operation identity collision');
      }
      return 'REPLAY';
    }
    await _flights.record('synthetic-flight').put(txn, {'value': 'A'});
    await _revisions.record(operationId).put(txn, {
      'operationId': operationId,
      'digest': digest,
    });
    await _outbox.record(operationId).put(txn, {
      'digest': digest,
      'status': 'PENDING',
    });
    return 'NEW';
  });
}

void main() {
  test('SB01 exact package: multi-store commit survives close/reopen', () async {
    final name = _newDbName();
    final db = await databaseFactoryWeb.openDatabase(name);
    try {
      await db.transaction((txn) async {
        await _flights.record('f1').put(txn, {'value': 123});
        await _revisions.record('r1').put(txn, {'flightId': 'f1'});
        await _outbox.record('o1').put(txn, {'revisionId': 'r1'});
      });
    } finally {
      await db.close();
    }

    final reopened = await databaseFactoryWeb.openDatabase(name);
    try {
      expect((await _flights.record('f1').get(reopened))?['value'], 123);
      expect((await _revisions.record('r1').get(reopened))?['flightId'], 'f1');
      expect((await _outbox.record('o1').get(reopened))?['revisionId'], 'r1');
    } finally {
      await reopened.close();
    }
  });

  test('SB02 exact package: thrown transaction rolls back all stores', () async {
    final name = _newDbName();
    final db = await databaseFactoryWeb.openDatabase(name);
    try {
      await expectLater(
        db.transaction((txn) async {
          await _flights.record('f2').put(txn, {'value': 999});
          await _revisions.record('r2').put(txn, {'flightId': 'f2'});
          await _outbox.record('o2').put(txn, {'revisionId': 'r2'});
          throw StateError('synthetic abort');
        }),
        throwsStateError,
      );
    } finally {
      await db.close();
    }

    final reopened = await databaseFactoryWeb.openDatabase(name);
    try {
      expect(await _flights.record('f2').get(reopened), isNull);
      expect(await _revisions.record('r2').get(reopened), isNull);
      expect(await _outbox.record('o2').get(reopened), isNull);
    } finally {
      await reopened.close();
    }
  });

  test('SB03 exact package: stable operation retry does not duplicate', () async {
    final db = await databaseFactoryWeb.openDatabase(_newDbName());
    try {
      expect(await _applyStableOperation(db, 'op1', 'digest-A'), 'NEW');
      expect(await _applyStableOperation(db, 'op1', 'digest-A'), 'REPLAY');
      expect((await _outbox.find(db)).length, 1);
      expect((await _revisions.find(db)).length, 1);
      expect((await _flights.find(db)).length, 1);
    } finally {
      await db.close();
    }
  });

  test('SB04 exact package: same operation ID/different digest rejected', () async {
    final name = _newDbName();
    final db = await databaseFactoryWeb.openDatabase(name);
    try {
      expect(await _applyStableOperation(db, 'op1', 'digest-A'), 'NEW');
      await expectLater(
        _applyStableOperation(db, 'op1', 'digest-B'),
        throwsStateError,
      );
    } finally {
      await db.close();
    }
    final reopened = await databaseFactoryWeb.openDatabase(name);
    try {
      expect((await _outbox.record('op1').get(reopened))?['digest'], 'digest-A');
      expect((await _outbox.find(reopened)).length, 1);
      expect((await _revisions.find(reopened)).length, 1);
    } finally {
      await reopened.close();
    }
  });
}
