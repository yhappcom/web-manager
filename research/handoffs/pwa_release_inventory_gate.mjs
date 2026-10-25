#!/usr/bin/env node
// Web Manager research handoff. Not a product deployer or release authority.
import { createHash } from 'node:crypto';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REQUIRED = ['index.html', 'flutter_bootstrap.js', 'manifest.json', 'logmate_service_worker.js', 'logmate-offline-manifest.json', 'auth/action/index.html', 'main.dart.js', 'canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm'];
const SAFE_IGNORES = new Set(['firebase.json', '**/.*', '**/node_modules/**']);
// Firebase serves matching static content before a rewrite. An auth/index.html
// added to an otherwise identical release tree can shadow the /auth/ alias.
// This is a conservative source-level guard, not a Firebase emulator oracle.
const SHADOWING_AUTH_STATIC_PATHS = new Set(['auth/index.html']);
const REQUIRED_AUTH_REWRITES = new Map([
  ['/auth', '/auth/action/index.html'],
  ['/auth/', '/auth/action/index.html'],
  ['/auth/action', '/auth/action/index.html'],
]);
const sha256 = b => createHash('sha256').update(b).digest('hex');
const ACCEPTANCE_MARKER = 'LOGMATE_PERSISTENCE_ACCEPTANCE_FLIGHT_V1';
const ACCEPTANCE_MARKER_BYTES = Buffer.from(ACCEPTANCE_MARKER);
const REVIEWED_HOSTING_KEYS = new Set(['public', 'ignore', 'headers', 'rewrites', 'redirects', 'cleanUrls', 'trailingSlash']);
const REVIEWED_CACHE_HEADER = 'no-cache, no-store, must-revalidate';
const digestPacket = p => sha256(Buffer.from(JSON.stringify({schema:p.schema,releaseMode:p.releaseMode,sourceSha:p.sourceSha,files:p.files})));
async function assertNormal(root) {
  const js = await fs.readFile(path.join(root, 'main.dart.js'), 'utf8');
  if (js.includes(ACCEPTANCE_MARKER)) fail('development acceptance harness in NORMAL bytes');
}
const fail = message => { throw new Error(message); };

export async function inventory(root) {
  const base = path.resolve(root);
  const stat = await fs.lstat(base);
  if (!stat.isDirectory() || stat.isSymbolicLink()) fail('root must be a real directory');
  const rows = [];
  const seen = new Set();
  async function visit(dir, prefix) {
    for (const entry of (await fs.readdir(dir)).sort()) {
      if (entry === '.' || entry === '..' || /[\r\n\0]/.test(entry)) fail('unsafe filename');
      if (entry.startsWith('.')) fail(`hidden file/directory requires explicit review: ${prefix}${entry}`);
      if (entry === 'node_modules') fail('node_modules would be excluded from Hosting');
      const rel = prefix + entry;
      // Firebase Hosting ignores this root file even when raw trees match.
      if (rel === 'firebase.json') fail('Hosting-ignored root firebase.json cannot be treated as a deployed asset');
      if (SHADOWING_AUTH_STATIC_PATHS.has(rel.split(path.sep).join('/'))) fail(`static resource shadows reviewed Auth rewrite: ${rel}`);
      const folded = rel.toLowerCase();
      if (seen.has(folded)) fail(`case-fold collision: ${rel}`);
      seen.add(folded);
      const absolute = path.join(dir, entry);
      const info = await fs.lstat(absolute);
      if (info.isSymbolicLink()) fail(`symlink forbidden: ${rel}`);
      if (info.isDirectory()) await visit(absolute, rel + '/');
      else if (info.isFile()) {
        const bytes = await fs.readFile(absolute);
        if (bytes.includes(ACCEPTANCE_MARKER_BYTES)) fail(`development acceptance marker in ${rel}`);
        rows.push({ path: rel.split(path.sep).join('/'), bytes: bytes.length, sha256: sha256(bytes) });
      } else fail(`special file forbidden: ${rel}`);
    }
  }
  await visit(base, '');
  rows.sort((a,b) => a.path.localeCompare(b.path, 'en'));
  for (const required of REQUIRED) if (!rows.some(r => r.path === required)) fail(`required resource missing: ${required}`);
  return rows;
}

function assertInventory(rows) {
  if (!Array.isArray(rows) || rows.length === 0) fail('invalid inventory');
  const seen = new Set();
  for (const row of rows) {
    if (typeof row?.path !== 'string' || !row.path || row.path.startsWith('/') || row.path.includes('\\') || row.path.split('/').some(x => !x || x === '.' || x === '..' || x.startsWith('.')) || /[\r\n\0]/.test(row.path)) fail('invalid inventory path');
    if (!Number.isSafeInteger(row.bytes) || row.bytes < 0 || !/^[a-f0-9]{64}$/.test(row.sha256)) fail('invalid inventory digest/size');
    const folded = row.path.toLowerCase();
    if (seen.has(folded)) fail('duplicate inventory path');
    seen.add(folded);
  }
  for (const required of REQUIRED) if (!seen.has(required.toLowerCase())) fail(`required resource missing: ${required}`);
}

function assertHostingRoutes(hosting) {
  // Product-specific routing guard, not an emulator or HTTPS response oracle.
  if (hosting.redirects !== undefined && (!Array.isArray(hosting.redirects) || hosting.redirects.length !== 0)) fail('unreviewed Hosting redirect');
  if (hosting.cleanUrls !== undefined || hosting.trailingSlash !== undefined) fail('unreviewed Hosting URL normalization');
  if (!Array.isArray(hosting.rewrites) || hosting.rewrites.length !== REQUIRED_AUTH_REWRITES.size) fail('unreviewed Hosting rewrite set');
  const seen = new Set();
  for (const rule of hosting.rewrites) {
    if (!rule || Object.keys(rule).sort().join(',') !== 'destination,source' ||
        typeof rule.source !== 'string' || !REQUIRED_AUTH_REWRITES.has(rule.source) ||
        REQUIRED_AUTH_REWRITES.get(rule.source) !== rule.destination || seen.has(rule.source)) fail('unreviewed Hosting rewrite');
    seen.add(rule.source);
  }
}

function assertHostingHeadersAndOptions(hosting) {
  // This is a pinned, source-level projection policy, not a served-header oracle.
  for (const key of Object.keys(hosting)) {
    if (!REVIEWED_HOSTING_KEYS.has(key)) fail(`unreviewed Hosting option: ${key}`);
  }
  if (!Array.isArray(hosting.headers) || hosting.headers.length !== 1) fail('unreviewed Hosting header rules');
  const rule = hosting.headers[0];
  if (!rule || Object.keys(rule).sort().join(',') !== 'headers,source' ||
      rule.source !== '**' || !Array.isArray(rule.headers) || rule.headers.length !== 1) fail('unreviewed Hosting header rules');
  const header = rule.headers[0];
  if (!header || Object.keys(header).sort().join(',') !== 'key,value' ||
      header.key !== 'Cache-Control' || header.value !== REVIEWED_CACHE_HEADER) fail('unreviewed Hosting response header');
}

function compare(expected, actual, label) {
  assertInventory(expected);
  assertInventory(actual);
  const a = new Map(expected.map(row => [row.path, row]));
  const b = new Map(actual.map(row => [row.path, row]));
  for (const [name, row] of a) {
    const got = b.get(name);
    if (!got) fail(`${label}: missing ${name}`);
    if (got.bytes !== row.bytes || got.sha256 !== row.sha256) fail(`${label}: bytes differ ${name}`);
  }
  for (const name of b.keys()) if (!a.has(name)) fail(`${label}: unexpected ${name}`);
}

export async function snapshot(root, sourceSha) {
  if (!/^[0-9a-f]{40}$/.test(sourceSha)) fail('exact 40-character source SHA required');
  const files = await inventory(root);
  await assertNormal(root);
  const packet = { schema: 1, releaseMode: 'NORMAL', sourceSha, files };
  return {...packet, inventoryDigest: digestPacket(packet)};
}

export async function verify(packet, downloadedRoot, stagedRoot, firebaseConfigPath, expectedSourceSha, trustedInventoryDigest) {
  if (packet?.schema !== 1 || packet?.releaseMode !== 'NORMAL' || packet?.sourceSha !== expectedSourceSha || !/^[0-9a-f]{40}$/.test(expectedSourceSha)) fail('provenance mode/source mismatch');
  assertInventory(packet.files);
  if (!/^[a-f0-9]{64}$/.test(trustedInventoryDigest) || packet.inventoryDigest !== trustedInventoryDigest || digestPacket(packet) !== trustedInventoryDigest) fail('trusted inventory digest mismatch');
  const configPath = path.resolve(firebaseConfigPath);
  const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
  if (!config.hosting || Array.isArray(config.hosting) || typeof config.hosting.public !== 'string') fail('single Hosting target required');
  if (!Array.isArray(config.hosting.ignore) || config.hosting.ignore.length !== SAFE_IGNORES.size ||
      new Set(config.hosting.ignore).size !== SAFE_IGNORES.size || config.hosting.ignore.some(p => !SAFE_IGNORES.has(p))) fail('unreviewed Hosting ignore rule');
  const actualPublic = path.resolve(path.dirname(configPath), config.hosting.public);
  if (actualPublic !== path.resolve(stagedRoot)) fail(`Hosting public directory mismatch: ${config.hosting.public}`);
  const [downloadedCanonical, stagedCanonical] = await Promise.all([fs.realpath(downloadedRoot), fs.realpath(stagedRoot)]);
  if (downloadedCanonical === stagedCanonical) fail('download and Hosting staging roots must be distinct real directories');
  assertHostingRoutes(config.hosting);
  assertHostingHeadersAndOptions(config.hosting);
  compare(packet.files, await inventory(downloadedRoot), 'download');
  compare(packet.files, await inventory(stagedRoot), 'hosting');
  await assertNormal(downloadedRoot);
  await assertNormal(stagedRoot);
  return { verdict: 'PASS', files: packet.files.length, sourceSha: expectedSourceSha, note: 'Byte inventory only: not a release signature, Dart harness check, HTTPS observation, or device validation.' };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const [, , command, ...args] = process.argv;
    if (command === 'snapshot' && args.length === 3) {
      const packet = await snapshot(args[0], args[1]);
      await fs.writeFile(args[2], JSON.stringify(packet, null, 2) + '\n', { flag: 'wx' });
      console.log(`SNAPSHOT ${packet.files.length} files; source ${packet.sourceSha}; inventoryDigest ${packet.inventoryDigest}`);
    } else if (command === 'verify' && args.length === 6) {
      const packet = JSON.parse(await fs.readFile(args[0], 'utf8'));
      console.log(JSON.stringify(await verify(packet, args[1], args[2], args[3], args[4], args[5])));
    } else fail('usage: snapshot <normal-root> <source-sha> <new-inventory.json> | verify <trusted-inventory.json> <downloaded-root> <hosting-root> <firebase.json> <source-sha> <trusted-inventory-digest>');
  } catch (error) { console.error(`REJECT: ${error.message}`); process.exitCode = 1; }
}
