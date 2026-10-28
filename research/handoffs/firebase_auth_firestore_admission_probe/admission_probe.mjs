import assert from 'node:assert/strict';
import { test, after } from 'node:test';
import { createServer } from 'node:http';
import { initializeApp, deleteApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';

const PROJECT = 'demo-web-manager-auth';
assert.equal(process.env.FIREBASE_AUTH_EMULATOR_HOST, '127.0.0.1:9099');
assert.equal(process.env.FIRESTORE_EMULATOR_HOST, '127.0.0.1:8080');
const app = initializeApp({ projectId: PROJECT });
const auth = getAuth(app);
const db = getFirestore(app);
after(async () => { await db.terminate(); await deleteApp(app); });
const idPattern = /^[0-9a-f]{32}$/;
const digestPattern = /^[0-9a-f]{64}$/;
const microsPattern = /^[0-9]{16}$/;
const ID1 = '1'.repeat(32), ID2 = '2'.repeat(32), ID3 = '3'.repeat(32);
const D1 = 'a'.repeat(64), D2 = 'b'.repeat(64);
const TIME = '1793180000000000';

function fail(status, message) { const e = new Error(message); e.status = status; throw e; }
async function principal(token) {
  if (typeof token !== 'string' || !token) fail(401, 'missing bearer');
  try { return (await auth.verifyIdToken(token)).uid; }
  catch { fail(401, 'invalid bearer'); }
}
function operation(id=ID1, digest=D1, generation=1) {
  return { id, digest, generation, modifiedAtUtcMicros: TIME };
}
async function seed(name, ownerUid) {
  await db.doc('ledgers/' + name).set({ ownerUid, generation: 1, status: 'active', nextSequence: 0 });
}
async function admit(token, ledgerId, op) {
  const uid = await principal(token);
  if (!/^[a-z0-9-]{1,60}$/.test(ledgerId)) fail(400, 'bad ledger');
  if (!op || !idPattern.test(op.id) || !digestPattern.test(op.digest) ||
      !microsPattern.test(op.modifiedAtUtcMicros) ||
      !Number.isSafeInteger(op.generation) || op.generation < 1) fail(400, 'bad operation');
  const ledgerRef = db.doc('ledgers/' + ledgerId);
  const receiptRef = ledgerRef.collection('receipts').doc(op.id);
  const operationRef = ledgerRef.collection('operations').doc(op.id);
  return db.runTransaction(async tx => {
    const ledger = await tx.get(ledgerRef);
    const receipt = await tx.get(receiptRef);
    if (!ledger.exists) fail(404, 'missing ledger');
    const state = ledger.data();
    // Authority MUST precede any receipt disclosure or replay decision.
    if (state.status !== 'active' || state.ownerUid !== uid) fail(403, 'not current owner');
    if (state.generation !== op.generation) fail(409, 'stale generation');
    if (receipt.exists) {
      const old = receipt.data();
      if (old.ownerUid !== uid || old.digest !== op.digest) fail(409, 'receipt identity conflict');
      return { status: 'REPLAY', sequence: old.sequence, id: op.id };
    }
    const sequence = state.nextSequence + 1;
    tx.update(ledgerRef, { nextSequence: sequence });
    tx.create(receiptRef, { ownerUid: uid, digest: op.digest, sequence });
    tx.create(operationRef, { ownerUid: uid, digest: op.digest, sequence, modifiedAtUtcMicros: op.modifiedAtUtcMicros });
    return { status: 'ACCEPTED', sequence, id: op.id };
  }, { maxAttempts: 8 });
}
async function latest(token, ledgerId) {
  const uid = await principal(token);
  const snap = await db.doc('ledgers/' + ledgerId).get();
  if (!snap.exists || snap.data().ownerUid !== uid || snap.data().status !== 'active') fail(403, 'latest denied');
  return snap.data().nextSequence;
}
async function rotate(name, ownerUid) {
  await db.doc('ledgers/' + name).update({ ownerUid, generation: 2 });
}
async function signUp(email) {
  const res = await fetch('http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signUp?key=emulator-only', {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email, password: 'local-test-only-password', returnSecureToken: true })
  });
  const data = await res.json();
  assert.equal(res.status, 200, JSON.stringify(data));
  assert.ok(data.idToken && data.localId);
  return { token: data.idToken, uid: data.localId };
}
function httpServer() {
  return createServer(async (req, res) => {
    try {
      if (req.method !== 'POST' || req.url !== '/admit') fail(404, 'unknown route');
      let body = '';
      for await (const chunk of req) { body += chunk; if (body.length > 4096) fail(413, 'oversize'); }
      const data = JSON.parse(body);
      const token = (req.headers.authorization || '').replace(/^Bearer /, '');
      const receipt = await admit(token, data.ledgerId, data.operation);
      if (req.headers['x-drop-after-commit'] === 'yes') { req.socket.destroy(); return; }
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(receipt));
    } catch (e) {
      if (res.destroyed) return;
      res.writeHead(e.status || 500, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
  });
}
async function listen(server) {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  return 'http://127.0.0.1:' + server.address().port + '/admit';
}
async function close(server) {
  server.closeAllConnections();
  await new Promise(resolve => server.close(resolve));
}
async function post(url, token, ledgerId, op, drop=false) {
  return fetch(url, { method: 'POST', headers: {
    'content-type': 'application/json', authorization: 'Bearer ' + token,
    ...(drop ? { 'x-drop-after-commit': 'yes' } : {})
  }, body: JSON.stringify({ ledgerId, operation: op }) });
}
async function directRest(token, ledgerId, method='GET') {
  const url = 'http://127.0.0.1:8080/v1/projects/' + PROJECT + '/databases/(default)/documents/ledgers/' + ledgerId;
  return fetch(url, { method, headers: { authorization: 'Bearer ' + token, 'content-type': 'application/json' },
    ...(method === 'PATCH' ? { body: JSON.stringify({ fields: { nextSequence: { integerValue: '999' } } }) } : {}) });
}
async function expectStatus(promise, status) {
  await assert.rejects(promise, e => e.status === status);
}

test('Stage 8 authenticated emulator admission — FE01–FE16', { timeout: 180000 }, async t => {
  const a = await signUp('owner-a@stage8.example');
  const b = await signUp('owner-b@stage8.example');
  await t.test('FE01 emulator token verified to its actual UID', async () => {
    assert.equal(await principal(a.token), a.uid);
    assert.equal(await principal(b.token), b.uid);
  });
  await t.test('FE02 missing/forged bearer denied', async () => {
    await expectStatus(principal(''), 401);
    await expectStatus(principal('forged'), 401);
  });
  await seed('owner', a.uid);
  await t.test('FE03 authenticated current owner accepted; body owner hint irrelevant', async () => {
    assert.deepEqual(await admit(a.token, 'owner', { ...operation(), ownerUid: b.uid }),
      { status: 'ACCEPTED', sequence: 1, id: ID1 });
  });
  await t.test('FE04 different authenticated UID denied', async () => {
    await expectStatus(admit(b.token, 'owner', operation(ID2)), 403);
  });
  await t.test('FE05 same immutable ID/digest replays original receipt', async () => {
    assert.deepEqual(await admit(a.token, 'owner', operation()),
      { status: 'REPLAY', sequence: 1, id: ID1 });
    assert.equal((await db.doc('ledgers/owner').get()).data().nextSequence, 1);
  });
  await t.test('FE06 changed digest for same ID rejected', async () => {
    await expectStatus(admit(a.token, 'owner', operation(ID1, D2)), 409);
  });
  await seed('lost-ack', a.uid);
  await t.test('FE07 socket lost AFTER Firestore commit; retry after HTTP server restart', async () => {
    let server = httpServer();
    let url = await listen(server);
    try { await assert.rejects(post(url, a.token, 'lost-ack', operation(), true)); }
    finally { await close(server); }
    assert.equal((await db.doc('ledgers/lost-ack').get()).data().nextSequence, 1);
    server = httpServer(); url = await listen(server);
    try {
      const response = await post(url, a.token, 'lost-ack', operation());
      assert.equal(response.status, 200);
      assert.deepEqual(await response.json(), { status: 'REPLAY', sequence: 1, id: ID1 });
    } finally { await close(server); }
  });
  await seed('concurrent', a.uid);
  await t.test('FE08 concurrent same ID/digest converges to one Firestore receipt', async () => {
    const results = await Promise.all(Array.from({ length: 4 }, () => admit(a.token, 'concurrent', operation())));
    assert.equal(results.filter(x => x.status === 'ACCEPTED').length, 1);
    assert.equal(results.filter(x => x.status === 'REPLAY').length, 3);
    assert.deepEqual([...new Set(results.map(x => x.sequence))], [1]);
    assert.equal((await db.doc('ledgers/concurrent').get()).data().nextSequence, 1);
    assert.equal((await db.collection('ledgers/concurrent/operations').get()).size, 1);
  });
  await seed('transfer', a.uid);
  await admit(a.token, 'transfer', operation());
  await rotate('transfer', b.uid);
  await t.test('FE09 old owner denied even when its original receipt exists', async () => {
    await expectStatus(admit(a.token, 'transfer', operation()), 403);
    await expectStatus(latest(a.token, 'transfer'), 403);
  });
  await t.test('FE10 new owner stale generation denied; previous owner receipt isolated', async () => {
    await expectStatus(admit(b.token, 'transfer', operation(ID2, D1, 1)), 409);
    await expectStatus(admit(b.token, 'transfer', operation(ID1, D1, 2)), 409);
  });
  await t.test('FE11 new owner current generation can accept new ID and read latest', async () => {
    assert.equal((await admit(b.token, 'transfer', operation(ID2, D1, 2))).sequence, 2);
    assert.equal(await latest(b.token, 'transfer'), 2);
  });
  await t.test('FE12 direct authenticated Firestore REST read/write denied by Rules', async () => {
    const get = await directRest(a.token, 'owner');
    const patch = await directRest(a.token, 'owner', 'PATCH');
    assert.equal(get.status, 403, await get.text());
    assert.equal(patch.status, 403, await patch.text());
    assert.equal((await db.doc('ledgers/owner').get()).data().nextSequence, 1);
  });
  await t.test('FE13 privileged Admin read bypasses Rules; malformed input denied', async () => {
    assert.equal((await db.doc('ledgers/owner').get()).data().ownerUid, a.uid);
    await expectStatus(admit(a.token, 'owner', operation('BAD', D1)), 400);
    await expectStatus(admit(a.token, 'owner', { ...operation(ID3), modifiedAtUtcMicros: 'bad' }), 400);
  });
  await seed('revoked', a.uid);
  await admit(a.token, 'revoked', operation());
  await db.doc('ledgers/revoked').update({ status: 'revoked' });
  await t.test('FE14 same UID loses write and latest access when ledger revoked', async () => {
    await expectStatus(admit(a.token, 'revoked', operation()), 403);
    await expectStatus(admit(a.token, 'revoked', operation(ID2)), 403);
    await expectStatus(latest(a.token, 'revoked'), 403);
    assert.equal((await db.doc('ledgers/revoked').get()).data().nextSequence, 1);
    assert.equal((await db.collection('ledgers/revoked/operations').get()).size, 1);
  });
  await seed('isolated', b.uid);
  await t.test('FE15 same ID is scoped to ledger and its current owner', async () => {
    assert.deepEqual(await admit(b.token, 'isolated', operation()), { status: 'ACCEPTED', sequence: 1, id: ID1 });
    await expectStatus(admit(a.token, 'isolated', operation()), 403);
    assert.equal((await db.collection('ledgers/isolated/receipts').get()).size, 1);
    assert.equal((await db.collection('ledgers/owner/receipts').get()).size, 1);
  });
  await seed('conflict-race', a.uid);
  await t.test('FE16 concurrent same ID but different digest yields one acceptance and one conflict', async () => {
    const settled = await Promise.allSettled([
      admit(a.token, 'conflict-race', operation(ID1, D1)),
      admit(a.token, 'conflict-race', operation(ID1, D2))
    ]);
    const accepted = settled.filter(x => x.status === 'fulfilled');
    const rejected = settled.filter(x => x.status === 'rejected');
    assert.equal(accepted.length, 1);
    assert.equal(rejected.length, 1);
    assert.equal(accepted[0].value.status, 'ACCEPTED');
    assert.equal(rejected[0].reason.status, 409);
    assert.equal((await db.doc('ledgers/conflict-race').get()).data().nextSequence, 1);
    assert.equal((await db.collection('ledgers/conflict-race/operations').get()).size, 1);
    assert.equal((await db.collection('ledgers/conflict-race/receipts').get()).size, 1);
  });
});
