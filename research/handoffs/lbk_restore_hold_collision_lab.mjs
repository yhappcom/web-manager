// Synthetic semantic model of the pinned LogMate restore hold-key construction.
// Not Sembast/Dart execution; no private source or fixture is embedded.
import test from 'node:test';
import assert from 'node:assert/strict';

const CURSOR = 'logmate_sync_applied_cursor_v1';
const APPLIED = 'logmate_sync_applied_identities_v1';
const holdKey = (store, key) => `restored:${store}:${key}`;

function modelReset(sourceHolds, sources, { rejectCollision = false } = {}) {
  const holds = new Map(sourceHolds);
  for (const [store, rows] of sources) {
    for (const [key, value] of rows) {
      const target = holdKey(store, key);
      if (rejectCollision && holds.has(target)) throw Error('recovery-hold collision');
      holds.set(target, { classification: 'recoveryRequired', sourceStore: store, sourceKey: key, sourceEvidence: value });
    }
  }
  return holds;
}

const prior = { classification: 'recoveryRequired', sourceEvidence: { previous: 'epoch-1' } };
const newer = { cursor: 42 };

test('RH01 generated namespace is deterministic', () => assert.equal(holdKey(CURSOR,'current'), 'restored:logmate_sync_applied_cursor_v1:current'));
test('RH02 distinct cursor and applied namespaces do not collide', () => assert.notEqual(holdKey(CURSOR,'x'), holdKey(APPLIED,'x')));
test('RH03 no collision retains original hold and new evidence', () => {
  const got = modelReset(new Map([['legacy:record:a', prior]]), [[CURSOR, new Map([['current', newer]])]]);
  assert.equal(got.size, 2);
  assert.deepEqual(got.get('legacy:record:a'), prior);
});
test('RH04 pre-existing identical key is overwritten by put-like model', () => {
  const key = holdKey(CURSOR, 'current');
  const got = modelReset(new Map([[key, prior]]), [[CURSOR, new Map([['current', newer]])]]);
  assert.equal(got.size, 1);
  assert.notDeepEqual(got.get(key), prior);
  assert.deepEqual(got.get(key).sourceEvidence, newer);
});
test('RH05 collision can affect applied identity too', () => {
  const key = holdKey(APPLIED, 'op-1');
  const got = modelReset(new Map([[key, prior]]), [[APPLIED, new Map([['op-1', { receipt: 'r2' }]])]]);
  assert.equal(got.size, 1);
  assert.deepEqual(got.get(key).sourceEvidence, { receipt: 'r2' });
});
test('RH06 distinct source keys preserve both records', () => {
  const got = modelReset(new Map(), [[CURSOR, new Map([['a', newer],['b', newer]])]]);
  assert.equal(got.size, 2);
});
test('RH07 collision-aware admission rejects before publication', () => {
  const key = holdKey(CURSOR,'current');
  const original = new Map([[key, prior]]);
  assert.throws(() => modelReset(original, [[CURSOR, new Map([['current', newer]])]], { rejectCollision: true }), /collision/);
  assert.deepEqual(original.get(key), prior);
});
test('RH08 a valid semantic checksum of source rows cannot guarantee no derived-key collision', () => {
  const payload = { holds: [[holdKey(CURSOR,'current'), prior]], cursors: [['current', newer]] };
  assert.equal(JSON.parse(JSON.stringify(payload)).holds.length, 1);
  const got = modelReset(new Map(payload.holds), [[CURSOR, new Map(payload.cursors)]]);
  assert.equal(got.size, 1);
});
test('RH09 repeated recovery can re-use an earlier derived key', () => {
  const first = modelReset(new Map(), [[CURSOR, new Map([['current', { cursor: 5 }]])]]);
  const second = modelReset(first, [[CURSOR, new Map([['current', { cursor: 6 }]])]]);
  assert.equal(second.size, first.size);
  assert.deepEqual(second.get(holdKey(CURSOR,'current')).sourceEvidence, { cursor: 6 });
});
test('RH10 unbound, record-empty staging predicate alone does not inspect independent Sync rows', () => {
  const staging = { owner: 'unbound', entry: 'notStarted', recordRows: 0, syncRows: 1 };
  const modeledCurrentPredicate = staging.owner === 'unbound' && staging.entry === 'notStarted' && staging.recordRows === 0;
  assert.equal(modeledCurrentPredicate, true);
  assert.equal(staging.syncRows > 0, true);
});
