// Real independent Chrome tabs (separate pages, shared origin/context) plus fresh third-tab readback.
// This tests the public Sembast adapter and fixture-owned admission, NOT LogMate production.
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
  await p.waitForFunction(() => window.probeReady === true);
  return p;
}
async function call(p, method, ...args) {
  const value = await p.evaluate(([method, args]) => window[method](...args), [method, args]);
  return typeof value === 'string' && value.startsWith('{') ? JSON.parse(value) : value;
}
// Independent, read-only IndexedDB API inventory. Counts physical object-store entries,
 // not semantic Sembast rows or fsync durability; Chrome-only diagnostic.
async function rawIndexedDbSnapshot(p, targetName) {
  return p.evaluate(async (targetName) => {
    if (typeof indexedDB.databases !== 'function') {
      return {supported:false, databases:[]};
    }
    const catalog = await indexedDB.databases();
    const databases = [];
    for (const info of catalog) {
      if (info.name !== targetName) continue;
      const db = await new Promise((resolve, reject) => {
        const req = indexedDB.open(info.name);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
        req.onupgradeneeded = () => {
          req.transaction.abort();
          reject(new Error('Raw inspection refused to create or upgrade a DB'));
        };
      });
      try {
        const stores = {};
        for (const storeName of Array.from(db.objectStoreNames)) {
          stores[storeName] = await new Promise((resolve, reject) => {
            const tx = db.transaction(storeName, 'readonly');
            const req = tx.objectStore(storeName).count();
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
            tx.onabort = () => reject(tx.error || new Error('Raw count aborted'));
          });
        }
        databases.push({name:info.name, version:db.version, stores});
      } finally {
        db.close();
      }
    }
    return {supported:true, databases};
  }, targetName);
}

async function verify(name, expectedDigest, label) {
  const observer = await page();
  try {
    await call(observer,'probeOpen',name);
    const state = await call(observer,'probeRead');
    assert.equal(state.flights,1,label+' flight count');
    assert.equal(state.revisions,1,label+' revision count');
    assert.equal(state.outbox,1,label+' outbox count');
    assert.equal(state.digest,expectedDigest,label+' persisted digest');
    const raw = await rawIndexedDbSnapshot(observer,name);
    assert.equal(raw.supported,true,label+' raw IndexedDB inventory available');
    assert.equal(raw.databases.length,1,label+' exactly one target IndexedDB database');
    assert.equal(raw.databases[0].name,name,label+' target IndexedDB name');
    assert.ok(Object.values(raw.databases[0].stores).some(n => n > 0),
      label+' target IndexedDB has at least one physical object-store entry');
    return {...state, rawIndexedDb:raw};
  } finally {
    await call(observer,'probeClose');
    await observer.close();
  }
}
async function baseline(label, aDigest, bDigest, expectedA) {
  const name = 'stage8_twotab_baseline_' + Date.now() + '_' + pass;
  const a = await page(), b = await page();
  try {
    assert.notEqual(a,b,'two distinct Chrome tabs required');
    await Promise.all([call(a,'probeOpen',name),call(b,'probeOpen',name)]);
    const bResult = await call(b,'probeApply','op-shared',bDigest);
    const aResult = await call(a,'probeApply','op-shared',aDigest);
    assert.equal(bResult.outcome,'NEW',label+' first writer');
    assert.equal(aResult.outcome,expectedA,label+' second writer');
    await Promise.all([call(a,'probeClose'),call(b,'probeClose')]);
    const state = await verify(name,bDigest,label);
    pass++;
    console.log(JSON.stringify({label,verdict:'PASS',outcomes:[bResult,aResult],
      observer:state,origin,context:'two distinct Chrome tabs; third-tab reopen'}));
  } finally {
    await Promise.allSettled([a.close(),b.close()]);
  }
}
// Two independent tabs launch writes without a deterministic winner. This is a
// concurrency diagnostic, NOT a guaranteed callback-reexecution interleaving.
async function race(label, aDigest, bDigest, expectedOutcomes) {
  const name = 'stage8_twotab_race_' + Date.now() + '_' + pass;
  const a = await page(), b = await page();
  try {
    assert.notEqual(a,b,'two distinct Chrome tabs required');
    await Promise.all([call(a,'probeOpen',name),call(b,'probeOpen',name)]);
    const [aResult,bResult] = await Promise.all([
      call(a,'probeApply','op-shared',aDigest),
      call(b,'probeApply','op-shared',bDigest)
    ]);
    const outcomes = [aResult.outcome,bResult.outcome].sort();
    assert.deepEqual(outcomes,[...expectedOutcomes].sort(),label+' race outcomes');
    const winner = aResult.outcome === 'NEW' ? aDigest : bDigest;
    await Promise.all([call(a,'probeClose'),call(b,'probeClose')]);
    const state = await verify(name,winner,label);
    pass++;
    console.log(JSON.stringify({label,verdict:'PASS',outcomes:[aResult,bResult],
      observer:state,origin,context:'two distinct concurrent Chrome tabs; third-tab reopen',
      callbackReplayObserved:aResult.calls > 1 || bResult.calls > 1}));
  } finally {
    await Promise.allSettled([a.close(),b.close()]);
  }
}

async function overlapAttempt() {
  const name = 'stage8_twotab_overlap_' + Date.now();
  const a = await page(), b = await page();
  try {
    await Promise.all([call(a,'probeOpen',name),call(b,'probeOpen',name)]);
    await call(a,'probeArmHold');
    const pendingA = call(a,'probeApply','op-shared','digest-A');
    await a.waitForFunction(() => window.probeHasEntered() === true, null, {timeout:15000});
    const pendingB = call(b,'probeApply','op-shared','digest-B');
    const early = await Promise.race([
      pendingB.then(value => ({settled:true,value})),
      new Promise(resolve => setTimeout(() => resolve({settled:false}),2500))
    ]);
    await call(a,'probeReleaseHold');
    const [aResult,bResult] = await Promise.all([pendingA,pendingB]);
    await Promise.all([call(a,'probeClose'),call(b,'probeClose')]);
    const state = await verify(name,early.settled ? 'digest-B' : (aResult.outcome === 'NEW' ? 'digest-A' : 'digest-B'),
      'TB03 overlap');
    const verdict = early.settled && bResult.outcome === 'NEW' &&
      aResult.outcome === 'REJECTED' ? 'PASS (B committed before held A)' :
      'INCONCLUSIVE (desired interleaving not proven)';
    console.log(JSON.stringify({label:'TB03 controlled overlap',verdict,
      earlyBCommit:early.settled,aResult,bResult,observer:state,
      note:'Callback replay is proven only if aResult.calls > 1; no assumed replay.'}));
  } finally {
    await Promise.allSettled([a.close(),b.close()]);
  }
}
try {
  await baseline('TB01 two-tab same digest propagation','digest-A','digest-A','REPLAY');
  await baseline('TB02 two-tab conflicting digest rejection','digest-A','digest-B','REJECTED');
  await race('TB04 concurrent same-digest race','digest-A','digest-A',['NEW','REPLAY']);
  await race('TB05 concurrent conflicting-digest race','digest-A','digest-B',['NEW','REJECTED']);
  await overlapAttempt();
  assert.equal(pass,4,'exact deterministic two-tab baseline count');
  console.log('DETERMINISTIC TWO-TAB BASELINE:',pass,'/4 PASS; TB03 overlap reported separately');
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
