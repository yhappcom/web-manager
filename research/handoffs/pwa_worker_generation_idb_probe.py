#!/usr/bin/env python3
"""Synthetic actual Chrome v1 active/v2 waiting Worker IndexedDB control merge. NOT LogMate."""
import json, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

version={'value':1}
SW=r"""
const VERSION=__VERSION__;
let releaseOld=null;
function openDb(){
  return new Promise((resolve,reject)=>{
    const req=indexedDB.open('research-worker-generation-control',1);
    req.onupgradeneeded=()=>req.result.createObjectStore('control');
    req.onsuccess=()=>resolve(req.result);
    req.onerror=()=>reject(req.error);
  });
}
async function mutate(kind,value){
  const db=await openDb();
  return new Promise((resolve,reject)=>{
    const tx=db.transaction('control','readwrite');
    const store=tx.objectStore('control');
    const req=store.get('catalogue');
    req.onsuccess=()=>{
      const s=req.result||{oldAssignments:[],candidate:null};
      if(kind==='candidate')s.candidate=value;
      else s.oldAssignments.push(value);
      store.put(s,'catalogue');
    };
    tx.oncomplete=()=>{db.close();resolve(true)};
    tx.onabort=()=>{db.close();reject(new Error('aborted'))};
    tx.onerror=()=>{db.close();reject(tx.error||new Error('error'))};
  });
}
async function notify(tag){
  const cs=await self.clients.matchAll({type:'window',includeUncontrolled:true});
  for(const c of cs)c.postMessage({tag,version:VERSION});
}
self.addEventListener('install',e=>e.waitUntil((async()=>{
  if(VERSION===2)await mutate('candidate','v2');
})()));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('message',e=>{
  if(VERSION!==1)return;
  if(e.data==='BEGIN')e.waitUntil((async()=>{
    await notify('READ_BARRIER');
    await new Promise(resolve=>{releaseOld=resolve});
    await mutate('assignment','old-tab');
    await notify('DONE');
  })());
  if(e.data==='RELEASE'&&releaseOld){releaseOld();releaseOld=null;}
});
"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/sw.js'):
            body=SW.replace('__VERSION__',str(version['value'])).encode()
            typ='application/javascript'
        elif self.path=='/':
            body=b'<!doctype html><title>synthetic Worker IDB control</title>'
            typ='text/html'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type',typ)
        self.send_header('Cache-Control','no-store')
        self.send_header('Service-Worker-Allowed','/')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args):pass

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    result={'scope':'synthetic Chrome two actual Worker generations with IDB; not LogMate/Safari/EFB','cases':[]}
    def ok(case,meaning,observed):
        result['cases'].append({'id':case,'status':'PASS','meaning':meaning,'observed':observed})
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/google-chrome'),args=['--no-sandbox'])
            result['browser']=browser.version
            ctx=browser.new_context()
            page=ctx.new_page()
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            page.evaluate("async()=>{await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready}")
            page.reload()
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            page.evaluate("window.events=[];navigator.serviceWorker.addEventListener('message',e=>window.events.push(e.data))")
            page.evaluate("navigator.serviceWorker.controller.postMessage('BEGIN')")
            page.wait_for_function("window.events.some(e=>e.tag==='READ_BARRIER')")
            ok('WG01','old v1 Worker controls page and holds an event barrier',page.evaluate('navigator.serviceWorker.controller.state'))
            version['value']=2
            page.evaluate("async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update()}")
            page.wait_for_function("async()=>{const r=await navigator.serviceWorker.getRegistration();return r.waiting?.state==='installed'}")
            ok('WG02','v2 installed and waiting without skipWaiting',True)
            state=page.evaluate("""async()=>{
              const req=indexedDB.open('research-worker-generation-control',1);
              const db=await new Promise((res,rej)=>{req.onsuccess=()=>res(req.result);req.onerror=()=>rej(req.error)});
              return await new Promise((res,rej)=>{
                const tx=db.transaction('control','readonly');
                const q=tx.objectStore('control').get('catalogue');
                let s;q.onsuccess=()=>{s=q.result};
                tx.oncomplete=()=>{db.close();res(s)};
                tx.onerror=()=>{db.close();rej(tx.error)};
              });
            }""")
            assert state=={'oldAssignments':[],'candidate':'v2'},state
            ok('WG03','waiting v2 committed candidate to IDB before v1 delayed mutation',state)
            page.evaluate("navigator.serviceWorker.controller.postMessage('RELEASE')")
            page.wait_for_function("window.events.some(e=>e.tag==='DONE')")
            final=page.evaluate("""async()=>{
              const req=indexedDB.open('research-worker-generation-control',1);
              const db=await new Promise((res,rej)=>{req.onsuccess=()=>res(req.result);req.onerror=()=>rej(req.error)});
              return await new Promise((res,rej)=>{
                const tx=db.transaction('control','readonly');
                const q=tx.objectStore('control').get('catalogue');
                let s;q.onsuccess=()=>{s=q.result};
                tx.oncomplete=()=>{db.close();res(s)};
                tx.onerror=()=>{db.close();rej(tx.error)};
              });
            }""")
            assert final=={'oldAssignments':['old-tab'],'candidate':'v2'},final
            ok('WG04','old v1 IDB transaction observes candidate and retains both fields',final)
            waiting=page.evaluate("async()=>!!(await navigator.serviceWorker.getRegistration()).waiting")
            assert waiting
            ok('WG05','v2 remains waiting and v1 controller remains active',waiting)
            result['during']=state
            result['after']=final
            browser.close()
    finally:
        server.shutdown()
        if os.getenv('EVIDENCE_OUT'):
            with open(os.environ['EVIDENCE_OUT'],'w',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
