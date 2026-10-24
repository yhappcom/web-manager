// Bounded deterministic counterexample. NOT a browser, CacheStorage, or LogMate test.
// LogMate source model: a shared CacheStorage JSON control record, read/modify/put,
// and a Promise queue scoped to EACH worker instance (not across generations).
'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');

function clone(x) { return structuredClone(x); }
function baseline() {
  return {
    schemaVersion: 2, currentBuildId: 'v1', previousBuildId: null,
    candidateBuildId: null, versions: {v1: {verified: true}}, clientBuilds: {}
  };
}
function oldNavigation(control) { control.clientBuilds['old-client-42'] = 'v1'; }
function newInstallation(control) {
  control.versions.v2 = {verified: true};
  control.candidateBuildId = 'v2';
}
function interleave(commitOrder) {
  const storage = {record: baseline()};
  // Two independent workers read the same shared record before either writes.
  const oldSnapshot = clone(storage.record);
  const newSnapshot = clone(storage.record);
  oldNavigation(oldSnapshot);
  newInstallation(newSnapshot);
  for (const worker of commitOrder) {
    storage.record = clone(worker === 'old' ? oldSnapshot : newSnapshot);
  }
  return storage.record;
}
function serializedReference() {
  const storage = {record: baseline()};
  for (const change of [oldNavigation, newInstallation]) {
    const next = clone(storage.record);
    change(next);
    storage.record = next;
  }
  return storage.record;
}
test('new installer last: active-client assignment is lost', () => {
  const state = interleave(['old', 'new']);
  assert.equal(state.versions.v2.verified, true);
  assert.equal(state.clientBuilds['old-client-42'], undefined);
});
test('old active worker last: candidate catalogue is lost', () => {
  const state = interleave(['new', 'old']);
  assert.equal(state.clientBuilds['old-client-42'], 'v1');
  assert.equal(state.versions.v2, undefined);
  assert.equal(state.candidateBuildId, null);
});
test('hypothetical shared serialization preserves both writes', () => {
  const state = serializedReference();
  assert.equal(state.clientBuilds['old-client-42'], 'v1');
  assert.equal(state.versions.v2.verified, true);
  assert.equal(state.candidateBuildId, 'v2');
});
test('no pruning: closed-client IDs accumulate', () => {
  const state = baseline();
  for (let i = 0; i < 5000; i++) {
    state.clientBuilds['closed-client-' + i] = 'v1';
  }
  assert.equal(Object.keys(state.clientBuilds).length, 5000);
  assert.ok(JSON.stringify(state).length > JSON.stringify(baseline()).length);
});
console.log('MODEL ONLY; no product/browser/Service Worker execution.');
// Extension 2026-10-24: source-compatible FIRST-LOAD/CLAIM counterexamples.
// These functions deliberately abstract away actual browser event timing,
// CacheStorage, and asset-byte validation. A 503 here is a possible routing
// outcome under the stated event sequence, NOT a reproduced LogMate incident.
function sourceCompatibleRoute(control, {mode, clientId = '', resultingClientId = ''}) {
  let buildId;
  if (mode === 'navigate') {
    buildId = control.currentBuildId;
    if (buildId) for (const id of new Set([clientId, resultingClientId].filter(Boolean)))
      control.clientBuilds[id] = buildId;
  } else {
    buildId = control.clientBuilds[clientId];
  }
  return control.versions[buildId]?.manifest ? 200 : 503;
}
function routableControl() {
  const c = baseline();
  c.versions.v1.manifest = {shell: [{path: 'main.dart.js'}]};
  return c;
}
function sourceCompatibleReadControl(serialized) {
  try {
    if (serialized) {
      const c = JSON.parse(serialized);
      if (c?.schemaVersion === 2 && c.versions && c.clientBuilds) return c;
    }
  } catch (_) {}
  return {schemaVersion: 2, currentBuildId: null, previousBuildId: null,
    candidateBuildId: null, versions: {}, clientBuilds: {}};
}
test('claimed network-loaded first page has no navigation mapping for late shell', () => {
  const c = routableControl();
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'first-page'}), 503);
});
test('controlled root navigation maps resulting client before late subresources', () => {
  const c = routableControl();
  assert.equal(sourceCompatibleRoute(c, {mode: 'navigate', resultingClientId: 'reloaded'}), 200);
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'reloaded'}), 200);
});
test('verified cache or START_PRECACHE alone cannot map a claimed first page', () => {
  const c = routableControl();
  c.versions.v1.verified = true;
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'first-page'}), 503);
});
test('navigation with no reported IDs serves root but leaves later asset unmapped', () => {
  const c = routableControl();
  assert.equal(sourceCompatibleRoute(c, {mode: 'navigate'}), 200);
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'later-page'}), 503);
});
test('malformed control JSON is silently interpreted as empty control', () => {
  const c = sourceCompatibleReadControl('{broken');
  assert.equal(c.currentBuildId, null);
  assert.deepEqual(c.versions, {});
});
test('unmapped old client must not be assigned unverified candidate by default', () => {
  const c = routableControl();
  newInstallation(c);
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'unknown-old'}), 503);
  assert.equal(c.candidateBuildId, 'v2');
});
test('candidate byte readiness is not sufficient for client-route readiness', () => {
  const c = routableControl();
  c.versions.v1.verified = true;
  const candidateReady = true; // bounded status() analogue, not inspect().
  assert.equal(candidateReady, true);
  assert.equal(sourceCompatibleRoute(c, {mode: 'subresource', clientId: 'unmapped'}), 503);
});
