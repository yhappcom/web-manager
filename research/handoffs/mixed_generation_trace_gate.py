#!/usr/bin/env python3
"""Review-only M01/M02/M06/M09 mixed-generation Chrome evidence gate.

This verifies a *recorded* real-browser evidence envelope; it does not run
Chrome, establish the honesty of a recorder, or authorize a PWA release.
No flight records or identifiers belong in the trace.
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

V16 = '59cd171176c58b598a4db55d128ffd21d406e862'  # GitHub-resolved historical v16 commit
V17 = '5ad78167cb97d6846ed7b5f866151d2a080dcc88'
EVENTS = ('old_open', 'migration', 'stale_write', 'browser_exit', 'restart_readback')


def _sha(s):
    return isinstance(s, str) and len(s) == 40 and all(c in '0123456789abcdef' for c in s)


def _origin(s):
    """Validate a bare secure-context origin, not a URL with credentials/path."""
    if not isinstance(s, str):
        return False
    try:
        u = urlsplit(s)
        host = u.hostname
        port = u.port  # force validation of malformed/out-of-range ports
        return (u.scheme == 'https' or
                (u.scheme == 'http' and host in ('localhost', '127.0.0.1'))) and (
                bool(host) and u.username is None and u.password is None and
                u.path in ('', '/') and not u.query and not u.fragment and
                (port is None or 1 <= port <= 65535))
    except (TypeError, ValueError):
        return False


def _digest(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def _count(n):
    # bool is a subclass of int in Python; a boolean is not a record count.
    return type(n) is int and n >= 0


def assess(t):
    """Return (verdict, diagnostics). Never claims browser/product PASS from untrusted JSON alone."""
    issues = []
    if not isinstance(t, dict):
        return 'INVALID', ['root must be an object']
    for key in ('run_id', 'workflow_url', 'browser_version', 'platform', 'profile_id', 'origin', 'v16_build_sha256', 'v17_build_sha256'):
        if not isinstance(t.get(key), str) or not t[key].strip():
            issues.append(f'missing provenance: {key}')
    if t.get('evidence_kind') != 'real_chrome':
        issues.append('evidence_kind must be real_chrome (synthetic/model cannot pass)')
    if t.get('browser') not in ('Chrome', 'Chromium'):
        issues.append('browser must be Chrome or Chromium')
    if t.get('source_v17') != V17:
        issues.append('source_v17 is not pinned current main')
    if t.get('source_v16') != V16:
        issues.append('source_v16 must match exact historical commit')
    if not _origin(t.get('origin')):
        issues.append('origin must be a stable secure-context origin, not a path')
    for key in ('v16_build_sha256', 'v17_build_sha256'):
        digest = t.get(key)
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            issues.append(f'{key} must be a full SHA-256')
    if t.get('build_kind') not in ('test_instrumented', 'normal'):
        issues.append('build_kind must distinguish instrumented from NORMAL artifacts')
    if not (isinstance(t.get('browser_version'), str) and
            len(t['browser_version'].split('.')) == 4 and
            all(p.isdigit() for p in t['browser_version'].split('.'))):
        issues.append('browser_version must be a four-part numeric browser version')
    events = t.get('events')
    if not isinstance(events, list) or [x.get('kind') for x in events if isinstance(x, dict)] != list(EVENTS) or len(events) != len(EVENTS):
        return 'INVALID', issues + ['required event order: ' + ' > '.join(EVENTS)]
    if any(not isinstance(x, dict) for x in events):
        return 'INVALID', issues + ['events must be objects']
    old, migrated, stale, exit_event, resumed = events
    for event in events:
        for key in ('origin', 'profile_id', 'process_id'):
            if event.get(key) != t.get(key) and key != 'process_id':
                issues.append(f'{event["kind"]} {key} differs from envelope')
        if not isinstance(event.get('process_id'), str) or not event['process_id'].strip():
            issues.append(f'{event["kind"]} lacks process id')
    # Historical "binary_sha" actually holds a SOURCE commit, not an artifact
    # digest. The separate per-event build hash must match the envelope.
    if old.get('binary_sha') != t.get('source_v16') or old.get('capability') != 16:
        issues.append('old tab must claim pinned v16 source with capability 16')
    if migrated.get('binary_sha') != V17 or migrated.get('capability') != 17 or migrated.get('store_count') != 37:
        issues.append('migration must claim pinned v17 source with 37 stores')
    for event, expected_build in ((old, t.get('v16_build_sha256')),
                                  (migrated, t.get('v17_build_sha256')),
                                  (stale, t.get('v16_build_sha256')),
                                  (resumed, t.get('v17_build_sha256'))):
        if not _digest(event.get('build_sha256')) or event['build_sha256'] != expected_build:
            issues.append(f'{event["kind"]} lacks matching per-event build SHA-256')
    if old.get('tab_state') != 'open' or migrated.get('old_tab_still_open') is not True or stale.get('old_tab_still_open') is not True:
        issues.append('old v16 tab must remain open through migration and stale attempt')
    if old.get('process_id') != migrated.get('process_id') or stale.get('process_id') != old.get('process_id'):
        issues.append('old tab and migration/stale attempt must share live browser process')
    if old.get('tab_id') == migrated.get('tab_id') or not old.get('tab_id') or not migrated.get('tab_id'):
        issues.append('two distinct concurrently open tabs are required')
    if stale.get('tab_id') != old.get('tab_id') or stale.get('binary_sha') != t.get('source_v16'):
        issues.append('stale write must originate from the still-open old tab/binary')
    if stale.get('method') != 'commitLedgerMutation':
        issues.append('stale canonical commit not exercised')
    if stale.get('outcome') != 'rejected' or not isinstance(stale.get('error_code'), str) or not stale['error_code'].strip():
        issues.append('stale canonical commit must be rejected with an observed error')
    if (stale.get('preconditions_validated') is not True or
            stale.get('capability_marker_observed') != 17 or
            stale.get('rejection_class') != 'capability_version_guard'):
        issues.append('stale rejection must exercise capability guard, not unrelated invalid preconditions')
    baseline = migrated.get('ledger_digest')
    if not _digest(baseline):
        issues.append('migration ledger digest invalid')
    if stale.get('before_digest') != baseline or stale.get('after_digest') != baseline:
        issues.append('stale write changed 37-store ledger state or lacks before/after proof')
    if exit_event.get('process_id') != old.get('process_id') or exit_event.get('outcome') != 'closed' or exit_event.get('all_tabs_closed') is not True:
        issues.append('browser process exit and old-tab closure not recorded')
    if resumed.get('process_id') == old.get('process_id') or resumed.get('binary_sha') != V17:
        issues.append('restart must use a new browser process claiming v17')
    if resumed.get('profile_reused') is not True or resumed.get('reseeded') is not False:
        issues.append('restart must reuse persistent profile without fixture re-seeding')
    if resumed.get('capability') != 17 or resumed.get('store_count') != 37 or resumed.get('ledger_digest') != baseline:
        issues.append('post-restart 37-store semantic readback does not match')
    for e in (migrated, stale, resumed):
        if not _count(e.get('remote_receipts')) or e['remote_receipts'] != 0 or e.get('remote_authority') is not False:
            issues.append(f'{e["kind"]} must not fabricate remote authority/receipts')
        if not _count(e.get('unsynced_count')) or e['unsynced_count'] < 1:
            issues.append(f'{e["kind"]} must demonstrate nonempty preserved unsynced records')
    if migrated.get('unsynced_count') != stale.get('unsynced_count') or migrated.get('unsynced_count') != resumed.get('unsynced_count'):
        issues.append('unsynced record count changed across rejected stale write/restart')
    if t.get('fixture_kind') != 'synthetic_no_personal_data':
        issues.append('only synthetic data is acceptable for this evidence packet')
    # Even stricter metadata is self-reported; independently verify raw Chrome
    # process logs, app error provenance, build inventories and semantic digest.
    # Consistency is not attestation. A JSON recorder can fabricate every field.
    return ('TRACE_CONSISTENT_UNVERIFIED' if not issues else 'INVALID'), issues


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('trace', type=Path)
    args = p.parse_args()
    try:
        trace = json.loads(args.trace.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(json.dumps({'verdict': 'INVALID', 'issues': [str(e)]}))
        return 2
    verdict, issues = assess(trace)
    print(json.dumps({'verdict': verdict, 'issues': issues}, ensure_ascii=False, indent=2))
    return 0 if verdict == 'TRACE_CONSISTENT_UNVERIFIED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
