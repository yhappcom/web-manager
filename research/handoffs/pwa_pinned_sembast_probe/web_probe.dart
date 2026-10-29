// Synthetic pinned-package Sembast Web probe, NOT LogMate product evidence.
import 'dart:async';
import 'dart:convert';
import 'dart:html' as html;
import 'package:sembast/sembast.dart';
import 'package:sembast_web/sembast_web.dart';

final store = stringMapStoreFactory.store('synthetic_ledger');
late Database database;

Future<Map<String, Object?>> snapshot() async {
  final marker = await store.record('marker').get(database);
  final counter = await store.record('counter').get(database);
  final replica = await store.record('replica').get(database);
  return {'logicalCapability': marker?['capability'], 'counter': counter?['n'], 'replica': replica?['id']};
}

Future<Map<String, Object?>> execute(String command, int delayMs) async {
  if (command == 'reset') {
    await database.transaction((txn) async {
      await store.record('marker').put(txn, {'capability': 17});
      await store.record('counter').put(txn, {'n': 0});
      await store.record('replica').put(txn, {'id': 'SYNTHETIC-REPLICA'});
    });
    return snapshot();
  }
  if (command == 'inspect') return snapshot();
  if (command == 'increment') {
    var attempts = 0;
    await database.transaction((txn) async {
      attempts++;
      final current = await store.record('counter').get(txn);
      await Future<void>.delayed(Duration(milliseconds: delayMs));
      final n = (current?['n'] as num?)?.toInt() ?? 0;
      await store.record('counter').put(txn, {'n': n + 1});
    });
    return {'attempts': attempts, ...await snapshot()};
  }
  if (command == 'throw_before_commit') {
    var caught = false;
    try {
      await database.transaction((txn) async {
        await store.record('counter').put(txn, {'n': 999});
        throw StateError('deliberate synthetic transaction failure');
      });
    } catch (_) { caught = true; }
    return {'caught': caught, ...await snapshot()};
  }
  if (command == 'reopen') {
    await database.close();
    database = await databaseFactoryWeb.openDatabase('wm-pinned-sembast-246');
    return snapshot();
  }
  throw ArgumentError('Unknown command');
}

Future<void> main() async {
  database = await databaseFactoryWeb.openDatabase('wm-pinned-sembast-246');
  html.window.onMessage.listen((event) async {
    if (event.origin != html.window.location.origin || event.data is! String) return;
    Map<String, dynamic> message;
    try { message = jsonDecode(event.data as String) as Map<String, dynamic>; }
    catch (_) { return; }
    if (message['probeCmd'] != true) return;
    final id = message['id'].toString();
    try {
      final result = await execute(message['command'].toString(), (message['delayMs'] as num?)?.toInt() ?? 0);
      html.window.postMessage(jsonEncode({'probeReply': true, 'id': id, 'ok': true, 'result': result}), html.window.location.origin);
    } catch (error) {
      html.window.postMessage(jsonEncode({'probeReply': true, 'id': id, 'ok': false, 'error': '$error'}), html.window.location.origin);
    }
  });
  html.document.body?.setAttribute('data-ready', 'true');
}
