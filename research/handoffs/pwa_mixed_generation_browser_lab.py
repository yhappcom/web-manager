#!/usr/bin/env python3
"""REAL Chromium / SYNTHETIC app lab for PWA mixed-generation browser boundaries.

Not LogMate, not Sembast, not an actual Flutter build, not a product/release PASS.
Uses localhost (secure-context exception), a disposable persistent browser profile,
plain IndexedDB and an intentionally aggressive synthetic Service Worker.

Run: python pwa_mixed_generation_browser_lab.py --chromium /usr/bin/chromium
Requires playwright Python package and installed Chromium executable.
"""
import argparse
import json
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

APP_JS = r"""
window.GENERATION = Number(new URL(document.currentScript.src).searchParams.get('generation'));
const DB_NAME = 'minttap-synthetic-mixed-generation';
const STORE = 'state';
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, 1); // native IDB version remains 1
    request.onupgradeneeded = () => request.result.createObjectStore(STORE);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
async function readState() {
  const db = await openDB();
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).get('ledger');
      req.onsuccess = () => resolve(req.result ?? null);
      req.onerror = () => reject(req.error);
    });
  } finally { db.close(); }
}
async function putState(updater, requireCapability) {
  const db = await openDB();
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite');
      let rejected = false;
      let value;
      const req = tx.objectStore(STORE).get('ledger');
      req.onsuccess = () => {
        const current = req.result ?? null;
        if (requireCapability && current?.capability !== window.GENERATION) {
          rejected = true;
          tx.abort();
          return;
        }
        value = updater(current);
        tx.objectStore(STORE).put(value, 'ledger');
      };
      tx.oncomplete = () => resolve(value);
      tx.onabort = () => reject(new Error(rejected ? 'CAPABILITY_VERSION_GUARD' : 'IDB_TRANSACTION_ABORT'));
      tx.onerror = () => {}; // onabort reports the transaction failure
    });
  } finally { db.close(); }
}
window.lab = {
  generation: () => window.GENERATION,
  init: () => putState(() => ({capability:16, payload:'initial', unsynced:2, remoteReceipts:0}), false),
  migrate: () => putState(s => ({...s, capability:17}), false),
  read: readState,
  guarded: () => putState(s => ({...s, payload:'stale-guarded'}), true),
  unsafe: () => putState(s => ({...s, payload:'stale-unsafe'}), false),
  register: async () => {
    const r = await navigator.serviceWorker.register('/sw.js', {scope:'/'});
    await navigator.serviceWorker.ready;
    return r.scope;
  },
  updateWorker: async () => {const r = await navigator.serviceWorker.getRegistration('/'); await r.update();},
  workerVersion: async () => (await fetch('/worker-version', {cache:'no-store'})).text(),
  controller: () => !!navigator.serviceWorker.controller,
  nativeIdbVersion: async () => {const d=await openDB();const v=d.version;d.close();return v;},
};
"""

class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address):
        super().__init__(address, LabHandler)
        self.worker_version = 1

class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path in ('/old/', '/new/'):
            generation = 16 if path == '/old/' else 17
            body = f'<!doctype html><meta charset="utf-8"><title>Synthetic {generation}</title><script src="/app.js?generation={generation}"></script>'.encode()
            kind = 'text/html'
        elif path == '/app.js':
            body, kind = APP_JS.encode(), 'application/javascript'
        elif path == '/sw.js':
            v = self.server.worker_version
            body = (f"const V={v};self.addEventListener('install',e=>e.waitUntil(self.skipWaiting()));"
                    "self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));"
                    "self.addEventListener('fetch',e=>{if(new URL(e.request.url).pathname==='/worker-version')"
                    "e.respondWith(new Response('worker-v'+V,{headers:{'content-type':'text/plain'}}));});").encode()
            kind = 'application/javascript'
        elif path == '/worker-version':
            body, kind = b'network-uncontrolled', 'text/plain'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', kind)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def run(chromium_path: str):
    server = LabServer(('127.0.0.1', 0))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    evidence = {'classification': 'REAL_CHROMIUM_SYNTHETIC_MODEL_ONLY', 'origin_class': 'loopback_ephemeral_port',
                'checks': [], 'limitations': ['plain IndexedDB, not Sembast Web',
                'synthetic JavaScript, not Flutter/LogMate',
                'synthetic skipWaiting/clients.claim, not LogMate Worker',
                'normal browser restart, not power-loss or storage eviction',
                'localhost secure-context exception, not production HTTPS']}
    def record(label, result):
        require(result, label)
        evidence['checks'].append(label)
    try:
        with tempfile.TemporaryDirectory(prefix='pwa-lab-profile-') as profile:
            with sync_playwright() as p:
                ctx = p.chromium.launch_persistent_context(
                    profile, executable_path=chromium_path, headless=True,
                    service_workers='allow')
                old = ctx.new_page()
                old.goto(base+'/old/')
                old.wait_for_function('window.lab !== undefined')
                record('old_js_generation_16', old.evaluate('lab.generation()') == 16)
                record('origin_is_secure_context', old.evaluate('isSecureContext') is True)
                old.evaluate('lab.init()')
                old.evaluate('lab.register()')
                old.wait_for_function('navigator.serviceWorker.controller !== null')
                record('worker_v1_controls_old_tab', old.evaluate('lab.workerVersion()') == 'worker-v1')
                new = ctx.new_page()
                new.goto(base+'/new/')
                new.wait_for_function('window.lab !== undefined')
                record('new_js_generation_17', new.evaluate('lab.generation()') == 17)
                record('shared_origin_idb_before_migration', new.evaluate('lab.read()')['capability'] == 16)
                new.evaluate('lab.migrate()')
                record('logical_capability_17', new.evaluate('lab.read()')['capability'] == 17)
                record('native_idb_version_unchanged_1', old.evaluate('lab.nativeIdbVersion()') == 1)
                before = new.evaluate('lab.read()')
                guard = old.evaluate("async () => {try {await lab.guarded();return 'UNEXPECTED_WRITE'} catch(e){return e.message}}")
                after = new.evaluate('lab.read()')
                record('old_guarded_write_rejected', guard == 'CAPABILITY_VERSION_GUARD')
                record('guarded_write_no_mutation', before == after)
                server.worker_version = 2
                new.evaluate('lab.updateWorker()')
                old.wait_for_function("async () => (await lab.workerVersion()) === 'worker-v2'", timeout=10000)
                record('worker_v2_controls_old_tab', old.evaluate('lab.workerVersion()') == 'worker-v2')
                record('worker_update_did_not_replace_old_js', old.evaluate('lab.generation()') == 16)
                old.evaluate('lab.unsafe()')
                mutated = new.evaluate('lab.read()')
                record('intentionally_unsafe_old_write_mutates_shared_db', mutated['payload'] == 'stale-unsafe')
                record('unsafe_write_keeps_logical_marker_17', mutated['capability'] == 17)
                record('synthetic_remote_receipt_not_invented', mutated['remoteReceipts'] == 0 and mutated['unsynced'] == 2)
                ctx.close()  # launchPersistentContext.close closes browser
                ctx2 = p.chromium.launch_persistent_context(
                    profile, executable_path=chromium_path, headless=True,
                    service_workers='allow')
                reopened = ctx2.new_page()
                reopened.goto(base+'/new/')
                reopened.wait_for_function('window.lab !== undefined')
                readback = reopened.evaluate('lab.read()')
                record('new_browser_same_profile_readback', readback == mutated)
                record('restarted_browser_native_idb_version_1', reopened.evaluate('lab.nativeIdbVersion()') == 1)
                ctx2.close()
        evidence['verdict'] = 'BROWSER_LAB_PASS_NOT_PRODUCT_PASS'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = run(args.chromium)
    except Exception as exc:
        result = {'verdict': 'BROWSER_LAB_FAILED', 'error_type': type(exc).__name__, 'message': str(exc)}
    data = json.dumps(result, ensure_ascii=False, indent=2)
    print(data)
    if args.output:
        args.output.write_text(data+'\n', encoding='utf-8')
    return 0 if result['verdict'] == 'BROWSER_LAB_PASS_NOT_PRODUCT_PASS' else 2

if __name__ == '__main__':
    raise SystemExit(main())
