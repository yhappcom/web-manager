// Public synthetic browser bridge. NOT LogMate production source.
// Legacy JS bridge is confined to this dart2js diagnostic, not a PWA/Wasm recommendation.
import 'dart:async';
import 'dart:js' as js;
import 'dart:js_util' as js_util;
import 'package:sembast_web/sembast_web.dart';

final _flights = stringMapStoreFactory.store('flights');
final _revisions = stringMapStoreFactory.store('revisions');
final _outbox = stringMapStoreFactory.store('outbox');
Database? _db;
bool _holdNext = false;
Completer<void>? _release;
int _callbackCount = 0;

Future<String> _open(String name) async {
  if (_db != null) await _db!.close();
  _db = await databaseFactoryWeb.openDatabase(name);
  return 'READY';
}

void _armHold() {
  _holdNext = true;
  _release = Completer<void>();
  js.context['probeHoldEntered'] = false;
}

void _releaseHold() {
  if (_release != null && !_release!.isCompleted) _release!.complete();
}

Future<Map<String, Object?>> _apply(String id, String digest) async {
  final db = _db!;
  var calls = 0;
  try {
    final outcome = await db.transaction((txn) async {
      calls++;
      _callbackCount++;
      final existing = await _outbox.record(id).get(txn);
      if (_holdNext) {
        _holdNext = false;
        js.context['probeHoldEntered'] = true;
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
    'callbackCount': _callbackCount
  };
}

Future<String> _close() async {
  await _db?.close();
  _db = null;
  return 'CLOSED';
}

void main() {
  js.context['probeOpen'] = js.allowInterop(
    (String name) => js_util.futureToPromise(_open(name)));
  js.context['probeApply'] = js.allowInterop(
    (String id, String digest) => js_util.futureToPromise(
      _apply(id, digest).then((value) => js_util.jsify(value))));
  js.context['probeRead'] = js.allowInterop(
    () => js_util.futureToPromise(
      _read().then((value) => js_util.jsify(value))));
  js.context['probeClose'] = js.allowInterop(
    () => js_util.futureToPromise(_close()));
  js.context['probeArmHold'] = js.allowInterop(_armHold);
  js.context['probeReleaseHold'] = js.allowInterop(_releaseHold);
  js.context['probeReady'] = true;
}
