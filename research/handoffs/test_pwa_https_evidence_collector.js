"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const {collect, safeRoute, filterHeaders, publicIP, selectSafeDNSRecords, safeLookup, requestOnce} = require("./pwa_https_evidence_collector");
const https = require("node:https");
const {EventEmitter} = require("node:events");
const h = "a".repeat(64), b = "b".repeat(64);
const plan = () => ({schema:"wm-header-v1",commit:h,artifact:b,origin:"https://preview.example.com/",routes:[
 {path:"/",mime:"html",sha:h,policy:"enforce",headers:{"content-security-policy":["default-src 'self'"]}},
 {path:"/auth/action",mime:"html",sha:b,policy:"report",headers:{"content-security-policy-report-only":["default-src 'self'"]}},
 {path:"/logmate_service_worker.js",mime:"js",sha:b,policy:"enforce",headers:{"content-security-policy":["default-src 'self'"]}}
]});
const transport = async url => ({status:200,sha:url.endsWith("/")?h:b,bytes:25,headers:[
 ["Content-Type",url.endsWith(".js")?"text/javascript":"text/html"],
 ["Content-Security-Policy","default-src 'self'"],
 ["Set-Cookie","secret=value"],["Location","https://example.com/?oobCode=SECRET"],
 ["Referrer-Policy","no-referrer"]
]});
const opts = {allowOrigin:"https://preview.example.com/",transport};
test("positive three-route independent capture and secret redaction",async()=>{
 const r=await collect(plan(),opts);assert.equal(r.responses.length,3);
 assert.equal(r.responses[0].sha,h);assert.equal(r.responses[1].sha,b);
 assert.equal(r.responses[0].headers.length,3);
 assert.doesNotMatch(JSON.stringify(r),/secret|oobCode|Set-Cookie|Location/);
 assert.equal(r.captureKind,"READ_ONLY_HTTPS_BYTES_UNATTESTED");
});
for (const [name, mutate] of [
 ["origin mismatch",p=>p.origin="https://elsewhere.example.com/"],
 ["http",p=>p.origin="http://preview.example.com/"],
 ["user info",p=>p.origin="https://user:pass@preview.example.com/"],
 ["query",p=>p.origin="https://preview.example.com/?x=1"],
 ["fragment",p=>p.origin="https://preview.example.com/#frag"],
 ["localhost",p=>p.origin="https://localhost/"],
 ["internal",p=>p.origin="https://foo.internal/"],
 ["ip",p=>p.origin="https://8.8.8.8/"],
 ["duplicate",p=>p.routes.push({...p.routes[0]})],
 ["path traversal",p=>p.routes[0].path="/a/../b"],
 ["encoded path",p=>p.routes[0].path="/auth%2fsecret"],
 ["double slash",p=>p.routes[0].path="//attacker.com"],
 ["query in path",p=>p.routes[0].path="/auth?action=1"],
 ["bad hash",p=>p.routes[0].sha="bad"],
 ["unknown mime",p=>p.routes[0].mime="css"],
 ["unknown policy",p=>p.routes[0].policy="allow"],
 ["empty",p=>p.routes=[]],
 ["too many",p=>p.routes=Array.from({length:129},(_,i)=>({...p.routes[0],path:"/a"+i}))],
 ["bad provenance",p=>p.commit="abc"],
]) test(name,async()=>{const p=plan();mutate(p);await assert.rejects(collect(p,opts));});
test("redirect is not followed and is explicit",async()=>{
 const r=await collect(plan(),{...opts,transport:async u=>({...await transport(u),status:302})});
 assert.deepEqual(r.responses[0].redirects,["NOT_FOLLOWED"]);
});
test("oversized response rejects",async()=>{
 await assert.rejects(collect(plan(),{...opts,maxBytes:10}),/CAPTURE_INVALID/);
});
test("transport error does not include secret",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async()=>{throw Error("oobCode=SECRET")}}),/CAPTURE_FAILED/);
});
test("bad injected headers fail",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async u=>({...await transport(u),headers:[["Content-Type","a\r\nb"]]})}));
});
test("non-array headers fail",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async u=>({...await transport(u),headers:null})}));
});
test("reject malformed flat raw headers",()=>assert.throws(()=>filterHeaders(["Content-Type"]),/INVALID_RAW_HEADERS/));
test("public addresses positive",()=>{assert.equal(publicIP("8.8.8.8"),true);assert.equal(publicIP("2606:4700:4700::1111"),true)});
test("private and documentation addresses negative",()=>{
 for(const ip of ["127.0.0.1","10.0.0.1","172.16.0.1","192.168.1.1","169.254.2.3","100.64.0.1","203.0.113.2","2001:db8::1","::1","::ffff:127.0.0.1"]) assert.equal(publicIP(ip),false,ip);
});
test("safeRoute exact",()=>{assert.equal(safeRoute("/auth/action/index.html"),true);assert.equal(safeRoute("/a//b"),true);assert.equal(safeRoute("/../"),false)});
test("reject compressed representation even with valid hash",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async u=>({...await transport(u),headers:[["Content-Encoding","gzip"]]})}),/ENCODED_RESPONSE/);
});

test("injected exception code cannot leak action token",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async()=>{throw {code:"oobCode=SECRET"}}}),e=>e.message==="CAPTURE_FAILED");
});
test("reject sensitive value in allowed response header",async()=>{
 await assert.rejects(collect(plan(),{...opts,transport:async u=>({...await transport(u),headers:[["Content-Security-Policy","report-uri /?oobCode=SECRET"]]})}),/SENSITIVE_HEADER/);
});

test("IANA special-purpose IPv4/IPv6 ranges are not accepted as public capture targets",()=>{
 for (const ip of [
  "2001:db8::1","2001:0db8::1","3fff::1","3fff:0fff::1",
  "2001:2::1","2002:0a00:0001::","192.88.99.2","192.0.2.1",
  "198.18.1.1","198.51.100.2","::ffff:127.0.0.1"
 ]) assert.equal(publicIP(ip),false,ip);
 for (const ip of ["8.8.8.8","1.1.1.1","2606:4700:4700::1111","2001:4860:4860::8888"])
  assert.equal(publicIP(ip),true,ip);
});
test("DNS lookup must fail closed for mixed, malformed or empty address sets",()=>{
 const a={address:"8.8.8.8",family:4}, b={address:"2606:4700:4700::1111",family:6};
 assert.deepEqual(selectSafeDNSRecords([a,b]),a);
 for(const records of [
  [],null,[a,{address:"127.0.0.1",family:4}],
  [a,{address:"2001:0db8::1",family:6}],
  [{address:"8.8.8.8",family:6}],
  [{address:"3fff::1",family:6}]
 ]) assert.equal(selectSafeDNSRecords(records),null);
});
test("wall-clock deadline rejects a slow-drip request even without socket idle timeout",async()=>{
 const original=https.request;
 https.request=()=>{
  const req=new EventEmitter();
  req.setTimeout=()=>{};
  req.end=()=>{};
  req.destroy=e=>{req.emit("error",e);req.emit("close");};
  return req;
 };
 try {
  await assert.rejects(requestOnce("https://preview.example.com/",{timeoutMs:20}),e=>e.code==="TIMEOUT");
 } finally { https.request=original; }
});

test("aggregate route inventory is capped even when each response is under its own limit",async()=>{
 const p=plan();
 p.routes=Array.from({length:5},(_,i)=>({...p.routes[0],path:"/asset"+i+".js"}));
 let calls=0;
 const big=async()=>{calls++;return {status:200,sha:h,bytes:32*1024*1024,headers:[["Content-Type","text/javascript"]]};};
 await assert.rejects(collect(p,{...opts,transport:big}),/CAPTURE_TOTAL_LIMIT/);
 assert.equal(calls,4,"fifth request must not start once aggregate budget is exhausted");
 p.routes.pop();
 const four=await collect(p,{...opts,transport:big});
 assert.equal(four.responses.length,4);
});

test("Node 22 autoSelectFamily lookup all=true returns address records, scalar mode stays compatible",async()=>{
 const a={address:"8.8.8.8",family:4}, b={address:"2606:4700:4700::1111",family:6};
 const check=(records,options,lookupError=null)=>new Promise(resolve=>{
  safeLookup("preview.example.com",options,(err,...values)=>resolve({error:err?.code||null,values}),
   (_hostname,resolverOptions,callback)=>{
    assert.deepEqual(resolverOptions,{all:true});
    callback(lookupError,records);
   });
 });
 const multi=await check([a,b],{all:true,hints:32});
 assert.deepEqual(multi,{error:null,values:[[a,b]]},"all=true must pass one array, not a scalar IP");
 const single=await check([a,b],{all:false});
 assert.deepEqual(single,{error:null,values:[a.address,4]});
 const ipv6=await check([a,b],{all:true,family:6});
 assert.deepEqual(ipv6,{error:null,values:[[b]]});
 const missing=await check([a],{all:true,family:6});
 assert.equal(missing.error,"DNS_FAMILY_UNAVAILABLE");
 const mixed=await check([a,{address:"127.0.0.1",family:4}],{all:true});
 assert.equal(mixed.error,"DNS_NONPUBLIC","mixed answers must fail before connection");
 const failed=await check(null,{all:true},new Error("resolver unavailable"));
 assert.equal(failed.error,"DNS_FAILURE");
});

// Negative controls: reject unpinned or nonrestrictive CSP plans before any HTTPS request.
test("unapproved enforce CSP plan is rejected before transport",async()=>{
 const p=plan();delete p.routes[0].headers["content-security-policy"];let calls=0;
 await assert.rejects(collect(p,{...opts,transport:async u=>{calls++;return transport(u);}}),/ROUTE_POLICY_PLAN/);
 assert.equal(calls,0);
});
test("unapproved report-only CSP plan is rejected before transport",async()=>{
 const p=plan();delete p.routes[1].headers["content-security-policy-report-only"];let calls=0;
 await assert.rejects(collect(p,{...opts,transport:async u=>{calls++;return transport(u);}}),/ROUTE_POLICY_PLAN/);
 assert.equal(calls,0);
});
test("empty and report-uri-only CSP values are not meaningful pinned policy",async()=>{
 for(const value of ["","   ","report-uri /csp"]){const p=plan();p.routes[0].headers["content-security-policy"]=[value];let calls=0;
  await assert.rejects(collect(p,{...opts,transport:async u=>{calls++;return transport(u);}}),/ROUTE_POLICY_PLAN/);
  assert.equal(calls,0);
 }
});
