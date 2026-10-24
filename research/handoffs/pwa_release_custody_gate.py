#!/usr/bin/env python3
"""Independent, fail-closed LogMate PWA NORMAL/Acceptance artifact custody audit.

This tool verifies on-disk bytes and an externally stored receipt; it does NOT
prove a deployed origin, real browser offline behavior, or organizational signing.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

MARKER = b'LOGMATE_PERSISTENCE_ACCEPTANCE_FLIGHT_V1'
REQUIRED = ('index.html', 'flutter_bootstrap.js', 'main.dart.js',
            'logmate_service_worker.js', 'logmate-offline-manifest.json',
            'manifest.json', 'canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm')
HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')

class GateError(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical_path(encoded):
    if not isinstance(encoded, str) or not encoded or encoded.startswith('/'):
        raise GateError('invalid manifest path')
    pieces = encoded.split('/')
    decoded = [unquote(part, encoding='utf-8', errors='strict') for part in pieces]
    if any(part in ('', '.', '..') or '/' in part or '\\' in part or '\x00' in part
           for part in decoded):
        raise GateError('unsafe manifest path')
    return '/'.join(decoded)

def inventory(root):
    if root.is_symlink() or not root.is_dir():
        raise GateError('artifact root must be a real directory')
    result = {}
    for p in root.rglob('*'):
        if p.is_symlink():
            raise GateError('symlink in artifact')
        if p.is_dir():
            continue
        if not p.is_file():
            raise GateError('non-file artifact entry')
        relative = p.relative_to(root).as_posix()
        data = p.read_bytes()
        result[relative] = {'bytes': len(data), 'sha256': digest(data)}
    return dict(sorted(result.items()))

def manifest_check(root, items):
    for path in REQUIRED:
        if path not in items:
            raise GateError('required file missing: ' + path)
    try:
        manifest = json.loads((root / 'logmate-offline-manifest.json').read_text())
    except (ValueError, UnicodeError) as exc:
        raise GateError('invalid offline manifest') from exc
    if manifest.get('schemaVersion') != 2 or manifest.get('apiVersion') != 2:
        raise GateError('unexpected manifest schema/api')
    if not isinstance(manifest.get('appBuildId'), str) or not re.fullmatch(r'[0-9a-f]{32}', manifest['appBuildId']):
        raise GateError('invalid appBuildId')
    if not isinstance(manifest.get('fontSetId'), str):
        raise GateError('invalid fontSetId')
    groups = [('shell', None), ('fonts', 724), ('fontNotices', 148)]
    seen = set()
    for group, count in groups:
        records = manifest.get(group)
        if not isinstance(records, list) or (count is not None and len(records) != count) or not records:
            raise GateError('invalid record count: ' + group)
        for rec in records:
            if not isinstance(rec, dict) or type(rec.get('bytes')) is not int or rec['bytes'] < 0 or not isinstance(rec.get('sha256'), str) or not HEX64.fullmatch(rec['sha256']):
                raise GateError('invalid record: ' + group)
            path = canonical_path(rec.get('path'))
            if path in seen:
                raise GateError('duplicate manifest record: ' + path)
            seen.add(path)
            if items.get(path) != {'bytes': rec['bytes'], 'sha256': rec['sha256']}:
                raise GateError('manifest byte mismatch: ' + path)
    if sum(canonical_path(x['path']).endswith('/OFL.txt') for x in manifest['fontNotices']) != 144:
        raise GateError('incorrect OFL notice count')
    shell_hash = digest(json.dumps(manifest['shell'], ensure_ascii=False, separators=(',', ':')).encode())[:32]
    if shell_hash != manifest['appBuildId']:
        raise GateError('shell-derived appBuildId mismatch')
    worker = (root / 'logmate_service_worker.js').read_text()
    match = re.search(r'const OFFLINE_MANIFEST = (\{.*?\});\s*const CONTROL_CACHE', worker, re.S)
    if not match:
        raise GateError('worker embedded manifest not located')
    try:
        embedded = json.loads(match.group(1))
    except ValueError as exc:
        raise GateError('worker embedded manifest invalid') from exc
    if embedded != manifest:
        raise GateError('worker embedded manifest differs')
    if manifest['fontSetId'] not in (root / 'flutter_bootstrap.js').read_text():
        raise GateError('bootstrap fontSetId differs')
    return manifest

def scan_marker(root, items, kind):
    marked = []
    for path in items:
        if path.endswith(('.js', '.html', '.json', '.css')) and MARKER in (root / path).read_bytes():
            marked.append(path)
    if kind == 'normal' and marked:
        raise GateError('acceptance marker leaked: ' + ','.join(marked))
    if kind == 'acceptance' and 'main.dart.js' not in marked:
        raise GateError('acceptance marker missing from main.dart.js')

def snapshot(root, kind, source_sha):
    if not HEX40.fullmatch(source_sha):
        raise GateError('source SHA must be 40 lowercase hex characters')
    items = inventory(root)
    manifest = manifest_check(root, items)
    scan_marker(root, items, kind)
    canonical = json.dumps(items, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    return {'schema': 1, 'kind': kind, 'sourceSha': source_sha,
            'appBuildId': manifest['appBuildId'], 'fontSetId': manifest['fontSetId'],
            'workerSha256': items['logmate_service_worker.js']['sha256'],
            'manifestSha256': items['logmate-offline-manifest.json']['sha256'],
            'fileCount': len(items), 'treeSha256': digest(canonical), 'files': items}

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('freeze', 'verify'))
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--kind', choices=('normal', 'acceptance'), required=True)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--firebase-config', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.root.is_symlink():
            raise GateError('artifact root is a symlink')
        root = args.root.resolve(strict=True)
        receipt = args.receipt.absolute()
        if receipt == root or root in receipt.parents:
            raise GateError('receipt must be outside artifact root')
        current = snapshot(root, args.kind, args.source_sha)
        if args.firebase_config is not None:
            config = json.loads(args.firebase_config.read_text())
            hosting = config.get('hosting')
            if not isinstance(hosting, dict) or not isinstance(hosting.get('public'), str):
                raise GateError('unsupported Firebase Hosting public config')
            deployed_root = (args.firebase_config.resolve().parent / hosting['public']).resolve()
            if deployed_root != root:
                raise GateError('Firebase Hosting public root differs from verified artifact')
        if args.mode == 'freeze':
            if receipt.exists():
                raise GateError('receipt already exists: refusing overwrite')
            receipt.write_text(json.dumps(current, sort_keys=True, indent=2) + '\n')
        else:
            expected = json.loads(receipt.read_text())
            if current != expected:
                raise GateError('receipt mismatch: bytes or provenance changed')
        print(json.dumps({'verdict': 'DISK_ONLY_PASS', 'mode': args.mode,
                          'treeSha256': current['treeSha256'],
                          'workerSha256': current['workerSha256'],
                          'fileCount': current['fileCount']}))
        return 0
    except (GateError, OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({'verdict': 'HOLD', 'reason': str(exc)}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
