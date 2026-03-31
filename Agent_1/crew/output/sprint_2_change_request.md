===============================================
  CHANGE REQUEST — CR-0008
  Sprint 2: Security + Analytics
===============================================

RISK TIER: P1 — Elevated
  Rationale: Includes backend changes (desktop7), security-sensitive tier
  gating (JWT replacing URL param), WebSocket protocol changes, and spans
  4 products (desktop2, desktop4, desktop6, desktop7). Backend items are
  BLOCKED pending CEO permission.

CHANGE TYPE: Code (Frontend + Backend)
SOURCE: Sprint 2 backlog — Security hardening, test coverage, analytics hygiene
DATE: 2026-03-31
PHASE: 2 of 6 (Scope Lock & Change Request)

===============================================
  SCOPE — 6 FRONTEND FILES + BACKEND (PENDING)
===============================================

WORKING SET (updated in .claude/working_set.txt):

  Desktop2 (FamiliLook / FamiliUno):
  1. famililook-desktop2/src/components/keepsakes/utils/printProfiles.js  (DFMEA-FM-16)
  2. famililook-desktop2/src/pages/PlansPage.jsx                          (FL-007)

  Desktop4 (FamiliPoker):
  3. famililook-desktop4/src/analytics.js                                 (FP-015)
  4. famililook-desktop4/src/utils/analytics.js                           (FP-015)

  Desktop6 (FamiliMatch — frontend only):
  5. famililook-desktop6/src/pages/LandingPage.jsx                        (FM-009 frontend)
  6. famililook-desktop6/tests/                                           (FM-006)

  Desktop7 (FamiliMatch — backend) — NOT IN WORKING SET:
  - Requires CEO permission before files can be scoped
  - Affects: FM-009 (JWT signing), DFMEA-FM-05 (WS reconnection)

===============================================
  SCOPE VALIDATION RESULTS
===============================================

  famililook-desktop6/src/pages/LandingPage.jsx              — [ALLOWED] exit 0
  famililook-desktop6/tests/                                 — [ALLOWED] exit 0
  famililook-desktop2/src/components/keepsakes/utils/printProfiles.js — [ALLOWED] exit 0
  famililook-desktop2/src/pages/PlansPage.jsx                — [ALLOWED] exit 0
  famililook-desktop4/src/analytics.js                       — [ALLOWED] exit 0
  famililook-desktop4/src/utils/analytics.js                 — [ALLOWED] exit 0

  Backend (desktop7): NOT VALIDATED — blocked pending CEO permission.

===============================================
  TASK BREAKDOWN
===============================================

TASK 1 — FM-009: Replace ?tier= URL param with signed JWT
  Files: famililook-desktop6/src/pages/LandingPage.jsx (frontend)
         + desktop7 backend (BLOCKED)
  Description: Currently tier gating in FamiliMatch uses a ?tier= URL
    parameter which can be trivially spoofed. Replace with a signed JWT
    issued by the backend after Stripe checkout or plan verification.
    Frontend reads JWT from cookie/header, backend validates on every
    protected endpoint.
  Context: Security vulnerability — users can bypass Plus tier gating
    by manually setting ?tier=plus in the URL.
  Impact: Revenue protection — closes tier bypass attack vector.
  Contract impact: None (compare_faces.v1 response unchanged).
  Backend dependency: YES — JWT issuance endpoint must exist first.

TASK 2 — DFMEA-FM-05: WebSocket auto-reconnection with room rejoin
  Files: desktop6 frontend (exact file TBD) + desktop7 backend (BLOCKED)
  Description: When WebSocket connection drops (network blip, server restart),
    the client should automatically reconnect and rejoin its current room
    without user intervention. Currently a drop = session lost.
  Context: DFMEA finding — single point of failure for multiplayer Match sessions.
  Impact: Session resilience — prevents user frustration on flaky connections.
  Contract impact: None (transport layer, not API response schema).
  Backend dependency: YES — server must support idempotent room rejoin.

TASK 3 — FM-006: Write FamiliMatch test suite
  Files: famililook-desktop6/tests/ (new test files)
  Description: Establish baseline test coverage for FamiliMatch.
    Cover: LandingPage consent flow, SoloPage face upload + result display,
    tier gating logic, match history hook, compare_faces.v1 contract compliance.
  Context: FamiliMatch currently has minimal test coverage compared to
    desktop2 (836 tests). This is a quality and CI gap.
  Impact: Regression safety — enables confident future changes.
  Contract impact: Tests VALIDATE the contract, they do not change it.

TASK 4 — DFMEA-FM-16: Currency disclaimer or live rates
  File: famililook-desktop2/src/components/keepsakes/utils/printProfiles.js
  Description: Add a disclaimer noting that displayed prices are in GBP
    and may differ at checkout due to currency conversion, OR integrate
    a live rate display. Disclaimer is the S-effort path.
  Context: DFMEA finding — users in non-GBP regions see GBP prices with
    no indication that their charge may differ.
  Impact: Consumer protection compliance — price transparency.
  Contract impact: None (frontend display only).

TASK 5 — FP-015: Consolidate two Poker analytics implementations
  Files: famililook-desktop4/src/analytics.js
         famililook-desktop4/src/utils/analytics.js
  Description: Desktop4 has two analytics files with overlapping but
    inconsistent implementations. Consolidate into a single authoritative
    module. Preserve all tracked events. Update all import paths.
  Context: Dual implementations risk double-counting or missed events.
    Analytics data quality issue.
  Impact: Data accuracy — single source of truth for Poker analytics.
  Contract impact: None (analytics layer, not API).

TASK 6 — FL-007: Stripe Price ID startup check + support link
  File: famililook-desktop2/src/pages/PlansPage.jsx
  Description: On PlansPage mount, verify that configured Stripe Price IDs
    are valid/reachable. If validation fails, show a user-friendly message
    with a support contact link instead of a broken checkout button.
  Context: If Price IDs become stale (product changes in Stripe dashboard),
    checkout silently fails. Early detection + support link improves UX.
  Impact: Support reduction — users get actionable help instead of silent failure.
  Contract impact: None (frontend validation only).

===============================================
  VALIDATION CHECKLIST
===============================================

  [PASS] Traceability:
    FM-009   — FamiliMatch security backlog
    DFMEA-FM-05 — DFMEA finding (WebSocket resilience)
    FM-006   — FamiliMatch quality gap
    DFMEA-FM-16 — DFMEA finding (currency transparency)
    FP-015   — FamiliPoker analytics hygiene
    FL-007   — FamiliLook operational resilience

  [PASS] Scope validation: All 6 frontend files — ALLOWED (exit 0)

  [PASS] Contract impact: NONE
    kinship_analyze.v1 — not touched
    compare_faces.v1   — not touched (FM-006 tests validate it, do not change it)

  [BLOCKED] Backend impact: desktop7 changes for FM-009 + DFMEA-FM-05
    Status: AWAITING CEO PERMISSION
    No .py files are in the working set until permission is granted.

  [PASS] Working set: Updated (.claude/working_set.txt — 6 frontend files)

  [PASS] Blast radius:
    6 frontend files across 3 repos (desktop2: 2, desktop4: 2, desktop6: 2)
    + 2 backend items in desktop7 (BLOCKED)
    Cross-repo: Yes (desktop2 + desktop4 + desktop6), but repos are independent
    No shared state between repos

  [PENDING] Tests: To be run after implementation (Phase 4)
    Desktop2: npm run test:run + npm run build
    Desktop4: npm run test:run + npm run build
    Desktop6: npm run test:run + npm run build

  [PENDING] ops_report: Will be generated after implementation

  [PASS] Rollback plan:
    Frontend changes: git revert per-commit on production branch.
    Backend changes (if approved): git revert + redeploy desktop7.
    No data migrations, no schema changes.
    JWT rollback: revert to ?tier= param temporarily if JWT has issues.

===============================================
  RISK ASSESSMENT
===============================================

  RISK 1: FM-009 (JWT) — HIGH
    Security-critical. Incorrect implementation could either:
    a) Lock out legitimate Plus users (false negative), or
    b) Allow free users to access Plus features (false positive).
    Mitigation: Backend-authoritative validation. Frontend only reads JWT.
    Test with expired, tampered, and missing tokens. Require backend
    review before deploy.

  RISK 2: DFMEA-FM-05 (WebSocket reconnection) — MEDIUM
    Reconnection storms could overload backend if many clients reconnect
    simultaneously (e.g., after server restart).
    Mitigation: Exponential backoff with jitter. Server-side rate limiting
    on rejoin. Idempotent room state (rejoin = no-op if already in room).

  RISK 3: FP-015 (analytics consolidation) — MEDIUM
    Removing one analytics file and updating imports could break event
    tracking if any import path is missed.
    Mitigation: grep all imports before consolidating. Run build to catch
    broken imports. Verify events fire in dev mode after change.

  RISK 4: FM-006 (test suite) — LOW
    No production risk. Tests are additive.
    Only risk: tests codifying incorrect behavior.
    Mitigation: Validate assertions against compare_faces.v1 contract spec.

  RISK 5: DFMEA-FM-16 (currency disclaimer) — LOW
    Additive UI text. No logic change.
    Mitigation: Visual verification only.

  RISK 6: FL-007 (Stripe check) — LOW
    Must be non-blocking. If check crashes or hangs, PlansPage becomes
    unusable.
    Mitigation: Wrap in try/catch with timeout. Fallback = render normally
    without validation status. Support link always visible.

===============================================
  APPROVAL & NEXT STEPS
===============================================

  RECOMMENDATION: APPROVE (frontend items) / ESCALATE (backend items)

  Frontend items (4 tasks, 6 files): Ready for implementation.
    DFMEA-FM-16, FL-007, FP-015, FM-006 — no blockers.

  Backend items (2 tasks): BLOCKED on CEO permission.
    FM-009 frontend scaffolding can proceed, but cannot be tested end-to-end.
    DFMEA-FM-05 frontend work should NOT begin until backend protocol is defined.

  CONDITIONS:
    1. CEO must grant desktop7 backend permission before FM-009 / DFMEA-FM-05 proceed
    2. All tests must pass after implementation (Phase 4 gate)
    3. FM-009 requires security review before deploy (JWT validation correctness)
    4. FP-015 requires import audit before file deletion
    5. No deployment until Phase 5 (QA verification) completes

  NEXT PHASES:
    Phase 3 — FE Lead implementation (frontend items only)
    Phase 3b — Backend implementation (after CEO approval)
    Phase 4 — QA Lead verification (tests + manual checks)
    Phase 5 — Change Manager release gate
    Phase 6 — Deploy (merge main -> production, push per repo)

===============================================
  CHANGE REGISTER ENTRIES
===============================================

| Timestamp  | Repo     | Type | Description                                | Ref          | Tier | Approved    | Status  |
|------------|----------|------|--------------------------------------------|--------------|------|-------------|---------|
| 2026-03-31 | desktop6 | Code | Replace ?tier= with signed JWT (frontend)  | FM-009       | P1   | Pending CEO | Scoped  |
| 2026-03-31 | desktop7 | Code | JWT signing endpoint (backend)             | FM-009       | P1   | BLOCKED     | Blocked |
| 2026-03-31 | desktop6 | Code | WebSocket reconnection (frontend)          | DFMEA-FM-05  | P1   | Pending CEO | Blocked |
| 2026-03-31 | desktop7 | Code | WS room rejoin handler (backend)           | DFMEA-FM-05  | P1   | BLOCKED     | Blocked |
| 2026-03-31 | desktop6 | Test | FamiliMatch test suite                     | FM-006       | P2   | Pending CEO | Scoped  |
| 2026-03-31 | desktop2 | Code | Currency disclaimer on printProfiles       | DFMEA-FM-16  | P2   | Pending CEO | Scoped  |
| 2026-03-31 | desktop4 | Code | Consolidate analytics implementations      | FP-015       | P2   | Pending CEO | Scoped  |
| 2026-03-31 | desktop2 | Code | Stripe Price ID check + support link       | FL-007       | P2   | Pending CEO | Scoped  |

===============================================
  Change Manager: Change & Release Manager
  CR ID: CR-0008
  Date: 2026-03-31
===============================================
