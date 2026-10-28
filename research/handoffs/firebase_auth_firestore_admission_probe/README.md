# Stage 8 — Firebase Auth + Firestore emulator admission probe

Research-only executable fixture. **No LogMate source, Firebase production project, secrets, or deploy.** Run from this directory with Node 22, Java 21 and npm:

```sh
npm install --no-audit --no-fund
FIREBASE_AUTH_EMULATOR_HOST=127.0.0.1:9099 FIRESTORE_EMULATOR_HOST=127.0.0.1:8080 GCLOUD_PROJECT=demo-web-manager-auth npx firebase emulators:exec --only auth,firestore --project demo-web-manager-auth "node --test admission_probe.mjs"
```

The fixture uses **real emulator-issued Auth ID tokens**, Firebase Admin `verifyIdToken` with `FIREBASE_AUTH_EMULATOR_HOST`, real Firestore emulator transactions and a local HTTP endpoint. Direct Firestore client REST is denied by the fixture's deny-all rules; privileged Admin SDK access is separately demonstrated. An original receipt cannot grant a revoked owner new authority. Concurrent same-ID submissions share one receipt; conflicting digest is rejected. HTTP connection loss is injected **after** the Firestore transaction resolves.

Do not run with production credentials. The Auth emulator issues unsigned development tokens; `FIREBASE_AUTH_EMULATOR_HOST` must never be set in production. The Firestore emulator does not perfectly model production contention, indexes, multi-region durability or IAM. No Firebase Functions deployed runtime, App Check, production JWT signature, actual LogMate wire/digest, 37-store Apply/Cursor, Safari or EFB is tested.

Original FE01–FE13: **13/13 hosted emulator subtests PASS** at [run 40606283235](https://github.com/yhappcom/web-manager/actions/runs/40606283235), checkout `29f7bf7a` (Node TAP total 14 including suite). Extended FE14–FE16 test ledger revocation, per-ledger identity isolation and concurrent changed-digest collision; **their exact-ref hosted execution is OPEN until inspected**. The fixture does not recompute caller-provided digest, does not call `verifyIdToken(token, true)`, and does not restart the Firestore emulator or Node process in FE07. If a test fails, preserve the first failure and do not claim product failure. Dependencies are exact direct versions but no committed transitive lockfile; CI prints its resolved tree. [Integrated research 523](../../523_stage8_pwa_remote_admission_receipt_owner_boundary_20261028.md) owns interpretation.
