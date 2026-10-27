/**
 * Web Manager Stage 8 research-only oracle: LogMate APPROVED 2026-10-17 UTC LWW policy.
 * No product source, Firebase, Dart, Sembast, PWA or device is executed.
 * Deterministic synthetic examples; do not use this as a production Sync engine.
 */
import assert from 'node:assert/strict';

const iso = (s) => {
  const m = s.match(/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,6}))?Z$/);
  assert.ok(m, `invalid UTC wire timestamp ${s}`);
  const ms = Date.parse(`${m[1]}Z`);
  assert.ok(Number.isFinite(ms), `invalid timestamp ${s}`);
  assert.equal(new Date(ms).toISOString().slice(0,19), m[1], `nonexistent date ${s}`);
  return BigInt(ms) * 1000n + BigInt((m[2] ?? '').padEnd(6, '0') || '0');
};
const opCmp = (a,b) => Buffer.compare(Buffer.from(a, 'utf8'), Buffer.from(b,'utf8'));
function choose(a,b) {
  assert.equal(a.recordId,b.recordId);
  const ta=iso(a.modifiedAtUtc), tb=iso(b.modifiedAtUtc);
  if (ta !== tb) return ta>tb?a:b;
  if (a.operationId===b.operationId) {
    if (a.digest!==b.digest) return {status:'REJECT_SAME_ID_DIFFERENT_DIGEST'};
    return a;
  }
  return opCmp(a.operationId,b.operationId)>0?a:b;
}
function operation(operationId, modifiedAtUtc, value, extra={}) {
  return {recordId:'flight-001',operationId,modifiedAtUtc,value,digest:`digest-${operationId}-${value}`,kind:'UPDATE',...extra};
}
const at=(hour,minute=0,day='2026-10-27')=>`${day}T${String(hour).padStart(2,'0')}:${String(minute).padStart(2,'0')}:00Z`;
let passed=0; const records=[];
function test(id,name,fn){fn();records.push({id,name,result:'PASS'});passed++}
const A=operation('a',at(10), 'A'); const B=operation('b',at(11), 'B');
test('T01','Later source UTC wins despite later delivery of older edit',()=>assert.equal(choose(B,A).operationId,'b'));
test('T02','Arrival/sequence order does not reverse LWW winner',()=>assert.equal(choose(A,B).operationId,'b'));
test('T03','Equal UTC different IDs uses UTF-8 ordinal tie-break',()=>assert.equal(choose(operation('a',at(10),'A'),operation('z',at(10),'Z')).operationId,'z'));
test('T04','Same operation ID and digest retry is idempotent in model',()=>assert.equal(choose(A,{...A}).operationId,'a'));
test('T05','Same ID altered digest must reject, not tie-break',()=>assert.equal(choose(A,{...A,digest:'forged'}).status,'REJECT_SAME_ID_DIFFERENT_DIGEST'));
test('T06','One-day fast device dominates later real-world edit',()=>{const fast=operation('fast',at(10,0,'2026-10-28'),'FAST'); const actualLater=operation('later',at(11),'LATER'); assert.equal(choose(fast,actualLater).operationId,'fast')});
test('T07','New user correction with clock still behind cannot beat future edit',()=>{const future=operation('future',at(10,0,'2026-10-28'),'FUTURE'); const correction=operation('correct',at(12),'CORRECT'); assert.equal(choose(future,correction).operationId,'future')});
test('T08','Future-dated tombstone can dominate later actual edit',()=>{const tomb=operation('delete',at(10,0,'2026-10-28'),null,{kind:'DELETE'});const edit=operation('edit',at(11),'RESTORED');assert.equal(choose(tomb,edit).kind,'DELETE')});
test('T09','Old backup replay with original UTC cannot overtake later tombstone',()=>{const old=operation('old',at(9),'OLD');const tomb=operation('del',at(11),null,{kind:'DELETE'});assert.equal(choose(old,tomb).kind,'DELETE')});
test('T10','Wrong policy: restamping old backup with import time could revive it',()=>{const restamped=operation('old',at(12),'OLD');const tomb=operation('del',at(11),null,{kind:'DELETE'});assert.equal(choose(restamped,tomb).value,'OLD')});
test('T11','No wall-clock monotonic guarantee after clock rollback',()=>{const earlier=operation('x',at(12),'X');const laterIntent=operation('y',at(10),'Y');assert.equal(choose(earlier,laterIntent).operationId,'x')});
test('T12','Timestamp ordering is distinct from UTC operational flight date',()=>{const edit=operation('edit',at(12),'E',{operationalLocalDate:'2026-10-20'});assert.equal(edit.operationalLocalDate,'2026-10-20');assert.equal(choose(A,edit).operationId,'edit')});
test('T13','Equal timestamps can arise from bounded timestamp precision',()=>{const first=operation('a',at(10),'A');const second=operation('b',at(10),'B');assert.equal(choose(first,second).operationId,'b')});
test('T14','Offset-form and Z-form denote same instant under RFC3339 but strict wire contract is undecided',()=>{assert.equal(Date.parse('2026-10-27T19:00:00+09:00'),Date.parse(at(10)));assert.throws(()=>iso('2026-10-27T19:00:00+09:00'))});
test('T15','A server receipt sequence is not a user edit-time winner',()=>{const newer={...B,serverSequence:101};const older={...A,serverSequence:102};assert.equal(choose(newer,older).operationId,'b')});
test('T16','Clock anomaly warning is independent from LWW selection',()=>{const candidate=operation('fast',at(10,0,'2026-10-28'),'F');const trustedReference=iso(at(10));const anomaly=iso(candidate.modifiedAtUtc)-trustedReference>6n*60n*60n*1000000n;assert.equal(anomaly,true);assert.equal(choose(candidate,A).operationId,'fast')});
test('T17','Wrong-owner rejection must be outside this ordering function',()=>{const wrong={...B,ownerUid:'other'};const correct={...A,ownerUid:'owner'};assert.equal(choose(correct,wrong).operationId,'b');assert.notEqual(correct.ownerUid,wrong.ownerUid)});
test('T18','History custody must be separate from winner projection',()=>{const history=[A,B];assert.equal(choose(...history).operationId,'b');assert.equal(history.length,2)});
test('T19','Sub-millisecond wire times compare by exact microseconds, not Date.parse millisecond truncation',()=>{const early=operation('z','2026-10-27T10:00:00.123001Z','EARLY');const late=operation('a','2026-10-27T10:00:00.123999Z','LATE');assert.equal(choose(early,late).operationId,'a')});
test('T20','Invalid calendar date must reject before comparison',()=>{const bad=operation('bad','2026-02-30T10:00:00Z','BAD');assert.throws(()=>choose(A,bad))});
console.log(JSON.stringify({model:'research-only UTC LWW consequence model',node:process.version,tests:records.length,passed,results:records},null,2));
