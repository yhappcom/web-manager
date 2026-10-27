// Independent Chrome pages in one browser context: real tabs, same origin.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';

const root = resolve('web');
const server = createServer(async (req, res) => {
  const path = req.url === '/two_tab_probe.js' ? 'two_tab_probe.js' : 'index.html';
  try {
    const body = await readFile(resolve(root, path));
    res.writeHead(200, {'Content-Type': path.endsWith('.js') ? 'application/javascript' : 'text/html',
      'Cache-Control': 'no-store'});
    res.end(body);
  } catch (e) { res.writeHead(500); res.end(String(e)); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = 'http://127.0.0.1:' + server.address().port;
const browser = await chromium.launch({
  executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome',
  headless: true, args: ['--no-sandbox']
});
const context = await browser.newContext();
let pass = 0;
async function page() {
  const p = await context.newPage();
  p.on('pageerror', e => console.error('PAGE ERROR:', e.message));
  await p.goto(origin, {waitUntil:'load'});
  await p.waitForFunction(() => window.probeReady === true, {timeout: 30000});
  return p;
}
async function call(p, method, ...args) {
  return p.evaluate(([method, args]) => window[method](...args), [method, args]);
}
async function scenario(label, aDigest, bDigest, expected) {
  const name = 'stage8_twotab_' + Date.now() + '_' + pass;
  const a = await page(), b = await page();
  assert.notEqual(a, b, 'two distinct Playwright pages required');
  await Promise.all([call(a,'probeOpen',name),call(b,'probeOpen',name)]);
  await call(a,'probeArmHold');
  const pendingA = call(a,'probeApply','op-shared',aDigest);
  await a.waitForFunction(() => window.probeHoldEntered === true, {timeout:15000});
  const bResult = await call(b,'probeApply','op-shared',bDigest);
  await call(a,'probeReleaseHold');
  const aResult = await pendingA;
  const outcomes = [aResult.outcome,bResult.outcome].sort();
  assert.deepEqual(outcomes,expected.slice().sort(),label+' outcome');
  await Promise.all([call(a,'probeClose'),call(b,'probeClose')]);
  await Promise.all([a.close(),b.close()]);
  const observer = await page();
  await call(observer,'probeOpen',name);
  const state = await call(observer,'probeRead');
  assert.equal(state.flights,1,label+' flight count');
  assert.equal(state.revisions,1,label+' revision count');
  assert.equal(state.outbox,1,label+' outbox count');
  assert.equal(state.digest,bDigest,label+' B commit remains');
  await call(observer,'probeClose');
  await observer.close();
  pass++;
  console.log(JSON.stringify({label,pass:true,outcomes,callbacksA:aResult.calls,
    callbacksB:bResult.calls,observer:state,origin,context:'two Chrome tabs plus fresh observer tab'}));
}
try {
  await scenario('TB01 two-tab same digest held stale callback','digest-A','digest-A',['REPLAY','NEW']);
  await scenario('TB02 two-tab conflicting digest held stale callback','digest-A','digest-B',['REJECTED','NEW']);
  console.log('TWO-TAB BOUNDED RESULT:',pass,'/2 PASS');
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
