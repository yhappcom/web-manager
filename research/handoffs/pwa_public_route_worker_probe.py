#!/usr/bin/env python3
"""Synthetic Chrome test of a source-derived Service Worker routing boundary; not LogMate."""
import http.server
import json
import os
import socketserver
import threading
from playwright.sync_api import sync_playwright

CHROME = os.environ.get("CHROMIUM_PATH", "/usr/bin/google-chrome")
OUT = os.environ.get("EVIDENCE_OUT", "/tmp/pwa-public-route-evidence.json")
CSS = "body { background-color: rgb(1, 2, 3); }"

def worker(safe):
    return """
const SAFE = %s;
const clientBuilds = {};
self.addEventListener('install', e => e.waitUntil(self.skipWaiting()));
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;
  const relative = url.pathname.slice(1);
  if (relative === 'auth' || relative.startsWith('auth/') || relative.startsWith('__/')) return;
  if (SAFE && (relative === 'public.css' || relative.startsWith('icons/') || relative === 'favicon.png')) return;
  if (request.mode === 'navigate' && relative !== '') return;
  event.respondWith((async () => {
    let buildId;
    if (request.mode === 'navigate') {
      buildId = 'fixture-v1';
      for (const id of [event.clientId, event.resultingClientId]) if (id) clientBuilds[id] = buildId;
    } else buildId = clientBuilds[event.clientId];
    if (!buildId) return new Response('Offline version is not assigned; reload required.', {status: 503});
    return fetch(request);
  })());
});
""" % ("true" if safe else "false")

def serve(safe):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                data = b"""<!doctype html><html><head><link rel="stylesheet" href="/app.css"></head><body>ROOT<script>
navigator.serviceWorker.register('/sw.js').then(() => navigator.serviceWorker.ready)
.then(() => {document.body.dataset.ready='yes';});
</script></body></html>"""
                mime = "text/html"
            elif path in ("/account-deletion", "/account-deletion/"):
                data = b"""<!doctype html><html><head><link rel="stylesheet" href="/public.css"></head>
<body><h1>Account deletion</h1><p>Request deletion</p></body></html>"""
                mime = "text/html"
            elif path in ("/public.css", "/app.css"):
                data, mime = CSS.encode(), "text/css"
            elif path == "/sw.js":
                data, mime = worker(safe).encode(), "application/javascript"
            else:
                self.send_response(404); self.end_headers(); return
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
    class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True
    server = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, "http://127.0.0.1:%d" % server.server_port

def main():
    observations = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
        for safe in (False, True):
            server, base = serve(safe)
            try:
                context = browser.new_context()
                page = context.new_page()
                responses = []
                page.on("response", lambda r: responses.append({"path": r.url.split(base)[-1], "status": r.status}))
                page.goto(base + "/account-deletion/", wait_until="load")
                baseline = page.evaluate("getComputedStyle(document.body).backgroundColor")
                assert baseline == "rgb(1, 2, 3)", ("baseline", baseline)
                page.goto(base + "/", wait_until="load")
                page.wait_for_function("document.body.dataset.ready === 'yes'")
                page.wait_for_function("navigator.serviceWorker.controller !== null")
                page.reload(wait_until="load")
                assert page.evaluate("!!navigator.serviceWorker.controller")
                responses.clear()
                page.goto(base + "/account-deletion/", wait_until="load")
                controlled = page.evaluate("!!navigator.serviceWorker.controller")
                style = page.evaluate("getComputedStyle(document.body).backgroundColor")
                css_status = [r["status"] for r in responses if r["path"] == "/public.css"]
                html_status = [r["status"] for r in responses if r["path"] == "/account-deletion/"]
                assert controlled and html_status and html_status[-1] == 200, responses
                expected = 200 if safe else 503
                assert css_status and css_status[-1] == expected, (safe, css_status, responses)
                assert style == ("rgb(1, 2, 3)" if safe else "rgba(0, 0, 0, 0)"), style
                observations.append({"case": "SAFE" if safe else "SOURCE_DERIVED_UNSAFE",
                                     "controlled": controlled, "html": html_status[-1],
                                     "css": css_status[-1], "computedBackground": style})
                context.close()
            finally:
                server.shutdown(); server.server_close()
        browser.close()
    with open(OUT, "w", encoding="utf-8") as file:
        json.dump({"fixture": "synthetic source-derived; not LogMate compiled worker",
                   "observations": observations}, file, indent=2)
    print(json.dumps(observations, indent=2))
    print("2/2 controlled-route comparisons PASS (unsafe is intentional negative control)")

if __name__ == "__main__":
    main()
