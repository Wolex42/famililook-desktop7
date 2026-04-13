═══════════════════════════════════════════════
  SPRINT 1 BRIEFING — 2026-03-31
  Revenue + Critical UX
═══════════════════════════════════════════════

SPRINT GOAL: Unblock checkout revenue on /uno, fix upload conversion blockers, and close compliance + UX gaps in FamiliMatch.
DURATION: 2026-03-31 — 2026-04-02 (estimated 2 days)
PRODUCTS: famililook-desktop2 (4 items), famililook-desktop6 (2 items)
BACKEND CHANGES: None required

═══════════════════════════════════════════════
  ITEMS (6)
═══════════════════════════════════════════════

| # | ID     | Title                                                              | Effort | Product  | Priority |
|---|--------|--------------------------------------------------------------------|--------|----------|----------|
| 1 | FL-024 | Add BasketDrawer + BasketBadge to FamiliUnoPage (Option A — local) | M      | desktop2 | P0       |
| 2 | FL-002 | Helper message "Add [Parent B] to enable analysis"                 | S      | desktop2 | P1       |
| 3 | GAP-01 | Add error UI to FamiliMatch SoloPage                               | S      | desktop6 | P1       |
| 4 | FM-012 | Fix consent bypass via ?mode= auto-nav in LandingPage             | S      | desktop6 | P0       |
| 5 | FL-009 | buildDeck useEffect must watch groupSnapshot in FamiliUnoPage      | S      | desktop2 | P1       |
| 6 | GAP-02 | pointer-events:none on particles + CTA touch target audit          | S      | desktop2 | P1       |

TOTAL EFFORT: 1M + 5S = ~3-4 dev hours equivalent

═══════════════════════════════════════════════
  FILE SCOPE (expected)
═══════════════════════════════════════════════

desktop2:
  - src/pages/FamiliUnoPage.jsx          (FL-024, FL-009)
  - src/components/keepsakes/BasketDrawer.jsx  (FL-024 — import, no modification)
  - src/components/keepsakes/BasketBadge.jsx   (FL-024 — import, no modification)
  - src/layout/UploadSection.jsx         (FL-002 — or relevant upload panel)
  - src/pages/HomePage.jsx               (GAP-02)

desktop6:
  - src/pages/SoloPage.jsx               (GAP-01)
  - src/pages/LandingPage.jsx            (FM-012)

═══════════════════════════════════════════════
  PRE-SPRINT CHECKLIST
═══════════════════════════════════════════════

  [x] Dist backup for desktop6 — completed in Sprint 0A (dist_backup_20260331/)
  [x] Backend permission — NOT NEEDED (pure frontend sprint)
  [x] Change log exists — desktop2/.claude/change_log.md VERIFIED
  [x] Change log exists — desktop6/.claude/change_log.md VERIFIED
  [x] Pre-commit hook installed — .git/hooks/pre-commit VERIFIED
  [x] Rollback strategy — git revert per-commit
  [ ] Working set — NEEDS UPDATE (currently contains docs/PLATFORM_ARCHITECTURE.md from prior work)

═══════════════════════════════════════════════
  DEPENDENCIES
═══════════════════════════════════════════════

  - FL-024 and FL-009 both touch FamiliUnoPage.jsx — implement in sequence, not parallel.
    Recommended order: FL-009 first (smaller, fixes existing bug), then FL-024 (adds new UI).
  - No cross-product dependencies.
  - No backend dependencies.
  - All desktop6 items are independent of desktop2 items.

RECOMMENDED EXECUTION ORDER:
  1. FM-012 (P0 compliance — smallest risk, highest urgency)
  2. GAP-01 (desktop6, independent — batch with FM-012)
  3. FL-009 (desktop2, FamiliUnoPage prep)
  4. FL-024 (desktop2, FamiliUnoPage — builds on clean state after FL-009)
  5. FL-002 (desktop2, upload flow — independent)
  6. GAP-02 (desktop2, HomePage — independent, lowest risk)

═══════════════════════════════════════════════
  CEO DECISIONS NEEDED
═══════════════════════════════════════════════

  None. All items are pre-approved. No backend changes. No breaking changes.
  No budget implications (zero vendor cost — pure code changes).

═══════════════════════════════════════════════
  RISKS
═══════════════════════════════════════════════

  1. FL-024 (BasketDrawer on /uno) — MEDIUM
     Risk: BasketDrawer may have implicit dependencies on AppLayout context or keepsakes state.
     Mitigation: Option A renders locally — verify BasketContext/provider is available or wrap.

  2. FM-012 (consent bypass) — LOW
     Risk: Fix could break legitimate deep-linking to ?mode=solo|duo|group.
     Mitigation: Consent check must gate navigation, not remove deep-link capability.
     Users with consent already granted should still auto-navigate.

  3. GAP-02 (particle pointer-events) — LOW
     Risk: pointer-events:none on wrong layer could disable legitimate interactions.
     Mitigation: Target only the particle container div, not parent layout.

  4. FL-009 (groupSnapshot dependency) — LOW
     Risk: Adding dependency could cause excessive re-renders.
     Mitigation: Verify groupSnapshot reference stability; use appropriate memo if needed.

═══════════════════════════════════════════════
  KPI IMPACT
═══════════════════════════════════════════════

  | Item   | KPI                    | Expected Impact                              |
  |--------|------------------------|----------------------------------------------|
  | FL-024 | Monthly Revenue        | Unblocks /uno checkout — direct revenue path  |
  | FL-002 | Upload Conversion      | Reduces 0% upload drop-off                   |
  | GAP-01 | User Retention (Match) | Prevents silent failures → reduces bounce     |
  | FM-012 | Compliance (BIPA/GDPR) | Closes P0 consent gap — legal exposure        |
  | FL-009 | Feature Completeness   | Fixes group→Uno broken flow                  |
  | GAP-02 | Mobile Conversion      | Ensures CTA taps register on mobile           |

═══════════════════════════════════════════════
  HANDOFF
═══════════════════════════════════════════════

  TO: change_manager
  TASK: Set up governance for Sprint 1 — update working_set.txt, validate scope,
        classify risk tier, create change request package.
  ARTIFACTS: This briefing (crew/output/sprint_1_briefing.md)
  CONTEXT: 6 items, 2 products, no backend, no CEO gates needed.

═══════════════════════════════════════════════
