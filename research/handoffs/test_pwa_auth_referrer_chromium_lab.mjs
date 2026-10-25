import test from 'node:test';
import assert from 'node:assert/strict';
import {classifyCase} from './pwa_auth_referrer_chromium_lab.mjs';
const browser={reason:'COMPLETED',domReady:true};
const ref=(present,hasToken=false,originOnly=false)=>({present,hasToken,originOnly});
function fixture(header=false,cleanup=false,redirect=false){
  const c={id:'test',header,cleanup,redirect};
  const r={document:{queryPreserved:true},early:ref(!header,!header),
    late:ref(!header,!header&&!cleanup),cross:ref(!header,false,!header)};
  if(redirect)r.redirect={queryPreserved:true};
  return {c,r};
}
for(const [name,h,clean,redir] of [
  ['default same-origin full query, cross origin only',false,false,false],
  ['header suppresses same and cross',true,false,false],
  ['history cleanup is not retroactive',false,true,false],
  ['header and cleanup',true,true,false],
  ['redirect both policies',true,false,true],
  ['redirect final only',true,false,true],
])test(name,()=>{const {c,r}=fixture(h,clean,redir);assert.equal(classifyCase(c,r,browser).verdict,'PASS');});
for(const [name,mutate,reason] of [
  ['missing early',r=>delete r.early,'MISSING_REQUEST_EVIDENCE'],
  ['missing cross',r=>delete r.cross,'MISSING_REQUEST_EVIDENCE'],
  ['wrong late token',r=>r.late.hasToken=false,'LATE_SAME_ORIGIN_REFERER_MISMATCH'],
  ['cross token leak',r=>r.cross.hasToken=true,'CROSS_ORIGIN_TOKEN_PRESENT'],
  ['cross full URL',r=>r.cross.originOnly=false,'CROSS_ORIGIN_NOT_ORIGIN_ONLY'],
  ['document query lost',r=>r.document.queryPreserved=false,'DOCUMENT_QUERY_NOT_RECEIVED'],
  ['invalid referrer',r=>r.early.invalid=true,'INVALID_REFERER_VALUE'],
])test(name,()=>{const {c,r}=fixture();mutate(r);assert.equal(classifyCase(c,r,browser).reason,reason);});
test('redirect absent fails',()=>{const {c,r}=fixture(true,false,true);delete r.redirect;assert.equal(classifyCase(c,r,browser).reason,'REDIRECT_NOT_OBSERVED');});
test('redirect query lost fails',()=>{const {c,r}=fixture(true,false,true);r.redirect.queryPreserved=false;assert.equal(classifyCase(c,r,browser).reason,'REDIRECT_LOCATION_QUERY_LOST');});
test('browser timeout never passes',()=>{const {c,r}=fixture();assert.equal(classifyCase(c,r,{reason:'TIMEOUT',domReady:false}).verdict,'UNKNOWN');});
test('no DOM marker never passes',()=>{const {c,r}=fixture();assert.equal(classifyCase(c,r,{reason:'COMPLETED',domReady:false}).verdict,'UNKNOWN');});
