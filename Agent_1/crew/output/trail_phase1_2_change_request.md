═══════════════════════════════════════════════
  CHANGE REQUEST — CR-0001
═══════════════════════════════════════════════

RISK TIER: P2 — Standard
CHANGE TYPE: Code (FE only)
SOURCE: /crew feature — FamiliTrail fix + test coverage

DESCRIPTION: Fixed 17 broken/weak trail nodes and added 44 test cases across 6 files
CONTEXT: FamiliTrail is the primary discovery surface (22 nodes). Only 3/20 active nodes worked correctly. Zero test coverage existed.
ACTION: Phase 1 fixed routing (BrandHub tiles, deep-links, intent wiring). Phase 2 added comprehensive test suite.

FILES CHANGED (Phase 1 — fixes):
  famililook-desktop2/src/pages/BrandHubPage.jsx — Added FamiliPoker + FamiliMatch tiles
  famililook-desktop2/src/components/trail/trailData.js — Updated routes: arcade→?game=, casino/chemistry→external URLs
  famililook-desktop2/src/components/trail/TrailTooltip.jsx — Added external URL navigation
  famililook-desktop2/src/layout/UploadSection.jsx — Added ?intent= URL param reading
  famililook-desktop2/src/game/CardGame.jsx — Added ?game= URL param reading
  famililook-desktop2/src/components/upload/IntentSelector.jsx — Added pet intent config
  famililook-desktop2/vite.config.mjs — Added VITE_FAMILIPOKER_URL to define block

FILES CREATED (Phase 2 — tests):
  famililook-desktop2/tests/trail/trailData.test.js — 16 cases
  famililook-desktop2/tests/trail/trail-integration.test.js — 5 cases
  famililook-desktop2/tests/trail/FamilyTrailCanvas.test.jsx — 5 cases
  famililook-desktop2/tests/trail/TrailTooltip.test.jsx — 8 cases
  famililook-desktop2/tests/trail/PeekPreview.test.jsx — 4 cases
  famililook-desktop2/tests/trail/TrailHomePage.test.jsx — 6 cases

FILES MODIFIED (infrastructure):
  famililook-desktop2/vitest.config.ts — Added @vitejs/plugin-react for JSX transform

CREW ARTIFACTS:
  crew/output/trail_tests_cpo_spec.md — CPO spec (approved)
  crew/output/trail_tests_qa_spec.md — QA Lead test specifications
  crew/output/WORKFLOW_PROGRESS.md — Live progress tracker

VALIDATION:
  ✅ Traceability: FamiliTrail PRD (Agent_1/crew/tasks/PRD_FAMILITRAIL.md), TASK-016/017
  ✅ Tests: 967 / 967 pass (was 923 — +44 new trail tests)
  ✅ Build: passes
  ✅ Contract impact: None — no frozen contracts touched
  ✅ Blast radius: 7 FE files modified + 6 test files created + 1 config. No BE changes.
  ✅ Rollback plan: Revert commits (all changes are additive, no destructive modifications)

APPROVED BY: CEO (spec gate + test gate)
RECOMMENDATION: APPROVE — ready to commit
═══════════════════════════════════════════════
