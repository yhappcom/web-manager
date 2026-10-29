#!/usr/bin/env python3
"""Disposable Chrome CSP/header-vs-body integrity fixture; NOT LogMate."""
import hashlib,http.server,json,os,socketserver,threading
from playwright.sync_api import sync_playwright
HTML="<html><body><h1>fixture</h1><script>document.documentElement.dataset.ran='yes'</script></body></html>"
CSP="script-src 'none'; object-src 'none'; base-uri 'none'"
HASH=hashlib.sha256(HTML.encode()).hexdigest()
OUT=os.getenv("EVIDENCE_OUT","/tmp/pwa-cached-header-integrity.json")
CHROME=os.getenv("CHROMIUM_PATH","/usr/bin/google-chrome")
def serve(force):
    sw="""
const EXPECTED='HASHVALUE',FORCE=FORCEVALUE,CSP=CSPVALUE;
self.addEventListener('install',e=>e.waitUntil(self.skipWaiting()));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
 if(e.request.mode!=='navigate'||new URL(e.request.url).pathname!=='/')return;
 e.respondWith((async()=>{
  const cached=await(await caches.open('shell')).match('/index.html');
  if(!cached)return new Response('missing',{status:503});
  const bytes=await cached.arrayBuffer();
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
  if(hash!==EXPECTED)return new Response('body rejected',{status:503});
  const headers=new Headers(cached.headers);
  if(FORCE)headers.set('content-security-policy',CSP);
  return new Response(bytes,{status:200,headers});
 })());
});
""".replace("HASHVALUE",HASH).replace("FORCEVALUE","true" if force else "false").replace("CSPVALUE",json.dumps(CSP))
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*a):pass
        def do_GET(self):
            path=self.path.split("?")[0]
            data,mime=({"/setup":("<p>setup</p>","text/html"),
                         "/index.html":(HTML,"text/html"),
                         "/sw.js":(sw,"application/javascript")}).get(path,(None,None))
            if data is None:self.send_response(404);self.end_headers();return
            b=data.encode();self.send_response(200)
            self.send_header("content-type",mime)
            self.send_header("cache-control","no-store")
            if path=="/index.html":self.send_header("content-security-policy",CSP)
            self.send_header("content-length",str(len(b)));self.end_headers();self.wfile.write(b)
    class Server(socketserver.ThreadingMixIn,http.server.HTTPServer):
        daemon_threads=True
        allow_reuse_address=True
    s=Server(("127.0.0.1",0),Handler)
    threading.Thread(target=s.serve_forever,daemon=True).start()
    return s,"http://127.0.0.1:%s"%s.server_port
def main():
    cases=[("BASELINE",False,"none",200,False,True),
           ("CSP_HEADER_STRIPPED",False,"strip",200,True,False),
           ("WORKER_REAPPLIES_CSP",True,"strip",200,False,True),
           ("BODY_CHANGED",False,"body",503,False,False),
           ("MIME_ONLY_CHANGED",False,"mime",200,False,True)]
    evidence=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=CHROME,headless=True,args=["--no-sandbox"])
        version=browser.version
        for name,force,mutation,status,ran,csp_present in cases:
            server,base=serve(force);ctx=browser.new_context()
            try:
                page=ctx.new_page();page.goto(base+"/setup")
                page.evaluate("""async()=>{await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready}""")
                page.wait_for_function("navigator.serviceWorker.controller!==null")
                seed=page.evaluate("""async mutation=>{
                    const src=await fetch('/index.html'),body=await src.text(),h=new Headers(src.headers);
                    if(mutation==='strip')h.delete('content-security-policy');
                    if(mutation==='mime')h.set('content-type','text/plain');
                    await(await caches.open('shell')).put('/index.html',new Response(
                       mutation==='body'?body+'!':body,{status:200,headers:h}));
                    const stored=await(await caches.open('shell')).match('/index.html');
                    return {sourceCsp:src.headers.get('content-security-policy'),
                      sourceCacheControl:src.headers.get('cache-control'),
                      storedCsp:stored.headers.get('content-security-policy')};
                }""",mutation)
                r=page.goto(base+"/",wait_until="load")
                actual=page.evaluate("document.documentElement.dataset.ran==='yes'")
                h=r.headers
                assert r.status==status,(name,"status",r.status)
                assert actual==ran,(name,"inline",actual)
                assert bool(h.get("content-security-policy"))==csp_present,(name,"CSP",h)
                assert seed["sourceCsp"]==CSP and seed["sourceCacheControl"]=="no-store",seed
                if mutation=="strip":assert seed["storedCsp"] is None
                if mutation=="mime":assert h.get("content-type")=="text/plain",h
                evidence.append({"case":name,"status":r.status,"inlineExecuted":actual,
                    "csp":h.get("content-security-policy"),"mime":h.get("content-type"),
                    "sourceNoStore":seed["sourceCacheControl"],"sha256":HASH})
            finally:ctx.close();server.shutdown();server.server_close()
        browser.close()
    with open(OUT,"w") as f:json.dump({"scope":"synthetic; NOT LogMate","browser":version,"cases":evidence},f,indent=2)
    print(json.dumps(evidence,indent=2))
    print(f"{len(evidence)}/5 synthetic checks PASS")
if __name__=="__main__":main()
