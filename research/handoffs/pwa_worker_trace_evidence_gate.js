// Research-only evidence admission oracle. Not a browser probe or product test.
// A PASS here is bounded to the supplied independently captured trace.
// Node: node pwa_worker_trace_gate.js --self-test | node pwa_worker_trace_gate.js trace.json
'use strict';
const HEX40 = /^[a-f0-9]{40}$/;
const HEX64 = /^[a-f0-9]{64}$/;
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const validStatus = x => Number.isInteger(x) && typeof x !== 'boolean' && x >= 100 && x <= 599;
const fail = (verdict, reason) => ({verdict, reason});
const names = ['initial_navigation','first_claim_asset','controlled_navigation','controlled_asset','offline_navigation','offline_asset','reopen_navigation','reopen_asset'];
function assessRuntime(t) {
  if (!object(t) || !object(t.identity) || !object(t.phases)) return fail('INCOMPLETE_EVIDENCE','identity or phases absent');
  const i = t.identity;
  if (!HEX40.test(i.source_sha || '') || !HEX64.test(i.worker_sha256 || '') ||
      !HEX64.test(i.release_tree_sha256 || '') || !HEX64.test(i.index_sha256 || '') ||
      !HEX64.test(i.asset_sha256 || '') || typeof i.browser_version !== 'string' ||
      !i.browser_version.trim() || !['loopback','https'].includes(i.origin_class) ||
      i.disposable_profile !== true || i.browser_family !== 'Chromium')
    return fail('INCOMPLETE_EVIDENCE','unbound source/worker/receipt/browser/profile identity');
  for (const name of names) {
    const p = t.phases[name];
    if (!object(p) || !validStatus(p.status) || typeof p.controlled !== 'boolean' ||
        typeof p.offline_enforced !== 'boolean' || !Number.isInteger(p.process_epoch) ||
        p.process_epoch < 1 || typeof p.content_type !== 'string' ||
        typeof p.response_sha256 !== 'string')
      return fail('INCOMPLETE_EVIDENCE','missing/invalid observation: ' + name);
  }
  for (const name of names) {
    const p = t.phases[name];
    const epoch = name.startsWith('reopen_') ? 2 : 1;
    const offline = name.startsWith('offline_') || name.startsWith('reopen_');
    const controlled = name !== 'initial_navigation';
    if (p.process_epoch !== epoch || p.offline_enforced !== offline || p.controlled !== controlled)
      return fail('INCOMPLETE_EVIDENCE','phase context not proven: ' + name);
    if (controlled && (p.controller_worker_sha256 !== i.worker_sha256 || p.intercept_proven !== true))
      return fail('WORKER_IDENTITY_MISMATCH','controller identity differs or missing: ' + name);
  }
  if (t.phases.initial_navigation.status !== 200)
    return fail('INITIAL_NAVIGATION_FAILURE_OBSERVED','first document did not load');
  if (t.phases.first_claim_asset.status !== 200)
    return fail('FIRST_CLAIM_ASSET_FAILURE_OBSERVED','newly claimed page could not load expected asset');
  for (const name of names.slice(2))
    if (t.phases[name].status !== 200)
      return fail('RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED','navigation or asset failed: ' + name);
  for (const name of names) {
    const p = t.phases[name];
    const asset = name.endsWith('_asset');
    const expected = asset ? i.asset_sha256 : i.index_sha256;
    const mime = p.content_type.split(';',1)[0].trim().toLowerCase();
    if (asset ? !['application/javascript','text/javascript'].includes(mime) : mime !== 'text/html')
      return fail('REPRESENTATION_MISMATCH_OBSERVED','unexpected MIME: ' + name);
    if (p.response_sha256 !== expected)
      return fail('RESPONSE_BYTES_MISMATCH_OBSERVED','served bytes differ from pinned receipt: ' + name);
  }
  if (t.offline_negative_control_failed !== true || t.reopen_negative_control_failed !== true)
    return fail('INCOMPLETE_EVIDENCE','offline transport negative controls not proven');
  return fail('BOUNDED_CHROMIUM_TRACE_PASS','exact phases, controller and response hashes observed; no release/data/iPad claim');
}
function assessRace(t) {
  if (!object(t) || !object(t.identity) || !object(t.final_catalogue) ||
      !Array.isArray(t.events) || t.barrier_observed !== true || t.old_client_live !== true ||
      t.candidate_verified_independently !== true || t.final_catalogue_readback_independent !== true ||
      !HEX64.test(t.identity.old_worker_sha256 || '') ||
      !HEX64.test(t.identity.new_worker_sha256 || '') ||
      t.identity.old_worker_sha256 === t.identity.new_worker_sha256 ||
      !t.identity.old_build_id || !t.identity.new_build_id ||
      t.identity.old_build_id === t.identity.new_build_id)
    return fail('INCOMPLETE_INTERLEAVING','generation, barrier, live client or candidate proof absent');
  const events = t.events;
  const reads = events.filter(e => object(e) && e.op === 'read' && ['old','new'].includes(e.actor));
  const writes = events.filter(e => object(e) && e.op === 'write' && ['old','new'].includes(e.actor));
  if (reads.length !== 2 || writes.length !== 2 ||
      new Set(reads.map(e=>e.actor)).size !== 2 || new Set(writes.map(e=>e.actor)).size !== 2 ||
      events.indexOf(reads[0]) > Math.min(...writes.map(e=>events.indexOf(e))) ||
      events.indexOf(reads[1]) > Math.min(...writes.map(e=>events.indexOf(e))) ||
      !reads.every(e=>Number.isInteger(e.revision) && e.revision === reads[0].revision))
    return fail('INCOMPLETE_INTERLEAVING','both generation reads before writes on same revision not proven');
  const c = t.final_catalogue;
  if (!object(c.clientBuilds) || !object(c.versions) || typeof c.candidateBuildId !== 'string')
    return fail('INCOMPLETE_INTERLEAVING','independent final catalogue shape absent');
  if (c.clientBuilds[t.identity.old_client_id] !== t.identity.old_build_id ||
      c.candidateBuildId !== t.identity.new_build_id ||
      !object(c.versions[t.identity.new_build_id]) ||
      c.versions[t.identity.new_build_id].verified !== true)
    return fail('CATALOGUE_LOST_UPDATE_OBSERVED','at least one required postcondition absent');
  return fail('BOUNDED_RACE_PRESERVATION_OBSERVED','overlap and both postconditions observed; not a cross-browser or durability guarantee');
}
function selfTest() {
  const h = x => x.repeat(64), old = h('a'), next = h('b'), tree=h('c'), idx=h('d'), asset=h('e');
  const runtime = () => {
    const identity = {source_sha:'f'.repeat(40),worker_sha256:old,release_tree_sha256:tree,
      index_sha256:idx,asset_sha256:asset,browser_version:'Chromium test',
      origin_class:'loopback',disposable_profile:true,browser_family:'Chromium'};
    const phases = {};
    for (const name of names) {
      const isAsset=name.endsWith('_asset'), isReopen=name.startsWith('reopen_');
      const isOffline=name.startsWith('offline_') || isReopen;
      phases[name]={status:200,controlled:name!=='initial_navigation',offline_enforced:isOffline,
        process_epoch:isReopen?2:1,content_type:isAsset?'text/javascript':'text/html',
        response_sha256:isAsset?asset:idx,controller_worker_sha256:old,intercept_proven:true};
    }
    return {identity,phases,offline_negative_control_failed:true,reopen_negative_control_failed:true};
  };
  const race = () => ({identity:{old_worker_sha256:old,new_worker_sha256:next,
    old_build_id:'v1',new_build_id:'v2',old_client_id:'client-1'},
    barrier_observed:true,old_client_live:true,candidate_verified_independently:true,final_catalogue_readback_independent:true,
    events:[{actor:'old',op:'read',revision:1},{actor:'new',op:'read',revision:1},
      {actor:'old',op:'write'},{actor:'new',op:'write'}],
    final_catalogue:{clientBuilds:{'client-1':'v1'},candidateBuildId:'v2',versions:{v2:{verified:true}}}});
  const tests = [
    ['clean runtime','BOUNDED_CHROMIUM_TRACE_PASS',runtime()],
    ['first claim 503','FIRST_CLAIM_ASSET_FAILURE_OBSERVED',(()=>{const t=runtime();t.phases.first_claim_asset.status=503;return t})()],
    ['initial 404','INITIAL_NAVIGATION_FAILURE_OBSERVED',(()=>{const t=runtime();t.phases.initial_navigation.status=404;return t})()],
    ['offline 503','RELOAD_OFFLINE_OR_REOPEN_FAILURE_OBSERVED',(()=>{const t=runtime();t.phases.offline_asset.status=503;return t})()],
    ['HTML masquerading as JS','REPRESENTATION_MISMATCH_OBSERVED',(()=>{const t=runtime();t.phases.offline_asset.content_type='text/html';return t})()],
    ['wrong body digest','RESPONSE_BYTES_MISMATCH_OBSERVED',(()=>{const t=runtime();t.phases.offline_asset.response_sha256=tree;return t})()],
    ['wrong worker','WORKER_IDENTITY_MISMATCH',(()=>{const t=runtime();t.phases.offline_asset.controller_worker_sha256=next;return t})()],
    ['missing controller','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.phases.controlled_asset.controlled=false;return t})()],
    ['missing negative control','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.offline_negative_control_failed=false;return t})()],
    ['process not restarted','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.phases.reopen_asset.process_epoch=1;return t})()],
    ['offline not enforced','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.phases.offline_asset.offline_enforced=false;return t})()],
    ['boolean status rejected','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.phases.offline_asset.status=true;return t})()],
    ['no receipt','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.identity.release_tree_sha256='';return t})()],
    ['wrong browser family','INCOMPLETE_EVIDENCE',(()=>{const t=runtime();t.identity.browser_family='WebKit';return t})()],
    ['interception not proven','WORKER_IDENTITY_MISMATCH',(()=>{const t=runtime();t.phases.offline_asset.intercept_proven=false;return t})()]
  ];
  let count=0;
  for(const [label,want,input] of tests){const got=assessRuntime(input).verdict;if(got!==want)throw Error(label+': '+got+' expected '+want);count++}
  const races=[
    ['both postconditions','BOUNDED_RACE_PRESERVATION_OBSERVED',race()],
    ['lost old client','CATALOGUE_LOST_UPDATE_OBSERVED',(()=>{const t=race();t.final_catalogue.clientBuilds={};return t})()],
    ['lost candidate','CATALOGUE_LOST_UPDATE_OBSERVED',(()=>{const t=race();t.final_catalogue.candidateBuildId='v1';return t})()],
    ['no overlap','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.barrier_observed=false;return t})()],
    ['read after write','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.events=[t.events[0],t.events[2],t.events[1],t.events[3]];return t})()],
    ['different revision','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.events[1].revision=2;return t})()],
    ['same worker generation','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.identity.new_worker_sha256=old;return t})()],
    ['client not alive','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.old_client_live=false;return t})()],
    ['final readback not independent','INCOMPLETE_INTERLEAVING',(()=>{const t=race();t.final_catalogue_readback_independent=false;return t})()]
  ];
  for(const [label,want,input] of races){const got=assessRace(input).verdict;if(got!==want)throw Error(label+': '+got+' expected '+want);count++}
  return count;
}
if (typeof module !== 'undefined') module.exports = {assessRuntime,assessRace,selfTest};
if (typeof require !== 'undefined' && require.main === module) {
  const fs=require('node:fs');
  if(process.argv[2]==='--self-test'){console.log(selfTest()+'/24 synthetic oracle cases PASS; no browser or product execution');}
  else {
    const t=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
    const out=t.kind==='race'?assessRace(t):t.kind==='runtime'?assessRuntime(t):fail('INCOMPLETE_EVIDENCE','unknown kind');
    console.log(JSON.stringify(out));
    if(!['BOUNDED_CHROMIUM_TRACE_PASS','BOUNDED_RACE_PRESERVATION_OBSERVED'].includes(out.verdict))process.exitCode=2;
  }
}
