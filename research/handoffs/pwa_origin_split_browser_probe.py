#!/usr/bin/env python3
"""Research-only Chromium origin/path/redirect/worker/cookie/bridge probe. No LogMate code or data."""
import http.server
import json
import os
import socketserver
import threading
from playwright.sync_api import sync_playwright

CHROME = os.getenv("CHROMIUM_PATH", "/usr/bin/google-chrome")
OUT = os.getenv("EVIDENCE_OUT", "/tmp/pwa-origin-split-evidence.json")

class ThreadServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def start_server(label, peer_ref):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/move":
                self.send_response(302)
                self.send_header("Location", peer_ref["url"] + "/public")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                return
            if path == "/sw.js":
                body = b"self.addEventListener('install',e=>e.waitUntil(self.skipWaiting()));self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));"
                mime = "application/javascript"
            elif path == "/manifest.json":
                body = json.dumps({"name": "Synthetic PWA " + label, "start_url": ".", "display": "standalone"}).encode()
                mime = "application/manifest+json"
            elif path in ("/app", "/public", "/frame"):
                body = ("<!doctype html><html><head><meta charset='utf-8'><title>" + label + "</title></head><body>" + label + "</body></html>").encode()
                mime = "text/html"
            else:
                self.send_response(404)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
    server = ThreadServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, "http://127.0.0.1:%d" % server.server_port

SEED = """async () => {
 const db=await new Promise((resolve,reject)=>{const r=indexedDB.open('pilot-fixture',1);r.onupgradeneeded=()=>r.result.createObjectStore('records');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 await new Promise((resolve,reject)=>{const tx=db.transaction('records','readwrite');tx.objectStore('records').put('synthetic-only','entry');tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)});db.close();
 await (await caches.open('fixture-shell')).put('/fixture-entry',new Response('synthetic-shell'));
 document.cookie='fixture_cookie=shared_across_ports; Path=/; SameSite=Lax';
 return {origin:location.origin,dbs:(await indexedDB.databases()).map(d=>d.name),caches:await caches.keys(),cookie:document.cookie};
}"""
READ = """async () => {
 const db=await new Promise((resolve,reject)=>{const r=indexedDB.open('pilot-fixture');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 const stores=Array.from(db.objectStoreNames);let value=null;
 if(stores.includes('records'))value=await new Promise((resolve,reject)=>{const tx=db.transaction('records');const r=tx.objectStore('records').get('entry');r.onsuccess=()=>resolve(r.result||null);r.onerror=()=>reject(r.error)});
 db.close();return {stores,value};
}"""

def main():
    peer = {"url": ""}
    old_server, old = start_server("old-private-origin", peer)
    new_server, new = start_server("new-public-origin", {"url": old})
    peer["url"] = new
    observations = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
            context = browser.new_context()
            page = context.new_page()
            page.goto(old + "/app")
            seeded = page.evaluate(SEED)
            assert seeded["origin"] == old and "pilot-fixture" in seeded["dbs"]
            assert "fixture-shell" in seeded["caches"]
            observations.append({"case": "OLD_ORIGIN_SEED", "result": "seeded synthetic IndexedDB and CacheStorage"})
            page.goto(old + "/public")
            assert page.evaluate(READ)["value"] == "synthetic-only"
            observations.append({"case": "PATH_ONLY_PUBLIC_READS_PRIVATE_IDB", "result": "same-origin path reads synthetic record"})
            page.goto(new + "/public")
            before = page.evaluate("indexedDB.databases().then(d=>d.map(x=>x.name))")
            assert "pilot-fixture" not in before, before
            assert "fixture-shell" not in page.evaluate("caches.keys()")
            observations.append({"case": "NEW_ORIGIN_NO_IDB_OR_CACHE_COPY", "result": "both absent"})
            cookie = page.evaluate("document.cookie")
            assert "fixture_cookie=shared_across_ports" in cookie, cookie
            observations.append({"case": "COOKIE_SCOPE_DIFFERS_FROM_ORIGIN", "result": "cookie shared across ports on same host"})
            try:
                page.evaluate("url=>navigator.serviceWorker.register(url)", old + "/sw.js")
                raise AssertionError("cross-origin service worker registration unexpectedly succeeded")
            except Exception as exc:
                if isinstance(exc, AssertionError): raise
                assert "SecurityError" in str(exc), str(exc)
            observations.append({"case": "CROSS_ORIGIN_WORKER_REGISTRATION_REJECTED", "result": "SecurityError"})
            page.goto(old + "/app")
            page.evaluate("async()=>{await navigator.serviceWorker.register('/sw.js',{scope:'/'});await navigator.serviceWorker.ready}")
            page.wait_for_function("navigator.serviceWorker.controller !== null")
            assert page.evaluate("!!navigator.serviceWorker.controller")
            observations.append({"case": "OLD_WORKER_CONTROLS_OLD", "result": "controlled"})
            page.goto(new + "/public")
            assert not page.evaluate("!!navigator.serviceWorker.controller")
            observations.append({"case": "OLD_WORKER_DOES_NOT_CONTROL_NEW", "result": "uncontrolled"})
            page.goto(old + "/move")
            assert page.url == new + "/public", page.url
            assert "pilot-fixture" not in page.evaluate("indexedDB.databases().then(d=>d.map(x=>x.name))")
            observations.append({"case": "REDIRECT_DOES_NOT_TRANSFER_IDB", "result": "new origin remains empty"})
            page.goto(old + "/app")
            assert page.evaluate(READ)["value"] == "synthetic-only"
            observations.append({"case": "OLD_SOURCE_SURVIVES_REDIRECT", "result": "record retained"})
            page.evaluate("""peer=>{
              window.__accepted=[];window.addEventListener('message',e=>{if(e.origin===peer)window.__accepted.push(e.data)});
              const f=document.createElement('iframe');f.id='peer';f.src=peer+'/frame';document.body.appendChild(f);
            }""", new)
            page.frame_locator("#peer").locator("body").wait_for()
            frame = page.frame(url=new + "/frame")
            assert frame is not None
            frame.evaluate("target=>window.parent.postMessage({kind:'allowed-synthetic'},target)", old)
            page.wait_for_function("window.__accepted.length === 1")
            page.evaluate("window.postMessage({kind:'spoofed-origin'}, '*')")
            page.wait_for_timeout(100)
            accepted = page.evaluate("window.__accepted")
            assert len(accepted) == 1 and accepted[0]["kind"] == "allowed-synthetic", accepted
            observations.append({"case": "POSTMESSAGE_ORIGIN_CHECK", "result": "expected sender accepted, same-window spoof ignored"})
            page.goto(new + "/public")
            assert "pilot-fixture" not in page.evaluate("indexedDB.databases().then(d=>d.map(x=>x.name))")
            observations.append({"case": "MESSAGE_HANDSHAKE_IS_NOT_LEDGER_RESTORE", "result": "new IDB still absent"})
            for origin in (old, new):
                page.goto(origin + "/public")
                manifest = page.evaluate("""async()=>{const u=new URL('/manifest.json',location.href);const m=await(await fetch(u)).json();return {start:new URL(m.start_url,u).href,hasId:Object.hasOwn(m,'id'),hasScope:Object.hasOwn(m,'scope')}}""")
                assert manifest == {"start": origin + "/", "hasId": False, "hasScope": False}, manifest
            observations.append({"case": "RELATIVE_MANIFEST_RESOLVES_PER_ORIGIN", "result": "different derived start URLs; not installed-app identity proof"})
            context.close()
            version = browser.version
            browser.close()
        assert len(observations) == 12, len(observations)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump({"scope": "synthetic loopback Chromium; not LogMate, Safari, installed PWA or EFB", "browser": version, "old": "port-A", "new": "port-B", "observations": observations}, f, indent=2)
        print(json.dumps({"browser": version, "observations": observations}, indent=2))
        print("12/12 synthetic origin-split checks PASS")
    finally:
        old_server.shutdown(); old_server.server_close()
        new_server.shutdown(); new_server.server_close()

if __name__ == "__main__":
    main()
