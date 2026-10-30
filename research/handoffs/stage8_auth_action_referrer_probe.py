"""Disposable, synthetic-only Chromium Referrer-Policy oracle; no Firebase or product access."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright

SENTINEL = "SYNTHETIC_NOT_A_REAL_ACTION_CODE"
requests = []
servers = []


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        requests.append((self.server.server_port, parsed.path, self.headers.get("Referer")))
        if parsed.path == "/auth/action":
            policy = parse_qs(parsed.query).get("policy", ["default"])[0]
            cross_port = servers[1].server_port
            body = ("<!doctype html><html><head><meta charset='utf-8'></head><body>"
                    "<img src='/asset.png' alt='same'>"
                    f"<img src='http://127.0.0.1:{cross_port}/cross.png' alt='cross'>"
                    "</body></html>").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            if policy in ("no-referrer", "strict-origin"):
                self.send_header("Referrer-Policy", policy)
        else:
            body = b"not-an-image"
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    for _ in range(2):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        servers.append(server)
        Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{servers[0].server_port}/"
    cases = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/google-chrome"),
                headless=True, args=["--no-sandbox"])
            try:
                for policy in ("default", "no-referrer", "strict-origin"):
                    before = len(requests)
                    url = f"{origin}auth/action?mode=resetPassword&oobCode={SENTINEL}&policy={policy}"
                    context = browser.new_context()
                    try:
                        context.new_page().goto(url, wait_until="networkidle")
                    finally:
                        context.close()
                    rows = requests[before:]
                    same = [ref for port, path, ref in rows if port == servers[0].server_port and path == "/asset.png"]
                    cross = [ref for port, path, ref in rows if port == servers[1].server_port and path == "/cross.png"]
                    assert len(same) == 1 and len(cross) == 1, f"missing resources in {policy}"
                    expected_same = url if policy == "default" else (None if policy == "no-referrer" else origin)
                    expected_cross = None if policy == "no-referrer" else origin
                    assert same[0] == expected_same, f"same-origin referrer mismatch: {policy}"
                    assert cross[0] == expected_cross, f"cross-origin referrer mismatch: {policy}"
                    cases.append({"policy": policy, "same_origin_query_exposed": bool(same[0] and SENTINEL in same[0]),
                                  "cross_origin_query_exposed": bool(cross[0] and SENTINEL in cross[0]),
                                  "expected_referrers_matched": True})
            finally:
                browser.close()
    finally:
        for server in servers:
            server.shutdown()
    evidence = {"scope": "SYNTHETIC Chromium only; not LogMate/HTTPS/Safari/MDM",
                "cases": cases, "passed_assertions": len(cases) * 2}
    out = os.environ.get("EVIDENCE_OUT")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
