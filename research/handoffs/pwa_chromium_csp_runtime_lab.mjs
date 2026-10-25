// Research-only Chromium CSP lab: loopback HTTP is NOT TLS or product evidence.
// Node 22+, installed Chromium/Chrome. No dependencies, credentials or fixture-initiated external requests.
import http from 'node:http';
import { spawn, execFileSync } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const expected = {
  enforce: { baseline: true, inline: false, disposition: 'enforce' },
  report: { baseline: true, inline: true, disposition: 'report' },
  multi: { baseline: true, inline: false, disposition: 'enforce' },
  unrestricted: { baseline: true, inline: true, disposition: null },
};
export function classifyDom(dom, id) {
  if (!Object.hasOwn(expected, id)) return { verdict: 'FAIL', reason: 'UNKNOWN_CASE' };
  const m = /<pre id="probe-result">([^<]*)<\/pre>/.exec(dom);
  if (!m || m[1] === 'PENDING') return { verdict: 'UNKNOWN', reason: 'NO_COMPLETED_BROWSER_PROBE' };
  let x;
  try { x = JSON.parse(m[1].replaceAll('&amp;', '&')); }
  catch { return { verdict: 'FAIL', reason: 'INVALID_PROBE_JSON' }; }
  if (!x || typeof x.baseline !== 'boolean' || typeof x.inline !== 'boolean' ||
      !Array.isArray(x.dispositions) || x.dispositions.some(d => !['enforce','report'].includes(d)))
    return { verdict: 'FAIL', reason: 'INVALID_PROBE_SCHEMA' };
  const e = expected[id];
  if (x.baseline !== e.baseline) return { verdict: 'FAIL', reason: 'ALLOWED_BASELINE_MISMATCH' };
  if (x.inline !== e.inline) return { verdict: 'FAIL', reason: 'BLOCKED_EXECUTION_MISMATCH' };
  if (e.disposition && (!x.dispositions.length || x.dispositions.some(d => d !== e.disposition)))
    return { verdict: 'FAIL', reason: 'VIOLATION_DISPOSITION_MISSING' };
  if (!e.disposition && x.dispositions.length)
    return { verdict: 'FAIL', reason: 'UNEXPECTED_VIOLATION' };
  return { verdict: 'PASS', reason: 'EXECUTION_AND_VIOLATION_ORACLES' };
}

// Actual browser admission requires successful process completion and a matching
// server-issued fixture marker; a plausible DOM fragment alone is not a PASS.
export function classifyBrowserOutcome(outcome, id) {
  if (!Object.hasOwn(expected, id)) return { verdict: 'FAIL', reason: 'UNKNOWN_CASE' };
  if (!outcome || typeof outcome.output !== 'string' || typeof outcome.reason !== 'string')
    return { verdict: 'UNKNOWN', reason: 'NO_BROWSER_PROCESS_EVIDENCE' };
  if (outcome.reason !== 'COMPLETED')
    return { verdict: 'UNKNOWN', reason: 'BROWSER_PROCESS_' + outcome.reason.replace(/[^A-Z_]/g, '').slice(0, 32) };
  const marker = '<meta name="fixture-case" content="' + id + '">';
  if (!outcome.output.includes(marker) || !outcome.output.includes('<html'))
    return { verdict: 'FAIL', reason: 'WRONG_OR_MISSING_FIXTURE_DOCUMENT' };
  return classifyDom(outcome.output, id);
}

const bootstrap = "(()=>{const d=[];document.addEventListener('securitypolicyviolation',e=>d.push(e.disposition));window.addEventListener('DOMContentLoaded',()=>setTimeout(()=>{document.querySelector('#probe-result').textContent=JSON.stringify({baseline:window.__allowedRan===true,inline:window.__inlineRan===true,dispositions:d})},400))})();";
const documentHtml = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body><pre id="probe-result">PENDING</pre><script src="/bootstrap.js"></script><script>window.__inlineRan=true;</script><script src="/allowed.js"></script></body></html>';
export function makeServer() {
  return http.createServer((req,res) => {
    const route = new URL(req.url,'http://127.0.0.1').pathname;
    const h = {'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
    if (route === '/bootstrap.js' || route === '/allowed.js') {
      res.writeHead(200,{...h,'Content-Type':'text/javascript; charset=utf-8'});
      return res.end(route === '/bootstrap.js' ? bootstrap : 'window.__allowedRan=true;');
    }
    const id = route.slice(1);
    if (!Object.hasOwn(expected,id)) { res.writeHead(404); return res.end(); }
    h['Content-Type']='text/html; charset=utf-8';
    if (id === 'enforce') h['Content-Security-Policy']="script-src 'self'; object-src 'none'";
    if (id === 'report') h['Content-Security-Policy-Report-Only']="script-src 'self'; report-uri /csp-report";
    if (id === 'multi') h['Content-Security-Policy']=[
      "script-src 'self'; object-src 'none'",
      "script-src 'self' 'unsafe-inline'; object-src 'none'"
    ];
    res.writeHead(200,h); res.end(documentHtml.replace('<head>', '<head><meta name="fixture-case" content="'+id+'">'));
  });
}
function findChrome() {
  for (const p of [process.env.CHROME_PATH,'/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser'].filter(Boolean)) {
    try { return {path:p,version:execFileSync(p,['--version'],{encoding:'utf8',timeout:3000}).trim()}; }
    catch {}
  }
  return null;
}
async function visit(chrome,url,profile) {
  return new Promise(resolve => {
    const args=['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage',
      '--no-first-run','--no-default-browser-check','--disable-extensions',
      '--disable-background-networking','--virtual-time-budget=5000','--dump-dom',
      '--user-data-dir='+profile,url];
    const p=spawn(chrome,args,{detached:process.platform!=='win32',stdio:['ignore','pipe','pipe']});
    let output='',done=false;
    const finish=(reason)=>{if(done)return;done=true;clearTimeout(timer);p.stdout.destroy();p.stderr.destroy();resolve({output,reason});};
    const kill=()=>{try {if(process.platform!=='win32'&&p.pid)process.kill(-p.pid,'SIGKILL');else p.kill('SIGKILL');}catch{}};
    const timer=setTimeout(()=>{kill();finish('CHROME_TIMEOUT');},12000);
    p.stdout.on('data',b=>{output+=b.toString();if(output.length>200000){kill();finish('OUTPUT_LIMIT');}});
    p.stderr.on('data',()=>{});
    p.on('error',()=>finish('CHROME_START_ERROR'));
    p.on('exit',code=>finish(code===0?'COMPLETED':'CHROME_NONZERO'));
  });
}
export async function runLab() {
  const chrome=findChrome();
  if(!chrome) return {tier:'LOCAL_CHROMIUM_SYNTHETIC_NO_TLS',verdict:'UNKNOWN',reason:'NO_CHROME',cases:[]};
  const server=makeServer();
  await new Promise((ok,bad)=>{server.once('error',bad);server.listen(0,'127.0.0.1',ok);});
  const cases=[];
  try {
    const port=server.address().port;
    for(const id of Object.keys(expected)) {
      const profile=await mkdtemp(path.join(os.tmpdir(),'pwa-csp-lab-'));
      try {
        const result=await visit(chrome.path,'http://127.0.0.1:'+port+'/'+id,profile);
        cases.push({id,...classifyBrowserOutcome(result,id),processReason:result.reason});
      } finally {
        try {await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:200});}
        catch { /* restricted runners can retain a profile; no false PASS */ }
      }
    }
  } finally {await new Promise(ok=>server.close(ok));}
  const verdict=cases.every(x=>x.verdict==='PASS')?'PASS':
    cases.some(x=>x.verdict==='FAIL')?'FAIL':'UNKNOWN';
  return {tier:'LOCAL_CHROMIUM_SYNTHETIC_NO_TLS',browser:chrome.version,verdict,cases,
    caveat:'No product, HTTPS/TLS, Safari, Home Screen or managed iPad acceptance'};
}
if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const result=await runLab();
  process.stdout.write(JSON.stringify(result,null,2)+'\n');
  process.exitCode=result.verdict==='PASS'?0:result.verdict==='FAIL'?1:2;
}
