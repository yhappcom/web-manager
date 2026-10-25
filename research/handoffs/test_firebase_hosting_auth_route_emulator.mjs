#!/usr/bin/env node
// Isolated Firebase Hosting emulator experiment; no production project, credentials,
// deploy, authentication token, or user data. This is NOT a live HTTPS oracle.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const cli = process.argv[2];
if (!cli) throw new Error('usage: node test_firebase_hosting_auth_route_emulator.mjs <pinned-firebase-cli>');
const AUTH = '<!doctype html><title>AUTH_SENTINEL</title><h1>AUTH_SENTINEL</h1>';
const ROOT = '<!doctype html><title>ROOT_SENTINEL</title><h1>ROOT_SENTINEL</h1>';
const SHADOW = '<!doctype html><title>SHADOW_SENTINEL</title><h1>SHADOW_SENTINEL</h1>';
const ROUTES = ['/','/auth','/auth/','/auth/action','/auth/action/','/auth/action/index.html'];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function runCase(name, port, withShadow, withPolicy=false) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'webmgr-hosting-route-'));
  const publicDir = path.join(dir, 'public');
  let child;
  let logs = '';
  try {
    await fs.mkdir(path.join(publicDir, 'auth/action'), {recursive:true});
    await fs.writeFile(path.join(publicDir,'index.html'), ROOT);
    await fs.writeFile(path.join(publicDir,'auth/action/index.html'), AUTH);
    if (withShadow) await fs.writeFile(path.join(publicDir,'auth/index.html'), SHADOW);
    const config = {
      hosting: {
        public: 'public',
        ignore: ['firebase.json','**/.*','**/node_modules/**'],
        headers: [
          {source:'**',headers:[{key:'Cache-Control',value:'no-cache, no-store, must-revalidate'}]},
          ...(withPolicy ? ['/auth','/auth/','/auth/action','/auth/action/','/auth/action/index.html'].map(source=>({
            source,headers:[{key:'Referrer-Policy',value:'no-referrer'}],
          })) : []),
        ],
        rewrites: [
          {source:'/auth',destination:'/auth/action/index.html'},
          {source:'/auth/',destination:'/auth/action/index.html'},
          {source:'/auth/action',destination:'/auth/action/index.html'},
        ],
      },
      emulators: {hosting:{host:'127.0.0.1',port},ui:{enabled:false}},
    };
    const configPath = path.join(dir,'firebase.json');
    await fs.writeFile(configPath,JSON.stringify(config,null,2));
    child = spawn(cli, ['emulators:start','--only','hosting','--project','demo-webmgr-routing','--config',configPath,'--non-interactive'], {
      cwd:dir, env:{...process.env,CI:'true',FIREBASE_CLI_EXPERIMENTS:''}, stdio:['ignore','pipe','pipe'],
    });
    child.stdout.on('data',d=>{logs=(logs+d.toString()).slice(-10000);});
    child.stderr.on('data',d=>{logs=(logs+d.toString()).slice(-10000);});
    const base = 'http://127.0.0.1:'+port;
    let ready=false;
    for (let i=0;i<90;i++) {
      if (child.exitCode!==null) break;
      try {
        const r=await fetch(base+'/',{signal:AbortSignal.timeout(1200)});
        if (r.status===200 && (await r.text()).includes('ROOT_SENTINEL')) {ready=true;break;}
      } catch {}
      await sleep(400);
    }
    if (!ready) throw new Error('Hosting emulator not ready; last log: '+logs.slice(-3500));
    const result={};
    for (const route of ROUTES) {
      const initial=await fetch(base+route,{redirect:'manual',signal:AbortSignal.timeout(4000)});
      const final=await fetch(base+route,{redirect:'follow',signal:AbortSignal.timeout(4000)});
      const body=await final.text();
      const marker=body.includes('AUTH_SENTINEL')?'AUTH':body.includes('SHADOW_SENTINEL')?'SHADOW':body.includes('ROOT_SENTINEL')?'ROOT':'OTHER';
      result[route]={
        initialStatus:initial.status,location:initial.headers.get('location'),
        finalStatus:final.status,finalPath:new URL(final.url).pathname,marker,
        initialReferrerPolicy:initial.headers.get('referrer-policy'),
        finalReferrerPolicy:final.headers.get('referrer-policy'),
        initialCacheControl:initial.headers.get('cache-control'),
        finalCacheControl:final.headers.get('cache-control'),
      };
    }
    // Synthetic query probe only; never use real Firebase action codes or print URLs.
    const fakeCode='SYNTHETIC_NON_SECRET';
    const query='?mode=resetPassword&oobCode='+fakeCode;
    const queryProbe={};
    for(const route of ['/auth','/auth/action']){
      const initial=await fetch(base+route+query,{redirect:'manual',signal:AbortSignal.timeout(4000)});
      const final=await fetch(base+route+query,{redirect:'follow',signal:AbortSignal.timeout(4000)});
      const body=await final.text();
      const location=initial.headers.get('location');
      queryProbe[route]={
        initialStatus:initial.status,
        redirectPreservedQuery:initial.status>=300&&initial.status<400
          ? new URL(location,base).searchParams.get('oobCode')===fakeCode
          : null,
        finalPreservedQuery:new URL(final.url).searchParams.get('oobCode')===fakeCode,
        finalStatus:final.status,
        finalMarker:body.includes('AUTH_SENTINEL')?'AUTH':body.includes('SHADOW_SENTINEL')?'SHADOW':'OTHER',
        initialReferrerPolicy:initial.headers.get('referrer-policy'),
        finalReferrerPolicy:final.headers.get('referrer-policy'),
        initialCacheControl:initial.headers.get('cache-control'),
      };
    }
    console.log(JSON.stringify({case:name,cliVersion:process.env.FIREBASE_CLI_PIN||'unknown',routes:result,queryProbe},null,2));
    result.queryProbe=queryProbe;
    return result;
  } finally {
    if (child && child.exitCode===null) {child.kill('SIGTERM');await Promise.race([new Promise(resolve=>child.once('exit',resolve)),sleep(3500)]);if(child.exitCode===null)child.kill('SIGKILL');}
    await fs.rm(dir,{recursive:true,force:true});
  }
}
const baseline=await runCase('baseline',5511,false);
const shadow=await runCase('auth-index-shadow',5512,true);
const protectedBaseline=await runCase('auth-referrer-policy',5513,false,true);
const protectedShadow=await runCase('auth-referrer-policy-shadow',5514,true,true);
// Assertions are intentionally explicit: if Hosting serves different content
// or redirects unexpectedly, the experiment FAILS rather than calling it PASS.
assert.equal(baseline['/'].marker,'ROOT','root control must remain distinct');
for(const alias of ['/auth','/auth/','/auth/action','/auth/action/','/auth/action/index.html']){
  assert.equal(baseline[alias].finalStatus,200,alias+' must resolve to HTTP 200');
  assert.equal(baseline[alias].marker,'AUTH',alias+' must serve intended auth action document');
}
assert.equal(shadow['/'].marker,'ROOT','shadow must not change root');
assert.equal(shadow['/auth/'].marker,'SHADOW','auth/index.html must expose static priority counterexample');
assert.equal(baseline['/auth/action'].initialStatus,301,'existing auth/action directory should redirect in this pinned emulator');
assert.equal(shadow['/auth'].initialStatus,301,'shadow auth/index.html should redirect /auth in this pinned emulator');
for(const [label,observed] of [['baseline',baseline],['shadow',shadow]]){
  for(const alias of ['/auth','/auth/action']){
    assert.equal(observed.queryProbe[alias].finalPreservedQuery,true,label+' '+alias+' query must survive navigation');
    assert.equal(observed.queryProbe[alias].finalStatus,200,label+' '+alias+' final HTTP 200');
    if(observed.queryProbe[alias].redirectPreservedQuery!==null){
      assert.equal(observed.queryProbe[alias].redirectPreservedQuery,true,label+' '+alias+' redirect must preserve synthetic query');
    }
  }
}
assert.equal(baseline.queryProbe['/auth/action'].finalMarker,'AUTH');
assert.equal(shadow.queryProbe['/auth'].finalMarker,'SHADOW');
// Referrer policy must be attached to each requested URL, not only to the rewrite
// destination. The 301 is separately observed because final-200 policy cannot
// prove redirect-hop policy. These are HTTP-emulator checks, not browser Referer.
for (const alias of ['/auth','/auth/','/auth/action','/auth/action/','/auth/action/index.html']) {
  assert.equal(baseline[alias].finalReferrerPolicy,null,alias+' negative-control policy must be absent');
  assert.equal(protectedBaseline[alias].finalStatus,200,alias+' protected final response');
  assert.equal(protectedBaseline[alias].marker,'AUTH',alias+' protected content identity');
  assert.equal(protectedBaseline[alias].finalReferrerPolicy,'no-referrer',alias+' must have final response policy');
}
assert.equal(protectedBaseline['/'].finalReferrerPolicy,null,'root must not acquire auth-only policy');
assert.equal(protectedShadow['/auth/'].marker,'SHADOW','policy must not mask static shadow');
assert.equal(protectedShadow['/auth/'].finalReferrerPolicy,'no-referrer','static shadow still gets matched policy');
for(const alias of ['/auth','/auth/action']){
  assert.equal(protectedBaseline.queryProbe[alias].finalPreservedQuery,true,'policy does not remove initial query: '+alias);
  assert.equal(protectedBaseline.queryProbe[alias].finalReferrerPolicy,'no-referrer','query probe final policy: '+alias);
}
console.log('EMULATOR ROUTE/POLICY GATE PASS: synthetic aliases, shadow, per-request referrer header and query continuity; redirect-hop header observations printed separately; HTTPS/browser/Safari/managed iPad OPEN');
