import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';

// Research-only pure-state model; NOT a browser, IDB, CacheStorage or LogMate runtime.
const sha = x => createHash('sha256').update(x).digest('hex');
const files = {
  v1: {'index.html':'v1-index','main.dart.js':'v1-js','canvaskit.wasm':'v1-wasm'},
  v2: {'index.html':'v2-index','main.dart.js':'v2-js','canvaskit.wasm':'v2-wasm'}
};
const hashes = Object.fromEntries(Object.entries(files).map(([b,fs]) =>
  [b,Object.fromEntries(Object.entries(fs).map(([p,v])=>[p,sha(v)]))]));
const copy = x => structuredClone(x);
const fresh = () => ({
  caches:{'shell-v1':copy(files.v1)},
  control:{active:'v1',cacheFor:{v1:'shell-v1'},clientBuilds:{tab1:'v1'}},seq:0
});
function verified(s,b,cacheName) {
  const c=s.caches[cacheName]||{};
  return Object.entries(hashes[b]).every(([p,h])=>typeof c[p]==='string' && sha(c[p])===h);
}
function serve(s,client,path) {
  const b=s.control.clientBuilds[client]||s.control.active;
  const bytes=s.caches[s.control.cacheFor[b]]?.[path];
  return typeof bytes==='string' && hashes[b]?.[path]===sha(bytes)
    ? {status:200,build:b,bytes} : {status:503,build:b};
}
function stage(s,b,paths,{bad=false,offline=false}={}) {
  const cacheName='staging-'+b+'-'+(++s.seq);
  s.caches[cacheName]={};
  for(const p of paths) {
    if(offline) return {ok:false,cacheName,reason:'OFFLINE'};
    const bytes=bad && p==='main.dart.js'?'tampered':files[b][p];
    if(sha(bytes)!==hashes[b][p]) return {ok:false,cacheName,reason:'HASH_MISMATCH'};
    s.caches[cacheName][p]=bytes;
  }
  return {ok:verified(s,b,cacheName),cacheName};
}
function commit(s,b,cacheName,{expectedActive=s.control.active}={}) {
  // Conceptual single serialized IDB readwrite transaction, NOT actual IDB.
  if(s.control.active!==expectedActive || !verified(s,b,cacheName)) return false;
  const next=copy(s.control);
  next.cacheFor[b]=cacheName;
  next.active=b;
  s.control=next;
  return true;
}
function repair(s,b,{bad=false,offline=false}={}) {
  const r=stage(s,b,Object.keys(files[b]),{bad,offline});
  if(!r.ok) return false;
  const next=copy(s.control);
  next.cacheFor[b]=r.cacheName; // no active-build switch or client reassignment
  s.control=next;
  return true;
}
function cleanup(s) {
  const retained=new Set(Object.values(s.control.cacheFor));
  for(const k of Object.keys(s.caches)) if(!retained.has(k)) delete s.caches[k];
}
const tests=[];
const test=(n,fn)=>tests.push([n,fn]);
test('M01 old tab pinned after new build',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  assert.equal(serve(s,'tab1','main.dart.js').bytes,'v1-js');
  assert.equal(serve(s,'tab2','main.dart.js').bytes,'v2-js');
});
test('M02 every incomplete staging prefix cannot activate',()=>{
  for(let n=0;n<3;n++){
    const s=fresh(),r=stage(s,'v2',Object.keys(files.v2).slice(0,n));
    assert.equal(r.ok,false);assert.equal(commit(s,'v2',r.cacheName),false);
    assert.equal(serve(s,'tab1','index.html').status,200);
  }
});
test('M03 wrong digest blocks promotion',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2),{bad:true});
  assert.equal(r.ok,false);assert.equal(commit(s,'v2',r.cacheName),false);
  assert.equal(serve(s,'tab1','main.dart.js').status,200);
});
test('M04 offline repair cannot claim ready',()=>{
  const s=fresh();delete s.caches['shell-v1']['main.dart.js'];
  assert.equal(repair(s,'v1',{offline:true}),false);
  assert.equal(serve(s,'tab1','main.dart.js').status,503);
});
test('M05 verified online repair restores exact bytes',()=>{
  const s=fresh();delete s.caches['shell-v1']['main.dart.js'];
  assert.equal(repair(s,'v1'),true);
  assert.equal(serve(s,'tab1','main.dart.js').bytes,'v1-js');
});
test('M06 changed-origin bytes fail repair',()=>{
  const s=fresh();delete s.caches['shell-v1']['main.dart.js'];
  assert.equal(repair(s,'v1',{bad:true}),false);
  assert.equal(serve(s,'tab1','main.dart.js').status,503);
});
test('M07 stale compare-and-swap cannot undo new active',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  assert.equal(commit(s,'v1','shell-v1',{expectedActive:'v1'}),false);
  assert.equal(s.control.active,'v2');
});
test('M08 pointer with missing cache bytes fails closed',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));delete s.caches[r.cacheName]['main.dart.js'];
  assert.equal(serve(s,'tab2','main.dart.js').status,503);
});
test('M09 mutated bytes after verification fail closed',()=>{
  const s=fresh();s.caches['shell-v1']['index.html']='malicious';
  assert.equal(serve(s,'tab1','index.html').status,503);
});
test('M10 cleanup retains old and new referenced builds',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));cleanup(s);
  assert.equal(serve(s,'tab1','index.html').status,200);
  assert.equal(serve(s,'tab2','index.html').status,200);
});
test('M11 orphan staging can be removed without active loss',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2).slice(0,1));
  assert.equal(r.ok,false);cleanup(s);
  assert.equal(s.caches[r.cacheName],undefined);
  assert.equal(serve(s,'tab1','index.html').status,200);
});
test('M12 UNSAFE negative control: deleting live old cache breaks tab',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));delete s.caches['shell-v1'];
  assert.equal(serve(s,'tab1','index.html').status,503);
});
test('M13 restart with uncommitted candidate does not activate',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(r.ok);const reopened=copy(s);
  assert.equal(reopened.control.active,'v1');
  assert.equal(serve(reopened,'tab1','index.html').status,200);
});
test('M14 interrupted candidate cleanup preserves active',()=>{
  const s=fresh();stage(s,'v2',Object.keys(files.v2).slice(0,2));cleanup(s);
  assert.equal(s.control.active,'v1');
  assert.equal(serve(s,'tab1','main.dart.js').status,200);
});
test('M15 shell repair does not mutate user-data sentinel',()=>{
  const s=fresh();s.userData={flightCount:26,replica:'opaque-local'};
  const before=copy(s.userData);delete s.caches['shell-v1']['index.html'];
  assert.ok(repair(s,'v1'));assert.deepEqual(s.userData,before);
});
test('M16 unknown mapped build fails closed',()=>{
  const s=fresh();s.control.clientBuilds.tab1='missing';
  assert.equal(serve(s,'tab1','index.html').status,503);
});

test('M17 UNSAFE stale whole-catalogue write loses v2 promotion',()=>{
  const s=fresh(),stale=copy(s.control),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  stale.clientBuilds.legacy='v1';s.control=stale;
  assert.equal(s.control.active,'v1');
  assert.equal(s.control.cacheFor.v2,undefined);
});
test('M18 fresh serialized catalogue merge preserves promotion and old client',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  const next=copy(s.control);next.clientBuilds.legacy='v1';s.control=next;
  assert.equal(s.control.active,'v2');
  assert.equal(serve(s,'legacy','main.dart.js').bytes,'v1-js');
  assert.equal(serve(s,'tab2','main.dart.js').bytes,'v2-js');
});
test('M19 UNSAFE stale repair snapshot can erase newer active pointer',()=>{
  const s=fresh(),stale=copy(s.control),repairStage=stage(s,'v1',Object.keys(files.v1));
  const upgrade=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',upgrade.cacheName));
  stale.cacheFor.v1=repairStage.cacheName;s.control=stale;
  assert.equal(s.control.active,'v1');
  assert.equal(s.control.cacheFor.v2,undefined);
});
test('M20 fresh merge of old-build repair retains new active build',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  delete s.caches['shell-v1']['main.dart.js'];
  assert.ok(repair(s,'v1'));
  assert.equal(s.control.active,'v2');
  assert.equal(serve(s,'tab1','main.dart.js').bytes,'v1-js');
  assert.equal(serve(s,'tab2','main.dart.js').bytes,'v2-js');
});
test('M21 UNSAFE missing old-client mapping silently switches to active build',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  delete s.control.clientBuilds.tab1;
  assert.equal(serve(s,'tab1','main.dart.js').bytes,'v2-js');
});
test('M22 ambiguous known-client mapping must deny rather than remap',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  const knownBeforeLoss=new Set(['tab1']);
  delete s.control.clientBuilds.tab1;
  const serveWithKnownClientFence=(client,path)=>
    knownBeforeLoss.has(client)&&!Object.hasOwn(s.control.clientBuilds,client)
      ? {status:503,reason:'AMBIGUOUS_CLIENT_BUILD'}:serve(s,client,path);
  assert.equal(serveWithKnownClientFence('tab1','main.dart.js').status,503);
  assert.equal(serveWithKnownClientFence('tab2','main.dart.js').bytes,'v2-js');
});
test('M23 UNSAFE verified old bytes alone permit implicit active downgrade',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  assert.equal(commit(s,'v1','shell-v1',{expectedActive:'v2'}),true);
  assert.equal(s.control.active,'v1');
});
test('M24 explicit release policy fence blocks unapproved downgrade',()=>{
  const s=fresh(),r=stage(s,'v2',Object.keys(files.v2));
  assert.ok(commit(s,'v2',r.cacheName));
  const allowed=(from,to)=>!(from==='v2'&&to==='v1');
  const guardedCommit=(build,cache,expected)=>
    allowed(s.control.active,build)&&commit(s,build,cache,{expectedActive:expected});
  assert.equal(guardedCommit('v1','shell-v1','v2'),false);
  assert.equal(s.control.active,'v2');
  assert.equal(serve(s,'tab1','main.dart.js').bytes,'v1-js');
  assert.equal(serve(s,'tab2','main.dart.js').bytes,'v2-js');
});

let passed=0;
for(const [name,fn] of tests){
  try{fn();passed++;console.log('PASS '+name);}
  catch(error){console.error('FAIL '+name,error);process.exitCode=1;}
}
console.log(JSON.stringify({passed,total:tests.length,kind:'PURE_STATE_SYNTHETIC',browser:false,product:false}));
