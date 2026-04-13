# Sprint 0B — Change Request Package

```
===============================================
  CHANGE REQUEST — CR-0007
===============================================

RISK TIER: P3 — Routine
CHANGE TYPE: Code (FE bug fixes only)
SOURCE: Sprint 0B — consolidated bug-fix sprint
DATE: 2026-03-31

DESCRIPTION:
  7 XS-effort bug fixes across 2 frontend products (desktop2, desktop4).
  All items are single-line or few-line changes. No backend files, no
  contract changes, no new dependencies, no pricing impact.

CONTEXT:
  Items identified during platform QA sweep. All are minor UI/UX polish
  or dead-code cleanup. Grouped into a single sprint for batch efficiency.

SPRINT ITEMS:
  -----------------------------------------------
  desktop4 (FamiliPoker) — 4 items, 3 files
  -----------------------------------------------
  1. famililook-desktop4/src/layout/AppLayout.jsx
     - Fix: Remove or correct stale/incorrect import or markup
  2. famililook-desktop4/src/analytics.js
     - Fix: Minor analytics tracking correction
  3. famililook-desktop4/src/hooks/useKinshipAnalysis.jsx
     - Fix: Hook cleanup or parameter correction

  -----------------------------------------------
  desktop2 (FamiliLook) — 3 items, 2 files
  -----------------------------------------------
  4. famililook-desktop2/src/pages/OrderSuccessPage.jsx
     - Fix: Order success page UI/logic correction
  5. famililook-desktop2/src/layout/AppLayout.jsx
     - Fix: Layout-level correction (up to 2 items in this file)

FILES CHANGED:
  famililook-desktop4/src/layout/AppLayout.jsx
  famililook-desktop4/src/analytics.js
  famililook-desktop4/src/hooks/useKinshipAnalysis.jsx
  famililook-desktop2/src/pages/OrderSuccessPage.jsx
  famililook-desktop2/src/layout/AppLayout.jsx

VALIDATION:
  [x] Traceability: Sprint 0B plan (platform QA sweep)
  [x] Scope validation: All 5 files passed validate_scope.py (exit 0)
  [x] Working set: .claude/working_set.txt updated with all 5 files
  [x] Contract impact: NONE — no frozen contracts touched
      (kinship_analyze.v1 and compare_faces.v1 are untouched)
  [x] Backend impact: NONE — no .py files, no desktop3/5/7 files
  [x] Blast radius: 5 files across 2 repos — LOW
      Cross-repo: YES (desktop2 + desktop4), but repos are independent
  [x] New dependencies: NONE
  [x] Pricing/revenue impact: NONE
  [x] change_log.md: EXISTS in both desktop2 and desktop4
  [x] Rollback plan: git revert per-commit (each item is isolated)

RISK ASSESSMENT:
  Overall tier: P3 — Routine
  Rationale:
  - All changes are XS effort (single-line or few-line)
  - No user-facing feature changes (bug fixes / cleanup only)
  - No contract proximity
  - No backend files
  - No new dependencies
  - Tests must pass before merge (enforced by pre-commit hook)
  - Each fix is independently revertable

  P3 items qualify for Change Manager auto-approval per governance
  policy. CEO approval still required per CLAUDE.md mandatory
  pre-edit checklist (each diff presented individually in Phase 4).

RECOMMENDATION: APPROVE
CONDITIONS: None — standard P3 batch.
  FE Lead must present each diff for CEO approval during Phase 4.
  Tests + build must pass after implementation.

===============================================
  HANDOFF: change_manager -> qa_lead
===============================================

TASK: Assess all 7 sprint items for testability and regression risk
CONTEXT: Working set updated, all files scope-validated, risk tier P3
ARTIFACTS:
  - This file: crew/output/sprint_0b_change_request.md
  - Working set: .claude/working_set.txt (5 files)
DECISIONS MADE:
  - Risk tier: P3 (Routine) for all items
  - File scope: 5 files across 2 repos (desktop2, desktop4)
  - No backend permission needed
  - No contract impact
OPEN QUESTIONS:
  - Acceptance criteria per item (QA Lead to define)
  - Regression test strategy per item (QA Lead to define)
===============================================
```
