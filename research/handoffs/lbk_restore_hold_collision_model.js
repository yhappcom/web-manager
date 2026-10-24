// LogMate main@4101ec7: source-compatible model of _resetRestoredSyncTrust.
// NOT a Dart/Sembast, browser, physical-device, or production execution.
"use strict";
const CURSOR="logmate_sync_applied_cursor_v1";
const APPLIED="logmate_sync_applied_identities_v1";
const clone=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function restore(source,dest={freshCore:true,syncExtras:{}},strict=false){
  if(!dest.freshCore)throw Error("NOT_FRESH_CORE");
  if(strict&&Object.keys(dest.syncExtras||{}).length)throw Error("STAGING_SYNC_NOT_EMPTY");
  const holds=clone(source.holds||{}),overwritten=[];
  for(const [name,rows] of [[CURSOR,source.cursor||{}],[APPLIED,source.applied||{}]]){
    for(const [key,value] of Object.entries(rows)){
      const k="restored:"+name+":"+key;
      if(Object.prototype.hasOwnProperty.call(holds,k)){
        overwritten.push(k);
        if(strict)throw Error("HOLD_KEY_COLLISION");
      }
      holds[k]={classification:"recoveryRequired",sourceStore:name,
        sourceKey:key,sourceEvidence:clone(value)};
    }
  }
  return {holds,overwritten,cursor:{},applied:{},
    originReplicaId:dest.replicaId||"new-destination-replica",
    remoteBaselineStatus:"unverified",ownerLocked:true};
}
function oracle(source,out){
  for(const [k,v] of Object.entries(source.holds||{}))
    if(!Object.prototype.hasOwnProperty.call(out.holds,k)||!eq(out.holds[k],v))return false;
  for(const [name,rows] of [[CURSOR,source.cursor||{}],[APPLIED,source.applied||{}]])
    for(const [key,value] of Object.entries(rows)){
      const hold=out.holds["restored:"+name+":"+key];
      if(!hold||hold.sourceStore!==name||hold.sourceKey!==key||
         !eq(hold.sourceEvidence,value))return false;
    }
  return Object.keys(out.cursor).length===0&&Object.keys(out.applied).length===0&&
    out.remoteBaselineStatus==="unverified"&&out.ownerLocked===true;
}
function runTests(){
  const passed=[];
  const check=(name,fn)=>{if(!fn())throw Error("FAIL: "+name);passed.push(name)};
  const fails=(fn,code)=>{try{fn();return false}catch(e){return e.message.includes(code)}};
  const ck="restored:"+CURSOR+":stream",ak="restored:"+APPLIED+":op";
  const base={holds:{keep:{proof:"original"}},cursor:{stream:{sequence:"7"}},
    applied:{op:{operationId:"op"}}};
  check("clean preservation",()=>oracle(base,restore(base)));
  check("clean no collision",()=>restore(base).overwritten.length===0);
  check("new replica retained",()=>restore(base,{freshCore:true,replicaId:"B"}).originReplicaId==="B");
  check("cursor cleared",()=>Object.keys(restore(base).cursor).length===0);
  check("applied cleared",()=>Object.keys(restore(base).applied).length===0);
  check("remote baseline unverified",()=>restore(base).remoteBaselineStatus==="unverified");
  check("owner locked",()=>restore(base).ownerLocked);
  check("input immutable",()=>{const b=clone(base);restore(base);return eq(base,b)});
  check("cursor collision overwrites hold",()=>{
    const s={...base,holds:{[ck]:{proof:"earlier recovery"}}};
    return restore(s).overwritten.includes(ck)&&!oracle(s,restore(s));});
  check("applied collision overwrites hold",()=>{
    const s={...base,holds:{[ak]:{proof:"earlier recovery"}}};
    return restore(s).overwritten.includes(ak)&&!oracle(s,restore(s));});
  check("dual collision",()=>{
    const s={...base,holds:{[ck]:{proof:"c"},[ak]:{proof:"a"}}};
    return restore(s).overwritten.length===2&&!oracle(s,restore(s));});
  check("colon key collision",()=>{
    const key="part:two",h="restored:"+CURSOR+":"+key;
    const s={holds:{[h]:{proof:"prior"}},cursor:{[key]:{sequence:"8"}}};
    return restore(s).overwritten.includes(h)&&!oracle(s,restore(s));});
  check("nonmatching prefix preserved",()=>{
    const s={...base,holds:{[ck+"-other"]:{proof:"retain"}}};
    return oracle(s,restore(s));});
  check("cursor/applied namespace distinct",()=>{
    const s={cursor:{same:{sequence:"1"}},applied:{same:{operationId:"same"}}};
    return oracle(s,restore(s))&&Object.keys(restore(s).holds).length===2;});
  check("strict cursor collision rejection",()=>fails(()=>restore({...base,holds:{[ck]:{proof:"old"}}},undefined,true),"HOLD_KEY_COLLISION"));
  check("strict applied collision rejection",()=>fails(()=>restore({...base,holds:{[ak]:{proof:"old"}}},undefined,true),"HOLD_KEY_COLLISION"));
  check("strict clean acceptance",()=>oracle(base,restore(base,undefined,true)));
  check("strict staging Sync rejection",()=>fails(()=>restore(base,{freshCore:true,syncExtras:{hold:{proof:"local"}}},true),"STAGING_SYNC_NOT_EMPTY"));
  check("source-compatible staging permits Sync extras",()=>oracle(base,restore(base,{freshCore:true,syncExtras:{hold:{proof:"local"}}})));
  check("nonfresh core rejection",()=>fails(()=>restore(base,{freshCore:false}),"NOT_FRESH_CORE")&&fails(()=>restore(base,{freshCore:false},true),"NOT_FRESH_CORE"));
  check("oracle detects missing original hold",()=>{const out=restore(base);delete out.holds.keep;return !oracle(base,out)});
  check("oracle detects modified evidence",()=>{const out=restore(base);out.holds[ck].sourceEvidence.sequence="99";return !oracle(base,out)});
  check("strict rejects same-value key collision",()=>fails(()=>restore({...base,holds:{[ck]:{classification:"recoveryRequired",sourceStore:CURSOR,sourceKey:"stream",sourceEvidence:{sequence:"7"}}}},undefined,true),"HOLD_KEY_COLLISION"));
  check("second-restore-like collision",()=>{
    const prior=restore({cursor:{stream:{sequence:"old"}}});
    const s={holds:prior.holds,cursor:{stream:{sequence:"new"}}};
    return !oracle(s,restore(s));});
  return {passed:passed.length,tests:passed};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
  console.log(JSON.stringify(runTests(),null,2));
