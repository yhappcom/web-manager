#!/usr/bin/env python3
"""Synthetic two-tab IndexedDB control-state probe; NOT LogMate or worker-generation execution."""
import json, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

JS = r"""
window.openControl = () => new Promise((resolve,reject)=>{
  const req=indexedDB.open('research-control-transaction-v1',1);
  req.onupgradeneeded=()=>req.result.createObjectStore('control');
  req.onsuccess=()=>resolve(req.result);
  req.onerror=()=>reject(req.error);
});
window.getState = async () => {
  const db=await openControl();
  return new Promise((resolve,reject)=>{
    const tx=db.transaction('control','readonly');
    const req=tx.objectStore('control').get('catalogue');
    let state;
    req.onsuccess=()=>{state=req.result??{oldAssignments:[],candidate:null}};
    tx.oncomplete=()=>{db.close();resolve(state)};
    tx.onerror=()=>{db.close();reject(tx.error)};
  });
};
window.replaceState = async (state) => {
  const db=await openControl();
  return new Promise((resolve,reject)=>{
    const tx=db.transaction('control','readwrite');
    tx.objectStore('control').put(state,'catalogue');
    tx.oncomplete=()=>{db.close();resolve(true)};
    tx.onerror=()=>{db.close();reject(tx.error)};
  });
};
window.mergeState = async (kind, value, abort=false) => {
  const db=await openControl();
  return new Promise((resolve,reject)=>{
    const tx=db.transaction('control','readwrite');
    const store=tx.objectStore('control');
    const req=store.get('catalogue');
    req.onsuccess=()=>{
      const s=req.result??{oldAssignments:[],candidate:null};
      if(kind==='assignment')s.oldAssignments.push(value);
      else if(kind==='candidate')s.candidate=value;
      store.put(s,'catalogue');
      if(abort)tx.abort();
    };
    tx.oncomplete=()=>{db.close();resolve('committed')};
    tx.onabort=()=>{db.close();resolve('aborted')};
    tx.onerror=()=>{if(!abort){db.close();reject(tx.error||new Error('transaction error'))}};
  });
};
"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/': self.send_error(404);return
        body=b'<!doctype html><title>synthetic IDB control test</title>'
        self.send_response(200)
        self.send_header('Content-Type','text/html')
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args): pass

def main():
    srv=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    result={'scope':'synthetic Chrome IndexedDB two-tab; NOT LogMate/Worker-generation/Safari','cases':[]}
    def ok(case,meaning,observed):
        result['cases'].append({'id':case,'status':'PASS','meaning':meaning,'observed':observed})
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/google-chrome'),args=['--no-sandbox'])
            result['browser']=browser.version
            context=browser.new_context()
            a=context.new_page()
            c=context.new_page()
            url=f'http://127.0.0.1:{srv.server_port}/'
            for pg in (a,c):
                pg.goto(url)
                pg.add_script_tag(content=JS)
            initial={'oldAssignments':[],'candidate':None}
            a.evaluate('(s)=>replaceState(s)',initial)
            assert c.evaluate('getState()')==initial
            ok('ID01','two independent tabs share same-origin IDB control state',initial)
            a.evaluate("window.pending=mergeState('assignment','old-tab')")
            c.evaluate("window.pending=mergeState('candidate','v2')")
            assert a.evaluate('window.pending')=='committed'
            assert c.evaluate('window.pending')=='committed'
            both=c.evaluate('getState()')
            assert both=={'oldAssignments':['old-tab'],'candidate':'v2'},both
            ok('ID02','readwrite get+put in each transaction preserves both fields',both)
            a.evaluate('(s)=>replaceState(s)',initial)
            snap_a=a.evaluate('getState()')
            snap_c=c.evaluate('getState()')
            snap_a['oldAssignments'].append('old-tab')
            snap_c['candidate']='v2'
            a.evaluate('(s)=>replaceState(s)',snap_a)
            c.evaluate('(s)=>replaceState(s)',snap_c)
            lost=a.evaluate('getState()')
            assert lost=={'oldAssignments':[],'candidate':'v2'},lost
            ok('ID03','UNSAFE negative control: stale pretransaction read loses update',lost)
            a.evaluate('(s)=>replaceState(s)',both)
            aborted=c.evaluate("mergeState('candidate','v3',true)")
            after=a.evaluate('getState()')
            assert aborted=='aborted' and after==both,(aborted,after)
            ok('ID04','explicit IDB abort leaves original state',after)
            a.evaluate('(s)=>replaceState(s)',{'oldAssignments':['old-tab'],'candidate':'v4'})
            missing=a.evaluate("async()=>!!(await (await caches.open('research-asset-cache')).match('/asset-v4'))")
            assert missing is False
            ok('ID05','IDB candidate pointer can reference missing CacheStorage asset',{'candidate':'v4','assetPresent':missing})
            a.evaluate("async()=>{await (await caches.open('research-asset-cache')).put('/asset-v4',new Response('verified-asset'))}")
            present=c.evaluate("async()=>await(await(await caches.open('research-asset-cache')).match('/asset-v4')).text()")
            assert present=='verified-asset'
            ok('ID06','staged asset independently readable before pointer promotion (ordering model only)',present)
            browser.close()
    finally:
        srv.shutdown()
        if os.getenv('EVIDENCE_OUT'):
            with open(os.environ['EVIDENCE_OUT'],'w',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
