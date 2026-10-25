import test from 'node:test';
import assert from 'node:assert/strict';
import {classifyDom,makeServer} from './pwa_chromium_csp_runtime_lab.mjs';
const html=(baseline,inline,dispositions)=>'<pre id="probe-result">'+JSON.stringify({baseline,inline,dispositions})+'</pre>';
test('enforce requires baseline success, inline blocked, enforce violation',()=>{
  assert.equal(classifyDom(html(true,false,['enforce']),'enforce').verdict,'PASS');
  assert.equal(classifyDom(html(true,true,['enforce']),'enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(false,false,['enforce']),'enforce').verdict,'FAIL');
  assert.equal(classifyDom(html(true,false,[]),'enforce').verdict,'FAIL');
});
test('report-only must execute forbidden script and report rather than block',()=>{
  assert.equal(classifyDom(html(true,true,['report']),'report').verdict,'PASS');
  assert.equal(classifyDom(html(true,false,['report']),'report').verdict,'FAIL');
  assert.equal(classifyDom(html(true,true,['enforce']),'report').verdict,'FAIL');
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
