## QA Lead: FamiliTrail Test Specification

**Agent**: QA Lead
**Input**: CPO spec (`trail_tests_cpo_spec.md`) — approved by CEO
**Date**: 2026-03-23

---

### Test File Plan (6 files, ~55 test cases)

All tests in `tests/trail/` directory, following project conventions:
- Vitest + @testing-library/react
- TestWrapper with BrowserRouter + CurrencyProvider + BasketProvider + FamililookProvider + EmotionalJourneyProvider
- No snapshots — explicit assertions only
- INVARIANT and REGRESSION labels where applicable

---

### File 1: `tests/trail/trailData.test.js` (AC-1 — Data Integrity)

Pure function tests — no render needed.

```
describe("Trail Data Integrity")
  it("has exactly 22 nodes")
  it("has no duplicate node IDs")
  it("every node has required fields: id, zone, label, icon, tier, desc")

  describe("Zone Validity")
    it("every node.zone maps to a valid zone in ZONES")
    it("ZONES has exactly 6 entries")
    it("every zone has id, label, color, icon")

  describe("Tier Validity")
    it("every node.tier maps to a valid tier in TIER_CONFIG")
    it("INVARIANT: tier counts = 9 free + 6 plus + 5 pro + 2 coming_soon")

  describe("Route Validity")
    it("coming_soon nodes have route: null")
    it("non-coming_soon nodes have truthy route or external")
    it("casino nodes have external property set")
    it("chemistry nodes have external property set")
    it("external URLs start with http")
    it("internal routes start with /")

  describe("Deep-Link Integrity")
    it("arcade nodes use ?game= param with valid game names")
    it("discovery nodes use ?intent= param with valid intent names")
```

**17 test cases**

---

### File 2: `tests/trail/FamilyTrailCanvas.test.jsx` (AC-2 — Canvas Rendering)

Component render test with TestWrapper.

```
describe("FamilyTrailCanvas")
  it("renders without crashing")
  it("renders 22 node elements")
  it("renders 6 zone background bands")
  it("renders the YOU ARE HERE token")

  describe("Visited Nodes")
    it("shows checkmark on visited nodes")
    it("does not show checkmark on unvisited nodes")
    it("applies glow effect to visited nodes")

  describe("Tier Badges")
    it("shows lock icon on plus/pro nodes")
    it("does not show lock on free nodes")
```

**9 test cases**

---

### File 3: `tests/trail/TrailTooltip.test.jsx` (AC-3 — Tooltip Behaviour)

Component interaction test with TestWrapper + mocked analytics.

```
describe("TrailTooltip")
  beforeEach: mock analytics.trackAction, clear localStorage

  describe("Rendering")
    it("renders node label and description")
    it("renders tier badge with correct colour")
    it("renders zone sibling nodes")

  describe("CTA Logic")
    it("shows 'Try It Now' for free node when user is free")
    it("shows 'Upgrade to Plus' for plus node when user is free")
    it("shows 'Upgrade to Pro' for pro node when user is plus")
    it("shows 'Get Notified When Ready' for coming_soon node")

  describe("Navigation")
    it("calls navigate() for internal route on CTA click")
    it("calls window.location.href for external node on CTA click")
    it("navigates to /plans for locked node upgrade click")

  describe("Analytics")
    it("fires trail_tooltip_opened on mount")
    it("fires trail_node_click on accessible CTA click")
    it("fires trail_upgrade_clicked on upgrade CTA click")

  describe("Dismiss")
    it("closes on Escape key")
    it("closes on backdrop click")
```

**14 test cases**

---

### File 4: `tests/trail/PeekPreview.test.jsx` (AC-4 — Peek Preview)

Component test with TestWrapper + localStorage mock.

```
describe("PeekPreview")
  beforeEach: set fl:analysisResults in localStorage

  it("renders timed preview content")
  it("shows upgrade CTA for locked content")
  it("shows personalised data from localStorage when available")
  it("countdown bar renders")
```

**4 test cases**

---

### File 5: `tests/trail/TrailHomePage.test.jsx` (AC-5 — Trail Page)

Page-level test with TestWrapper.

```
describe("TrailHomePage")
  beforeEach: clear localStorage

  describe("Rendering")
    it("renders trail canvas component")
    it("renders tier legend with free/plus/pro labels")

  describe("Progress Persistence")
    it("reads fl:trail_visited from localStorage on mount")
    it("writes visited node ID to localStorage on node click")
    it("REGRESSION: visited nodes persist across re-render")

  describe("Campaign Badges")
    it("shows campaign badge when current date is within event range")
    it("does not show expired campaign badges")
```

**7 test cases**

---

### File 6: `tests/trail/trail-integration.test.js` (AC-6 — Route Integration)

Integration test — verifies trail data maps to real app routes.

```
describe("Trail Route Integration")
  describe("Internal Routes")
    it("every non-null non-external route exists in AppRouter")
    it("INVARIANT: all ?intent= values are in UploadSection validIntents")
    it("INVARIANT: all ?game= values are in CardGame validGames")

  describe("External Routes")
    it("all external URLs are well-formed (start with http)")
```

**4 test cases**

---

### Total: 55 test cases across 6 files

| File | AC | Cases | Type |
|------|----|-------|------|
| trailData.test.js | AC-1 | 17 | Pure data validation |
| FamilyTrailCanvas.test.jsx | AC-2 | 9 | Component render |
| TrailTooltip.test.jsx | AC-3 | 14 | Component interaction |
| PeekPreview.test.jsx | AC-4 | 4 | Component render |
| TrailHomePage.test.jsx | AC-5 | 7 | Page-level |
| trail-integration.test.js | AC-6 | 4 | Route integration |

---

**Handoff: QA Lead → FE Lead**

**Task**: Implement the 6 test files per these specifications
**Context**: CPO spec approved, test conventions documented, zero trail tests exist today
**Artifacts**: This spec (`trail_tests_qa_spec.md`), CPO spec (`trail_tests_cpo_spec.md`)
**Decisions Made**: Tests go in `tests/trail/` directory, follow existing TestWrapper pattern, no snapshots
**Open Questions**: None — specs are explicit, conventions are documented
