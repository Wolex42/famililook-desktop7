═══════════════════════════════════════════════
  CHANGE REQUEST — CR-0004
═══════════════════════════════════════════════

RISK TIER: P2 — Standard
CHANGE TYPE: Code (FE only)
SOURCE: /crew feature — FamiliTrail P1 fixes (eliminate all BLOCKED nodes)

DESCRIPTION: Differentiated Discovery nodes 2,3 with section=results deep-link. Added game hint params to Poker/21 external URLs. Honest descriptions for cross-app experience.
CONTEXT: After CR-0003, 5 nodes remained BLOCKED (2,3,5,15,16). All scored 4-5, close to threshold.
ACTION: Fix 4 (nodes 2,3 → ?section=results), Fix 5 (node 5 accepted at 5), Fix 6 (nodes 15,16 → ?game= hint + honest desc).

FILES MODIFIED:
  famililook-desktop2/src/components/trail/trailData.js — routes + descriptions for nodes 2,3,15,16
  famililook-desktop2/src/layout/AppLayout.jsx — ?section=results handler (extended existing keepsakes handler)

VALIDATION:
  ✅ Tests: 975 / 975 pass
  ✅ Build: passes
  ✅ Contract impact: None
  ✅ Blast radius: 2 files modified

RESULTS:
  BLOCKED nodes: 15 → 0
  Active acceptance: 67% → 69%
  SHIP: 4 | FIX REQUIRED: 12 | COMING SOON: 5 | BLOCKED: 0

APPROVED BY: CEO
═══════════════════════════════════════════════
