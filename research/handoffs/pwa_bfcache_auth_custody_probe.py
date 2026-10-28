#!/usr/bin/env python3
"""Research-only bfcache/privacy probe. Synthetic state and content; no LogMate code/data."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

state = {"authenticated": True, "unreachable": False}
HTML = """<!doctype html><meta charset="utf-8"><title>synthetic ledger</title>
<h1 id="secret">LOCKED</h1><script>
const guarded = new URLSearchParams(location.search).get('guard') === '1';
window.trace = [];
async function verify() {
  try {
    const response = await fetch('/state', {cache:'reload'});
    if (!response.ok) throw new Error('unreachable');
    const state = await response.json();
    document.querySelector('#secret').textContent =
      state.authenticated ? 'SYNTHETIC PRIVATE LEDGER' : 'LOCKED';
    trace.push(['verify', state.authenticated]);
  } catch (e) {
    document.querySelector('#secret').textContent = 'LOCKED';
    trace.push(['verify', 'unknown']);
  }
}
addEventListener('pageshow', event => {
  trace.push(['pageshow', event.persisted]);
  if (guarded && event.persisted) verify();
});
addEventListener('pagehide', event => {
  trace.push(['pagehide', event.persisted]);
  if (guarded) document.querySelector('#secret').textContent = 'LOCKED';
});
verify();
</script>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/state":
            if state["unreachable"]:
                self.send_response(503)
                body = b"unavailable"
            else:
                self.send_response(200)
                body = json.dumps({"authenticated": state["authenticated"]}).encode()
            mime = "application/json"
        elif path == "/app":
            self.send_response(200)
            body = HTML.encode()
            mime = "text/html"
        elif path == "/neutral":
            self.send_response(200)
            body = b"<!doctype html><h1>Neutral navigation</h1>"
            mime = "text/html"
        else:
            self.send_response(404)
            body = b"missing"
            mime = "text/plain"
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "public, max-age=600" if path in ("/app","/neutral") else "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass

def run_case(browser, base, name, guarded, after_auth, unreachable, expected):
    state.update(authenticated=True, unreachable=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto(base + ("/app?guard=1" if guarded else "/app?guard=0"))
        page.wait_for_function("document.querySelector('#secret').textContent === 'SYNTHETIC PRIVATE LEDGER'")
        page.goto(base + "/neutral")
        state.update(authenticated=after_auth, unreachable=unreachable)
        page.go_back(wait_until="load")
        page.wait_for_function("window.trace && trace.some(e => e[0] === 'pageshow')")
        # The page may have been restored or reloaded. A reloaded page is not
        # evidence of the bfcache hazard or its mitigation.
        page.wait_for_timeout(200)
        trace = page.evaluate("window.trace")
        navigation = page.evaluate("""() => { const n=performance.getEntriesByType('navigation')[0]; return {type:n?.type, notRestoredReasons:n?.notRestoredReasons ?? null}; }""")
        restored = any(x == ["pageshow", True] for x in trace)
        observed = page.locator("#secret").inner_text()
        passed = restored and observed == expected
        return {"case":name, "passed":passed, "bfcache_restored":restored,
                "observed":observed, "expected":expected, "trace":trace, "navigation":navigation}
    finally:
        context.close()

def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:" + str(server.server_port)
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
                headless=True, args=["--no-sandbox"])
            version = browser.version
            cases = [
                ("BF01_UNSAFE_STALE_AFTER_SIGNOUT", False, False, False, "SYNTHETIC PRIVATE LEDGER"),
                ("BF02_GUARDED_SIGNOUT", True, False, False, "LOCKED"),
                ("BF03_GUARDED_UNREACHABLE", True, True, True, "LOCKED"),
                ("BF04_GUARDED_SAME_OWNER", True, True, False, "SYNTHETIC PRIVATE LEDGER"),
            ]
            for case in cases:
                result = run_case(browser, base, *case)
                results.append(result)
                print(json.dumps(result))
            browser.close()
    finally:
        server.shutdown()
    report = {"kind":"synthetic-chrome-bfcache-not-product",
              "browser_version":version, "cases":results,
              "passed":sum(x["passed"] for x in results),
              "total":len(results)}
    path = os.environ.get("EVIDENCE_OUT", "/tmp/pwa-bfcache-evidence.json")
    with open(path,"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2)
    print("RESULT",report["passed"],"/",report["total"])
    if report["passed"] != report["total"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
