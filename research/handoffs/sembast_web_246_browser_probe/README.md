# Exact-version Sembast Web browser diagnostic — Stage 8

**Scope:** standalone public research only, not LogMate code or production data. Synthetic three-store fixture uses `sembast_web 2.4.6`, `sembast 3.8.11`, `idb_shim 2.9.9` and Dart 3.12.0 in Chrome. The four assertions test browser persistence after close/reopen, thrown-transaction rollback, stable-operation retry and conflicting digest rejection. The last two behaviors are **implemented by the synthetic fixture**, not an assertion that the LogMate app already enforces them.

**Run:** `dart pub get && dart test -p chrome -r expanded` from this directory. GitHub Actions pins SDK and runs the exact committed fixture. The direct dependencies are exact-version; a generated lockfile/transitive package hash is not preserved in this research artifact, so the resolved graph must be recorded for any release-grade use.

**Never promote:** Chrome headless PASS to Safari, iPadOS, Home Screen installation, managed Web Clip, LogMate 37-store restoration, native↔PWA Sync, physical power-loss durability, cross-tab callback replay, deletion/owner fences, or real product release. No private repository checkout, credentials, user data or LBK files.
