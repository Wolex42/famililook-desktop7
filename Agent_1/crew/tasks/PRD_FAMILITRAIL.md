# PRD: FamiliTrail — Feature Discovery Board

> **Author**: CPO Agent
> **Date**: 2026-03-21
> **Product**: FamiliLook (desktop2)
> **Priority**: P1
> **Status**: IN_PROGRESS (core built, enhancements needed)

---

## 1. Problem Statement

Users don't discover the full breadth of FamiliLook features. The homepage shows a 4-tile brand hub, but the 22+ features across analysis, games, keepsakes, and cross-product experiences are buried in navigation. Users churn after a single analysis without trying games, ordering keepsakes, or exploring premium tiers.

## 2. Goal

A gamified, visually engaging product map that surfaces all features, drives tier upgrades (Free → Plus → Pro), and increases feature adoption by 40%.

## 3. Context

- **Current state**: FamiliTrail is BUILT and LIVE at `/trail`. Core board, tooltip, peek preview, and tier gating all working. 3 homepage entry points exist.
- **Evidence**: Build output confirms `TrailHomePage-*.js` bundled. All 22 nodes render. Routes verified. Campaign dates current.
- **What's missing**: Analytics tracking, progress persistence, achievements, seasonal theming, A/B testing.

## 4. User Stories

- As a free user, I want to see all features on one page, so I know what upgrading unlocks.
- As a Plus subscriber, I want to see my progress through the trail, so I feel rewarded for exploring.
- As a returning user, I want the trail to remember which stops I've visited, so I don't repeat discovery.
- As an admin, I want analytics on trail interactions, so I can optimize the upgrade funnel.

## 5. Acceptance Criteria

### Already Done
- [x] 22 trail nodes across 6 zones render on SVG canvas
- [x] Snaking board-game path with smooth Bezier curves between nodes
- [x] Tier gating: Free/Plus/Pro/Coming Soon visual differentiation
- [x] "YOU ARE HERE" bouncing token at last accessible stop
- [x] Bottom-sheet tooltip with node description, CTA, zone cross-sell
- [x] 2-second peek preview for locked nodes using personalised localStorage data
- [x] Campaign window badges (Mother's Day UK/US, Easter)
- [x] 3 homepage entry points (event countdown, portal button, Uno teaser)
- [x] Zone background bands + floating particles + zone labels
- [x] Lock badges on gated nodes + tier pills
- [x] Upgrade nudge for free users
- [x] Footer links

### To Build (Priority Order)
- [ ] **P1: Analytics tracking** — fire `trail_node_click`, `trail_peek_viewed`, `trail_tooltip_opened`, `trail_upgrade_clicked` events via `analytics.trackAction()`
- [ ] **P1: Progress persistence** — store visited node IDs in `localStorage fl:trail_visited`, show checkmark/glow on visited stops
- [ ] **P2: Achievement badges** — "Discovery Explorer" (visit all free), "Power User" (visit 15+), render as toast + badge on trail header
- [ ] **P2: A/B test framework** — feature flag `VITE_TRAIL_DEFAULT_LANDING` to test trail vs homepage as default route
- [ ] **P3: Dynamic unlock animation** — particle burst + scale-up when user upgrades and new stops become accessible
- [ ] **P3: Seasonal zone theming** — Easter eggs in Discovery Zone, Christmas snow particles, Valentine hearts in Chemistry Lab
- [ ] **P3: Animated trail completion** — confetti animation when all accessible stops visited

## 6. Scope

### In Scope
- Analytics event tracking (FE only, uses existing `analytics.js`)
- localStorage progress persistence
- Achievement system (FE only, no backend)
- A/B test feature flag in vite config

### Out of Scope
- Backend changes (all FE-only)
- Trail node content changes (node data in trailData.js is stable)
- New routes or pages (trail already has its route)

## 7. Agent Assignments

| Step | Agent | Task | Depends On |
|------|-------|------|-----------|
| 1 | fe_lead | Add analytics event tracking to TrailTooltip, PeekPreview, FamilyTrailCanvas | — |
| 2 | fe_lead | Implement progress persistence (fl:trail_visited in localStorage) | — |
| 3 | fe_lead | Add visited node visual indicator (checkmark/glow overlay on TrailNode) | Step 2 |
| 4 | design_lead | Design achievement badge visuals (3 tiers) | — |
| 5 | fe_lead | Implement achievement system + toast notifications | Steps 3, 4 |
| 6 | qa_lead | Write tests for trail analytics + persistence + achievements | Steps 1-5 |
| 7 | fe_lead | A/B test feature flag for trail as default landing | Step 6 |
| 8 | design_lead | Seasonal zone theming assets | — |
| 9 | fe_lead | Implement seasonal theming system | Step 8 |

## 8. Dependencies & Blockers

- Dependency: `analytics.js` must be working (it is — verified)
- Dependency: `localStorage` access (standard, no issues)
- No blockers

## 9. Success Metrics

| Metric | Baseline | Target | Measured By |
|--------|----------|--------|-------------|
| Feature discovery rate | Unknown | 60% of users visit trail | trail_node_click events |
| Upgrade conversion from trail | 0% | 5% of free users click upgrade CTA | trail_upgrade_clicked events |
| Stops visited per session | Unknown | ≥4 stops per visit | fl:trail_visited count |
| Trail bounce rate | Unknown | <30% (user interacts with ≥1 node) | trail_tooltip_opened events |

## 10. Effort Estimate

- **Size**: M (analytics + persistence = 2 days; achievements = 2 days; A/B test = 1 day; seasonal = 2 days)
- **ICE Score**: Impact(8) × Confidence(9) × Ease(7) = 504

## Files to Modify

| File | Changes |
|------|---------|
| `src/components/trail/FamilyTrailCanvas.jsx` | Add visited node glow, achievement check |
| `src/components/trail/TrailTooltip.jsx` | Add analytics.trackAction() calls |
| `src/components/trail/PeekPreview.jsx` | Add analytics.trackAction() for peek_viewed |
| `src/components/trail/trailData.js` | No changes (data stable) |
| `src/pages/TrailHomePage.jsx` | Progress bar, achievement banner |
| `src/utils/analytics.js` | No changes (API stable) |
| `tests/trail/*.test.jsx` | New test file(s) for trail features |
