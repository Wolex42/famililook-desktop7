═══════════════════════════════════════════════
  SPRINT 0B BRIEFING — 2026-03-31
═══════════════════════════════════════════════

SPRINT GOAL: Clear 7 quick-fix bugs across FamiliPoker and FamiliLook frontends
DURATION: 2026-03-31 (single-day sprint)
PRODUCTS: famililook-desktop2, famililook-desktop4

ITEMS:
  1. FP-003 — Fix Poker Back button (setSelectedGame → null)       — XS — desktop4
  2. FP-001 — Surface analysis errors in Poker (error card)        — XS — desktop4
  3. FL-003 — Fix OrderSuccess dark theme (bgPrimary → bgMain)     — XS — desktop2
  4. FL-004 — Fix from=home back nav (add missing case)            — XS — desktop2
  5. FL-006 — Move pet analysis from Coming Soon (remove entry)    — XS — desktop2
  6. FP-006 — Add analytics dev bypass (DEV guard)                 — XS — desktop4
  7. FP-007 — Fix Poker client ID (desktop2 → desktop4)            — XS — desktop4

TOTAL EFFORT: 7 x XS = ~30 min implementation + verification

FILE-TO-ITEM MAP (batching guide for FE Lead):
  famililook-desktop4/src/layout/AppLayout.jsx      — FP-003 (:538), FP-001 (:272)
  famililook-desktop2/src/layout/AppLayout.jsx      — FL-004 (:339), FL-006 (:809)
  famililook-desktop2/src/pages/OrderSuccessPage.jsx — FL-003 (:75)
  famililook-desktop4/src/utils/analytics.js         — FP-006 (:3)
  famililook-desktop4/src/hooks/useKinshipAnalysis.jsx — FP-007 (:337)

PRE-SPRINT CHECKLIST:
  [x] Dist backup — desktop6 dist_backup_20260331 (done)
  [x] Backend permission — NOT NEEDED (all frontend-only)
  [x] Change log exists — desktop2/.claude/change_log.md (exists)
  [x] Change log exists — desktop4/.claude/change_log.md (exists)
  [!] Pre-commit hooks — desktop4 has no .git/hooks/pre-commit installed.
      Root-level hook at .claude/pre-commit-hook.sh exists.
      MITIGATION: FE Lead must run `npm run test:run && npm run build`
      manually after each batch. Change Manager should install hook
      post-sprint if desktop4 will see regular commits.
  [x] Rollback strategy — git revert HEAD per repo
  [x] Working set — needs update (currently stale: docs/PLATFORM_ARCHITECTURE.md).
      Change Manager will set correct working set in Phase 2.

DEPENDENCIES:
  - NONE between items. All 7 are independent.
  - Items sharing a file (FP-003 + FP-001; FL-004 + FL-006) should be batched
    per file for a single CEO gate per file.

CEO DECISIONS NEEDED:
  - NONE. All items are XS effort, frontend-only, no contract changes,
    no backend modifications, no breaking changes.

RISKS:
  - LOW: desktop4 has no pre-commit hook — mitigated by manual test+build runs.
  - LOW: FP-001 (error card render) is the most complex item — requires
    destructuring + JSX addition. FE Lead should present full context.
  - NEGLIGIBLE: All other items are single-line changes at known locations.

HANDOFF:
  TO: change_manager
  TASK: Set up governance for Sprint 0B (working set, scope validation,
        risk classification, change request package)
  ARTIFACTS: This briefing (crew/output/sprint_0b_briefing.md)
  DECISIONS MADE: Sprint scope confirmed, no CEO gates required
  OPEN QUESTIONS: None

═══════════════════════════════════════════════
  COO SIGN-OFF: Sprint 0B ready for Phase 2
═══════════════════════════════════════════════
