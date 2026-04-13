# MODULE SPEC — resultsContract

**Platform Architect — 2026-04-09**
**Version:** 1.0
**Status:** SPEC COMPLETE — Awaiting CEO approval

---

## 1. PROBLEM CATEGORY

**Class of bugs eliminated:** Divergent winner determination, percentage calculation, feature vote extraction, and 50/50 nudge logic independently reimplemented across 7+ files. Each reimplementation makes slightly different assumptions about field paths, fallback behavior, and edge cases.

**Current instance count:** After full code audit, there are **6 independent reimplementations** of the same core logic:

### 1.1 Winner Determination — 6 locations

| # | File | Lines | Pattern | Notes |
|---|------|-------|---------|-------|
| 1 | `hooks/useKinshipAnalysis.jsx` | 126 | `inheritance.winner ?? child.winner ?? null` | Used for `fl:lastResults` storage. No normalization to mum/dad. |
| 2 | `hooks/useKinshipAnalysis.jsx` | 446, 456 | `inheritance.winner ?? child.winner ?? null` | Same pattern repeated for childRows and familyContext. |
| 3 | `layout/MobileResultsSection.jsx` | 365-378 | `childResult?.inheritance?.winner \|\| childResult?.winner \|\| childResult?.verdict?.primary_parent \|\| childResult?.verdict?.primaryParent` — then normalizes to "mum"/"dad" + feature count fallback | The most thorough but also the most complex. 4 fallback paths. |
| 4 | `layout/AnalysisSection.jsx` | 367-372 | `childEntry?.inheritance?.winner \|\| childEntry?.winner` → normalizes to "parent1"/"parent2" | Different normalization target than MobileResultsSection. |
| 5 | `components/keepsakes/hooks/useKeepsakeData.js` | 40-41 | `winner === "parent1" \|\| winner === "parent_a" \|\| winner === "mum"` → boolean `isParent1Winner` | Yet another normalization variant. |
| 6 | `components/keepsakes/hooks/useFamilyKeepsakeData.js` | 41-43 | `childResult.winner \|\| childResult.inheritance?.winner` → same triple check | Reversed field order from MobileResultsSection (`.winner` before `.inheritance?.winner`). |

**Divergence risk:** Files #3 and #6 check fields in **different order**. `childResult.winner` vs `childResult.inheritance?.winner` — if both fields are present with different values (a backend bug), these files will disagree on who won.

### 1.2 Feature Vote Extraction — 5 locations

| # | File | Lines | Pattern |
|---|------|-------|---------|
| 1 | `layout/MobileResultsSection.jsx` | 292-296 | `childResult?.feature_votes \|\| childResult?.features?.feature_votes \|\| childResult?.inheritance?.feature_votes \|\| {}` |
| 2 | `components/keepsakes/hooks/useKeepsakeData.js` | 52-56 | Identical 4-path fallback |
| 3 | `components/keepsakes/hooks/useFamilyKeepsakeData.js` | 45-49 | Identical 4-path fallback |
| 4 | `layout/AnalysisSection.jsx` | 375 | `childEntry?.feature_votes \|\| childEntry?.features?.feature_votes \|\| {}` — **missing** `inheritance?.feature_votes` path |
| 5 | `hooks/useKinshipAnalysis.jsx` | 137, 447 | `child.feature_votes \|\| {}` or `child.feature_votes \|\| inheritance.feature_votes \|\| {}` — **inconsistent** between the two locations |

**Divergence risk:** AnalysisSection (#4) misses the `inheritance.feature_votes` path. If the backend puts votes under `inheritance`, AnalysisSection shows no features while MobileResultsSection shows them correctly.

### 1.3 Percentage Calculation — 3 locations

| # | File | Lines | Pattern |
|---|------|-------|---------|
| 1 | `layout/MobileResultsSection.jsx` | 384-398 | Backend scores normalized to 100%. Fallback: feature count / 8 × 100. |
| 2 | `components/keepsakes/hooks/useKeepsakeData.js` | 96-104 | `Math.round((p1Score / total) * 100)`, `parent2Pct = 100 - parent1Pct`. Default scores: `0.5`. |
| 3 | `components/keepsakes/hooks/useFamilyKeepsakeData.js` | 72-77 | Identical to #2 but uses `p1Score`/`p2Score` variable names. |

**Divergence risk:** MobileResultsSection (#1) does NOT round. useKeepsakeData (#2) uses `Math.round`. On a 62.5/37.5 split, MobileResultsSection shows 62.5% while useKeepsakeData shows 63%. Different numbers for the same child.

### 1.4 The 50/50 Nudge Rule — 1 location (but incomplete)

| # | File | Lines | Pattern |
|---|------|-------|---------|
| 1 | `layout/MobileResultsSection.jsx` | 404-424 | `if (Math.abs(parent1Pct - parent2Pct) < 2)` → force 51/49. Then a second check: if display winner doesn't match backend winner, flip percentages. |

**Only MobileResultsSection implements the nudge.** useKeepsakeData and useFamilyKeepsakeData do NOT. If a keepsake product receives a 50/50 split, it will display "50% Mum / 50% Dad" — violating the cardinal rule.

### 1.5 Parent Normalization — 4 patterns

The backend returns `"parent1"`, `"parent2"`, `"parent_a"`, `"parent_b"`. The frontend normalizes to different targets:

| File | Target | Pattern |
|------|--------|---------|
| MobileResultsSection | `"mum"` / `"dad"` | `parent2 \|\| parent_b → "dad"`, `parent1 \|\| parent_a → "mum"` |
| AnalysisSection | `"parent1"` / `"parent2"` | Only normalizes `parent_a → parent1`, `parent_b → parent2` |
| useKeepsakeData | boolean `isParent1Winner` | Triple-checks `parent1 \|\| parent_a \|\| mum` |
| childSummaryGenerator | `"mum"` / `"parent1"` | `winner === "mum" \|\| winner === "parent1"` |

Four different normalization strategies for the same semantic concept.

### 1.6 Impact

- **AN-02 (Winner flip):** If `.winner` and `.inheritance.winner` disagree, MobileResultsSection and useFamilyKeepsakeData show different winners for the same child.
- **AN-03 (Percentage mismatch):** MobileResultsSection shows unrounded percentages; keepsake products show rounded percentages. Different numbers for the same child.
- **AN-04 (50/50 violation):** Keepsake products can display 50%/50% because they don't implement the nudge rule.
- **GM-04 (Feature path miss):** AnalysisSection misses the `inheritance.feature_votes` path, showing empty features when other views show them correctly.

---

## 2. MODULE INTERFACE

### 2.1 Architecture Decision: Pure Functions Module

**No state, no side effects, no React dependencies, no imports from AppErrorBus or AppStorage.**

This module is a collection of pure functions:
- Same input → same output, always
- No `localStorage`, no `sessionStorage`, no DOM access
- No `import.meta.env` checks
- Importable from any module (React components, utils, API clients, tests)
- Extractable to `@famililook/shared/infrastructure/resultsContract` without code changes
- Every function is independently testable with zero mocks

**Why pure functions?** Winner determination and percentage calculation are mathematical operations on data. They have no reason to touch state, storage, or the DOM. Making them pure eliminates an entire class of bugs (stale closures, race conditions, initialization order).

### 2.2 File Location

```
src/infrastructure/resultsContract.js     (alongside AppErrorBus.js and AppStorage.js)
```

### 2.3 Constants

```javascript
/**
 * The 8 canonical features. Every analysis result must have exactly these.
 * Order is display order (eyes first, ears last).
 */
export const CANONICAL_FEATURES = Object.freeze([
  'eyes', 'eyebrows', 'smile', 'nose', 'face_shape', 'skin', 'hair', 'ears'
]);

/**
 * Human-readable labels for display.
 */
export const FEATURE_LABELS = Object.freeze({
  eyes: 'Eyes',
  eyebrows: 'Eyebrows',
  smile: 'Smile',
  nose: 'Nose',
  face_shape: 'Face Shape',
  skin: 'Skin',
  hair: 'Hair',
  ears: 'Ears',
});

/**
 * The minimum percentage gap between parents.
 * If the gap is less than this, the nudge rule forces 51/49.
 */
export const MIN_PERCENTAGE_GAP = 2;

/**
 * The nudge values applied when percentages are too close.
 */
export const NUDGE_WINNER_PCT = 51;
export const NUDGE_LOSER_PCT = 49;
```

### 2.4 Type Definitions

```javascript
/**
 * @typedef {'parent1' | 'parent2' | 'parent_a' | 'parent_b' | 'mum' | 'dad' | null} RawWinner
 *
 * @typedef {'parent1' | 'parent2'} NormalizedParent
 *   - 'parent1' always means the first parent uploaded (slot 0, "Mum" in traditional mode)
 *   - 'parent2' always means the second parent uploaded (slot 1, "Dad" in traditional mode)
 *
 * @typedef {Object} FeatureVotes
 * @property {string} eyes       - 'parent1'|'parent2'|'unknown'
 * @property {string} eyebrows   - 'parent1'|'parent2'|'unknown'
 * @property {string} smile      - 'parent1'|'parent2'|'unknown'
 * @property {string} nose       - 'parent1'|'parent2'|'unknown'
 * @property {string} face_shape - 'parent1'|'parent2'|'unknown'
 * @property {string} skin       - 'parent1'|'parent2'|'unknown'
 * @property {string} hair       - 'parent1'|'parent2'|'unknown'
 * @property {string} ears       - 'parent1'|'parent2'|'unknown'
 *
 * @typedef {Object} FeatureCounts
 * @property {number} parent1Count   - Features matching parent1 (0-8)
 * @property {number} parent2Count   - Features matching parent2 (0-8)
 * @property {number} unknownCount   - Features that could not be determined (0-8)
 * @property {boolean} invariantHolds - parent1Count + parent2Count + unknownCount === 8
 *
 * @typedef {Object} Percentages
 * @property {number} parent1Pct - Parent 1 percentage (integer, 0-100)
 * @property {number} parent2Pct - Parent 2 percentage (integer, 0-100, parent1Pct + parent2Pct === 100)
 * @property {boolean} nudged    - Whether the 50/50 rule was applied
 *
 * @typedef {Object} ResultsSummary
 * @property {NormalizedParent|null} winner    - Who won
 * @property {string|null}          winnerReason - Backend reason string
 * @property {Percentages}          percentages  - Display percentages (always sum to 100)
 * @property {FeatureVotes}         featureVotes - Normalized 8-feature votes
 * @property {FeatureCounts}        featureCounts - Counts per parent + unknown
 * @property {number}               winnerPct    - The winner's percentage (convenience)
 * @property {number}               loserPct     - The loser's percentage (convenience)
 */
```

### 2.5 Public API

```javascript
// ─── Winner Determination ───────────────────────────────────────

resultsContract.getWinner(childResult: Object): NormalizedParent | null
// Extracts and normalizes the winner from a backend child result object.
//
// Field resolution order (first non-null wins):
//   1. childResult.inheritance?.winner
//   2. childResult.winner
//   3. childResult.verdict?.primary_parent
//   4. childResult.verdict?.primaryParent
//
// Normalization:
//   'parent1' | 'parent_a' | 'mum'  → 'parent1'
//   'parent2' | 'parent_b' | 'dad'  → 'parent2'
//   'blend' | 'unknown' | null      → null
//
// If all fields are null/undefined: returns null.
// If childResult is null/undefined: returns null.

// ─── Feature Vote Extraction ────────────────────────────────────

resultsContract.extractFeatureVotes(childResult: Object): FeatureVotes
// Extracts and normalizes the 8-feature vote map from a backend child result.
//
// Field resolution order:
//   1. childResult.feature_votes
//   2. childResult.features?.feature_votes
//   3. childResult.inheritance?.feature_votes
//
// Per-feature normalization:
//   'parent1' | 'parent_a' | 'mum'  → 'parent1'
//   'parent2' | 'parent_b' | 'dad'  → 'parent2'
//   anything else (null, undefined, 'unknown') → 'unknown'
//
// Missing features are filled as 'unknown'.
// Always returns exactly 8 keys (CANONICAL_FEATURES).
// If childResult is null/undefined: returns all 8 features as 'unknown'.

// ─── Feature Counting ───────────────────────────────────────────

resultsContract.countFeatures(featureVotes: FeatureVotes): FeatureCounts
// Counts features per parent from a FeatureVotes object.
//
// Returns: { parent1Count, parent2Count, unknownCount, invariantHolds }
// invariantHolds is true when parent1Count + parent2Count + unknownCount === 8.
//
// If featureVotes is null/undefined: returns { 0, 0, 8, true }.

// ─── Percentage Calculation ─────────────────────────────────────

resultsContract.getPercentages(childResult: Object, winner: NormalizedParent | null): Percentages
// Calculates display percentages from backend scores or feature counts.
//
// Step 1: Try backend parent_scores
//   If childResult.parent_scores.parent1 AND .parent2 are numbers:
//     parent1Pct = round((parent1 / (parent1 + parent2)) * 100)
//     parent2Pct = 100 - parent1Pct
//
// Step 2: Fallback to feature counts
//   If no backend scores: extract feature votes, count features
//     parent1Pct = round((parent1Count / 8) * 100)
//     parent2Pct = 100 - parent1Pct
//
// Step 3: Apply 50/50 nudge rule (calls apply5050Rule internally)
//
// Always returns integers that sum to exactly 100.
// If childResult is null: returns { parent1Pct: 50, parent2Pct: 50, nudged: true }
//   (50/50 with nudge applied to match winner direction).

// ─── 50/50 Nudge Rule ──────────────────────────────────────────

resultsContract.apply5050Rule(parent1Pct: number, parent2Pct: number, winner: NormalizedParent | null): Percentages
// The Cardinal Rule: NEVER show 50/50.
//
// If Math.abs(parent1Pct - parent2Pct) < MIN_PERCENTAGE_GAP (2):
//   If winner === 'parent1': return { parent1Pct: 51, parent2Pct: 49, nudged: true }
//   If winner === 'parent2': return { parent1Pct: 49, parent2Pct: 51, nudged: true }
//   If winner is null: return { parent1Pct: 51, parent2Pct: 49, nudged: true } (arbitrary tiebreak)
//
// If percentages disagree with winner (winner is parent1 but parent2Pct > parent1Pct):
//   Flip to match: winner's percentage = max(currentPct, 51), loser's = 100 - winner's
//   nudged: true
//
// Otherwise: return as-is with nudged: false.
//
// Input percentages must be integers. Output percentages always sum to 100.

// ─── Full Summary Builder ───────────────────────────────────────

resultsContract.buildResultsSummary(childResult: Object): ResultsSummary
// One-call convenience that runs all the above functions and returns
// a complete, consistent, display-ready summary for one child.
//
// Equivalent to:
//   const winner = getWinner(childResult)
//   const featureVotes = extractFeatureVotes(childResult)
//   const featureCounts = countFeatures(featureVotes)
//   const percentages = getPercentages(childResult, winner)
//   const winnerPct = winner === 'parent1' ? percentages.parent1Pct : percentages.parent2Pct
//   const loserPct = winner === 'parent1' ? percentages.parent2Pct : percentages.parent1Pct
//
// This is the recommended entry point for most consumers.
// MobileResultsSection, useKeepsakeData, useFamilyKeepsakeData should all
// call buildResultsSummary() instead of reimplementing.
//
// Returns null if childResult is null/undefined.

// ─── Validation ─────────────────────────────────────────────────

resultsContract.validateResults(childResult: Object): { valid: boolean, errors: string[] }
// Checks a backend child result for contract violations.
//
// Checks:
//   1. feature_votes exists and has exactly 8 keys
//   2. All 8 CANONICAL_FEATURES are present
//   3. Each vote is 'parent1'|'parent2'|'parent_a'|'parent_b'|'mum'|'dad'|'unknown'
//   4. parent1Count + parent2Count + unknownCount === 8
//   5. If winner is present, it matches feature majority (5-3 rule)
//   6. parent_scores (if present) are both numbers in [0, 1]
//
// Returns { valid: true, errors: [] } or { valid: false, errors: ['...', '...'] }.
// This function does NOT throw — it returns errors as data.
// Used for dev-mode contract checking and test assertions.
```

---

## 3. ADOPTION RULE

**Once resultsContract ships (Phase 1 complete), the following is FORBIDDEN:**

### Rule A: No inline winner extraction

```javascript
// FORBIDDEN after Phase 1:
const winner = inheritance.winner ?? child.winner ?? null;
const winner = childResult.winner || childResult.inheritance?.winner;

// REQUIRED:
import { getWinner } from '../infrastructure/resultsContract';
const winner = getWinner(childResult);
```

### Rule B: No inline feature vote extraction

```javascript
// FORBIDDEN:
const featureVotes =
  childResult?.feature_votes ||
  childResult?.features?.feature_votes ||
  childResult?.inheritance?.feature_votes ||
  {};

// REQUIRED:
import { extractFeatureVotes } from '../infrastructure/resultsContract';
const featureVotes = extractFeatureVotes(childResult);
```

### Rule C: No inline percentage calculation

```javascript
// FORBIDDEN:
const parent1Pct = Math.round((p1Score / total) * 100);
const parent2Pct = 100 - parent1Pct;

// REQUIRED:
import { getPercentages } from '../infrastructure/resultsContract';
const { parent1Pct, parent2Pct } = getPercentages(childResult, winner);
```

### Rule D: No inline 50/50 nudge logic

```javascript
// FORBIDDEN:
if (Math.abs(parent1Pct - parent2Pct) < 2) {
  parent1Pct = 51; parent2Pct = 49;
}

// REQUIRED:
// Already handled inside getPercentages() and apply5050Rule()
```

### Enforcement

- **Change Manager** — reviews all PRs for inline winner/percentage/feature logic outside `resultsContract.js`. Rejects any PR that re-derives these values.
- **Platform Architect** — blocks any PR that adds winner determination logic outside the contract.
- **QA Lead** — verifies migration completeness. Blocks release if inline logic remains.
- **ESLint rule** (Phase 4) — `no-inline-results-logic` custom rule that flags patterns like `inheritance.winner ?? child.winner` or `featureCount / 8 * 100` outside of `resultsContract.js`.

---

## 4. MIGRATION PATH

### Phase 1: Build Module + Tests (1 session)

**Deliverables:**
1. Create `src/infrastructure/resultsContract.js` — pure functions per Section 2 spec
2. Create `tests/infrastructure/resultsContract.test.js` — minimum 20 tests per Section 6
3. No existing files changed

**Zero migration in Phase 1.** The module is built and tested in isolation.

### Phase 2: Migrate useKinshipAnalysis.jsx (1 session)

The hook currently builds `childRows` for `fl:lastResults` with inline winner extraction (lines 126, 446, 456). Migrate to use `getWinner()` and `extractFeatureVotes()`.

**Phase 2 files:**

| File | Lines | What changes |
|------|-------|-------------|
| `hooks/useKinshipAnalysis.jsx` | 126, 137, 446-447, 456 | Replace inline `inheritance.winner ?? child.winner ?? null` with `getWinner(child)`. Replace `child.feature_votes \|\| {}` with `extractFeatureVotes(child)`. |

**Blocked file:** useKinshipAnalysis.jsx requires Platform Architect review + CEO waiver.

### Phase 3: Migrate MobileResultsSection + all consumers (1-2 sessions)

Migrate the 175-line results processing block (lines 270-513) in MobileResultsSection to a single `buildResultsSummary()` call. Then migrate all keepsake data hooks and remaining consumers.

**Phase 3 files:**

| File | Lines | What changes |
|------|-------|-------------|
| `layout/MobileResultsSection.jsx` | 270-513 | Replace 240-line block with `buildResultsSummary(childResult)`. Keep cache logic (lines 457-494) — that is UI-specific, not contract logic. |
| `layout/AnalysisSection.jsx` | 367-389 | Replace inline winner + feature extraction with `getWinner()` + `extractFeatureVotes()`. |
| `components/keepsakes/hooks/useKeepsakeData.js` | 40-116 | Replace 76-line winner/feature/percentage block with `buildResultsSummary()`. |
| `components/keepsakes/hooks/useFamilyKeepsakeData.js` | 37-114 | Replace 77-line winner/feature/percentage block with `buildResultsSummary()`. |
| `utils/childSummaryGenerator.js` | 182-195 | Replace inline `isParentAWinner` + percentage extraction with `getWinner()` + contract-provided percentages. |
| `utils/narrativeGenerator.js` | 27-40 | Replace inline parent normalization (`"mum" \|\| "parent1"`) with constants from resultsContract. |

### Phase 4: ESLint Rule (0.5 session)

1. Add `no-inline-results-logic` custom rule to `eslint.config.js`
2. Flag: `inheritance.winner`, `child.winner ?? null`, `featureCount / 8`, `Math.abs(.*Pct.*) < 2`
3. Exemption: `src/infrastructure/resultsContract.js`
4. Severity: `error` (blocks CI)

---

## 5. FILES AFFECTED — Complete List

### New Files (Phase 1)

| File | Purpose |
|------|---------|
| `src/infrastructure/resultsContract.js` | Pure functions module |
| `tests/infrastructure/resultsContract.test.js` | Unit tests |

### Modified Files (Phase 2) — 1 file

| File | Change |
|------|--------|
| `hooks/useKinshipAnalysis.jsx` | 5 inline winner/feature extractions → resultsContract |

### Modified Files (Phase 3) — 6 files

| File | Change |
|------|--------|
| `layout/MobileResultsSection.jsx` | 240-line processing block → `buildResultsSummary()` |
| `layout/AnalysisSection.jsx` | Inline winner + feature extraction → contract functions |
| `components/keepsakes/hooks/useKeepsakeData.js` | 76-line block → `buildResultsSummary()` |
| `components/keepsakes/hooks/useFamilyKeepsakeData.js` | 77-line block → `buildResultsSummary()` |
| `utils/childSummaryGenerator.js` | Inline parent check → contract functions |
| `utils/narrativeGenerator.js` | Inline parent normalization → contract constants |

### Modified Files (Phase 4) — 1 file

| File | Change |
|------|--------|
| `eslint.config.js` | Add `no-inline-results-logic` rule |

---

## 6. TEST REQUIREMENTS

### 6.1 Unit Tests — resultsContract (`resultsContract.test.js`)

**Pure functions = deterministic tests. No mocks, no timers, no async.** Every test is `input → expected output`.

**Must test (minimum 20):**

**getWinner (5 tests):**
1. **Normal case — inheritance.winner present** — `{ inheritance: { winner: "parent1" } }` → `'parent1'`
2. **Fallback to child.winner** — `{ winner: "parent2" }` → `'parent2'`
3. **Normalizes parent_a/parent_b** — `{ winner: "parent_a" }` → `'parent1'`, `{ winner: "parent_b" }` → `'parent2'`
4. **Normalizes mum/dad** — `{ inheritance: { winner: "mum" } }` → `'parent1'`; `{ winner: "dad" }` → `'parent2'`
5. **Null input** — `null` → `null`; `undefined` → `null`; `{}` → `null`

**extractFeatureVotes (4 tests):**
6. **Normal case — feature_votes present** — returns all 8 features normalized to parent1/parent2/unknown
7. **Fallback to inheritance.feature_votes** — `{ inheritance: { feature_votes: {...} } }` → extracted
8. **Missing features filled as unknown** — `{ feature_votes: { eyes: "parent1" } }` → 7 features are 'unknown'
9. **Null input** — returns all 8 features as 'unknown'

**countFeatures (3 tests):**
10. **Normal 5-3 split** — 5 parent1 + 3 parent2 → `{ parent1Count: 5, parent2Count: 3, unknownCount: 0, invariantHolds: true }`
11. **With unknowns** — 4 parent1 + 2 parent2 + 2 unknown → `{ 4, 2, 2, true }`
12. **All unknown** — returns `{ 0, 0, 8, true }`

**getPercentages (4 tests):**
13. **From backend scores** — `parent_scores: { parent1: 0.62, parent2: 0.38 }` → `{ parent1Pct: 62, parent2Pct: 38, nudged: false }`
14. **Fallback to feature counts** — no parent_scores, 6 parent1 features → `{ parent1Pct: 75, parent2Pct: 25, nudged: false }`
15. **50/50 nudge applied** — `parent_scores: { parent1: 0.5, parent2: 0.5 }`, winner=parent1 → `{ parent1Pct: 51, parent2Pct: 49, nudged: true }`
16. **Null input** — returns `{ parent1Pct: 50, parent2Pct: 50, nudged: true }` (nudged to match default)

**apply5050Rule (3 tests):**
17. **Gap < 2, winner parent1** — `apply5050Rule(50, 50, 'parent1')` → `{ 51, 49, true }`
18. **Gap < 2, winner parent2** — `apply5050Rule(50, 50, 'parent2')` → `{ 49, 51, true }`
19. **Winner disagrees with percentages** — `apply5050Rule(45, 55, 'parent1')` → `{ 51, 49, true }` (flipped to match winner)

**buildResultsSummary (2 tests):**
20. **Full normal case** — complete backend result → summary with all fields consistent
21. **Null input** — returns null

**validateResults (3 tests):**
22. **Valid result** — full 8-feature result with consistent winner → `{ valid: true, errors: [] }`
23. **Missing features** — only 5 features → `{ valid: false, errors: ['Expected 8 features, got 5'] }`
24. **Winner contradicts features** — winner is parent1 but parent2 has 6 features → `{ valid: false, errors: [...] }`

---

## 7. SECONDARY FAILURE RISKS

### Risk 1: Null/Undefined Propagation
**Scenario:** A consumer calls `getWinner(undefined)` or `buildResultsSummary(null)` and the function throws instead of returning null.
**Mitigation:** Every function handles null/undefined input explicitly. `getWinner(null)` → `null`. `extractFeatureVotes(null)` → 8 unknowns. `buildResultsSummary(null)` → `null`. No function throws on null input.

### Risk 2: Integer vs Float Percentage Rounding
**Scenario:** Backend returns `parent_scores: { parent1: 0.625, parent2: 0.375 }`. One consumer shows 62.5%, another shows 63%.
**Mitigation:** `getPercentages()` always returns **integers**. `parent1Pct = Math.round(...)`, `parent2Pct = 100 - parent1Pct`. This guarantees sum to 100 and eliminates float divergence. All consumers get the same integer.

### Risk 3: Feature Count Mismatch
**Scenario:** Backend returns 7 features instead of 8. The 8th feature is missing.
**Mitigation:** `extractFeatureVotes()` always returns exactly 8 features (CANONICAL_FEATURES). Missing features default to `'unknown'`. `countFeatures()` always produces counts that sum to 8. `validateResults()` flags the mismatch so dev mode can warn.

### Risk 4: Backend Field Path Changes
**Scenario:** A backend deploy changes `inheritance.winner` to `analysis.winner`. The contract module becomes the single point to update.
**Mitigation:** This is the **design goal**. The 6 current reimplementations mean 6 files to update. After migration, only `resultsContract.js` needs updating. One file, one PR, one test run.

### Risk 5: Order Invariance Violation
**Scenario:** Parent A and Parent B are swapped. The winner label should change but the real winner should stay the same. If percentage calculation uses parent_scores positionally, swapping parents changes percentages.
**Mitigation:** `getPercentages()` always ties parent1Pct to parent_scores.parent1 and parent2Pct to parent_scores.parent2. The backend handles order invariance at the scoring level. The contract module does not re-derive who is parent1 vs parent2 — it trusts the backend slot assignment.

### Risk 6: The "Blend" Winner Edge Case
**Scenario:** Backend returns `winner: "blend"` or `winner: "unknown"`. No clear parent won.
**Mitigation:** `getWinner()` returns `null` for blend/unknown. `getPercentages()` with `winner: null` still applies the nudge (arbitrary tiebreak to parent1 at 51/49). `buildResultsSummary()` returns `winner: null` — the UI must handle this case (show "Perfect Blend" or similar). This edge case is already handled in MobileResultsSection's current code.

---

## 8. BUILD ESTIMATE

| Phase | Sessions | FE Lead Work |
|-------|----------|-------------|
| Phase 1: Build module + tests | 0.5 | Pure functions — fast to write, fast to test. No mocks, no async. |
| Phase 2: Migrate useKinshipAnalysis | 0.5 | 5 call sites in 1 file. CEO waiver required. |
| Phase 3: Full migration | 1-2 | 6 files. MobileResultsSection is the largest (240 → ~20 lines). |
| Phase 4: ESLint rule | 0.5 | Custom pattern matching for winner/percentage/feature inline logic. |
| **Total** | **2.5-3.5 sessions** | |

**Dependencies:**
- No dependencies on AppErrorBus or AppStorage. Pure functions module.
- No new npm dependencies.

**Risk to existing tests:** LOW. The module produces the same outputs as the current inline logic. Migrated files should pass existing tests without modification. Any test that hardcodes percentage values may need adjustment if the rounding behavior changes (current: some locations don't round, some do — the contract always rounds).

---

## 9. IMPLEMENTATION NOTES FOR FE LEAD

### Do:
- Keep every function pure (no side effects, no state mutation, no DOM access)
- Use `Object.freeze()` on all exported constants
- Use `Math.round()` for ALL percentage calculations — never return floats
- Ensure `parent1Pct + parent2Pct === 100` in every code path (use `100 - otherPct` pattern)
- Export individual named functions AND a default object for convenience:
  ```javascript
  export { getWinner, getPercentages, extractFeatureVotes, ... };
  export default { getWinner, getPercentages, extractFeatureVotes, ... };
  ```
- Handle null/undefined input in every function — return sensible defaults, never throw
- Use CANONICAL_FEATURES as the source of truth for which 8 features exist

### Do Not:
- Do NOT import AppErrorBus — this module is pure logic, no error reporting
- Do NOT import AppStorage — this module does not touch persistence
- Do NOT import React or any React hooks — this module is framework-agnostic
- Do NOT use `import.meta.env` — no environment-specific behavior
- Do NOT add any side effects (logging, console.log, analytics) — consumers do that
- Do NOT add caching — consumers (useMemo in React components) handle memoization
- Do NOT handle the "consistency cache" logic from MobileResultsSection:457-494 — that is UI-specific state management, not contract logic

### Normalization Convention:
- All functions normalize to `'parent1'` / `'parent2'` / `'unknown'` — never to `'mum'`/`'dad'`
- Consumers map `'parent1'` → display label (e.g., "Mum", parent name) at the UI layer
- This keeps the contract module parent-label-agnostic (works for any family structure)

---

## APPENDIX A: Example Migration — useKinshipAnalysis.jsx (getWinner)

**Before (current code, lines 126-130):**
```javascript
const winner = inheritance.winner ?? child.winner ?? null;

return {
  name: child.name,
  winner,
  confidence,
  features: ...
};
```

**After (Phase 2 migration):**
```javascript
import { getWinner, extractFeatureVotes } from '../infrastructure/resultsContract';

const winner = getWinner(child);

return {
  name: child.name,
  winner,
  confidence,
  features: ...
};
```

**Key points:**
- One import replaces the inline extraction
- `getWinner()` handles all 4 field paths (inheritance.winner, child.winner, verdict.primary_parent, verdict.primaryParent)
- Normalization is consistent with every other consumer

---

## APPENDIX B: Example Migration — MobileResultsSection.jsx (buildResultsSummary)

**Before (current code, lines 270-513 — 240 lines):**
```javascript
const childCards = React.useMemo(() => {
  return analysisResults.children.map((childResult, idx) => {
    // 240 lines of:
    // - feature vote extraction (4 fallback paths)
    // - unknown feature counting
    // - parent normalization (parent2/parent_b → "dad")
    // - feature count invariant check
    // - percentage calculation from backend scores OR feature counts
    // - 50/50 nudge rule
    // - winner/percentage alignment check
    // - consistency cache logic
    // - debug logging
    return { id, name, photo, winner, confidence, parent1Pct, parent2Pct, features, ... };
  });
}, [...]);
```

**After (Phase 3 migration):**
```javascript
import { buildResultsSummary } from '../infrastructure/resultsContract';

const childCards = React.useMemo(() => {
  return analysisResults.children.map((childResult, idx) => {
    const summary = buildResultsSummary(childResult);
    if (!summary) return null;

    const uploadedChild = children?.[idx];

    // Consistency cache logic stays here (UI-specific)
    let finalWinner = summary.winner;
    let finalParent1Pct = summary.percentages.parent1Pct;
    let finalParent2Pct = summary.percentages.parent2Pct;

    if (childFile && getCachedResult && setCachedResult) {
      // ... cache logic unchanged ...
    }

    return {
      id: childResult?.id || uploadedChild?.id || `child-${idx}`,
      name: uploadedChild?.label || childResult?.name || `Child ${idx + 1}`,
      photo: uploadedChild?.previewUrl || childResult?.photo,
      winner: finalWinner === 'parent1' ? 'mum' : 'dad',  // UI-layer label mapping
      confidence: finalWinner === 'parent1' ? finalParent1Pct : finalParent2Pct,
      parent1Pct: finalParent1Pct,
      parent2Pct: finalParent2Pct,
      features: summary.featureVotes,
      featureSimilarities,
      unknownFeatureCount: summary.featureCounts.unknownCount,
      unknownFeatures: CANONICAL_FEATURES.filter(f => summary.featureVotes[f] === 'unknown'),
      hasQualityIssue: summary.featureCounts.unknownCount >= 2,
    };
  });
}, [...]);
```

**Key points:**
- 240 lines → ~30 lines. The contract module handles all the extraction, normalization, counting, percentage calculation, and nudge logic.
- The consistency cache logic stays in MobileResultsSection — it is UI state management, not contract logic.
- `'parent1' → 'mum'` mapping happens at the UI layer, not inside the contract.
- `featureVotes` from the contract is already normalized (no need for the `getParent()` helper).
- The feature count invariant check is now inside `validateResults()` — can be called in dev mode.

---

**END OF SPEC**

**Next step:** CEO approval required. Upon approval, FE Lead implements Phase 1. QA Lead reviews Phase 1 tests before Phase 2 begins.

**Prerequisites confirmed:**
- AppErrorBus: BUILT (Phases 1-3 complete)
- AppStorage: BUILT (Phase 1 complete)
- Both are in `src/infrastructure/` — resultsContract will sit alongside them
- resultsContract has NO dependency on either — pure functions only
