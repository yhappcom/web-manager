#!/usr/bin/env python3
"""Exact-source-generated LogMate Worker, synthetic tiny manifest/HTTP assets.

Research-only: exercises the unmodified JS template extracted from pinned
tool/pwa_precache.dart; not a compiled Flutter NORMAL build or real deployment.
"""
import hashlib
import http.server
import json
import os
import socketserver
import threading
import urllib.request

from playwright.sync_api import sync_playwright

SOURCE_COMMIT = "2f78e731"
SOURCE_BLOB_SHA = "90a67954af618a4e18199fa92555491c56167c17"
SOURCE_URL = (
    "https://raw.githubusercontent.com/yhappcom/logmate/"
    + SOURCE_COMMIT + "/tool/pwa_precache.dart"
)
CHROME = os.environ.get("CHROMIUM_PATH", "/usr/bin/google-chrome")
OUT = os.environ.get("EVIDENCE_OUT", "/tmp/pwa-exact-worker-source-evidence.json")

ROOT = b"""<!doctype html><html><body><h1>Root shell</h1><script>
navigator.serviceWorker.register('/sw.js').then(() => navigator.serviceWorker.ready)
.then(() => document.body.dataset.registered = 'yes');
</script></body></html>"""
PUBLIC = b"""<!doctype html><html><head><link rel="stylesheet" href="/public.css"></head>
<body><h1>Account deletion</h1></body></html>"""
CSS_V1 = b"body { background-color: rgb(1, 2, 3); }"
CSS_V2 = b"body { background-color: rgb(4, 5, 6); }"
EXTRA = b"body { color: rgb(7, 8, 9); }"


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def extract_exact_worker():
    with urllib.request.urlopen(SOURCE_URL, timeout=20) as response:
        raw = response.read()
    actual = git_blob_sha(raw)
    assert actual == SOURCE_BLOB_SHA, ("source blob mismatch", actual)
    source = raw.decode("utf-8")
    anchor = source.index("String _workerSource(Map<String, Object> manifest)")
    start = source.index("return '''", anchor) + len("return '''")
    end = source.index("''';", start)
    template = source[start:end]
    assert template.count("$encoded") == 1
    assert "self.addEventListener('fetch'" in template
    assert "Offline version is not assigned" in template
    return template


def manifest_item(path, data):
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def generated_worker(template):
    manifest = {
        "schemaVersion": 2, "apiVersion": 2, "databaseCapability": 14,
        "appBuildId": "fixture-exact-v1", "fontSetId": "fixture-fonts-v1",
        "shell": [manifest_item("index.html", ROOT), manifest_item("public.css", CSS_V1)],
        "fonts": [], "fontNotices": [],
    }
    assert all(len(x["sha256"]) == 64 for x in manifest["shell"])
    # Dart's escaped interpolation markers must become JS template markers.
    worker = template.replace("$encoded", json.dumps(manifest))
    worker = worker.replace(chr(92) + chr(36) + "{", chr(36) + "{")
    assert "OFFLINE_MANIFEST = {" in worker
    assert "logmate-shell-" + chr(36) + "{" in worker
    return worker.encode("utf-8")


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def serve(worker_js):
    state = {"public_css": CSS_V1}

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            path = self.path.split("?")[0]
            routes = {
                "/": (ROOT, "text/html"),
                "/index.html": (ROOT, "text/html"),
                "/account-deletion/": (PUBLIC, "text/html"),
                "/auth/action/": (PUBLIC, "text/html"),
                "/public-extra.css": (EXTRA, "text/css"),
                "/api/ping": (b'{"ok":true}', "application/json"),
                "/__/health": (b'{"reserved":true}', "application/json"),
                "/sw.js": (worker_js, "application/javascript"),
            }
            if path == "/public.css":
                data, mime = state["public_css"], "text/css"
            elif path in routes:
                data, mime = routes[path]
            else:
                self.send_response(404)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, state, "http://127.0.0.1:%d" % server.server_port


def observed_fetch(page, path):
    return page.evaluate(
        """async path => {
            try {
              const r = await fetch(path);
              return {status:r.status, body:await r.text()};
            } catch(e) {return {status:"NETWORK_ERROR", body:String(e)};}
        }""", path
    )


def main():
    template = extract_exact_worker()
    server, state, base = serve(generated_worker(template))
    obs = []

    def record(label, actual, expected):
        assert actual == expected, (label, "expected", expected, "actual", actual)
        obs.append({"case": label, "observed": actual, "expected": expected})
        print(label, json.dumps(actual))

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=CHROME, headless=True, args=["--no-sandbox"]
            )
            context = browser.new_context()
            page = context.new_page()
            page.goto(base + "/account-deletion/", wait_until="load")
            record("P01_DIRECT_PUBLIC_CSS", page.evaluate(
                "getComputedStyle(document.body).backgroundColor"), "rgb(1, 2, 3)")
            preexisting = context.new_page()
            preexisting.goto(base + "/account-deletion/", wait_until="load")
            record("P15_PREEXISTING_PUBLIC_UNCONTROLLED", preexisting.evaluate(
                "!!navigator.serviceWorker.controller"), False)

            page.goto(base + "/", wait_until="load")
            page.wait_for_function("document.body.dataset.registered === 'yes'")
            page.wait_for_function("navigator.serviceWorker.controller !== null")
            page.reload(wait_until="load")
            preexisting.wait_for_function("navigator.serviceWorker.controller !== null")
            record("P16_PREEXISTING_PUBLIC_CLAIMED", preexisting.evaluate(
                "!!navigator.serviceWorker.controller"), True)
            record("P17_CLAIMED_PUBLIC_GET_UNASSIGNED",
                   observed_fetch(preexisting, "/api/ping")["status"], 503)
            record("P02_ROOT_CONTROLLED", page.evaluate(
                "!!navigator.serviceWorker.controller"), True)
            root_css = observed_fetch(page, "/public.css")
            record("P03_ASSIGNED_ROOT_CSS", root_css["status"], 200)
            record("P04_ASSIGNED_ROOT_BYTES", root_css["body"], CSS_V1.decode())

            # Server changes a URL while the verified v1 shell remains installed.
            state["public_css"] = CSS_V2
            root_css_after = observed_fetch(page, "/public.css")
            record("P05_VERIFIED_OLD_SHELL_PIN", root_css_after["body"], CSS_V1.decode())

            page.goto(base + "/account-deletion/", wait_until="load")
            record("P06_PUBLIC_HTML", page.locator("h1").inner_text(), "Account deletion")
            record("P07_PUBLIC_CSS_UNASSIGNED", page.evaluate(
                "getComputedStyle(document.body).backgroundColor"), "rgba(0, 0, 0, 0)")
            record("P08_UNLISTED_PUBLIC_FETCH_UNASSIGNED",
                   observed_fetch(page, "/public-extra.css")["status"], 503)
            record("P09_SAME_ORIGIN_API_UNASSIGNED",
                   observed_fetch(page, "/api/ping")["status"], 503)
            record("P10_RESERVED_HELPER_BYPASS",
                   observed_fetch(page, "/__/health")["status"], 200)

            other = context.new_page()
            responses = []
            other.on("response", lambda r: responses.append(
                (r.url.split(base)[-1], r.status)))
            other.goto(base + "/account-deletion/", wait_until="load")
            record("P11_NEW_TAB_CONTROLLED", other.evaluate(
                "!!navigator.serviceWorker.controller"), True)
            record("P12_NEW_TAB_PUBLIC_CSS", [status for path, status in responses
                   if path == "/public.css"][-1], 503)

            responses.clear()
            other.goto(base + "/auth/action/", wait_until="load")
            record("P13_RESERVED_AUTH_HTML", other.locator("h1").inner_text(),
                   "Account deletion")
            record("P14_RESERVED_AUTH_CSS", [status for path, status in responses
                   if path == "/public.css"][-1], 503)

            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    evidence = {
        "scope": "exact pinned LogMate Dart-generated Worker JS template; synthetic manifest/assets",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBlobSha": SOURCE_BLOB_SHA,
        "not": "compiled Flutter NORMAL, production Hosting, Safari, real account deletion, EFB",
        "observations": obs,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)
    assert len(obs) == 17
    print("17/17 source-generated synthetic Chrome assertions PASS")


if __name__ == "__main__":
    main()
