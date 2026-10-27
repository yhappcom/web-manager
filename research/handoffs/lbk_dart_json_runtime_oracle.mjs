// Independent expected-value checks against Dart VM and dart2js observations.
// Source: RFC 8259 §4 and dart.dev/resources/language/number-representation.
// Research-only: this is NOT a LogMate backup decode, browser or Safari test.
import assert from 'node:assert/strict';
import fs from 'node:fs';
const [vmFile, webFile] = process.argv.slice(2);
assert.ok(vmFile && webFile, 'Usage: node ... <vm.json> <dart2js.json>');
const vm = JSON.parse(fs.readFileSync(vmFile, 'utf8').trim());
const web = JSON.parse(fs.readFileSync(webFile, 'utf8').trim());
let count = 0;
const check = (name, f) => { f(); count++; console.log('PASS ' + name); };
check('probe identity', () => {
  assert.equal(vm.probe, 'stage8-lbk-json-cross-runtime-v1');
  assert.equal(web.probe, vm.probe);
});
check('VM duplicate member observed last', () => assert.equal(vm.duplicateOwner, 'new'));
check('dart2js duplicate member observed last', () => assert.equal(web.duplicateOwner, 'new'));
check('VM escaped duplicate member observed last', () => assert.equal(vm.escapedDuplicateOwner, 'new'));
check('dart2js escaped duplicate member observed last', () => assert.equal(web.escapedDuplicateOwner, 'new'));
check('VM reviver sees only collapsed owner', () => assert.equal(vm.duplicateReviverOwnerVisits, 1));
check('dart2js reviver sees only collapsed owner', () => assert.equal(web.duplicateReviverOwnerVisits, 1));
check('VM integer above 2^53 exact', () => assert.equal(vm.largeIntegerDecodedString, '9007199254740993'));
check('dart2js integer above 2^53 rounded', () => assert.equal(web.largeIntegerDecodedString, '9007199254740992'));
check('VM re-encoding preserves this integer', () => assert.equal(vm.largeIntegerEncoded, '{"value":9007199254740993}'));
check('dart2js re-encoding changes this integer', () => assert.equal(web.largeIntegerEncoded, '{"value":9007199254740992}'));
check('nested duplicate key in separate objects permitted', () => {
  assert.equal(vm.sameNestedKeySeparateObjects, true);
  assert.equal(web.sameNestedKeySeparateObjects, true);
});
check('UTF-16 sort vs UTF-8 byte-order distinction', () => {
  assert.equal(vm.bmpBeforeSupplementary, false);
  assert.equal(web.bmpBeforeSupplementary, false);
  assert.equal(vm.utf8BmpBeforeSupplementary, true);
  assert.equal(web.utf8BmpBeforeSupplementary, true);
});
check('negative zero is recorded rather than assumed equal', () => {
  assert.equal(typeof vm.negativeZeroEncoded, 'string');
  assert.equal(typeof web.negativeZeroEncoded, 'string');
});
console.log('DART_VM_VS_DART2JS ' + count + '/' + count + ' PASS — synthetic runtime observations only');
console.log('VM=' + JSON.stringify(vm));
console.log('WEB=' + JSON.stringify(web));
