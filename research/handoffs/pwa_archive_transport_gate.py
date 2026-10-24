#!/usr/bin/env python3
"""Fail-closed read-only ZIP transport audit for a pinned NORMAL PWA receipt.

No extraction, network access, release authorization, or product runtime execution.
The expected archive and receipt SHA-256 values MUST originate outside the
artifact/receipt trust domain; CLI values alone are not an attestation.
"""
import argparse
import hashlib
import json
import re
import stat
import sys
import unicodedata
import zipfile
import zlib
from pathlib import Path

HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
DRIVE = re.compile(r'^[a-zA-Z]:')
REQUIRED = ('index.html', 'flutter_bootstrap.js', 'main.dart.js',
            'logmate_service_worker.js', 'logmate-offline-manifest.json',
            'manifest.json', 'canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm')
MAX_ENTRIES = 12000
MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 2 * 1024 * 1024 * 1024
MAX_RATIO = 1000
MAX_RECEIPT = 16 * 1024 * 1024
CHUNK = 1024 * 1024

class GateError(ValueError):
    pass

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(CHUNK), b''):
            h.update(block)
    return h.hexdigest()

def safe_path(path, directory=False):
    if not isinstance(path, str) or not path or '\\' in path or '\x00' in path or '%' in path:
        raise GateError('unsafe archive path')
    if path.startswith('/') or DRIVE.match(path) or unicodedata.normalize('NFC', path) != path:
        raise GateError('noncanonical archive path')
    raw = path[:-1] if directory and path.endswith('/') else path
    parts = raw.split('/')
    if not parts or any(p in ('', '.', '..') or p.endswith((' ', '.')) or ':' in p
                        or any(ord(c) < 32 or ord(c) == 127 for c in p) for p in parts):
        raise GateError('unsafe archive component')
    return raw

def validate_receipt(receipt, source):
    if not isinstance(receipt, dict) or receipt.get('schema') != 1 or receipt.get('kind') != 'normal':
        raise GateError('not a NORMAL schema-1 receipt')
    if not HEX40.fullmatch(source) or receipt.get('sourceSha') != source:
        raise GateError('source identity mismatch')
    files = receipt.get('files')
    if not isinstance(files, dict) or not files or len(files) > MAX_ENTRIES:
        raise GateError('invalid file inventory')
    if type(receipt.get('fileCount')) is not int or receipt['fileCount'] != len(files):
        raise GateError('file count mismatch')
    folded = set()
    total = 0
    for path, item in files.items():
        safe_path(path)
        key = path.casefold()
        if key in folded:
            raise GateError('casefold collision in receipt')
        folded.add(key)
        if not isinstance(item, dict) or type(item.get('bytes')) is not int or item['bytes'] < 0 or item['bytes'] > MAX_FILE or not isinstance(item.get('sha256'), str) or not HEX64.fullmatch(item['sha256']):
            raise GateError('invalid receipt file record')
        total += item['bytes']
    for path in files:
        parts = path.split('/')
        if any('/'.join(parts[:i]) in files for i in range(1, len(parts))):
            raise GateError('file/directory prefix collision in receipt')
    if total > MAX_TOTAL or any(p not in files for p in REQUIRED):
        raise GateError('receipt exceeds limits or missing critical file')
    for key, name in [('workerSha256', 'logmate_service_worker.js'),
                      ('manifestSha256', 'logmate-offline-manifest.json')]:
        if receipt.get(key) != files[name]['sha256']:
            raise GateError('receipt independent digest mismatch: ' + key)
    if not isinstance(receipt.get('treeSha256'), str) or not HEX64.fullmatch(receipt['treeSha256']):
        raise GateError('invalid tree hash')
    canonical = json.dumps(files, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    if sha(canonical) != receipt['treeSha256']:
        raise GateError('receipt tree hash mismatch')
    return files

def audit(archive, receipt_path, archive_pin, receipt_pin, source):
    if not HEX64.fullmatch(archive_pin) or not HEX64.fullmatch(receipt_pin):
        raise GateError('both independent SHA-256 pins are required')
    if not archive.is_file() or archive.is_symlink() or not receipt_path.is_file() or receipt_path.is_symlink():
        raise GateError('archive and receipt must be regular files')
    if receipt_path.stat().st_size > MAX_RECEIPT or archive.stat().st_size > MAX_TOTAL:
        raise GateError('input exceeds physical size limits')
    if file_sha(archive) != archive_pin or file_sha(receipt_path) != receipt_pin:
        raise GateError('independent pin mismatch')
    try:
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    except (UnicodeError, ValueError) as exc:
        raise GateError('malformed receipt') from exc
    files = validate_receipt(receipt, source)
    observed = set()
    folded = set()
    declared_total = 0
    try:
        with zipfile.ZipFile(archive) as zf:
            entries = zf.infolist()
            if len(entries) > MAX_ENTRIES:
                raise GateError('too many archive entries')
            for entry in entries:
                is_dir = entry.is_dir()
                path = safe_path(entry.filename, directory=is_dir)
                folded_key = path.casefold()
                if folded_key in folded:
                    raise GateError('duplicate/casefold archive entry')
                folded.add(folded_key)
                mode = (entry.external_attr >> 16) & 0xffff
                if entry.create_system == 3:
                    kind = stat.S_IFMT(mode)
                    if kind not in (0, stat.S_IFDIR if is_dir else stat.S_IFREG):
                        raise GateError('symlink or special ZIP member')
                if entry.flag_bits & 1 or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise GateError('encrypted or unsupported ZIP member')
                if is_dir:
                    if entry.file_size:
                        raise GateError('directory with data')
                    continue
                if path not in files:
                    raise GateError('unexpected archive file: ' + path)
                if entry.file_size > MAX_FILE or entry.file_size != files[path]['bytes']:
                    raise GateError('file size mismatch')
                if entry.file_size > 0 and entry.file_size / max(1, entry.compress_size) > MAX_RATIO:
                    raise GateError('excessive expansion ratio')
                declared_total += entry.file_size
                if declared_total > MAX_TOTAL:
                    raise GateError('total expansion limit exceeded')
                h = hashlib.sha256()
                size = 0
                with zf.open(entry) as src:
                    for block in iter(lambda: src.read(CHUNK), b''):
                        size += len(block)
                        if size > entry.file_size or size > MAX_FILE:
                            raise GateError('stream exceeded declared size')
                        h.update(block)
                if size != entry.file_size or h.hexdigest() != files[path]['sha256']:
                    raise GateError('archive content digest mismatch: ' + path)
                observed.add(path)
    except (zipfile.BadZipFile, zipfile.LargeZipFile, zlib.error, NotImplementedError, RuntimeError, EOFError, OSError) as exc:
        raise GateError('unreadable or corrupt ZIP') from exc
    if observed != set(files):
        raise GateError('missing archived files')
    return {'verdict': 'ARCHIVE_BYTES_MATCH_UNVERIFIED', 'kind': 'normal',
            'sourceSha': source, 'fileCount': len(observed),
            'archiveSha256': archive_pin, 'receiptSha256': receipt_pin,
            'treeSha256': receipt['treeSha256'], 'workerSha256': receipt['workerSha256'],
            'limitations': 'No G3 approval, re-run of 509 semantic disk verifier, host, browser or device proof'}

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--receipt', type=Path, required=True)
    p.add_argument('--archive-sha256', required=True)
    p.add_argument('--receipt-sha256', required=True)
    p.add_argument('--source-sha', required=True)
    p.add_argument('--out', type=Path)
    args = p.parse_args(argv)
    try:
        result = audit(args.archive, args.receipt, args.archive_sha256, args.receipt_sha256, args.source_sha)
        output = json.dumps(result, sort_keys=True)
        if args.out:
            if args.out.resolve() in (args.archive.resolve(), args.receipt.resolve()):
                raise GateError('cannot overwrite evidence input')
            args.out.write_text(output + '\n', encoding='utf-8')
        print(output)
        return 0
    except (GateError, OSError) as exc:
        print('HOLD: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
