"use strict";
/* Stage 8 research handoff. Read-only HTTPS capture; NOT a release or CSP enforcement proof. */
const fs = require("node:fs");
const https = require("node:https");
const dns = require("node:dns");
const net = require("node:net");
const crypto = require("node:crypto");
const {URL} = require("node:url");
const MAX_BYTES = 32 * 1024 * 1024;
const SAFE_HEADERS = new Set([
 "content-type", "content-security-policy", "content-security-policy-report-only",
 "referrer-policy", "x-content-type-options", "cache-control", "permissions-policy",
 "cross-origin-opener-policy", "cross-origin-resource-policy", "cross-origin-embedder-policy",
 "strict-transport-security", "vary", "service-worker-allowed", "content-encoding"
]);
const HASH = /^[0-9a-f]{64}$/;
function error(code) { const e = new Error(code); e.code = code; return e; }
function safeRoute(path) {
 return typeof path === "string" && /^\/[a-zA-Z0-9_./-]*$/.test(path) &&
  !path.startsWith("//") && !path.split("/").some(x => x === "." || x === "..") &&
  !path.includes("\\") && path.length <= 512;
}
function validatePlan(plan, allowOrigin) {
 if (!plan || plan.schema !== "wm-header-v1" || !HASH.test(plan.commit) ||
     !HASH.test(plan.artifact) || typeof plan.origin !== "string" ||
     typeof allowOrigin !== "string" || plan.origin !== allowOrigin) throw error("PLAN_OR_ORIGIN");
 let u;
 try { u = new URL(plan.origin); } catch { throw error("PLAN_OR_ORIGIN"); }
 if (u.protocol !== "https:" || u.username || u.password || u.search || u.hash ||
     u.pathname !== "/" || u.href !== plan.origin || net.isIP(u.hostname) ||
     !u.hostname.includes(".") || /(?:^|\.)(?:localhost|local|internal|test)$/.test(u.hostname))
   throw error("UNSAFE_ORIGIN");
 if (!Array.isArray(plan.routes) || plan.routes.length < 1 || plan.routes.length > 128)
   throw error("ROUTE_SET");
 const seen = new Set();
 for (const r of plan.routes) {
  if (!r || !safeRoute(r.path) || seen.has(r.path) || !HASH.test(r.sha) ||
      !["html", "js"].includes(r.mime) || !["observe", "report", "enforce"].includes(r.policy) ||
      !r.headers || typeof r.headers !== "object" || Array.isArray(r.headers)) throw error("ROUTE_PLAN");
  seen.add(r.path);
 }
 return u;
}
function publicIP(ip) {
 if (net.isIP(ip) === 4) {
  const a = ip.split(".").map(Number);
  if ([0, 10, 127].includes(a[0]) || a[0] >= 224 ||
      (a[0] === 100 && a[1] >= 64 && a[1] <= 127) ||
      (a[0] === 169 && a[1] === 254) ||
      (a[0] === 172 && a[1] >= 16 && a[1] <= 31) ||
      (a[0] === 192 && (a[1] === 168 || a[1] === 0 || (a[1] === 0 && a[2] === 2))) ||
      (a[0] === 198 && (a[1] === 18 || a[1] === 19 || (a[1] === 51 && a[2] === 100))) ||
      (a[0] === 203 && a[1] === 0 && a[2] === 113)) return false;
  return true;
 }
 if (net.isIP(ip) === 6) {
  const s = ip.toLowerCase();
  return /^[23][0-9a-f]{0,3}:/.test(s) && !s.startsWith("2001:db8:") && !s.includes(".");
 }
 return false;
}
function safeLookup(hostname, options, callback) {
 dns.lookup(hostname, {all: true}, (err, records) => {
  if (err) return callback(error("DNS_FAILURE"));
  const good = (records || []).find(x => publicIP(x.address));
  if (!good) return callback(error("DNS_NONPUBLIC"));
  callback(null, good.address, good.family);
 });
}
function filterHeaders(raw) {
 if (!Array.isArray(raw) || raw.length % 2) throw error("INVALID_RAW_HEADERS");
 const out = [];
 for (let i = 0; i < raw.length; i += 2) {
  const k = raw[i], v = raw[i + 1];
  if (typeof k !== "string" || typeof v !== "string") throw error("INVALID_RAW_HEADERS");
  if (SAFE_HEADERS.has(k.toLowerCase())) {
   if (!/^[a-z0-9-]+$/i.test(k) || /[\r\n]/.test(v)) throw error("INVALID_RAW_HEADERS");
   out.push([k, v]);
  }
 }
 return out;
}
function requestOnce(url, {maxBytes = MAX_BYTES, timeoutMs = 15000} = {}) {
 return new Promise((resolve, reject) => {
  const req = https.request(url, {
   method: "GET", rejectUnauthorized: true, lookup: safeLookup,
   headers: {"Accept": "*/*", "Accept-Encoding": "identity", "User-Agent": "MintTap-WM-ReadOnly-Header-Capture/1"}
  }, res => {
   let headers;
   try { headers = filterHeaders(res.rawHeaders); } catch (e) { res.destroy(); return reject(e); }
   const h = crypto.createHash("sha256"); let bytes = 0; let settled = false;
   res.on("data", chunk => {
    bytes += chunk.length;
    if (bytes > maxBytes) { settled = true; res.destroy(error("BODY_LIMIT")); return; }
    h.update(chunk);
   });
   res.on("end", () => { if (!settled) resolve({status: res.statusCode, headers, sha: h.digest("hex"), bytes}); });
   res.on("error", e => reject(e.code === "BODY_LIMIT" ? e : error("RESPONSE_FAILURE")));
  });
  req.setTimeout(timeoutMs, () => req.destroy(error("TIMEOUT")));
  req.on("error", e => reject(["BODY_LIMIT", "TIMEOUT", "DNS_NONPUBLIC", "DNS_FAILURE"].includes(e.code) ? e : error("REQUEST_FAILURE")));
  req.end();
 });
}
async function collect(plan, {allowOrigin, transport = requestOnce, maxBytes = MAX_BYTES} = {}) {
 validatePlan(plan, allowOrigin);
 const responses = [];
 for (const r of plan.routes) {
  const url = plan.origin.slice(0, -1) + r.path;
  let result;
  try { result = await transport(url, {maxBytes}); }
  catch (e) { throw error("CAPTURE_" + (e.code || "FAILED")); }
  if (!result || !Number.isInteger(result.status) || !HASH.test(result.sha) ||
      !Number.isSafeInteger(result.bytes) || result.bytes < 0 || result.bytes > maxBytes ||
      !Array.isArray(result.headers)) throw error("CAPTURE_INVALID");
  const flat = result.headers.flatMap(x => Array.isArray(x) && x.length === 2 ? x : [null, null]);
  const headers = filterHeaders(flat);
  if (headers.some(([k,v]) => k.toLowerCase() === "content-encoding" && v.toLowerCase().trim() !== "identity")) throw error("ENCODED_RESPONSE");
  responses.push({path:r.path,url,kind:"HTTPS_RESPONSE",transport:"https",method:"GET",
   status:result.status,redirects:result.status >= 300 && result.status < 400 ? ["NOT_FOLLOWED"] : [],
   sha:result.sha,bytes:result.bytes,headers});
 }
 return {schema:"wm-header-v1",commit:plan.commit,artifact:plan.artifact,origin:plan.origin,responses,
  captureKind:"READ_ONLY_HTTPS_BYTES_UNATTESTED",collector:"wm-https-capture-v1"};
}
async function cli(argv) {
 if (argv.length !== 6 || argv[0] !== "--plan" || argv[2] !== "--allow-origin" || argv[4] !== "--out")
   throw error("USAGE");
 const plan = JSON.parse(fs.readFileSync(argv[1], "utf8"));
 const run = await collect(plan, {allowOrigin:argv[3]});
 const {gate} = require("./pwa_served_header_evidence_gate.js");
 const result = gate(plan, run);
 if (!result || result.verdict !== "SERVED_HEADER_CONSISTENT_UNVERIFIED") throw error("EVIDENCE_REJECTED");
 fs.writeFileSync(argv[5], JSON.stringify(run,null,2) + "\n", {flag:"wx",mode:0o600});
 process.stdout.write("CAPTURE_WRITTEN_CONSISTENT_UNVERIFIED\n");
}
module.exports = {collect, validatePlan, safeRoute, filterHeaders, publicIP, requestOnce, MAX_BYTES};
if (require.main === module) cli(process.argv.slice(2)).catch(e => {
 console.error("CAPTURE_FAILED:" + (e.code || "INVALID_INPUT")); process.exitCode = 2;
});
