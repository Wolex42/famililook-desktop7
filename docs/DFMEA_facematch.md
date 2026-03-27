# DFMEA: Platform-Wide — Design Failure Mode and Effects Analysis

**Document ID**: DFMEA-FM-002
**Feature**: Full platform including FamiliMatch modes, commerce layer, keepsake templates, and order flow
**Date**: 2026-03-07 (updated from 2026-02-23)
**Author**: Claude Code (automated governance)
**Status**: CURRENT — Investor-ready audit (March 2026)

---

## 1. Scope and Objective

This Design Failure Mode and Effects Analysis (DFMEA) identifies potential failure modes across the FamiliLook platform: FamiliMatch compatibility analysis, keepsake template rendering, commerce/checkout flow, Prodigi print fulfilment, and family data aggregation.

**Objective**: Ensure facial comparison, keepsake production, payment processing, and order fulfilment produce correct, safe, and privacy-compliant results.

---

## 2. System Boundary Diagram

```
[desktop6 — React SPA]
    |
    |-- Solo Mode -------> [desktop3 /kinship/analyze] ---> analysis results
    |                       [desktop3 /face/morph]     ---> fusion image
    |
    |-- Duo/Group Mode --> [desktop7 WebSocket server]
    |                           |
    |                           +-- rooms.py (RAM dict) stores photos + state
    |                           +-- desktop3_client.py --> [desktop3 /kinship/analyze]
    |                           +-- comparison.py     --> pairwise matrix
    |                           +-- desktop3_client.py --> [desktop3 /face/morph]
    |                           |
    |                           +-- Broadcasts results to all room players
    |                           +-- Room close --> ALL data deleted from RAM
    |
    +-- ConsentContext.jsx  --> BIPA consent gate (blocks all features until accepted)
    +-- matchClient.js      --> API client (Solo mode)
    +-- useMatchConnection.js --> WebSocket client (Duo/Group mode)
```

---

## 3. DFMEA Table

### Rating Scale

| Rating | Severity (S) | Occurrence (O) | Detection (D) |
|--------|-------------|----------------|----------------|
| 1 | No effect | Almost impossible | Almost certain to detect |
| 2-3 | Minor annoyance | Remote | High chance of detection |
| 4-5 | Moderate, user notices | Low | Moderate detection |
| 6-7 | Significant, affects UX | Moderate | Low detection |
| 8-9 | Critical, feature broken | High | Very low detection |
| 10 | Safety/data loss | Very high | No detection |

**RPN Threshold**: S x O x D <= 100 (acceptable). Above 100 = action required.

---

### FM-01: `/kinship/analyze` returns no `engineResult` wrapper

| Attribute | Value |
|-----------|-------|
| **Function** | Parse backend analysis response in matchClient.js |
| **Failure Mode** | Backend returns flat response (no `engineResult` key) — e.g., if request hits `routes/kinship.py` instead of `main.py` handler |
| **Effect** | `engine` variable = full response (wrong shape), `parents` = undefined, all features show "Unknown", score = 0% |
| **Cause** | Route registration order change in main.py, or backend downgrade/refactor |
| **Severity** | 8 |
| **Occurrence** | 2 (route order is stable, tested) |
| **Detection** | 4 (fallback `analysis.engineResult || analysis` handles flat responses, but field paths still fail) |
| **RPN** | **64** |
| **Current Controls** | Defensive fallback: `const engine = analysis.engineResult || analysis` (matchClient.js:127). Tests mock actual response shape. |
| **Recommended Action** | Add response shape validation — check for `parents.parent1` existence before proceeding |
| **Test Coverage** | `matchClient.test.js`: 7 tests covering response parsing |

---

### FM-02: `calibrated_features` null/empty on parent objects

| Attribute | Value |
|-----------|-------|
| **Function** | Extract feature labels for comparison display |
| **Failure Mode** | `parent1.calibrated_features` or `parent2.calibrated_features` is null, undefined, or empty object |
| **Effect** | All feature comparisons show "Unknown" vs "Unknown", all marked as non-matching. Feature similarity = 0% |
| **Cause** | Backend face detection fails (no face found), low-quality photo, or backend model loading failure |
| **Severity** | 6 |
| **Occurrence** | 4 (poor quality photos are common in user uploads) |
| **Detection** | 3 (labels default to "Unknown" — visible to user, but not an error state) |
| **RPN** | **72** |
| **Current Controls** | `extractLabels()` (matchClient.js:95-105) returns empty object for null input. Comparisons use "Unknown" fallback. |
| **Recommended Action** | Show user-friendly "Face not detected clearly" message instead of showing all "Unknown" |
| **Test Coverage** | `matchClient.test.js`: extractLabels tested with null input |

---

### FM-03: `embedding_similarity_parent2` missing or 0

| Attribute | Value |
|-----------|-------|
| **Function** | Compute compatibility percentage from facial embeddings |
| **Failure Mode** | `child.embedding_similarity_parent2` is undefined, null, or 0 |
| **Effect** | Compatibility shows 0% — "Opposites Attract" label. User sees minimum score regardless of actual similarity. |
| **Cause** | Backend fails to compute embeddings (model error), or child object malformed |
| **Severity** | 7 |
| **Occurrence** | 2 (backend embedding pipeline is well-tested) |
| **Detection** | 5 (0% score is technically valid — hard to distinguish from real 0%) |
| **RPN** | **70** |
| **Current Controls** | Nullish coalescing: `child.embedding_similarity_parent2 ?? 0` (matchClient.js:139). All chemistry labels are positive ("Opposites Attract" for low scores). |
| **Recommended Action** | If embedding_similarity is exactly 0 AND calibrated_features are also empty, show "Analysis incomplete" instead of a score |
| **Test Coverage** | `matchClient.test.js`: percentage calculation tested (expects 68 from mock) |

---

### FM-04: Face morph fails silently (catch returns null)

| Attribute | Value |
|-----------|-------|
| **Function** | Create face fusion blend via `/face/morph` |
| **Failure Mode** | `createMorph()` catches error and returns null — no morph image displayed |
| **Effect** | Fusion reveal section is empty/hidden. Core "wow" feature missing. |
| **Cause** | Backend morph endpoint down, face not detected, Delaunay triangulation fails on unusual face angles |
| **Severity** | 5 |
| **Occurrence** | 4 (morph is fragile — requires good face alignment) |
| **Detection** | 2 (console.warn logged, UI can check for null fusion_image) |
| **RPN** | **40** |
| **Current Controls** | try/catch in `createMorph()` (matchClient.js:70-89), `console.warn('[morph] Failed:', err.message)`. Morph is treated as bonus feature — comparison results shown regardless. |
| **Recommended Action** | None (RPN acceptable). Morph failure doesn't block core comparison. |
| **Test Coverage** | `matchClient.test.js`: morph failure test (returns null, doesn't throw) |

---

### FM-05: WebSocket disconnect during photo upload (Duo/Group)

| Attribute | Value |
|-----------|-------|
| **Function** | Transmit player's photo to desktop7 via WebSocket |
| **Failure Mode** | WebSocket connection drops mid-upload — photo data partially received or lost |
| **Effect** | Player appears "not ready" to other players. Room stuck waiting. |
| **Cause** | Mobile network switch (WiFi → cellular), browser tab backgrounded, server restart |
| **Severity** | 7 |
| **Occurrence** | 5 (mobile network instability is common) |
| **Detection** | 4 (WebSocket `onclose` event fires, but reconnection may not restore upload state) |
| **RPN** | **140** |
| **Current Controls** | `useMatchConnection.js` handles WebSocket lifecycle events. Desktop7 has room timeout for inactive rooms. |
| **Recommended Action** | **ACTION REQUIRED (RPN > 100)**: Implement auto-reconnection with room rejoin. On reconnect, check if photo was received (server ack). If not, re-prompt upload. |
| **Test Coverage** | `useMatchConnection.test.js`: connection lifecycle tests |

---

### FM-06: Room closes before analysis completes (Duo/Group)

| Attribute | Value |
|-----------|-------|
| **Function** | Room lifecycle management in desktop7 |
| **Failure Mode** | Host disconnects or room timeout triggers while desktop3 is still processing comparison |
| **Effect** | Analysis results lost. Players see no results. Desktop3 CPU wasted on abandoned computation. |
| **Cause** | Host closes browser, network timeout, room inactivity timer fires during slow desktop3 response |
| **Severity** | 7 |
| **Occurrence** | 3 (inactivity timeout should be long enough for analysis) |
| **Detection** | 3 (room close event logged, but results are already lost) |
| **RPN** | **63** |
| **Current Controls** | Room timeout is set longer than expected analysis time. Desktop7 awaits desktop3 response before closing. |
| **Recommended Action** | Extend room timeout during active analysis. Add "analysis in progress" state that prevents room cleanup. |
| **Test Coverage** | `test_rooms.py`: room lifecycle tests (111 tests total) |

---

### FM-07: Photos persist in RAM after room close

| Attribute | Value |
|-----------|-------|
| **Function** | Clean up room data on room close |
| **Failure Mode** | Room dict removed but photo bytes remain referenced elsewhere (e.g., in a pending desktop3 request closure, or Python garbage collector delay) |
| **Effect** | BIPA violation — photos exist in server memory beyond declared retention period |
| **Cause** | Python reference counting doesn't immediately free large byte arrays, or an open HTTP request to desktop3 holds a reference |
| **Severity** | 9 |
| **Occurrence** | 3 (Python GC is non-deterministic for large objects) |
| **Detection** | 8 (no monitoring of memory contents — would require memory profiling) |
| **RPN** | **216** |
| **Current Controls** | Room close deletes room dict. Python GC eventually frees unreferenced objects. |
| **Recommended Action** | **ACTION REQUIRED (RPN > 100)**: Explicitly `del` photo byte references and call `gc.collect()` on room close. Add memory monitoring/logging for photo lifecycle. Consider zeroing byte arrays before deletion. |
| **Test Coverage** | `test_rooms.py`: room cleanup tests verify dict removal |

---

### FM-08: Desktop3 unreachable from desktop7

| Attribute | Value |
|-----------|-------|
| **Function** | desktop7 calls desktop3 `/kinship/analyze` and `/face/morph` for comparison |
| **Failure Mode** | desktop3 is down, overloaded, or network partition between containers |
| **Effect** | Duo/Group rooms collect photos but cannot produce results. Players wait indefinitely. |
| **Cause** | desktop3 container crashed, ML model OOM, Docker network issue |
| **Severity** | 8 |
| **Occurrence** | 3 (single VPS, containers generally stable) |
| **Detection** | 3 (desktop7 gets HTTP error/timeout, can report to players) |
| **RPN** | **72** |
| **Current Controls** | `desktop3_client.py` has timeout and error handling. Desktop7 can report "analysis failed" to room players. |
| **Recommended Action** | Add health check endpoint on desktop3. Desktop7 checks health before accepting room creation. Show "service temporarily unavailable" if desktop3 is down. |
| **Test Coverage** | `test_desktop3_client.py`: error handling tests |

---

### FM-09: Consent bypass — photo upload without BIPA consent

| Attribute | Value |
|-----------|-------|
| **Function** | Gate all facial analysis behind BIPA consent |
| **Failure Mode** | User bypasses consent modal by calling API directly (curl, browser dev tools) or by manipulating React state |
| **Effect** | Photos processed without consent — BIPA violation ($5K/person statutory damages) |
| **Cause** | Consent check is frontend-only (ConsentContext.jsx). No server-side consent validation. |
| **Severity** | 10 |
| **Occurrence** | 2 (requires technical skill to bypass) |
| **Detection** | 3 (server-side `BiometricConsentMiddleware` at middleware.py:65-87 rejects requests missing `X-Biometric-Consent` header) |
| **RPN** | **60** |
| **Current Controls** | `ConsentContext.jsx` blocks all UI functionality until consent accepted. `BiometricConsentMiddleware` (middleware.py:65-87) enforces server-side consent by rejecting requests without `X-Biometric-Consent` header. |
| **Recommended Action** | None (RPN acceptable after server-side enforcement). |
| **Test Coverage** | `ConsentContext.test.jsx`: 12 tests for consent flow |

---

### FM-10: Group matrix computation fails for 6 players

| Attribute | Value |
|-----------|-------|
| **Function** | Compute pairwise comparison matrix for N players |
| **Failure Mode** | 6 players = 15 pairwise comparisons = 15 `/kinship/analyze` + 15 `/face/morph` calls. desktop3 CPU saturation causes timeouts. |
| **Effect** | Partial results (some pairs compared, others timeout). Inconsistent matrix. |
| **Cause** | 30 sequential API calls to desktop3 on a 2-vCPU server. Each takes ~2-5 seconds. Total: 60-150 seconds. |
| **Severity** | 6 |
| **Occurrence** | 4 (6-player rooms are expected use case) |
| **Detection** | 3 (timeout errors logged, partial results detectable) |
| **RPN** | **72** |
| **Current Controls** | `comparison.py` processes pairs sequentially. Timeout per request. Results collected as they arrive. |
| **Recommended Action** | Implement batched/parallel comparison (2-3 concurrent desktop3 calls). Add progress indicator showing "X of 15 comparisons complete." Consider limiting group size to 4 (6 pairs) for initial launch. |
| **Test Coverage** | `test_comparison.py`: pairwise matrix tests for 2, 3, and 6 players |

---

### FM-11: Keepsake template renders blank or misaligned for print

| Attribute | Value |
|-----------|-------|
| **Function** | Render keepsake template (mug, certificate, card) as PNG for Prodigi |
| **Failure Mode** | Template renders with missing data (null child name, no photo, broken layout) producing a blank or corrupt PNG |
| **Effect** | Customer receives a printed product with missing text, blank areas, or garbled layout. Refund required. |
| **Cause** | `useKeepsakeData()` or `useFamilyKeepsakeData()` returns null/partial data; `printExport.js` html2canvas fails on complex CSS; template dimensions mismatch print profile |
| **Severity** | 8 |
| **Occurrence** | 3 (templates tested with sample data, but edge cases with unusual names/photos possible) |
| **Detection** | 3 (user sees preview in KeepsakesModal before ordering; printExport generates visible PNG) |
| **RPN** | **72** |
| **Current Controls** | KeepsakesModal shows live preview. Templates have null guards (`child?.name || "Child"`). Print profiles define exact pixel dimensions matching template CSS. |
| **Recommended Action** | Add automated visual regression tests for all template variants. Validate PNG dimensions before upload to Prodigi. |

---

### FM-12: Family Mug Set data aggregation mismatches child count

| Attribute | Value |
|-----------|-------|
| **Function** | Aggregate ALL children's analysis results for Family Mug Set template |
| **Failure Mode** | `useFamilyKeepsakeData()` returns fewer children than analysed (e.g., 2 of 3 children) due to missing `analysisResults.children[idx]` entries |
| **Effect** | Mug shows incomplete family — missing child. Customer disappointment. |
| **Cause** | Analysis cancelled mid-way, partial results in context, child added after analysis completed |
| **Severity** | 7 |
| **Occurrence** | 2 (aggregation maps by index, matching children[] and analysisResults.children[] arrays) |
| **Detection** | 3 (preview shows all children — user would notice missing child) |
| **RPN** | **42** |
| **Current Controls** | `useFamilyKeepsakeData()` filters null entries (`.filter(Boolean)`). Returns null if no valid children. Preview renders all children visually. |
| **Recommended Action** | None (RPN acceptable). Preview provides user verification gate. |

---

### FM-13: Stripe checkout session creation fails

| Attribute | Value |
|-----------|-------|
| **Function** | Create Stripe checkout session for keepsake/basket purchase |
| **Failure Mode** | `POST /payments/create-basket-checkout` or `POST /payments/create-checkout-session` returns 500 error |
| **Effect** | Customer cannot complete purchase. Revenue lost. Frustration. |
| **Cause** | Stripe API key invalid/expired, Stripe API down, payload validation error, missing product price in server catalogue |
| **Severity** | 8 |
| **Occurrence** | 2 (Stripe is reliable; key rotation is the main risk) |
| **Detection** | 2 (error shown in UI immediately; customer reports failure) |
| **RPN** | **32** |
| **Current Controls** | Backend returns error response with message. Frontend shows toast notification. Stripe dashboard monitors failed sessions. |
| **Recommended Action** | None (RPN acceptable). Monitor Stripe webhook for recurring failures. |

---

### FM-14: Prodigi order rejected — invalid image dimensions or format

| Attribute | Value |
|-----------|-------|
| **Function** | Submit keepsake order to Prodigi print API |
| **Failure Mode** | Prodigi rejects order because image is wrong size, wrong format (not JPG/PNG/PDF), or too low resolution |
| **Effect** | Order stuck in "pending" — customer pays but product not printed. Manual intervention needed. |
| **Cause** | `printExport.js` generates PNG at wrong DPI; `printProfiles.js` dimensions don't match Prodigi SKU requirements; image upload fails |
| **Severity** | 8 |
| **Occurrence** | 3 (image dimensions verified against Prodigi specs, but new products may have mismatches) |
| **Detection** | 4 (Prodigi validates on creation; webhook reports status — but delay before detection) |
| **RPN** | **96** |
| **Current Controls** | `printProfiles.js` has exact pixel dimensions per product. `printExport.js` outputs PNG (accepted format). Prodigi webhook reports order status changes. Verified SKUs documented in MEMORY.md. |
| **Recommended Action** | Add pre-submission dimension validation (compare generated PNG against printProfile expected pixels). Log all Prodigi rejection reasons. |

---

### FM-15: Personalised message surcharge not applied correctly

| Attribute | Value |
|-----------|-------|
| **Function** | Add 1.99 surcharge for personalised LLM message on keepsake |
| **Failure Mode** | Surcharge applied when message is empty, or not applied when message exists |
| **Effect** | Customer overcharged (complaint) or undercharged (revenue loss) |
| **Cause** | `hasPersonalisedMessage` flag out of sync between FE and BE; basket item metadata incorrect |
| **Severity** | 5 |
| **Occurrence** | 2 (flag is a simple boolean, straightforward logic) |
| **Detection** | 3 (customer sees line items in Stripe checkout; surcharge is visible) |
| **RPN** | **30** |
| **Current Controls** | Backend validates `hasPersonalisedMessage` flag and adds separate Stripe line_item. Customer sees breakdown at checkout. |
| **Recommended Action** | None (RPN acceptable). |

---

### FM-16: Currency conversion shows incorrect price to customer

| Attribute | Value |
|-----------|-------|
| **Function** | Display product prices in customer's local currency |
| **Failure Mode** | Hardcoded exchange rates in `CurrencyContext.jsx` diverge significantly from real rates, showing misleading prices |
| **Effect** | Customer expects one price, Stripe charges different amount (Adaptive Pricing converts from GBP). Complaint or chargeback. |
| **Cause** | Rates hardcoded at ~March 2026 values; no auto-update mechanism; currency fluctuation |
| **Severity** | 6 |
| **Occurrence** | 4 (exchange rates fluctuate daily; hardcoded rates will drift) |
| **Detection** | 5 (difference only visible at Stripe checkout — may be subtle) |
| **RPN** | **120** |
| **Current Controls** | Prices displayed with "approx" qualifier. Stripe Adaptive Pricing handles actual conversion at checkout. |
| **Recommended Action** | **ACTION REQUIRED (RPN > 100)**: Either (a) fetch live rates from a free API (e.g. exchangerate.host) periodically, or (b) add prominent "prices shown are approximate — final amount at checkout" disclaimer, or (c) show GBP only with "converted at checkout" note. |

---

### FM-17: Parent-parent comparison shown in family/group results

| Attribute | Value |
|-----------|-------|
| **Function** | Display pairwise kinship links in group snapshot results |
| **Failure Mode** | Husband/wife or partner pair included in pairwise comparison results, scoring them against each other as if they share inherited traits |
| **Effect** | Social discomfort — users report finding it "wrong" or "creepy" to see spouse-vs-spouse kinship scores. Product trust eroded. Complaints received. |
| **Cause** | Group snapshot generates all N×(N-1)/2 pairwise links including parent-parent pairs. No role-aware filtering existed. |
| **Severity** | 6 |
| **Occurrence** | 7 (any family group with 2+ parents triggers this — extremely common use case) |
| **Detection** | 2 (results are immediately visible to user — complaint is the detection mechanism) |
| **RPN** | **84** → **12** (after mitigation) |
| **Current Controls** | **MITIGATED (2026-03-08)**: `PARENT_ROLES` set + `parentNameSet` filter in GroupSnapshotSection.jsx excludes parent-parent pairs by default. Label gate requires parent tagging before results shown. Opt-in toggle allows users to include parent pairs if desired. UploadSection nudges couples (2 parents, 0 children) to FamiliMatch instead. |
| **Post-mitigation** | S=6, O=1 (opt-in only), D=2 → RPN **12** |
| **Test Coverage** | Manual verification — label gate blocks results until parents tagged; toggle controls pair visibility |

---

## 4. RPN Summary

| ID | Failure Mode | S | O | D | RPN | Status |
|----|-------------|---|---|---|-----|--------|
| FM-01 | No `engineResult` wrapper in response | 8 | 2 | 4 | 64 | Acceptable |
| FM-02 | `calibrated_features` null/empty | 6 | 4 | 3 | 72 | Acceptable |
| FM-03 | `embedding_similarity_parent2` missing | 7 | 2 | 5 | 70 | Acceptable |
| FM-04 | Face morph fails silently | 5 | 4 | 2 | 40 | Acceptable |
| **FM-05** | **WebSocket disconnect during upload** | **7** | **5** | **4** | **140** | **ACTION REQUIRED** |
| FM-06 | Room closes during analysis | 7 | 3 | 3 | 63 | Acceptable |
| FM-07 | ~~Photos persist in RAM after close~~ | 9 | 3 | 8 | ~~216~~ | **MITIGATED** (2026-02-27) — gc.collect + zero-fill |
| FM-08 | Desktop3 unreachable | 8 | 3 | 3 | 72 | Acceptable |
| FM-09 | ~~Consent bypass (frontend-only)~~ | 10 | 2 | 3 | ~~160~~ **60** | **IMPLEMENTED** (BiometricConsentMiddleware) |
| FM-10 | Group matrix computation timeout | 6 | 4 | 3 | 72 | Acceptable |
| FM-11 | Keepsake template renders blank | 8 | 3 | 3 | 72 | Acceptable |
| FM-12 | Family Mug data aggregation mismatch | 7 | 2 | 3 | 42 | Acceptable |
| FM-13 | Stripe checkout creation fails | 8 | 2 | 2 | 32 | Acceptable |
| FM-14 | Prodigi rejects image dimensions | 8 | 3 | 4 | 96 | Acceptable (monitor) |
| FM-15 | Personalised message surcharge error | 5 | 2 | 3 | 30 | Acceptable |
| **FM-16** | **Currency conversion price drift** | **6** | **4** | **5** | **120** | **ACTION REQUIRED** |
| FM-17 | ~~Parent-parent comparison shown~~ | 6 | ~~7~~ 1 | 2 | ~~84~~ **12** | **MITIGATED** (2026-03-08) — couple gate + label gate |

### Action Items (RPN > 100)

| Priority | FM | Action | Owner | Status |
|----------|-----|--------|-------|--------|
| P0 | FM-09 | Add server-side consent validation (consent token or header) | Dev | **DONE** — `BiometricConsentMiddleware` (middleware.py:65-87) rejects requests without `X-Biometric-Consent` header |
| P1 | FM-07 | Explicit photo byte deletion + `gc.collect()` on room close | Dev | **DONE (2026-02-27)** |
| P1 | FM-05 | Auto-reconnection with room rejoin + upload retry | Dev | NOT STARTED |
| P1 | FM-16 | Add currency disclaimer or live rate fetching | Dev | NOT STARTED |

---

## 5. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Claude Code | 2026-02-23 | — |
| Updated | Claude Code | 2026-03-07 | — (commerce + keepsake failure modes FM-11 to FM-16 added) |
| Reviewer | — | — | — |
| Approver | — | — | — |
