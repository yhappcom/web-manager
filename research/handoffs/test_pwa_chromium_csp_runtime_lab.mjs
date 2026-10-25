import test from 'node:test';
import assert from 'node:assert/strict';
import {classifyDom,classifyBrowserOutcome,makeServer,visit} from './pwa_chromium_csp_runtime_lab.mjs';
const html=(baseline,inline,dispositions)=>'<pre id="probe-result">'+JSON.stringify({baseline,inline,dispositions})+'</pre>';
test('enforce requires baseline success, inline blocked, enforce violation',()=>{
  assert.equal(classifyDom(html(true,false,['enforce']),'enforce').verdict,'PASS');
  assert.equal(classifyDom(html(true,true,['enforce']),'enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(false,false,['enforce']),'enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(true,false,[]),'enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(true,false,['enforce','report']),'enforce').verdict,'FAIL');
});
test('report-only must execute forbidden script and report rather than block',()=>{
  assert.equal(classifyDom(html(true,true,['report']),'report').verdict,'PASS');
  assert.equal(classifyDom(html(true,false,['report']),'report').verdict,'FAIL');
  assert.equal(classifyDom(html(true,true,['enforce']),'report').verdict,'FAIL');
  assert.equal(classifyDom(html(true,true,['report','enforce']),'report').verdict,'FAIL');
});
test('multiple CSP policies intersect',()=>{
  assert.equal(classifyDom(html(true,false,['enforce']),'multi').verdict,'PASS');
  assert.equal(classifyDom(html(true,true,['enforce']),'multi').verdict,'FAIL');
});
test('unrestricted control must run both scripts without violation',()=>{
  assert.equal(classifyDom(html(true,true,[]),'unrestricted').verdict,'PASS');
  assert.equal(classifyDom(html(true,true,['report']),'unrestricted').verdict,'FAIL');
});
test('missing, pending and malformed results never pass',()=>{
  assert.equal(classifyDom('','enforce').verdict,'UNKNOWN');
  assert.equal(classifyDom('<pre id="probe-result">PENDING</pre>','enforce').verdict,'UNKNOWN');
  assert.equal(classifyDom('<pre id="probe-result">bad</pre>','enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(true,true,[]),'unknown').verdict,'FAIL');
});
test('fixture serves distinct enforce, report-only, multiple, and baseline headers',async()=>{
  const server=makeServer();
  await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
  try {
    const base='http://127.0.0.1:'+server.address().port;
    const enforce=await fetch(base+'/enforce');
    assert.ok(enforce.headers.get('content-security-policy')?.includes("script-src 'self'"));
    assert.equal(enforce.headers.get('content-security-policy-report-only'),null);
    const report=await fetch(base+'/report');
    assert.equal(report.headers.get('content-security-policy'),null);
    assert.ok(report.headers.get('content-security-policy-report-only')?.includes('report-uri'));
    const multi=await fetch(base+'/multi');
    assert.ok(multi.headers.get('content-security-policy')?.includes('unsafe-inline'));
    const plain=await fetch(base+'/unrestricted');
    assert.equal(plain.headers.get('content-security-policy'),null);
    assert.equal((await fetch(base+'/bootstrap.js')).status,200);
    assert.equal((await fetch(base+'/allowed.js')).status,200);
  } finally {await new Promise(ok=>server.close(ok));}
});

test('browser process failures cannot pass from plausible DOM fragments',()=>{
  const valid='<html><head><meta name="fixture-case" content="enforce"></head><body>'+html(true,false,['enforce'])+'</body></html>';
  assert.equal(classifyBrowserOutcome({output:valid,reason:'COMPLETED'},'enforce').verdict,'PASS');
  for (const reason of ['CHROME_NONZERO','CHROME_TIMEOUT','OUTPUT_LIMIT','CHROME_START_ERROR']) {
    const result=classifyBrowserOutcome({output:valid,reason},'enforce');
    assert.equal(result.verdict,'UNKNOWN');
  }
  assert.equal(classifyBrowserOutcome(null,'enforce').verdict,'UNKNOWN');
});
test('completed Chromium output must match server fixture identity',()=>{
  const doc='<html><head><meta name="fixture-case" content="enforce"></head><body>'+html(true,false,['enforce'])+'</body></html>';
  assert.equal(classifyBrowserOutcome({output:doc,reason:'COMPLETED'},'report').verdict,'FAIL');
  assert.equal(classifyBrowserOutcome({output:html(true,false,['enforce']),reason:'COMPLETED'},'enforce').verdict,'FAIL');
  assert.equal(classifyBrowserOutcome({output:doc.replace('fixture-case','wrong-case'),reason:'COMPLETED'},'enforce').verdict,'FAIL');
});
test('fixture serves a case-specific marker, not a caller-invented identity',async()=>{
  const server=makeServer();
  await new Promise(ok=>server.listen(0,'127.0.0.1',ok));
  try {
    const base='http://127.0.0.1:'+server.address().port;
    for (const id of ['enforce','report','multi','unrestricted']) {
      const body=await (await fetch(base+'/'+id)).text();
      assert.ok(body.includes('<meta name="fixture-case" content="'+id+'">'));
    }
  } finally {await new Promise(ok=>server.close(ok));}
});

import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

// A synthetic executable can exit while a descendant still owns its stdout pipe.
// The former 'exit' listener destroyed the pipe and lost TAIL. This is a
// transport/lifecycle test only: no Chromium or product browser claim.
test('browser subprocess waits for stdio close after exit', {skip:process.platform==='win32'}, async()=>{
  const dir=await mkdtemp(path.join(os.tmpdir(),'pwa-csp-stdio-'));
  const executable=path.join(dir,'synthetic-browser');
  const script=[
    '#!/usr/bin/env node',
    "const {spawn}=require('node:child_process');",
    "const child=spawn(process.execPath,['-e',\"setTimeout(()=>process.stdout.write('TAIL'),350)\"],{stdio:['ignore',process.stdout,'ignore'],detached:true});",
    'child.unref();',
    "process.stdout.write('HEAD');",
    'process.exit(0);',
  ].join('\\n');
  try {
    await writeFile(executable,script,{mode:0o755});
    const result=await visit(executable,'http://127.0.0.1/fixture',path.join(dir,'profile'));
    assert.equal(result.reason,'COMPLETED');
    assert.equal(result.output,'HEADTAIL');
  } finally {await rm(dir,{recursive:true,force:true});}
});

test('browser transport preserves nonzero process verdict', {skip:process.platform==='win32'}, async()=>{
  const dir=await mkdtemp(path.join(os.tmpdir(),'pwa-csp-nonzero-'));
  const executable=path.join(dir,'synthetic-browser');
  try {
    await writeFile(executable,[
      '#!/usr/bin/env node',
      "process.stdout.write('<html><meta name=\"fixture-case\" content=\"enforce\"><pre id=\"probe-result\">{\"baseline\":true,\"inline\":false,\"dispositions\":[\"enforce\"]}</pre></html>');",
      'process.exit(7);',
    ].join('\\n'),{mode:0o755});
    const result=await visit(executable,'http://127.0.0.1/fixture',path.join(dir,'profile'));
    assert.equal(result.reason,'CHROME_NONZERO');
    assert.equal(classifyBrowserOutcome(result,'enforce').verdict,'UNKNOWN');
  } finally {await rm(dir,{recursive:true,force:true});}
});
