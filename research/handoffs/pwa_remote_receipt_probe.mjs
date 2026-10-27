import assert from 'node:assert/strict';
import http from 'node:http';
import { test } from 'node:test';

// RESEARCH FIXTURE ONLY. Test bearer strings are not verified Firebase tokens.
// In-memory synchronous admission is not a Firestore transaction or durable server.
const A='a'.repeat(32), B='b'.repeat(32);
const dig=x=>x.repeat(64);
const op=(id=A,digest=dig('a'),modifiedAtUtc='2026-10-28T00:00:00.000001Z',generation=1,owner='uid-A',kind='UPDATE')=>
  ({id,digest,modifiedAtUtc,generation,owner,kind,record:'flight-1'});
function validUtc(x) {
  if(typeof x!=='string'|| !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}Z$/.test(x))return false;
  const whole=x.slice(0,19)+'Z', d=new Date(whole);
  return Number.isFinite(d.getTime()) && d.toISOString().slice(0,19)+'Z'===whole;
}
function fixture(){
  const state={owner:'uid-A',generation:1,active:true,seq:0,ops:new Map(),receipts:new Map(),heads:new Map()};
  const subjects=new Map([['test-A','uid-A'],['test-B','uid-B']]);
  const view=()=>({owner:state.owner,generation:state.generation,active:state.active,seq:state.seq,
    ops:[...state.ops.values()],receipts:[...state.receipts.values()],heads:[...state.heads.entries()]});
  function guard(uid,generation){
    if(!uid)return {status:401,code:'UNAUTHENTICATED'};
    if(!state.active||uid!==state.owner||generation!==state.generation)
      return {status:403,code:'DENIED_CURRENT_AUTHORITY'};
    return null;
  }
  function admit(uid,b){
    const denial=guard(uid,b.generation);
    if(denial)return denial;
    if(b.owner!==uid||typeof b.id!=='string'|| !/^[a-f0-9]{32}$/.test(b.id)||
       typeof b.digest!=='string'|| !/^[a-f0-9]{64}$/.test(b.digest)||
       b.record!=='flight-1'||!validUtc(b.modifiedAtUtc)||
       !['UPDATE','DELETE','RESTORE'].includes(b.kind))
      return {status:400,code:'INVALID_WIRE'};
    const old=state.ops.get(b.id);
    if(old){
      if(old.owner!==uid)return {status:403,code:'DENIED_OLD_OPERATION_OWNER'};
      if(old.digest!==b.digest)return {status:409,code:'DIGEST_COLLISION'};
      return {status:200,code:'REPLAY',receipt:state.receipts.get(b.id)};
    }
    const seq=++state.seq;
    const record=Object.freeze({...b,serverSequence:seq});
    const receipt=Object.freeze({id:b.id,digest:b.digest,serverSequence:seq});
    state.ops.set(b.id,record);state.receipts.set(b.id,receipt);
    const prev=state.heads.get(b.record);
    // Fixed-width ASCII ID and fixed-width UTC microsecond strings: narrow fixture only.
    if(!prev||b.modifiedAtUtc>prev.modifiedAtUtc||
       (b.modifiedAtUtc===prev.modifiedAtUtc&&b.id>prev.id))
      state.heads.set(b.record,{id:b.id,modifiedAtUtc:b.modifiedAtUtc,deleted:b.kind==='DELETE'});
    return {status:201,code:'ACCEPTED',receipt};
  }
  const server=http.createServer(async(req,res)=>{
    const uid=subjects.get((req.headers.authorization||'').replace(/^Bearer /,''));
    const parts=[];for await(const part of req)parts.push(part);
    let body={};
    try{if(parts.length)body=JSON.parse(Buffer.concat(parts).toString('utf8'));}
    catch{res.writeHead(400).end(JSON.stringify({code:'INVALID_JSON'}));return;}
    let out;
    if(req.method==='POST'&&req.url==='/admit')out=admit(uid,body);
    else if(req.method==='GET'&&(req.url==='/latest'||req.url==='/pull')){
      out=guard(uid,Number(req.headers['x-generation']))||
        (req.url==='/latest'?{status:200,code:'LATEST_ONLY',latestSequence:state.seq}:
          {status:200,code:'DELTA',operations:[...state.ops.values()]});
    }else out={status:404,code:'NOT_FOUND'};
    // Inject ACK loss AFTER the in-memory admission, not before it.
    if(req.headers['x-test-drop-ack']==='yes'&&out.code==='ACCEPTED'){req.socket.destroy();return;}
    res.writeHead(out.status,{'content-type':'application/json'}).end(JSON.stringify(out));
  });
  return {state,view,setAuthority:(owner,generation,active=true)=>{
    state.owner=owner;state.generation=generation;state.active=active;
  },async start(){
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    return 'http://127.0.0.1:'+server.address().port;
  },async close(){await new Promise((resolve,reject)=>server.close(e=>e?reject(e):resolve()));}};
}
async function withFixture(fn){
  const f=fixture(),url=await f.start();
  const call=async(path,{body,token='test-A',generation=1,dropAck=false,method='POST'}={})=>{
    const res=await fetch(url+path,{method,headers:{
      authorization:token?'Bearer '+token:'',
      'content-type':'application/json','x-generation':String(generation),
      ...(dropAck?{'x-test-drop-ack':'yes'}:{})},
      ...(method==='POST'?{body:JSON.stringify(body||{})}:{})});
    return {status:res.status,...await res.json()};
  };
  try{await fn(f,call);}finally{await f.close();}
}
const check=(label,fn)=>test(label,()=>withFixture(fn));
check('RA01 unauthenticated denied',async(f,c)=>{
  assert.equal((await c('/admit',{token:'',body:op()})).code,'UNAUTHENTICATED');
  assert.equal(f.view().seq,0);
});
check('RA02 caller owner hint cannot override subject',async(f,c)=>{
  assert.equal((await c('/admit',{body:op(A,dig('a'),undefined,1,'uid-B')})).code,'INVALID_WIRE');
  assert.equal(f.view().seq,0);
});
check('RA03 accepted operation and same-ID replay share receipt',async(f,c)=>{
  const a=await c('/admit',{body:op()}),b=await c('/admit',{body:op()});
  assert.equal(a.code,'ACCEPTED');assert.equal(b.code,'REPLAY');
  assert.deepEqual(a.receipt,b.receipt);assert.equal(f.view().seq,1);
});
check('RA04 same ID different digest rejects',async(f,c)=>{
  await c('/admit',{body:op()});
  assert.equal((await c('/admit',{body:op(A,dig('b'))})).code,'DIGEST_COLLISION');
  assert.equal(f.view().seq,1);
});
check('RA05 after-commit ACK loss is client UNKNOWN, retry reconciles original ID',async(f,c)=>{
  await assert.rejects(()=>c('/admit',{body:op(),dropAck:true}));
  assert.equal(f.view().seq,1);
  const r=await c('/admit',{body:op()});
  assert.equal(r.code,'REPLAY');assert.equal(r.receipt.serverSequence,1);
});
check('RA06 revoked authority denies even old receipt',async(f,c)=>{
  await c('/admit',{body:op()});f.setAuthority('uid-A',2,false);
  assert.equal((await c('/admit',{body:op()})).code,'DENIED_CURRENT_AUTHORITY');
  assert.equal(f.view().receipts.length,1);
});
check('RA07 ACTIVE new generation rejects stale expected generation',async(f,c)=>{
  f.setAuthority('uid-A',2,true);
  assert.equal((await c('/admit',{body:op()})).code,'DENIED_CURRENT_AUTHORITY');
  assert.equal((await c('/admit',{body:op(B,dig('b'),undefined,2)})).code,'ACCEPTED');
});
check('RA08 wrong authenticated UID denied',async(f,c)=>{
  assert.equal((await c('/admit',{token:'test-B',body:op()})).code,'DENIED_CURRENT_AUTHORITY');
});
check('RA09 transfer cannot replay prior owner operation ID',async(f,c)=>{
  await c('/admit',{body:op()});f.setAuthority('uid-B',2,true);
  const r=await c('/admit',{token:'test-B',body:op(A,dig('a'),undefined,2,'uid-B')});
  assert.equal(r.code,'DENIED_OLD_OPERATION_OWNER');assert.equal(f.view().seq,1);
});
check('RA10 delivery sequence does not override original UTC winner',async(f,c)=>{
  await c('/admit',{body:op(A,dig('a'),'2026-10-28T12:00:00.000001Z')});
  await c('/admit',{body:op(B,dig('b'),'2026-10-28T11:00:00.000001Z')});
  assert.equal(f.view().seq,2);assert.equal(f.view().heads[0][1].id,A);
});
check('RA11 future-stamped edit retains approved no-clock-correction winner',async(f,c)=>{
  await c('/admit',{body:op(A,dig('a'),'2026-10-30T12:00:00.000001Z')});
  await c('/admit',{body:op(B,dig('b'),'2026-10-28T12:00:00.000001Z')});
  assert.equal(f.view().heads[0][1].id,A);
});
check('RA12 DELETE tombstone beats older UPDATE; history retained',async(f,c)=>{
  await c('/admit',{body:op(A,dig('a'),'2026-10-28T12:00:00.000001Z',1,'uid-A','DELETE')});
  await c('/admit',{body:op(B,dig('b'),'2026-10-28T11:00:00.000001Z')});
  assert.equal(f.view().heads[0][1].deleted,true);assert.equal(f.view().ops.length,2);
});
check('RA13 later explicit RESTORE wins without restamping DELETE',async(f,c)=>{
  await c('/admit',{body:op(A,dig('a'),'2026-10-28T12:00:00.000001Z',1,'uid-A','DELETE')});
  await c('/admit',{body:op(B,dig('b'),'2026-10-28T13:00:00.000001Z',1,'uid-A','RESTORE')});
  assert.equal(f.view().heads[0][1].deleted,false);
  assert.equal(f.view().ops[0].modifiedAtUtc,'2026-10-28T12:00:00.000001Z');
});
check('RA14 startup latest-only does not mutate server state',async(f,c)=>{
  await c('/admit',{body:op()});const before=JSON.stringify(f.view());
  const r=await c('/latest',{method:'GET'});
  assert.equal(r.code,'LATEST_ONLY');assert.equal(r.latestSequence,1);
  assert.equal(JSON.stringify(f.view()),before);
});
check('RA15 revoked cached token cannot read latest or pull',async(f,c)=>{
  await c('/admit',{body:op()});f.setAuthority('uid-A',2,false);
  assert.equal((await c('/latest',{method:'GET'})).code,'DENIED_CURRENT_AUTHORITY');
  assert.equal((await c('/pull',{method:'GET'})).code,'DENIED_CURRENT_AUTHORITY');
});
check('RA16 concurrent same ID yields one accepted and eleven replays',async(f,c)=>{
  const results=await Promise.all(Array.from({length:12},()=>c('/admit',{body:op()})));
  assert.equal(results.filter(x=>x.code==='ACCEPTED').length,1);
  assert.equal(results.filter(x=>x.code==='REPLAY').length,11);
  assert.equal(f.view().seq,1);
});
check('RA17 concurrent conflicting digests yield one accept and one collision',async(f,c)=>{
  const results=await Promise.all([c('/admit',{body:op()}),c('/admit',{body:op(A,dig('b'))})]);
  assert.deepEqual(new Set(results.map(x=>x.code)),new Set(['ACCEPTED','DIGEST_COLLISION']));
  assert.equal(f.view().seq,1);
});
check('RA18 malformed ID, timestamp and fake administrative route rejected',async(f,c)=>{
  assert.equal((await c('/admit',{body:op('🤖')})).code,'INVALID_WIRE');
  assert.equal((await c('/admit',{body:op(A,dig('a'),'2026-99-99T12:00:00.000001Z')})).code,'INVALID_WIRE');
  assert.equal((await c('/authority',{body:{owner:'uid-B'}})).code,'NOT_FOUND');
  assert.equal(f.view().seq,0);
});
