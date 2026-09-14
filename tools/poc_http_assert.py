#!/usr/bin/env python3
from __future__ import annotations
import argparse, contextlib, json, threading, tempfile, urllib.error, urllib.parse, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from build_poc_corpus import build, verify

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

def request(url):
    op=urllib.request.build_opener(NoRedirect)
    try: r=op.open(url,timeout=5); return r.status, {k.lower():v for k,v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e: return e.code,{k.lower():v for k,v in e.headers.items()},e.read()

def assert_contract(base, contract, profile):
    failures=[]; checks=0
    def chk(ok,label):
        nonlocal checks; checks+=1
        if not ok: failures.append(label)
    origin=contract['canonical_origin']
    for path in contract['html_paths']:
        st,h,b=request(base+path); text=b.decode('utf-8','replace')
        chk(st==200,f'{path}:status'); chk(h.get('content-type','').startswith('text/html'),f'{path}:content-type')
        for k,v in contract['required_html_headers'].items(): chk(h.get(k)==v,f'{path}:header:{k}')
        chk(h.get('cache-control')==contract['html_cache_control'],f'{path}:cache-control')
        chk(f'rel="canonical" href="{origin}{path}"' in text,f'{path}:canonical')
        lang='ko' if path.startswith('/ko/') else 'en'; chk(f'<html lang="{lang}">' in text,f'{path}:lang')
        if profile=='preview': chk(contract['preview_required_header'][1] in h.get(contract['preview_required_header'][0],''),f'{path}:preview-noindex')
    for src,dst in contract['canonical_redirects']:
        st,h,_=request(base+src); chk(st in (301,308),f'{src}:redirect-status'); chk(urllib.parse.urlparse(h.get('location','')).path==dst,f'{src}:redirect-location')
    for path,mime in contract['machine_files'].items():
        st,h,b=request(base+path); chk(st==200,f'{path}:status'); chk(h.get('content-type','').startswith(mime),f'{path}:content-type'); chk(h.get('cache-control')==contract['machine_cache_control'],f'{path}:cache-control')
        if path.endswith('assetlinks.json') or path.endswith('apple-app-site-association'):
            try: json.loads(b); valid=True
            except Exception: valid=False
            chk(valid,f'{path}:valid-json')
    st,h,b=request(base+contract['not_found_path']); chk(st==404,'404:status'); chk(contract['not_found_marker'] in b.decode('utf-8','replace'),'404:body')
    return {'ok':not failures,'checks':checks,'failures':failures,'profile':profile,'base_url':base}

class RefHandler(SimpleHTTPRequestHandler):
    root=None; profile='production'; contract=None; fault=None
    def log_message(self,*args): pass
    def _headers(self,path,is_html):
        if is_html:
            for k,v in self.contract['required_html_headers'].items():
                if self.fault=='missing-csp' and k=='content-security-policy': continue
                self.send_header(k,v)
            self.send_header('Cache-Control',self.contract['html_cache_control'])
            if self.profile=='preview' and self.fault!='missing-preview-noindex': self.send_header('X-Robots-Tag','noindex, nofollow')
        else: self.send_header('Cache-Control',self.contract['machine_cache_control'])
    def do_GET(self):
        path=urllib.parse.urlparse(self.path).path
        for src,dst in self.contract['canonical_redirects']:
            if path==src:
                self.send_response(308); self.send_header('Location',dst); self.end_headers(); return
        if path==self.contract['not_found_path']:
            data=(self.root/'404.html').read_bytes(); self.send_response(404); self.send_header('Content-Type','text/html; charset=utf-8'); self._headers(path,True); self.end_headers(); self.wfile.write(data); return
        rel=path.lstrip('/')
        fp=self.root/rel
        if path.endswith('/'): fp=fp/'index.html'
        if not fp.exists():
            data=(self.root/'404.html').read_bytes(); self.send_response(404); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(data); return
        data=fp.read_bytes(); is_html=fp.suffix=='.html'
        if self.fault=='wrong-canonical' and is_html and path=='/en/': data=data.replace(b'https://minttap.app/en/',b'https://minttap.app/ko/',1)
        if path.endswith('apple-app-site-association'): mime='application/json'
        elif fp.suffix=='.json': mime='application/json'
        elif fp.suffix=='.xml': mime='application/xml'
        elif fp.suffix=='.txt': mime='text/plain'
        else: mime='text/html'
        if self.fault=='bad-assetlinks-mime' and path.endswith('assetlinks.json'): mime='text/plain'
        self.send_response(200); self.send_header('Content-Type',mime+'; charset=utf-8'); self._headers(path,is_html)
        self.end_headers(); self.wfile.write(data)

@contextlib.contextmanager
def reference_server(root,contract,profile,fault=None):
    class H(RefHandler): pass
    H.root=root; H.contract=contract; H.profile=profile; H.fault=fault
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); t=threading.Thread(target=srv.serve_forever,daemon=True); t.start()
    try: yield f'http://127.0.0.1:{srv.server_port}'
    finally: srv.shutdown(); t.join()

def self_test(contract_path, cases_path):
    contract=json.loads(Path(contract_path).read_text())
    cases=json.loads(Path(cases_path).read_text())
    out=[]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'site'; build(root,Path(td)/'artifact.json')
        manifest=Path(td)/'artifact.json'
        for case in cases:
            name=case['name']; profile=case['profile']; fault=case.get('fault'); expected=case['expected_ok']
            with reference_server(root,contract,profile,fault) as base:
                r=assert_contract(base,contract,profile); out.append({'name':name,'passed':r['ok']==expected,'expected_ok':expected,'observed_ok':r['ok'],'failures':r['failures'][:5]})
        v_ok,_=verify(root,manifest); out.append({'name':'artifact-clean','passed':v_ok,'expected_ok':True,'observed_ok':v_ok,'failures':[]})
        target=root/'en/index.html'; original=target.read_text(); target.write_text(original+'\nmutation')
        v_ok,reason=verify(root,manifest); out.append({'name':'artifact-mutation-detected','passed':not v_ok,'expected_ok':False,'observed_ok':v_ok,'failures':[reason] if reason else []})
    ok=all(x['passed'] for x in out); print(json.dumps({'ok':ok,'passed':sum(x['passed'] for x in out),'total':len(out),'results':out},indent=2)); return 0 if ok else 1

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-url'); ap.add_argument('--contract',default='control/poc/http_contract.json'); ap.add_argument('--profile',choices=['production','preview'],default='production'); ap.add_argument('--self-test',action='store_true'); ap.add_argument('--self-test-cases',default='control/tests/poc_http_assert_cases.json'); args=ap.parse_args()
    if args.self_test: raise SystemExit(self_test(args.contract,args.self_test_cases))
    if not args.base_url: ap.error('--base-url required unless --self-test')
    c=json.loads(Path(args.contract).read_text()); r=assert_contract(args.base_url.rstrip('/'),c,args.profile); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
if __name__=='__main__': main()
