import test from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { inventory, snapshot, verify } from './pwa_release_inventory_gate.mjs';
const SOURCE = 'a'.repeat(40);
const required = ['index.html','flutter_bootstrap.js','manifest.json','logmate_service_worker.js','logmate-offline-manifest.json','auth/action/index.html','main.dart.js','canvaskit/canvaskit.js','canvaskit/canvaskit.wasm'];
async function fixture(fn) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'webmgr-inventory-'));
  const normal = path.join(dir, 'normal'), downloaded = path.join(dir, 'downloaded'), staged = path.join(dir, 'staged');
  const config = path.join(dir, 'firebase.json');
  try {
    for (const root of [normal, downloaded, staged]) {
      for (const name of required) { await fs.mkdir(path.dirname(path.join(root, name)), { recursive:true }); await fs.writeFile(path.join(root, name), 'content:' + name); }
    }
    await fs.writeFile(config, JSON.stringify({hosting:{public:'staged',ignore:['firebase.json','**/.*','**/node_modules/**'],rewrites:[{source:'/auth',destination:'/auth/action/index.html'},{source:'/auth/',destination:'/auth/action/index.html'},{source:'/auth/action',destination:'/auth/action/index.html'}]}}));
    await fn({dir,normal,downloaded,staged,config,packet:await snapshot(normal,SOURCE)});
  } finally { await fs.rm(dir,{recursive:true,force:true}); }
}
test('matching independent downloaded and Hosting trees PASS', async () => fixture(async f => {
  assert.equal((await verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest)).verdict,'PASS');
}));
test('mutated downloaded byte REJECT', async () => fixture(async f => {
  await fs.writeFile(path.join(f.downloaded,'index.html'),'altered');
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/bytes differ/);
}));
test('unexpected hosted resource REJECT', async () => fixture(async f => {
  await fs.writeFile(path.join(f.staged,'unexpected.js'),'x');
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/unexpected/);
}));
test('Hosting public points elsewhere REJECT', async () => fixture(async f => {
  await fs.writeFile(f.config,JSON.stringify({hosting:{public:'normal',ignore:['firebase.json']}}));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/public directory mismatch/);
}));
test('unreviewed Hosting ignore REJECT', async () => fixture(async f => {
  await fs.writeFile(f.config,JSON.stringify({hosting:{public:'staged',ignore:['**/*.js']}}));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/unreviewed/);
}));
test('hidden file REJECT', async () => fixture(async f => {
  await fs.writeFile(path.join(f.downloaded,'.secret'),'x');
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/hidden/);
}));
test('symlink REJECT', async () => fixture(async f => {
  await fs.symlink(path.join(f.downloaded,'index.html'),path.join(f.downloaded,'alias.html'));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/symlink/);
}));
test('mode and source spoof REJECT', async () => fixture(async f => {
  await assert.rejects(verify({...f.packet,releaseMode:'ACCEPTANCE'},f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/provenance/);
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,'b'.repeat(40),f.packet.inventoryDigest),/provenance/);
}));
test('missing required file REJECT', async () => fixture(async f => {
  await fs.rm(path.join(f.downloaded,'auth/action/index.html'));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/required resource missing/);
}));
test('case-fold duplicate REJECT', async () => fixture(async f => {
  await fs.writeFile(path.join(f.downloaded,'INDEX.html'),'x');
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/case-fold collision/);
}));
test('tampered manifest digest REJECT', async () => fixture(async f => {
  f.packet.files[0].sha256='0'.repeat(64);
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/trusted inventory digest mismatch/);
}));
test('acceptance harness byte marker REJECT', async () => fixture(async f => {
  await fs.writeFile(path.join(f.downloaded,'main.dart.js'),'LOGMATE_PERSISTENCE_ACCEPTANCE_FLIGHT_V1');
  f.packet.files.find(x=>x.path==='main.dart.js').sha256 = '0'.repeat(64);
  // The trusted digest prevents altering the inventory to hide an acceptance marker.
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/trusted inventory digest mismatch/);
  await assert.rejects(snapshot(f.downloaded,SOURCE),/acceptance harness/);
}));
test('wrong independently supplied inventory digest REJECT', async () => fixture(async f => {
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,'b'.repeat(64)),/trusted inventory digest mismatch/);
}));
test('non-hex source SHA REJECT', async () => fixture(async f => {
  await assert.rejects(snapshot(f.normal,'main'),/40-character/);
}));
test('packet cannot be silently overwritten by snapshot CLI', async () => fixture(async f => {
  const { spawnSync } = await import('node:child_process');
  const out = path.join(f.dir,'inventory.json');
  const cli = path.resolve(path.dirname(new URL(import.meta.url).pathname),'pwa_release_inventory_gate.mjs');
  const first = spawnSync(process.execPath,[cli,'snapshot',f.normal,SOURCE,out],{encoding:'utf8'});
  assert.equal(first.status,0,first.stderr);
  const second = spawnSync(process.execPath,[cli,'snapshot',f.normal,SOURCE,out],{encoding:'utf8'});
  assert.equal(second.status,1);
  assert.match(second.stderr,/REJECT/);
}));
test('CLI rejects wrong Hosting projection with nonzero exit', async () => fixture(async f => {
  const { spawnSync } = await import('node:child_process');
  const cli = path.resolve(path.dirname(new URL(import.meta.url).pathname),'pwa_release_inventory_gate.mjs');
  const packetPath = path.join(f.dir,'packet.json');
  await fs.writeFile(packetPath,JSON.stringify(f.packet));
  await fs.writeFile(f.config,JSON.stringify({hosting:{public:'normal',ignore:['firebase.json']}}));
  const r = spawnSync(process.execPath,[cli,'verify',packetPath,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest],{encoding:'utf8'});
  assert.equal(r.status,1);
  assert.match(r.stderr,/public directory mismatch/);
}));

test('Hosting-ignored root firebase.json in identical raw trees REJECT', async () => fixture(async f => {
  for (const root of [f.normal, f.downloaded, f.staged]) await fs.writeFile(path.join(root,'firebase.json'),'{"hosting":{}}');
  await assert.rejects(snapshot(f.normal,SOURCE),/Hosting-ignored/);
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/Hosting-ignored/);
}));
test('missing or changed auth rewrite alias REJECT', async () => fixture(async f => {
  const config = JSON.parse(await fs.readFile(f.config,'utf8'));
  config.hosting.rewrites = config.hosting.rewrites.slice(0,2);
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/rewrite/);
  config.hosting.rewrites.push({source:'/auth/action',destination:'/index.html'});
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/rewrite/);
  config.hosting.rewrites[2] = {source:undefined,destination:undefined};
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/rewrite/);
}));
test('unreviewed redirect or URL normalization REJECT', async () => fixture(async f => {
  const config = JSON.parse(await fs.readFile(f.config,'utf8'));
  config.hosting.redirects = [{source:'/auth',destination:'https://example.invalid/',type:302}];
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/redirect/);
  delete config.hosting.redirects;
  config.hosting.cleanUrls = true;
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/normalization/);
}));
test('unexpected catch-all rewrite REJECT even when all files match', async () => fixture(async f => {
  const config = JSON.parse(await fs.readFile(f.config,'utf8'));
  config.hosting.rewrites.push({source:'**',destination:'/index.html'});
  await fs.writeFile(f.config,JSON.stringify(config));
  await assert.rejects(verify(f.packet,f.downloaded,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/rewrite/);
}));

test('same directory cannot count as independent download and Hosting staging', async () => fixture(async f => {
  await assert.rejects(verify(f.packet,f.staged,f.staged,f.config,SOURCE,f.packet.inventoryDigest),/distinct real directories/);
}));
test('symlinked parent alias cannot spoof independent roots', async () => fixture(async f => {
  const aliasParent = path.join(f.dir,'alias-parent');
  await fs.symlink(f.dir,aliasParent);
  await assert.rejects(verify(f.packet,path.join(aliasParent,'staged'),f.staged,f.config,SOURCE,f.packet.inventoryDigest),/distinct real directories/);
}));
