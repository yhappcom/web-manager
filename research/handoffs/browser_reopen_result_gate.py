#!/usr/bin/env python3
"""Review-only fail-closed oracle for one LogMate Chrome IndexedDB reopen test.

Consumes Flutter `flutter test --machine` JSONL. This validates reporter evidence,
not the correctness of the test implementation or PWA/Service Worker behavior.
"""
import argparse
import json
import sys
from pathlib import Path

EXPECTED = 'IndexedDB canonical ledger survives create delete restore reopen'


def check(path: Path, process_exit: int):
    if process_exit != 0:
        raise ValueError(f'Flutter test process exit={process_exit}')
    tests = {}
    suites = {}
    finished = {}
    errors = []
    done = []
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines:
        raise ValueError('empty machine reporter stream')
    for index, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'non-JSON machine event on line {index}') from exc
        if not isinstance(event, dict) or 'type' not in event:
            raise ValueError(f'malformed machine event on line {index}')
        kind = event['type']
        if kind == 'suite':
            suite = event.get('suite', {})
            suites[suite.get('id')] = str(suite.get('platform', '')).lower()
        elif kind == 'testStart':
            test = event.get('test', {})
            ident = test.get('id')
            if ident is None or ident in tests:
                raise ValueError('missing or duplicate test ID')
            tests[ident] = test
        elif kind == 'testDone':
            ident = event.get('testID')
            if ident not in tests or ident in finished:
                raise ValueError('orphan or duplicate testDone')
            finished[ident] = event
        elif kind == 'error':
            errors.append(event)
        elif kind == 'done':
            done.append((index, event.get('success')))
    if len(done) != 1 or done[0] != (len(lines), True):
        raise ValueError('missing/duplicate/nonfinal successful done event')
    if errors:
        raise ValueError(f'{len(errors)} error event(s), including late errors')
    if len(finished) != len(tests):
        raise ValueError('unfinished tests')
    visible = [(test, finished[ident]) for ident, test in tests.items()
               if not finished[ident].get('hidden', False)]
    if len(visible) != 1:
        raise ValueError(f'expected one visible test, observed {len(visible)}')
    test, result = visible[0]
    if test.get('name') != EXPECTED:
        raise ValueError(f'unexpected test name: {test.get("name")!r}')
    if result.get('skipped') is not False or result.get('result') != 'success':
        raise ValueError('expected test did not execute successfully')
    platform = suites.get(test.get('suiteID'), '')
    if 'chrome' not in platform:
        raise ValueError(f'expected Chrome suite, got {platform!r}')
    return f'BROWSER REOPEN ORACLE PASS: 1/1 executed in {platform}; no skips/errors'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--events', required=True, type=Path)
    parser.add_argument('--exit-code', required=True, type=int)
    args = parser.parse_args()
    try:
        print(check(args.events, args.exit_code))
    except (OSError, ValueError) as exc:
        print(f'BROWSER REOPEN ORACLE FAIL: {exc}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
