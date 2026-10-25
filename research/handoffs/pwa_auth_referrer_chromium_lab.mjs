#!/usr/bin/env node
// Synthetic Chromium Referer experiment: loopback HTTP only, no real action code,
// account, product build, Firebase project, third-party network or token-bearing logs.
import assert from 'node:assert/strict';
import http from 'node:http';
import {spawn,execFileSync} from 'node:child_process';
import {mkdtemp,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const SENTINEL='SYNTHETIC_NOT_A_SECRET_6b84';
const CASES=[
  {id:'baseline',header:false,cleanup:false,redirect:false},
  {id:'protected',header:true,cleanup:false,redirect:false},
  {id:'cleanup-only',header:false,cleanup:true,redirect:false},
  {id:'protected-cleanup',header:true,cleanup:true,redirect:false},
  {id:'redirect-protected',header:true,cleanup:false,redirect:true},
  {id:'redirect-final-only',header:true,cleanup:false,redirect:true,hopPolicy:false}
];
const seen=new Map();
const listen=s=>new Promise((ok,bad)=>{s.once('error',bad);s.listen(0,'127.0.0.1',ok);});
const close=s=>new Promise(ok=>{s.closeAllConnections();s.close(ok);});
function ref(value){
  if(!value)return {present:false,hasToken:false,originOnly:false};
  try{const u=new URL(value);return {present:true,hasToken:u.searchParams.get('oobCode')===SENTINEL,originOnly:value===u.origin+'/'};}
  catch{return {present:true,hasToken:false,originOnly:false,invalid:true};}
}
function chrome(){
  for(const p of [process.env.CHROME_PATH,'/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser'].filter(Boolean)){
    try{return {path:p,version:execFileSync(p,['--version'],{encoding:'utf8',timeout:3000}).trim()};}catch{}
  }
  return null;
}
async function visit(binary,url,profile){
  return await new Promise(resolve=>{
    const args=['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage',
      '--no-first-run','--no-default-browser-check','--disable-extensions','--disable-background-networking',
      '--dump-dom','--user-data-dir='+profile,url];
    const p=spawn(binary,args,{detached:process.platform!=='win32',stdio:['ignore','pipe','pipe']});
    let output='',done=false;
    const finish=reason=>{if(done)return;done=true;clearTimeout(timer);p.stdout.destroy();p.stderr.destroy();resolve({reason,domReady:output.includes('REFERRER_PROBE_DONE')});};
    const kill=()=>{try{if(process.platform!=='win32'&&p.pid)process.kill(-p.pid,'SIGKILL');else p.kill('SIGKILL');}catch{}};
    const timer=setTimeout(()=>{kill();finish('TIMEOUT');},16000);
    p.stdout.on('data',b=>{output+=b.toString();if(output.length>180000){kill();finish('OUTPUT_LIMIT');}});
    p.stderr.on('data',()=>{});
    p.on('error',()=>finish('START_ERROR'));
    p.on('close',code=>finish(code===0?'COMPLETED':'NONZERO'));
  });
}
export function classifyCase(c,r,b){
  if(!b||b.reason!=='COMPLETED'||!b.domReady)return {verdict:'UNKNOWN',reason:'BROWSER_OR_DOCUMENT_INCOMPLETE'};
  if(!r||!r.early||!r.late||!r.cross||!r.document)return {verdict:'FAIL',reason:'MISSING_REQUEST_EVIDENCE'};
  if([r.early,r.late,r.cross].some(x=>x.invalid))return {verdict:'FAIL',reason:'INVALID_REFERER_VALUE'};
  if(!r.document.queryPreserved)return {verdict:'FAIL',reason:'DOCUMENT_QUERY_NOT_RECEIVED'};
  if(c.redirect&&!r.redirect)return {verdict:'FAIL',reason:'REDIRECT_NOT_OBSERVED'};
  if(c.redirect&&!r.redirect.queryPreserved)return {verdict:'FAIL',reason:'REDIRECT_LOCATION_QUERY_LOST'};
  if(r.early.hasToken!==!c.header)return {verdict:'FAIL',reason:'EARLY_SAME_ORIGIN_REFERER_MISMATCH'};
  if(r.late.hasToken!==(!c.header&&!c.cleanup))return {verdict:'FAIL',reason:'LATE_SAME_ORIGIN_REFERER_MISMATCH'};
  if(r.early.present!==!c.header||r.late.present!==!c.header)return {verdict:'FAIL',reason:'SAME_ORIGIN_HEADER_PRESENCE_MISMATCH'};
  if(r.cross.hasToken)return {verdict:'FAIL',reason:'CROSS_ORIGIN_TOKEN_PRESENT'};
  if(r.cross.present!==!c.header)return {verdict:'FAIL',reason:'CROSS_ORIGIN_HEADER_PRESENCE_MISMATCH'};
  if(!c.header&&!r.cross.originOnly)return {verdict:'FAIL',reason:'CROSS_ORIGIN_NOT_ORIGIN_ONLY'};
  return {verdict:'PASS',reason:'REAL_CHROMIUM_REQUEST_REFERER_ORACLES'};
}
export async function runLab(){
  const browser=chrome();
  if(!browser)return {tier:'SYNTHETIC_CHROMIUM_LOOPBACK_HTTP',verdict:'UNKNOWN',reason:'NO_CHROMIUM',cases:[]};
  let main;
  const cross=http.createServer((req,res)=>{
    const u=new URL(req.url,'http://127.0.0.1');
    if(u.pathname!=='/cross.js'){res.writeHead(404);return res.end();}
    const r=seen.get(u.searchParams.get('id'));
    if(r)r.cross=ref(req.headers.referer);
    res.writeHead(200,{'Content-Type':'application/javascript','Cache-Control':'no-store'});
    res.end('window.__crossLoaded=true;');
  });
  await listen(cross);
  const crossPort=cross.address().port;
  main=http.createServer((req,res)=>{
    const u=new URL(req.url,'http://127.0.0.1');
    const id=u.searchParams.get('id'),c=CASES.find(x=>x.id===id),r=seen.get(id);
    if(!c||!r){res.writeHead(404);return res.end();}
    const h={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
    if(u.pathname==='/auth/action'&&c.redirect){
      const location='/auth/action/'+u.search;
      r.redirect={queryPreserved:new URL(location,'http://127.0.0.1').searchParams.get('oobCode')===SENTINEL};
      if(c.hopPolicy!==false)h['Referrer-Policy']='no-referrer';
      res.writeHead(301,{...h,Location:location});return res.end();
    }
    if(u.pathname==='/early.js'||u.pathname==='/late.js'){
      r[u.pathname==='/early.js'?'early':'late']=ref(req.headers.referer);
      res.writeHead(200,{...h,'Content-Type':'application/javascript'});
      return res.end('window.__loaded=true;');
    }
    if(u.pathname==='/auth'||u.pathname==='/auth/action/'){
      r.document={queryPreserved:u.searchParams.get('oobCode')===SENTINEL};
      if(c.header)h['Referrer-Policy']='no-referrer';
      const cleanup=c.cleanup?'<script>history.replaceState(null,"",location.pathname);</script>':'';
      const html='<!doctype html><html><head><meta charset="utf-8"><title>synthetic</title>'+
        '<script src="/early.js?id='+id+'"></script>'+cleanup+
        '<script src="/late.js?id='+id+'"></script>'+
        '<script src="http://127.0.0.1:'+crossPort+'/cross.js?id='+id+'"></script>'+
        '</head><body><pre id="probe">REFERRER_PROBE_DONE</pre></body></html>';
      res.writeHead(200,{...h,'Content-Type':'text/html; charset=utf-8'});return res.end(html);
    }
    res.writeHead(404);res.end();
  });
  await listen(main);
  const cases=[];
  try{
    for(const c of CASES){
      seen.set(c.id,{});
      const profile=await mkdtemp(path.join(os.tmpdir(),'webmgr-referrer-'));
      try{
        const start=c.redirect?'/auth/action':'/auth';
        const url='http://127.0.0.1:'+main.address().port+start+'?id='+c.id+'&mode=resetPassword&oobCode='+SENTINEL;
        const b=await visit(browser.path,url,profile),r=seen.get(c.id),out=classifyCase(c,r,b);
        cases.push({case:c.id,...out,process:b.reason,requestEvidence:!!(r.early&&r.late&&r.cross),
          earlyToken:r.early?.hasToken??null,lateToken:r.late?.hasToken??null,
          crossOriginOnly:r.cross?.originOnly??null,redirectQueryPreserved:r.redirect?.queryPreserved??null});
      }finally{await rm(profile,{recursive:true,force:true});}
    }
  }finally{await close(main);await close(cross);}
  const verdict=cases.every(x=>x.verdict==='PASS')?'PASS':cases.some(x=>x.verdict==='FAIL')?'FAIL':'UNKNOWN';
  return {tier:'SYNTHETIC_CHROMIUM_LOOPBACK_HTTP',browser:browser.version,verdict,cases};
}
if(process.argv[1]&&import.meta.url===new URL('file://'+path.resolve(process.argv[1])).href){
  const result=await runLab();console.log(JSON.stringify(result,null,2));
  if(result.verdict!=='PASS')process.exitCode=1;
}
