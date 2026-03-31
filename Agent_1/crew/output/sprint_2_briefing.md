===============================================
  SPRINT 2 BRIEFING — 2026-03-31
  Security + Analytics
===============================================

SPRINT GOAL: Harden tier gating with signed JWTs, add WebSocket resilience, establish FamiliMatch test coverage, and close compliance/analytics gaps across desktop2 and desktop4.
DURATION: 2026-03-31 — 2026-04-03 (estimated 3 days)
PRODUCTS: famililook-desktop2 (2 items), famililook-desktop4 (1 item), famililook-desktop6 (2 items), famililook-desktop7 (2 items — BACKEND)
BACKEND CHANGES: Yes — desktop7 (FM-009, DFMEA-FM-05). CEO permission required.

===============================================
  ITEMS (6)
===============================================

| # | ID           | Title                                                  | Effort | Product  | Priority |
|---|--------------|--------------------------------------------------------|--------|----------|----------|
| 1 | FM-009       | Replace ?tier= URL param with signed JWT (FamiliMatch) | L      | desktop6 + desktop7 | P1 |
| 2 | DFMEA-FM-05  | WebSocket auto-reconnection with room rejoin           | L      | desktop6 + desktop7 | P1 |
| 3 | FM-006       | Write FamiliMatch test suite                           | L      | desktop6 | P2       |
| 4 | DFMEA-FM-16  | Currency disclaimer or live rates                      | S      | desktop2 | P2       |
| 5 | FP-015       | Consolidate two Poker analytics implementations        | M      | desktop4 | P2       |
| 6 | FL-007       | Stripe Price ID startup check + support link           | S      | desktop2 | P1       |

TOTAL EFFORT: 3L + 1M + 2S = ~8-10 dev hours equivalent

===============================================
  FILE SCOPE (expected)
===============================================

desktop2 (FamiliLook / FamiliUno):
  - src/components/keepsakes/utils/printProfiles.js  (DFMEA-FM-16 — currency formatting)
  - src/pages/PlansPage.jsx                          (FL-007 — Stripe check + support link)

desktop4 (FamiliPoker):
  - src/analytics.js                                 (FP-015 — consolidation target)
  - src/utils/analytics.js                           (FP-015 — consolidation source)

desktop6 (FamiliMatch — frontend):
  - src/pages/LandingPage.jsx                        (FM-009 — JWT consumption on frontend side)
  - tests/                                           (FM-006 — new test suite)

desktop7 (FamiliMatch — backend) — REQUIRES CEO PERMISSION:
  - JWT signing endpoint                             (FM-009)
  - WebSocket reconnection + room rejoin handler     (DFMEA-FM-05)

===============================================
  PRE-SPRINT CHECKLIST
===============================================

  [x] Working set updated — .claude/working_set.txt (frontend files only)
  [x] Change log exists — .claude/change_log.md
  [x] Pre-commit hook installed — .git/hooks/pre-commit
  [x] Rollback strategy — git revert per-commit
  [ ] CEO permission — NEEDED for desktop7 backend files (FM-009, DFMEA-FM-05)
  [ ] desktop7 file inventory — Pending CEO approval before scoping backend files

===============================================
  DEPENDENCIES
===============================================

  - FM-009 spans desktop6 (frontend) AND desktop7 (backend):
    Backend must issue signed JWT before frontend can consume it.
    Frontend work (LandingPage.jsx) can be scaffolded but NOT tested until backend is ready.

  - DFMEA-FM-05 spans desktop6 (frontend) AND desktop7 (backend):
    Backend must support room rejoin protocol before frontend reconnection logic works.
    Same dependency pattern as FM-009.

  - FM-006 (test suite) is independent — can start immediately.

  - DFMEA-FM-16 and FL-007 are independent desktop2 items — no cross-product deps.

  - FP-015 is independent desktop4 work — no cross-product deps.

RECOMMENDED EXECUTION ORDER:
  1. FM-006 (desktop6 tests — independent, no blockers, L effort — start early)
  2. DFMEA-FM-16 (desktop2, S effort — quick win)
  3. FL-007 (desktop2, S effort — quick win)
  4. FP-015 (desktop4, M effort — independent)
  5. FM-009 (desktop6+7 — blocked on CEO permission for backend)
  6. DFMEA-FM-05 (desktop6+7 — blocked on CEO permission for backend)

===============================================
  CEO DECISIONS NEEDED
===============================================

  1. BACKEND PERMISSION — desktop7 (famililook-desktop7)
     Items FM-009 and DFMEA-FM-05 require backend changes.
     Per CLAUDE.md guardrails, backend files cannot be modified without explicit CEO permission.
     These two items are BLOCKED until permission is granted.

  2. JWT SIGNING STRATEGY (FM-009)
     Decision: What signing method? Options:
       a) Symmetric HMAC (HS256) — simpler, shared secret between desktop6 and desktop7
       b) Asymmetric RSA (RS256) — more secure, public key on frontend
     Recommendation: HS256 for internal service-to-service (both deployed on same infra).

===============================================
  RISKS
===============================================

  1. FM-009 (JWT tier gating) — HIGH
     Risk: Security-critical change. If JWT validation is bypassed or misconfigured,
       users could access Plus features without payment.
     Mitigation: Backend-authoritative validation. Frontend JWT is read-only.
       Test with tampered tokens. Add expiry checks.

  2. DFMEA-FM-05 (WebSocket reconnection) — MEDIUM
     Risk: Reconnection logic could cause duplicate room joins or state desync
       if the server-side room state is not idempotent.
     Mitigation: Server must treat rejoin as idempotent (same socket_id = same participant).
       Add reconnection backoff (exponential) to prevent thundering herd.

  3. FM-006 (test suite) — LOW
     Risk: Tests may be written against current behavior that has bugs,
       locking in incorrect behavior.
     Mitigation: Review test assertions against compare_faces.v1 contract spec.
       Tests must validate contract compliance, not just snapshot current output.

  4. FP-015 (analytics consolidation) — LOW
     Risk: Consolidating two files could break event tracking if one file
       has different event names or parameter shapes.
     Mitigation: Inventory all events in both files before consolidating.
       Verify event names match analytics dashboard expectations.

  5. DFMEA-FM-16 (currency disclaimer) — LOW
     Risk: Minimal. Adding a disclaimer is additive UI.
     Mitigation: Visual verification only.

  6. FL-007 (Stripe Price ID check) — LOW
     Risk: Startup check could block app load if Stripe is unreachable.
     Mitigation: Check must be non-blocking (log warning + show support link, do not crash).

===============================================
  KPI IMPACT
===============================================

  | Item          | KPI                      | Expected Impact                                    |
  |---------------|--------------------------|---------------------------------------------------|
  | FM-009        | Security / Revenue       | Closes tier bypass vulnerability — protects Plus revenue |
  | DFMEA-FM-05   | User Retention (Match)   | Prevents dropped sessions — reduces bounce from WS failures |
  | FM-006        | Quality / CI             | Establishes regression safety net for FamiliMatch  |
  | DFMEA-FM-16   | Compliance               | Currency transparency — consumer protection compliance |
  | FP-015        | Analytics Accuracy       | Single source of truth for Poker events — cleaner data |
  | FL-007        | Support / UX             | Early Stripe misconfiguration detection — faster resolution |

===============================================
  HANDOFF
===============================================

  TO: change_manager
  TASK: Set up governance for Sprint 2 — update working_set.txt, validate scope,
        classify risk tier, create change request package.
  ARTIFACTS: This briefing (crew/output/sprint_2_briefing.md)
  CONTEXT: 6 items, 4 products, 2 require backend permission, P1 risk tier.

===============================================
