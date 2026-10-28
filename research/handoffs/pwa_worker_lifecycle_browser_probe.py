#!/usr/bin/env python3
"""Disposable Chromium SW lifecycle/IndexedDB probe. Synthetic, NOT LogMate."""
import json
import os
import shutil
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

VERSION = {"value": "v1"}
CASES = []

def shell(v, source):
    return ("<!doctype html><meta charset='utf-8'><main id='app' "
            f"data-build='{v}' data-source='{source}'>Synthetic {v}</main>")

def worker(v):
    src = r"""
const V=__V__, C='stage8-shell-'+V;
self.addEventListener('install', e=>e.waitUntil((async()=>{
 if(V==='v4-broken') throw new Error('injected install failure');
 const c=await caches.open(C);
 await c.put('/',new Response(__HTML__,{headers:{'Content-Type':'text/html'}}));
 await c.put('/asset.json',new Response(JSON.stringify({version:V,source:'worker-cache'}),
    {headers:{'Content-Type':'application/json'}}));
})()));
self.addEventListener('activate',e=>e.waitUntil((async()=>{
 const keys=await caches.keys();
 await Promise.all(keys.filter(k=>k.startsWith('stage8-shell-')&&k!==C).map(k=>caches.delete(k)));
 await self.clients.claim();
})()));
self.addEventListener('message',e=>{if(e.data==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('fetch',e=>{
 const path=new URL(e.request.url).pathname;
 if(e.request.mode==='navigate'&&path==='/')
   e.respondWith((async()=>{const c=await caches.open(C);return await c.match('/')||fetch(e.request);})());
 else if(path==='/asset.json')
   e.respondWith((async()=>{const c=await caches.open(C);return await c.match('/asset.json')||Response.error();})());
});
"""
    return src.replace('__V__',json.dumps(v)).replace('__HTML__',json.dumps(shell(v,'worker-cache')))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        v=VERSION['value']
        path=urlsplit(self.path).path
        if path=='/': data,mime=shell(v,'network').encode(),'text/html'
        elif path=='/sw.js': data,mime=worker(v).encode(),'text/javascript'
        elif path=='/asset.json': data,mime=json.dumps({'version':v,'source':'network'}).encode(),'application/json'
        else:
            self.send_response(404);self.end_headers();return
        self.send_response(200)
        self.send_header('Content-Type',mime)
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers();self.wfile.write(data)
    def log_message(self,*args): pass

def check(label, ok, **details):
    if not ok: raise AssertionError(f'{label} FAILED: {details}')
    CASES.append({'case':label,'verdict':'PASS',**details})
    print(label,'PASS',flush=True)

def state(p):
    return p.locator('#app').evaluate('(e)=>({build:e.dataset.build,source:e.dataset.source})')

def asset(p):
    return p.evaluate("""async()=>{const r=await fetch('/asset.json',{cache:'no-store'});
        return {status:r.status,body:await r.json()};}""")

def caches(p):
    return p.evaluate('async()=>await window.caches.keys()')

def write_db(p):
    return p.evaluate("""async()=>{
 const db=await new Promise((resolve,reject)=>{
  const r=indexedDB.open('stage8-test-ledger',1);
  r.onupgradeneeded=()=>r.result.createObjectStore('flights');
  r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
 });
 await new Promise((resolve,reject)=>{
  const tx=db.transaction('flights','readwrite');
  tx.objectStore('flights').put({id:'synthetic-op-01',pending:true},'flight-01');
  tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);
 });
 db.close();return true;
}""")

def read_db(p):
    return p.evaluate("""async()=>{
 const db=await new Promise((resolve,reject)=>{
  const r=indexedDB.open('stage8-test-ledger',1);
  r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
 });
 const value=await new Promise((resolve,reject)=>{
  const tx=db.transaction('flights','readonly');
  const r=tx.objectStore('flights').get('flight-01');
  r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
 });
 db.close();return value;
}""")

def waiting(p):
    p.wait_for_function("""async()=>{
      const r=await navigator.serviceWorker.getRegistration();
      return !!r?.waiting&&r.waiting.state==='installed';
    }""",timeout=20000)

def launch(playwright, profile):
    chrome=os.environ.get('CHROMIUM_PATH') or shutil.which('google-chrome') or shutil.which('chromium')
    if not chrome: raise RuntimeError('CHROMIUM_UNAVAILABLE')
    return playwright.chromium.launch_persistent_context(str(profile),executable_path=chrome,
        headless=True,service_workers='allow',args=['--no-sandbox','--no-proxy-server'])

def run():
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    profile=Path(tempfile.mkdtemp(prefix='stage8-disposable-'))
    try:
        with sync_playwright() as p:
            ctx=launch(p,profile)
            try:
                a=ctx.pages[0] if ctx.pages else ctx.new_page()
                a.goto(origin+'/',wait_until='load',timeout=20000)
                check('SW01_INITIAL_NETWORK_UNCONTROLLED',
                    state(a)=={'build':'v1','source':'network'} and
                    a.evaluate('navigator.serviceWorker.controller===null'))
                a.evaluate("async()=>await navigator.serviceWorker.register('/sw.js',{updateViaCache:'none'})")
                a.wait_for_function('navigator.serviceWorker.controller!==null',timeout=20000)
                check('SW02_CLAIM_NOT_RETROACTIVE_NAV',
                    state(a)['source']=='network' and
                    asset(a)['body']=={'version':'v1','source':'worker-cache'})
                check('SW03_IDB_COMMIT',write_db(a))
                b=ctx.new_page();b.goto(origin+'/',wait_until='load',timeout=20000)
                check('SW04_SECOND_TAB_SHARED_ORIGIN',
                    state(b)=={'build':'v1','source':'worker-cache'} and
                    read_db(b)=={'id':'synthetic-op-01','pending':True})
                VERSION['value']='v2'
                a.evaluate("async()=>await (await navigator.serviceWorker.getRegistration()).update()")
                waiting(a)
                names=caches(a)
                check('SW05_WAITING_CACHE_NOT_ACTIVE',
                    'stage8-shell-v1' in names and 'stage8-shell-v2' in names and
                    asset(a)['body']['version']=='v1' and asset(b)['body']['version']=='v1',
                    cache_names=names)
                b.close()
                check('SW06_ONE_CLIENT_BLOCKS_ACTIVATION',
                    a.evaluate("""async()=>{
                      const r=await navigator.serviceWorker.getRegistration();
                      return r.waiting?.state==='installed';
                    }"""))
                a.close()
                # A new navigation can itself race waiting-worker activation and pin v1.
                # Release any stale new client before retrying; preserve the first observation.
                attempts=[]
                c=None
                for _ in range(20):
                    c=ctx.new_page();c.goto(origin+'/',wait_until='load',timeout=20000)
                    c.wait_for_function('navigator.serviceWorker.controller!==null',timeout=20000)
                    observed_asset=asset(c)
                    attempts.append({'page':state(c),'asset':observed_asset['body']})
                    if observed_asset['body']['version']=='v2':
                        break
                    c.close();c=None;time.sleep(0.25)
                if c is None or observed_asset['body']['version']!='v2':
                    raise AssertionError('SW07 no v2 activation after releasing stale clients: '+repr(attempts))
                c.reload(wait_until='load',timeout=20000)
                observed_state=state(c)
                observed_asset=asset(c)
                check('SW07_ACTIVATION_AFTER_CLOSE',
                    observed_state=={'build':'v2','source':'worker-cache'} and
                    observed_asset['body']['version']=='v2',
                    observed_state=observed_state,observed_asset=observed_asset,
                    attempts=attempts,cache_names=caches(c))
                check('SW08_CACHE_GC_PRESERVES_IDB',
                    caches(c)==['stage8-shell-v2'] and
                    read_db(c)=={'id':'synthetic-op-01','pending':True})
                ctx.set_offline(True);c.reload(wait_until='load',timeout=20000)
                failed=c.evaluate("""async()=>{
                  try{await fetch('/network-only');return false;}catch{return true;}
                }""")
                check('SW09_OFFLINE_WITH_NETWORK_NEGATIVE',
                    state(c)=={'build':'v2','source':'worker-cache'} and failed)
            finally: ctx.close()
            ctx=launch(p,profile)
            try:
                ctx.set_offline(True)
                d=ctx.pages[0] if ctx.pages else ctx.new_page()
                d.goto(origin+'/',wait_until='load',timeout=25000)
                check('SW10_PROCESS_REOPEN_OFFLINE_IDB',
                    state(d)=={'build':'v2','source':'worker-cache'} and
                    read_db(d)=={'id':'synthetic-op-01','pending':True})
                ctx.set_offline(False);VERSION['value']='v3'
                d.evaluate("async()=>await (await navigator.serviceWorker.getRegistration()).update()")
                waiting(d)
                d.evaluate("""async()=>{
                  const r=await navigator.serviceWorker.getRegistration();
                  r.waiting.postMessage('SKIP_WAITING');
                }""")
                d.wait_for_function("""async()=>{
                  const r=await navigator.serviceWorker.getRegistration();
                  if(r?.waiting||r?.active?.state!=='activated')return false;
                  const x=await fetch('/asset.json');return (await x.json()).version==='v3';
                }""",timeout=20000)
                check('SW11_FORCED_UPDATE_MIXES_DOCUMENT_AND_ASSET',
                    state(d)['build']=='v2' and asset(d)['body']['version']=='v3')
                check('SW12_FORCED_UPDATE_IDB_SURVIVES',
                    read_db(d)=={'id':'synthetic-op-01','pending':True})
                d.reload(wait_until='load',timeout=20000)
                check('SW13_RELOAD_RECONCILES',
                    state(d)['build']=='v3' and asset(d)['body']['version']=='v3')
                VERSION['value']='v4-broken'
                try: d.evaluate("async()=>await (await navigator.serviceWorker.getRegistration()).update()")
                except Exception: pass
                d.wait_for_function("""async()=>{
                  const r=await navigator.serviceWorker.getRegistration();
                  return !r?.installing&&!r?.waiting;
                }""",timeout=20000)
                check('SW14_FAILED_INSTALL_KEEPS_ACTIVE_AND_IDB',
                    asset(d)['body']['version']=='v3' and
                    'stage8-shell-v4-broken' not in caches(d) and
                    read_db(d)=={'id':'synthetic-op-01','pending':True})
                storage=d.evaluate("""async()=>({
                  persisted:await navigator.storage.persisted(),
                  estimate:await navigator.storage.estimate()
                })""")
                check('SW15_PERSISTENCE_OBSERVATION_NOT_BACKUP',
                    isinstance(storage['persisted'],bool) and storage['estimate']['quota']>0,
                    persisted=storage['persisted'])
            finally: ctx.close()
        return {'verdict':'BOUNDED_SYNTHETIC_CHROMIUM_PASS','cases':CASES,
                'production_validation':'OPEN','safari_managed_efb':'OPEN'}
    finally:
        server.shutdown();server.server_close()
        shutil.rmtree(profile,ignore_errors=True)

if __name__=='__main__':
    try:
        result=run()
        if os.environ.get('EVIDENCE_OUT'):
            Path(os.environ['EVIDENCE_OUT']).write_text(json.dumps(result,indent=2),encoding='utf-8')
        print('VERDICT',result['verdict'],len(result['cases']),flush=True)
    except Exception as exc:
        failure={'verdict':'INCOMPLETE_OR_FAILURE','cases':CASES,
                 'error_type':type(exc).__name__,'error':str(exc)[:1500],
                 'production_validation':'OPEN'}
        if os.environ.get('EVIDENCE_OUT'):
            Path(os.environ['EVIDENCE_OUT']).write_text(json.dumps(failure,indent=2),encoding='utf-8')
        print('VERDICT INCOMPLETE_OR_FAILURE',type(exc).__name__,str(exc),flush=True)
        raise
