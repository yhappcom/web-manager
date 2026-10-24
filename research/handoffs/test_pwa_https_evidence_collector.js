"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const {collect, safeRoute, filterHeaders, publicIP} = require("./pwa_https_evidence_collector");
const h = "a".repeat(64), b = "b".repeat(64);
const plan = () => ({schema:"wm-header-v1",commit:h,artifact:b,origin:"https://preview.example.com/",routes:[
 {path:"/",mime:"html",sha:h,policy:"enforce",headers:{"content-security-policy":["default-src 'self'"]}},
 {path:"/auth/action",mime:"html",sha:b,policy:"report",headers:{}},
 {path:"/logmate_service_worker.js",mime:"js",sha:b,policy:"enforce",headers:{}}
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
