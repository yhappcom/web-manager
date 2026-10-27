// Public synthetic browser bridge; not LogMate production source.
// Modern JS interop keeps this diagnostic compatible with Dart's current web APIs.
import 'dart:async';
import 'dart:convert';
import 'dart:js_interop';
import 'package:sembast_web/sembast_web.dart';

@JS('probeOpen')
external set probeOpen(JSFunction callback);
@JS('probeApply')
external set probeApply(JSFunction callback);
@JS('probeApplyGuarded')
external set probeApplyGuarded(JSFunction callback);
@JS('probeSetOwner')
external set probeSetOwner(JSFunction callback);
@JS('probeRead')
external set probeRead(JSFunction callback);
@JS('probeClose')
external set probeClose(JSFunction callback);
@JS('probeArmHold')
external set probeArmHold(JSFunction callback);
@JS('probeReleaseHold')
external set probeReleaseHold(JSFunction callback);
@JS('probeHasEntered')
external set probeHasEntered(JSFunction callback);
@JS('probeReady')
external set probeReady(JSBoolean value);

final _flights = stringMapStoreFactory.store('flights');
final _revisions = stringMapStoreFactory.store('revisions');
final _outbox = stringMapStoreFactory.store('outbox');
final _authority = stringMapStoreFactory.store('authority');
Database? _db;
bool _holdNext = false;
bool _holdEntered = false;
Completer<void>? _release;
int _callbackCount = 0;

Future<String> _open(String name) async {
  if (_db != null) await _db!.close();
  _db = await databaseFactoryWeb.openDatabase(name);
  return 'READY';
}

void _armHold() {
  _holdNext = true;
  _holdEntered = false;
  _release = Completer<void>();
}

void _releaseHold() {
  if (_release != null && !_release!.isCompleted) _release!.complete();
}

// Fixture-only local policy transition. This is NOT Firebase/UID authority.
Future<String> _setOwner(int epoch, String state) async {
  if (epoch < 1 || (state != 'ACTIVE' && state != 'REVOKED')) {
    throw StateError('invalid fixture owner state');
  }
  await _db!.transaction((txn) async {
    await _authority.record('current').put(txn, {
      'epoch': epoch, 'state': state
    });
  });
  return 'OWNER_SET';
}

Future<Map<String, Object?>> _apply(String id, String digest,
    {int? expectedEpoch}) async {
  final db = _db!;
  var calls = 0;
  try {
    final outcome = await db.transaction((txn) async {
      calls++;
      _callbackCount++;
      // The counter is intentionally outside the transaction: it demonstrates
      // that callback attempts can outnumber durable writes after replay/abort.
      if (expectedEpoch != null) {
        final owner = await _authority.record('current').get(txn);
        if (owner == null || owner['state'] != 'ACTIVE' ||
            owner['epoch'] != expectedEpoch) {
          throw StateError('owner fence denied');
        }
      }
      final existing = await _outbox.record(id).get(txn);
      if (_holdNext) {
        _holdNext = false;
        _holdEntered = true;
        await _release!.future;
      }
      if (existing != null) {
        if (existing['digest'] != digest) {
          throw StateError('operation identity collision');
        }
        return 'REPLAY';
      }
      await _flights.record('synthetic-flight').put(txn, {'value': 'A'});
      await _revisions.record(id).put(txn, {
        'operationId': id, 'digest': digest
      });
      await _outbox.record(id).put(txn, {
        'digest': digest, 'status': 'PENDING'
      });
      return 'NEW';
    });
    return {'outcome': outcome, 'calls': calls, 'totalCalls': _callbackCount};
  } catch (error) {
    return {'outcome': 'REJECTED', 'calls': calls,
      'totalCalls': _callbackCount, 'error': '$error'};
  }
}

Future<Map<String, Object?>> _read() async {
  final db = _db!;
  final outbox = await _outbox.find(db);
  return {
    'flights': (await _flights.find(db)).length,
    'revisions': (await _revisions.find(db)).length,
    'outbox': outbox.length,
    'digest': outbox.isEmpty ? null : outbox.first.value['digest'],
    'callbackCount': _callbackCount,
    'owner': await _authority.record('current').get(db)
  };
}

Future<String> _close() async {
  await _db?.close();
  _db = null;
  return 'CLOSED';
}

void main() {
  probeOpen = ((JSString name) =>
    _open(name.toDart).then((v) => v.toJS).toJS).toJS;
  probeApply = ((JSString id, JSString digest) =>
    _apply(id.toDart, digest.toDart)
      .then((v) => jsonEncode(v).toJS).toJS).toJS;
  probeApplyGuarded = ((JSString id, JSString digest, JSNumber epoch) =>
    _apply(id.toDart, digest.toDart, expectedEpoch: epoch.toDartInt)
      .then((v) => jsonEncode(v).toJS).toJS).toJS;
  probeSetOwner = ((JSNumber epoch, JSString state) =>
    _setOwner(epoch.toDartInt, state.toDart)
      .then((v) => v.toJS).toJS).toJS;
  probeRead = (() => _read()
    .then((v) => jsonEncode(v).toJS).toJS).toJS;
  probeClose = (() => _close()
    .then((v) => v.toJS).toJS).toJS;
  probeArmHold = (() { _armHold(); return true.toJS; }).toJS;
  probeReleaseHold = (() { _releaseHold(); return true.toJS; }).toJS;
  probeHasEntered = (() => _holdEntered.toJS).toJS;
  probeReady = true.toJS;
}
