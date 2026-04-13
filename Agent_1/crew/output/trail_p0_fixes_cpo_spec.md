## CPO Spec: FamiliTrail P0 Fixes — Raise Acceptance from 40% to 70%+

**Agent**: CPO
**Task**: Fix the 15 BLOCKED nodes to reach shippable acceptance rate
**Date**: 2026-03-23

---

### Problem

E2E audit scored 88/220 (40%). 15 of 22 nodes are BLOCKED. Trail cannot be the front door at this rate. Target: 70%+ (154/220).

### Three P0 Fix Groups

---

#### FIX 1: Reclassify unbuilt features as `coming_soon` (nodes 17, 19, 20)

**What**: Multiplayer Battle (17) is explicitly "Coming Soon" in desktop4. Duo Room (19) and Group Party (20) depend on WebSocket endpoints that are unverified.

**Action**: Change tier to `coming_soon` in trailData.js for nodes 17, 19, 20. This is honest — don't promise what doesn't work.

**Acceptance Criteria**:
- [ ] Node 17 (`mp_battle`): tier → `coming_soon`, route → `null`, remove `external`
- [ ] Node 19 (`duo_room`): tier → `coming_soon`, route → `null`, remove `external`
- [ ] Node 20 (`group_party`): tier → `coming_soon`, route → `null`, remove `external`
- [ ] Tier count invariant updated: free=8, plus=4, pro=3, coming_soon=5 (was 9/6/5/2, total still 22 — adjust test)
- [ ] Node 18 (`solo_compare`) stays as-is (scored 8/10, works)

**Impact**: Removes 3 BLOCKED nodes. Honest with users. No more dead-end cross-app links.

---

#### FIX 2: Fix Keepsake Kingdom routing (nodes 6-9)

**What**: All 4 keepsake nodes route to `/app` with no section anchor. Users land on IntentSelector, not keepsakes. Node 7 should go to `/uno`.

**Action**: Route nodes to the correct destinations with state-aware behaviour:
- If user has analysis results → go to feature
- If user has no results → go to upload with a message "Complete an analysis first to unlock keepsakes"

**Acceptance Criteria**:
- [ ] Node 6 (`keepsake_cards`): route → `/app?section=keepsakes`
- [ ] Node 7 (`card_deck`): route → `/uno` (this is where the full card deck lives)
- [ ] Node 8 (`digital_dl`): route → `/app?section=keepsakes`
- [ ] Node 9 (`print_order`): route → `/app?section=keepsakes`
- [ ] AppLayout or UploadSection reads `?section=keepsakes` and auto-scrolls to results/keepsakes when data exists
- [ ] When no analysis data: shows toast/banner "Run an analysis first to unlock keepsakes" instead of dead end

**Impact**: Fixes 4 BLOCKED nodes. Keepsake Kingdom is the revenue zone — these must work.

---

#### FIX 3: Game cold-start fallback (nodes 11-14)

**What**: Games at `/uno?game=X` require `buildDeck()` to return cards. Cold users see upload phase, not the game.

**Action**: When user arrives at `/uno?game=X` with no deck data, show a friendly prompt instead of the raw upload phase:

**Acceptance Criteria**:
- [ ] FamiliUnoPage detects `?game=` param on mount
- [ ] If `hasCards` is false and `?game=` is present: show a targeted message — "To play [Game Name], run a family analysis first. Your family photos become the cards!"
- [ ] Include a CTA button: "Start Analysis →" linking to `/app?intent=child`
- [ ] If `hasCards` is true and `?game=` present: auto-launch the game (already works)

**Impact**: Fixes 4 BLOCKED nodes. Users get a clear path instead of confusion.

---

### Scope

- **FE only** — desktop2
- **Files to modify**: `trailData.js`, `FamiliUnoPage.jsx`, `AppLayout.jsx` or `UploadSection.jsx`
- **Tests to update**: `trailData.test.js` (tier count invariant changes)
- **No backend changes**

### Effort: S-M (half day)

---

**Handoff: CPO → CTO (verify WS endpoints for node reclassification) + FE Lead (implement all 3 fixes)**
