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

async function runCase(name, port, withShadow) {
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
        headers: [{source:'**',headers:[{key:'Cache-Control',value:'no-cache, no-store, must-revalidate'}]}],
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
      result[route]={initialStatus:initial.status,location:initial.headers.get('location'),finalStatus:final.status,finalPath:new URL(final.url).pathname,marker};
    }
    console.log(JSON.stringify({case:name,cliVersion:process.env.FIREBASE_CLI_PIN||'unknown',routes:result},null,2));
    return result;
  } finally {
    if (child && child.exitCode===null) {child.kill('SIGTERM');await Promise.race([new Promise(resolve=>child.once('exit',resolve)),sleep(3500)]);if(child.exitCode===null)child.kill('SIGKILL');}
    await fs.rm(dir,{recursive:true,force:true});
  }
}
const baseline=await runCase('baseline',5511,false);
const shadow=await runCase('auth-index-shadow',5512,true);
// Assertions are intentionally explicit: if Hosting serves different content
// or redirects unexpectedly, the experiment FAILS rather than calling it PASS.
assert.equal(baseline['/'].marker,'ROOT','root control must remain distinct');
for(const alias of ['/auth','/auth/','/auth/action','/auth/action/','/auth/action/index.html']){
  assert.equal(baseline[alias].finalStatus,200,alias+' must resolve to HTTP 200');
  assert.equal(baseline[alias].marker,'AUTH',alias+' must serve intended auth action document');
}
assert.equal(shadow['/'].marker,'ROOT','shadow must not change root');
assert.equal(shadow['/auth/'].marker,'SHADOW','auth/index.html must expose static priority counterexample');
console.log('EMULATOR ROUTE GATE PASS: baseline auth aliases and static shadow observed; live HTTPS/Safari/managed iPad remain OPEN');
