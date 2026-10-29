#!/usr/bin/env python3
"""Synthetic Chrome origin-storage/UI-lock probe; NOT LogMate or a vulnerability exploit.

All values are invented and ephemeral. Distinguishes app UI gating from
origin-wide IndexedDB authorization, and from cross-origin/context isolation.
"""
import http.server
import json
import os
import threading
from playwright.sync_api import sync_playwright

CHROME = os.environ.get("CHROMIUM_PATH", "/usr/bin/google-chrome")
OUT = os.environ.get("EVIDENCE_OUT", "/tmp/pwa-owner-origin-evidence.json")
DB = "logmate_ledger"
KEY = "synthetic-only-key"
VALUE = "synthetic-only-value"

JS_WRITE = """async ({db, key, value}) => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(db, 1);
    request.onupgradeneeded = () => request.result.createObjectStore('ledger');
    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const database = request.result;
      const tx = database.transaction('ledger', 'readwrite');
      tx.objectStore('ledger').put(value, key);
      tx.oncomplete = () => {database.close(); resolve(true);};
      tx.onerror = () => reject(tx.error);
    };
  });
}"""
JS_READ = """async ({db, key}) => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(db, 1);
    request.onupgradeneeded = () => request.result.createObjectStore('ledger');
    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const database = request.result;
      const tx = database.transaction('ledger', 'readonly');
      const get = tx.objectStore('ledger').get(key);
      get.onsuccess = () => {const value = get.result ?? null; database.close(); resolve(value);};
      get.onerror = () => reject(get.error);
    };
  });
}"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass
    def do_GET(self):
        path = self.path.split("?")[0]
        if path not in ("/app", "/public", "/locked", "/"):
            self.send_response(404)
            self.end_headers()
            return
        body = ("""<!doctype html><html><head><meta charset="utf-8"></head>
        <body><h1>Fixture page</h1><p>Not LogMate.</p></body></html>""").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def start_server():
    server = Server(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"

def main():
    observations = []
    server_a, origin_a = start_server()
    server_b, origin_b = start_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
            context = browser.new_context()
            app = context.new_page()
            app.goto(origin_a + "/app")
            assert app.evaluate(JS_WRITE, {"db": DB, "key": KEY, "value": VALUE})
            assert app.evaluate(JS_READ, {"db": DB, "key": KEY}) == VALUE
            observations.append({"case": "APP_ORIGIN_IDB_WRITE_READ", "passed": True})

            # A route under the same origin can access the database without app UI approval.
            public = context.new_page()
            public.goto(origin_a + "/public")
            assert public.evaluate(JS_READ, {"db": DB, "key": KEY}) == VALUE
            observations.append({"case": "SAME_ORIGIN_PUBLIC_PATH_CAN_READ_IDB", "passed": True})

            # Simulated sign-out/route lock is not storage encryption or an IDB ACL.
            app.evaluate("localStorage.setItem('synthetic_ui_lock','locked')")
            app.goto(origin_a + "/locked")
            assert app.evaluate("localStorage.getItem('synthetic_ui_lock')") == "locked"
            assert app.evaluate(JS_READ, {"db": DB, "key": KEY}) == VALUE
            observations.append({"case": "SYNTHETIC_UI_LOCK_DOES_NOT_RESTRICT_IDB", "passed": True})

            # Different port => different origin, even with same hostname/database name.
            other = context.new_page()
            other.goto(origin_b + "/public")
            assert other.evaluate(JS_READ, {"db": DB, "key": KEY}) is None
            observations.append({"case": "DIFFERENT_ORIGIN_NO_SHARED_IDB", "passed": True})

            # Browser context/profile isolation is a separate boundary.
            separate = browser.new_context()
            separate_page = separate.new_page()
            separate_page.goto(origin_a + "/app")
            assert separate_page.evaluate(JS_READ, {"db": DB, "key": KEY}) is None
            observations.append({"case": "INDEPENDENT_CONTEXT_NO_SHARED_IDB", "passed": True})
            separate.close()

            # A lock marker stored on one origin is not inherited by a different origin.
            assert other.evaluate("localStorage.getItem('synthetic_ui_lock')") is None
            observations.append({"case": "DIFFERENT_ORIGIN_NO_SHARED_UI_LOCK", "passed": True})
            context.close()
            browser.close()
    finally:
        server_a.shutdown()
        server_b.shutdown()

    evidence = {
        "target": "SYNTHETIC_CHROME_ONLY",
        "not_product": True,
        "browser_executable": CHROME,
        "case_count": len(observations),
        "observations": observations,
        "limits": [
            "No real LogMate code, ledger, UID, MDM or authentication",
            "Same-origin scripted access is intentionally provided in fixture; no XSS found",
            "Different port tests browser origin isolation, not a production subdomain migration",
            "Chrome result cannot be transferred to Safari Home Screen or physical EFB"
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)
    print(json.dumps({"case_count": len(observations),
                      "passed": sum(x["passed"] for x in observations),
                      "target": "SYNTHETIC_CHROME_ONLY"}))
    assert len(observations) == 6

if __name__ == "__main__":
    main()
