import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {makeWorkerServer,classifyWorkerDom} from './pwa_chromium_worker_durability_lab.mjs';
const result=(phase,overrides={})=>'<html><meta name="fixture-program" content="worker-durability-v1"><pre id="worker-result">'+JSON.stringify({phase,registered:true,active:true,controller:true,waiting:false,version:'v2',sentinel:true,cacheV1:true,cacheV2:true,...overrides})+'</pre></html>';
test('cold offline needs actual controller and synthetic ledger',()=>{assert.equal(classifyWorkerDom(result('offline'),'offline','COMPLETED').verdict,'PASS');assert.equal(classifyWorkerDom(result('offline',{controller:false}),'offline','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom(result('offline',{sentinel:false}),'offline','COMPLETED').verdict,'FAIL');});
test('post-update version and cache independently required',()=>{assert.equal(classifyWorkerDom(result('post-update'),'post-update','COMPLETED').verdict,'PASS');assert.equal(classifyWorkerDom(result('post-update',{version:'v1'}),'post-update','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom(result('post-update',{cacheV2:false}),'post-update','COMPLETED').verdict,'FAIL');});
test('waiting v2 must not seize old controlled client',()=>{assert.equal(classifyWorkerDom(result('update',{version:'v1',waiting:true}),'update','COMPLETED').verdict,'PASS');assert.equal(classifyWorkerDom(result('update',{version:'v2',waiting:true}),'update','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom(result('update',{version:'v1',waiting:false}),'update','COMPLETED').verdict,'FAIL');});
test('initial install is not automatically controlled',()=>{assert.equal(classifyWorkerDom(result('install',{controller:false}),'install','COMPLETED').verdict,'PASS');assert.equal(classifyWorkerDom(result('install'),'install','COMPLETED').verdict,'FAIL');});
test('controlled warm visit requires v1, IDB, cache and controller',()=>{assert.equal(classifyWorkerDom(result('controlled',{version:'v1'}),'controlled','COMPLETED').verdict,'PASS');for(const k of ['sentinel','controller','cacheV1'])assert.equal(classifyWorkerDom(result('controlled',{version:'v1',[k]:false}),'controlled','COMPLETED').verdict,'FAIL');});
test('missing result, wrong phase, wrong fixture never PASS',()=>{assert.equal(classifyWorkerDom('', 'offline','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom('<html><meta name="fixture-program" content="worker-durability-v1"><pre id="worker-result">PENDING</pre></html>','offline','COMPLETED').verdict,'UNKNOWN');assert.equal(classifyWorkerDom(result('controlled'),'offline','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom(result('offline'),'wrong','COMPLETED').verdict,'FAIL');});
test('transport failure cannot PASS from plausible DOM',()=>{for(const reason of ['CHROME_TIMEOUT','CHROME_NONZERO','OUTPUT_LIMIT','CHROME_START_ERROR'])assert.equal(classifyWorkerDom(result('offline'),'offline',reason).verdict,'UNKNOWN');});
test('auth exclusion is a distinct response identity',()=>{const auth='<html><meta name="fixture-program" content="auth-excluded">AUTH_OUTSIDE_SCOPE<pre id="auth-result">{"controller":false,"path":"/auth/action"}</pre></html>';assert.equal(classifyWorkerDom(auth,'auth','COMPLETED').verdict,'PASS');assert.equal(classifyWorkerDom(result('offline'),'auth','COMPLETED').verdict,'FAIL');assert.equal(classifyWorkerDom(auth.replace('false','true'),'auth','COMPLETED').verdict,'FAIL');});
test('server exposes separate app, worker and auth scopes',async()=>{const {server,setVersion,hits}=makeWorkerServer();await new Promise(ok=>server.listen(0,'127.0.0.1',ok));try{const b='http://127.0.0.1:'+server.address().port;const sw1=await (await fetch(b+'/app/sw.js')).text();assert.ok(sw1.includes('synthetic-app-v1'));assert.ok(!sw1.includes('skipWaiting'));assert.ok(!sw1.includes('clients.claim'));assert.ok(sw1.includes("u.pathname==='/app/'"));setVersion('v2');const sw2=await (await fetch(b+'/app/sw.js')).text();assert.ok(sw2.includes('synthetic-app-v2'));assert.ok(sw2.includes('caches.open(CACHE)'));assert.ok(!sw2.includes('caches.match('));assert.notEqual(sw1,sw2);assert.equal((await (await fetch(b+'/app/version.txt')).text()),'v2');assert.ok((await (await fetch(b+'/auth/action')).text()).includes('auth-excluded'));assert.equal((await fetch(b+'/missing')).status,404);assert.ok(hits.includes('/auth/action'));}finally{await new Promise(ok=>server.close(ok));}});

async function transactionProbe(abortFirst=false){
 const {server}=makeWorkerServer();
 await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
 let source;
 try{source=await (await fetch('http://127.0.0.1:'+server.address().port+'/app/client.js')).text();}
 finally{await new Promise(ok=>server.close(ok));}
 const transactions=[];let output='PENDING';let closes=0;
 const database={close:()=>{closes++;},transaction:(_name,mode)=>{
   const t={mode,error:null,oncomplete:null,onabort:null,onerror:null,request:null};
   t.objectStore=()=>({
     put:()=>{t.request={result:undefined,onsuccess:null,onerror:null};return t.request;},
     get:()=>{t.request={result:'SYNTHETIC-LOCAL-LEDGER-20261025',onsuccess:null,onerror:null};return t.request;}
   });
   transactions.push(t);return t;
 }};
 const context={
   URLSearchParams,Date,Promise,Error,setTimeout,
   location:{search:'?phase=controlled'},
   navigator:{serviceWorker:{controller:{},getRegistration:async()=>({active:{state:'activated'},waiting:null})}},
   indexedDB:{open:()=>{const request={result:database,onsuccess:null,onerror:null};queueMicrotask(()=>request.onsuccess());return request;}},
   caches:{keys:async()=>['synthetic-app-v1']},
   fetch:async()=>({text:async()=> 'v1'}),
   document:{getElementById:()=>({set textContent(value){output=value;}})}
 };
 vm.runInNewContext(source,context);
 const tick=()=>new Promise(resolve=>setImmediate(resolve));
 await tick();
 assert.equal(transactions.length,1);
 transactions[0].request.onsuccess();
 await tick();
 assert.equal(transactions.length,1,'request success must not release uncommitted write');
 assert.equal(output,'PENDING','browser result must wait for transaction commit');
 if(abortFirst){
   transactions[0].onabort();
   await tick();
   assert.equal(transactions.length,1);
   assert.match(output,/IDB_TRANSACTION_ABORT/);
   assert.equal(closes,1);
   return;
 }
 transactions[0].oncomplete();
 await tick();
 assert.equal(transactions.length,2,'read starts only after committed write');
 transactions[1].request.onsuccess();
 await tick();
 assert.equal(output,'PENDING','read result must wait for transaction completion');
 transactions[1].oncomplete();
 await tick();
 const parsed=JSON.parse(output);
 assert.equal(parsed.sentinel,true);
 assert.equal(parsed.version,'v1');
 assert.equal(closes,2);
}
test('Worker ledger waits for IDB write and read transaction completion',async()=>{await transactionProbe(false);});
test('aborted IDB transaction cannot emit a successful Worker durability result',async()=>{await transactionProbe(true);});
