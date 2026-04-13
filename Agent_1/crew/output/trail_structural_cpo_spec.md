## CPO Spec: Trail Structural Gap Fixes — Target 80%+ Acceptance

**Agent**: CPO
**Date**: 2026-03-23
**Current**: 69% active acceptance. Target: 80%+

---

### Fix A: Re-enable Duo Room (node 19) — instant win
Desktop7 WebSocket is live and verified. Flip tier back.
- Node 19 (`duo_room`): `coming_soon` → `plus`, restore route + external URL
- Expected score: 3→7 (+4 points)
- File: trailData.js

### Fix B: Wire "Get Notified" to EmailCapture (nodes 17,19,20,21,22)
Currently the CTA on coming_soon nodes calls `onClose()` — ghost button.
Replace with EmailCapture inline in the tooltip.
- Import EmailCapture component into TrailTooltip
- For coming_soon nodes: render EmailCapture variant="inline" instead of ghost button
- Expected: converts interest into leads. UX score +1 per node.
- Files: TrailTooltip.jsx

### Fix C: Demo mode for games (nodes 11-14)
Games require `buildDeck()` to have data. Cold users see upload prompt.
Add "Try with sample family" using built-in demo data.
- Create DEMO_DECK constant in deckBuilder.js (3 sample cards with generic features)
- FamiliUnoPage: when ?game= present and !hasCards, show "Try Demo" button alongside "Start Analysis"
- Demo loads sample cards into CardGame without requiring real analysis
- Expected: Data-Ready 0→2 for all 4 arcade nodes (+4 points each = +16 total)
- Files: deckBuilder.js, FamiliUnoPage.jsx

### Fix D: Analysis-required message for keepsakes (nodes 6,8,9)
When user arrives at /app?section=keepsakes with no results, they see IntentSelector.
Add a contextual banner: "Complete a family analysis to unlock your keepsakes"
- AppLayout: when ?section=keepsakes and !hasResults, show info banner above upload
- Banner has "Start Analysis →" CTA
- Expected: UX score +1 for nodes 6,8,9 (+3 total)
- Files: AppLayout.jsx

### Fix E: Pet monetisation cross-sell (node 5)
Pet Compare has no revenue path. Add a cross-sell nudge after pet analysis.
- After pet results display, show: "Love your pet results? Compare with FamiliMatch!"
- Link to VITE_FAMILIMATCH_URL
- Expected: Monetisation 0→1 (+1 point)
- Files: UploadSection.jsx or results section

### Projected Score Impact

| Fix | Nodes | Points gained | Effort |
|-----|-------|--------------|--------|
| A: Duo re-enable | 19 | +4 | XS |
| B: Email capture | 17,20,21,22 | +4 (UX) | S |
| C: Demo mode | 11,12,13,14 | +8 (Data) | M |
| D: Keepsake banner | 6,8,9 | +3 (UX) | S |
| E: Pet cross-sell | 5 | +1 (Money) | XS |
| **Total** | **13 nodes** | **+20 points** | — |

Current: 117/170 (69%). After: ~137/170 (81%). Target exceeded.

---

**Handoff: CPO → FE Lead (all 5 fixes in order A→E)**
