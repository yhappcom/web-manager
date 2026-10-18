# Stage 8 PWA CI archive delivery audit — 2026-10-18

Canonical baseline: web-manager main 2c706c19; LogMate main 61016665 (read-only).

Two historical GitHub Actions PWA acceptance archives (runs 38341345115 and 38293013412) were independently inspected. Both workflows succeeded. Each archive contains 954 entries and an offline manifest with 952 resource records. Exactly 951 records were present and byte/hash matched. The required hidden build marker `.last_build_id` was missing from both archives. This is an archived artifact delivery FAIL, not a production incident. The current Firebase Hosting configuration also excludes hidden files. The archived acceptance builds use database capability 15; current LogMate main declares 16. These are not current normal production builds.

Track E owns release delivery and Hosting admission; A supplies Service Worker lifecycle; C owns actual browser and device validation; B and D consume truthful recovery and claims boundaries. Production validation remains OPEN and PWA release HOLD.

Next: exclude non-runtime build markers from the precache manifest after engineering review, verify post-upload archive and served bytes, then test actual Worker installation and offline data recovery. Sources: https://github.com/yhappcom/logmate/actions/runs/38341345115 ; https://github.com/yhappcom/logmate/actions/runs/38293013412 ; https://github.com/actions/upload-artifact/blob/main/README.md .
