═══════════════════════════════════════════════
  CHANGE REQUEST — CR-0003
═══════════════════════════════════════════════

RISK TIER: P2 — Standard
CHANGE TYPE: Code (FE only)
SOURCE: /crew feature — FamiliTrail P0 fixes (raise acceptance from 40% to 67%)

DESCRIPTION: Fixed 11 trail nodes — reclassified 3 unbuilt features as coming_soon, fixed 4 keepsake dead-end routes, added game cold-start prompt for 4 arcade nodes
CONTEXT: E2E acceptance audit scored 40% (88/220). 15 of 22 nodes BLOCKED. Trail cannot be the front door at this rate.
ACTION: Three fix groups applied per CPO spec (trail_p0_fixes_cpo_spec.md).

FIX 1 — Reclassified unbuilt features:
  Node 17 (mp_battle): tier pro → coming_soon, route removed (multiplayer not built)
  Node 19 (duo_room): tier plus → coming_soon, route removed (WebSocket unverified)
  Node 20 (group_party): tier pro → coming_soon, route removed (WebSocket unverified)

FIX 2 — Keepsake Kingdom routing:
  Node 6 (keepsake_cards): /app → /app?section=keepsakes (auto-scroll to results)
  Node 7 (card_deck): /app → /uno (correct destination — card deck lives here)
  Node 8 (digital_dl): /app → /app?section=keepsakes
  Node 9 (print_order): /app → /app?section=keepsakes
  AppLayout.jsx: added ?section=keepsakes handler (reads param, scrolls to results, cleans URL)

FIX 3 — Game cold-start fallback:
  FamiliUnoPage.jsx: when ?game=X present but no deck data, shows friendly prompt:
    "To play [Game Name], run a quick family analysis first" + "Start Analysis →" CTA

FILES MODIFIED:
  famililook-desktop2/src/components/trail/trailData.js
  famililook-desktop2/src/layout/AppLayout.jsx
  famililook-desktop2/src/pages/FamiliUnoPage.jsx
  famililook-desktop2/tests/trail/trailData.test.js

VALIDATION:
  ✅ Tests: 975 / 975 pass
  ✅ Build: passes
  ✅ Contract impact: None
  ✅ Blast radius: 4 files modified, no new files
  ✅ Tier invariant test updated and passing (9 free + 5 plus + 3 pro + 5 coming_soon = 22)

RESULTS:
  Before: 88/220 (40%), 15 BLOCKED
  After: 120/220 (55%), active nodes 114/170 (67%)
  SHIP: 5 nodes | FIX REQUIRED: 7 | COMING_SOON: 5 | BLOCKED: 5

APPROVED BY: CEO
═══════════════════════════════════════════════
