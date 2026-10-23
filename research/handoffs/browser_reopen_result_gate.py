#!/usr/bin/env python3
"""Engineering-review-only fail-closed Chrome machine-result oracle.

Default contract preserves the original single IndexedDB reopen test.
Pass repeated --expected-test to verify an exact multi-test B1 Chrome bundle.
This proves runner/test execution only, not correctness or device durability.
"""
import argparse
import json
import sys
from pathlib import Path

DEFAULT_EXPECTED = (
    'IndexedDB canonical ledger survives create delete restore reopen',
)


def check(path: Path, process_exit: int, expected_names=None, expected_suite_suffix=None):
    if process_exit != 0:
        raise ValueError(f'Flutter test process exit={process_exit}')
    expected = tuple(DEFAULT_EXPECTED if expected_names is None else expected_names)
    if not expected or len(set(expected)) != len(expected):
        raise ValueError('expected test names must be nonempty and unique')
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
            ident = suite.get('id')
            if ident is None or ident in suites:
                raise ValueError('missing or duplicate suite ID')
            suites[ident] = (str(suite.get('platform', '')).lower(),\n                             str(suite.get('path', '')).replace('\\\\', '/'))
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
    names = [test.get('name') for test, _ in visible]
    if len(visible) != len(expected) or set(names) != set(expected):
        raise ValueError(f'exact test set mismatch: expected={expected!r}, got={names!r}')
    for test, result in visible:
        if (result.get('skipped') is not False or\n                result.get('result') != 'success' or\n                result.get('retried') is not False):
            raise ValueError(f'test did not execute successfully: {test.get("name")!r}')
        platform = suites.get(test.get('suiteID'), '')
        if 'chrome' not in platform:
            raise ValueError(f'expected Chrome suite for {test.get("name")!r}, got {platform!r}')
    return f'BROWSER MACHINE ORACLE PASS: {len(expected)}/{len(expected)} executed in Chrome; no skips/errors'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--events', required=True, type=Path)
    parser.add_argument('--exit-code', required=True, type=int)
    parser.add_argument('--expected-test', action='append', dest='expected_tests')\n    parser.add_argument('--expected-suite-suffix')
    args = parser.parse_args()
    try:
        print(check(args.events, args.exit_code, args.expected_tests, args.expected_suite_suffix))
    except (OSError, ValueError) as exc:
        print(f'BROWSER MACHINE ORACLE FAIL: {exc}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
