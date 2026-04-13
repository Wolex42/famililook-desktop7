# Architecture Migration Candidates
**Maintained by:** Change Manager + Platform Architect
**Last updated:** 2026-04-07

---

## AppErrorBus Migration Queue
Files with catch blocks to migrate once AppErrorBus is built.

| File | Line | Current pattern | Added | Priority |
|------|------|----------------|-------|----------|
| `src/components/FacePicker.jsx` | ~83 | Inline error state + console.warn (UP-01 fix) | 2026-04-07 | HIGH |
| `src/state/BasketContext.jsx` | 25 | Empty catch block | pre-audit | CRITICAL |
| `src/utils/orderApi.js` | 22-31 | Timeout not surfaced to user | pre-audit | HIGH |
| `src/state/FamililookContext.jsx` | 154-157 | sessionStorage catch-all | pre-audit | MEDIUM |
| `src/game/CardGame.jsx` | 32-37 | buildDeck fail = blank screen | pre-audit | HIGH |
| `src/components/ui/ErrorBoundary.jsx` | various | safeSessionGet/Set wrappers (NV-03 fix) | 2026-04-07 | MEDIUM |
| `src/utils/lazyWithReload.js` | various | try/catch on sessionStorage (NV-03 fix) | 2026-04-07 | MEDIUM |
| + 18 others from platform audit Appendix A | | | pre-audit | VARIES |

**Total candidates:** ~25 files
**Recommendation:** Platform Architect should prioritise AppErrorBus build next sprint. FacePicker.jsx and BasketContext.jsx are highest priority due to user-facing impact.

---

## AppStorage Migration Queue
Files with raw localStorage/sessionStorage to migrate once AppStorage is built.

| File | Pattern | Added | Priority |
|------|---------|-------|----------|
| `src/hooks/useKinshipAnalysis.jsx` | localStorage.setItem catch ignored (lines ~297, ~539) | 2026-04-07 | HIGH |
| `src/utils/kinshipClient.js` | localStorage.getItem catch ignored (line ~65) | pre-audit | MEDIUM |
| `src/state/FamililookContext.jsx` | Multiple localStorage calls | pre-audit | HIGH |
| `src/hooks/usePlanFeatures.js` | localStorage for plan state | pre-audit | MEDIUM |
| `src/utils/analytics.js` | localStorage consent check | pre-audit | LOW |
| `src/components/ui/ErrorBoundary.jsx` | sessionStorage via safe wrappers (NV-03 fix) | 2026-04-07 | MEDIUM |
| `src/utils/lazyWithReload.js` | sessionStorage via try/catch (NV-03 fix) | 2026-04-07 | MEDIUM |
| + 30 others from 35-key localStorage audit | | pre-audit | VARIES |

**Total candidates:** ~37 files (35 keys documented in cookie-policy.html)
**Recommendation:** AppStorage should wrap localStorage with quota checks, JSON parse safety, and error reporting via AppErrorBus.

---

## resultsContract.js Migration Queue
Files with winner/percentage logic to migrate once resultsContract.js is built.

| File | What to migrate | Added | Priority |
|------|----------------|-------|----------|
| `src/hooks/useKinshipAnalysis.jsx` | Winner determination (lines ~443-457) | 2026-04-07 | HIGH |
| `src/hooks/useKinshipAnalysis.jsx` | Feature vote extraction (lines ~291-295) | pre-audit | HIGH |
| `src/layout/MobileResultsSection.jsx` | Winner re-derivation (lines ~350-416) | pre-audit | HIGH |
| `src/layout/MobileResultsSection.jsx` | Feature vote extraction (lines ~270-322) | pre-audit | HIGH |

**Total candidates:** 2 files (4 code regions)
**Recommendation:** This is the smallest migration scope. resultsContract.js should be a pure function module that both useKinshipAnalysis and MobileResultsSection import. Eliminates the 5-3 rule duplication risk.

---

## Patch Frequency Report (as of 2026-04-07)

Files at 3+ patches (AT LIMIT - requires CEO sign-off for further edits):

| File | Patch count | Status |
|------|-------------|--------|
| `src/layout/GroupSnapshotSection.jsx` | 11 | OVER LIMIT |
| `src/layout/AppLayout.jsx` | 5-8 | OVER LIMIT |
| `src/layout/MobileResultsSection.jsx` | 4 | OVER LIMIT |
| `src/game/MemoryMatch.jsx` | 4 | OVER LIMIT |
| `src/game/FaceMatchGame.jsx` | 4 | OVER LIMIT |
| `src/components/results/MobileResultsCarousel.jsx` | 4 | OVER LIMIT |
| `src/components/keepsakes/KeepsakesModal.jsx` | 4 | OVER LIMIT |
| `src/assets/characters/index.js` | 4 | OVER LIMIT |
| `src/utils/constants.js` | 3 | AT LIMIT |
| `src/pages/OccasionLanding.jsx` | 3 | AT LIMIT |
| `src/layout/UploadSection.jsx` | 3 | AT LIMIT |
| `src/game/CardGame.jsx` | 3 | AT LIMIT |
| `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` | 3 | AT LIMIT |
| `src/components/creation/ProductCreationFlow.jsx` | 3 | AT LIMIT |
| `src/AppRouter.jsx` | 3 | AT LIMIT |

Files at 2 patches (APPROACHING limit):

| File | Patch count |
|------|-------------|
| `src/utils/roleSuggestions.js` | 2 |
| `src/state/FamililookContext.jsx` | 2 |
| `src/pages/ProductCreationPage.jsx` | 2 |
| `src/pages/HomePage.jsx` | 2 |

**Action:** GroupSnapshotSection.jsx (11 patches) is the strongest redesign candidate. AppLayout.jsx and the 4-patch files should be reviewed by Platform Architect for structural issues.
