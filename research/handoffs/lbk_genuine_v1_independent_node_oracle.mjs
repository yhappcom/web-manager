// Read-only, source-pinned independent JS diagnostic. NOT LogMate's Dart verifier.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const fixturePath = process.env.LBK_FIXTURE ?? 'source-logmate/test/fixtures/f1_v16_populated_format_v1.lbk';
const evidencePath = process.env.LBK_EVIDENCE ?? 'source-logmate/docs/evidence/w019-f1-backup-boundary-2026-10-27.jsonl';
const bytes = readFileSync(fixturePath);
const raw = bytes.toString('utf8');
const original = JSON.parse(raw);
const sha256 = (v) => createHash('sha256').update(v).digest('hex');
const gitBlob = (buf) => createHash('sha1').update(Buffer.from('blob ' + buf.length + '\0')).update(buf).digest('hex');
const canonical = (v) => {
  if (Array.isArray(v)) return v.map(canonical);
  if (v && typeof v === 'object') {
    return Object.fromEntries(Object.entries(v).sort(([a],[b]) => a < b ? -1 : a > b ? 1 : 0).map(([k,x]) => [k,canonical(x)]));
  }
  return v;
};
const semantic = (obj) => JSON.stringify(canonical(obj));
const unsigned = (obj) => ({ manifest: Object.fromEntries(Object.entries(obj.manifest).filter(([k]) => k !== 'snapshotDigest')), stores: obj.stores });
const digest = (obj) => sha256(semantic(unsigned(obj)));

test('01 exact genuine v16 exporter fixture blob is pinned', () => {
  assert.equal(gitBlob(bytes), 'e702040503997f5f6c8cf099314c5607537d864c');
});
test('02 historical LBK v1 manifest and owner are explicit', () => {
  assert.equal(original.manifest.backupFormatVersion, 1);
  assert.equal(original.manifest.sourceCapability, 16);
  assert.equal(original.manifest.formatId, 'logmate.full-ledger-backup');
  assert.equal(original.manifest.ownerUid, 'firebase-user-b1');
  assert.deepEqual(Object.keys(original).sort(), ['manifest','stores']);
});
test('03 independent JS canonical digest agrees with genuine v1 manifest', () => {
  assert.equal(digest(original), '29ebc34e050fc3f809e87464ed0b61693af37393fdaa8a7dc9411b9cc56c4345');
});
test('04 registry and actual row counts agree for 30 stores', () => {
  assert.equal(original.manifest.storeRegistry.length, 30);
  assert.equal(Object.keys(original.stores).length, 30);
  for (const item of original.manifest.storeRegistry) {
    assert.equal(original.stores[item.name].length, item.count, item.name);
  }
  assert.equal(original.stores.logmate_active_records_v1.length, 4);
  assert.equal(original.stores.logmate_outbox_v1.length, 9);
});
test('05 original rows have unique source keys per store', () => {
  for (const [name,rows] of Object.entries(original.stores)) {
    const keys = rows.map(row => String(row.key));
    assert.equal(new Set(keys).size, keys.length, name);
  }
});
test('06 raw byte identity is not semantic checksum identity', () => {
  const reordered = JSON.stringify({ stores: original.stores, manifest: original.manifest });
  assert.notEqual(sha256(reordered), sha256(raw));
  assert.equal(digest(JSON.parse(reordered)), digest(original));
});
test('07 duplicate root JSON member survives JS parsing as same semantic object', () => {
  const crafted = raw.replace('{"manifest":{', '{"manifest":{},"manifest":{');
  assert.notEqual(crafted, raw);
  assert.notEqual(sha256(crafted), sha256(raw));
  assert.deepEqual(JSON.parse(crafted), original);
  assert.equal(digest(JSON.parse(crafted)), digest(original));
});
test('08 duplicate manifest owner property can disappear before semantic digest', () => {
  const needle = '"ownerUid":"firebase-user-b1"';
  assert.ok(raw.includes(needle));
  const crafted = raw.replace(needle, '"ownerUid":"wrong-owner",' + needle);
  assert.notEqual(sha256(crafted), sha256(raw));
  assert.deepEqual(JSON.parse(crafted), original);
  assert.equal(digest(JSON.parse(crafted)), digest(original));
});
test('09 genuine payload mutation is detected by independent checksum', () => {
  const changed = structuredClone(original);
  changed.stores.logmate_active_records_v1[0].key += '-modified';
  assert.notEqual(digest(changed), original.manifest.snapshotDigest);
});
test('10 unkeyed digest can be recomputed for a wrong owner; no auth claim', () => {
  const changed = structuredClone(original);
  changed.manifest.ownerUid = 'other-owner';
  changed.manifest.snapshotDigest = digest(changed);
  assert.equal(digest(changed), changed.manifest.snapshotDigest);
  assert.notEqual(changed.manifest.ownerUid, original.manifest.ownerUid);
});
test('11 parsed genuine fixture has no unsafe JS numeric values', () => {
  let numbers = 0;
  const walk = (v) => {
    if (typeof v === 'number') { numbers++; assert.ok(Number.isSafeInteger(v)); }
    else if (Array.isArray(v)) v.forEach(walk);
    else if (v && typeof v === 'object') Object.values(v).forEach(walk);
  };
  walk(original);
  assert.ok(numbers > 0);
});
test('12 historical Dart VM test receipt records two focused successes only', () => {
  const events = readFileSync(evidencePath,'utf8').trim().split('\n').map(line=>JSON.parse(line));
  const named = events.filter(x=>x.type === 'testStart' && x.test?.name?.startsWith('F1-B01') || x.type === 'testStart' && x.test?.name?.startsWith('B1 native'));
  assert.equal(named.length, 2);
  for (const entry of named) {
    const result = events.find(x=>x.type==='testDone' && x.testID===entry.test.id);
    assert.equal(result?.result,'success');
  }
  assert.equal(events.at(-1).success, true);
});
test('13 malformed JSON and unknown root keys are distinct from genuine fixture', () => {
  assert.throws(()=>JSON.parse(raw.slice(0,-1)), SyntaxError);
  const changed = { ...original, surprise: true };
  assert.notDeepEqual(Object.keys(changed).sort(), ['manifest','stores']);
});
test('14 historical genuine v1 evidence does not constitute v2 or browser validation', () => {
  assert.equal(original.manifest.backupFormatVersion,1);
  assert.equal(original.stores.logmate_sync_state_v1,undefined);
  assert.ok(!raw.includes('logmate_sync_state_v1'));
});
