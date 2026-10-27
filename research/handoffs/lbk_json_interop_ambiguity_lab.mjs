// Synthetic JSON interchange diagnostic for Web Manager Stage 8.
// This does not import LogMate Dart or validate an LBK restore.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';

let checks = 0;
const check = (name, f) => { f(); checks++; console.log(`PASS ${String(checks).padStart(2,'0')} ${name}`); };
const digest = (s) => createHash('sha256').update(s, 'utf8').digest('hex');
const stable = (x) => {
  if (Array.isArray(x)) return x.map(stable);
  if (x && typeof x === 'object') return Object.fromEntries(Object.keys(x).sort().map(k => [k, stable(x[k])]));
  return x;
};
const semantic = (s) => JSON.stringify(stable(JSON.parse(s)));

const dup = '{"manifest":{"ownerUid":"A","ownerUid":"B"},"stores":{}}';
const single = '{"manifest":{"ownerUid":"B"},"stores":{}}';
check('duplicate object member is collapsed by JS JSON.parse', () => assert.equal(JSON.parse(dup).manifest.ownerUid, 'B'));
check('duplicate source and unique source have same JS parsed semantics', () => assert.equal(semantic(dup), semantic(single)));
check('duplicate source and unique source have different raw SHA-256', () => assert.notEqual(digest(dup), digest(single)));
check('duplicate source and unique source have same post-parse synthetic SHA-256', () => assert.equal(digest(semantic(dup)), digest(semantic(single))));
check('escaped and literal member names collide after parsing', () => assert.equal(JSON.parse('{"ownerUid":"A","owner\\u0055id":"B"}').ownerUid, 'B'));
check('duplicate row member is collapsed before row-shape inspection', () => assert.deepEqual(Object.keys(JSON.parse('{"key":"first","key":"second","value":{}}')), ['key','value']));
check('nested duplicate value member is collapsed', () => assert.equal(JSON.parse('{"value":{"rev":1,"rev":2}}').value.rev, 2));
check('IEEE-754 safe integer boundary is exact in JS', () => assert.equal(JSON.parse('9007199254740991'), 9007199254740991));
check('integer above JS safe range loses precision', () => assert.equal(JSON.parse('9007199254740993'), 9007199254740992));
check('distinct numeric spellings collapse after parsing', () => assert.equal(semantic('{"n":1e0}'), semantic('{"n":1}')));
check('JSON.stringify serializes rounded unsafe integer', () => assert.equal(JSON.stringify(JSON.parse('9007199254740993')), '9007199254740992'));
check('JS JSON.parse accepts lone surrogate escape (not JCS-conformant)', () => assert.equal(JSON.parse('"\\ud800"').length, 1));
check('different object member order canonicalizes in this ASCII-only fixture', () => assert.equal(semantic('{"z":1,"a":2}'), semantic('{"a":2,"z":1}')));
console.log(`SYNTHETIC_NODE_JSON_DIAGNOSTIC ${checks}/13 PASS`);
console.log('LIMIT: JavaScript JSON.parse + synthetic sorted JSON only; Dart, LBK validation, browser, Safari, file, iPad, owner authority NOT TESTED.');
