## CPO Spec: FamiliTrail P1 Fixes — Last 5 BLOCKED Nodes

**Agent**: CPO
**Task**: Fix remaining 5 BLOCKED nodes to push active acceptance above 80%
**Date**: 2026-03-23

---

### Current: 114/170 active (67%). Target: 80%+ (136/170).

---

#### FIX 4: Collapse Discovery duplicates (nodes 2, 3)

**Problem**: Nodes 1, 2, 3 all route to `/app?intent=child`. Three trail stops → same screen. Users feel cheated.

**Decision**: Don't collapse — differentiate. These represent 3 real stages of the same journey. Fix by adding `#section` hints so post-analysis users land closer to the promised feature.

**Action**:
- Node 2 (`features_8`): route → `/app?intent=child&section=results` — when results exist, auto-scroll to feature breakdown
- Node 3 (`parent_compare`): route → `/app?intent=child&section=results` — same deep-link (results show parent comparison)
- When NO results exist: both still land on upload (correct — user needs to complete analysis first). Add tooltip hint: "Complete an analysis to see this"

**Acceptance Criteria**:
- [ ] Node 2 route updated to `/app?intent=child&section=results`
- [ ] Node 3 route updated to `/app?intent=child&section=results`
- [ ] AppLayout `?section=results` triggers auto-scroll to `resultsRef` when results exist
- [ ] Tooltip shows "Run an analysis first" context for nodes 2,3 when results don't exist (handled by existing tier gate — these are free nodes, so CTA always shows "Try It Now")

---

#### FIX 5: Pet Compare monetisation (node 5)

**Problem**: Pet mode works but has zero revenue path. Score 5/10 because Monetisation=0.

**Decision**: Don't build pet keepsakes now. Instead, add a cross-sell nudge after pet analysis: "Love your pet results? Try FamiliMatch to see who in the family looks most like the pet!"

**Action**:
- Node 5 stays as-is (route `/app?intent=pet` works)
- This is a UX/content fix, not a code fix — the monetisation gap is structural (no pet products exist). Accept the score for now.
- **No code change needed** — accept score of 5 as FIX REQUIRED, not BLOCKED.

**Acceptance Criteria**:
- [ ] Re-classify node 5 from BLOCKED to FIX REQUIRED (score 5 = threshold)

---

#### FIX 6: Cross-app deep-linking for Poker/21 (nodes 15, 16)

**Problem**: Nodes 15,16 navigate to desktop4 root. User lands on beta intro, needs 3+ clicks to find the game. No data portability.

**Decision**: We can't fix desktop4's routing from desktop2. But we CAN improve the trail node:
1. Update the external URL to include a hint param: `?from=trail&game=poker`
2. Update node descriptions to set expectations: "Opens FamiliPoker app — you'll need to upload photos there"

**Action**:
- [ ] Node 15 external URL: append `?from=trail&game=poker`
- [ ] Node 16 external URL: append `?from=trail&game=blackjack`
- [ ] Update descriptions to be honest about the cross-app experience
- [ ] Desktop4 wiring of `?game=` param is a separate task (TASK-NEW for desktop4 backlog, not this sprint)

---

### Scope
- **FE only** — desktop2
- **2 code changes**: trailData.js (routes + descriptions), AppLayout.jsx (section=results handler)
- **No new files**
- **Effort: S** (30 minutes)

---

**Handoff: CPO → FE Lead**
