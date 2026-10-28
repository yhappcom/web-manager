#!/usr/bin/env python3
"""Disposable synthetic Chrome repair-liveness experiment; NOT LogMate code."""
import hashlib
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

ASSETS = {
    "/index.html": b"<!doctype html><html><body><h1>Offline fixture</h1></body></html>",
    "/app.js": b'window.SYNTHETIC_APP_VERSION="v1";',
    "/font.woff2": b"SYNTHETIC_FONT_BYTES",
}
HASH = {k: hashlib.sha256(v).hexdigest() for k, v in ASSETS.items()}
SERVER_ASSETS = dict(ASSETS)
REQUESTS = []
SW = r"""
const ASSETS=__MANIFEST__;
const CACHE='synthetic-repair-shell-v1';
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
async function verified(cache,path){
  let r=await cache.match(path);if(!r)return null;
  let b=await r.arrayBuffer();if(await sha(b)!==ASSETS[path])return null;
  let mime=path.endsWith('.js')?'text/javascript':path.endsWith('.html')?'text/html':'application/octet-stream';
  return new Response(b,{status:200,headers:{'content-type':mime}});
}
async function repair(paths){
  let c=await caches.open(CACHE),results={};
  for(let path of paths){
    try{
      let r=await fetch(new Request(path,{cache:'no-store'}));
      if(!r.ok)throw Error('http');
      let b=await r.arrayBuffer();
      if(await sha(b)!==ASSETS[path])throw Error('digest');
      await c.put(path,new Response(b));results[path]='repaired';
    }catch(e){results[path]='rejected:'+String(e.message)}
  }
  return results;
}
self.addEventListener('install',e=>e.waitUntil(repair(Object.keys(ASSETS)).then(r=>{
  if(Object.values(r).some(v=>v!=='repaired'))throw Error('initial install incomplete');
})));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  let path=new URL(e.request.url).pathname;
  if(e.request.method!=='GET'||!(path in ASSETS))return;
  e.respondWith((async()=>await verified(await caches.open(CACHE),path)
    ||new Response('repair required',{status:503}))());
});
self.addEventListener('message',e=>{
  if(!e.ports[0])return;
  let paths=e.data.type==='REPAIR_FONT_ONLY'?['/font.woff2']
    :e.data.type==='REPAIR_FULL'?Object.keys(ASSETS):[];
  e.waitUntil(repair(paths).then(r=>e.ports[0].postMessage(r)));
});
""".replace("__MANIFEST__", json.dumps(HASH))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.append(self.path)
        if self.path == "/sw.js":
            data, mime = SW.encode(), "text/javascript"
        elif self.path in SERVER_ASSETS:
            data = SERVER_ASSETS[self.path]
            mime = ("text/html" if self.path.endswith(".html") else
                    "text/javascript" if self.path.endswith(".js") else
                    "application/octet-stream")
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def run():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{server.server_port}"
    results = []

    def check(name, passed, detail):
        results.append({"case": name, "pass": bool(passed), "detail": detail})
        print(f"{name}: {'PASS' if passed else 'FAIL'} — {detail}", flush=True)
        if not passed:
            raise AssertionError(name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
                args=["--no-sandbox"],
            )
            try:
                context = browser.new_context(service_workers="allow")
                page = context.new_page()
                page.goto(origin + "/index.html")
                page.evaluate("""async()=>{
                  await navigator.serviceWorker.register('/sw.js');
                  await navigator.serviceWorker.ready;
                  if(!navigator.serviceWorker.controller)
                    await new Promise(r=>navigator.serviceWorker.addEventListener('controllerchange',r,{once:true}));
                }""")
                page.reload()

                def response(path):
                    return page.evaluate("""async path=>{
                      let r=await fetch(path);return {status:r.status,body:await r.text()};
                    }""", path)

                def mutate(path, mode):
                    return page.evaluate("""async ({path,mode})=>{
                      let c=await caches.open('synthetic-repair-shell-v1');
                      if(mode==='delete')await c.delete(path);
                      else await c.put(path,new Response('TAMPERED'));
                    }""", {"path": path, "mode": mode})

                def repair(kind):
                    return page.evaluate("""kind=>new Promise((resolve,reject)=>{
                      let ch=new MessageChannel();ch.port1.onmessage=e=>resolve(e.data);
                      navigator.serviceWorker.controller.postMessage({type:kind},[ch.port2]);
                      setTimeout(()=>reject(Error('timeout')),5000);
                    })""", kind)

                check("RL-S01", response("/app.js")["status"] == 200, "initial verified shell")
                page.evaluate("""()=>new Promise((resolve,reject)=>{
                  let r=indexedDB.open('synthetic-ledger',1);
                  r.onupgradeneeded=()=>r.result.createObjectStore('records');
                  r.onsuccess=()=>{
                    let t=r.result.transaction('records','readwrite');
                    t.objectStore('records').put('preserve-me','flight-sentinel');
                    t.oncomplete=()=>resolve(true);t.onerror=reject;
                  };
                })""")
                mutate("/app.js", "delete")
                check("RL-S02", response("/app.js")["status"] == 503, "missing shell fails closed")
                before = REQUESTS.count("/app.js")
                repair("REPAIR_FONT_ONLY")
                check("RL-S03", response("/app.js")["status"] == 503 and
                      REQUESTS.count("/app.js") == before, "font-only repair cannot heal shell")
                outcome = repair("REPAIR_FULL")
                check("RL-S04", response("/app.js")["status"] == 200 and
                      outcome["/app.js"] == "repaired", "online hash-verified repair")
                mutate("/app.js", "corrupt")
                check("RL-S05", response("/app.js")["status"] == 503, "corrupt cached bytes rejected")
                SERVER_ASSETS["/app.js"] = b"ATTACKER_CHANGED_BYTES"
                outcome = repair("REPAIR_FULL")
                check("RL-S06", response("/app.js")["status"] == 503 and
                      outcome["/app.js"].startswith("rejected:digest"), "changed origin bytes rejected")
                SERVER_ASSETS["/app.js"] = ASSETS["/app.js"]
                repair("REPAIR_FULL")
                check("RL-S07", response("/app.js")["status"] == 200, "valid origin restored")
                mutate("/app.js", "delete")
                context.set_offline(True)
                outcome = repair("REPAIR_FULL")
                check("RL-S08", response("/app.js")["status"] == 503 and
                      outcome["/app.js"].startswith("rejected:"), "offline cannot claim repair")
                sentinel = page.evaluate("""()=>new Promise((resolve,reject)=>{
                  let r=indexedDB.open('synthetic-ledger');
                  r.onsuccess=()=>{
                    let t=r.result.transaction('records');
                    let q=t.objectStore('records').get('flight-sentinel');
                    q.onsuccess=()=>resolve(q.result);q.onerror=reject;
                  };
                })""")
                check("RL-S09", sentinel == "preserve-me", "IDB sentinel preserved")
                context.set_offline(False)
                repair("REPAIR_FULL")
                check("RL-S10", response("/app.js")["status"] == 200, "post-offline recovery")
                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        output = {"cases": results, "passed": sum(x["pass"] for x in results),
                  "total": len(results), "scope": "synthetic browser fixture; NOT LogMate"}
        if os.environ.get("EVIDENCE_OUT"):
            with open(os.environ["EVIDENCE_OUT"], "w") as file:
                json.dump(output, file, indent=2)
        print(json.dumps(output, indent=2))
    if len(results) != 10:
        raise AssertionError("missing expected cases")


if __name__ == "__main__":
    run()
