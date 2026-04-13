## CPO Spec: FamiliTrail Test Coverage & Governance

**Agent**: CPO
**Task**: `/crew feature "FamiliTrail — 22 nodes governed and tested"`
**Date**: 2026-03-23
**ICE Score**: Impact 8 × Confidence 9 × Ease 7 = 504

---

### Problem

FamiliTrail is the primary discovery surface for the platform — 22 nodes mapping every feature across 4 products. Phase 1 just fixed 17 broken/weak nodes. But there are **zero tests** covering trail components. Any future change to routes, node data, or tier gating could silently break the user's gateway to every feature. This is a regression bomb.

### Goal

100% test coverage for trail components with invariant protection, so no code change can break the user's path through the platform without tests catching it.

### Acceptance Criteria

**AC-1: Trail data integrity (trailData.test.js)**
- [ ] All 22 nodes exist with valid `id`, `zone`, `label`, `tier`, `route`
- [ ] Every node's `zone` maps to a valid zone in `ZONES`
- [ ] Every node's `tier` maps to a valid tier in `TIER_CONFIG`
- [ ] No duplicate node IDs
- [ ] Tier counts: 9 free + 6 plus + 5 pro + 2 coming_soon = 22
- [ ] `coming_soon` nodes have `route: null`
- [ ] Non-coming_soon nodes have a truthy `route` or `external`
- [ ] Casino/Chemistry nodes have `external` property set

**AC-2: Canvas rendering (FamilyTrailCanvas.test.jsx)**
- [ ] Renders without crashing
- [ ] Renders exactly 22 node elements
- [ ] Applies visited checkmark to nodes in `visitedNodes` prop
- [ ] Zone backgrounds render for all 6 zones
- [ ] "YOU ARE HERE" token renders

**AC-3: Tooltip behaviour (TrailTooltip.test.jsx)**
- [ ] Renders node label and description
- [ ] Shows "Try It Now" CTA for accessible nodes (tier ≤ user plan)
- [ ] Shows "Upgrade to Plus/Pro" CTA for locked nodes
- [ ] Shows "Get Notified" for coming_soon nodes
- [ ] Fires `trail_tooltip_opened` analytics event
- [ ] Fires `trail_node_click` on CTA click for accessible nodes
- [ ] Fires `trail_upgrade_clicked` on upgrade CTA click
- [ ] Uses `window.location.href` for nodes with `external` property
- [ ] Uses `navigate()` for internal route nodes
- [ ] Closes on Escape key
- [ ] Closes on backdrop click

**AC-4: Peek preview (PeekPreview.test.jsx)**
- [ ] Renders timed preview (2 seconds)
- [ ] Shows personalised data from localStorage
- [ ] Shows upgrade CTA for locked content
- [ ] Countdown bar animates

**AC-5: Trail page (TrailHomePage.test.jsx)**
- [ ] Page renders with trail canvas
- [ ] Reads `fl:trail_visited` from localStorage on mount
- [ ] Writes visited node ID on click
- [ ] Shows tier legend
- [ ] Shows campaign badges when within event date range

**AC-6: Route integration (trail-integration.test.js)**
- [ ] Every non-null, non-external route in `TRAIL_NODES` is a registered route in AppRouter
- [ ] Every `?intent=` value used by trail nodes is in the `validIntents` array in UploadSection
- [ ] Every `?game=` value used by trail nodes is in the `validGames` array in CardGame
- [ ] External URLs are well-formed (start with http)

### Scope

- **FE-only** — no backend changes
- **desktop2 only** — trail lives here
- **Files to create**: 6 new test files in `src/__tests__/trail/` or co-located
- **Files NOT to modify**: No production code changes — tests only

### Priority

**P1** — Trail is the front door. Untested front door = silent breakage = user drop-off.

### Effort

**M** — 6 test files, ~50 test cases total. QA Lead specs, FE Lead implements.

---

**Handoff: CPO → QA Lead**

**Task**: Write detailed test specifications for all 6 acceptance criteria above
**Context**: Trail components are built, Phase 1 fixes applied, zero tests exist today
**Artifacts**: This spec (`trail_tests_cpo_spec.md`)
**Decisions Made**: Test scope is trail components only, no production code changes
**Open Questions**: None — acceptance criteria are explicit
