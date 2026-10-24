#!/usr/bin/env python3
"""Read-only HTTP byte audit against an independently pinned NORMAL disk receipt.

This does not attest deployment authority, CDN-wide consistency, PWA runtime,
IndexedDB durability, or physical iPad acceptance.
"""
import argparse
import hashlib
import json
import re
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, HTTPHandler, Request, build_opener

REQUIRED = ('index.html', 'flutter_bootstrap.js', 'main.dart.js',
            'logmate_service_worker.js', 'logmate-offline-manifest.json',
            'manifest.json', 'canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm')
MUTABLE = {'index.html', 'flutter_bootstrap.js', 'logmate_service_worker.js',
           'logmate-offline-manifest.json', 'manifest.json'}
HEX = re.compile(r'^[0-9a-f]{64}$')

class GateError(ValueError):
    pass

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise GateError('redirect rejected: ' + str(code))

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def path_check(path):
    if not isinstance(path, str) or not path or path.startswith('/') or '\\' in path or '%' in path or '?' in path or '#' in path or '\x00' in path:
        raise GateError('unsafe receipt path')
    if any(part in ('', '.', '..') for part in path.split('/')):
        raise GateError('unsafe receipt path')
    return path

def validate_receipt(raw, pinned):
    if not HEX.fullmatch(pinned) or sha256(raw) != pinned:
        raise GateError('receipt not matched to independent SHA-256 pin')
    try:
        receipt = json.loads(raw)
    except (UnicodeError, ValueError) as exc:
        raise GateError('invalid receipt JSON') from exc
    if not isinstance(receipt, dict) or receipt.get('schema') != 1 or receipt.get('kind') != 'normal':
        raise GateError('not a NORMAL schema-1 receipt')
    files = receipt.get('files')
    if not isinstance(files, dict) or not files:
        raise GateError('missing file inventory')
    if receipt.get('fileCount') != len(files):
        raise GateError('fileCount mismatch')
    for path, rec in files.items():
        path_check(path)
        if not isinstance(rec, dict) or type(rec.get('bytes')) is not int or rec['bytes'] < 0 or not isinstance(rec.get('sha256'), str) or not HEX.fullmatch(rec['sha256']):
            raise GateError('invalid inventory record: ' + path)
    if any(p not in files for p in REQUIRED):
        raise GateError('missing required receipt entry')
    tree = sha256(json.dumps(files, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())
    if receipt.get('treeSha256') != tree or receipt.get('workerSha256') != files['logmate_service_worker.js']['sha256']:
        raise GateError('receipt self-consistency mismatch')
    return files

def origin_base(value, allow_loopback):
    u = urlsplit(value)
    if u.username or u.password or u.query or u.fragment or not u.hostname or u.path not in ('', '/'):
        raise GateError('origin must be bare HTTPS scheme://host[:port]')
    if u.scheme != 'https' and not (allow_loopback and u.scheme == 'http' and u.hostname in ('127.0.0.1', 'localhost', '::1')):
        raise GateError('HTTPS required outside explicit loopback test')
    if u.port is not None and not 1 <= u.port <= 65535:
        raise GateError('invalid port')
    return urlunsplit((u.scheme, u.netloc, '', '', ''))

def expected_type(path):
    if path.endswith('.js'):
        return ('javascript', 'ecmascript')
    if path.endswith('.html'):
        return ('text/html',)
    if path.endswith('.json'):
        return ('application/json',)
    if path.endswith('.wasm'):
        return ('application/wasm',)
    return ()

def fetch(opener, origin, path, rec, max_bytes):
    url = origin + '/' + '/'.join(quote(part, safe='-._~') for part in path.split('/'))
    req = Request(url, headers={'Accept-Encoding': 'identity', 'Cache-Control': 'no-cache',
                                'Pragma': 'no-cache', 'User-Agent': 'WebManagerServedByteAudit/1'})
    try:
        with opener.open(req, timeout=20) as response:
            if response.status != 200 or response.geturl() != url:
                raise GateError('status or final URL mismatch: ' + path)
            encoding = response.headers.get('Content-Encoding', 'identity').lower().strip()
            if encoding not in ('identity', ''):
                raise GateError('content-encoding not identity: ' + path)
            media = response.headers.get('Content-Type', '').split(';', 1)[0].strip().lower()
            if expected_type(path) and not any(x in media for x in expected_type(path)):
                raise GateError('unexpected content type: ' + path + ' ' + media)
            if path in MUTABLE:
                cc = response.headers.get('Cache-Control', '').lower()
                if 'no-cache' not in cc and 'no-store' not in cc:
                    raise GateError('mutable entrypoint cache policy missing: ' + path)
            declared = response.headers.get('Content-Length')
            if declared is not None and (not declared.isdecimal() or int(declared) != rec['bytes']):
                raise GateError('Content-Length mismatch: ' + path)
            body = response.read(min(max_bytes, rec['bytes']) + 1)
            if len(body) != rec['bytes'] or sha256(body) != rec['sha256']:
                raise GateError('served bytes differ from receipt: ' + path)
            return {'path': path, 'sha256': sha256(body), 'status': response.status,
                    'contentType': media, 'cacheControl': response.headers.get('Cache-Control', ''),
                    'etag': response.headers.get('ETag', '')}
    except (HTTPError, URLError, TimeoutError, ssl.SSLError) as exc:
        raise GateError('HTTP transport failed: ' + path + ' ' + str(exc)) from exc

def audit(receipt_bytes, receipt_pin, origin, scope='critical', rounds=2,
          allow_loopback=False, max_bytes=64 * 1024 * 1024):
    files = validate_receipt(receipt_bytes, receipt_pin)
    base = origin_base(origin, allow_loopback)
    if rounds < 2 or rounds > 5:
        raise GateError('rounds must be 2..5')
    paths = sorted(files) if scope == 'all' else list(REQUIRED)
    if scope not in ('critical', 'all'):
        raise GateError('invalid scope')
    opener = build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context()), HTTPHandler())
    evidence = []
    for round_number in range(1, rounds + 1):
        for path in paths:
            result = fetch(opener, base, path, files[path], max_bytes)
            evidence.append({'round': round_number, **result})
    return {'verdict': 'HOST_TREE_MATCH_UNVERIFIED' if scope == 'all' else 'HOST_CRITICAL_MATCH_UNVERIFIED',
            'scope': scope, 'origin': base, 'rounds': rounds, 'checkedRequests': len(evidence),
            'receiptSha256': receipt_pin, 'observations': evidence}

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--receipt', type=Path, required=True)
    p.add_argument('--receipt-sha256', required=True)
    p.add_argument('--origin', required=True)
    p.add_argument('--scope', choices=('critical', 'all'), default='critical')
    p.add_argument('--rounds', type=int, default=2)
    p.add_argument('--allow-loopback-test', action='store_true')
    p.add_argument('--out', type=Path)
    args = p.parse_args(argv)
    try:
        result = audit(args.receipt.read_bytes(), args.receipt_sha256, args.origin,
                       args.scope, args.rounds, args.allow_loopback_test)
        payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
        if args.out:
            if args.out.exists():
                raise GateError('evidence output exists; refusing overwrite')
            args.out.write_text(payload)
        print(json.dumps({k: v for k, v in result.items() if k != 'observations'}))
        return 0
    except (GateError, OSError, ValueError) as exc:
        print(json.dumps({'verdict': 'HOLD', 'reason': str(exc)}), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
