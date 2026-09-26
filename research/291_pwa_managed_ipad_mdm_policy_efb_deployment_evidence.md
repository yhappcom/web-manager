# 291 — Managed-iPad / MDM Policy Boundary & EFB Deployment Evidence Contract

Status: **PASS (generic) / REPRESENTATIVE MANAGED-IPAD + PRODUCT EXECUTION OPEN**  
Date: 2026-09-27  
Primary owner: **Track E — Web Architecture, Security & Operations**  
Dependencies: 289–290; Track A browser/platform mechanics; Track C evidence promotion.

## Purpose
Separate generic WebKit/PWA capability from what a representative company-managed iPad actually permits, routes, trusts and can recover. The central rule is: **browser support is not managed-fleet operational authority.**

## SOURCE
- Apple Platform Deployment — Web Clips device-management payload: https://support.apple.com/guide/deployment/depbc7c7808/web
- Apple Platform Deployment — Global HTTP Proxy payload: https://support.apple.com/guide/deployment/dep7ba46fcd/web
- Apple Platform Deployment — content filtering: https://support.apple.com/guide/deployment/dep1129ff8d2/web
- Apple deployment guidance remains OS/enrollment/MDM-version-specific CHANGE WATCH.
- 290 owns D/L/S/U physical-iPad evidence dimensions.

## Five-track allocation
- **A:** consumes MDM/network constraints to bound actual Safari/Home Screen/WebKit behavior; does not infer policy from browser capability.
- **B:** consumes launch/restriction/recovery outcomes for truthful install/offline/recovery UX.
- **C:** owns representative-device evidence promotion and regression/failure campaign.
- **D:** may observe managed-fleet outcomes but telemetry cannot prove policy configuration or authority.
- **E:** owns management-policy, network/trust, deployment/update and operational-recovery contract.

## Why a separate management envelope is required
A PWA may be standards-conformant and work on an unmanaged physical iPad while failing or behaving differently on the company fleet because enrollment, supervision, Safari restrictions, content filtering, proxy/PAC/VPN/DNS, trust anchors, certificate deployment, launch mode or update policy differ.

Apple documents that managed Web Clips can be placed on the Home Screen and that Safari management/restriction affects Web Clip behavior. Apple also documents Global HTTP Proxy for enrolled devices and multiple content-filtering mechanisms. These are management controls, not WebKit capability guarantees.

## M0–M8 representative managed-device envelope
Record independently:
- **M0 Enrollment/supervision:** enrollment method, supervision state, Shared-iPad status where applicable, relevant management authority.
- **M1 Launch/deployment:** Safari tab, user-added Home Screen web app, managed Web Clip, full-screen setting, removability and actual launch result.
- **M2 Web restrictions:** Safari allowed/hidden/restricted state, website allow/block/content-filter policy and relevant app/web restrictions.
- **M3 Network-policy path:** Wi-Fi/cellular/hotspot as applicable; Global HTTP Proxy/PAC, VPN, DNS/filter path and policy version.
- **M4 Trust context:** relevant certificate/root deployment mechanism, TLS interception policy where applicable, certificate validity/trust outcome.
- **M5 Destination reachability:** test shell/static assets, Service Worker/update resources, API, authentication/session endpoints and sync destinations separately.
- **M6 Update/policy lifecycle:** iPadOS/WebKit/browser/MDM profile update policy, policy generation and transition evidence.
- **M7 Data/recovery envelope:** reference 290 D/L/S/U class, unique-local-data integrity, persistence/storage condition and destructive-recovery boundaries.
- **M8 Operations/support:** recovery ownership, profile redeployment path, lost/stolen/replaced-device handling, evidence capture and normalization.

## Evidence promotion
Representative company-iPad claims require a current **T4 + M0–M8** envelope appropriate to the claim. Generic Apple documentation, simulator/desktop Safari, unmanaged iPad and a different MDM profile are prerequisite or transfer evidence, not representative managed-fleet PASS.

A material MDM/network/trust/policy change expires only evidence dependent on the changed control. Revalidate affected claims; do not erase unrelated evidence without cause.

## Persistent guards
- `browser supports X ≠ managed fleet permits/routes/trusts X`;
- `unmanaged physical-iPad PASS ≠ managed-fleet PASS`;
- `Home Screen icon present ≠ launch permitted`;
- `user-added web app ≠ managed Web Clip`;
- `shell reachable ≠ Service Worker/API/auth/sync reachable`;
- `certificate installed ≠ equivalent TLS trust context`;
- `proxy configured ≠ every required destination reachable`;
- `MDM can redeploy configuration ≠ unique local application data recoverable`;
- `telemetry observed success ≠ management policy proven`;
- `old T4 PASS ≠ current T4 PASS after material policy drift`.

## EFB / LogMate transfer
For a company-iPad PWA expected to work offline, M0–M8 becomes part of the deployment evidence contract. Do not assume App Store absence implies unrestricted Home Screen deployment, that managed Web Clips are equivalent to installed PWAs, or that hotspot/direct device-to-device/background behavior follows from ordinary Safari networking. Verify each separately.

Actual company MDM/ADE vendor, profile, network topology, certificate policy, support process, offline-support duration and physical fleet remain **OPEN**.

## Track C destructive additions — defined, not executed
1081. **Unmanaged→managed promotion:** unmanaged physical PASS promoted to managed fleet.  
1082. **Web-Clip equivalence:** managed Web Clip treated as equivalent to user-added Home Screen web app.  
1083. **Installed→launchable fallacy:** icon/profile presence treated as successful permitted launch.  
1084. **Shell-reachability composition:** shell success promoted to API/auth/sync/SW-update reachability.  
1085. **Network-policy omission:** proxy/PAC/VPN/DNS/filter path absent from evidence.  
1086. **Trust-context omission:** certificate deployment/trust context omitted from TLS-dependent PASS.  
1087. **Policy-drift stale evidence:** pre-change PASS reused after a material management-policy transition.  
1088. **Telemetry-as-policy oracle:** observed fleet telemetry treated as proof of configured policy/authority.

All are **DEFINED / NOT EXECUTED**.

## MINTTAP DECISION / DIRECTION
Use M0–M8 alongside 290 D/L/S/U for representative managed-iPad evidence. Keep actual product/fleet facts OPEN. Next: authentication/session continuity and offline-rejoin authority under managed-device constraints.
