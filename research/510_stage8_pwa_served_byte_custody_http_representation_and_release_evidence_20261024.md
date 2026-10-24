# 510 — Stage 8 PWA served-byte custody, HTTP representation traps, and release promotion evidence

Date: 2026-10-24 (Asia/Seoul). **Applied Stage 8 Security / Privacy / Trust**; sequential Stages 1–12 were historically passed as *generic competency*, not product certification. Primary owner **E Web Architecture/Security/Operations**. A supplies HTTP/Service Worker mechanics; C owns independent falsification; B/D consume consequences. **PRODUCT HOST/RUNTIME/DEVICE VALIDATION OPEN; PWA RELEASE HOLD.**

## 1. Canonical refresh and highest-value bottleneck [SOURCE / DEPENDENCY]

At run start Web Manager `main@74e2dd176efa64f4dc00cc68cd09f457a448ea55`: read AGENTS.md, SPECIALIST_TRACKS.md, LEARNING_ROADMAP.md, STATUS.md, research/README.md, studies 508–509 and latest commits. LogMate read-only latest `main@27f926aa6ea1e032dfa9affc598e8e41131eb092`: inspected `firebase.json`, `Makefile`, `tool/verify_pwa_artifact.dart`, `web/flutter_bootstrap.js` and `.github/workflows/data001-pwa-artifact-validation.yml`. Design Studio `progress/WEB_STATUS.md` reports W121 Stage 3 PRACTICE with runtime/AT/human gates OPEN. Software Engineering Studio `research/README.md` reports M006 bounded Chromium/macOS Safari transfer, D006 protocol interruption, Q006 CI-verdict evidence, not actual LogMate hosted release acceptance. Marketing Manager `STATUS.md` 2026-10-24 14:28 KST keeps LogMate pilot and ads HOLD.

**Track comparison:** E remains the highest-risk gate: NORMAL artifact identity must survive archive, deployment input and served HTTPS response, and neither Worker nor local ledger may be sacrificed for rollback. C has the strongest immediate verification dependency: an independent HTTP oracle is missing after 509's disk-only gate. A supplies representation/caching/redirect semantics. B has no new user-journey evidence and should consume readiness distinctions; D has no trustworthy install/ads measurement without a verified host. Allocate primary work to E+C/A, not another generic PWA primer.

## 2. History/problem → principle → standards → present implementation [SOURCE / SYNTHESIS]

An identical Git source tree does not guarantee identical built bytes; identical disk bytes do not guarantee the selected deploy root; identical deploy input does not guarantee served responses. A CDN may return stale, transformed, compressed, redirected or rewritten responses; a 200 status alone is not a byte oracle. Conversely, a valid content-coded response can be operationally correct yet differ byte-for-byte from the source file's encoded wire representation. **The audit must name the representation being compared.**

Primary/current references checked 2026-10-24:
- RFC 9111 HTTP caching (no-cache/no-store, validation, cache obligations): https://www.rfc-editor.org/rfc/rfc9111.html
- WHATWG Fetch Standard (cache and redirect modes, browser fetch behavior): https://fetch.spec.whatwg.org/
- Firebase Hosting full configuration (public/ignore/rewrites/headers): https://firebase.google.com/docs/hosting/full-config
- Firebase Hosting cache behavior and CDN invalidation: https://firebase.google.com/docs/hosting/manage-cache
- GitHub artifact attestation provenance, availability and verification: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- GitHub attestation trust limits: https://docs.github.com/en/actions/concepts/security/artifact-attestations

**Exact source:** LogMate `firebase.json` sets Hosting `public: build/web`, `ignore: [firebase.json, **/.*, **/node_modules/**]`, all-path `Cache-Control: no-cache, no-store, must-revalidate`, and three `/auth` rewrites. The PWA CI builds NORMAL to `build/web-normal`, then builds Acceptance to `build/web` and uploads **Acceptance** only. `Makefile` verifies both using the product's Dart verifier; no observed release deploy in that workflow. The NORMAL-vs-Hosting path mismatch remains a *configuration hazard*, not evidence of deployed Acceptance code. Auth rewrites are **not** offline shell URLs and must not be used to assert cached navigation readiness.

## 3. Independent read-only served-byte oracle [VALIDATION / E+C]

New `research/handoffs/pwa_served_byte_gate.py` consumes the **external schema-1 NORMAL receipt** produced by study 509, plus an independently supplied SHA-256 pin of the exact receipt file and an explicit bare HTTPS origin. It is a **non-deploying read-only verifier**; it does not fetch private user data or use cookies, credentials, tokens or an authenticated session.

The oracle:
1. Rejects Acceptance receipts, incorrect external receipt pin, malformed inventory/tree/Worker digest, missing critical paths, traversal/encoded paths, URL credentials, query, fragment and non-HTTPS origin (loopback HTTP requires an explicit *test-only* flag).
2. GETs the exact paths with `Accept-Encoding: identity`, `Cache-Control: no-cache` and `Pragma: no-cache`, rejecting redirects, non-200, final-URL drift and content-coding other than identity. It hashes **response body bytes**, not a 304 validator, ETag, metadata-only HEAD or CDN deployment label.
3. Rejects HTML rewrites returned for JS, invalid media type for critical HTML/JS/JSON/WASM, mismatched Content-Length, size or SHA-256, and missing conservative no-cache/no-store response policy on mutable entrypoints. These cache directives are a **LogMate-specific conservative release policy**, not a universal requirement for all PWAs.
4. Requires 2–5 independent sequential rounds. `--scope critical` checks 8 entrypoints; `--scope all` checks every receipt inventory path (including files outside the offline manifest). It records per-path response status, digest, media type, cache-control and ETag without interpreting ETag as content authenticity.
5. Emits only `HOST_CRITICAL_MATCH_UNVERIFIED` or `HOST_TREE_MATCH_UNVERIFIED`; any negative control emits HOLD. Neither result is `PRODUCTION_PASS`, a trusted attestation, a proof of all CDN points of presence, or browser/Service Worker readiness.

**Executable evidence:** Python 3 unittest against an isolated localhost HTTP server: **18/18 PASS** on 2026-10-24, including two-round critical and all-tree positives; byte drift; unlisted-file drift caught only in all-tree; 302 redirect; 404; SPA HTML rewrite; Content-Encoding mismatch; mutable cache-policy failure; wrong Content-Length; wrong receipt pin; Acceptance receipt; Worker digest mismatch; unsafe paths; insecure origin; credentials/query; one-round attempt; invalid scope. Python syntax compilation PASS. Tests are of the verifier against a synthetic HTTP server, **not LogMate Hosting**.

Example **only after Engineering provides an approved NORMAL release receipt, its independently anchored digest and a verified target origin**:

```sh
python3 research/handoffs/pwa_served_byte_gate.py \
  --receipt normal-release-receipt.json \
  --receipt-sha256 <independently-pinned-64-hex> \
  --origin https://<approved-normal-release-host> \
  --scope critical --rounds 2 --out hosted-critical-evidence.json
python3 research/handoffs/pwa_served_byte_gate.py \
  --receipt normal-release-receipt.json \
  --receipt-sha256 <same-independent-pin> \
  --origin https://<approved-normal-release-host> \
  --scope all --rounds 2 --out hosted-tree-evidence.json
```

No actual NORMAL archive/receipt pin or approved LogMate release URL was supplied. **No real hosted request or deployment was made.**

## 4. Twelve operational falsifiers and bounded decisions [CONTRADICTION / MINTTAP DECISION / OPEN]

| Case | Incorrect inference | Required counterevidence / disposition |
| --- | --- | --- |
| H01 | A 200 means expected JS | JS URL returning SPA HTML must HOLD by type and bytes. |
| H02 | ETag/304 proves same body | Hash full 200 body against independently pinned receipt. |
| H03 | Same appBuildId means same Worker | Verify independent Worker SHA from receipt; no shell-only promotion. |
| H04 | Redirected URL is equivalent | Reject redirects for release entrypoints until explicitly reviewed. |
| H05 | Critical 8 files represent full release | `critical` is sample-only; `all` is separate, including unlisted files. |
| H06 | Successful disk gate means hosted bytes | Different evidence tiers; no promotion without independent GET. |
| H07 | `no-cache` request guarantees latest deploy | HTTP validation is not organizational release authorization. |
| H08 | One CDN region represents all devices | Repeat across regions/conditions and device cohorts where applicable. |
| H09 | An independently hashed receipt is signed | SHA pin is an integrity anchor only; protect approval provenance separately. |
| H10 | gzip wire bytes must equal uncompressed file | This conservative oracle requests identity and HOLDs coding; legitimate compressed variants require a distinct representation-aware test. |
| H11 | Host match proves offline app | Run Worker install/claim/overlap, offline cold start and process restart separately. |
| H12 | Host match proves local records survive | Populated 37-store semantic restore, R03/R04 collision, physical Safari/MDM remain separate. |

**Design decision candidate:** Production promotion requires independently anchored NORMAL build/receipt and archived custody, exact deployment selection, sampled then full served-byte checks, correct cache/route headers, actual Worker/browser offline and data-preserving update, and physical policy-matched iPad evidence. A passed receipt+host hash cannot authorize remote Sync or suppress a backup requirement. Do not modify the product's `firebase.json` automatically or promote Acceptance to make a gate green.

**Security and quality limits:** The Python HTTP client is not a browser; it does not execute Service Workers, model browser caches, enforce CSP, prove DNS/CDN independence, or capture signed deployment identity. An HTTP request with no-cache is not a guaranteed cache bypass across all intermediaries. The code rejects content coding rather than decoding it, may HOLD on valid deployments that force compression, has no pagination/progress or global traffic budget for 880+ files, and does not independently validate the *producer* receipt signature or GitHub OIDC provenance. The schema-1 receipt may be forged if attacker controls both bytes and pin. Real deployments may use path prefixes, query routing, alternate MIME mappings, hosting transforms or access controls; each requires a reviewed, explicit policy extension, not silent weakening. For privacy, only static public release paths should be probed.

**Attestation boundary:** GitHub Docs currently state public-repository attestations are available across current plans, while private/internal repositories require Enterprise Cloud. Verify actual repository visibility/entitlement before prescribing `actions/attest`; an attestation proves provenance claims only under verified identity/policy and **does not establish code security or hosted bytes**.

## 5. Cross-track transfer and next evidence boundary [TRANSFER VALIDATION / DEPENDENCY / CHANGE WATCH]

- **E owner:** release approval and origin identity; immutable NORMAL selection; independent receipt/attestation pin; incident rollback preserving older runnable shell and unique local ledger. Engineering implements product CI/deployment; Web Manager defines web release evidence.
- **A supplier:** Fetch/HTTP caching semantics, content coding, redirects, Service Worker control and versioned cache. Browser `cache: no-store` differs from this external Python GET; neither alone certifies Worker-installed resources.
- **C supplier:** 18 falsifiers and exact source/receipt/host/region/time/probe evidence; extend to browser tests W01–W28, 37-store R01–R12 and iPad I01–I16. CI exit status must be coupled to semantic verdict (Engineering Q006 transfer).
- **B consumer:** do not say 'Offline ready' based on a host check. Distinguish host deployed, shell cached, this client controlled, local data present, backup verified and Sync confirmed. Design Studio W121 human/AT work remains OPEN.
- **D consumer/challenger:** use privacy-minimized release/installation and cohort telemetry only after valid production identity; do not send flight records or claim automatic iPad↔native background Sync. Marketing Manager LogMate pilot/ads remain HOLD.
- **CHANGE WATCH:** Firebase Hosting cache/rewrite behavior, WebKit Home Screen/MDM policies, GitHub attestation eligibility, browser content-coding/cache behavior and OS background capabilities are version-/policy-sensitive.

**End-of-run adjacent-value check:** The immediate adjacent question after disk custody was whether an independent exact-response oracle could falsify incorrect deployment selection and common HTTP traps. Implemented and exercised both scopes and 18 positive/negative tests. A real NORMAL receipt, approved HTTPS deployment and permitted browser/iPad environments are now the material context boundary; additional synthetic scenarios cannot close it. **Applied Stage 8 ACTIVE / E primary bottleneck / Production validation OPEN / PWA release HOLD.** Product, Design Studio, Engineering and Marketing repositories remained read-only.
