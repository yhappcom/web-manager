#!/usr/bin/env python3
"""Synthetic browser CORS/admission probe. No LogMate or production credentials."""
import hashlib
import json
import os
import platform
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

TOKEN = "synthetic-browser-probe-token"
OUTPUT = Path(os.environ.get("EVIDENCE_OUT", "/tmp/pwa-cors-admission-evidence.json"))


class State:
    good_origin = ""
    receipt_value = "v1"
    requests = None
    receipts = None

    def __init__(self):
        self.requests = []
        self.receipts = {}


state = State()


def digest(op_id, value):
    return hashlib.sha256(("fixture-v1|" + op_id + "|" + value).encode("utf-8")).hexdigest()


def op(op_id, value):
    return {"id": op_id, "value": value, "digest": digest(op_id, value)}


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/sw.js":
            body = b"""self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  if (new URL(e.request.url).pathname !== '/api-receipt') return;
  e.respondWith((async () => {
    const cache = await caches.open('synthetic-unsafe-receipt');
    const hit = await cache.match(e.request);
    if (hit) return hit;
    const response = await fetch(e.request);
    await cache.put(e.request, response.clone());
    return response;
  })());
});"""
            mime = "text/javascript; charset=utf-8"
        elif self.path == "/api-receipt":
            body = json.dumps({"value": state.receipt_value}).encode()
            mime = "application/json"
        else:
            body = b"<!doctype html><title>Disposable PWA API origin probe</title>"
            mime = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        if self.path == "/api-receipt":
            self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


class APIHandler(BaseHTTPRequestHandler):
    def headers_for(self, origin):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Vary", "Origin")
        if origin == state.good_origin:
            self.send_header("Access-Control-Allow-Origin", origin)

    def reply(self, status, data, origin):
        body = json.dumps(data, separators=(",", ":")).encode()
        self.send_response(status)
        self.headers_for(origin)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def record(self, method):
        state.requests.append({
            "method": method,
            "origin": self.headers.get("Origin"),
            "authorization_present": bool(self.headers.get("Authorization")),
            "requested_headers": self.headers.get("Access-Control-Request-Headers", ""),
        })

    def do_OPTIONS(self):
        self.record("OPTIONS")
        origin = self.headers.get("Origin")
        requested = {
            x.strip().lower() for x in
            self.headers.get("Access-Control-Request-Headers", "").split(",") if x.strip()
        }
        if origin != state.good_origin or not requested.issubset({"authorization", "content-type"}):
            self.reply(403, {"error": "preflight denied"}, origin)
            return
        self.send_response(204)
        self.headers_for(origin)
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "authorization, content-type")
        self.send_header("Access-Control-Max-Age", "0")
        self.end_headers()

    def do_POST(self):
        self.record("POST")
        origin = self.headers.get("Origin")
        if origin is not None and origin != state.good_origin:
            self.reply(403, {"error": "origin denied"}, origin)
            return
        if self.headers.get("Authorization") != "Bearer " + TOKEN:
            self.reply(401, {"error": "unauthorized"}, origin)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 1024:
                self.reply(413, {"error": "size"}, origin)
                return
            body = json.loads(self.rfile.read(length))
            if (set(body) != {"id", "value", "digest"} or
                not isinstance(body["id"], str) or
                not isinstance(body["value"], str) or
                body["digest"] != digest(body["id"], body["value"])):
                self.reply(400, {"error": "bad payload"}, origin)
                return
            existing = state.receipts.get(body["id"])
            if existing is not None:
                if existing != body["digest"]:
                    self.reply(409, {"error": "conflict"}, origin)
                else:
                    self.reply(200, {"status": "REPLAY"}, origin)
                return
            state.receipts[body["id"]] = body["digest"]
            self.reply(200, {"status": "ACCEPTED"}, origin)
        except (ValueError, TypeError, KeyError):
            self.reply(400, {"error": "invalid json"}, origin)

    def log_message(self, *_):
        pass


def start(handler):
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def raw_post(url, body, bearer=None, origin=None):
    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "Bearer " + bearer
    if origin is not None:
        headers["Origin"] = origin
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


FETCH = """async ({url, body, token, extra}) => {
  try {
    const headers = {'content-type': 'application/json'};
    if (token !== null) headers.authorization = 'Bearer ' + token;
    if (extra) headers['x-extra'] = '1';
    const response = await fetch(url, {
      method: 'POST', mode: 'cors', credentials: 'omit',
      cache: 'no-store', headers, body: JSON.stringify(body)
    });
    return {status: response.status, body: await response.json(),
            cacheControl: response.headers.get('cache-control')};
  } catch (error) {
    return {networkError: true, name: error.name};
  }
}"""


def main():
    good = start(AppHandler)
    bad = start(AppHandler)
    api = start(APIHandler)
    state.good_origin = f"http://127.0.0.1:{good.server_port}"
    bad_origin = f"http://127.0.0.1:{bad.server_port}"
    endpoint = f"http://127.0.0.1:{api.server_port}/admit"
    checks = []

    def check(name, passed, observation):
        checks.append({"id": name, "passed": bool(passed), "observation": observation})
        print(f"{name} {'PASS' if passed else 'FAIL'}: {observation}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                executable_path=os.environ.get("CHROMIUM_PATH") or None,
                args=["--no-sandbox"],
            )
            version = browser.version
            page = browser.new_page()
            page.goto(state.good_origin + "/", wait_until="domcontentloaded")
            def call(body, token=TOKEN, extra=False):
                return page.evaluate(FETCH, {"url": endpoint, "body": body, "token": token, "extra": extra})
            first = call(op("op-1", "alpha"))
            check("BP01", first.get("status") == 200 and first.get("body", {}).get("status") == "ACCEPTED",
                  "authorized browser request accepted")
            check("BP02", len(state.receipts) == 1 and
                  any(x["method"] == "OPTIONS" and x["origin"] == state.good_origin for x in state.requests),
                  "cross-origin authorization/json request preflighted without mutation")
            replay = call(op("op-1", "alpha"))
            check("BP03", replay.get("body", {}).get("status") == "REPLAY" and len(state.receipts) == 1,
                  "same ID/digest replay is immutable")
            bad_auth = call(op("op-2", "beta"), token="wrong-token")
            check("BP04", bad_auth.get("status") == 401 and len(state.receipts) == 1,
                  "valid CORS origin does not grant authentication")
            conflict = call(op("op-1", "altered"))
            check("BP05", conflict.get("status") == 409 and len(state.receipts) == 1,
                  "same ID/changed digest rejected")
            missing = call(op("op-2", "beta"), token=None)
            check("BP06", missing.get("status") == 401 and len(state.receipts) == 1,
                  "missing bearer denied with allowed CORS")
            extra_before = len([x for x in state.requests if x["method"] == "POST"])
            extra = call(op("op-3", "gamma"), extra=True)
            extra_after = len([x for x in state.requests if x["method"] == "POST"])
            check("BP07", extra.get("networkError") and extra_before == extra_after,
                  "unallowlisted request header fails browser preflight without POST")
            page.goto(bad_origin + "/", wait_until="domcontentloaded")
            evil_before = len([x for x in state.requests if x["method"] == "POST"])
            evil = page.evaluate(FETCH, {"url": endpoint, "body": op("op-4", "delta"),
                                         "token": TOKEN, "extra": False})
            evil_after = len([x for x in state.requests if x["method"] == "POST"])
            check("BP08", evil.get("networkError") and evil_before == evil_after,
                  "disallowed browser origin blocked before mutation")
            check("BP09", raw_post(endpoint, op("op-5", "epsilon"), bearer="bad") == 401
                  and len(state.receipts) == 1,
                  "nonbrowser HTTP is not protected by CORS; server bearer check required")
            check("BP10", raw_post(endpoint, op("op-6", "zeta"), bearer=TOKEN) == 200
                  and len(state.receipts) == 2,
                  "nonbrowser authorized HTTP succeeds without Origin; CORS is not authentication")
            check("BP11", raw_post(endpoint, op("op-7", "eta"), bearer=TOKEN, origin="null") == 403
                  and len(state.receipts) == 2,
                  "literal null Origin not trusted by this research policy")
            check("BP12", first.get("cacheControl") == "no-store" and
                  all(not x["authorization_present"] for x in state.requests if x["method"] == "OPTIONS"),
                  "response no-store and preflight carries no Authorization header")
            # Separate deliberately UNSAFE Service Worker control: HTTP no-store is
            # not an automatic veto on explicit CacheStorage.put().
            page.goto(state.good_origin + "/", wait_until="domcontentloaded")
            controlled = page.evaluate("""async () => {
              await navigator.serviceWorker.register('/sw.js');
              await navigator.serviceWorker.ready;
              if (!navigator.serviceWorker.controller) {
                await new Promise((resolve, reject) => {
                  const timer = setTimeout(() => reject(new Error('control timeout')), 10000);
                  navigator.serviceWorker.addEventListener('controllerchange', () => {
                    clearTimeout(timer); resolve();
                  }, {once: true});
                });
              }
              return !!navigator.serviceWorker.controller;
            }""")
            check("BP13", controlled, "disposable Service Worker controls allowed-origin page")
            first_receipt = page.evaluate("""async () => {
              const r = await fetch('/api-receipt', {cache: 'no-store'});
              return {value: (await r.json()).value, cacheControl: r.headers.get('cache-control')};
            }""")
            check("BP14", first_receipt == {"value": "v1", "cacheControl": "no-store"},
                  "first synthetic receipt has HTTP no-store response")
            state.receipt_value = "v2"
            second_receipt = page.evaluate("""async () => {
              const r = await fetch('/api-receipt', {cache: 'no-store'});
              const cached = await (await caches.open('synthetic-unsafe-receipt')).match('/api-receipt');
              return {seen: (await r.json()).value, cached: cached && (await cached.json()).value};
            }""")
            check("BP15", second_receipt == {"seen": "v1", "cached": "v1"},
                  "UNSAFE negative control: Worker explicitly caches no-store response and serves stale receipt")
            cleared_receipt = page.evaluate("""async () => {
              await caches.delete('synthetic-unsafe-receipt');
              const r = await fetch('/api-receipt', {cache: 'no-store'});
              return (await r.json()).value;
            }""")
            check("BP16", cleared_receipt == "v2",
                  "deleting disposable CacheStorage entry restores fresh synthetic response")
            browser.close()
        report = {
            "target": "disposable browser/HTTP origin and bearer fixture, NOT Firebase or LogMate",
            "environment": {"python": platform.python_version(), "chromium": version,
                            "playwright": "1.57.0", "browser": "Chromium"},
            "passed": sum(x["passed"] for x in checks), "total": len(checks),
            "checks": checks,
            "limitations": [
                "Synthetic localhost origins and fixed fake bearer only",
                "No deployed Functions, Firebase Auth, real LogMate canonical wire, Safari or EFB",
                "CORS is a browser read/preflight mechanism, not authentication or nonbrowser access control",
                "BP15 deliberately proves this synthetic Service Worker can cache and replay no-store response; not a LogMate defect",
            ],
        }
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        assert report["passed"] == report["total"], report
        print(f"RESULT {report['passed']}/{report['total']} PASS")
    finally:
        for server in (good, bad, api):
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
