## CPO Spec: FamiliTrail 22-Node E2E Customer Acceptance Audit

**Agent**: CPO
**Task**: `/crew audit "E2E deep-dive of all 22 trail features — customer acceptance scoring"`
**Date**: 2026-03-23

---

### What This Is

A customer-perspective walkthrough of every trail node. For each node, we test: can a user tap it, reach the feature, use it, and get value? We score each node on 5 dimensions.

### Scoring Rubric (per node)

| Dimension | Score | Meaning |
|-----------|-------|---------|
| **Reachable** | 0-2 | 0 = dead end, 1 = reaches page but wrong section, 2 = lands exactly where expected |
| **Functional** | 0-2 | 0 = broken/crashes, 1 = renders but incomplete, 2 = fully functional |
| **Data-Ready** | 0-2 | 0 = needs data that isn't available, 1 = works with mock/empty state, 2 = works with real data |
| **UX Quality** | 0-2 | 0 = confusing/broken layout, 1 = usable but rough, 2 = polished, iOS HIG compliant |
| **Monetisation** | 0-2 | 0 = no path to revenue, 1 = upgrade prompt exists but weak, 2 = clear CTA to purchase/upgrade |

**Max score per node: 10. Total max: 220.**

### Acceptance Thresholds

| Rating | Score Range | Meaning |
|--------|-----------|---------|
| SHIP | 8-10 | Customer-ready |
| FIX REQUIRED | 5-7 | Usable but gaps need addressing |
| BLOCKED | 0-4 | Cannot release to customers |

### Test Method

For each node:
1. Start at `/trail`
2. Tap the node on the trail board
3. Verify tooltip shows with correct description + CTA
4. Tap the CTA
5. Verify destination loads correctly
6. Verify the feature works (upload, game plays, keepsake renders, etc.)
7. Verify there's a path back to trail
8. Score all 5 dimensions

### What to Check Per Zone

**Discovery Zone (nodes 1-5)**: Upload flow starts, intent is set correctly, photos can be added
**Keepsake Kingdom (nodes 6-10)**: Keepsake cards render (requires prior analysis data), vault preview works
**Game Arcade (nodes 11-14)**: Game launches with correct mode, playable, cards render
**Casino Floor (nodes 15-17)**: External app loads, FamiliPoker is reachable and functional
**Chemistry Lab (nodes 18-20)**: External app loads, FamiliMatch is reachable and functional
**Coming Soon (nodes 21-22)**: Tooltip shows "Get Notified", no navigation occurs

### Parallel Execution

- QA Lead tests nodes 1-14 + 21-22 (internal, desktop2)
- CTO tests nodes 15-20 (cross-app, requires desktop4 + desktop6 reachability check)

---

**Handoff: CPO → QA Lead (nodes 1-14, 21-22) + CTO (nodes 15-20)**
