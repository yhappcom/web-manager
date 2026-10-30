#!/usr/bin/env python3
"""Disposable Chrome CacheStorage catalogue trust-root probe. NOT LogMate."""
import hashlib, http.server, json, os, socketserver, threading
from playwright.sync_api import sync_playwright

GOOD = "window.__catalogueMarker = 'TRUSTED';"
BAD = "window.__catalogueMarker = 'ALTERED';"
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
OUT = os.getenv("EVIDENCE_OUT", "/tmp/pwa-mutable-catalogue.json")
CHROME = os.getenv("CHROMIUM_PATH", "/usr/bin/google-chrome")

# Reduced, source-aligned readControl -> versionFor -> verifiedResponse path.
# Deliberately NOT the full LogMate-generated worker.
SW = r"""
const KEY='/__control.json';
const hash=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
async function readControl(){
 const r=await(await caches.open('control')).match(KEY);
 if(!r)return {schemaVersion:2,currentBuildId:null,versions:{},clientBuilds:{}};
 try{const c=await r.json();if(c?.schemaVersion===2&&c.versions&&c.clientBuilds)return c;}catch(_){}
 return {schemaVersion:2,currentBuildId:null,versions:{},clientBuilds:{}};
}
const versionFor=(c,id)=>c.versions[id]?.manifest||null;
async function verifiedResponse(cache,item){
 const r=await cache.match(item.path);if(!r)return null;
 const bytes=await r.arrayBuffer();
 if(bytes.byteLength!==item.bytes||await hash(bytes)!==item.sha256)return null;
 return new Response(bytes,{status:200,headers:r.headers});
}
self.addEventListener('install',e=>e.waitUntil(self.skipWaiting()));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
 if(new URL(e.request.url).pathname!=='/app.js')return;
 e.respondWith((async()=>{
  const c=await readControl(),m=versionFor(c,c.currentBuildId);
  if(!m)return new Response('unassigned',{status:503});
  const item=m.shell.find(i=>i.path==='app.js');
  if(!item)return new Response('not in manifest',{status:503});
  return await verifiedResponse(await caches.open('shell-'+c.currentBuildId),item)
    ||new Response('repair required',{status:503});
 })());
});
"""

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads=True
    allow_reuse_address=True
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        path=self.path.split('?')[0]
        items={'/setup':('<p>fixture</p>','text/html'),
               '/sw.js':(SW,'application/javascript'),
               '/app.js':(GOOD,'application/javascript')}
        if path not in items:
            self.send_response(404);self.end_headers();return
        data,mime=items[path];data=data.encode()
        self.send_response(200)
        self.send_header('content-type',mime)
        self.send_header('cache-control','no-store')
        self.send_header('content-length',str(len(data)))
        self.end_headers();self.wfile.write(data)

def main():
    server=Server(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    cases=[
        ('TRUSTED_CATALOGUE',GOOD,sha(GOOD),True,200,GOOD),
        ('BODY_ONLY_TAMPER',BAD,sha(GOOD),True,503,None),
        ('CATALOGUE_AND_BODY_TAMPER',BAD,sha(BAD),True,200,BAD),
        ('UNVERIFIED_FLAG_WITH_MATCHING_BYTES',GOOD,sha(GOOD),False,200,GOOD),
        ('MALFORMED_CONTROL_FAIL_CLOSED',GOOD,sha(GOOD),True,503,None)]
    evidence=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
            version=browser.version
            for name,body,expected,verified,status,served in cases:
                ctx=browser.new_context()
                try:
                    page=ctx.new_page();page.goto(base+'/setup')
                    page.evaluate("async()=>{await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready}")
                    page.wait_for_function('navigator.serviceWorker.controller!==null')
                    page.evaluate("""async p=>{
                      const b=new TextEncoder().encode(p.body);
                      const manifest={appBuildId:'build-a',shell:[{path:'app.js',bytes:b.byteLength,sha256:p.expected}]};
                      const control={schemaVersion:2,currentBuildId:'build-a',previousBuildId:null,
                        candidateBuildId:null,versions:{'build-a':{manifest,verified:p.verified}},clientBuilds:{}};
                      await(await caches.open('control')).put('/__control.json',
                        new Response(p.malformed?'not-json':JSON.stringify(control)));
                      await(await caches.open('shell-build-a')).put('app.js',
                        new Response(b,{headers:{'content-type':'application/javascript'}}));
                    }""",{'body':body,'expected':expected,'verified':verified,
                           'malformed':name=='MALFORMED_CONTROL_FAIL_CLOSED'})
                    result=page.evaluate("""async()=>{
                      const r=await fetch('/app.js');return {status:r.status,body:await r.text()};
                    }""")
                    assert result['status']==status,(name,result)
                    if served is not None:assert result['body']==served,(name,result)
                    evidence.append({'case':name,'status':result['status'],
                      'servedTrusted':result['body']==GOOD,
                      'servedReplacement':result['body']==BAD,
                      'catalogueVerifiedFlag':verified})
                finally:ctx.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    with open(OUT,'w') as f:
        json.dump({'scope':'reduced source-path synthetic; NOT LogMate',
                   'browser':version,'cases':evidence},f,indent=2)
    print(json.dumps(evidence,indent=2))
    print(f'{len(evidence)}/{len(cases)} synthetic expected-outcome checks PASS')
if __name__=='__main__':main()
