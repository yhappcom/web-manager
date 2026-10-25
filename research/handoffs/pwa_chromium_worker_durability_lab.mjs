// Research-only Chromium loopback SW/IDB/Cache lab; not product, HTTPS, Safari, MDM or backup proof.
import http from 'node:http';
import {mkdtemp,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {visit} from './pwa_chromium_csp_runtime_lab.mjs';
const phases=['install','controlled','update','post-update','auth','offline'];
const script=String.raw`(async()=>{
const phase=new URLSearchParams(location.search).get('phase')||'unknown';
const result={phase,controller:!!navigator.serviceWorker?.controller,active:false,waiting:false,version:null,sentinel:false,cacheV1:false,cacheV2:false,registered:false};
const out=()=>{document.getElementById('worker-result').textContent=JSON.stringify(result)};
const db=()=>new Promise((resolve,reject)=>{const r=indexedDB.open('pwa-synthetic-ledger',1);r.onupgradeneeded=()=>r.result.createObjectStore('ledger');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
const ledger=async(write)=>{const d=await db();return await new Promise((resolve,reject)=>{const t=d.transaction('ledger',write?'readwrite':'readonly');const s=t.objectStore('ledger');const q=write?s.put('SYNTHETIC-LOCAL-LEDGER-20261025','sentinel'):s.get('sentinel');q.onsuccess=()=>resolve(write?true:q.result==='SYNTHETIC-LOCAL-LEDGER-20261025');q.onerror=()=>reject(q.error);t.oncomplete=()=>d.close();});};
try {
 if(!('serviceWorker' in navigator))throw Error('NO_SERVICE_WORKER');
 let reg=await navigator.serviceWorker.getRegistration('/app/');
 if(phase==='install') {reg=await navigator.serviceWorker.register('/app/sw.js',{scope:'/app/',updateViaCache:'none'});await navigator.serviceWorker.ready;}
 if(!reg)throw Error('NO_REGISTRATION');
 if(phase==='update'){
   await reg.update();
   const start=Date.now();
   while(!reg.waiting&&Date.now()-start<3500)await new Promise(r=>setTimeout(r,100));
 }
 result.registered=true;result.active=reg.active?.state==='activated';result.waiting=!!reg.waiting;
 if(phase==='controlled')await ledger(true);
 if(phase!=='install')result.sentinel=await ledger(false);
 if(phase!=='install'){const r=await fetch('/app/version.txt',{cache:'no-store'});result.version=(await r.text()).trim();}
 const keys=await caches.keys();result.cacheV1=keys.includes('synthetic-app-v1');result.cacheV2=keys.includes('synthetic-app-v2');
 result.controller=!!navigator.serviceWorker.controller;
}catch(e){result.error=String(e?.name||'Error')+':'+String(e?.message||'').slice(0,80)}
out();
})();`;
const html='<!doctype html><html><head><meta charset="utf-8"><meta name="fixture-program" content="worker-durability-v1"></head><body><pre id="worker-result">PENDING</pre><script src="/app/client.js"></script></body></html>';
const worker=v=>`const VERSION=${JSON.stringify(v)};const CACHE='synthetic-app-${v}';\n`+
`self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/app/','/app/version.txt','/app/client.js'])))});\n`+
`self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==self.location.origin)return;`+
`if(e.request.mode==='navigate'&&u.pathname==='/app/'){e.respondWith(caches.open(CACHE).then(c=>c.match('/app/')).then(r=>r||fetch(e.request)));return;}`+
`if(u.pathname==='/app/version.txt'||u.pathname==='/app/client.js'){e.respondWith(caches.open(CACHE).then(c=>c.match(u.pathname)).then(r=>r||fetch(e.request)));}});\n`;
export function makeWorkerServer(){
 let version='v1';const hits=[];
 const server=http.createServer((req,res)=>{
   const u=new URL(req.url,'http://127.0.0.1');hits.push(u.pathname);
   const common={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
   const send=(status,type,body)=>{res.writeHead(status,{...common,'Content-Type':type});res.end(body)};
   if(u.pathname==='/app/sw.js')return send(200,'text/javascript',worker(version));
   if(u.pathname==='/app/client.js')return send(200,'text/javascript',script);
   if(u.pathname==='/app/version.txt')return send(200,'text/plain',version);
   if(u.pathname==='/app/')return send(200,'text/html',html);
   if(u.pathname==='/auth/action')return send(200,'text/html','<!doctype html><html><head><meta name="fixture-program" content="auth-excluded"></head><body>AUTH_OUTSIDE_SCOPE<pre id="auth-result">PENDING</pre><script>document.querySelector("#auth-result").textContent=JSON.stringify({controller:!!navigator.serviceWorker?.controller,path:location.pathname})</script></body></html>');
   return send(404,'text/plain','NOT_FOUND');
 });
 return {server,setVersion:v=>{if(!['v1','v2'].includes(v))throw Error('INVALID_VERSION');version=v;},hits};
}
export function classifyWorkerDom(output,phase,processReason){
 if(!phases.includes(phase))return {verdict:'FAIL',reason:'UNKNOWN_PHASE'};
 if(processReason!=='COMPLETED')return {verdict:'UNKNOWN',reason:'BROWSER_'+String(processReason||'NO_PROCESS')};
 if(phase==='auth'){const m=/<pre id="auth-result">([^<]*)<\/pre>/.exec(output);if(!output.includes('content="auth-excluded"')||!output.includes('AUTH_OUTSIDE_SCOPE'))return {verdict:'FAIL',reason:'AUTH_ROUTE_MISMATCH'};if(!m||m[1]==='PENDING')return {verdict:'UNKNOWN',reason:'AUTH_PROBE_NOT_COMPLETED'};try{const x=JSON.parse(m[1].replaceAll('&amp;','&'));return x.controller===false&&x.path==='/auth/action'?{verdict:'PASS',reason:'EXCLUDED_ROUTE_UNCONTROLLED'}:{verdict:'FAIL',reason:'AUTH_CONTROLLED_OR_WRONG_PATH'};}catch{return {verdict:'FAIL',reason:'INVALID_AUTH_JSON'};}}
 if(!output.includes('name="fixture-program" content="worker-durability-v1"'))return {verdict:'FAIL',reason:'WRONG_FIXTURE'};
 const m=/<pre id="worker-result">([^<]*)<\/pre>/.exec(output);
 if(!m||m[1]==='PENDING')return {verdict:'UNKNOWN',reason:'NO_COMPLETED_PROBE'};
 let x;try{x=JSON.parse(m[1].replaceAll('&amp;','&'));}catch{return {verdict:'FAIL',reason:'INVALID_PROBE_JSON'};}
 if(!x||x.phase!==phase||x.error||typeof x.controller!=='boolean'||typeof x.registered!=='boolean')return {verdict:'FAIL',reason:'INVALID_PHASE_OR_ERROR'};
 const req={
  install:{registered:true,active:true,controller:false,cacheV1:true},
  controlled:{registered:true,active:true,controller:true,version:'v1',sentinel:true,cacheV1:true},
  update:{registered:true,active:true,controller:true,waiting:true,version:'v1',sentinel:true,cacheV1:true,cacheV2:true},
  'post-update':{registered:true,active:true,controller:true,waiting:false,version:'v2',sentinel:true,cacheV2:true},
  offline:{registered:true,active:true,controller:true,version:'v2',sentinel:true,cacheV2:true}
 }[phase];
 for(const [k,v] of Object.entries(req))if(x[k]!==v)return {verdict:'FAIL',reason:'ORACLE_'+k.toUpperCase()};
 return {verdict:'PASS',reason:'WORKER_CONTROL_VERSION_AND_DATA_ORACLES'};
}
function findChrome(){for(const p of [process.env.CHROME_PATH,'/usr/bin/google-chrome','/usr/bin/chromium'].filter(Boolean))try{return {path:p,version:execFileSync(p,['--version'],{encoding:'utf8',timeout:3000}).trim()};}catch{}return null;}
export async function runWorkerLab(){
 const chrome=findChrome();if(!chrome)return {tier:'CHROMIUM_LOOPBACK_SYNTHETIC_NO_TLS',verdict:'UNKNOWN',reason:'NO_CHROME',cases:[]};
 const {server,setVersion}=makeWorkerServer();await new Promise((ok,bad)=>{server.once('error',bad);server.listen(0,'127.0.0.1',ok)});
 const port=server.address().port;const base='http://127.0.0.1:'+port;
 const profile=await mkdtemp(path.join(os.tmpdir(),'pwa-worker-lab-'));const cases=[];
 try{
  for(const phase of phases){
   if(phase==='update')setVersion('v2');
   if(phase==='offline')await new Promise(ok=>server.close(ok));
   const url=phase==='auth'?base+'/auth/action':base+'/app/?phase='+phase;
   const r=await visit(chrome.path,url,profile);
   const result=classifyWorkerDom(r.output,phase,r.reason);
   cases.push({phase,...result,processReason:r.reason});
   if(result.verdict!=='PASS')break;
  }
 }finally{
  if(server.listening)await new Promise(ok=>server.close(ok));
  try{await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:200})}catch{}
 }
 return {tier:'CHROMIUM_LOOPBACK_SYNTHETIC_NO_TLS',browser:chrome.version,verdict:cases.length===phases.length&&cases.every(c=>c.verdict==='PASS')?'PASS':cases.some(c=>c.verdict==='FAIL')?'FAIL':'UNKNOWN',cases,caveat:'No HTTPS, approved product, Safari, managed iPad, real data restore or storage-pressure proof'};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){const r=await runWorkerLab();process.stdout.write(JSON.stringify(r,null,2)+'\n');process.exitCode=r.verdict==='PASS'?0:r.verdict==='FAIL'?1:2;}
