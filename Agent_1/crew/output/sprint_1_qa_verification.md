# Sprint 1 — QA Verification Report

**Date**: 2026-03-31
**QA Lead**: Claude Code (QA Lead persona)
**Sprint**: Sprint 1 — Revenue + Critical UX
**Build status**: desktop2 1,071 tests PASSED | desktop6 build PASSED | desktop2 build PASSED

---

## Verification Matrix

| # | Ticket | Product | Fix Description | Status | Evidence |
|---|--------|---------|-----------------|--------|----------|
| 1 | FM-012 | FamiliMatch (desktop6) | Consent check in auto-nav useEffect | PASS | See V1 below |
| 2 | GAP-01 | FamiliMatch (desktop6) | Error card with "Try Again" between analysis and results | PASS | See V2 below |
| 3 | FL-024 | FamiliLook (desktop2) | BasketDrawer/BasketBadge integration in FamiliUnoPage | PASS | See V3 below |
| 4 | FL-002 | FamiliLook (desktop2) | singleParentHint helper message in UploadSection | PASS | See V4 below |
| 5 | FL-009 | FamiliLook (desktop2) | Storage event listener for fl:groupSnapshot | PASS | See V5 below |
| 6 | GAP-02 | FamiliLook (desktop2) | Portal button minHeight: 48 on HomePage | PASS | See V6 below |

**Result: 6/6 PASS — Sprint 1 fixes verified.**

---

## Detailed Verification

### V1: FM-012 — Consent check in auto-nav useEffect
**File**: `famililook-desktop6/src/pages/LandingPage.jsx` lines 178-192

**Expected**: Auto-navigation useEffect must check `consent.bipaConsented` before navigating. If not consented, store pending mode and show consent modal.

**Found**: Lines 184-188 contain:
```jsx
if (!consent.bipaConsented) {
  setPendingMode(card);
  setShowConsent(true);
  return;
}
```
This correctly gates auto-navigation behind consent. The consent check runs before `setMode` and `navigate`, and the early return prevents navigation without consent.

**Verdict**: PASS

---

### V2: GAP-01 — Error card with "Try Again" button
**File**: `famililook-desktop6/src/pages/SoloPage.jsx` lines 252-271

**Expected**: An error phase card must exist between the analysis spinner and results phase, displaying the error message and a "Try Again" button.

**Found**: Lines 252-271 contain a `motion.div` keyed as `"error"` that renders when `error && !analyzing && !results`. It includes:
- Red-tinted background card with border
- Error message: `<p className="text-red-400 ...">{error}</p>`
- "Try Again" button with `onClick={() => { setError(null); }}` and `minHeight: 44` (meets 44pt touch target)
- FamiliMatch brand gradient on button

**Verdict**: PASS

---

### V3: FL-024 — BasketDrawer and BasketBadge in FamiliUnoPage
**File**: `famililook-desktop2/src/pages/FamiliUnoPage.jsx`

**Expected**: (a) BasketDrawer and BasketBadge imported, (b) isBasketOpen state exists, (c) Event dispatch replaced with setIsBasketOpen(true), (d) Both rendered at bottom.

**Found**:
- **(a) Imports** — Lines 24-25:
  ```jsx
  import { BasketBadge } from "../components/keepsakes/BasketBadge.jsx";
  import { BasketDrawer } from "../components/keepsakes/BasketDrawer.jsx";
  ```
- **(b) State** — Line 57:
  ```jsx
  const [isBasketOpen, setIsBasketOpen] = useState(false);
  ```
- **(c) Event dispatch replaced** — Line 281:
  ```jsx
  setTimeout(() => setIsBasketOpen(true), 350);
  ```
  (No `window.dispatchEvent` for basket — uses direct state setter)
- **(d) Rendered at bottom** — Lines 734-735:
  ```jsx
  <BasketBadge onClick={() => setIsBasketOpen(true)} />
  <BasketDrawer isOpen={isBasketOpen} onClose={() => setIsBasketOpen(false)} />
  ```

**Verdict**: PASS (all 4 sub-checks confirmed)

---

### V4: FL-002 — singleParentHint helper message
**File**: `famililook-desktop2/src/layout/UploadSection.jsx`

**Expected**: A helper message appears between parent upload slots and the divider when only one parent is uploaded.

**Found**:
- Line 543: `const singleParentHint = mode !== "group" && ((hasParentA && !hasParentB) || (!hasParentA && hasParentB)) && !canAnalyze;`
- Lines 738-743: Conditional render of hint text:
  ```jsx
  {singleParentHint && (
    <p style={{ fontSize: "13px", color: colors.accent, textAlign: "center", ... }}>
      Add {hasParentA ? (parents[1]?.label || "a second parent") : (parents[0]?.label || "a parent")} to enable analysis
    </p>
  )}
  ```
- Uses brand accent colour, centered, contextually aware of which parent is missing.

**Verdict**: PASS

---

### V5: FL-009 — Storage event listener for fl:groupSnapshot
**File**: `famililook-desktop2/src/pages/FamiliUnoPage.jsx` lines 86-94

**Expected**: A `storage` event listener watches for `fl:groupSnapshot` changes and triggers card rebuild.

**Found**: Lines 86-94:
```jsx
useEffect(() => {
  const handleStorage = (e) => {
    if (e.key === "fl:groupSnapshot" && e.newValue) {
      if (checkHasCards()) setHasCards(true);
    }
  };
  window.addEventListener("storage", handleStorage);
  return () => window.removeEventListener("storage", handleStorage);
}, []);
```
- Correctly listens for `storage` events
- Filters on `e.key === "fl:groupSnapshot"` with `e.newValue` check
- Triggers `checkHasCards()` to rebuild deck
- Properly cleans up listener on unmount

**Verdict**: PASS

---

### V6: GAP-02 — Portal button minHeight: 48
**File**: `famililook-desktop2/src/pages/HomePage.jsx` line 427

**Expected**: The portal button (Link to "/trail") must have `minHeight: 48` for touch target compliance.

**Found**: Line 427 within the portal `<Link to="/trail" ...>` style object:
```jsx
minHeight: 48,
```

**Verdict**: PASS

---

## Regression Checks

| Check | Result |
|-------|--------|
| desktop2 unit tests (1,071) | PASSED |
| desktop2 build | PASSED |
| desktop6 build | PASSED |
| No contract changes (kinship_analyze.v1) | Confirmed |
| No contract changes (compare_faces.v1) | Confirmed |
| No backend modifications | Confirmed |

---

## Sprint 1 QA Summary

All 6 fixes verified against requirements. No regressions detected. Both repos build successfully. All 1,071 desktop2 tests pass. Sprint 1 is clear for closure.

**Signed off by**: QA Lead
**Date**: 2026-03-31
