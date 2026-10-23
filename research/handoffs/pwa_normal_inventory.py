#!/usr/bin/env python3
"""Review-only prototype for NORMAL PWA file-tree custody; not product release authority."""
import argparse
import hashlib
import json
import os
import stat
import sys
import unicodedata
from pathlib import Path


def inventory(root: Path):
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('root is not a directory')
    records = []
    seen = set()
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ValueError(f'symlink not allowed: {path}')
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise ValueError(f'special file not allowed: {path}')
            if name.startswith('.'):
                raise ValueError(f'hidden path needs explicit policy review: {path}')
        for name in files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            normalized = unicodedata.normalize('NFC', rel).casefold()
            if normalized in seen:
                raise ValueError(f'portable path collision: {rel}')
            seen.add(normalized)
            h = hashlib.sha256()
            count = 0
            with path.open('rb') as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(chunk)
                    count += len(chunk)
            records.append({'path': rel, 'bytes': count, 'sha256': h.hexdigest()})
    records.sort(key=lambda r: r['path'])
    if not records:
        raise ValueError('empty release tree')
    return records


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['create', 'verify'])
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--inventory', required=True, type=Path)
    p.add_argument('--source-sha', required=True)
    args = p.parse_args()
    if len(args.source_sha) != 40 or any(c not in '0123456789abcdef' for c in args.source_sha):
        raise ValueError('source-sha must be 40 lowercase hex chars')
    files = inventory(args.root)
    record = {'schemaVersion': 1, 'releaseMode': 'NORMAL', 'sourceSha': args.source_sha, 'files': files}
    if args.mode == 'create':
        if args.inventory.resolve() == args.root.resolve() or args.root.resolve() in args.inventory.resolve().parents:
            raise ValueError('inventory must be outside release tree')
        args.inventory.parent.mkdir(parents=True, exist_ok=True)
        args.inventory.write_text(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n', encoding='utf-8')
    else:
        expected = json.loads(args.inventory.read_text(encoding='utf-8'))
        if expected != record:
            raise ValueError('inventory mismatch (source, mode, path, size, or content)')
    print(f'{args.mode.upper()} PASS: {len(files)} files; source={args.source_sha}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f'RELEASE INVENTORY FAIL: {e}', file=sys.stderr)
        sys.exit(2)
