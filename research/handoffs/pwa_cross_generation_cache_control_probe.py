#!/usr/bin/env python3
"""Research-only Chrome Service Worker generation race. Not LogMate source or runtime."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

version = {"value": 1}
SW = r"""
const VERSION = __VERSION__, CACHE = 'research-control-cache', KEY = '/research-control.json';
let releaseStale = null;
async function read() {
  const c = await caches.open(CACHE), r = await c.match(KEY);
  return r ? await r.json() : {oldAssignments:[],candidate:null};
}
async function write(s) {
  await (await caches.open(CACHE)).put(KEY,new Response(JSON.stringify(s)));
}
async function notify(tag) {
  const all = await self.clients.matchAll({type:'window',includeUncontrolled:true});
  for(const c of all) c.postMessage({tag,version:VERSION});
}
self.addEventListener('install',e=>e.waitUntil((async()=>{
  if(VERSION===2) { const s=await read();s.candidate='v2';await write(s); }
})()));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('message',e=>{
  if(VERSION!==1) return;
  if(e.data==='BEGIN') e.waitUntil((async()=>{
    const stale=await read();
    await notify('READ');
    await new Promise(resolve=>{releaseStale=resolve});
    stale.oldAssignments.push('old-tab');
    await write(stale);
    await notify('DONE');
  })());
  if(e.data==='RELEASE' && releaseStale) {releaseStale();releaseStale=null;}
});
"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/sw.js'):
            body=SW.replace('__VERSION__',str(version['value'])).encode()
            kind='application/javascript'
        elif self.path=='/':
            body=b'<!doctype html><title>SW generation research</title><body>synthetic</body>'
            kind='text/html'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type',kind)
        self.send_header('Cache-Control','no-store')
        self.send_header('Service-Worker-Allowed','/')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args): pass

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    observations=[]
    result={'scope':'synthetic Chrome; not LogMate runtime','cases':observations}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/google-chrome'),args=['--no-sandbox'])
            result['browser']=browser.version
            context=browser.new_context()
            page=context.new_page()
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            page.evaluate("""async()=>{
              window.events=[];
              navigator.serviceWorker.addEventListener('message',e=>window.events.push(e.data));
              await navigator.serviceWorker.register('/sw.js');
              await navigator.serviceWorker.ready;
              await (await caches.open('research-control-cache')).put('/research-control.json',new Response(JSON.stringify({oldAssignments:[],candidate:null})));
            }""")
            page.reload()
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            baseline=page.evaluate("""async()=>{
              const c=await caches.open('research-control-cache');
              const s=await(await c.match('/research-control.json')).json();
              s.oldAssignments.push('baseline');await c.put('/research-control.json',new Response(JSON.stringify(s)));
              const t=await(await c.match('/research-control.json')).json();
              t.candidate='baseline-candidate';await c.put('/research-control.json',new Response(JSON.stringify(t)));
              return await(await c.match('/research-control.json')).json();
            }""")
            assert baseline=={'oldAssignments':['baseline'],'candidate':'baseline-candidate'},baseline
            observations.append({'id':'CG01','status':'PASS','meaning':'sequential read/modify/write retains both fields'})
            page.evaluate("""async()=>{
              await (await caches.open('research-control-cache')).put('/research-control.json',new Response(JSON.stringify({oldAssignments:[],candidate:null})));
              navigator.serviceWorker.controller.postMessage('BEGIN');
            }""")
            page.wait_for_function("window.events.some(e=>e.tag==='READ')")
            version['value']=2
            page.evaluate("async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update()}")
            page.wait_for_function("async()=>{const r=await navigator.serviceWorker.getRegistration();return r.waiting?.state==='installed'}")
            during=page.evaluate("async()=>await(await(await caches.open('research-control-cache')).match('/research-control.json')).json()")
            assert during=={'oldAssignments':[],'candidate':'v2'},during
            observations.append({'id':'CG02','status':'PASS','meaning':'installing v2 wrote shared catalogue while v1 controls tab'})
            page.evaluate("navigator.serviceWorker.controller.postMessage('RELEASE')")
            page.wait_for_function("window.events.some(e=>e.tag==='DONE')")
            after=page.evaluate("async()=>await(await(await caches.open('research-control-cache')).match('/research-control.json')).json()")
            assert after=={'oldAssignments':['old-tab'],'candidate':None},after
            observations.append({'id':'CG03','status':'PASS','meaning':'old worker stale snapshot overwrote v2 candidate'})
            keys=page.evaluate("""async()=>{
              const c=await caches.open('research-control-cache');
              await Promise.all([c.put('/immutable-v1',new Response('old')),c.put('/immutable-v2',new Response('new'))]);
              return [await(await c.match('/immutable-v1')).text(),await(await c.match('/immutable-v2')).text()];
            }""")
            assert keys==['old','new'],keys
            observations.append({'id':'CG04','status':'PASS','meaning':'distinct immutable version keys survive, not an atomic pointer proof'})
            waiting=page.evaluate("async()=>!!(await navigator.serviceWorker.getRegistration()).waiting")
            assert waiting,waiting
            observations.append({'id':'CG05','status':'PASS','meaning':'v2 remains waiting; no forced skipWaiting'})
            result['during']=during
            result['after']=after
            browser.close()
    finally:
        server.shutdown()
        out=os.environ.get('EVIDENCE_OUT')
        if out:
            with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
