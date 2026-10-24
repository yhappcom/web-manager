#!/usr/bin/env python3
"""Engineering handoff: read-only Chromium PWA first-claim/process-reopen probe.

This does NOT certify release, restore, Safari, EFB or production. Requires a
prebuilt NORMAL root, playwright and a local Chromium. Serves loopback only.
"""
import argparse
import functools
import hashlib
import http.server
import json
import pathlib
import re
import tempfile
import threading
from playwright.sync_api import sync_playwright

REQUIRED = ('index.html', 'main.dart.js', 'logmate_service_worker.js',
            'logmate-offline-manifest.json')

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

def inspect_asset(page):
    # Never copy a flight record, JS body, credential or other payload to evidence.
    return page.evaluate("""async () => {
      const r = await fetch('main.dart.js', {cache: 'no-store'});
      return {status: r.status, contentType: r.headers.get('content-type')};
    }""")

def launch(p, profile, chromium):
    opts = dict(user_data_dir=profile, headless=True, service_workers='allow',
                args=['--no-proxy-server', '--proxy-bypass-list=<-loopback>'])
    if chromium:
        opts['executable_path'] = chromium
    return p.chromium.launch_persistent_context(**opts)

def classify(o):
    """Fail closed on missing proof, invalid status types, or HTML masquerading as JS."""
    required_assets = ('first_claim_asset', 'controlled_asset', 'offline_asset', 'cold_process_asset')
    required_nav = ('initial_navigation_status', 'controlled_reload_status',
                    'offline_reload_status', 'cold_process_reopen_status')
    if o.get('controller_claimed') is not True or not isinstance(o.get('chromium_version'), str) or not o['chromium_version']:
        return 'INCOMPLETE_OR_ERROR'
    if not all(isinstance(o.get(k), dict) and type(o[k].get('status')) is int
               for k in required_assets) or not all(type(o.get(k)) is int for k in required_nav):
        return 'INCOMPLETE_OR_ERROR'
    if o['initial_navigation_status'] != 200:
        return 'INITIAL_NAVIGATION_FAILURE_OBSERVED'
    if o['first_claim_asset']['status'] != 200:
        return 'FIRST_CLAIM_ASSET_FAILURE_OBSERVED'
    if any(o[k]['status'] != 200 for k in required_assets[1:]) or any(o[k] != 200 for k in required_nav[1:]):
        return 'RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED'
    accepted = {'text/javascript', 'application/javascript', 'application/x-javascript'}
    if any(str(o[k].get('contentType') or '').split(';', 1)[0].strip().lower() not in accepted for k in required_assets):
        return 'ASSET_REPRESENTATION_MISMATCH_OBSERVED'
    return 'BOUNDED_CHROMIUM_PATH_PASS'

def probe(root, chromium, timeout_ms, source_sha):
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f'missing or unsafe NORMAL file: {name}')
    handler = functools.partial(QuietHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    result = {
        'classification': 'NOT_EXECUTED', 'source_sha_asserted_not_attested': source_sha,
        'worker_sha256_observed': hashlib.sha256((root / REQUIRED[2]).read_bytes()).hexdigest(),
        'origin_class': 'ephemeral_loopback', 'observations': {},
        'limitations': ['Not exact HTTPS Hosting', 'Not independently approved artifact',
                        'Chromium only', 'No Safari/managed iPad',
                        'No 37-store data/backup/Sync validation']}
    try:
        with tempfile.TemporaryDirectory(prefix='logmate-pwa-chrome-') as profile:
            with sync_playwright() as p:
                ctx = None
                try:
                    ctx = launch(p, profile, chromium)
                    result['observations']['chromium_version'] = ctx.browser.version if ctx.browser else 'unknown'
                    page = ctx.pages[0] if ctx.pages else ctx.new_page()
                    nav = page.goto(base, wait_until='domcontentloaded', timeout=timeout_ms)
                    result['observations']['initial_navigation_status'] = nav.status if nav else None
                    page.wait_for_function('!!navigator.serviceWorker?.controller', timeout=timeout_ms)
                    result['observations']['controller_claimed'] = True
                    result['observations']['first_claim_asset'] = inspect_asset(page)
                    nav = page.reload(wait_until='domcontentloaded', timeout=timeout_ms)
                    result['observations']['controlled_reload_status'] = nav.status if nav else None
                    result['observations']['controlled_asset'] = inspect_asset(page)
                    ctx.set_offline(True)
                    nav = page.reload(wait_until='domcontentloaded', timeout=timeout_ms)
                    result['observations']['offline_reload_status'] = nav.status if nav else None
                    result['observations']['offline_asset'] = inspect_asset(page)
                    ctx.set_offline(False)
                    ctx.close()
                    ctx = None
                    # Same browser profile, new Chromium process, network disabled.
                    ctx = launch(p, profile, chromium)
                    ctx.set_offline(True)
                    page = ctx.pages[0] if ctx.pages else ctx.new_page()
                    nav = page.goto(base, wait_until='domcontentloaded', timeout=timeout_ms)
                    result['observations']['cold_process_reopen_status'] = nav.status if nav else None
                    result['observations']['cold_process_asset'] = inspect_asset(page)
                    result['classification'] = classify(result['observations'])
                except Exception as exc:
                    message = str(exc)
                    result['classification'] = ('EXECUTION_ENVIRONMENT_BLOCKED'
                        if 'ERR_BLOCKED_BY_ADMINISTRATOR' in message
                        else 'INCOMPLETE_OR_ERROR')
                    result['error_type'] = type(exc).__name__
                    result['error_summary'] = message[:260]
                finally:
                    if ctx:
                        ctx.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=pathlib.Path)
    parser.add_argument('--chromium', help='path to local Chromium executable')
    parser.add_argument('--source-sha', required=True, help='operator-asserted 40-character commit')
    parser.add_argument('--timeout-ms', type=int, default=90000)
    parser.add_argument('--out', required=True, type=pathlib.Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}', args.source_sha):
        parser.error('--source-sha must be a 40-character lowercase SHA')
    if not 1000 <= args.timeout_ms <= 300000:
        parser.error('--timeout-ms outside allowed 1000–300000 range')
    root = args.root.resolve(strict=True)
    out = args.out.resolve()
    if out == root or root in out.parents:
        parser.error('output must be outside the artifact root')
    result = probe(root, args.chromium, args.timeout_ms, args.source_sha)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['classification'])
    return 0 if result['classification'] == 'BOUNDED_CHROMIUM_PATH_PASS' else 2

if __name__ == '__main__':
    raise SystemExit(main())
