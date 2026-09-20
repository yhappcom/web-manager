# 169 — PWA Redress Case Confidentiality Across Delegated/Representative Access, Shared/Managed Devices & Support Collaboration

Status: **PASS (generic) / PRODUCT + IDP + DELEGATION + SUPPORT + MDM + LEGAL + HUMAN/AT + MANAGED-FLEET VALIDATION OPEN**  
Date: 2026-09-20  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Major consumers: Track B case/disclosure UX; Track C authorization/privacy/accessibility validation; Track A browser/session/storage/shared-device mechanics; Track D purpose-limited operational measurement.  
Dependencies: 166 explainability/redress; 167 identity/authorization/anti-abuse; 168 notification/contact-channel integrity.

## Why this study exists

168 prevents a notification/contact channel from becoming authority. The adjacent failure is broader: a representative may legitimately act for a subject but not see every case or every evidence item; a support operator may need to diagnose a workflow without receiving adjudication authority; and an organization may own/manage an iPad without owning the human subject's redress rights or every record visible in a browser session.

Central rule:

> **Confidentiality follows the specific subject–case–capability–purpose relationship, not device ownership, organizational employment, support role, case-ID possession or prior access. Delegate only the minimum operations and views required, and re-evaluate authority at every consequential request.**

## Five-track balance

- **A Platform/Browser:** high dependency supplier. Owns session/origin/storage/SW/cache mechanics and platform facts around shared/managed devices. Browser state cannot prove human delegation.
- **B UX/IA/Content:** very high dependency pressure. Owns role-aware case views, explicit `acting for` context, disclosure-safe summaries, delegation/revocation UX and shared-device exit/recovery requirements.
- **C Quality/Accessibility:** high dependency pressure. Owns horizontal/vertical authorization, cache/history/back-navigation leakage, role transition, keyboard/AT and physical-device validation.
- **D Search/Analytics:** bounded consumer. May measure aggregate workflow quality; case evidence, representative relationships and support-view content must not become acquisition/marketing profiles.
- **E Security/Operations:** **bottleneck/owner**. Owns capability-scoped delegation, object-level enforcement, support separation of duties, managed-device trust boundaries, audit/minimization and incident response.

## SOURCE

### NIST SP 800-53 Rev.5 / Release 5.2.0 — least privilege and separation

NIST AC-6 defines least privilege as allowing only authorized accesses necessary to accomplish assigned tasks. The Access Control family separately includes access enforcement, information-flow enforcement and separation of duties. These controls support treating `representative`, `support`, `employer admin`, and `device manager` as different authority relationships rather than broad roles that inherit all case content.

Sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/fpd
- https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

### NIST SP 800-162 / SP 800-205 — authorization can depend on subject, object, operation and environment

NIST's ABAC model evaluates attributes of the requesting subject, protected object, requested operation and relevant environment against policy. SP 800-205 emphasizes lifecycle/assurance considerations for the attributes used by access-control systems.

Sources:
- https://csrc.nist.gov/pubs/sp/800/162/upd2/final
- https://csrc.nist.gov/pubs/sp/800/205/final

Transfer: this supports a capability/object model such as `representative R may read explanation class X for case C until T`, rather than a global `representative=true` switch. It does **not** require MintTap/LogMate to implement a particular ABAC product.

### OWASP Authorization — least privilege, deny by default and object-level checks

OWASP recommends least privilege, deny-by-default and validating permission for the specific object/function on every request. Guess-resistant identifiers do not replace authorization; possession of an object ID is not permission.

Sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html

### Apple — Shared iPad separates users, but management is not subject authority

Apple documents Shared iPad as a supervised, MDM-managed multiuser mode using organization-issued Managed Apple Accounts. User data is separated into protected storage domains; temporary-session data is deleted at sign-out. Apple also documents device- and user-channel management profiles and local/remote authentication options.

Sources:
- https://support.apple.com/guide/security/secd99f373ef/web
- https://support.apple.com/guide/deployment/dep6fa9dd532/1/web/1.0
- https://support.apple.com/guide/deployment/depa60247ff8/1/web/1.0

TRANSFER VALIDATION: Apple platform separation reduces some shared-device risks but does not establish LogMate PWA case confidentiality, representative authority, browser-profile semantics, MDM policy, or actual company-iPad configuration. Those remain OPEN.

## SYNTHESIS — separate eight authority/disclosure objects

Do not collapse these into `has access`:

1. **Subject** — person/entity whose case or rights are involved.
2. **Actor** — currently authenticated requester.
3. **Relationship/delegation** — why the actor may act for the subject, with provenance/currentness.
4. **Case/object scope** — which case, evidence item, explanation class or operation is in scope.
5. **Capability** — read summary, submit evidence, receive notice, withdraw, appeal, administer delegation, adjudicate, etc.
6. **Purpose/context** — support diagnosis, representation, adjudication, device administration, emergency recovery, etc.
7. **Device/session context** — browser/session/device posture; useful risk context, never sufficient subject authority by itself.
8. **Disclosure projection** — minimum fields/content the actor needs for that capability.

Persistent guards:
- `authenticated actor ≠ subject`;
- `representative for one case ≠ representative for all cases`;
- `may submit evidence ≠ may read all evidence`;
- `may view explanation ≠ may adjudicate`;
- `support access ≠ subject authority`;
- `device ownership ≠ data-subject authority`;
- `MDM enrollment ≠ representative consent`;
- `case ID possession ≠ case entitlement`;
- `access granted once ≠ access current forever`;
- `shared device ≠ shared account`;
- `browser cache present ≠ current disclosure authorization`;
- `audit need ≠ unrestricted case-content retention`.

## Delegation model — capability and object scope, not role inflation

A durable delegation should identify, at minimum, the subject, delegate/representative, allowed case/object scope, allowed capabilities, provenance/authority basis, effective generation, expiry/review conditions and revocation/supersession state. Product/legal rules determine whether delegation is self-service, organizational, statutory, guardian-based or reviewer-approved; generic research must not invent that authority.

Prefer narrow grants. A representative who can upload a supporting document may not need identity-document history, unrelated cases, internal fraud signals, privileged legal notes, other representatives, account recovery data or contact-channel secrets. Server-side object-level authorization remains mandatory even if the UI hides those fields.

Delegation changes create a new authority generation. Revocation must prevent future reads/mutations and queued consequence-bearing operations from using stale authority. It cannot erase material already legitimately disclosed to an external human/device, so claims about post-revocation confidentiality must remain bounded.

## Support collaboration — diagnostic access without silent adjudication

Support work should be split into purpose-limited capabilities. Generic pattern:
- ordinary support can see workflow metadata needed to diagnose delivery/state problems;
- sensitive evidence is masked or withheld unless a separately authorized support purpose requires it;
- impersonation/view-as-subject features, if ever present, require explicit governance, narrow duration and audit, and cannot silently acquire subject credentials;
- support cannot both manufacture delegation and independently approve the consequence-bearing case without a product-specific separation-of-duties decision;
- privileged legal/security/fraud notes remain separate from user-facing explanation and routine support view.

A screenshot or copied case payload is an uncontrolled disclosure surface. Prefer structured minimum projections over `show support everything`.

## Shared and managed device boundary

Company ownership or supervision of an iPad proves an organizational device relationship, not that every current user is the same person, nor that the organization may read every redress case. Conversely, a personally authenticated user on an organization-managed device may still be subject to actual employer/MDM policy; that product/legal boundary is OPEN.

For a PWA:
1. current server authorization wins over cached role/case state;
2. Service Worker and IndexedDB data are origin storage, not delegation evidence;
3. sign-out/account switch must prevent the next user from receiving the prior user's case projection through app state, history, cache, screenshots or notification previews as far as the platform/product can control;
4. do not assume Shared iPad APFS user separation automatically maps to Safari/Home Screen PWA product semantics without physical validation;
5. a managed-device certificate/device claim may be a risk/context attribute but not sufficient proof of representative authority;
6. unique unsynced flight data remains independently preservable/exportable even if remote case access is withdrawn;
7. queued redress drafts may be preserved locally but consequence-bearing submission must revalidate current actor/delegation/case generation on reconnect.

## Disclosure projection and privacy minimization

Authorization answers `may this actor perform this operation on this object?`; confidentiality additionally asks `what is the minimum representation required?` A case summary can expose fewer fields than an adjudicator view. A representative view can omit internal security/fraud telemetry. A support view can expose delivery state without the case reason. Analytics should receive event classes and quality metrics rather than case payloads or representative graphs unless a separately justified purpose exists.

Do not rely on front-end redaction alone. APIs, exports, logs, error payloads, search endpoints, browser history, notification text, cached HTML/JSON and support tooling are all disclosure surfaces.

## MINTTAP DECISION — generic governance

1. Model subject, actor, relationship/delegation, case/object, capability, purpose, device/session and disclosure projection separately.
2. Enforce authorization server-side for each case/object/operation; UI visibility is not the security boundary.
3. Delegation is narrow, generation/currentness-aware, revocable and auditable; never a global representative super-role by default.
4. Support gets purpose-limited diagnostic views; support identity does not imply subject, delegation or adjudication authority.
5. Managed/company-owned device state may inform risk but does not establish human subject/representative authority.
6. Shared-device/session transitions require leakage testing across cache/history/SW/IndexedDB/notifications and account switching.
7. Revocation stops future authorized access but cannot claim to recall information already legitimately disclosed externally.
8. Preserve unique unsynced local operational data independently from remote redress authorization failure.
9. Keep privileged notes, routine support data, user-facing explanation, representative evidence and analytics as distinct disclosure classes.
10. Actual representative law/policy, employer/MDM rights, product account model, support roles, Safari/Home Screen behavior and managed-iPad configuration remain OPEN.

## VALIDATION — 112-case destructive campaign

1 subject reads own case; 2 unrelated subject denied; 3 sequential ID tamper denied; 4 UUID guess denied; 5 representative valid case read; 6 representative unrelated case denied; 7 representative sibling case denied; 8 representative expired; 9 representative revoked; 10 stale delegation generation denied; 11 submit-only delegate cannot read evidence; 12 read-only delegate cannot submit; 13 explanation reader cannot appeal; 14 appellant cannot adjudicate; 15 support cannot adjudicate; 16 adjudicator cannot silently become representative; 17 device admin cannot read case by device role; 18 MDM enrollment alone denied; 19 device certificate alone denied; 20 old case link denied after revocation; 21 cached case shell contains no newly protected payload; 22 stale API response rejected/hidden after authority refresh; 23 back navigation; 24 browser history; 25 BFCache; 26 Cache Storage; 27 IndexedDB; 28 localStorage/sessionStorage if used; 29 SW stale projection; 30 notification preview; 31 account switch; 32 sign-out; 33 session timeout; 34 second user same browser; 35 second user Shared iPad; 36 temporary session; 37 lost device; 38 remote device revocation; 39 offline representative reads only previously authorized local material per product policy; 40 offline representative cannot mint new authority; 41 reconnect revalidates; 42 queued submit after revocation blocked; 43 queued draft preserved; 44 unique flight data preserved; 45 representative relationship changed concurrently; 46 subject revokes while delegate online; 47 delegate submits during race; 48 server generation arbitration; 49 support search by case ID; 50 support search by email; 51 support cannot enumerate unrelated cases; 52 support export minimized; 53 screenshot policy/UX warning where applicable; 54 privileged note hidden; 55 fraud signal hidden from routine support; 56 legal note hidden; 57 recovery secrets hidden; 58 contact destinations masked; 59 identity documents minimized; 60 error payload does not leak; 61 GraphQL/REST field-level leakage; 62 bulk endpoint leakage; 63 search index leakage; 64 CSV/PDF export leakage; 65 print leakage; 66 analytics payload leakage; 67 crash log leakage; 68 support telemetry leakage; 69 audit log least-content; 70 audit actor/capability trace; 71 delegation creation trace; 72 delegation revocation trace; 73 no secret in trace; 74 representative invited wrong address; 75 invitation intercepted; 76 invitation alone not full authority; 77 representative account takeover; 78 subject account takeover; 79 support impersonation; 80 support account compromise; 81 emergency support access expires; 82 emergency access independently reviewed; 83 delegation expiry; 84 renewal new generation; 85 statutory/guardian authority OPEN; 86 employer authority OPEN; 87 deceased/incapacitated subject OPEN; 88 jurisdiction conflict OPEN; 89 multiple representatives; 90 conflicting representative actions; 91 representative delegates onward denied unless explicitly authorized; 92 cross-tenant organization access; 93 tenant-admin overreach; 94 PITR restores old delegation; 95 current authority floor wins; 96 export/import does not restore revoked delegation; 97 stale native app/PWA view; 98 stale Home Screen app; 99 physical Safari OPEN; 100 Shared iPad physical OPEN; 101 MDM policy OPEN; 102 keyboard role switch; 103 screen-reader announces acting-for context; 104 focus after access denial; 105 zoom/reflow; 106 forced colors; 107 plain-language delegation scope; 108 localization; 109 RTL; 110 human shared-device test OPEN; 111 actual LogMate/MintTap roles OPEN; 112 legal/privacy review OPEN.

## OPEN / DEPENDENCY / CHANGE WATCH

OPEN: actual MintTap/LogMate account/tenant model; representative/delegation rights; employer/airline authority; support/adjudication roles; identity provider; API/schema/field projections; actual company-iPad sharing model; MDM profiles; Safari/Home Screen PWA storage/session behavior; legal retention/disclosure requirements; physical-device and human/AT evidence.

DEPENDENCY: Software Engineering owns implementation architecture and executable authorization/cache/session tests. Its current canonical evidence has generic Chromium PWA offline/restart/update/cold-start transfer, but explicitly leaves Safari/iPadOS/EFB and canonical LogMate runtime OPEN. Design Studio owns reusable role/context interaction patterns; its current web status remains Stage 3 PRACTICE, not production PASS.

CHANGE WATCH: Apple Shared iPad/Managed Apple Account/MDM behavior; Safari/WebKit storage/session/PWA behavior; NIST 800-53/ABAC updates; OWASP authorization guidance; applicable representative/privacy law.

## Adjacent next question

The next high-value boundary is **delegation lifecycle recovery and authority conflict**: how delegation survives or terminates across subject account recovery, representative account recovery, organization/employment change, multiple conflicting delegates, offline queued actions and long-offline managed devices without allowing stale relationship state to resurrect authority.