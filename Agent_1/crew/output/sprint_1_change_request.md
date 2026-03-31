═══════════════════════════════════════════════
  CHANGE REQUEST — CR-0007
  Sprint 1: Revenue + Critical UX
═══════════════════════════════════════════════

RISK TIER: P2 — Standard
  Rationale: Multi-file (5 files), multi-product (desktop2 + desktop6),
  but NO backend changes, NO contract changes (kinship_analyze.v1 and
  compare_faces.v1 untouched), NO new dependencies, NO pricing changes.
  All changes are frontend-only within existing patterns.

CHANGE TYPE: Code (Frontend only)
SOURCE: Sprint 1 backlog — prioritised by CPO from platform audit findings
DATE: 2026-03-31
PHASE: 2 of 6 (Scope Lock & Change Request)

═══════════════════════════════════════════════
  SCOPE — 5 FILES ACROSS 2 REPOS
═══════════════════════════════════════════════

WORKING SET (updated in .claude/working_set.txt):

  Desktop2 (FamiliLook / FamiliUno):
  1. famililook-desktop2/src/pages/FamiliUnoPage.jsx
  2. famililook-desktop2/src/layout/UploadSection.jsx
  3. famililook-desktop2/src/pages/HomePage.jsx

  Desktop6 (FamiliMatch):
  4. famililook-desktop6/src/pages/SoloPage.jsx
  5. famililook-desktop6/src/pages/LandingPage.jsx

═══════════════════════════════════════════════
  TASK BREAKDOWN
═══════════════════════════════════════════════

TASK 1 — FL-024: Add BasketDrawer + BasketBadge to FamiliUno
  File: famililook-desktop2/src/pages/FamiliUnoPage.jsx
  Description: Wire up basket UI components (BasketDrawer, BasketBadge)
    so users can add FamiliUno decks to basket and proceed to checkout.
  Context: Revenue-critical. FamiliUno deck ordering is LIVE via
    QPMarkets but the basket UX on the Uno page is missing/incomplete.
  Impact: Revenue enablement — direct path to conversion.
  Contract impact: None (no backend API changes).

TASK 2 — FL-002: Add helper message for single-parent upload
  File: famililook-desktop2/src/layout/UploadSection.jsx
  Description: Show a contextual helper message when user uploads only
    one parent photo, guiding them to upload the second parent.
  Context: Upload conversion is at 0% (9 visitors, 14 CTAs, 0 uploads).
    This is a UX friction fix to reduce user confusion at the upload step.
  Impact: Conversion improvement — addresses known 0% upload funnel drop.
  Contract impact: None (frontend-only UX change).

TASK 3 — FL-009: Fix buildDeck useEffect groupSnapshot
  File: famililook-desktop2/src/pages/FamiliUnoPage.jsx
  Description: Fix the buildDeck useEffect to correctly handle
    groupSnapshot data, preventing stale or missing deck builds.
  Context: Bug fix — deck generation may fail or produce incorrect
    results when groupSnapshot changes.
  Impact: Functional correctness for FamiliUno deck feature.
  Contract impact: None.

TASK 4 — GAP-02: Fix pointer-events on particles + CTA audit
  File: famililook-desktop2/src/pages/HomePage.jsx
  Description: Fix particle animation layer blocking pointer-events
    on CTAs. Audit all CTA buttons for correct click handling.
  Context: Homepage CTAs may be unclickable due to particle overlay
    z-index/pointer-events issue. Directly blocks conversion.
  Impact: Critical UX — users cannot click CTAs if particles intercept.
  Contract impact: None.

TASK 5 — GAP-01: Add error UI to SoloPage
  File: famililook-desktop6/src/pages/SoloPage.jsx
  Description: Add proper error state UI when face comparison fails
    (network error, no face detected, etc.).
  Context: Currently errors may fail silently or show raw error text.
    Users have no actionable feedback on failure.
  Impact: UX quality — error handling is a baseline expectation.
  Contract impact: None (consumes existing error responses).

TASK 6 — FM-012: Fix consent bypass on ?mode= auto-navigation
  File: famililook-desktop6/src/pages/LandingPage.jsx
  Description: Fix auto-navigation triggered by ?mode= query parameter
    that bypasses the consent flow (GDPR compliance issue).
  Context: When users arrive at LandingPage with ?mode=solo (or duo/group),
    the page auto-navigates before consent can be collected.
  Impact: Compliance — GDPR consent must be obtained before processing.
  Contract impact: None.

═══════════════════════════════════════════════
  VALIDATION CHECKLIST
═══════════════════════════════════════════════

  [PASS] Traceability:
    FL-024, FL-002, FL-009 — platform audit backlog items
    GAP-01, GAP-02 — gap analysis findings
    FM-012 — FamiliMatch compliance finding

  [PASS] Scope validation (all 5 files):
    famililook-desktop2/src/pages/FamiliUnoPage.jsx    — ALLOWED
    famililook-desktop2/src/layout/UploadSection.jsx   — ALLOWED
    famililook-desktop2/src/pages/HomePage.jsx         — ALLOWED
    famililook-desktop6/src/pages/SoloPage.jsx         — ALLOWED
    famililook-desktop6/src/pages/LandingPage.jsx      — ALLOWED

  [PASS] Contract impact: NONE
    kinship_analyze.v1 — not touched
    compare_faces.v1   — not touched

  [PASS] Backend impact: NONE
    No .py files modified. No desktop3/5/7 changes.

  [PASS] Working set: Updated (.claude/working_set.txt)

  [PASS] Blast radius:
    5 files across 2 repos (desktop2: 3 files, desktop6: 2 files)
    Cross-repo: Yes (desktop2 + desktop6), but repos are independent
    No shared state between the two repos

  [PENDING] Tests: To be run after implementation (Phase 4)
    Desktop2: npm run test:run (836 Vitest tests)
    Desktop6: npm run test:run (98 Vitest tests)
    Both: npm run build (must succeed)

  [PENDING] ops_report: Will be generated after implementation

  [PASS] Rollback plan:
    All changes are additive frontend-only edits.
    Rollback: git revert the merge commit on production branch.
    No data migrations, no schema changes, no state to clean up.

═══════════════════════════════════════════════
  RISK ASSESSMENT
═══════════════════════════════════════════════

  RISK 1: Tasks 1+3 both target FamiliUnoPage.jsx
    Mitigation: Assign to same implementer. Non-overlapping code regions
    (Task 1 = basket components, Task 3 = useEffect hook). Low conflict risk.

  RISK 2: Task 6 (consent bypass) is compliance-adjacent
    Mitigation: Change is a FIX to restore correct consent flow, not a
    removal or weakening. GDPR-positive change. No escalation needed.

  RISK 3: Task 4 (pointer-events) could affect visual layout
    Mitigation: CSS-only change (pointer-events: none on particle layer).
    Manual visual verification required after implementation.

═══════════════════════════════════════════════
  APPROVAL & NEXT STEPS
═══════════════════════════════════════════════

  RECOMMENDATION: APPROVE
    All changes are P2 (standard), frontend-only, within existing patterns,
    and address documented revenue/UX/compliance gaps.

  CONDITIONS:
    1. All tests must pass after implementation (Phase 4 gate)
    2. Manual verification of consent flow after FM-012 fix
    3. Manual verification of CTA clickability after GAP-02 fix
    4. No deployment until Phase 5 (QA verification) completes

  NEXT PHASES:
    Phase 3 — FE Lead implementation (delegated code changes)
    Phase 4 — QA Lead verification (tests + manual checks)
    Phase 5 — Change Manager release gate
    Phase 6 — Deploy (merge main -> production, push)

═══════════════════════════════════════════════
  CHANGE REGISTER ENTRIES
═══════════════════════════════════════════════

| Timestamp | Repo | Type | Description | Ref | Tier | Approved | Status |
|-----------|------|------|-------------|-----|------|----------|--------|
| 2026-03-31 | desktop2 | Code | BasketDrawer+BasketBadge on FamiliUno | FL-024 | P2 | Pending CEO | Scoped |
| 2026-03-31 | desktop2 | Code | Single-parent upload helper message | FL-002 | P2 | Pending CEO | Scoped |
| 2026-03-31 | desktop2 | Code | Fix buildDeck useEffect groupSnapshot | FL-009 | P2 | Pending CEO | Scoped |
| 2026-03-31 | desktop2 | Code | Fix pointer-events on particles + CTA audit | GAP-02 | P2 | Pending CEO | Scoped |
| 2026-03-31 | desktop6 | Code | Add error UI to SoloPage | GAP-01 | P2 | Pending CEO | Scoped |
| 2026-03-31 | desktop6 | Code | Fix consent bypass on ?mode= auto-nav | FM-012 | P2 | Pending CEO | Scoped |

═══════════════════════════════════════════════
  Change Manager: Change & Release Manager
  CR ID: CR-0007
  Date: 2026-03-31
═══════════════════════════════════════════════
