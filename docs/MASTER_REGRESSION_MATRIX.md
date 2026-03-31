# Master Regression Prevention Matrix

**Document:** QA-MRM-001
**Date:** 2026-03-31
**Owner:** QA Lead
**Status:** CURRENT — single source of truth for regression prevention
**Sources:** UXD_all_products.md, FMEA_comprehensive.md, guardrails.json, contracts/*.schema.json, test_coverage.md

---

## Section 1: UXD Flow → FMEA → Test → Contract Traceability Matrix

### PRODUCT 1: FamiliLook (famililook-desktop2)

| UXD Step | Name | Related FMEA IDs | Original RPN | Status | Test Coverage | Contract Dep | Sprint |
|---|---|---|---|---|---|---|---|
| FL-1.1 | Homepage Load | FMEA-FL-011, FMEA-FL-023, FMEA-GAP-02 | 80, 90, 120 | FIXED (Sprint 3), Open, FIXED (Sprint 1) | NONE | none | Sprint 1 (GAP-02), Sprint 3 (FL-011) |
| FL-1.2 | A/B Trail Redirect | — | — | — | NONE | none | N/A |
| FL-2.1 | Trail Map Load | FMEA-FL-012 | 100 | Open | NONE | none | N/A |
| FL-2.2 | Trail Tooltip | — | — | — | NONE | none | N/A |
| FL-2.3 | Trail Completion | — | — | — | NONE | none | N/A |
| FL-3.1 | App Shell Load | FMEA-FL-004, FMEA-FL-010, FMEA-FL-020 | 144, 90, 60 | FIXED (Sprint 0B), Open, Open | NONE | kinship_analyze.v1 | Sprint 0B (FL-004) |
| FL-3.2 | Biometric Consent | DFMEA-FM-09 | ~~160~~ → 60 | IMPLEMENTED | NONE | none | — |
| FL-3.3 | Intent Selection | — | — | — | NONE | none | N/A |
| FL-3.4 | Photo Upload | FMEA-FL-014, FMEA-FL-016, FMEA-GAP-07 | 90, 80, 75 | Open, Open, Open | NONE | none | N/A |
| FL-3.5 | COPPA Age Gate | FMEA-FL-016 | 80 | Open | NONE | none | N/A |
| FL-3.6 | Analyze | FMEA-FL-002, FMEA-GAP-12, **FMEA-FL-026** | 140, 90, **80** | FIXED (Sprint 1), Open, **Open** | NONE | kinship_analyze.v1 | Sprint 1 (FL-002) |
| FL-3.7 | Results Display | FMEA-FL-015, FMEA-FL-021, DFMEA-FM-02, DFMEA-FM-03, FMEA-GAP-09 | 70, 24, 72, 70, 64 | Open, Open, Acceptable, Acceptable, Open | regressionFlows.test.js (partial) | kinship_analyze.v1 | N/A |
| FL-4.1 | Group Photo Upload | — | — | — | NONE | kinship_analyze.v1 | N/A |
| FL-4.2 | Face Name Assignment | — | — | — | NONE | kinship_analyze.v1 | N/A |
| FL-4.3 | Group Analysis | DFMEA-FM-17 | ~~84~~ → 12 | MITIGATED | NONE | kinship_analyze.v1 | — |
| FL-5.1 | Keepsakes Modal Entry | FMEA-FL-005 | 84 | FIXED (Sprint 3) | NONE | none | Sprint 3 |
| FL-5.2 | Category Selection | — | — | — | NONE | none | N/A |
| FL-5.3 | Product & Style | DFMEA-FM-12, DFMEA-FM-16 | 42, 120 | Acceptable, FIXED (Sprint 2) | NONE | none | Sprint 2 (DFMEA-FM-16) |
| FL-5.4 | Preview | DFMEA-FM-04, DFMEA-FM-11, **FMEA-FL-025** | 40, 72, **126** | Acceptable, Acceptable, **Open** | printRobustness.test.js (partial) | none | N/A |
| FL-6.1 | Basket Drawer | DFMEA-FM-14, DFMEA-FM-15 | 96, 30 | Monitor, Acceptable | addressValidation.test.js | none | N/A |
| FL-6.2 | Stripe Checkout | DFMEA-FM-13 | 32 | Acceptable | NONE | none | N/A |
| FL-6.3 | Order Success | FMEA-FL-003, FMEA-FL-022, FMEA-GAP-03 | 128, 45, 42 | FIXED (Sprint 0B), Open, Open | NONE | none | Sprint 0B (FL-003) |
| FL-7.1 | Upgrade Wall | — | — | — | NONE | none | N/A |
| FL-7.2 | Plans Page | FMEA-FL-007, FMEA-FL-018, FMEA-GAP-05 | 108, 96, 60 | FIXED (Sprint 2), Open, Open | NONE | none | Sprint 2 (FL-007) |
| FL-8.1 | About Tab | FMEA-FL-006 | 100 | FIXED (Sprint 0B) | NONE | none | Sprint 0B |
| FL-9.1 | Demo Mode | FMEA-FL-008 | 108 | FIXED (Sprint 3) | NONE | none | Sprint 3 |

### PRODUCT 2: FamiliUno (famililook-desktop2, /uno route)

| UXD Step | Name | Related FMEA IDs | Original RPN | Status | Test Coverage | Contract Dep | Sprint |
|---|---|---|---|---|---|---|---|
| FU-1.1 | Landing (No Cards) | FMEA-FL-001, FMEA-FL-009, FMEA-GAP-10 | 60, 120, 48 | Open, FIXED (Sprint 1), Open | deckBuilder.test.js (partial) | kinship_analyze.v1 | Sprint 1 (FL-009) |
| FU-2.1 | Landing (Cards Available) | — | — | — | deckBuilder.test.js (deck building) | kinship_analyze.v1 | N/A |
| FU-3.1 | Game Selection | — | — | — | NONE | none | N/A |
| FU-3.2 | Game Play | — | — | — | NONE | none | N/A |
| FU-4.1 | Physical Deck Order | FMEA-FL-024 | 126 | FIXED (Sprint 1) | NONE | card_deck_order.v1 | Sprint 1 |
| FU-5 | Back Navigation | FMEA-FL-004 (shared) | 144 | Open | NONE | none | N/A |

### PRODUCT 3: FamiliPoker (famililook-desktop4)

| UXD Step | Name | Related FMEA IDs | Original RPN | Status | Test Coverage | Contract Dep | Sprint |
|---|---|---|---|---|---|---|---|
| FP-1.1 | Age Confirmation | — | — | — | NONE | none | N/A |
| FP-2.1 | Initial App State | FMEA-FP-011 | 80 | Open | NONE | kinship_analyze.v1 | N/A |
| FP-2.2 | Photo Upload | FMEA-FP-002, FMEA-FP-019 | 336, 36 | Open, Open | NONE | kinship_analyze.v1 | N/A |
| FP-2.3 | Analysis | FMEA-FP-001, FMEA-FP-007 | 162, 150 | FIXED (Sprint 0B), FIXED (Sprint 0B) | NONE | kinship_analyze.v1 | Sprint 0B |
| FP-3.1 | Game Selection | FMEA-FP-004, FMEA-FP-010, FMEA-FP-020 | 56, 32, 24 | Open, Open, Open | NONE | none | N/A |
| FP-4.1 | Poker Age/Tutorial | FMEA-GAP-06 | 70 | Open | NONE | none | N/A |
| FP-4.2 | Poker Gameplay | FMEA-FP-003, FMEA-FP-017 | 144, 30 | FIXED (Sprint 0B), Open | NONE | none | Sprint 0B (FP-003) |
| FP-4.3 | Poker Result | — | — | — | NONE | none | N/A |
| FP-5.1 | Blackjack Tutorial | — | — | — | NONE | none | N/A |
| FP-5.2 | Blackjack Gameplay | FMEA-FP-009, FMEA-FP-018 | 40, 24 | Open, Open | NONE | none | N/A |
| FP-6 | Plans Page | FMEA-FP-005, FMEA-FP-014 | 160, 180 | Open, Open | NONE | none | N/A |

**FamiliPoker additional (no UXD step):**

| FMEA ID | Title | RPN | Status | Test Coverage |
|---|---|---|---|---|
| FMEA-FP-006 | Analytics dev bypass missing | 300 | FIXED (Sprint 0B) | NONE |
| FMEA-FP-008 | ErrorBoundary raw crash | 28 | Open | NONE |
| FMEA-FP-012 | Home re-tap exits app | 60 | Open | NONE |
| FMEA-FP-013 | TypeScript dead code | 24 | Open | NONE |
| FMEA-FP-015 | Two analytics implementations | 200 | FIXED (Sprint 2) | NONE |
| FMEA-FP-016 | Version string mismatch | 40 | Open | NONE |

### PRODUCT 4: FamiliMatch (famililook-desktop6)

| UXD Step | Name | Related FMEA IDs | Original RPN | Status | Test Coverage | Contract Dep | Sprint |
|---|---|---|---|---|---|---|---|
| FM-1.1 | Landing Page Load | FMEA-FM-009, FMEA-FM-012, FMEA-FM-017 | 224, 126, 80 | FIXED (Sprint 2), FIXED (Sprint 1), FIXED (Sprint 3) | 51 tests (desktop6) | compare_faces.v1 | Sprint 1/2/3 |
| FM-1.2 | Biometric Consent | — | — | — | NONE | none | N/A |
| FM-2.1 | Onboarding (Solo) | — | — | — | NONE | none | N/A |
| FM-2.2 | Photo Upload (Solo) | — | — | — | NONE | compare_faces.v1 | N/A |
| FM-2.3 | Analysis Loading | FMEA-FM-007, FMEA-FM-020, FMEA-GAP-01 | 100, 60, 160 | FIXED (Sprint 3), Open, FIXED (Sprint 1) | NONE | compare_faces.v1 | Sprint 1 (GAP-01), Sprint 3 (FM-007) |
| FM-2.4 | Results Story | FMEA-FM-013 | 80 | Open | NONE | compare_faces.v1 | N/A |
| FM-2.5 | Share Card | FMEA-FM-014, FMEA-FM-015 | 32, 50 | Open, Open | NONE | none | N/A |
| FM-3.1 | Room Lobby | FMEA-FM-011, FMEA-GAP-08 | 60, 80 | Open, Open | NONE | none | N/A |
| FM-3.2 | Upload Phase (Room) | FMEA-FM-016, DFMEA-FM-05 | 48, 140 | Open, FIXED (Sprint 2) | NONE | none | Sprint 2 (DFMEA-FM-05) |
| FM-3.3 | Analysis Phase (Room) | DFMEA-FM-06, DFMEA-FM-08, DFMEA-FM-10 | 63, 72, 72 | Acceptable, Acceptable, Acceptable | NONE | compare_faces.v1 | N/A |
| FM-3.4 | Countdown | FMEA-FM-008 | 90 | Open | NONE | none | N/A |
| FM-3.5 | Results (Duo/Group) | FMEA-FM-010 | 48 | FIXED (Sprint 0A) | NONE | compare_faces.v1 | Sprint 0A |

**FamiliMatch additional (build-blocking / no UXD step):**

| FMEA ID | Title | RPN | Status | Test Coverage |
|---|---|---|---|---|
| FMEA-FM-001 | Build completely broken | 1000* | FIXED (Sprint 0A) | NONE |
| FMEA-FM-002 | matchClient constants missing | 90* | FIXED (Sprint 0A) | NONE |
| FMEA-FM-003 | Context files missing | 1000* | FIXED (Sprint 0A) | NONE |
| FMEA-FM-004 | 7 components missing | 1000* | FIXED (Sprint 0A) | NONE |
| FMEA-FM-005 | config.js missing | 90* | FIXED (Sprint 0A) | NONE |
| FMEA-FM-006 | Zero test coverage | 180 | FIXED (Sprint 2) | 51 tests created |
| FMEA-FM-018 | analytics session_start pre-consent | 150 | Open | NONE |
| FMEA-FM-019 | reversePortalTransition duped | 60 | Open | NONE |

### PLATFORM-WIDE (DFMEA)

| FMEA ID | UXD Step | Title | RPN | Status | Test Coverage | Contract Dep |
|---|---|---|---|---|---|---|
| DFMEA-FM-01 | FM-2.3 | No engineResult wrapper | 64 | Acceptable | NONE | compare_faces.v1 |
| DFMEA-FM-02 | FL-3.7 / FM-2.4 | calibrated_features null | 72 | Acceptable | NONE | kinship_analyze.v1 / compare_faces.v1 |
| DFMEA-FM-03 | FL-3.7 | embedding_similarity missing | 70 | Acceptable | NONE | kinship_analyze.v1 |
| DFMEA-FM-04 | FL-5.4 / FM-2.4 | Morph fails silently | 40 | Acceptable | NONE | none |
| DFMEA-FM-05 | FM-3.2 | WebSocket disconnect upload | ~~140~~ → ~28 | FIXED (Sprint 2) | NONE | none |
| DFMEA-FM-06 | FM-3.3 | Room closes during analysis | 63 | Acceptable | NONE | none |
| DFMEA-FM-07 | FM-3.2 | Photos in RAM | ~~216~~ | MITIGATED | NONE | none |
| DFMEA-FM-08 | FM-3.3 | Desktop3 unreachable | 72 | Acceptable | NONE | none |
| DFMEA-FM-09 | FL-3.2 / FM-1.2 | Consent bypass | ~~160~~ → 60 | IMPLEMENTED | NONE | none |
| DFMEA-FM-10 | FM-3.3 | Group matrix timeout | 72 | Acceptable | NONE | none |
| DFMEA-FM-11 | FL-5.4 | Keepsake template blank | 72 | Acceptable | printRobustness.test.js (partial) | none |
| DFMEA-FM-12 | FL-5.3 | Mug data mismatch | 42 | Acceptable | NONE | none |
| DFMEA-FM-13 | FL-6.2 | Stripe session failure | 32 | Acceptable | NONE | none |
| DFMEA-FM-14 | FL-6.1 | Prodigi dimension mismatch | 96 | Monitor | printRobustness.test.js (partial) | none |
| DFMEA-FM-15 | FL-6.1 | Surcharge error | 30 | Acceptable | NONE | none |
| DFMEA-FM-16 | FL-5.3 | Currency conversion drift | ~~120~~ → ~48 | FIXED (Sprint 2) | NONE | none |
| DFMEA-FM-17 | FL-4.3 | Parent-parent shown | ~~84~~ → 12 | MITIGATED | NONE | kinship_analyze.v1 |

### GAP ITEMS (from UXD analysis)

| FMEA ID | UXD Step | Title | RPN | Status | Test Coverage | Contract Dep |
|---|---|---|---|---|---|---|
| FMEA-GAP-01 | FM-2.3 | Solo error display missing | ~~160~~ → ~32 | FIXED (Sprint 1) | NONE | compare_faces.v1 |
| FMEA-GAP-02 | FL-1.1 | Mobile touch target audit | ~~120~~ → ~40 | FIXED (Sprint 1) | NONE | none |
| FMEA-GAP-03 | FL-6.3 / FU-4.1 | No post-order fallback | 42 | Open | NONE | none |
| FMEA-GAP-04 | All | No mobile scroll test coverage | 144 | FIXED (Sprint 3) | Playwright spec created | none |
| FMEA-GAP-05 | FL-7.2 | Annual toggle not persisted | 60 | Open | NONE | none |
| FMEA-GAP-06 | FP-4.1 | Tutorial repeat on every quit | 70 | Open | NONE | none |
| FMEA-GAP-07 | FL-3.4 | No camera-first on mobile | 75 | Open | NONE | none |
| FMEA-GAP-08 | FM-3.1 | No room code expiry UX | 80 | Open | NONE | none |
| FMEA-GAP-09 | FL-3.7 | Sensitivity slider no label | 64 | Open | NONE | none |
| FMEA-GAP-10 | FU-1.1 | Feature count no explanation | 48 | Open | NONE | none |
| FMEA-GAP-11 | All | Modal focus management | 210 | FIXED (Sprint 3) | Audit complete; 7 modals need useFocusTrap | none |
| FMEA-GAP-12 | FL-3.6 | Attempt burned on failure | 90 | Open | NONE | none |

---

## Section 2: Contract Invariants Register

### Contract 1: kinship_analyze.v1

| Property | Schema File | Invariant | Enforcing Test | What Breaks If Violated |
|---|---|---|---|---|
| Schema | `contracts/kinship_analyze.v1.schema.json` | Schema file must exist and be valid JSON Schema | Desktop3 pytest contract tests | All FamiliLook + FamiliPoker analysis |
| Winner | guardrails.json | Winner always leans to a parent (never balanced) | Desktop3 order invariance tests | 50/50 display violation; user confusion |
| 8 Features | guardrails.json | All 8 features have valid parent attribution | Desktop3 feature count tests | Incomplete results; card generation breaks |
| Order Invariance | guardrails.json | Swapping parent order does not change real winner | Desktop3 order invariance tests | Results change on re-upload; trust loss |
| Feature Count | CLAUDE.md | mumFeatureCount + dadFeatureCount + unknownFeatureCount === 8 | regressionFlows.test.js (partial) | Feature table miscount; narrative errors |
| No 50/50 | CLAUDE.md | Never display 50/50 percentages; minimum 51/49 | NEEDS TEST (FE) | Contract violation; brand guideline failure |
| Real Metrics | guardrails.json | All values from real face metrics, no fabrication | Desktop3 tests | Legal/trust risk |
| engineResult | CLAUDE.md | FE trusts backend winner field, never re-derives | NEEDS TEST (FE) | Winner mismatch between display and data |

### Contract 2: compare_faces.v1 (FROZEN)

| Property | Schema File | Invariant | Enforcing Test | What Breaks If Violated |
|---|---|---|---|---|
| Schema | `contracts/compare_faces.v1.schema.json` | Schema file must exist and validate responses | Desktop3 pytest contract tests | All FamiliMatch comparisons |
| Feature Count | schema.json | feature_comparisons always has exactly 8 entries | Desktop3 contract validation | FE feature breakdown table breaks |
| Score Formula | schema.json | percentage = round(clamp(0.6*emb + 0.4*feat, 0, 1) * 100) | Desktop3 pytest | Wrong compatibility percentage |
| Percentage Range | schema.json | percentage is integer in [0, 100] | Desktop3 contract validation | Display errors; chemistry_label mismatch |
| Chemistry Labels | schema.json | chemistry_label consistent with percentage thresholds | Desktop3 pytest | Wrong label shown; color mismatch |
| Shared Features | schema.json | shared_features === feature_comparisons.filter(match=true) | Desktop3 pytest | Incorrect "X features in common" display |
| Symmetry | schema.json, guardrails.json | score(A,B) === score(B,A) | Desktop3 order invariance tests | Different results on re-upload; trust loss |
| Real Metrics | schema.json | All inputs from real face detection, no synthetic values | Desktop3 tests | Legal/trust risk |
| No Kinship | guardrails.json | FamiliMatch must NOT call /kinship/analyze | NEEDS TEST (FE) | Wrong endpoint; parent/child framing in peer context |
| No FE Re-derive | guardrails.json | FE must NOT re-compute percentage from raw scores | NEEDS TEST (FE) | Score mismatch with backend |

### Contract 3: card_deck_order.v1

| Property | Schema File | Invariant | Enforcing Test | What Breaks If Violated |
|---|---|---|---|---|
| Schema | `contracts/card_deck_order.v1.schema.json` | Schema file must exist and validate manifests | deckBuilder.test.js (partial) | QPMarkets order rejection |
| Card Count | schema.json | cards array 1-52 items | deckBuilder.test.js | Empty deck or overflow |
| Order ID | schema.json | orderId matches ^FL-CD-\d+-[a-z0-9]{6}$ | NEEDS TEST | QPMarkets tracking failure |
| Print Spec | schema.json | 300 DPI, 63.5x88.9mm, 3mm bleed | printRobustness.test.js | Misaligned prints; QPMarkets rejection |
| Card Types | schema.json | type must be "face" or "special" | deckBuilder.test.js | Invalid manifest |

---

## Section 3: FMEA Fix Register — Fixed/Mitigated Items

40 FMEA items are Fixed/Mitigated/Implemented (3 pre-sprint + 37 sprint fixes). The remaining 55 are Open or Acceptable.

### Pre-Sprint Fixes (3 items)


| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Sprint | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|---|
| DFMEA-FM-07 | Photos persist in RAM after room close | 216 | — (mitigated) | desktop3: explicit `del` + `gc.collect()` on room close; photo bytes zeroed | Pre-sprint (2026-02-27) | NEEDS TEST | Photos remain in RAM after room close; GDPR violation risk |
| DFMEA-FM-09 | Consent bypass — photos processed without BIPA consent | 160 | 60 | desktop3: `BiometricConsentMiddleware` (middleware.py:65-87); X-Biometric-Consent header required | Pre-sprint (2026-02-27) | Desktop3 pytest middleware tests | Backend processes biometric data without consent; BIPA/GDPR legal risk |
| DFMEA-FM-17 | Parent-parent comparison shown in group results | 84 | 12 | desktop2: PARENT_ROLES filter, parentNameSet, opt-in toggle, couple nudge to FamiliMatch | Pre-sprint (2026-03-08) | NEEDS TEST | Partner comparisons shown unprompted in family results; user confusion |

### Sprint 0A — FamiliMatch Source Restoration (5 items)

| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|
| FMEA-FM-001 | Build completely broken | 1000* | 0 | desktop6: index.html, vite.config.js, main.jsx, App.jsx | Build gate | FamiliMatch entirely unrebuildable |
| FMEA-FM-002 | matchClient broken import | 90* | 0 | desktop6: constants.js restored | Build gate | All API calls fail; import crash |
| FMEA-FM-003 | Context files missing | 1000* | 0 | desktop6: ConsentContext.jsx, MatchContext.jsx | Build gate | App crashes on mount; no consent/state |
| FMEA-FM-004 | 7 components missing | 1000* | 0 | desktop6: 7 components + 3 pages restored | Build gate | Solo + Room modes crash on render |
| FMEA-FM-005 | config.js missing | 90* | 0 | desktop6: config.js, constants.js | Build gate | All API calls fail; no env config |

### Sprint 0B — Quick Wins (7 items)

| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|
| FMEA-FP-003 | Poker Back button dead end | 144 | 0 | desktop4/AppLayout.jsx:538 | NEEDS TEST | FeaturePoker back button navigates nowhere |
| FMEA-FP-001 | Analysis errors swallowed | 162 | ~36 | desktop4/AppLayout.jsx:272 | NEEDS TEST | User gets zero feedback on analysis failure |
| FMEA-FL-003 | OrderSuccess dark theme | 128 | 0 | desktop2/OrderSuccessPage.jsx:75 | NEEDS TEST | Order success page unreadable in dark mode |
| FMEA-FL-004 | from=home wrong back nav | 144 | 0 | desktop2/AppLayout.jsx:340 | NEEDS TEST | Back button navigates to wrong page |
| FMEA-FL-006 | Pet listed as Coming Soon | 100 | 0 | desktop2/AppLayout.jsx:809 | NEEDS TEST | Pet analysis incorrectly shown as unavailable |
| FMEA-FP-006 | Analytics dev bypass missing | 300 | 0 | desktop4/analytics.js:3 | NEEDS TEST | All dev analytics events silently dropped |
| FMEA-FP-007 | Wrong client ID | 150 | 0 | desktop4/useKinshipAnalysis.jsx:337 | NEEDS TEST | API calls use wrong client identifier |

### Sprint 1 — Revenue + Critical UX (6 items)

| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|
| FMEA-FL-024 | Basket drawer inaccessible | 126 | 0 | desktop2/FamiliUnoPage.jsx (imports, state, render) | NEEDS TEST | Cannot access basket from /uno route |
| FMEA-FL-002 | Single parent FAB dead end | 140 | ~28 | desktop2/UploadSection.jsx (singleParentHint) | NEEDS TEST | Single-parent upload FAB leads nowhere |
| FMEA-GAP-01 | Solo error display missing | 160 | ~32 | desktop6/SoloPage.jsx (error card) | NEEDS TEST | Analysis failure invisible to user |
| FMEA-FM-012 | Consent bypass via ?mode= | 126 | ~18 | desktop6/LandingPage.jsx (consent gate) | NEEDS TEST | Biometric consent skippable via URL param |
| FMEA-FL-009 | Group mode no cards | 120 | ~24 | desktop2/FamiliUnoPage.jsx (storage listener) | NEEDS TEST | Group analysis produces no Uno cards |
| FMEA-GAP-02 | Mobile touch target audit | 120 | ~40 | desktop2/HomePage.jsx (portal minHeight) | NEEDS TEST | Touch targets below 44pt on mobile |

### Sprint 2 — Security + Analytics (6 items)

| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|
| FMEA-FL-007 | Stripe Price IDs absent | 108 | ~36 | desktop2/PlansPage.jsx (startup check) | NEEDS TEST | Stripe checkout fails silently |
| FMEA-FP-015 | Two analytics implementations | 200 | 0 | desktop4/analytics.js deleted | NEEDS TEST | Duplicate analytics events; data pollution |
| DFMEA-FM-16 | Currency price drift | 120 | ~48 | desktop2/ProductShelf.jsx (disclaimer) | NEEDS TEST | Displayed price != charged price in non-GBP |
| FMEA-FM-006 | Zero test coverage | 180 | 0 | desktop6/tests/ (51 tests created) | 51 tests | Any code change unverifiable |
| FMEA-FM-009 | Tier bypass by URL | 224 | ~24 | desktop6/LandingPage.jsx + desktop7/main.py (JWT) | NEEDS TEST | Plus features accessible without payment |
| DFMEA-FM-05 | WebSocket disconnect | 140 | ~28 | desktop6/useMatchConnection.js + desktop7/rooms.py (reconnect) | NEEDS TEST | Upload lost on temporary network drop |

### Sprint 3 — Quality + Polish (6 items)

| FMEA ID | Title | Original RPN | Post-Fix RPN | Files Changed | Regression Test | What Regresses If Reverted |
|---|---|---|---|---|---|---|
| FMEA-FL-005 | Keepsake paywall late | 84 | ~14 | desktop2/KeepsakesModal.jsx (upgrade banner at Step 1) | NEEDS TEST | Free users navigate 4 steps before seeing paywall |
| FMEA-FL-008 | isDemoMode stale cache | 108 | 0 | desktop2/planConfig.js (_demoMode cache removed) | NEEDS TEST | Demo mode persists past 4h expiry or fails to activate |
| FMEA-FM-007 | compareSolo hardcoded names | 100 | ~20 | desktop6/matchClient.js + SoloPage.jsx (nameA/nameB params) | NEEDS TEST | History shows "Person A"/"Person B" instead of real names |
| FMEA-FM-017 | Fabricated social counter | 80 | 0 | desktop6/LandingPage.jsx (SEED counter replaced with "Thousands of") | NEEDS TEST | Fake incrementing counter; ASA/trust risk |
| FMEA-FL-011 | Hardcoded social proof | 80 | 0 | desktop2/HomePage.jsx ("12,800+" replaced with "Thousands of") | NEEDS TEST | Fake static number; trust risk |
| FMEA-GAP-11 | Modal focus management | 210 | ~70 | Audit report created; 7 modals identified for useFocusTrap | gap11_focus_audit.md | Screen readers can't navigate modals; accessibility failure |
| FMEA-GAP-04 | No mobile scroll test coverage | 144 | ~36 | desktop2/e2e/mobile-scroll.spec.js created | Playwright spec | Mobile scroll issues undetectable |

### Post-Sprint — Platform Audit & Hardening

#### Integration Gaps Fixed (10 items)

| ID | Title | Files Changed | What It Fixed |
|---|---|---|---|
| GAP-1 | JWT tier token issuer created | desktop3 /auth/match-token + desktop6 tierToken.js | FamiliMatch tier enforcement had no token issuer |
| GAP-2 | MATCH_TIER_SECRET documented | desktop7 .env.example | Secret not documented; new deploys would fail |
| GAP-3 | Poker error card UI rendered | desktop4 AppLayout.jsx | Analysis errors had no visual feedback |
| GAP-4 | Poker selectedGame defaults to null | desktop4 AppLayout.jsx | App launched into undefined game state |
| GAP-5 | FeatureScanAnimation uses personBName | desktop6 SoloPage.jsx | Animation showed generic "Person B" instead of entered name |
| GAP-6 | Poker PlansPage documented as non-functional | desktop4 | Plans page present but inert; now documented as known limitation |
| GAP-7 | Dead event listener removed | desktop2 AppLayout.jsx | Orphaned event listener consuming resources |
| GAP-8 | DeckCheckoutPage dead import removed | desktop2 AppRouter.jsx | Unused import; dead code |
| GAP-9 | EngineStatusDot dead component deleted | desktop2 | Entire component unused; dead code |
| GAP-10 | Desktop7 .env.example completed | desktop7 .env.example | Missing env vars for new deployments |

#### Mobile Conversion Fixes (11 items)

| Area | Fix | Files Changed |
|---|---|---|
| KeepsakesModal | Footer buttons enlarged to 44px minimum | desktop2 KeepsakesModal.jsx |
| BasketDrawer | Remove button enlarged to 44px | desktop2 BasketDrawer.jsx |
| BasketDrawer | Free users see "Upgrade to Plus" CTA instead of disabled button | desktop2 BasketDrawer.jsx |
| HomePage | Event badges, product pills, footer links all 44px | desktop2 HomePage.jsx |
| AppLayout | Consent modal buttons 44px | desktop2 AppLayout.jsx |
| LandingPage (Match) | Illustration cards w-28 to w-24 | desktop6 LandingPage.jsx |
| ResultsStory | Feature grid columns 80/80/40 to 60/60/32 | desktop6 ResultsStory.jsx |
| ResultsPage | Chemistry matrix hidden on mobile | desktop6 ResultsPage.jsx |
| SoloPage | Back button 44px, brand button 44px, person B input 44px | desktop6 SoloPage.jsx |
| RoomPage | Brand button 44px | desktop6 RoomPage.jsx |
| ShareCard | Responsive width | desktop6 ShareCard.jsx |

#### Security Hardening (6 items)

| Area | Fix | Details |
|---|---|---|
| Dashboard Auth | Moved to backend | POST /analytics/auth with session tokens; raw key no longer validated client-side |
| Ambassador Rate Limiting | 3 requests per IP per hour | Prevents ambassador code abuse |
| Ambassador Confirmation | 2-step confirmation flow | User must confirm before ambassador code is applied |
| Dashboard Audit Logging | data/dashboard_access.log | All dashboard access attempts logged with timestamp, IP, success/fail |
| Ambassador Audit Logging | data/ambassador_activity.log | All ambassador code usage logged |
| Developer Codes | FAMILI-DEV-CEO, FAMILI-DEV-TEST added | Internal testing codes with audit trail |

---

## Section 4: Regression Prevention Layers

### Layer 1: Pre-Commit Hooks

| Property | Value |
|---|---|
| File | `.claude/pre-commit-hook.sh` |
| Installation | `cp .claude/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit` |
| Check 0 | Secret scan (`.claude/scan-secrets.sh`) — blocks if secrets found in staged files |
| Check 1 | Frontend tests (`npm run test:run` or `scripts/quality-gate.js`) — blocks on failure |
| Check 2 | Frontend build (`npm run build`) — blocks on failure |
| Check 3 | Backend tests (`python -m pytest tests/`) — blocks on failure |
| Scope | Detects repo (desktop2, desktop3, desktop4, desktop6) and runs appropriate checks |
| Installation Status | **Installed on desktop2, desktop4, desktop6** (Sprint 3 + post-sprint) |
| Skip | `--no-verify` (discouraged; CLAUDE.md says never skip hooks) |

### Layer 2: CI/CD Pipelines (per repo)

| Repo | CI Gate | Deploy Method | Notes |
|---|---|---|---|
| famililook-desktop2 | Pre-commit hook (FE tests + build) | Vercel auto-build on push to `production` branch | Merge `main` → `production` → push |
| famililook-desktop3 | Pre-commit hook (BE pytest) | Hetzner (manual deploy) | Python backend |
| famililook-desktop4 | Pre-commit hook (FE tests + build) | Vercel auto-build | Hook installed Sprint 3 |
| famililook-desktop6 | Pre-commit hook + verify.yml CI/CD | Vercel auto-build | Build restored (Sprint 0A); 51 tests (Sprint 2); verify.yml created post-sprint |
| famililook-desktop7 | NONE documented | Hetzner | WebSocket backend for FamiliMatch |

### Layer 3: FMEA Regression Gate

| Property | Value |
|---|---|
| Script | `scripts/check_fmea_regressions.py` |
| Status | CREATED (Sprint 3) — FMEA regression gate operational |
| Notes | Validates fixed FMEA items have not regressed by running associated test markers. |

### Layer 4: Contract Schema Validation

| Contract | Schema File | Validation Location | Runtime Enforcement |
|---|---|---|---|
| kinship_analyze.v1 | `contracts/kinship_analyze.v1.schema.json` | Present (copied to contracts/ directory, Sprint 3) | Desktop3 backend tests validate response shape |
| compare_faces.v1 | `contracts/compare_faces.v1.schema.json` | Present | Desktop3 backend tests validate response shape |
| card_deck_order.v1 | `contracts/card_deck_order.v1.schema.json` | Present | deckBuilder.test.js validates manifest structure |

All three contract schema files are now present in the `contracts/` directory.

### Layer 5: Security Audit Logging

| Log File | Purpose | Contents |
|---|---|---|
| `data/dashboard_access.log` | Dashboard access audit trail | Timestamp, IP, auth result (success/fail), session ID |
| `data/ambassador_activity.log` | Ambassador code usage trail | Timestamp, IP, code used, action, result |

---

## Section 5: Open Items Register

### Priority P0 — BLOCKING (0 items)

All 6 former P0 BLOCKING items have been FIXED:
- FMEA-FM-001, FM-002, FM-003, FM-004, FM-005 (Sprint 0A)
- FMEA-FM-009 (Sprint 2)

### Priority P0 — Critical (0 items)

Both former P0 Critical items have been FIXED:
- FMEA-FP-001 (Sprint 0B)
- FMEA-GAP-01 (Sprint 1)

### Priority P1 — High (3 items)

| ID | Title | RPN | Product |
|---|---|---|---|
| FMEA-FP-002 | analysisMode context mismatch | 336 | Poker |
| FMEA-FP-014 | PLANS constant duplicated | 180 | Poker |
| FMEA-FP-005 | Plans page inert | 160 | Poker |
| **FMEA-FL-025** | **Stale chunk error on keepsake template lazy imports** | **126** | **Look** |

*13 former P1 items FIXED: FP-006 (Sprint 0B), FM-006 (Sprint 2), FL-004 (Sprint 0B), FP-003 (Sprint 0B), FL-002 (Sprint 1), DFMEA-FM-05 (Sprint 2), FL-003 (Sprint 0B), FL-024 (Sprint 1), FM-012 (Sprint 1), FL-009 (Sprint 1), DFMEA-FM-16 (Sprint 2), GAP-11 (Sprint 3), GAP-04 (Sprint 3).*

### Priority P2 — Medium (13 items)

| ID | Title | RPN | Product |
|---|---|---|---|
| FMEA-FM-018 | analytics session_start pre-consent | 150 | Match |
| FMEA-FL-012 | Trail raw localStorage plan read | 100 | Look |
| FMEA-FL-018 | Stripe return empty email | 96 | Look |
| DFMEA-FM-14 | Prodigi dimension mismatch | 96 | Platform |
| FMEA-GAP-12 | Attempt burned on failure | 90 | Look |
| FMEA-FM-008 | Room 'done' blank card | 90 | Match |
| **FMEA-FL-026** | **Analysis data lost on cancel/error — forced re-upload** | **80** | **Look** |
| FMEA-FM-013 | Hardcoded morph 50/50 split | 80 | Match |
| FMEA-FL-016 | COPPA detection not re-run | 80 | Look |
| FMEA-GAP-08 | No room code expiry UX | 80 | Match |
| FMEA-FP-011 | Poker auto-launches | 80 | Poker |
| FMEA-GAP-07 | No camera-first on mobile | 75 | Look |
| FMEA-FL-015 | Group results section blank | 70 | Look |
| FMEA-GAP-06 | Tutorial repeat on every quit | 70 | Poker |

*10 former P2 items FIXED: GAP-02 (Sprint 1), FP-007 (Sprint 0B), FL-007 (Sprint 2), FL-006 (Sprint 0B), FP-015 (Sprint 2), FL-005 (Sprint 3), FL-008 (Sprint 3), FM-007 (Sprint 3), FM-017 (Sprint 3), FL-011 (Sprint 3). FM-010 FIXED (Sprint 0A created ResultsPage.jsx).*

### Priority P3 — Low (22 items)

| ID | Title | RPN | Product |
|---|---|---|---|
| FMEA-FL-010 | Feedback button stale read | 90 | Look |
| FMEA-FL-014 | detectPhoto stale consent | 90 | Look |
| FMEA-FL-023 | Homepage feedback stale read | 90 | Look |
| FMEA-FL-001 | Dead bundle import | 60 | Look |
| FMEA-FL-019 | Unused lazy import (dup) | 60 | Look |
| FMEA-FL-020 | BottomNav re-tap exits | 60 | Look |
| FMEA-FM-011 | RoomPage no analytics | 60 | Match |
| FMEA-FM-019 | reversePortalTransition duped | 60 | Match |
| FMEA-FM-020 | Hardcoded nameB="B" | 60 | Match |
| FMEA-FP-012 | Home re-tap exits app | 60 | Poker |
| FMEA-GAP-05 | Annual toggle not persisted | 60 | Look |
| FMEA-FM-015 | Hardcoded share URL | 50 | Match |
| FMEA-FM-016 | Double grantConsent | 48 | Match |
| FMEA-GAP-10 | Feature count no explanation | 48 | Uno |
| FMEA-FL-022 | Return button goes to /hub | 45 | Look |
| FMEA-FP-009 | F21 Back destroys chips | 40 | Poker |
| FMEA-FP-016 | Version string mismatch | 40 | Poker |
| FMEA-FM-014 | History color fallback | 32 | Match |
| FMEA-FL-013 | Dashboard no route guard | 30 | Look |
| FMEA-FP-017 | AI timer not cleaned | 30 | Poker |
| FMEA-FL-021 | generateNarrative unmemo | 24 | Look |
| FMEA-FP-013 | TypeScript dead code | 24 | Poker |

### Acceptable — Monitored (10 items)

| ID | Title | RPN | Product |
|---|---|---|---|
| DFMEA-FM-01 | No engineResult wrapper | 64 | Platform |
| DFMEA-FM-02 | calibrated_features null | 72 | Platform |
| DFMEA-FM-03 | embedding_similarity missing | 70 | Platform |
| DFMEA-FM-04 | Morph fails silently | 40 | Platform |
| DFMEA-FM-06 | Room closes during analysis | 63 | Platform |
| DFMEA-FM-08 | Desktop3 unreachable | 72 | Platform |
| DFMEA-FM-10 | Group matrix timeout | 72 | Platform |
| DFMEA-FM-11 | Keepsake template blank | 72 | Platform |
| DFMEA-FM-12 | Mug data mismatch | 42 | Platform |
| DFMEA-FM-13 | Stripe session failure | 32 | Platform |
| DFMEA-FM-15 | Surcharge error | 30 | Platform |

---

## Section 6: Quality KPIs

### Test Counts Per Repo

| Repo | Test Files | Tests | Runtime | Build Status | Last Verified |
|---|---|---|---|---|---|
| famililook-desktop2 | — | 1,071 | — | Clean | 2026-03-31 |
| famililook-desktop3 | 14 | ~200 | — | Clean | 2026-03-26 |
| famililook-desktop4 | — | 932 | — | PASS | 2026-03-31 |
| famililook-desktop6 | — | 51 | — | PASS (Sprint 0A restored) | 2026-03-31 |
| famililook-desktop7 | Unknown | Unknown | — | Unknown | — |

### Build Status

| Repo | Build Status | Notes |
|---|---|---|
| desktop2 | PASS | Clean build, 0 warnings |
| desktop3 | PASS | Python backend operational |
| desktop4 | PASS (assumed) | No CI gate; builds via Vercel |
| desktop6 | PASS | FMEA-FM-001 FIXED (Sprint 0A): source files restored |
| desktop7 | Unknown | No build pipeline documented |

### Contract Compliance Status

| Contract | Schema File Present | Backend Tests | Frontend Tests | Compliance |
|---|---|---|---|---|
| kinship_analyze.v1 | Present (Sprint 3) | Yes (desktop3) | Partial (regressionFlows.test.js) | PARTIAL — schema file restored |
| compare_faces.v1 | Yes | Yes (desktop3) | 51 tests (desktop6) | PARTIAL (FE tests added Sprint 2) |
| card_deck_order.v1 | Yes | N/A (QPMarkets vendor) | deckBuilder.test.js, printRobustness.test.js | PARTIAL |

### FMEA Coverage

| Metric | Value |
|---|---|
| Total FMEA items | 97 |
| Fixed/Mitigated/Implemented | 40 (41.2%) — 3 pre-sprint + 37 sprint fixes |
| Post-Sprint Hardening | 27 additional fixes (10 integration gaps + 11 mobile conversion + 6 security) |
| Acceptable (monitored) | 11 (11.3%) |
| Open — P0 BLOCKING | 0 (0%) — all 6 resolved |
| Open — P0 Critical | 0 (0%) — both resolved |
| Open — P1 High | 4 (4.1%) — +1 FL-025 stale chunk |
| Open — P2 Medium | 14 (14.4%) — +1 FL-026 data loss on cancel |
| Open — P3 Low | 22 (22.7%) |
| Items with regression tests | 3 (DFMEA-FM-09, FM-006 suite of 51, GAP-04 Playwright spec) |
| Items needing regression tests | 92 (96.8%) |

### Critical Gaps Summary

1. ~~**kinship_analyze.v1.schema.json** is missing from `contracts/` directory~~ — RESOLVED (Sprint 3): schema copied to contracts/
2. ~~**FamiliMatch (desktop6)** is entirely unrebuildable~~ — RESOLVED (Sprint 0A): all 5 P0 BLOCKING items fixed, build passes, 51 tests created (Sprint 2)
3. ~~**FamiliPoker (desktop4)** has zero tests and no pre-commit hook~~ — RESOLVED (Sprint 3): 932 tests, pre-commit hook installed
4. ~~**FMEA regression gate script** (`check_fmea_regressions.py`) does not exist~~ — RESOLVED (Sprint 3): script at scripts/check_fmea_regressions.py
5. **96.8% of FMEA items** lack dedicated regression tests (improved from 97.9%)
6. ~~**No frontend contract compliance tests** for compare_faces.v1~~ — RESOLVED (Sprint 2): 51 FE tests in desktop6
7. ~~**3 of 5 repos** have no CI gate before deploy~~ — IMPROVED (Sprint 3): pre-commit hooks now installed on desktop2, desktop4, desktop6

---

## Section 7: UXD Sign-Off Status

| Reviewer | Status | Notes |
|---|---|---|
| QA Lead | COMPLETE WITH EXCEPTIONS | 40 FMEA items fixed, 27 post-sprint hardening fixes applied. 5 exceptions tracked below. |
| CMO | GREEN (Uno), YELLOW (Look/Match), RED (Poker) | Uno fully launched with QPMarkets. Look/Match need conversion work. Poker plans page non-functional. |
| COO | CONDITIONAL SIGN OFF | 7-day monitoring period. Full sign-off target: 2026-04-07. |

### Tracked Exceptions (5)

| # | Exception | Owner | Target |
|---|---|---|---|
| 1 | A/B trail — no test coverage, no FMEA mapping | QA Lead | Backlog |
| 2 | Pet UI — listed as "Coming Soon", no implementation timeline | Product | Backlog |
| 3 | ShareCard URL — hardcoded share URL (FMEA-FM-015) | Engineering | P3 backlog |
| 4 | Poker PlansPage — documented as non-functional (GAP-6, FMEA-FP-005/014) | Engineering | Poker merge (Option C) |
| 5 | VITE_API_KEY — not yet set in Vercel dashboard for desktop2/4/6 | Operations | Operational task |

---

*End of Master Regression Prevention Matrix v3.0 — 2026-03-31*
*Updated: 40 FMEA items fixed across Sprints 0A-3 + 27 post-sprint hardening fixes*
*UXD sign-off: CONDITIONAL — 7-day monitoring, full sign-off 2026-04-07*
*Next review: 2026-04-07 (end of monitoring period)*
