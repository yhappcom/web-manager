#!/usr/bin/env python3
"""Synthetic Chrome Auth Action URL, DOM secret and bfcache lifecycle probe.

Only invented values. No real Firebase calls, user credentials or product source.
"""
import http.server
import json
import os
import threading
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

CODE = 'SYNTHETIC_ACTION_CODE_20261029'
PASSWORD = 'SYNTHETIC_PASSWORD_20261029'
OUT = os.getenv('EVIDENCE_OUT', '/tmp/pwa-auth-lifecycle.json')
CHROME = os.getenv('CHROMIUM_PATH', '/usr/bin/google-chrome')


class Handler(http.server.BaseHTTPRequestHandler):
    ingress = []
    referers = []

    def log_message(self, *_):
        pass

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/pixel':
            Handler.referers.append(CODE in self.headers.get('Referer', ''))
            self.send_response(204)
            self.end_headers()
            return
        if path not in ('/unsafe', '/safe', '/other'):
            self.send_response(404)
            self.end_headers()
            return
        Handler.ingress.append({'route': path, 'hasSyntheticQuery': CODE in self.path})
        if path == '/other':
            html = '<!doctype html><html><body>Other page</body></html>'
        else:
            safe = path == '/safe'
            html = """<!doctype html><html><body>
            <img src="/pixel?case=early" alt="">
            <form id="form"><input id="pw" type="password">
            <input id="confirm" type="password">
            <button id="done" type="button">Success</button></form>
            <p id="result"></p>
            <script>
            const code = new URLSearchParams(location.search).get('oobCode');
            window.__initialCodePresent = Boolean(code);
            window.__restored = false;
            window.addEventListener('pageshow', e => {
              if (e.persisted) { window.__restored = true; __RESTORE__ }
            });
            __REPLACE__
            document.querySelector('#done').addEventListener('click', () => {
              document.querySelector('#form').hidden = true;
              document.querySelector('#result').textContent = 'Password updated';
              __SCRUB__
            });
            </script></body></html>"""
            scrub = "document.querySelector('#pw').value='';document.querySelector('#confirm').value='';" if safe else ''
            replace = "const u=new URL(location.href);u.searchParams.delete('oobCode');history.replaceState(null,'',u.pathname+u.search);" if safe else ''
            html = html.replace('__REPLACE__', replace).replace('__SCRUB__', scrub).replace('__RESTORE__', scrub)
        payload = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main():
    Handler.ingress = []
    Handler.referers = []
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox'])
            try:
                for name in ('unsafe', 'safe'):
                    context = browser.new_context()
                    page = context.new_page()
                    response = page.goto(base + '/' + name + '?mode=resetPassword&oobCode=' + CODE, wait_until='load')
                    assert response.status == 200
                    assert page.evaluate('window.__initialCodePresent')
                    assert (CODE in page.url) == (name == 'unsafe')
                    page.locator('#pw').fill(PASSWORD)
                    page.locator('#confirm').fill(PASSWORD)
                    page.locator('#done').click()
                    before = page.evaluate("""() => ({
                        hidden: document.querySelector('#form').hidden,
                        pw: Boolean(document.querySelector('#pw').value),
                        confirm: Boolean(document.querySelector('#confirm').value)
                    })""")
                    assert before['hidden']
                    assert before['pw'] == (name == 'unsafe')
                    assert before['confirm'] == (name == 'unsafe')
                    page.goto(base + '/other', wait_until='load')
                    page.go_back(wait_until='domcontentloaded')
                    after = page.evaluate("""() => ({
                        bfcache: window.__restored,
                        pw: Boolean(document.querySelector('#pw').value),
                        query: location.search.includes('oobCode'),
                        success: document.querySelector('#result').textContent === 'Password updated'
                    })""")
                    if name == 'safe':
                        assert not after['pw'] and not after['query']
                    elif after['bfcache']:
                        assert after['pw'] and after['query'] and after['success']
                    results.append({
                        'variant': name,
                        'initialNavigationHasSyntheticQuery': True,
                        'postSuccessHiddenFormRetainsPassword': before['pw'],
                        'postSuccessUrlRetainsCode': name == 'unsafe',
                        'bfcacheRestoredObserved': after['bfcache'],
                        'afterBackPasswordPresent': after['pw'],
                        'afterBackQueryPresent': after['query']
                    })
                    context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    assert len(Handler.ingress) >= 4
    assert any(x['route'] == '/unsafe' and x['hasSyntheticQuery'] for x in Handler.ingress)
    assert any(x['route'] == '/safe' and x['hasSyntheticQuery'] for x in Handler.ingress)
    assert len(Handler.referers) >= 2
    report = {
        'scope': 'synthetic Chrome, not LogMate/Firebase/Safari/managed EFB',
        'cases': results,
        'initialNavigationQueryReachedServer': True,
        'earlySubresourceRefererIncludedQuery': any(Handler.referers),
        'bfcacheNote': 'observed only; no-store does not guarantee either restore or non-restore'
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    print('Synthetic lifecycle assertions PASS; bfcache evidence is observational only')


if __name__ == '__main__':
    main()
