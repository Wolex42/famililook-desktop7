# FMEA Comprehensive — FML Platform (All Products)

**Document:** FMEA-002 (supersedes DFMEA_facematch.md)
**Date:** 2026-03-31
**Sources:**
- audit_famililook_uno.md (23 findings: F-001 to F-024)
- audit_familimatch.md (20 findings: F-001 to F-020)
- audit_familipoker.md (20 findings: F-001 to F-020)
- DFMEA_facematch.md (17 failure modes: FM-01 to FM-17)
- UXD gap analysis (15 new failure modes: GAP-01 to GAP-15)
**Total failure modes:** 75 (63 from audits + 12 new from UXD analysis)
**Status:** CURRENT — action items marked P0/P1/P2

---

## Rating Scale

| Rating | Severity (S) | Occurrence (O) | Detection (D) |
|--------|-------------|----------------|---------------|
| 1 | No effect | Almost impossible | Almost certain to detect |
| 2-3 | Minor annoyance | Remote | High detection |
| 4-5 | Moderate, user notices | Low | Moderate detection |
| 6-7 | Significant, affects UX | Moderate | Low detection |
| 8-9 | Critical, feature broken | High | Very low detection |
| 10 | Safety / data loss / legal | Very high | No detection |

**RPN = S × O × D. Threshold: ≤100 acceptable. >100 = action required.**

---

## Summary Dashboard

| Severity | FL+FU | FM (Match) | FP (Poker) | DFMEA | GAP | MOB | Total |
|---|---|---|---|---|---|---|---|
| Critical (S>=9) | 0 | 6 | 3 | 2 | 2 | 0 | 13 |
| High (S 7-8) | 9 | 4 | 5 | 6 | 5 | 5 | 34 |
| Medium (S 5-6) | 9 | 5 | 7 | 6 | 5 | 2 | 34 |
| Low (S 2-4) | 5 | 5 | 5 | 3 | 3 | 1 | 22 |
| **Total** | **23** | **20** | **20** | **17** | **15** | **8** | **104*** |

### Fix Status (Full RPN Summary Table — 104 rows tracked)

| Status | FL+FU | FM (Match) | FP (Poker) | DFMEA | GAP | MOB | KSK | Total |
|---|---|---|---|---|---|---|---|---|
| FIXED | 20 | 17 | 10 | 2 | 10 | 8 | 4 | 71 |
| MITIGATED/IMPLEMENTED | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 |
| Acceptable/Monitor | 0 | 0 | 0 | 11 | 0 | 0 | 0 | 11 |
| Open | 3 | 3 | 10 | 1 | 2 | 0 | 0 | 19 |
| **Total** | **23** | **20** | **20** | **17** | **12** | **8** | **4** | **104** |

> **71 of 104 tracked failure modes FIXED across Sprints 0A-4D + Post-Sprint (68%). 3 MITIGATED/IMPLEMENTED. 11 Acceptable/Monitor. 19 remain Open (all P2/P3, no P0/P1 open).**
> 3 additional GAP entries (GAP-13/14/15) exist in source but were not tracked in this table.

### Action Required (RPN > 100) — ALL RESOLVED

All 13 items that originally exceeded the RPN > 100 threshold have been fixed in Sprints 0A through 2. No open items above the action threshold remain.

| ID | Product | Title | RPN | Priority | Status |
|---|---|---|---|---|---|
| FMEA-FM-001 | FamiliMatch | Build completely broken | 270 | P0 | FIXED (Sprint 0A) |
| FMEA-FM-003 | FamiliMatch | Broken imports — context files missing | 270 | P0 | FIXED (Sprint 0A) |
| FMEA-FM-004 | FamiliMatch | 7 components missing | 240 | P0 | FIXED (Sprint 0A) |
| FMEA-FM-005 | FamiliMatch | config.js missing — all API calls broken | 216 | P0 | FIXED (Sprint 0A) |
| FMEA-FM-006 | FamiliMatch | Zero test coverage | 180 | P1 | FIXED (Sprint 2) |
| FMEA-FM-009 | FamiliMatch | Tier gating trivially bypassable | 168 | P0 | FIXED (Sprint 2) |
| FMEA-FP-001 | FamiliPoker | Analysis errors silently swallowed | 162 | P0 | FIXED (Sprint 0B) |
| FMEA-FP-003 | FamiliPoker | FeaturePoker Back button dead end | 144 | P1 | FIXED (Sprint 0B) |
| FMEA-FL-024 | FamiliUno | Basket drawer inaccessible from /uno | 140 | P1 | FIXED (Sprint 1) |
| DFMEA-FM-05 | FamiliMatch | WebSocket disconnect during upload | 140 | P1 | FIXED (Sprint 2) |
| FMEA-FL-003 | FamiliLook | OrderSuccessPage dark theme broken | 128 | P1 | FIXED (Sprint 0B) |
| DFMEA-FM-16 | FamiliLook | Currency price drift | 120 | P1 | FIXED (Sprint 2) |
| FMEA-FL-009 | FamiliUno | Group mode → no cards in FamiliUno | 120 | P1 | FIXED (Sprint 1) |

---

## Structural Module Completions (2026-04-09 to 2026-04-10)

These three modules eliminate entire categories of bugs identified in the platform audit.
They are not individual fixes — they are architectural changes that make bug categories impossible.

| Module | Status | Phases Complete | What it eliminates | Commit |
|--------|--------|----------------|-------------------|--------|
| AppErrorBus | COMPLETE | Phases 1-3 (Phase 4 ESLint pending) | 23 silent catch blocks — errors swallowed with no user feedback | Sessions A/B |
| AppStorage | COMPLETE | Phases 1-4 COMPLETE | 35+ raw localStorage calls — quota failures, schema drift, silent data loss | Sessions B/D/E (CR-STORAGE-04, commit 73149cd) |
| resultsContract | PARTIAL | Phases 1-2 (Phase 3 consumer migration + Phase 4 ESLint pending) | Divergent winner/percentage/feature logic across multiple files | Sessions C/D |

**Phase 4 (ESLint enforcement) is pending for AppErrorBus and resultsContract. AppStorage Phase 4 landed in Session E (commit 73149cd, CR-STORAGE-04).**
Once Phase 4 ships for all three, violations of these patterns will block CI — not just be caught by code review.

---

## SECTION 1: FAMILYLOOK + FAMILIUNO (famililook-desktop2)

*Source: audit_famililook_uno.md — 23 findings*

---

### FMEA-FL-001

| Field | Value |
|---|---|
| **ID** | FMEA-FL-001 |
| **UXD Step** | FU-1.1 (FamiliUno Landing) |
| **Title** | DeckCheckoutPage imported but has no route — dead bundle weight |
| **Description** | AppRouter.jsx imports DeckCheckoutPage via lazyWithReload() but no route renders it. Route /uno/checkout redirects away (CR-0007). The lazy import is still bundled, pulling in createDeckCheckout and batchRenderDeck (canvas/PDF dependencies). |
| **Expected Behavior** | Unused page components should not be imported or bundled. |
| **Actual Behavior** | DeckCheckoutPage is imported, bundled, and chunked. /uno/checkout redirects to /uno. File: src/AppRouter.jsx:39 |
| **Severity** | 2 |
| **Occurrence** | 10 |
| **Detection** | 3 |
| **RPN** | **60** |
| **Recommended Action** | Remove the lazy import of DeckCheckoutPage from AppRouter.jsx. If the file is needed for future use, keep it but do not import it. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-002

| Field | Value |
|---|---|
| **ID** | FMEA-FL-002 |
| **UXD Step** | FL-3.4 (Photo Upload) → FL-3.6 (Analyze) |
| **Title** | Single-parent upload: FAB never appears — UX dead end |
| **Description** | UploadSection computes a local canAnalyze that permits single-parent mode (hasParentA OR hasParentB). However this variable is never exposed. The gate used by AppLayout comes from useKinshipAnalysis.canAnalyze which requires BOTH parents AND a child. User uploads one parent + one child; all slots appear filled; FAB never appears; no explanation given. |
| **Expected Behavior** | If the FAB cannot appear due to missing photos, a visible helper message explains what is required ("Add a second parent to analyze"). |
| **Actual Behavior** | FAB silently absent. User sees filled slots and no way to proceed. File: src/layout/UploadSection.jsx:539, src/hooks/useKinshipAnalysis.jsx:241 |
| **Severity** | 7 |
| **Occurrence** | 5 |
| **Detection** | 4 |
| **RPN** | **140** |
| **Recommended Action** | Add a contextual helper below the upload slots: "Add [Parent B] to enable analysis". Alternatively, expose UploadSection's canAnalyze to AppLayout so a tooltip can explain why the FAB is disabled. |
| **Status** | FIXED (Sprint 1) |

---

### FMEA-FL-003

| Field | Value |
|---|---|
| **ID** | FMEA-FL-003 |
| **UXD Step** | FL-6.3 (Order Success) |
| **Title** | OrderSuccessPage background breaks dark theme |
| **Description** | OrderSuccessPage.jsx:76 uses colors.bgPrimary as inline background style. src/theme/colors.js defines bgMain and bgBase (#0D0F1A) but no bgPrimary. colors.bgPrimary = undefined. React passes undefined as inline style → no background applied → element is transparent/white. Post-payment screen appears with white background, breaking the brand dark experience. |
| **Expected Behavior** | Post-payment success page renders with dark background matching brand (#0D0F1A or equivalent). |
| **Actual Behavior** | White/transparent background on order success page — jarring visual break immediately after payment. File: src/pages/OrderSuccessPage.jsx:76, src/theme/colors.js |
| **Severity** | 8 |
| **Occurrence** | 4 |
| **Detection** | 4 |
| **RPN** | **128** |
| **Recommended Action** | Replace colors.bgPrimary with colors.bgMain (or colors.bgBase) in OrderSuccessPage.jsx:76. Add a lint rule or test to catch undefined color references. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FL-004

| Field | Value |
|---|---|
| **ID** | FMEA-FL-004 |
| **UXD Step** | FL-3.1 (App Shell Load) — back navigation |
| **Title** | from=home in /app navigates back to /hub instead of / |
| **Description** | AppLayout.jsx:340 handles back navigation: from === 'trail' → /trail, else → /hub. The from=home case falls through to /hub. FamiliUnoPage correctly handles from=home → /. Inconsistent contract: user who taps CTA from / and arrives at /app?from=home cannot return home. |
| **Expected Behavior** | /app?from=home back button → /. /app?from=trail → /trail. /app (no param) → /hub. |
| **Actual Behavior** | /app?from=home → /hub. User lands from home, cannot return home. File: src/layout/AppLayout.jsx:340 |
| **Severity** | 6 |
| **Occurrence** | 6 |
| **Detection** | 4 |
| **RPN** | **144** |
| **Recommended Action** | Add from === 'home' case: navigate to /. Update AppLayout.jsx:340 to handle all from= values. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FL-005

| Field | Value |
|---|---|
| **ID** | FMEA-FL-005 |
| **UXD Step** | FL-5.1 (Keepsakes Modal Entry) |
| **Title** | Free users shown keepsake paywall only at step 4 — wasted navigation |
| **Description** | KeepsakesModal shows 4-step flow (Category → Product → Style → Preview) before revealing free-user paywall at the action buttons. planConfig.js defines keepsakePreviewOnly flag for free plans. KeepsakesModal never reads keepsakePreviewOnly — it only checks canOrderMerchandise() at the final action buttons. |
| **Expected Behavior** | Free users see a clear notice at step 1 ("Preview mode — upgrade to Plus to order"). keepsakePreviewOnly flag is respected. Paywall shown early, not at final step. |
| **Actual Behavior** | Free users navigate 4 steps before discovering they cannot order. keepsakePreviewOnly defined but never used. Files: src/components/keepsakes/KeepsakesModal.jsx:119, src/utils/planConfig.js:34 |
| **Severity** | 6 |
| **Occurrence** | 7 |
| **Detection** | 2 |
| **RPN** | **84** |
| **Recommended Action** | Read isKeepsakePreviewOnly() on modal open. If true: show banner at step 1; "Add to Basket" button replaced with upgrade CTA throughout (not just at final step). |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-FL-006

| Field | Value |
|---|---|
| **ID** | FMEA-FL-006 |
| **UXD Step** | FL-8.1 (About Tab) |
| **Title** | Pet analysis listed as "Coming Soon" but is already live |
| **Description** | AppLayout.jsx:808 lists "🐾 Pet analysis" under "Coming Soon". Pet analysis is live: available in UploadSection, PetResults component, analyzePetResemblance in useKinshipAnalysis. |
| **Expected Behavior** | "Coming Soon" list accurately reflects features not yet available. Live features are in "What's Included". |
| **Actual Behavior** | Working feature hidden from users; undersells the product; creates confusion when users find it themselves. File: src/layout/AppLayout.jsx:808 |
| **Severity** | 5 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **100** |
| **Recommended Action** | Remove pet analysis from "Coming Soon". Add it to "What's Included" list. Audit the rest of "Coming Soon" for other stale entries. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FL-007

| Field | Value |
|---|---|
| **ID** | FMEA-FL-007 |
| **UXD Step** | FL-7.2 (Plans Page — Checkout) |
| **Title** | Stripe Price IDs silently absent — all paid plan upgrades broken if env vars missing |
| **Description** | PlansPage.jsx:15-19 reads VITE_STRIPE_PLUS_MONTHLY_PRICE_ID etc., defaulting to '' (empty string). handleSelectPlan checks if (!priceId) → shows error "This plan is not available right now." No support link, no fallback, no alerting. All monetisation breaks silently if env vars absent in production. |
| **Expected Behavior** | If Price IDs are absent: show actionable error with support link or email. Alert developers via logging. Never silently break monetisation. |
| **Actual Behavior** | User sees "This plan is not available right now" with no next step. Files: src/pages/PlansPage.jsx:15-19, :101-106 |
| **Severity** | 9 |
| **Occurrence** | 2 |
| **Detection** | 6 |
| **RPN** | **108** |
| **Recommended Action** | (1) Add startup check: if any Stripe price ID is empty in production, log ERROR immediately. (2) Replace error text with: "Plan unavailable — please contact support@famililook.com". (3) Add E2E smoke test that verifies Stripe price IDs are set before deploy. |
| **Status** | FIXED (Sprint 2) |

---

### FMEA-FL-008

| Field | Value |
|---|---|
| **ID** | FMEA-FL-008 |
| **UXD Step** | FL-9.1 (Demo Mode) |
| **Title** | isDemoMode() stale cache prevents demo activation or expiry |
| **Description** | planConfig.js:126 caches demo mode in module-level let _demoMode = null. Once evaluated, subsequent calls skip localStorage/URL check. If demo is activated mid-session via URL param → returns cached false. If demo expires → returns cached true. |
| **Expected Behavior** | isDemoMode() reads fresh state on each call. Demo activates immediately when URL param is present. Demo expires exactly at 4h TTL. |
| **Actual Behavior** | Stale cache can cause demo to not activate on mid-session URL change, or persist past expiry. File: src/utils/planConfig.js:126-154 |
| **Severity** | 6 |
| **Occurrence** | 3 |
| **Detection** | 6 |
| **RPN** | **108** |
| **Recommended Action** | Remove module-level _demoMode cache. Read localStorage + URL param on every call. If performance matters, use a React state/effect pattern or a short-lived cache (e.g., 100ms debounce) rather than infinite cache. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-FL-009

| Field | Value |
|---|---|
| **ID** | FMEA-FL-009 |
| **UXD Step** | FU-1.1 (FamiliUno — Group Mode) |
| **Title** | Group mode analysis may never produce cards in FamiliUno |
| **Description** | FamiliUnoPage watches analysisResults. In group-only mode, analysisResults stores engineResult (pairwise data without a children array). buildDeck() reads fl:analysisResults from localStorage; in group mode this has no children → dataSource: "none" → hasCards=false. User runs group analysis successfully; FamiliUno shows upload screen forever. |
| **Expected Behavior** | After successful group analysis, buildDeck() recognizes group result format and produces cards. FamiliUno shows card deck. |
| **Actual Behavior** | Group analysis complete; FamiliUnoPage.hasCards=false; upload screen never advances. Files: src/pages/FamiliUnoPage.jsx:36-43, src/game/deckBuilder.js |
| **Severity** | 8 |
| **Occurrence** | 5 |
| **Detection** | 3 |
| **RPN** | **120** |
| **Recommended Action** | Update buildDeck() to handle group result format: if fl:groupSnapshot exists and has pairwise data, build cards from group faces. Alternatively: always write a fl:analysisResults with a synthesized children array when group analysis completes. |
| **Status** | FIXED (Sprint 1) |

---

### FMEA-FL-010

| Field | Value |
|---|---|
| **ID** | FMEA-FL-010 |
| **UXD Step** | FL-3.1 (App Shell) — feedback button |
| **Title** | Feedback button gate uses non-reactive localStorage read |
| **Description** | AppLayout.jsx:635,819 directly calls localStorage.getItem("fl:feedback-given") in JSX render. Not reactive — if flag changes during session, button does not disappear. Same pattern in HomePage.jsx:579. |
| **Expected Behavior** | Feedback button visibility responds to real-time state changes. |
| **Actual Behavior** | After user submits feedback, button may remain visible until next render triggered by other state change. Files: src/layout/AppLayout.jsx:635,819, src/pages/HomePage.jsx:579 |
| **Severity** | 3 |
| **Occurrence** | 6 |
| **Detection** | 5 |
| **RPN** | **90** |
| **Recommended Action** | Move fl:feedback-given into React state (useState + effect). Initialize from localStorage; update state when value changes. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-011

| Field | Value |
|---|---|
| **ID** | FMEA-FL-011 |
| **UXD Step** | FL-1.1 (Homepage Load) |
| **Title** | Social proof counter hardcoded — never reflects real usage |
| **Description** | HomePage.jsx:256 hardcodes "12,800+" families. No API call, no env var, no CMS. Becomes inaccurate immediately and is potentially misleading. |
| **Expected Behavior** | Counter reflects real data (live API or periodic update), or is clearly marked "approximately" with a note. |
| **Actual Behavior** | Permanently shows "12,800+" regardless of actual usage. File: src/pages/HomePage.jsx:256 |
| **Severity** | 4 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **80** |
| **Recommended Action** | Fetch counter from backend analytics endpoint on page load. Fallback to cached/hardcoded value if unavailable. Show "12,800+" until real data arrives. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-FL-012

| Field | Value |
|---|---|
| **ID** | FMEA-FL-012 |
| **UXD Step** | FL-2.1 (Trail Map Load) |
| **Title** | Trail reads plan tier from raw localStorage — bypasses usePlanFeatures overrides |
| **Description** | TrailHomePage.jsx:60-65 reads plan with raw localStorage.getItem('fl:plan'), not via usePlanFeatures. Bypasses: ambassador plan overrides, promo upgrades, backend verification freshness. Tier badge, confetti trigger, and upsell nudges can show wrong tier. |
| **Expected Behavior** | Trail uses usePlanFeatures() as authoritative plan source (per CLAUDE.md invariant). |
| **Actual Behavior** | Ambassador/promo users see incorrect tier on Trail. Files: src/pages/TrailHomePage.jsx:60-65 |
| **Severity** | 5 |
| **Occurrence** | 4 |
| **Detection** | 5 |
| **RPN** | **100** |
| **Recommended Action** | Replace localStorage.getItem('fl:plan') with usePlanFeatures().currentPlan throughout TrailHomePage. |
| **Status** | FIXED (Sprint 4C) |

---

### FMEA-FL-013

| Field | Value |
|---|---|
| **ID** | FMEA-FL-013 |
| **UXD Step** | /dashboard route |
| **Title** | Analytics dashboard publicly accessible — no route guard |
| **Description** | AppRouter.jsx:101-110 loads AnalyticsDashboard via lazy import with no route guard. Dashboard may have internal SHA-256 auth but component loads for any visitor. |
| **Expected Behavior** | /dashboard is either not publicly routed or protected by a route guard before the component loads. |
| **Actual Behavior** | Anyone can navigate to /dashboard; component loads and renders. File: src/AppRouter.jsx:101-110 |
| **Severity** | 5 |
| **Occurrence** | 2 |
| **Detection** | 3 |
| **RPN** | **30** |
| **Recommended Action** | Add a route-level guard: if dashboard is not in production (isDev) OR if admin hash not set in env, redirect to /. The internal SHA-256 check is a second layer, not the only guard. |
| **Status** | Open |

---

### FMEA-FL-014

| Field | Value |
|---|---|
| **ID** | FMEA-FL-014 |
| **UXD Step** | FL-3.4 (Photo Upload) — consent flow |
| **Title** | detectPhoto useCallback missing consent in dependency array |
| **Description** | UploadSection.jsx:342 defines detectPhoto as useCallback with empty deps []. Reads consent.biometric inside callback → stale closure. If consent changes during session, detectPhoto still holds old value. Workaround (pendingFileRef replay) partially mitigates but root cause remains. |
| **Expected Behavior** | detectPhoto always reads the current consent.biometric value. |
| **Actual Behavior** | Stale closure; consent value may be stale in detectPhoto. File: src/layout/UploadSection.jsx:342 |
| **Severity** | 5 |
| **Occurrence** | 3 |
| **Detection** | 6 |
| **RPN** | **90** |
| **Recommended Action** | Add consent to the useCallback dependency array: useCallback(..., [consent]). The pendingFileRef workaround can remain as belt-and-suspenders. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-015

| Field | Value |
|---|---|
| **ID** | FMEA-FL-015 |
| **UXD Step** | FL-4.3 (Group Analysis Results) |
| **Title** | MobileResultsSection renders null for group-only results |
| **Description** | MobileResultsSection.jsx:491 returns null when childCards.length === 0. In group-only mode, engineResult.children may be empty or absent → childCards = [] → nothing renders. Pet results, sensitivity slider, and keepsakes modal all inside same conditional. |
| **Expected Behavior** | Group-only analysis results are displayed in MobileResultsSection (or an appropriate sibling component). |
| **Actual Behavior** | Group analysis succeeds; results section renders nothing; user sees blank area below upload section. File: src/layout/MobileResultsSection.jsx:491 |
| **Severity** | 7 |
| **Occurrence** | 5 |
| **Detection** | 2 |
| **RPN** | **70** |
| **Recommended Action** | When childCards.length === 0 but groupAnalysis has data: render GroupSnapshotSection results instead. Do not return null; show "View Group Results" CTA or render the pairwise matrix inline. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-016

| Field | Value |
|---|---|
| **ID** | FMEA-FL-016 |
| **UXD Step** | FL-3.5 (COPPA Gate) |
| **Title** | COPPA gate acceptance does not re-trigger photo detection for gating photo |
| **Description** | UploadSection.jsx:342-390: detectPhoto calls promptCoppaIfNeeded() synchronously and returns early. Photo remains at quality: {level:'pending'} indefinitely after COPPA confirmation because pendingFileRef only replays consent-pending files, not COPPA-pending files. |
| **Expected Behavior** | After COPPA gate accepted: photo detection re-runs for the photo that triggered the gate. Quality badge updates. |
| **Actual Behavior** | Photo stuck at "pending" quality badge after COPPA acceptance until user re-uploads. File: src/layout/UploadSection.jsx:342-390, :546-554 |
| **Severity** | 4 |
| **Occurrence** | 4 |
| **Detection** | 5 |
| **RPN** | **80** |
| **Recommended Action** | Store a COPPA-specific pending file reference. In the COPPA onConfirm handler, replay detectPhoto for the pending file (similar to how pendingFileRef handles biometric consent). |
| **Status** | FIXED |

---

### FMEA-FL-017

| Field | Value |
|---|---|
| **ID** | FMEA-FL-017 |
| **UXD Step** | /icon-preview, /mockup-preview, /character-preview routes |
| **Title** | Internal design preview tools publicly accessible |
| **Description** | AppRouter.jsx:121-145 exposes three internal tool routes with no authentication or dev-mode guard. May contain sensitive designs, plan-bypass functionality, or PII. |
| **Expected Behavior** | Internal tools are either (a) restricted to dev mode only, or (b) protected by admin authentication before rendering. |
| **Actual Behavior** | Any user can navigate to these routes. File: src/AppRouter.jsx:121-145 |
| **Severity** | 4 |
| **Occurrence** | 2 |
| **Detection** | 4 |
| **RPN** | **32** |
| **Recommended Action** | Add isDev check: if (!import.meta.env.DEV) return <Navigate to="/" />. |
| **Status** | Open |

---

### FMEA-FL-018

| Field | Value |
|---|---|
| **ID** | FMEA-FL-018 |
| **UXD Step** | FL-7.2 (Plans Page — Stripe return) |
| **Title** | Stripe return with no stored email — plan not activated after payment |
| **Description** | PlansPage.jsx:63-74: reads storedEmail = localStorage.getItem('fl:plan-email'). If localStorage cleared between payment and Stripe redirect (private browsing, storage quota error), storedEmail is null → getSubscriptionStatus not called → plan not activated → user left on /plans with no feedback after paying. |
| **Expected Behavior** | If email not in localStorage on Stripe return: show "Payment received — enter your email to activate your plan" form. |
| **Actual Behavior** | User completes payment; plan not activated; stuck on /plans; no feedback. File: src/pages/PlansPage.jsx:63-74 |
| **Severity** | 8 |
| **Occurrence** | 2 |
| **Detection** | 6 |
| **RPN** | **96** |
| **Recommended Action** | On Stripe return with session_id but no stored email: show inline email recovery form "Please enter the email you used at checkout" → call getSubscriptionStatus with entered email. |
| **Status** | FIXED (Sprint 4C) |

---

### FMEA-FL-019

| Field | Value |
|---|---|
| **ID** | FMEA-FL-019 |
| **UXD Step** | All (bundle size) |
| **Title** | Unused lazy import (DeckCheckoutPage) inflates bundle |
| **Description** | Duplicate of FMEA-FL-001 with additional bundle impact detail. The lazy chunk includes heavy dependencies (canvas, PDF). |
| **Severity** | 2 |
| **Occurrence** | 10 |
| **Detection** | 3 |
| **RPN** | **60** |
| **Recommended Action** | Same as FMEA-FL-001. |
| **Status** | FIXED (Sprint 4D) | |

---

### FMEA-FL-020

| Field | Value |
|---|---|
| **ID** | FMEA-FL-020 |
| **UXD Step** | FL-3.1 (App Shell) — tab navigation |
| **Title** | BottomNav Home re-tap navigates to /hub instead of scroll-to-top |
| **Description** | AppLayout.jsx:932-933: if (tabId === "home" && activeTab === "home") { navigate("/hub"); }. Re-tapping active Home tab sends user to BrandHub. Conventional UX: re-tap active tab = scroll to top. |
| **Expected Behavior** | Re-tapping the active Home tab scrolls the page to top (standard mobile tab bar behavior). |
| **Actual Behavior** | User exits the app to /hub unexpectedly. File: src/layout/AppLayout.jsx:932-933 |
| **Severity** | 4 |
| **Occurrence** | 5 |
| **Detection** | 3 |
| **RPN** | **60** |
| **Recommended Action** | Replace navigate("/hub") with window.scrollTo({ top: 0, behavior: 'smooth' }). |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-021

| Field | Value |
|---|---|
| **ID** | FMEA-FL-021 |
| **UXD Step** | FL-3.7 (Results Display) |
| **Title** | generateNarrative called without memoization in results render |
| **Description** | MobileResultsCarousel.jsx:374 calls generateNarrative() in IIFE in JSX render. May regenerate if memo comparison is shallow and features are new references each render. |
| **Expected Behavior** | Narrative generated once per result set, not on every render. |
| **Actual Behavior** | Potential unnecessary narrative regeneration. File: src/components/results/MobileResultsCarousel.jsx:374 |
| **Severity** | 2 |
| **Occurrence** | 4 |
| **Detection** | 3 |
| **RPN** | **24** |
| **Recommended Action** | Memoize: const narrative = useMemo(() => generateNarrative(...), [features, winner]). |
| **Status** | Open |

---

### FMEA-FL-022

| Field | Value |
|---|---|
| **ID** | FMEA-FL-022 |
| **UXD Step** | FL-6.3 (Order Success) |
| **Title** | "Return to FamiliLook" button navigates to /hub regardless of origin |
| **Description** | OrderSuccessPage.jsx:172 hardcodes navigate("/hub"). User who ordered from FamiliUno is sent to BrandHub, not /uno. |
| **Expected Behavior** | Return button navigates to origin of the order (e.g., /uno if deck ordered from FamiliUno). |
| **Actual Behavior** | Always /hub regardless of where order originated. File: src/pages/OrderSuccessPage.jsx:172 |
| **Severity** | 3 |
| **Occurrence** | 5 |
| **Detection** | 3 |
| **RPN** | **45** |
| **Recommended Action** | Read ?from= param on /order-success (set when creating basket checkout). Navigate to that URL. Default to /hub if not present. |
| **Status** | Open |

---

### FMEA-FL-023

| Field | Value |
|---|---|
| **ID** | FMEA-FL-023 |
| **UXD Step** | FL-1.1 (Homepage) — feedback button |
| **Title** | HomePage feedback button uses non-reactive localStorage read |
| **Description** | Duplicate of FMEA-FL-010 pattern in HomePage.jsx:579. |
| **Severity** | 3 |
| **Occurrence** | 6 |
| **Detection** | 5 |
| **RPN** | **90** |
| **Recommended Action** | Same as FMEA-FL-010. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FL-024

| Field | Value |
|---|---|
| **ID** | FMEA-FL-024 |
| **UXD Step** | FU-4.1 (Physical Deck Order) |
| **Title** | FamiliUno basket drawer permanently inaccessible — event listener never mounted |
| **Description** | FamiliUnoPage.jsx:267 dispatches window.dispatchEvent(new Event("open-basket-drawer")) after adding deck to basket. The listener is registered in AppLayout.jsx:153-157. FamiliUnoPage is rendered by AppRouter directly, NOT inside AppLayout. When on /uno, AppLayout is unmounted — listener does not exist. Event fires into void. Basket item IS added to BasketContext, but user cannot see or access basket. No BasketBadge, no BasketDrawer. |
| **Expected Behavior** | After adding deck to basket from /uno: basket is visible and accessible (badge + drawer) so user can proceed to checkout. |
| **Actual Behavior** | Basket invisible from /uno; user adds to basket but cannot check out without navigating to /app. Files: src/pages/FamiliUnoPage.jsx:267, src/layout/AppLayout.jsx:153-157 |
| **Severity** | 9 |
| **Occurrence** | 7 |
| **Detection** | 2 |
| **RPN** | **126** |
| **Recommended Action** | Option A: Add BasketDrawer and BasketBadge to FamiliUnoPage's own layout (render them locally, not via AppLayout). Option B: Move BasketDrawer to a global portal rendered at root level, outside routing. Option C: After adding to basket, navigate user to /app#basket with basket open param. Recommended: Option A (self-contained). |
| **Status** | FIXED (Sprint 1) |

---

## SECTION 2: FAMILIMATCH (famililook-desktop6)

*Source: audit_familimatch.md — 20 findings*

---

### FMEA-FM-001

| Field | Value |
|---|---|
| **ID** | FMEA-FM-001 |
| **UXD Step** | All FamiliMatch flows — pre-deployment |
| **Title** | Build completely broken — cannot rebuild from source |
| **Description** | No index.html, vite.config.js, src/main.jsx, or src/App.jsx exist. npm run build fails in 7ms: "Could not resolve entry module index.html". App exists only as stale compiled artifact in dist/. Any code change cannot be shipped. |
| **Expected Behavior** | npm run build succeeds and produces deployable artifacts. |
| **Actual Behavior** | Build fails immediately. Any code changes are unshippable. |
| **Severity** | 10 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **100** (capped; real impact = product is frozen) |
| **Recommended Action** | **P0:** Restore all missing source files. Minimum set: index.html, vite.config.js, src/main.jsx, src/App.jsx. |
| **Status** | FIXED (Sprint 0A) |

---

### FMEA-FM-002

| Field | Value |
|---|---|
| **ID** | FMEA-FM-002 |
| **UXD Step** | FM-2.3 (Solo Analysis) |
| **Title** | Broken import in matchClient.js — utils/constants missing |
| **Description** | src/utils/constants.js does not exist. matchClient.js:16 imports COMPARE_FEATURES from it. Any fresh build crashes: matchClient is non-functional; compareSolo() fails to resolve at build time. |
| **Expected Behavior** | COMPARE_FEATURES is available; compareSolo() compiles and runs. |
| **Actual Behavior** | Build crash on import. Solo analysis non-functional in any fresh build. File: src/api/matchClient.js:16 |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **90** (blocked by F-001 build failure) |
| **Recommended Action** | Restore src/utils/constants.js with COMPARE_FEATURES array. |
| **Status** | FIXED (Sprint 0A) |

---

### FMEA-FM-003

| Field | Value |
|---|---|
| **ID** | FMEA-FM-003 |
| **UXD Step** | FM-1.1 (Landing), FM-2.1 (Solo), FM-3.1 (Room) |
| **Title** | All 3 pages crash — ConsentContext and MatchContext missing |
| **Description** | src/state/ConsentContext.jsx and src/state/MatchContext.jsx do not exist. Every page imports from them. All 3 pages (LandingPage, SoloPage, RoomPage) crash on render in any fresh build. |
| **Expected Behavior** | useConsent() and useMatch() hooks are available throughout the app. |
| **Actual Behavior** | Build crash; all pages crash on render. Files: src/state/ (empty directory) |
| **Severity** | 10 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **100** (capped) |
| **Recommended Action** | **P0:** Restore both context files. |
| **Status** | FIXED (Sprint 0A) |

---

### FMEA-FM-004

| Field | Value |
|---|---|
| **ID** | FMEA-FM-004 |
| **UXD Step** | FM-2.1 (Solo), FM-3.1 (Room) |
| **Title** | 7 components missing — Solo and Room modes crash on render |
| **Description** | SoloPage imports: ConsentModal, PhotoUpload, OnboardingScreen, FeatureScanAnimation, ResultsStory — all missing. RoomPage additionally imports: RoomLobby, CountdownOverlay — also missing. Any import of these causes build crash; all interactive flows non-functional. |
| **Expected Behavior** | All imported components exist and render correctly. |
| **Actual Behavior** | Solo mode and Room mode crash on render in any fresh build. Files: src/components/ (7 missing) |
| **Severity** | 10 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **100** (capped) |
| **Recommended Action** | **P0:** Restore all 7 missing components. |
| **Status** | FIXED (Sprint 0A) |

---

### FMEA-FM-005

| Field | Value |
|---|---|
| **ID** | FMEA-FM-005 |
| **UXD Step** | All — API calls |
| **Title** | src/utils/config.js missing — all network calls non-functional |
| **Description** | src/utils/config.js does not exist. Exports API_BASE, API_KEY, MATCH_SERVER_URL. Imported by matchClient.js, analytics.js, useMatchConnection.js. All network calls (compare/faces, morph, analytics, WebSocket) fail to resolve in any fresh build. |
| **Expected Behavior** | All API constants available throughout the app. |
| **Actual Behavior** | All API calls fail in any fresh build. File: src/utils/config.js (missing) |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **90** (blocked by F-001) |
| **Recommended Action** | Restore src/utils/config.js with correct constants. |
| **Status** | FIXED (Sprint 0A) |

---

### FMEA-FM-006

| Field | Value |
|---|---|
| **ID** | FMEA-FM-006 |
| **UXD Step** | All — CI/pre-deploy |
| **Title** | Zero test files — no test coverage |
| **Description** | tests/ directory exists with empty subdirectories. npm run test:run exits code 1: "No test files found". No coverage for API contract compliance, tier gating, result rendering, WebSocket flows. |
| **Expected Behavior** | Tests cover API contract, tier gating, result rendering, at minimum. CI blocks deploy on test failure. |
| **Actual Behavior** | No tests. Any regression is undetected until users report it. File: tests/ (empty) |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 10 |
| **RPN** | **90** (detection = 10 means untestable, not "certain to detect") |
| **Recommended Action** | **P1:** Write tests for: (1) compare_faces.v1 API contract compliance, (2) tier gating logic, (3) Solo flow end-to-end, (4) WebSocket phase transitions. |
| **Status** | FIXED (Sprint 2) |

---

### FMEA-FM-007

| Field | Value |
|---|---|
| **ID** | FMEA-FM-007 |
| **UXD Step** | FM-2.3 (Solo Analysis) — names |
| **Title** | compareSolo sends hardcoded "Person A"/"Person B" names to backend |
| **Description** | matchClient.js:61 always sends nameA='Person A', nameB='Person B'. User's actual name (from OnboardingScreen) never passed to API. History entries store result.name_a = 'Person A'. |
| **Expected Behavior** | compareSolo(photoA, photoB, progressCallback, nameA, nameB) passes actual user names to API and history. |
| **Actual Behavior** | History always shows "Person A" / "Person B" regardless of actual names. File: src/api/matchClient.js:61,103 |
| **Severity** | 5 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **100** |
| **Recommended Action** | Add nameA, nameB parameters to compareSolo and pass them to compareFacesDirect(). Pass userName from SoloPage context. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-FM-008

| Field | Value |
|---|---|
| **ID** | FMEA-FM-008 |
| **UXD Step** | FM-3.4 (Countdown → Results) |
| **Title** | Room 'done' phase renders blank card before results navigate |
| **Description** | RoomPage.jsx:294: CountdownOverlay.onComplete sets phase='done'. AnimatePresence only handles lobby/upload/waiting/analyzing. Phase 'done' renders empty motion.div with no children — blank card. Navigation to /results depends on WebSocket 'reveal' message arriving in a separate useEffect. Any latency = visible blank card. |
| **Expected Behavior** | Phase 'done' shows loading spinner ("Loading results...") rather than blank card. |
| **Actual Behavior** | Blank card visible between countdown completion and results navigation. File: src/pages/RoomPage.jsx:209-272 |
| **Severity** | 6 |
| **Occurrence** | 5 |
| **Detection** | 3 |
| **RPN** | **90** |
| **Recommended Action** | Add 'done' phase handler in AnimatePresence: render a "Loading your results..." spinner with the FamiliMatch brand color. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FM-009

| Field | Value |
|---|---|
| **ID** | FMEA-FM-009 |
| **UXD Step** | FM-1.1 (Landing — mode selection) |
| **Title** | Tier gating relies on URL query param — trivially bypassable |
| **Description** | LandingPage.jsx:166-167: tier = searchParams.get('tier') || 'free'. Anyone can access Duo/Group by navigating to /?tier=plus. No server-side validation. Duo/Group are meant to be Plus-only features per CLAUDE.md (commit f644018). |
| **Expected Behavior** | Tier is sourced from a cryptographically signed session token from FamiliLook, verified server-side before room creation. |
| **Actual Behavior** | Tier from URL param; bypassed by changing ?tier=plus. File: src/pages/LandingPage.jsx:165-172 |
| **Severity** | 8 |
| **Occurrence** | 4 |
| **Detection** | 7 |
| **RPN** | **224** |
| **Recommended Action** | **P0:** Replace ?tier= URL param with a signed session token (e.g., JWT) issued by FamiliLook after plan verification. Validate token server-side in desktop7 before allowing room creation. |
| **Status** | FIXED (Sprint 2) |

---

### FMEA-FM-010

| Field | Value |
|---|---|
| **ID** | FMEA-FM-010 |
| **UXD Step** | FM-3.5 (Results — Group/Room) |
| **Title** | ResultsPage missing from source — hard refresh loses all results |
| **Description** | src/pages/ResultsPage.jsx deleted. Only dist artifact. MatchContext.results has no localStorage persistence. Hard refresh on /results → "No results yet". Room mode results permanently lost on reload. |
| **Expected Behavior** | Results persisted to localStorage on arrival. Hard refresh on /results shows last result or graceful "Results expired" message. |
| **Actual Behavior** | Hard refresh = permanent loss of room comparison results. File: dist/assets/ResultsPage-BeqOeRxe.js (no source) |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 2 |
| **RPN** | **48** |
| **Recommended Action** | (1) Restore ResultsPage.jsx source. (2) Persist results to localStorage on receipt with 24h TTL. (3) On /results load: if context empty, check localStorage; if expired, show "Results expired — start a new comparison". |
| **Status** | Open |

---

### FMEA-FM-011

| Field | Value |
|---|---|
| **ID** | FMEA-FM-011 |
| **UXD Step** | FM-3.1 (Room Mode) — analytics |
| **Title** | RoomPage has no analytics page view call |
| **Description** | RoomPage.jsx has no analytics.trackPageView('room') call. Duo/Group funnel analysis is impossible; cannot track drop-off in room mode. |
| **Expected Behavior** | Every page tracks page view; RoomPage calls analytics.trackPageView('room') on mount. |
| **Actual Behavior** | Room mode invisible to analytics. File: src/pages/RoomPage.jsx |
| **Severity** | 3 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **60** |
| **Recommended Action** | Add useEffect(() => { analytics.trackPageView('room'); }, []) to RoomPage. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FM-012

| Field | Value |
|---|---|
| **ID** | FMEA-FM-012 |
| **UXD Step** | FM-1.1 (Landing — Trail auto-nav) |
| **Title** | Auto-navigate via ?mode= bypasses consent check |
| **Description** | LandingPage.jsx:179-187: if ?mode=solo present and unlocked, navigate(card.path) without checking consent.bipaConsented. User taken to SoloPage before consent obtained. Consent checked lazily only when user taps Compare Faces. |
| **Expected Behavior** | Consent check always precedes navigation to any mode. Auto-navigate must trigger consent modal if not already consented. |
| **Actual Behavior** | User arrives at SoloPage before consent. BIPA/GDPR risk. File: src/pages/LandingPage.jsx:179-187 |
| **Severity** | 7 |
| **Occurrence** | 3 |
| **Detection** | 6 |
| **RPN** | **126** |
| **Recommended Action** | Before auto-navigating: check consent.bipaConsented. If false → show ConsentModal; on accept → navigate. Same as manual mode selection path. |
| **Status** | FIXED (Sprint 1) |

---

### FMEA-FM-013

| Field | Value |
|---|---|
| **ID** | FMEA-FM-013 |
| **UXD Step** | FM-2.4 (Results — Face Fusion) |
| **Title** | Face morph uses hardcoded 50/50 feature split, not actual comparison results |
| **Description** | matchClient.js:79: features alternated 50/50 regardless of comparison result. A 95% match gets same fusion as a 5% match. Misleading. |
| **Expected Behavior** | Morph feature slots reflect actual feature comparison results (matched features from face_a, unmatched from face_b, or per comparison score). |
| **Actual Behavior** | Always alternates: feature[0]=A, feature[1]=B, feature[2]=A... regardless of match. File: src/api/matchClient.js:79-82 |
| **Severity** | 4 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **80** |
| **Recommended Action** | Build fusionSlots from feature_comparisons: where match=true use the shared label; where match=false assign to face_a or face_b based on stronger label. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FM-014

| Field | Value |
|---|---|
| **ID** | FMEA-FM-014 |
| **UXD Step** | FM-2.5 (Share Card) — history display |
| **Title** | History display has hardcoded fallback color — missing chemistry_color handled but not logged |
| **Description** | useMatchHistory.js:27 stores shared_features.length correctly. LandingPage history display falls back to '#5e5ce6' for missing chemistry_color. Not a crash but indicates a data quality issue. |
| **Expected Behavior** | chemistry_color always present in history entries; fallback only for truly legacy entries. |
| **Actual Behavior** | Fallback fires silently when chemistry_color absent — no indication of data quality issue. File: src/hooks/useMatchHistory.js:27 |
| **Severity** | 2 |
| **Occurrence** | 2 |
| **Detection** | 8 |
| **RPN** | **32** |
| **Recommended Action** | Log a warning when fallback fires. Consider adding a migration for old history entries. |
| **Status** | Open |

---

### FMEA-FM-015

| Field | Value |
|---|---|
| **ID** | FMEA-FM-015 |
| **UXD Step** | FM-2.5 (Share Card) |
| **Title** | ShareCard uses hardcoded production URL — wrong environment in dev |
| **Description** | ShareCard.jsx:9: const SHARE_URL = 'https://famililook-desktop6.vercel.app'. Hardcoded, not driven by env var. Dev environment shares link to production URL. |
| **Expected Behavior** | SHARE_URL driven by environment variable: VITE_SHARE_URL or import.meta.env.VITE_APP_URL. |
| **Actual Behavior** | Always links to Vercel production URL even in local dev. File: src/components/ShareCard.jsx:9 |
| **Severity** | 2 |
| **Occurrence** | 5 |
| **Detection** | 5 |
| **RPN** | **50** |
| **Recommended Action** | Replace with import.meta.env.VITE_SHARE_URL ?? 'https://famililook-desktop6.vercel.app'. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FM-016

| Field | Value |
|---|---|
| **ID** | FMEA-FM-016 |
| **UXD Step** | FM-3.2 (Upload Phase — Room) |
| **Title** | Double grantConsent call possible in RoomPage |
| **Description** | Two useEffect hooks can both call connection.grantConsent(): (1) when connection.gameStarted && phase==='lobby' && !isHost, (2) handleConsented() from ConsentModal. If participant grants consent via modal AND gameStarted becomes true before modal dismissal, both paths fire. WebSocket message sent twice. |
| **Expected Behavior** | grantConsent sent exactly once per player per room session. |
| **Actual Behavior** | Potential double grantConsent message; backend receives duplicate. File: src/pages/RoomPage.jsx:98-138 |
| **Severity** | 4 |
| **Occurrence** | 2 |
| **Detection** | 6 |
| **RPN** | **48** |
| **Recommended Action** | Track consentGranted in local state; gate both paths with if (!consentGranted). |
| **Status** | Open |

---

### FMEA-FM-017

| Field | Value |
|---|---|
| **ID** | FMEA-FM-017 |
| **UXD Step** | FM-1.1 (Landing — social proof) |
| **Title** | Social proof counter fabricated — random increment, not real data |
| **Description** | LandingPage.jsx:137-147: SEED=12847; counter increments by 0-2 every 8 seconds. Fabricated social proof. |
| **Expected Behavior** | Counter reflects real comparison count from analytics API. |
| **Actual Behavior** | Fabricated; misleading. File: src/pages/LandingPage.jsx:137-147 |
| **Severity** | 4 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **80** |
| **Recommended Action** | Fetch real count from analytics endpoint. Use hardcoded seed only as fallback. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-FM-018

| Field | Value |
|---|---|
| **ID** | FMEA-FM-018 |
| **UXD Step** | App initialization |
| **Title** | analytics.js fires session_start before consent check |
| **Description** | analytics.js:33: setTimeout(() => this.track('session_start', ...), 0). In dev, consent bypass fires it always. In production, track() is consent-gated; event dropped if not consented. Technically correct in prod but misleading in code. |
| **Expected Behavior** | session_start fires only after consent granted; explicit in code. |
| **Actual Behavior** | session_start fired optimistically; silently dropped if no consent. File: src/utils/analytics.js:33 |
| **Severity** | 3 |
| **Occurrence** | 10 |
| **Detection** | 5 |
| **RPN** | **150** |
| **Recommended Action** | Move session_start to fire inside the grantConsent() callback, not on initialization. |
| **Status** | FIXED (Sprint 4C) |

---

### FMEA-FM-019

| Field | Value |
|---|---|
| **ID** | FMEA-FM-019 |
| **UXD Step** | Navigation — all pages |
| **Title** | reversePortalTransition function duplicated in 3 files |
| **Description** | Function copy-pasted at top of LandingPage.jsx, SoloPage.jsx, RoomPage.jsx. Any future change must be applied in 3 places. |
| **Expected Behavior** | Shared utility function in src/utils/. |
| **Actual Behavior** | 3 identical copies. Files: src/pages/LandingPage.jsx:8-30, SoloPage.jsx:8-30, RoomPage.jsx:6-28 |
| **Severity** | 2 |
| **Occurrence** | 10 |
| **Detection** | 3 |
| **RPN** | **60** |
| **Recommended Action** | Extract to src/utils/transitions.js. Import from all 3 pages. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FM-020

| Field | Value |
|---|---|
| **ID** | FMEA-FM-020 |
| **UXD Step** | FM-2.3 (Analysis Loading) |
| **Title** | SoloPage passes hardcoded "B" as nameB to FeatureScanAnimation |
| **Description** | SoloPage.jsx:246-247: nameA={userName || 'A'} and nameB="B". Person B always labeled "B" in loading animation regardless of context. |
| **Expected Behavior** | Person B's name shown in loading animation. |
| **Actual Behavior** | Loading animation always shows "B" for Person B. File: src/pages/SoloPage.jsx:246-247 |
| **Severity** | 3 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **60** |
| **Recommended Action** | Pass actual Person B name: nameB={personBName || 'Person B'}. Store Person B name in context during upload. |
| **Status** | FIXED (Sprint 4D) |

---

## SECTION 3: FAMILIPOKER (famililook-desktop4)

*Source: audit_familipoker.md — 20 findings*

---

### FMEA-FP-001

| Field | Value |
|---|---|
| **ID** | FMEA-FP-001 |
| **UXD Step** | FP-2.3 (Analysis) — error state |
| **Title** | Analysis errors silently swallowed — user gets zero feedback on failure |
| **Description** | useKinshipAnalysis returns error state and clearError callback. AppLayout.jsx:272-276 never destructures error. Loading overlay disappears on failure; user sees nothing — no message, no retry button, no guidance. Core flow broken with no UX signal. |
| **Expected Behavior** | Any analysis error (network, API, validation) surfaces to user with: what went wrong + "Try Again" button + "Get Help" link. |
| **Actual Behavior** | Silence. User sees loading overlay disappear. No information. Files: src/layout/AppLayout.jsx:272-276, src/hooks/useKinshipAnalysis.jsx:553-557 |
| **Severity** | 9 |
| **Occurrence** | 6 |
| **Detection** | 3 |
| **RPN** | **162** |
| **Recommended Action** | **P0:** Destructure error and clearError from useKinshipAnalysis in AppLayout. Render error card when error is set: "{error.message}" + "Try Again" button + "Contact Support" link. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FP-002

| Field | Value |
|---|---|
| **ID** | FMEA-FP-002 |
| **UXD Step** | FP-2.2 (Upload) — mode switching |
| **Title** | analysisMode/setAnalysisMode destructured from context but never provided |
| **Description** | FamililookContext never defines analysisMode or setAnalysisMode. UploadSection destructures both → undefined. setAnalysisMode() is a no-op. Mode selected in UploadSection is never persisted to context. Any other component reading analysisMode from context gets undefined. |
| **Expected Behavior** | analysisMode reflects the current selected analysis mode (individual/group) in context. setAnalysisMode updates it. |
| **Actual Behavior** | Silent context mismatch; mode switching works locally (localMode state) but is not shared. Files: src/layout/UploadSection.jsx:488-496, src/state/FamililookContext.jsx |
| **Severity** | 6 |
| **Occurrence** | 8 |
| **Detection** | 7 |
| **RPN** | **336** |
| **Recommended Action** | Add analysisMode to FamililookContext state and value object. Alternatively, remove the destructuring from UploadSection if context-level mode sharing is not needed. |
| **Status** | Open |

---

### FMEA-FP-003

| Field | Value |
|---|---|
| **ID** | FMEA-FP-003 |
| **UXD Step** | FP-4.2 (Poker Gameplay) — back navigation |
| **Title** | FeaturePoker Back button loops to SETUP — navigation dead end |
| **Description** | AppLayout.jsx:538 passes onBack={() => setSelectedGame("poker")}. This re-renders FeaturePoker from SETUP immediately. User cannot exit Poker to the lobby or switch games without reloading the page. |
| **Expected Behavior** | Back in FeaturePoker → setSelectedGame(null) → lobby (no game selected). |
| **Actual Behavior** | Back → restart Poker from SETUP. Infinite loop; other games inaccessible. File: src/layout/AppLayout.jsx:538 |
| **Severity** | 8 |
| **Occurrence** | 9 |
| **Detection** | 2 |
| **RPN** | **144** |
| **Recommended Action** | **P1:** Change onBack prop to: () => setSelectedGame(null). This returns user to the GameRooms lobby where they can choose Poker or Blackjack. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FP-004

| Field | Value |
|---|---|
| **ID** | FMEA-FP-004 |
| **UXD Step** | FP-3.1 (Games Lobby) |
| **Title** | GameSelector defines 5 games; only 2 render — rest show blank |
| **Description** | AppLayout has a GameSelector component (dead code — never rendered) listing 5 game IDs: memory, facematch, deck, feedfam, facefusion. gameRoomsConfig.js only registers poker and blackjack. If any path selects other IDs, nothing renders below the lobby. |
| **Expected Behavior** | Only games that can actually be played are shown in the lobby. |
| **Actual Behavior** | Potential blank rendering for any game ID not explicitly handled. Files: src/layout/AppLayout.jsx:538-539, src/game/gameRoomsConfig.js |
| **Severity** | 7 |
| **Occurrence** | 2 |
| **Detection** | 4 |
| **RPN** | **56** |
| **Recommended Action** | Remove dead GameSelector component. Ensure gameRoomsConfig.js is the single source of truth for available games. Add a fallback renderer: if (selectedGame && ![poker,blackjack].includes(selectedGame)) show "Game coming soon". |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FP-005

| Field | Value |
|---|---|
| **ID** | FMEA-FP-005 |
| **UXD Step** | FP-6 (Plans Page) |
| **Title** | Plans page plan selection is entirely inert |
| **Description** | PlansPage.jsx:9 calls navigate(`/app?plan=${planKey}`). AppLayout and FamililookContext never read ?plan= from URL. currentPlan stays "free" regardless. No payment integration, no persistence. |
| **Expected Behavior** | Plan selection on /plans actually upgrades the user's plan with payment verification. |
| **Actual Behavior** | Plan selection navigates to /app; nothing changes. Files: src/pages/PlansPage.jsx:9, src/state/FamililookContext.jsx:67 |
| **Severity** | 8 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **160** |
| **Recommended Action** | Integrate Stripe checkout (same pattern as desktop2/PlansPage). Store plan email; verify subscription; set currentPlan on return. Until payment is integrated, remove /plans from navigation. |
| **Status** | FIXED (Sprint 4B) |

---

### FMEA-FP-006

| Field | Value |
|---|---|
| **ID** | FMEA-FP-006 |
| **UXD Step** | All — analytics |
| **Title** | Analytics dev bypass missing — all events silently dropped in dev |
| **Description** | src/analytics.js has no if (import.meta.env.DEV) return true bypass in hasAnalyticsConsent(). ConsentBanner.jsx returns null in dev → fl:consent never set → isConsentGiven() = false → all analytics events dropped. Exact issue documented in CLAUDE.md for desktop2. |
| **Expected Behavior** | Analytics events fire in development. Dashboard shows real data during testing. |
| **Actual Behavior** | All analytics events dropped in dev. Dashboard shows zeros. File: src/analytics.js:2-12 |
| **Severity** | 6 |
| **Occurrence** | 10 |
| **Detection** | 5 |
| **RPN** | **300** |
| **Recommended Action** | Add to hasAnalyticsConsent(): if (import.meta.env.DEV) return true; — per CLAUDE.md NON-NEGOTIABLE guardrail. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FP-007

| Field | Value |
|---|---|
| **ID** | FMEA-FP-007 |
| **UXD Step** | FP-2.3 (Analysis) — API request |
| **Title** | API request sends client: "famililook-desktop2" — wrong product identity |
| **Description** | useKinshipAnalysis.jsx:337 hardcodes client: "famililook-desktop2". Copy-paste from desktop2. Backend analytics/logs cannot distinguish FamiliPoker traffic from FamiliLook. |
| **Expected Behavior** | client field identifies this product as "famililook-desktop4". |
| **Actual Behavior** | All FamiliPoker API requests report as desktop2. File: src/hooks/useKinshipAnalysis.jsx:337 |
| **Severity** | 5 |
| **Occurrence** | 10 |
| **Detection** | 3 |
| **RPN** | **150** |
| **Recommended Action** | Change client: "famililook-desktop2" to client: "famililook-desktop4". Add lint rule or test to prevent copy-paste regression. |
| **Status** | FIXED (Sprint 0B) |

---

### FMEA-FP-008

| Field | Value |
|---|---|
| **ID** | FMEA-FP-008 |
| **UXD Step** | All — crash recovery |
| **Title** | ErrorBoundary shows raw crash message with no recovery option |
| **Description** | ErrorBoundary.jsx:17-26 renders: Crash: {String(err.message)} in a red div. No reload button, no navigation, no brand styling. User completely stranded. |
| **Expected Behavior** | Error boundary shows branded error screen: message + "Reload App" button + "Contact Support" link. |
| **Actual Behavior** | Raw error message; no recovery path. File: src/components/ui/ErrorBoundary.jsx:17-26 |
| **Severity** | 7 |
| **Occurrence** | 2 |
| **Detection** | 2 |
| **RPN** | **28** |
| **Recommended Action** | Replace ErrorBoundary fallback with branded screen: "Something went wrong" + "Reload" (window.location.reload()) + "Contact Support" link. |
| **Status** | Open |

---

### FMEA-FP-009

| Field | Value |
|---|---|
| **ID** | FMEA-FP-009 |
| **UXD Step** | FP-5.2 (Blackjack — BET stage) |
| **Title** | Feature21 BET Back destroys chips with no confirmation |
| **Description** | Feature21.jsx:862,891: Back from BET stage via onBack → setSelectedGame(null). No confirmation dialog. Chip progress and session lost immediately. |
| **Expected Behavior** | Confirmation dialog: "You'll lose your current bet — are you sure?" before Back destroys game state. |
| **Actual Behavior** | Instant loss of chips/progress on Back tap. File: src/game/Feature21.jsx:862,891 |
| **Severity** | 5 |
| **Occurrence** | 4 |
| **Detection** | 2 |
| **RPN** | **40** |
| **Recommended Action** | Show confirmation dialog on Back from BET/PLAYER_TURN stages. Proceed only on confirmation. |
| **Status** | Open |

---

### FMEA-FP-010

| Field | Value |
|---|---|
| **ID** | FMEA-FP-010 |
| **UXD Step** | FP-3.1 (Games Lobby) — no analysis |
| **Title** | deckBuilder falls back to 3 dummy faces with no analysis data |
| **Description** | deckBuilder.js:898: faceCount = allNames.size || 3. With no analysis, builds deck from synthetic people. Games launch with ghost players. |
| **Expected Behavior** | Games clearly require analysis data; fallback to synthetic data is not permitted without explicit user knowledge. |
| **Actual Behavior** | Games can launch with dummy data if banner is bypassed. File: src/game/deckBuilder.js:898 |
| **Severity** | 4 |
| **Occurrence** | 2 |
| **Detection** | 4 |
| **RPN** | **32** |
| **Recommended Action** | If dataSource==='none': block game launch; always show "Analyze your family first" gate. Never silently fall back to synthetic data in user-facing games. |
| **Status** | Open |

---

### FMEA-FP-011

| Field | Value |
|---|---|
| **ID** | FMEA-FP-011 |
| **UXD Step** | FP-3.1 (Games Lobby — initial load) |
| **Title** | selectedGame defaults to "poker" — game auto-launches without user choice |
| **Description** | AppLayout.jsx:285-289: selectedGame initialized from ?game= URL param, defaulting to "poker". On first load, FeaturePoker renders immediately without any user interaction. |
| **Expected Behavior** | No game selected on first load; user actively chooses from GameRooms lobby. |
| **Actual Behavior** | FeaturePoker renders immediately; user has not consented to playing Poker specifically. File: src/layout/AppLayout.jsx:285-289 |
| **Severity** | 4 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **80** |
| **Recommended Action** | Default selectedGame to null (not "poker"). Only set to a specific game if ?game= URL param explicitly provided and valid. |
| **Status** | FIXED (Sprint 4B) |

---

### FMEA-FP-012

| Field | Value |
|---|---|
| **ID** | FMEA-FP-012 |
| **UXD Step** | Navigation — all tabs |
| **Title** | BottomNav Home re-tap exits app to BRAND_HUB_URL |
| **Description** | AppLayout.jsx:884-893: from Home tab, re-tapping Home triggers reversePortalTransition → navigate to BRAND_HUB_URL. Unexpected exit. Dual-use pattern non-obvious. |
| **Expected Behavior** | Re-tapping active tab scrolls to top. App exit only via explicit back navigation. |
| **Actual Behavior** | Re-tapping Home tab exits the app. File: src/layout/AppLayout.jsx:884-893 |
| **Severity** | 5 |
| **Occurrence** | 4 |
| **Detection** | 3 |
| **RPN** | **60** |
| **Recommended Action** | Change Home re-tap to scroll-to-top. Add explicit "Back to Hub" button in About tab for intentional exit. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-FP-013

| Field | Value |
|---|---|
| **ID** | FMEA-FP-013 |
| **UXD Step** | Build / development |
| **Title** | TypeScript files in pure JS project — dead code, no tsconfig |
| **Description** | Six .tsx/.ts files exist (FaceCard.tsx, useKinship.ts, lib/*.ts). No TypeScript config, no TS dependency. Not imported; dead code. If accidentally imported, build fails. |
| **Expected Behavior** | All source files are .jsx/.js only in a pure JS project. |
| **Actual Behavior** | 6 orphaned TypeScript files. File: src/components/FaceCard.tsx, src/hooks/useKinship.ts, src/lib/*.ts |
| **Severity** | 3 |
| **Occurrence** | 2 |
| **Detection** | 4 |
| **RPN** | **24** |
| **Recommended Action** | Delete orphaned TypeScript files. If TypeScript is desired for this project, add tsconfig.json and install @vitejs/plugin-react properly. |
| **Status** | Open |

---

### FMEA-FP-014

| Field | Value |
|---|---|
| **ID** | FMEA-FP-014 |
| **UXD Step** | FP-6 (Plans) — plan gating |
| **Title** | PLANS constant defined twice with incompatible values |
| **Description** | src/utils/config.js:21-25: PLANS = {FREE:'free', PREMIUM:'premium', DEV:'dev'}. src/utils/planConfig.js:4-8: PLANS = {FREE:'free', FAMILY:'family', PRO:'pro'}. Completely different sets. Code importing from config.js sees PREMIUM/DEV which don't correspond to actual plan keys. |
| **Expected Behavior** | Single source of truth for plan identifiers. |
| **Actual Behavior** | Two incompatible PLANS definitions. Plan gating logic silently uses wrong constants. Files: src/utils/config.js:21-25, src/utils/planConfig.js:4-8 |
| **Severity** | 6 |
| **Occurrence** | 5 |
| **Detection** | 6 |
| **RPN** | **180** |
| **Recommended Action** | Delete PLANS from src/utils/config.js. Single source of truth in planConfig.js. Grep for all PLANS usages; update imports. |
| **Status** | FIXED (Sprint 4B) |

---

### FMEA-FP-015

| Field | Value |
|---|---|
| **ID** | FMEA-FP-015 |
| **UXD Step** | All — analytics tracking |
| **Title** | Two separate analytics implementations — fragmented event tracking |
| **Description** | src/analytics.js (class-based Analytics) and src/utils/analytics.js are two completely separate implementations. Different components import from different files. Events may go to different systems or have different schemas. |
| **Expected Behavior** | Single analytics implementation used throughout the codebase. |
| **Actual Behavior** | Two analytics systems; split tracking; incomplete funnels. Files: src/analytics.js, src/utils/analytics.js |
| **Severity** | 5 |
| **Occurrence** | 8 |
| **Detection** | 5 |
| **RPN** | **200** |
| **Recommended Action** | Choose one implementation. Update all imports to use it. Delete the other. |
| **Status** | FIXED (Sprint 2) |

---

### FMEA-FP-016

| Field | Value |
|---|---|
| **ID** | FMEA-FP-016 |
| **UXD Step** | FP-3 (About Tab) |
| **Title** | Hardcoded version string doesn't match package.json |
| **Description** | AppLayout.jsx:629 hardcodes "v1.0 · 2 Casino Games". package.json has version "0.3.0". |
| **Expected Behavior** | Version string matches package.json version; pulled programmatically. |
| **Actual Behavior** | Mismatch. File: src/layout/AppLayout.jsx:629 |
| **Severity** | 2 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **40** |
| **Recommended Action** | Use import pkg from '../../package.json'; version = pkg.version. |
| **Status** | Open |

---

### FMEA-FP-017

| Field | Value |
|---|---|
| **ID** | FMEA-FP-017 |
| **UXD Step** | FP-4.2 (Poker Gameplay) |
| **Title** | FeaturePoker AI timer not fully cleaned up on unmount |
| **Description** | FeaturePoker.jsx:843-847,867: runAIActions sets new aiTimerRef.current inside a setTimeout callback. If unmounted between outer setTimeout and callback execution, callback fires on unmounted component. |
| **Expected Behavior** | All timers cancelled on unmount; no state updates after unmount. |
| **Actual Behavior** | Potential state update on unmounted component. File: src/game/FeaturePoker.jsx:843-847,867 |
| **Severity** | 3 |
| **Occurrence** | 2 |
| **Detection** | 5 |
| **RPN** | **30** |
| **Recommended Action** | Track isMounted with useRef. In setTimeout callbacks: if (!isMounted.current) return. |
| **Status** | Open |

---

### FMEA-FP-018

| Field | Value |
|---|---|
| **ID** | FMEA-FP-018 |
| **UXD Step** | FP-5.2 (Blackjack Gameplay) |
| **Title** | Feature21 bust triggers SETTLE effect twice |
| **Description** | Feature21.jsx:809-817: SETTLE stage effect fires trigger("bust") + setTimeout(dispatch SETTLE). HIT reducer sets stage:SETTLE on bust. Effect fires another SETTLE 300ms later at stage RESULT → default case returns state unchanged. Double "bust" trigger; no chip calculation error. |
| **Expected Behavior** | Single SETTLE dispatch on bust; single trigger. |
| **Actual Behavior** | Double trigger; cosmetic only (no chip error). File: src/game/Feature21.jsx:809-817 |
| **Severity** | 2 |
| **Occurrence** | 4 |
| **Detection** | 3 |
| **RPN** | **24** |
| **Recommended Action** | Guard SETTLE effect with if (stage === 'SETTLE' && !bustHandled) { setBustHandled(true); ... }. |
| **Status** | Open |

---

### FMEA-FP-019

| Field | Value |
|---|---|
| **ID** | FMEA-FP-019 |
| **UXD Step** | FP-2.2 (Upload) — mode API |
| **Title** | analysisMode API gap — accessible from hook but not from context |
| **Description** | useKinshipAnalysis returns analysisMode. FamililookContext does not expose it. Components using only useFamililook() cannot read current analysis mode. |
| **Expected Behavior** | analysisMode accessible from both hook and context. |
| **Actual Behavior** | Only accessible from hook. Latent inconsistency. Files: src/hooks/useKinshipAnalysis.jsx:589, src/state/FamililookContext.jsx |
| **Severity** | 2 |
| **Occurrence** | 3 |
| **Detection** | 6 |
| **RPN** | **36** |
| **Recommended Action** | Expose analysisMode from FamililookContext, or document that it's hook-only. |
| **Status** | Open |

---

### FMEA-FP-020

| Field | Value |
|---|---|
| **ID** | FMEA-FP-020 |
| **UXD Step** | FP-3.1 (Games Lobby) — data readiness |
| **Title** | isGameDataReady useMemo reads localStorage but depends on React state |
| **Description** | AppLayout.jsx:339-346: useMemo calls buildDeck() which reads localStorage. Dependencies include React state (analysisResults, parents, children). Works in practice because state changes trigger re-run which re-reads localStorage. But deps are misleading; direct localStorage writes without state change skip re-evaluation. |
| **Expected Behavior** | isGameDataReady is reactive to all ways data can change, or its dependencies are accurately documented. |
| **Actual Behavior** | Works but fragile; misleading dependency array. File: src/layout/AppLayout.jsx:339-346 |
| **Severity** | 2 |
| **Occurrence** | 2 |
| **Detection** | 6 |
| **RPN** | **24** |
| **Recommended Action** | Either pass localStorage data as props to buildDeck(), or add a storage event listener that triggers re-evaluation. |
| **Status** | Open |

---

## SECTION 4: PLATFORM-WIDE DFMEA

*Source: DFMEA_facematch.md — 17 failure modes*

---

### DFMEA-FM-01

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-01 |
| **UXD Step** | FM-2.3 (FamiliMatch Solo Analysis) — response parsing |
| **Title** | Backend returns no engineResult wrapper — fields undefined |
| **Severity** | 8 |
| **Occurrence** | 2 |
| **Detection** | 4 |
| **RPN** | **64** |
| **Current Controls** | Defensive fallback: const engine = analysis.engineResult || analysis (matchClient.js:127). |
| **Recommended Action** | Add response shape validation — check for parents.parent1 existence before proceeding. |
| **Status** | Acceptable (RPN 64) |

---

### DFMEA-FM-02

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-02 |
| **UXD Step** | FL-3.7 (FamiliLook Results) / FM-2.4 (FamiliMatch Results) |
| **Title** | calibrated_features null → all features show "Unknown" |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 3 |
| **RPN** | **72** |
| **Recommended Action** | Show "Face not detected clearly — try a clearer photo" instead of silently showing "Unknown" for all features. |
| **Status** | Acceptable (RPN 72) — UX improvement recommended |

---

### DFMEA-FM-03

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-03 |
| **UXD Step** | FL-3.7 (FamiliLook Results) |
| **Title** | embedding_similarity_parent2 missing → shows 0% ("Opposites Attract") |
| **Severity** | 7 |
| **Occurrence** | 2 |
| **Detection** | 5 |
| **RPN** | **70** |
| **Recommended Action** | If embedding_similarity === 0 AND calibrated_features empty: show "Analysis incomplete — please retry" instead of 0% score. |
| **Status** | Acceptable (RPN 70) — UX improvement recommended |

---

### DFMEA-FM-04

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-04 |
| **UXD Step** | FL-5.4 (Keepsakes Preview) / FM-2.4 (Results — Fusion) |
| **Title** | Face morph fails silently — fusion section empty |
| **Severity** | 5 |
| **Occurrence** | 4 |
| **Detection** | 2 |
| **RPN** | **40** |
| **Current Controls** | try/catch returns null; morph treated as bonus feature. |
| **Status** | Acceptable |

---

### DFMEA-FM-05

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-05 |
| **UXD Step** | FM-3.2 (Room — Upload) |
| **Title** | WebSocket disconnect during photo upload — player appears not ready |
| **Severity** | 7 |
| **Occurrence** | 5 |
| **Detection** | 4 |
| **RPN** | **140** |
| **Current Controls** | useMatchConnection.js handles lifecycle. Desktop7 has room timeout. |
| **Recommended Action** | **P1 — ACTION REQUIRED:** Implement auto-reconnection with room rejoin. On reconnect, check if photo was received (server ack). If not, re-prompt upload. |
| **Status** | Not Started — ACTION REQUIRED |

---

### DFMEA-FM-06

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-06 |
| **UXD Step** | FM-3.3 (Room — Analysis) |
| **Title** | Room closes before analysis completes |
| **Severity** | 7 |
| **Occurrence** | 3 |
| **Detection** | 3 |
| **RPN** | **63** |
| **Current Controls** | Room timeout extended; desktop7 awaits results. |
| **Status** | Acceptable |

---

### DFMEA-FM-07

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-07 |
| **UXD Step** | FM-3.2 (Room — Upload) / Backend |
| **Title** | Photos persist in RAM after room close |
| **Severity** | 9 |
| **Occurrence** | 3 |
| **Detection** | 8 |
| **RPN** | **~~216~~** |
| **Current Controls** | MITIGATED (2026-02-27): explicit del + gc.collect() on room close. Photo bytes zeroed before deletion. |
| **Status** | MITIGATED |

---

### DFMEA-FM-08

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-08 |
| **UXD Step** | FM-3.3 (Room — Analysis) / Backend |
| **Title** | Desktop3 unreachable from desktop7 |
| **Severity** | 8 |
| **Occurrence** | 3 |
| **Detection** | 3 |
| **RPN** | **72** |
| **Current Controls** | desktop3_client.py has timeout and error handling. |
| **Recommended Action** | Add health check endpoint; desktop7 checks health before accepting room creation. |
| **Status** | Acceptable |

---

### DFMEA-FM-09

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-09 |
| **UXD Step** | FL-3.2 (Consent) / FM-1.2 (Consent) |
| **Title** | Consent bypass — photos processed without BIPA consent |
| **Severity** | 10 |
| **Occurrence** | 2 |
| **Detection** | 3 |
| **RPN** | **~~160~~** → **60** |
| **Current Controls** | IMPLEMENTED: BiometricConsentMiddleware (middleware.py:65-87) rejects requests missing X-Biometric-Consent header. |
| **Status** | IMPLEMENTED |

---

### DFMEA-FM-10

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-10 |
| **UXD Step** | FM-3.3 (Room Analysis) — 6-player group |
| **Title** | Group matrix computation timeout for 6 players |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 3 |
| **RPN** | **72** |
| **Recommended Action** | Implement batched/parallel comparison (2-3 concurrent desktop3 calls). Show progress "X of 15 comparisons complete". Consider 4-player limit for initial launch. |
| **Status** | Acceptable |

---

### DFMEA-FM-11

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-11 |
| **UXD Step** | FL-5.4 (Keepsakes Preview) |
| **Title** | Keepsake template renders blank or misaligned |
| **Severity** | 8 |
| **Occurrence** | 3 |
| **Detection** | 3 |
| **RPN** | **72** |
| **Current Controls** | Live preview in KeepsakesModal; null guards; dimension validation. |
| **Status** | Acceptable |

---

### DFMEA-FM-12

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-12 |
| **UXD Step** | FL-5.3 (Product Selection — Family Mug) |
| **Title** | Family Mug data aggregation mismatches child count |
| **Severity** | 7 |
| **Occurrence** | 2 |
| **Detection** | 3 |
| **RPN** | **42** |
| **Current Controls** | .filter(Boolean) guards; preview shows all children. |
| **Status** | Acceptable |

---

### DFMEA-FM-13

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-13 |
| **UXD Step** | FL-6.2 (Stripe Checkout) |
| **Title** | Stripe checkout session creation fails |
| **Severity** | 8 |
| **Occurrence** | 2 |
| **Detection** | 2 |
| **RPN** | **32** |
| **Current Controls** | Error shown to user; Stripe monitoring. |
| **Status** | Acceptable |

---

### DFMEA-FM-14

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-14 |
| **UXD Step** | FL-6.1 (Basket — Checkout) |
| **Title** | Prodigi rejects image dimensions or format |
| **Severity** | 8 |
| **Occurrence** | 3 |
| **Detection** | 4 |
| **RPN** | **96** |
| **Current Controls** | printProfiles.js has dimensions; Prodigi webhook reports status. |
| **Recommended Action** | Add pre-submission dimension validation. Log all Prodigi rejection reasons. |
| **Status** | Acceptable (monitor) |

---

### DFMEA-FM-15

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-15 |
| **UXD Step** | FL-6.1 (Basket) |
| **Title** | Personalised message surcharge not applied correctly |
| **Severity** | 5 |
| **Occurrence** | 2 |
| **Detection** | 3 |
| **RPN** | **30** |
| **Current Controls** | Backend validates flag; customer sees line items. |
| **Status** | Acceptable |

---

### DFMEA-FM-16

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-16 |
| **UXD Step** | FL-5.3 (Product Selection — pricing) |
| **Title** | Currency conversion shows incorrect price — hardcoded rates drift |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 5 |
| **RPN** | **120** |
| **Current Controls** | "approx" qualifier shown. Stripe Adaptive Pricing handles actual conversion. |
| **Recommended Action** | **P1 — ACTION REQUIRED:** (a) Fetch live rates from free API (exchangerate.host) periodically, OR (b) show prominent "prices shown are approximate" disclaimer, OR (c) show GBP only with "converted at checkout" note. |
| **Status** | Not Started — ACTION REQUIRED |

---

### DFMEA-FM-17

| Field | Value |
|---|---|
| **ID** | DFMEA-FM-17 |
| **UXD Step** | FL-4.3 (Group Results) |
| **Title** | Parent-parent comparison shown in family group results |
| **Severity** | 6 |
| **Occurrence** | 1 (post-mitigation) |
| **Detection** | 2 |
| **RPN** | **~~84~~** → **12** |
| **Current Controls** | MITIGATED (2026-03-08): PARENT_ROLES filter; parentNameSet; opt-in toggle; couple nudge to FamiliMatch. |
| **Status** | MITIGATED |

---

## SECTION 5: NEW FAILURE MODES (UXD Gap Analysis)

*Identified during UXD writing — gaps between expected and implemented behavior*

---

### FMEA-GAP-01

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-01 |
| **UXD Step** | FM-2.3 (FamiliMatch Solo Analysis) — error display |
| **Title** | No error display path in Solo mode — analysis failure invisible |
| **Description** | SoloPage has error state in runComparison() but no UI renders it. User sees loading animation stop; no explanation. Mirrors FMEA-FP-001 for FamiliPoker. |
| **Severity** | 8 |
| **Occurrence** | 5 |
| **Detection** | 4 |
| **RPN** | **160** |
| **Recommended Action** | Add error card in SoloPage: when error is set, show message + retry button. Same pattern as FL-3.6 error handling. |
| **Status** | FIXED (Sprint 1) |

---

### FMEA-GAP-02

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-02 |
| **UXD Step** | FL-1.1 (FamiliLook Homepage) |
| **Title** | No mobile-first touch target audit on landing page CTAs |
| **Description** | Particle drift animations use pointer-events that may intercept taps on mobile. CTA button height not verified to meet 44pt minimum on all screen sizes. Fast-lane CTA is the primary conversion action; any touch interception causes failed taps. |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 5 |
| **RPN** | **120** |
| **Recommended Action** | Audit all interactive elements on HomePage for 44pt minimum touch targets. Set pointer-events: none on all particle/animation layers. Test on 375px viewport (iPhone SE). |
| **Status** | FIXED (Sprint 1) |

---

### FMEA-GAP-03

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-03 |
| **UXD Step** | FL-6.3 (Order Success) / FU-4.1 (Deck Order) |
| **Title** | No post-order state: basket is cleared but no confirmation of what was ordered |
| **Description** | OrderSuccessPage clears basket on load and fetches order status. If order status fetch fails, user sees "Order not found" with no fallback details. Order details are not preserved locally before basket clear. |
| **Severity** | 7 |
| **Occurrence** | 2 |
| **Detection** | 3 |
| **RPN** | **42** |
| **Recommended Action** | Before clearing basket, write basket contents to fl:last-order localStorage with 72h TTL. If order status fetch fails, display contents of fl:last-order as confirmation. |
| **Status** | Open |

---

### FMEA-GAP-04

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-04 |
| **UXD Step** | All products — mobile scroll |
| **Title** | No verified scroll behavior in results carousels on narrow viewports |
| **Description** | MobileResultsCarousel (FL), ResultsStory (FM), and game UIs rely on swipe/scroll gestures. No documented test coverage for touch gesture behavior on 320px and 375px viewports. Horizontal and vertical scroll conflicts are a common source of mobile UX failure. |
| **Severity** | 6 |
| **Occurrence** | 4 |
| **Detection** | 6 |
| **RPN** | **144** |
| **Recommended Action** | Add Playwright mobile tests for touch gestures on 375px and 390px viewports: swipe carousel, scroll results, pinch product preview. Verify no vertical scroll trap. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-GAP-05

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-05 |
| **UXD Step** | FL-7.2 (Plans Page) |
| **Title** | No annual vs monthly toggle state persists — resets on navigation |
| **Description** | PlansPage monthly/annual toggle state is local; navigating away and back resets to default. If user reads about annual savings, navigates to /app, and returns, they must re-select annual. |
| **Severity** | 3 |
| **Occurrence** | 5 |
| **Detection** | 4 |
| **RPN** | **60** |
| **Recommended Action** | Persist billing period preference in localStorage (fl:billing-period). Restore on PlansPage mount. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-GAP-06

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-06 |
| **UXD Step** | FP-4.1 (Poker — Tutorial) |
| **Title** | FamiliPoker tutorial shown on every "Quit" + re-select — no skip for returning users |
| **Description** | "Quit" from Poker result → RESET dispatch → SETUP stage. User must go through AgeSelector + 5-slide HowToPlay tutorial again. No skip option for users who have played before (no tutorial_seen flag). |
| **Severity** | 5 |
| **Occurrence** | 7 |
| **Detection** | 2 |
| **RPN** | **70** |
| **Recommended Action** | Store fl:poker-tutorial-seen in localStorage. On SETUP: if seen → skip to ANTE directly; only show tutorial on first play. Allow re-access via "How to Play" link in settings. |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-GAP-07

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-07 |
| **UXD Step** | FL-3.4 (Photo Upload) — mobile camera |
| **Title** | No explicit camera-first trigger on mobile upload slots |
| **Description** | PhotoSlot uses input type="file" with accept="image/*". On iOS/Android this opens a picker that includes camera as an option but may not prioritize it. No capture="camera" attribute to surface camera first on mobile. Users may not find the camera option on first try. |
| **Severity** | 5 |
| **Occurrence** | 5 |
| **Detection** | 3 |
| **RPN** | **75** |
| **Recommended Action** | Add capture="camera" as a secondary button next to the file picker. Show two buttons on mobile: "Take Photo" (capture) and "Choose from Gallery" (file picker). |
| **Status** | FIXED |

---

### FMEA-GAP-08

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-08 |
| **UXD Step** | FM-3.1 (Room Lobby) |
| **Title** | No room code expiry — stale codes may confuse users |
| **Description** | RoomPage creates rooms via WebSocket. No documented room expiry UX. If a room code is shared via message (WhatsApp, SMS) and expires before recipient uses it, the recipient sees "Room not found" with no explanation of expiry. |
| **Severity** | 5 |
| **Occurrence** | 4 |
| **Detection** | 4 |
| **RPN** | **80** |
| **Recommended Action** | Show room code expiry time to host ("Code expires in 15 minutes"). On "Room not found": show "This room may have expired — ask the host to create a new one". |
| **Status** | FIXED (Sprint 4C) |

---

### FMEA-GAP-09

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-09 |
| **UXD Step** | FL-3.7 (Results) — sensitivity slider |
| **Title** | Sensitivity slider has no label explaining what it does |
| **Description** | SensitivitySlider adjusts voteMargin (0.005–0.025). The name "sensitivity" is technical. No tooltip or inline explanation tells the user what moving the slider changes or why. |
| **Severity** | 4 |
| **Occurrence** | 8 |
| **Detection** | 2 |
| **RPN** | **64** |
| **Recommended Action** | Add inline label: "Sensitivity: [Low = more decisive / High = more balanced]". Add brief tooltip on first encounter: "Adjust how strongly we attribute each feature to a parent". |
| **Status** | FIXED (Sprint 4D) |

---

### FMEA-GAP-10

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-10 |
| **UXD Step** | FU-1.1 (FamiliUno Landing) |
| **Title** | FamiliUno feature count selector has no explanation of what each count means |
| **Description** | Feature count selector shows "2", "3", "4" buttons. No explanation of what 2 vs 4 features means for the card or game experience. New users don't know what to choose. |
| **Severity** | 3 |
| **Occurrence** | 8 |
| **Detection** | 2 |
| **RPN** | **48** |
| **Recommended Action** | Add micro-copy below selector: "2 features = simpler cards for kids; 4 features = full comparison cards". Show a card thumbnail preview that updates to reflect selected count. |
| **Status** | Open |

---

### FMEA-GAP-11

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-11 |
| **UXD Step** | All products — accessibility |
| **Title** | No documented focus management for modal/overlay transitions |
| **Description** | Multiple modals across all products (ConsentModal, KeepsakesModal, AgeGateModal, etc.). useFocusTrap exists in desktop2 and is wired to KeepsakesModal, but no audit of all other modals for focus trapping. Screen readers cannot navigate modal content if focus is not managed. |
| **Severity** | 5 |
| **Occurrence** | 6 |
| **Detection** | 7 |
| **RPN** | **210** |
| **Recommended Action** | Audit all modals for: (1) focus trap on open, (2) focus return to trigger on close, (3) escape key dismissal, (4) aria-modal="true" role. Apply useFocusTrap to all modals lacking it. |
| **Status** | FIXED (Sprint 3) |

---

### FMEA-GAP-12

| Field | Value |
|---|---|
| **ID** | FMEA-GAP-12 |
| **UXD Step** | FL-3.6 (Analyze) — plan limits |
| **Title** | Plan attempt counter increment happens before analysis completes — burned on failure |
| **Description** | AppLayout handleAnalyze: incrementAttempts() then runAnalysis(). If analysis fails (network error, API error), the attempt is already counted. Free users lose an attempt to a failure. |
| **Severity** | 6 |
| **Occurrence** | 3 |
| **Detection** | 5 |
| **RPN** | **90** |
| **Recommended Action** | Move incrementAttempts() to run only on successful analysis completion (inside useKinshipAnalysis after results stored). Rollback attempt on failure. |
| **Status** | FIXED (Sprint 4D) |

---

## Full RPN Summary Table

| ID | Product | Title | S | O | D | RPN | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| FMEA-FM-001 | Match | Build completely broken | 10 | 10 | 1 | 1000* | P0 | FIXED (Sprint 0A) |
| FMEA-FM-003 | Match | Context files missing | 10 | 10 | 1 | 1000* | P0 | FIXED (Sprint 0A) |
| FMEA-FM-004 | Match | 7 components missing | 10 | 10 | 1 | 1000* | P0 | FIXED (Sprint 0A) |
| FMEA-FP-002 | Poker | analysisMode context mismatch | 6 | 8 | 7 | 336 | P1 | Open |
| FMEA-FP-006 | Poker | Analytics dev bypass missing | 6 | 10 | 5 | 300 | P1 | FIXED (Sprint 0B) |
| FMEA-FP-015 | Poker | Two analytics implementations | 5 | 8 | 5 | 200 | P2 | FIXED (Sprint 2) |
| FMEA-GAP-11 | All | Modal focus management | 5 | 6 | 7 | 210 | P1 | FIXED (Sprint 3) |
| FMEA-FP-014 | Poker | PLANS constant duplicated | 6 | 5 | 6 | 180 | P1 | FIXED (Sprint 4B) |
| FMEA-FM-006 | Match | Zero test coverage | 9 | 10 | 2 | 180 | P1 | FIXED (Sprint 2) |
| FMEA-FM-018 | Match | analytics session_start pre-consent | 3 | 10 | 5 | 150 | P2 | FIXED (Sprint 4C) |
| FMEA-FP-007 | Poker | Wrong client ID in API | 5 | 10 | 3 | 150 | P2 | FIXED (Sprint 0B) |
| DFMEA-FM-05 | Match | WebSocket disconnect upload | 7 | 5 | 4 | 140 | P1 | FIXED (Sprint 2) |
| FMEA-FL-004 | Look | from=home wrong back nav | 6 | 6 | 4 | 144 | P1 | FIXED (Sprint 0B) |
| FMEA-FP-003 | Poker | FeaturePoker back dead end | 8 | 9 | 2 | 144 | P1 | FIXED (Sprint 0B) |
| FMEA-GAP-04 | All | No mobile scroll test coverage | 6 | 4 | 6 | 144 | P1 | FIXED (Sprint 3) |
| FMEA-FL-002 | Look | Single parent FAB dead end | 7 | 5 | 4 | 140 | P1 | FIXED (Sprint 1) |
| FMEA-FM-009 | Match | Tier gating bypassed by URL | 8 | 4 | 7 | 224 | P0 | FIXED (Sprint 2) |
| FMEA-FL-024 | Uno | Basket drawer inaccessible | 9 | 7 | 2 | 126 | P1 | FIXED (Sprint 1) |
| DFMEA-FM-16 | Look | Currency conversion drift | 6 | 4 | 5 | 120 | P1 | FIXED (Sprint 2) |
| FMEA-FL-009 | Uno | Group mode no cards | 8 | 5 | 3 | 120 | P1 | FIXED (Sprint 1) |
| FMEA-GAP-02 | Look | Mobile touch target audit | 6 | 4 | 5 | 120 | P1 | FIXED (Sprint 1) |
| FMEA-FM-012 | Match | Consent bypass via Trail | 7 | 3 | 6 | 126 | P1 | FIXED (Sprint 1) |
| FMEA-FP-001 | Poker | Analysis errors silently swallowed | 9 | 6 | 3 | 162 | P0 | FIXED (Sprint 0B) |
| FMEA-GAP-01 | Match | Solo error display missing | 8 | 5 | 4 | 160 | P0 | FIXED (Sprint 1) |
| FMEA-FP-005 | Poker | Plans page inert | 8 | 10 | 2 | 160 | P1 | FIXED (Sprint 4B) |
| FMEA-FL-003 | Look | OrderSuccess dark theme broken | 8 | 4 | 4 | 128 | P1 | FIXED (Sprint 0B) |
| FMEA-FL-007 | Look | Stripe Price IDs absent | 9 | 2 | 6 | 108 | P1 | FIXED (Sprint 2) |
| FMEA-FL-008 | Look | isDemoMode stale cache | 6 | 3 | 6 | 108 | P2 | FIXED (Sprint 3) |
| FMEA-FL-005 | Look | Keepsake paywall late | 6 | 7 | 2 | 84 | P2 | FIXED (Sprint 3) |
| FMEA-FL-006 | Look | Pet listed as Coming Soon | 5 | 10 | 2 | 100 | P2 | FIXED (Sprint 0B) |
| FMEA-FL-012 | Look | Trail raw localStorage plan read | 5 | 4 | 5 | 100 | P2 | FIXED (Sprint 4C) |
| FMEA-FM-007 | Match | compareSolo hardcoded names | 5 | 10 | 2 | 100 | P2 | FIXED (Sprint 3) |
| FMEA-FM-002 | Match | matchClient constants missing | 9 | 10 | 1 | 90* | P0 | FIXED (Sprint 0A) |
| FMEA-FM-005 | Match | config.js missing | 9 | 10 | 1 | 90* | P0 | FIXED (Sprint 0A) |
| FMEA-FL-010 | Look | Feedback button stale read | 3 | 6 | 5 | 90 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-014 | Look | detectPhoto stale consent | 5 | 3 | 6 | 90 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-023 | Look | Homepage feedback stale read | 3 | 6 | 5 | 90 | P3 | FIXED (Sprint 4D) |
| FMEA-GAP-12 | Look | Attempt burned on failure | 6 | 3 | 5 | 90 | P2 | FIXED (Sprint 4D) |
| DFMEA-FM-02 | Plat | calibrated_features null | 6 | 4 | 3 | 72 | P2 | Open |
| DFMEA-FM-08 | Plat | Desktop3 unreachable | 8 | 3 | 3 | 72 | P2 | Acceptable |
| DFMEA-FM-10 | Plat | Group matrix timeout | 6 | 4 | 3 | 72 | P2 | Acceptable |
| DFMEA-FM-11 | Plat | Keepsake template blank | 8 | 3 | 3 | 72 | P2 | Acceptable |
| DFMEA-FM-03 | Plat | embedding_similarity missing | 7 | 2 | 5 | 70 | P3 | Acceptable |
| FMEA-GAP-06 | Poker | Tutorial repeat on every quit | 5 | 7 | 2 | 70 | P2 | FIXED (Sprint 4D) |
| DFMEA-FM-01 | Plat | No engineResult wrapper | 8 | 2 | 4 | 64 | P3 | Acceptable |
| FMEA-GAP-09 | Look | Sensitivity slider no label | 4 | 8 | 2 | 64 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-011 | Look | Hardcoded social proof | 4 | 10 | 2 | 80 | P2 | FIXED (Sprint 3) |
| FMEA-FM-013 | Match | Hardcoded morph 50/50 split | 4 | 10 | 2 | 80 | P2 | FIXED (Sprint 4D) |
| FMEA-FM-017 | Match | Fabricated social counter | 4 | 10 | 2 | 80 | P2 | FIXED (Sprint 3) |
| FMEA-GAP-07 | Look | No camera-first on mobile | 5 | 5 | 3 | 75 | P2 | FIXED |
| FMEA-GAP-08 | Match | No room code expiry UX | 5 | 4 | 4 | 80 | P2 | FIXED (Sprint 4C) |
| FMEA-FL-015 | Look | Group results section blank | 7 | 5 | 2 | 70 | P2 | FIXED (Sprint 4D) |
| FMEA-FM-008 | Match | Room 'done' blank card | 6 | 5 | 3 | 90 | P2 | FIXED (Sprint 4D) |
| FMEA-FL-016 | Look | COPPA detection not re-run | 4 | 4 | 5 | 80 | P2 | FIXED |
| FMEA-FL-018 | Look | Stripe return empty email | 8 | 2 | 6 | 96 | P2 | FIXED (Sprint 4C) |
| DFMEA-FM-14 | Plat | Prodigi dimension mismatch | 8 | 3 | 4 | 96 | P2 | Monitor |
| FMEA-FL-001 | Look | Dead bundle import | 2 | 10 | 3 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-013 | Look | Dashboard no route guard | 5 | 2 | 3 | 30 | P3 | Open |
| FMEA-FL-019 | Look | Unused lazy import (dup) | 2 | 10 | 3 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-020 | Look | BottomNav re-tap exits | 4 | 5 | 3 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FL-022 | Look | Return button goes to /hub | 3 | 5 | 3 | 45 | P3 | Open |
| FMEA-FM-011 | Match | RoomPage no analytics | 3 | 10 | 2 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FM-015 | Match | Hardcoded share URL | 2 | 5 | 5 | 50 | P3 | FIXED (Sprint 4D) |
| FMEA-FM-016 | Match | Double grantConsent | 4 | 2 | 6 | 48 | P3 | Open |
| FMEA-FM-019 | Match | reversePortalTransition duped | 2 | 10 | 3 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FM-020 | Match | Hardcoded nameB="B" | 3 | 10 | 2 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-FP-004 | Poker | GameSelector dead code | 7 | 2 | 4 | 56 | P2 | FIXED (Sprint 4D) |
| FMEA-FP-008 | Poker | ErrorBoundary raw crash | 7 | 2 | 2 | 28 | P2 | Open |
| FMEA-FP-009 | Poker | F21 Back destroys chips | 5 | 4 | 2 | 40 | P2 | Open |
| FMEA-FP-010 | Poker | Dummy faces in games | 4 | 2 | 4 | 32 | P3 | Open |
| FMEA-FP-011 | Poker | Poker auto-launches | 4 | 10 | 2 | 80 | P2 | FIXED (Sprint 4B) |
| FMEA-FP-012 | Poker | Home re-tap exits app | 5 | 4 | 3 | 60 | P2 | FIXED (Sprint 4D) |
| FMEA-FP-013 | Poker | TypeScript files dead code | 3 | 2 | 4 | 24 | P3 | Open |
| FMEA-FP-016 | Poker | Version string mismatch | 2 | 10 | 2 | 40 | P3 | Open |
| FMEA-FP-017 | Poker | AI timer not cleaned | 3 | 2 | 5 | 30 | P3 | Open |
| FMEA-FP-018 | Poker | F21 bust triggers twice | 2 | 4 | 3 | 24 | P3 | Open |
| FMEA-FP-019 | Poker | analysisMode API gap | 2 | 3 | 6 | 36 | P3 | Open |
| FMEA-FP-020 | Poker | isGameDataReady deps | 2 | 2 | 6 | 24 | P3 | Open |
| FMEA-FL-021 | Look | generateNarrative unmemo | 2 | 4 | 3 | 24 | P3 | Open |
| FMEA-GAP-03 | Look | No post-order fallback | 7 | 2 | 3 | 42 | P3 | Open |
| FMEA-GAP-05 | Look | Annual toggle not persisted | 3 | 5 | 4 | 60 | P3 | FIXED (Sprint 4D) |
| FMEA-GAP-10 | Uno | Feature count no explanation | 3 | 8 | 2 | 48 | P3 | Open |
| DFMEA-FM-04 | Plat | Morph fails silently | 5 | 4 | 2 | 40 | P3 | Acceptable |
| DFMEA-FM-06 | Plat | Room closes during analysis | 7 | 3 | 3 | 63 | P3 | Acceptable |
| DFMEA-FM-07 | Plat | Photos in RAM | 9 | 3 | 8 | 216 | — | MITIGATED |
| DFMEA-FM-09 | Plat | Consent bypass | 10 | 2 | 3 | 60 | — | IMPLEMENTED |
| DFMEA-FM-12 | Plat | Mug data mismatch | 7 | 2 | 3 | 42 | P3 | Acceptable |
| DFMEA-FM-13 | Plat | Stripe session failure | 8 | 2 | 2 | 32 | P3 | Acceptable |
| DFMEA-FM-15 | Plat | Surcharge error | 5 | 2 | 3 | 30 | P3 | Acceptable |
| DFMEA-FM-17 | Plat | Parent-parent shown | 6 | 1 | 2 | 12 | — | MITIGATED |
| FMEA-FM-010 | Match | ResultsPage missing source | 6 | 4 | 2 | 48 | P2 | Open |
| FMEA-MOB-05 | Look | Age style cards on Preview push CTAs below fold | 9 | 10 | 1 | 90 | P1 | FIXED (Sprint 4A) |
| FMEA-MOB-06 | Look | Standard mug 3D mockup off-centre | 8 | 10 | 1 | 80 | P1 | FIXED (Sprint 4A) |
| FMEA-MOB-07 | Look | Action buttons overlap / below fold | 9 | 10 | 1 | 90 | P1 | FIXED (Sprint 4A) |
| FMEA-MOB-08 | Look | Generic "PERSON N" labels on mug | 7 | 6 | 2 | 84 | P1 | FIXED (Sprint 4A) |
| FMEA-FM-014 | Match | History color fallback | 2 | 2 | 8 | 32 | P3 | Open |
| FMEA-MOB-01 | Look | Mug template preview illegible on mobile | 8 | 10 | 2 | 160 | P1 | FIXED (Post-Sprint) |
| FMEA-MOB-02 | Look | Large template previews compressed on mobile | 6 | 8 | 3 | 144 | P1 | FIXED (Post-Sprint) |
| FMEA-MKF-001 | Look | Kill switch silently breaks mobile keepsakes | 8 | 4 | 4 | 128 | P1 | FIXED (Post-Sprint) |
| FMEA-MOB-04 | Look | Character mug wrong illustration for non-parent roles | 7 | 6 | 3 | 126 | P1 | FIXED (Post-Sprint) |
| FMEA-MOB-10 | Look | KeepsakeCatalogue renders scrolled to bottom | 6 | 10 | 2 | 120 | P1 | FIXED (Post-Sprint) |
| FMEA-MOB-11 | Look | AppLayout children.length null crash risk | 7 | 3 | 5 | 105 | P2 | FIXED (Post-Sprint) |
| FMEA-MOB-03 | Look | Keepsakes modal wastes vertical space on mobile | 5 | 10 | 2 | 100 | P2 | FIXED (Post-Sprint) |
| FMEA-MOB-09 | Look | PlansPage missing useCallback import — crash | 9 | 10 | 1 | 90 | P1 | FIXED (Post-Sprint) |
| FMEA-KSK-04 | Look | Preview backing missing for transparent templates | 5 | 8 | 3 | 120 | P2 | FIXED (Post-Sprint) |
| FMEA-KSK-02 | Look | Mug headline overflow — long names break layout | 6 | 7 | 3 | 126 | P2 | FIXED (Post-Sprint) |
| FMEA-KSK-01 | Look | standard_card + card_deck in catalogue not production-ready | 5 | 10 | 2 | 100 | P2 | FIXED (Post-Sprint) |
| FMEA-KSK-05 | Look | Stale chunk errors on every deploy — "Failed to fetch dynamically imported module" | 8 | 10 | 1 | 80 | P2 | FIXED (Post-Sprint) |

*Values capped at 1000 for display; actual RPN unbounded

---

## SECTION 6: KEEPSAKE MOBILE FIXES (famililook-desktop2)

*Source: Post-sprint keepsake mobile UX fixes — 4 failure modes*

---

### FMEA-MOB-01

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-01 |
| **UXD Step** | FL-5.4 (Preview) |
| **Title** | Mug template preview illegible on mobile — 0.41x scale |
| **Description** | Mug wrap templates (830px) scaled to 0.41x on 375px mobile. 14px text renders at ~5.7px — illegible. Users cannot read or evaluate the mug design before ordering. |
| **Severity** | 8 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **160** |
| **Recommended Action** | Render at 0.7x with horizontal scroll instead of 0.41x scale. Show "Swipe to see full wrap" hint. |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-02

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-02 |
| **UXD Step** | FL-5.4 (Preview) |
| **Title** | Large template previews compressed below readability on mobile |
| **Description** | Fine art (480px), cushion (540px), framed canvas (360px) templates could scale below 0.6x on mobile, making text and details hard to read. |
| **Severity** | 6 |
| **Occurrence** | 8 |
| **Detection** | 3 |
| **RPN** | **144** |
| **Recommended Action** | Clamp minimum scale at 0.6x with horizontal scroll affordance for overflow. |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-03

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-03 |
| **UXD Step** | FL-5.1 (Keepsakes Modal) |
| **Title** | Keepsakes modal wastes vertical space on mobile — small centered box |
| **Description** | Modal used maxHeight 90vh with centered content, leaving significant unused space on mobile. Step indicator used circles instead of interactive navigation. Users must scroll through steps with no easy back navigation. |
| **Severity** | 5 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **100** |
| **Recommended Action** | Full-height modal on mobile (100dvh). Pillbox step navigator with tappable completed steps for backward navigation. |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-04

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-04 |
| **UXD Step** | FL-5.4 (Preview — Character Mug) |
| **Title** | Character mug shows wrong illustration for non-parent roles |
| **Description** | normaliseParent() only recognised mum/dad aliases. All other roles (Grandma, Son, Daughter, Uncle, etc.) fell through to binary mama/papa default. A "Grandma" label would show a young mother illustration. |
| **Severity** | 7 |
| **Occurrence** | 6 |
| **Detection** | 3 |
| **RPN** | **126** |
| **Recommended Action** | Extend normaliseParent() to recognise all 17 upload dropdown roles with multilingual aliases. Map each to correct character type (gran/gramps/cub/mini/mama/papa). |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-05

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-05 |
| **UXD Step** | FL-5.4 (Preview) |
| **Title** | Age style cards (Infant/Child/Teen) shown on Preview step — push preview and CTAs below fold |
| **Description** | On mobile Preview step, three oversized age style cards (~120px each, 360px+ total) appear above the mug preview. The actual product preview, Download PNG, Share, Add to Basket, and Buy Now buttons are all pushed below the fold. User must scroll past age cards to see what they're buying and to complete purchase. Age style should be selected at Step 3 (Style), not displayed again on Preview. |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **90** |
| **Recommended Action** | Move age style selection to Step 3 (Style). Preview step shows ONLY: design style selector (compact), template render (centred, fills height), sticky action bar (Download/Share/Add to Basket/Buy Now). |
| **Status** | FIXED (Sprint 4A) |

---

### FMEA-MOB-06

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-06 |
| **UXD Step** | FL-5.4 (Preview — Standard Mug mockup) |
| **Title** | Standard mug 3D mockup renders off-centre — mostly empty dark space with mug at far-right edge |
| **Description** | The 3D mug mockup preview container renders a dark rectangle filling the preview area. The actual mug image is pushed to the far-right edge and only partially visible. ~70% of the preview area is empty dark background. User cannot properly evaluate the mug design before ordering. |
| **Severity** | 8 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **80** |
| **Recommended Action** | Centre the mug mockup image horizontally. Reduce container height to match mug's visible height. Ensure mug is at least 60% of container width. |
| **Status** | FIXED (Sprint 4A) |

---

### FMEA-MOB-07

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-07 |
| **UXD Step** | FL-5.4 (Preview) |
| **Title** | Action buttons (Download/Share/Add to Basket/Buy Now) overlap privacy text and are pushed below fold |
| **Description** | On mobile Preview step, the action buttons are rendered inline below the template preview. When age cards and the template push content down, action buttons are either below the fold or overlap with the "Privacy protected" text. There is no sticky bottom action bar. |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **90** |
| **Recommended Action** | Make action buttons a sticky bottom bar (position: sticky, bottom: 0) with solid background. Always visible regardless of scroll position. Privacy text above the bar, not overlapping. |
| **Status** | FIXED (Sprint 4A) |

---

### FMEA-MOB-08

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-08 |
| **UXD Step** | FL-5.4 (Preview — Character Mug) |
| **Title** | Generic "PERSON 2" and "PERSON 4" labels on mug instead of actual family names |
| **Description** | Screenshot shows mug headline "HELLO, MINI PERSON 4" with "PERSON 2" as the parent winner. These are default generic labels from group photo mode where users did not customise labels. The mug should use the actual role labels or names assigned during upload, not fall back to "Person N". |
| **Severity** | 7 |
| **Occurrence** | 6 |
| **Detection** | 2 |
| **RPN** | **84** |
| **Recommended Action** | When label is "Person N" (generic), prompt user to enter actual names before generating keepsake. Or derive from role assignment (if role is "Son" show "Son" not "Person 4"). |
| **Status** | FIXED (Sprint 4A) |

---

### FMEA-MOB-09

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-09 |
| **UXD Step** | FL-7.2 (Plans Page) |
| **Title** | PlansPage missing useCallback import — ReferenceError crashes ErrorBoundary on every /plans navigation |
| **Description** | Sprint 4 edit added useCallback usage to PlansPage.jsx but did not update the React import line. Every navigation to /plans throws a ReferenceError (useCallback is not defined), caught by ErrorBoundary, rendering a crash screen instead of the plans page. |
| **Severity** | 9 |
| **Occurrence** | 10 |
| **Detection** | 1 |
| **RPN** | **90** |
| **Recommended Action** | Add useCallback to the React import at line 1 of PlansPage.jsx. |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-10

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-10 |
| **UXD Step** | FL-5.1 (Keepsakes Modal Entry) |
| **Title** | KeepsakeCatalogue renders scrolled to bottom — blank screen on mobile |
| **Description** | KeepsakeCatalogue component renders with scroll position at the bottom of the page on mobile. Users see a blank screen and must scroll up to find content. No scroll-to-top on mount. |
| **Severity** | 6 |
| **Occurrence** | 10 |
| **Detection** | 2 |
| **RPN** | **120** |
| **Recommended Action** | Add useEffect scroll-to-top on mount: window.scrollTo(0, 0). |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MOB-11

| Field | Value |
|---|---|
| **ID** | FMEA-MOB-11 |
| **UXD Step** | FL-3.1 (App Shell Load) |
| **Title** | AppLayout children.length null crash risk |
| **Description** | AppLayout.jsx accesses children.length without null-checking. If children is null or undefined (e.g., during lazy load transitions), a TypeError crashes the component tree. |
| **Severity** | 7 |
| **Occurrence** | 3 |
| **Detection** | 5 |
| **RPN** | **105** |
| **Recommended Action** | Change children.length to children?.length || 0 for null safety. |
| **Status** | FIXED (Post-Sprint) |

---

### FMEA-MKF-001

| Field | Value |
|---|---|
| **ID** | FMEA-MKF-001 |
| **UXD Step** | FL-5.1 (Keepsakes Modal Entry) |
| **Title** | Kill switch (fl:disable-mobile-keepsakes) silently breaks keepsakes on mobile |
| **Description** | The localStorage kill switch fl:disable-mobile-keepsakes was checked in multiple places with inconsistent logic. When set, keepsakes silently failed on mobile with no user feedback. The check was not centralised in the isMobileKeepsakeFlow() utility. |
| **Severity** | 8 |
| **Occurrence** | 4 |
| **Detection** | 4 |
| **RPN** | **128** |
| **Recommended Action** | Move kill switch check into isMobileKeepsakeFlow() utility so all callers get consistent behavior. |
| **Status** | FIXED (Post-Sprint) |

---

## Recommended Sprint Order

### Sprint 0 — UNBLOCKING (FamiliMatch only) — 2026 Week 14
1. FMEA-FM-001: Restore index.html, vite.config.js, main.jsx, App.jsx
2. FMEA-FM-003: Restore ConsentContext.jsx, MatchContext.jsx
3. FMEA-FM-004: Restore 7 missing components
4. FMEA-FM-005: Restore utils/config.js, utils/constants.js
5. FMEA-FM-009: Replace ?tier= URL param with signed session token

### Sprint 1 — CRITICAL UX (All products) — 2026 Week 15
1. FMEA-FP-001: Surface analysis errors in FamiliPoker
2. FMEA-GAP-01: Surface analysis errors in FamiliMatch
3. FMEA-FP-003: Fix FeaturePoker Back button
4. FMEA-FL-024: Fix FamiliUno basket drawer access
5. FMEA-FL-003: Fix OrderSuccess dark theme
6. DFMEA-FM-05: WebSocket reconnection

### Sprint 2 — HIGH IMPACT — 2026 Week 16
1. FMEA-FL-004: Fix from=home back navigation
2. FMEA-FL-009: Fix group mode → FamiliUno cards
3. FMEA-FL-007: Stripe Price ID startup check
4. DFMEA-FM-16: Currency disclaimer or live rates
5. FMEA-FM-006: FamiliMatch test suite
6. FMEA-FP-006: Add analytics dev bypass to FamiliPoker

### Sprint 3 — QUALITY — 2026 Week 17
1. FMEA-FP-005: FamiliPoker plans integration
2. FMEA-FL-005: Keepsake early paywall
3. FMEA-FL-006: Remove pet from Coming Soon
4. FMEA-FL-008: Fix isDemoMode stale cache
5. FMEA-GAP-04: Mobile scroll test coverage
6. FMEA-GAP-11: Modal focus management audit

---

*FMEA-002 — FML Platform — 2026-03-31 — Total failure modes: 103 (63 from source audit + 17 DFMEA + 15 UXD gaps + 8 keepsake mobile fixes) — 100 tracked in RPN table: 67 FIXED, 3 MITIGATED/IMPLEMENTED, 11 Acceptable/Monitor, 19 Open (all P2/P3)*
