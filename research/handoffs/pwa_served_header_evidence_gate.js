"use strict";
/* WM Stage 8: deterministic HTTPS evidence consistency, NOT CSP/browser/release proof. */
const SAFE_CAPTURE_HEADERS = new Set([
 "content-type", "content-security-policy", "content-security-policy-report-only",
 "referrer-policy", "x-content-type-options", "cache-control", "permissions-policy",
 "cross-origin-opener-policy", "cross-origin-resource-policy", "cross-origin-embedder-policy",
 "strict-transport-security", "vary", "service-worker-allowed", "content-encoding"
]);
const HASH=/^[0-9a-f]{64}$/;
function safeEvidenceRoute(path){return typeof path==="string" && /^\/[a-zA-Z0-9_./-]*$/.test(path) && !path.startsWith("//") && path.length<=512 && !path.split("/").some(s=>s==="."||s==="..");}
function sensitiveEvidenceValue(value){return /(?:oobCode|access_token|id_token)=|Authorization\s|Bearer\s/i.test(value);}
function admissibleEvidenceHeader(name,value){return typeof name==="string" && SAFE_CAPTURE_HEADERS.has(name.toLowerCase()) && /^[a-z0-9-]+$/i.test(name) && typeof value==="string" && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\r\n]/.test(value) && !sensitiveEvidenceValue(value);}

const GUARDED_CSP_DIRECTIVE=/(?:^|;)\s*(?:default-src|script-src(?:-elem|-attr)?|worker-src|object-src|base-uri|frame-ancestors|connect-src|form-action|style-src(?:-elem|-attr)?|img-src|font-src|child-src|frame-src|media-src|manifest-src|sandbox|require-trusted-types-for|trusted-types|upgrade-insecure-requests)(?=\s|;|$)/i;
// Evidence-admission check only; actual browser enforcement requires negative runtime tests.
function hasPinnedPolicy(route){
 if(route && route.policy==="observe")return true;
 const key=route?.policy==="enforce"?"content-security-policy":route?.policy==="report"?"content-security-policy-report-only":null;
 if(!key||!route.headers||typeof route.headers!=="object"||Array.isArray(route.headers))return false;
 const entries=Object.entries(route.headers).filter(([name])=>name.toLowerCase()===key);
 if(entries.length!==1)return false;
 const values=entries[0][1];
 return Array.isArray(values)&&values.length>0&&values.every(v=>typeof v==="string"&&v.trim().length>0)&&values.some(v=>GUARDED_CSP_DIRECTIVE.test(v));
}
function gate(plan,run){
 const errors=[];const bad=x=>{if(!errors.includes(x))errors.push(x);};
 if(!plan||!run||plan.schema!=="wm-header-v1"||run.schema!=="wm-header-v1")return {verdict:"REJECT",errors:["SCHEMA"]};
 if(!HASH.test(plan.commit)||!HASH.test(plan.artifact)||run.commit!==plan.commit||run.artifact!==plan.artifact)bad("PROVENANCE");
 if(typeof plan.origin!=="string"||!/^https:\/\/[a-z0-9.-]+(?::[0-9]{2,5})?\/$/i.test(plan.origin)||run.origin!==plan.origin)bad("ORIGIN");
 if(!Array.isArray(plan.routes)||!Array.isArray(run.responses)||!plan.routes.length)return {verdict:"REJECT",errors:[...errors,"ROUTES"]};
 const wanted=new Map(),seen=new Set();
 for(const e of plan.routes){
  if(!e||typeof e.path!=="string"||!safeEvidenceRoute(e.path)||wanted.has(e.path)||!["html","js"].includes(e.mime)||!HASH.test(e.sha)||!["enforce","report","observe"].includes(e.policy)||!e.headers||typeof e.headers!=="object"||Array.isArray(e.headers)){bad("PLAN");continue;}
  if(!hasPinnedPolicy(e))bad("POLICY_UNPINNED_OR_EMPTY");
  for(const [k,values] of Object.entries(e.headers)){if(!Array.isArray(values)||values.some(v=>!admissibleEvidenceHeader(k,v)))bad("UNSAFE_PLAN_HEADER");}
  wanted.set(e.path,e);
 }
 for(const r of run.responses){
  if(!r||!wanted.has(r.path)){bad("EXTRA_ROUTE");continue;}
  if(seen.has(r.path)){bad("DUPLICATE_ROUTE");continue;}
  seen.add(r.path);const e=wanted.get(r.path);
  if(r.kind!=="HTTPS_RESPONSE"||r.transport!=="https"||r.method!=="GET"||r.status!==200)bad("HTTP");
  if(!Array.isArray(r.redirects)||r.redirects.length)bad("REDIRECT");
  if(r.url!==plan.origin.slice(0,-1)+r.path)bad("URL");
  if(!HASH.test(r.sha)||r.sha!==e.sha||!Number.isSafeInteger(r.bytes)||r.bytes<1)bad("BODY");
  if(!Array.isArray(r.headers)){bad("HEADERS");continue;}
  const h=new Map();
  for(const pair of r.headers){
   if(!Array.isArray(pair)||pair.length!==2||!admissibleEvidenceHeader(pair[0],pair[1])){bad("UNSAFE_EVIDENCE_HEADER");continue;}
   const key=pair[0].toLowerCase();h.set(key,[...(h.get(key)||[]),pair[1]]);
  }
  const mime=h.get("content-type")||[];
  if(mime.length!==1||(e.mime==="html"?!/^text\/html(?:\s*;|$)/i.test(mime[0]):!/^(text|application)\/javascript(?:\s*;|$)/i.test(mime[0])))bad("MIME");
  if(e.policy==="enforce"&&!(h.get("content-security-policy")||[]).length)bad("NO_ENFORCEMENT");
  if(e.policy==="report"&&!(h.get("content-security-policy-report-only")||[]).length)bad("NO_REPORT");
  for(const [key,values] of Object.entries(e.headers)){
   const got=h.get(key.toLowerCase())||[];
   if(!Array.isArray(values)||values.some(v=>typeof v!=="string")||got.length!==values.length||got.some((v,i)=>v!==values[i]))bad("HEADER_MISMATCH");
  }
 }
 for(const path of wanted.keys())if(!seen.has(path))bad("MISSING_ROUTE");
 return {verdict:errors.length?"REJECT":"SERVED_HEADER_CONSISTENT_UNVERIFIED",errors};
}
function selfTest(){
 const a="a".repeat(64),b="b".repeat(64);
 const plan={schema:"wm-header-v1",commit:a,artifact:b,origin:"https://preview.example.test/",routes:[
 {path:"/",mime:"html",sha:a,policy:"enforce",headers:{"content-security-policy":["default-src 'self'"],"referrer-policy":["no-referrer"]}},
 ...["/auth","/auth/","/auth/action","/auth/action/index.html"].map(path=>({path,mime:"html",sha:b,policy:"report",headers:{"referrer-policy":["no-referrer"],"content-security-policy-report-only":["default-src 'self'"]}})),
 {path:"/logmate_service_worker.js",mime:"js",sha:b,policy:"enforce",headers:{"x-content-type-options":["nosniff"],"content-security-policy":["default-src 'self'"]}}
 ]};
 const run={schema:plan.schema,commit:a,artifact:b,origin:plan.origin,responses:plan.routes.map(e=>({path:e.path,url:plan.origin.slice(0,-1)+e.path,kind:"HTTPS_RESPONSE",transport:"https",method:"GET",status:200,redirects:[],sha:e.sha,bytes:100,headers:[["Content-Type",e.mime==="html"?"text/html; charset=utf-8":"text/javascript"],["Referrer-Policy","no-referrer"],["X-Content-Type-Options","nosniff"],...(e.policy==="report"?[["Content-Security-Policy-Report-Only","default-src 'self'"]]:[["Content-Security-Policy","default-src 'self'"]])]}))};
 const cases=[["baseline",()=>{},false],["source",x=>x.commit="c".repeat(64),true],["artifact",x=>x.artifact="c".repeat(64),true],["origin",x=>x.origin="https://wrong.example.test/",true],["missing",x=>x.responses.pop(),true],["extra",x=>x.responses.push({...x.responses[0],path:"/bad"}),true],["duplicate",x=>x.responses.push({...x.responses[0]}),true],["http",x=>x.responses[0].transport="http",true],["post",x=>x.responses[0].method="POST",true],["status",x=>x.responses[0].status=302,true],["redirect",x=>x.responses[0].redirects=["/"],true],["query",x=>x.responses[1].url+="?oobCode=fake",true],["foreign",x=>x.responses[1].url="https://wrong.example.test/auth",true],["body",x=>x.responses[0].sha="c".repeat(64),true],["zero",x=>x.responses[0].bytes=0,true],["boolean",x=>x.responses[0].bytes=true,true],["html-js",x=>x.responses[5].headers[0][1]="text/html",true],["no-csp",x=>x.responses[0].headers=x.responses[0].headers.filter(h=>h[0]!=="Content-Security-Policy"),true],["no-report",x=>x.responses[1].headers=x.responses[1].headers.filter(h=>h[0]!=="Content-Security-Policy-Report-Only"),true],["referrer",x=>x.responses[1].headers[1][1]="unsafe-url",true],["nosniff",x=>x.responses[5].headers=x.responses[5].headers.filter(h=>h[0]!=="X-Content-Type-Options"),true],["duplicate-header",x=>x.responses[0].headers.push(["Referrer-Policy","no-referrer"]),true],["crlf",x=>x.responses[0].headers.push(["X-Foo","a\r\nb"]),true],["null-headers",x=>x.responses[0].headers=null,true],["schema",x=>x.schema="bad",true],["path",x=>x.responses[0].url="https://preview.example.test/auth",true]];
 const failures=[];for(const [name,mutate,reject] of cases){const x=JSON.parse(JSON.stringify(run));mutate(x);const r=gate(plan,x);if((r.verdict==="REJECT")!==reject)failures.push({name,r});}
 const policyCases=[
  ["enforce-unpinned",(p,x)=>delete p.routes[0].headers["content-security-policy"]],
  ["report-unpinned",(p,x)=>delete p.routes[1].headers["content-security-policy-report-only"]],
  ["enforce-empty",(p,x)=>{p.routes[0].headers["content-security-policy"]=[""];x.responses[0].headers.find(h=>h[0]==="Content-Security-Policy")[1]="";}],
  ["enforce-whitespace",(p,x)=>{p.routes[0].headers["content-security-policy"]=["   "];x.responses[0].headers.find(h=>h[0]==="Content-Security-Policy")[1]="   ";}],
  ["enforce-report-uri-only",(p,x)=>{p.routes[0].headers["content-security-policy"]=["report-uri /csp"];x.responses[0].headers.find(h=>h[0]==="Content-Security-Policy")[1]="report-uri /csp";}],
  ["report-whitespace",(p,x)=>{p.routes[1].headers["content-security-policy-report-only"]=[" "];x.responses[1].headers.find(h=>h[0]==="Content-Security-Policy-Report-Only")[1]=" ";}],
  ["enforce-unknown-directive",(p,x)=>{p.routes[0].headers["content-security-policy"]=["not-a-csp-directive value"];x.responses[0].headers.find(h=>h[0]==="Content-Security-Policy")[1]="not-a-csp-directive value";}]
 ];
 for(const [name,mutate] of policyCases){const p=JSON.parse(JSON.stringify(plan));const x=JSON.parse(JSON.stringify(run));mutate(p,x);const r=gate(p,x);if(r.verdict!=="REJECT")failures.push({name,r});}
 
 const adversarialCases=[
 ["plan-path-traversal",(p,x)=>{p.routes[0].path="/auth/../action";x.responses[0].path=p.routes[0].path;x.responses[0].url=p.origin.slice(0,-1)+p.routes[0].path;}],
 ["plan-protocol-relative",(p,x)=>{p.routes[0].path="//evil.example.com";x.responses[0].path=p.routes[0].path;x.responses[0].url=p.origin.slice(0,-1)+p.routes[0].path;}],
 ["extra-cookie",(p,x)=>x.responses[0].headers.push(["Set-Cookie","session=SECRET"])],
 ["extra-authorization",(p,x)=>x.responses[0].headers.push(["Authorization","Bearer SECRET"])],
 ["extra-unapproved",(p,x)=>x.responses[0].headers.push(["X-Unreviewed","value"])],
 ["planned-cookie",(p,x)=>{p.routes[0].headers["set-cookie"]=["session=SECRET"];x.responses[0].headers.push(["Set-Cookie","session=SECRET"]);}],
 ["planned-sensitive-csp",(p,x)=>{const v="default-src 'self'; report-uri /?oobCode=SECRET";p.routes[0].headers["content-security-policy"]=[v];x.responses[0].headers.find(h=>h[0]==="Content-Security-Policy")[1]=v;}],
 ["header-nul",(p,x)=>x.responses[0].headers.push(["Cache-Control","max-age=0"+String.fromCharCode(0)])]
 ];
 for(const [name,mutate] of adversarialCases){const p=JSON.parse(JSON.stringify(plan));const x=JSON.parse(JSON.stringify(run));mutate(p,x);const result=gate(p,x);if(result.verdict!=="REJECT")failures.push({name,result});}
 return {count:cases.length+policyCases.length+adversarialCases.length,failures,baseline:gate(plan,run)};
}
if(typeof module!=="undefined")module.exports={gate,selfTest,hasPinnedPolicy,SAFE_CAPTURE_HEADERS,sensitiveEvidenceValue,admissibleEvidenceHeader,safeEvidenceRoute};
if(typeof require==="function"&&require.main===module){
 const fs=require("node:fs");
 if(process.argv.includes("--self-test")){const r=selfTest();console.log(JSON.stringify(r));process.exit(r.failures.length?1:0);}
 else{try{const e=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));const c=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));const r=gate(e,c);console.log(JSON.stringify(r));process.exit(r.verdict==="SERVED_HEADER_CONSISTENT_UNVERIFIED"?0:2);}catch(_){console.log(JSON.stringify({verdict:"REJECT",errors:["INPUT"]}));process.exit(2);}}
}