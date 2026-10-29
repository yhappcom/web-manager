#!/usr/bin/env python3
"""Research-only Chrome CSP route/report privacy fixture; never use real OOB codes."""
import base64
import hashlib
import http.server
import json
import os
import threading
import time
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright

TOKEN = 'SYNTHETIC_OOB_CODE_NOT_A_SECRET_20261029'
SCRIPT = "document.documentElement.dataset.started='yes'"
STYLE = 'body{color:rgb(1, 2, 3)}'
OUT = os.getenv('EVIDENCE_OUT', '/tmp/pwa-csp-route-privacy.json')
CHROME = os.getenv('CHROMIUM_PATH', '/usr/bin/google-chrome')

def sha(s):
    return base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()

class Handler(http.server.BaseHTTPRequestHandler):
    reports = []
    pixel_refs = {}
    def log_message(self, *_):
        pass
    def do_GET(self):
        parsed = urlsplit(self.path)
        path = parsed.path
        if path == '/pixel':
            case = parse_qs(parsed.query).get('case', [''])[0]
            Handler.pixel_refs[case] = self.headers.get('Referer', '')
            self.send_response(204)
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return
        if path not in ('/auth', '/auth-noref', '/safe', '/strict', '/hashed'):
            self.send_response(404)
            self.end_headers()
            return
        html = f'<!doctype html><html><head><style>{STYLE}</style></head><body><h1>CSP fixture</h1><img src="/pixel?case={path.lstrip(chr(47))}" alt=""><script>{SCRIPT}</script></body></html>'
        b = html.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        if path in ('/auth', '/auth-noref', '/safe'):
            self.send_header('Content-Security-Policy-Report-Only', "script-src 'none'; style-src 'none'; report-uri /collect")
        if path == '/auth-noref':
            self.send_header('Referrer-Policy', 'no-referrer')
        if path == '/strict':
            self.send_header('Content-Security-Policy', "script-src 'self'; style-src 'self'")
        if path == '/hashed':
            self.send_header('Content-Security-Policy', f"script-src 'sha256-{sha(SCRIPT)}'; style-src 'sha256-{sha(STYLE)}'")
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_POST(self):
        if urlsplit(self.path).path != '/collect':
            self.send_response(404)
            self.end_headers()
            return
        raw = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        try:
            obj = json.loads(raw)
            Handler.reports.append(obj)
        except (ValueError, UnicodeError):
            pass
        self.send_response(204)
        self.end_headers()

def main():
    Handler.reports = []
    Handler.pixel_refs = {}
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    cases = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
            try:
                context = browser.new_context()
                for path, expected_run, expected_style in [('/auth?mode=resetPassword&oobCode='+TOKEN, True, True), ('/auth-noref?mode=resetPassword&oobCode='+TOKEN, True, True), ('/safe', True, True), ('/strict', False, False), ('/hashed', True, True)]:
                    page = context.new_page()
                    response = page.goto(base+path, wait_until='load')
                    assert response.status == 200
                    actual_run = page.evaluate("document.documentElement.dataset.started==='yes'")
                    actual_style = page.evaluate("getComputedStyle(document.body).color==='rgb(1, 2, 3)'")
                    assert actual_run == expected_run, (path, 'script', actual_run)
                    assert actual_style == expected_style, (path, 'style', actual_style)
                    cases.append({'route': path.split('?')[0], 'scriptExecuted': actual_run, 'styleApplied': actual_style, 'http': response.status})
                    page.close()
                deadline = time.monotonic() + 8
                while (len(Handler.reports) < 6 or len(Handler.pixel_refs) < 2) and time.monotonic() < deadline:
                    time.sleep(.1)
                urls = [v.get('csp-report',{}).get('document-uri','') for v in Handler.reports]
                assert any(TOKEN in u and '/auth?' in u for u in urls), ('missing synthetic query in CSP report', len(urls), urls)
                assert any('/safe' in u and TOKEN not in u for u in urls), ('missing safe route report', urls)
                assert any(TOKEN in u and '/auth-noref?' in u for u in urls), ('no-referrer did not preserve query in CSP report', len(urls))
                assert TOKEN in Handler.pixel_refs.get('auth', ''), 'default same-origin Referer must carry synthetic query'
                assert 'auth-noref' in Handler.pixel_refs and Handler.pixel_refs['auth-noref'] == '', 'no-referrer must suppress same-origin Referer'
                cases.append({'case':'REPORT_URI_QUERY_CUSTODY','authReportIncludesSyntheticQuery':True,'safeReportOmitsSyntheticQuery':True,'reportCount':len(urls)})
                cases.append({'case':'REFERRER_VS_CSP_REPORT', 'defaultSameOriginRefererHasSyntheticQuery':True, 'noReferrerSuppressesReferer':True, 'noReferrerStillReportsDocumentQuery':True})
                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    result = {'scope':'synthetic local HTTP; NOT LogMate, not real OOB token, not Safari or production', 'cases':cases}
    with open(OUT,'w',encoding='utf-8') as f:
        json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
    print('6/6 synthetic route/CSP/report/referrer checks PASS')

if __name__=='__main__':
    main()
