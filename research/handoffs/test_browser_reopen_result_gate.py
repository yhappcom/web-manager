#!/usr/bin/env python3
"""Synthetic Dart JSON reporter contract tests; never product/Chrome execution evidence.

Run: python3 research/handoffs/test_browser_reopen_result_gate.py
All cases use disposable local JSONL; no network, user records or Flutter runtime.
"""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('oracle', HERE / 'browser_reopen_result_gate.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)

TESTS = (
    'B1 Chrome restores 30 stores across IndexedDB close reopen',
    'B1 Chrome rejects tamper and wrong owner without mutation',
    'B1 Chrome rolls back injected failure and retries after reopen',
)
SUITE = 'test/repository/logbook/whole_ledger_backup_browser_test.dart'


def fixture(names=TESTS, platform='chrome', path=SUITE):
    events = [
        {'type': 'start', 'protocolVersion': '0.1.2', 'runnerVersion': 'synthetic'},
        {'type': 'suite', 'suite': {'id': 10, 'platform': platform, 'path': path}},
        {'type': 'testStart', 'test': {'id': 90, 'name': 'loading synthetic', 'suiteID': 10}},
        {'type': 'testDone', 'testID': 90, 'result': 'success', 'hidden': True, 'skipped': False, 'retried': False},
    ]
    for i, name in enumerate(names, start=1):
        events += [
            {'type': 'testStart', 'test': {'id': i, 'name': name, 'suiteID': 10}},
            {'type': 'testDone', 'testID': i, 'result': 'success', 'hidden': False, 'skipped': False, 'retried': False},
        ]
    events.append({'type': 'done', 'success': True})
    return events


def run_case(label, events, should_pass, exit_code=0, names=TESTS, suite=SUITE):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'events.jsonl'
        p.write_text('\n'.join(json.dumps(x) for x in events) + '\n', encoding='utf-8')
        try:
            result = oracle.check(p, exit_code, names, suite)
            actual = True
        except (ValueError, OSError) as e:
            result = str(e)
            actual = False
    print(f'{"PASS" if actual == should_pass else "MISMATCH"}: {label}: {result[:110]}')
    return actual == should_pass


def main():
    cases = []
    base = fixture()
    cases.append(('three-test canonical chrome', base, True, 0, TESTS, SUITE))
    cases.append(('one-test original contract', fixture(names=oracle.DEFAULT_EXPECTED, path='test/repository/logbook/sembast_web_reopen_test.dart'), True, 0, oracle.DEFAULT_EXPECTED, 'test/repository/logbook/sembast_web_reopen_test.dart'))
    cases.append(('VM substitution', fixture(platform='vm'), False, 0, TESTS, SUITE))
    cases.append(('synthetic non-chrome token', fixture(platform='notchrome'), False, 0, TESTS, SUITE))
    cases.append(('missing test', fixture(names=TESTS[:2]), False, 0, TESTS, SUITE))
    cases.append(('extra test', fixture(names=TESTS+('unexpected',)), False, 0, TESTS, SUITE))
    cases.append(('wrong suite', fixture(path='other_test.dart'), False, 0, TESTS, SUITE))
    cases.append(('path suffix spoof', fixture(path='evil' + SUITE), False, 0, TESTS, SUITE))
    cases.append(('absolute correct suite', fixture(path='/runner/work/logmate/logmate/' + SUITE), True, 0, TESTS, SUITE))
    cases.append(('nonzero process', base, False, 7, TESTS, SUITE))
    for kind in ('skipped', 'retried', 'result', 'hidden'):
        x = copy.deepcopy(base)
        i = next(i for i,e in enumerate(x) if e.get('type') == 'testDone' and e.get('testID') == 1)
        x[i][kind] = {'skipped': True, 'retried': True, 'result': 'failure', 'hidden': True}[kind]
        cases.append((f'{kind} test result', x, False, 0, TESTS, SUITE))
    for kind in ('error', 'print'):
        x = copy.deepcopy(base)
        x.insert(-1, {'type': kind, 'testID': 1})
        cases.append((f'{kind} late event', x, kind == 'print', 0, TESTS, SUITE))
    for label, mod in [
        ('missing done', lambda x: x.pop()),
        ('false done', lambda x: x[-1].update(success=False)),
        ('duplicate done', lambda x: x.insert(-1, {'type':'done','success':True})),
        ('orphan testDone', lambda x: x.insert(-1, {'type':'testDone','testID':404,'result':'success','hidden':False,'skipped':False,'retried':False})),
        ('duplicate test ID', lambda x: x.insert(-1, {'type':'testStart','test':{'id':1,'name':'again','suiteID':10}})),
        ('duplicate suite ID', lambda x: x.insert(-1, {'type':'suite','suite':{'id':10,'platform':'chrome','path':SUITE}})),
        ('unfinished test', lambda x: x.insert(-1, {'type':'testStart','test':{'id':404,'name':'extra','suiteID':10}})),
        ('missing skipped field', lambda x: x[5].pop('skipped')),
        ('missing retried field', lambda x: x[5].pop('retried')),
    ]:
        x = copy.deepcopy(base)
        mod(x)
        cases.append((label, x, False, 0, TESTS, SUITE))
    matches = sum(run_case(*c) for c in cases)
    print(f'EXPECTED VERDICTS: {matches}/{len(cases)}')
    return matches == len(cases)


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
