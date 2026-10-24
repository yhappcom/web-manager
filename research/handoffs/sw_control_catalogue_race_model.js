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
