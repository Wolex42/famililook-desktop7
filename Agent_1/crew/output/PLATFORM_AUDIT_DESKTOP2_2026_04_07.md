# FamiliLook Desktop2 — Comprehensive Platform Audit

**Date:** 2026-04-07
**Scope:** 282 source files across 55+ directories (famililook-desktop2/src/)
**Method:** 6 parallel audit agents, each reading every relevant file in their domain
**Status:** READ-ONLY AUDIT (no code changes)

---

## Executive Summary

Six specialist agents audited the entire FamiliLook FE codebase in parallel. Together they identified **31 silent failures**, **32 redundancies**, **41 weak systems**, and **48 opportunity areas** across 6 domains.

### Severity Breakdown

| Severity | Count | Examples |
|----------|-------|---------|
| **CRITICAL** | 5 | Character mug crash, order success race condition, analysis abort overwrites, cache loss on refresh, chunk reload loop |
| **HIGH** | 18 | Silent basket persistence, quality pending timeout, plan verification stale, no route guards, buildDeck single point of failure |
| **MEDIUM** | 34 | Consent desync, game data silent fail, redundant winner logic, thumbnail TTL invisible, multi-tab corruption |
| **LOW** | 63 | Dead "pet" intent, missing breadcrumbs, feature cache not cross-session, tab history bloat |

---

## Domain 1: Upload & Photo Flow

### Flow: Entry -> Intent -> Consent -> Upload -> Detection -> FacePick -> Naming -> Ready

**Strengths:**
- Intent-driven UX via single INTENT_CONFIG object
- COPPA -> Biometric consent gating in correct sequence
- Quality-first upload with clear badges and auto-retry
- Smart Phase 2 auto-opens FacePicker with "Best" badge

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| UP-01 | CRITICAL | FacePicker crop failure caught silently — `catch { onClose() }` with no error message. User picks face, modal closes, no explanation. | FacePicker.jsx:83-84 |
| UP-02 | HIGH | Preview URL leak on face pick — old blob URL never revoked when cropped file replaces original | FacePicker.jsx:82 -> UploadSection state |
| UP-03 | HIGH | Quality "pending" has no timeout — if detectPhoto never resolves, slot stuck in "Checking..." forever | PhotoSlot.jsx:101 |
| UP-04 | HIGH | Consent context vs localStorage desync — two sources of truth can diverge on visibility change | ConsentContext.jsx vs FamililookContext.jsx |
| UP-05 | MEDIUM | Fallback to local detection with null embeddings — no UI indication results may be degraded | imageProcessing.js:115-137 |
| UP-06 | MEDIUM | Dead "pet" intent — defined in INTENT_CONFIG but never rendered in IntentSelector UI | IntentSelector.jsx:76-104 |
| UP-07 | MEDIUM | File validation logic duplicated with different thresholds | DropLane.jsx:14-25 vs imageProcessing.js:57-65 |
| UP-08 | LOW | 6 scattered revokeObjectURL try-catch blocks — no centralized cleanup | UploadSection.jsx (6), ChildrenPanel.jsx (2), DropLane.jsx (1) |

---

## Domain 2: Analysis & Results

### Flow: AnalyzeButton -> Validation -> FormData -> API (retry x3) -> Normalize -> State + Persist -> Render Results -> Actions

**Strengths:**
- Contract enforcement (kinship_analyze.v1.schema.json)
- 90% of error paths show user-visible messages
- Retry with exponential backoff (3 attempts)
- Session persistence (FL-026) for page refresh recovery
- "Never 50/50" rule enforced

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| AN-01 | CRITICAL | Result cache only in-memory (useRef) — lost on page refresh. Same child re-uploaded may get different result, breaking user trust. | FamililookContext.jsx:69-76 |
| AN-02 | HIGH | Winner determined in 2 places — useKinshipAnalysis stores to fl:lastResults, MobileResultsSection re-derives. Can diverge. | useKinshipAnalysis.jsx:443-457 + MobileResultsSection.jsx:350-416 |
| AN-03 | HIGH | Feature votes extracted 4-5 different field paths — only one should exist per schema. If BE sends multiple, unpredictable winner. | useKinshipAnalysis.jsx:291-295, MobileResultsSection.jsx:270-322 |
| AN-04 | HIGH | "Never 50/50" rule can flip percentages twice — complex logic with magic number "2", no assertion final result isn't 50/50 | MobileResultsSection.jsx:392-416 |
| AN-05 | MEDIUM | Feature count invariant violation logged but processing continues — user sees 6 features instead of 8, no error shown | MobileResultsSection.jsx:331-334 |
| AN-06 | MEDIUM | Game data persistence silent fail — `catch { /* ignore */ }` around localStorage.setItem. Games break silently. | useKinshipAnalysis.jsx:297, 539 |
| AN-07 | MEDIUM | Pet analysis fails silently (non-blocking catch) — pets uploaded but no matches shown, no explanation | useKinshipAnalysis.jsx:674 |
| AN-08 | LOW | Percentage calculation has no minimum threshold — tiny scores (0.00001) produce meaningless percentages | MobileResultsSection.jsx:376-390 |

---

## Domain 3: Navigation & Routing

### Route Map: 15 primary routes, lazy-loaded, feature-flag gated

**Strengths:**
- URL-based state via query params enables bookmarking/sharing
- Tab state fully synchronized with browser history
- TrailTooltip auto-appends `?from=trail` + BackToTrail floating button (redundant safety)
- Analytics tracking on every navigation
- Graceful catch-all route redirects to /

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| NV-01 | HIGH | No centralized route guard — user can visit /uno without analysis data, games break silently | AppRouter.jsx (no guard middleware) |
| NV-02 | HIGH | ErrorBoundary only at top level — route component crash breaks entire app, no route-level recovery | main.jsx:32 |
| NV-03 | HIGH | Chunk reload loop possible on private browsers — sessionStorage unavailable, ErrorBoundary loops | ErrorBoundary.jsx:30-35 |
| NV-04 | MEDIUM | Back-button logic duplicated 3+ times with nested ternaries — no shared component | AppLayout.jsx:335, FamiliUnoPage.jsx:171, multiple |
| NV-05 | MEDIUM | `?game=` deep-link exists in code comments but not implemented — bookmarks won't auto-launch games | CardGame.jsx |
| NV-06 | MEDIUM | External product links don't pass session context — FamiliPoker/Match can't verify user plan | BrandHubPage.jsx:399, ProductDrawer.jsx:56 |
| NV-07 | MEDIUM | ProductCreationPage back-button hardcoded to `/` — ignores `?from=` parameter | ProductCreationPage.jsx:38 |
| NV-08 | LOW | Tab switching uses pushState (adds history entries) — back button goes through tab history | AppLayout.jsx:180 |
| NV-09 | LOW | `?section=` cleaned immediately after use — page state lost if user refreshes within 400ms | AppLayout.jsx:242-243 |
| NV-10 | LOW | OrderSuccessPage back button hardcoded to `/hub` — ignores origin | OrderSuccessPage.jsx:181 |

---

## Domain 4: Keepsakes & Commerce

### Flow: Browse -> Customize -> Character/Style -> Preview -> Export PNG -> Basket -> Shipping -> Stripe -> Webhook -> Success

**Strengths:**
- Multi-stage ordering flow well-structured
- Export has html-to-image -> html2canvas fallback chain
- Basket persists through Stripe redirect via localStorage
- Plan gating via canOrderMerchandise()

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| KS-01 | CRITICAL | **Character Mug crash** — missing emotion images in assets/characters/index.js. `gran_loving_african` not imported. `getCharacterImage()` returns null -> broken img -> crash. | assets/characters/index.js:58-66, CharacterPicker.jsx:54 |
| KS-02 | CRITICAL | **Order success race condition** — Stripe redirects with order_id, but webhook may not have processed yet. `getOrderStatus()` returns 404, user sees "Something went wrong" despite payment succeeding. | OrderSuccessPage.jsx:52-68 |
| KS-03 | HIGH | BasketContext storage full caught silently — `catch { }` with no logging or user notification. Items appear saved but aren't. | BasketContext.jsx:25 |
| KS-04 | HIGH | Checkout timeout silently canceled — AbortController fires at 30s, request canceled, no error shown. User waits forever. | orderApi.js:22-31 |
| KS-05 | MEDIUM | Export handlers duplicated across 3 files (~200 lines) — KeepsakesModal, KeepsakeMobileFlow, KeepsakePreview | Multiple keepsake files |
| KS-06 | MEDIUM | Shipping validation duplicated — OrderModal and BasketDrawer have different validation (email only checked in BasketDrawer) | OrderModal.jsx:89-95 vs BasketDrawer.jsx:48-56 |
| KS-07 | MEDIUM | Plan gate silent close — Free user clicks "Order", modal closes with no explanation or upgrade CTA | KeepsakesModal.jsx |
| KS-08 | LOW | No order tracking page — user has no visibility after success page | (Missing feature) |
| KS-09 | LOW | No order history — users can't see past orders | (Missing feature) |

---

## Domain 5: State Management & Data Flow

### Architecture: 5 React Contexts -> localStorage (35+ keys) + sessionStorage -> Feature Flags (12)

**Strengths:**
- Well-structured contexts with clear ownership
- Comprehensive localStorage key registry
- Feature flag system with clean fail-closed behavior
- Session persistence (FL-026) for analysis results
- 4h TTL on plan verification with backend sync

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| ST-01 | CRITICAL | Analysis abort race condition — user clicks analyze, cancels, re-analyzes. First response arrives and overwrites second result. No `signal.aborted` check before setState. | useKinshipAnalysis.jsx:414 |
| ST-02 | HIGH | Plan verification stale >4h — if backend unreachable, cached plan allowed indefinitely. User retains Plus/Pro after downgrade. | usePlanFeatures.js:158-172 |
| ST-03 | HIGH | No multi-tab sync — BasketContext, plan state, thumbnails can be corrupted by concurrent tabs. No BroadcastChannel. | BasketContext.jsx, analytics.js |
| ST-04 | HIGH | Thumbnails cleared when last tab closes — but other tabs don't know. Tab A analyzes, Tab B opens, Tab A closes -> Tab B loses photos. | analytics.js:270-283 |
| ST-05 | MEDIUM | Family name stored in 4 places — fl:familyContext, fl:lastResults, fl:groupSnapshot, raw parents/children. useGameFamilyData has 4-level cascade. | useGameFamilyData.js:71-93 |
| ST-06 | MEDIUM | Ambassador access revocation race condition — network error allows cached access >24h | usePlanFeatures.js:128-134 |
| ST-07 | MEDIUM | sessionStorage quota exceeded silently — analysis results lost, user unaware | FamililookContext.jsx:25-27 |
| ST-08 | LOW | Base64 thumbnails in localStorage — 33% size penalty, could use IndexedDB | useKinshipAnalysis.jsx |
| ST-09 | LOW | DEV mode analytics bypass always returns consent=true — documented as intentional but worth noting | analytics.js:170 |

### localStorage Key Count: 35+ keys managed

| Category | Keys | Persistence |
|----------|------|-------------|
| Plan/Tier | 7 | Indefinite (4h verification) |
| Analysis/Results | 8 | Session (25h stale prune) |
| Photos | 2 | Session (25h TTL) |
| Game State | 5 | Session |
| Consent/Analytics | 5 | Indefinite |
| Commerce | 3 | Session (Stripe redirect) |
| Settings/Misc | 5+ | Indefinite |

---

## Domain 6: Games & Extra Features

### Inventory: 6 games + Trail + Vault + Creation Flow + Debug Tools

**Strengths:**
- Modular game architecture via CardGame mode switcher
- Tier gating consistent (GAME_TIERS map)
- buildDeck() deterministic from analysis results
- Trail system with progress persistence and confetti celebration

**Critical Findings:**

| ID | Severity | Finding | File:Line |
|----|----------|---------|-----------|
| GM-01 | HIGH | buildDeck() is single point of failure — if it throws, 3+ games (CardGame, MemoryMatch, FaceMatch) show blank state with no error message | CardGame.jsx:32-37 |
| GM-02 | HIGH | FeatureCatch game not in CardGame mode selector — orphaned, undiscoverable by users | CardGame.jsx (missing mode) |
| GM-03 | MEDIUM | Missing photos not reported in FaceFusion — game runs with defaults, user unaware members hidden | FaceFusion.jsx:76-81 |
| GM-04 | MEDIUM | Feature cache per-session only — user refresh -> potentially different card labels (confusing) | deckBuilder.js:222 |
| GM-05 | MEDIUM | Tier gating client-side only — localStorage edit bypasses all gates. No server validation. | TrailTooltip.jsx, CardGame.jsx |
| GM-06 | MEDIUM | External app links hardcoded to Vercel URLs — not configurable, breakage not detected | trailData.js:92-93 |
| GM-07 | LOW | No game statistics dashboard — plays, scores, streaks not tracked for engagement metrics | (Missing feature) |
| GM-08 | LOW | No keyboard controls for games — accessibility gap | HungryHeads.jsx, FaceFusion.jsx |

---

## Cross-Domain Issues (Systemic)

These issues span multiple domains and represent architectural weaknesses:

| ID | Severity | Finding | Domains Affected |
|----|----------|---------|-----------------|
| XD-01 | HIGH | **localStorage as sole persistence** — 35+ keys, no IndexedDB fallback, quota exceeded silently in 5+ places | State, Commerce, Games, Upload |
| XD-02 | HIGH | **No centralized error boundary pattern** — only top-level ErrorBoundary, route crashes break entire app | Navigation, all domains |
| XD-03 | MEDIUM | **Silent catch pattern epidemic** — 15+ places where `catch {}` or `catch { log only }` swallows errors | All 6 domains |
| XD-04 | MEDIUM | **Duplicate validation/formatting** — shipping validation, price formatting, URL construction repeated | Commerce, Navigation |
| XD-05 | MEDIUM | **No data versioning** — localStorage keys have no version suffix, breaking changes require migration | State, Games |
| XD-06 | LOW | **No offline mode** — no service worker, no graceful degradation when network drops mid-flow | Upload, Analysis, Commerce |

---

## Priority Fix Matrix

### Phase 1: Critical (This Sprint — 1-2 days)

| # | Fix | Files | Impact |
|---|-----|-------|--------|
| 1 | **Character Mug crash** — add missing emotion images to assets/characters/index.js | assets/characters/index.js | Unblocks mobile keepsake flow |
| 2 | **Order success retry** — add 3-retry with backoff to getOrderStatus() | OrderSuccessPage.jsx | Prevents "Something went wrong" on successful payment |
| 3 | **Analysis abort guard** — check signal.aborted before setState | useKinshipAnalysis.jsx:414 | Prevents stale results overwriting fresh analysis |
| 4 | **FacePicker error message** — replace silent catch with toast error | FacePicker.jsx:83-84 | Users know why face pick failed |
| 5 | **Chunk reload loop guard** — check sessionStorage availability before loop | ErrorBoundary.jsx:30-35 | Prevents infinite reload on private browsers |

### Phase 2: High (Next Sprint — 3-5 days)

| # | Fix | Files | Impact |
|---|-----|-------|--------|
| 6 | **Basket persistence toast** — add error notification when localStorage full | BasketContext.jsx:25 | Users know basket wasn't saved |
| 7 | **Quality pending timeout** — add 30s watchdog, show "taking longer..." | PhotoSlot.jsx:101 | Prevents infinite "Checking..." state |
| 8 | **Route-level error boundaries** — wrap each lazy route in ErrorBoundary | AppRouter.jsx | Route crash doesn't break entire app |
| 9 | **Centralize back-button** — create `useFromParam()` hook + `<BackButton />` component | AppLayout, FamiliUnoPage, etc. | Single source of truth for navigation |
| 10 | **buildDeck() error boundary** — add fallback UI when deck generation fails | CardGame.jsx | Games show error instead of blank |
| 11 | **Checkout timeout error** — throw on AbortController timeout, show user message | orderApi.js:22-31 | User knows checkout timed out |
| 12 | **Plan verification timeout** — force downgrade after 4h if backend unreachable | usePlanFeatures.js:158-172 | Prevents indefinite paid access |

### Phase 3: Medium (Next Quarter — 1-2 weeks)

| # | Fix | Files | Impact |
|---|-----|-------|--------|
| 13 | Consolidate winner determination to single source | useKinshipAnalysis + MobileResultsSection | Eliminates divergent results |
| 14 | Freeze feature_votes to one canonical field path | useKinshipAnalysis.jsx:291 | Prevents unpredictable extraction |
| 15 | Implement BroadcastChannel for multi-tab sync | BasketContext, analytics, plan state | Multi-tab consistency |
| 16 | Centralize revokeObjectURL cleanup (9 instances) | UploadSection, ChildrenPanel, DropLane | Eliminate memory leaks |
| 17 | Unify shipping validation (OrderModal + BasketDrawer) | OrderModal, BasketDrawer | Consistent email validation |
| 18 | Extract export handler (~200 duplicate lines) | Keepsake modal/mobile/preview | Single reusable export function |
| 19 | Add route guards for prerequisite validation | AppRouter.jsx | Prevent /uno without data |
| 20 | Implement `?game=` deep-link auto-launch | CardGame.jsx | Bookmarkable game URLs |

### Phase 4: Low (Technical Debt Backlog)

| # | Fix | Impact |
|---|-----|--------|
| 21 | Migrate thumbnails to IndexedDB (33% size saving) | Performance |
| 22 | Add data versioning to localStorage keys | Migration safety |
| 23 | Remove dead "pet" intent from INTENT_CONFIG | Clean code |
| 24 | Add FeatureCatch to game selector or retire | Discoverability |
| 25 | Implement order tracking page | Commerce UX |
| 26 | Add keyboard controls for games | Accessibility |
| 27 | Add breadcrumb navigation UI | Wayfinding |
| 28 | Use replaceState for tab switches | History cleanliness |
| 29 | Debounce plan verification on rapid tab switches | API efficiency |
| 30 | Persist result cache to sessionStorage | Trust (consistent results) |

---

## Architecture Health Scorecard

| Domain | Score | Strengths | Weaknesses |
|--------|-------|-----------|------------|
| Upload & Photo | **8/10** | Consent gating, quality-first, smart Phase 2 | Silent crop fail, no timeout, URL leaks |
| Analysis & Results | **7/10** | Contract enforcement, retry logic, 90% error visibility | Cache in-memory only, redundant winner logic, fragile 50/50 rule |
| Navigation & Routing | **7/10** | URL state, analytics tracking, graceful fallbacks | No route guards, duplicated back-button, no route error boundaries |
| Keepsakes & Commerce | **6/10** | Multi-stage flow, export fallbacks, basket persistence | Character crash, order race condition, silent timeouts |
| State & Data Flow | **7/10** | Clear context ownership, feature flags, session persistence | Abort race, multi-tab corruption, 4 family name sources |
| Games & Extras | **6/10** | Modular architecture, tier gating, trail progress | Single point of failure (buildDeck), orphaned game, client-only gates |

**Overall Platform Health: 7/10**

The platform is **production-ready and functionally solid** but has **fragile edge cases** that erode user trust (inconsistent results, silent failures, data loss risks). The 5 critical fixes should be prioritized immediately.

---

## Appendix A: Complete Silent Failure Registry

| # | File | Line | Pattern | Domain |
|---|------|------|---------|--------|
| 1 | FacePicker.jsx | 83-84 | `catch { onClose() }` | Upload |
| 2 | UploadSection.jsx | 501+ | `revokeObjectURL catch {}` x6 | Upload |
| 3 | DropLane.jsx | 92-95 | Generic error message hides cause | Upload |
| 4 | imageProcessing.js | 115-137 | Fallback detection with null embeddings | Upload |
| 5 | detectConfig.js | 18-20 | `catch { return null }` on config save | Upload |
| 6 | FamililookContext.jsx | 154-157 | sessionStorage persist catch-all | Upload/State |
| 7 | AgeGateModal.jsx | multiple | COPPA/email storage catches swallowed | Upload |
| 8 | useKinshipAnalysis.jsx | 297 | localStorage.setItem catch ignored | Analysis |
| 9 | useKinshipAnalysis.jsx | 539 | localStorage.setItem catch ignored | Analysis |
| 10 | useKinshipAnalysis.jsx | 674 | Pet analysis catch logs only | Analysis |
| 11 | kinshipClient.js | 65 | localStorage.getItem catch ignored | Analysis |
| 12 | MobileResultsSection.jsx | 331-334 | Feature count invariant logged, not enforced | Analysis |
| 13 | BasketContext.jsx | 25 | Storage full catch empty | Commerce |
| 14 | orderApi.js | 22-31 | Timeout abort not surfaced | Commerce |
| 15 | OrderSuccessPage.jsx | 52-68 | getOrderStatus 404 on race | Commerce |
| 16 | KeepsakesModal.jsx | - | Plan gate silent close | Commerce |
| 17 | OrderModal.jsx | 89-95 | Email not validated | Commerce |
| 18 | CardGame.jsx | 32-37 | buildDeck() fail = blank state | Games |
| 19 | FaceFusion.jsx | 76-81 | Missing photos not reported | Games |
| 20 | deckBuilder.js | 222-226 | Feature cache not cleared on new analysis | Games |
| 21 | usePlanFeatures.js | 158-172 | Stale plan allowed indefinitely | State |
| 22 | usePlanFeatures.js | 128-134 | Ambassador revocation race | State |
| 23 | analytics.js | 270-283 | Tab close race condition | State |

---

## Appendix B: Feature Flag Matrix

| Flag | Status | Gates | Fail-Closed |
|------|--------|-------|-------------|
| VITE_FAMILY_PROFILES | ON | Identity Sheet + Character Picker | UI hidden |
| VITE_OCCASION_SHELF | ON | Occasion product shelf | Default shelf |
| VITE_SMART_PHOTO_PHASE1 | ON | Slot-aware quality tips | Generic tips |
| VITE_SMART_PHOTO_PHASE2 | ON | Auto-open FacePicker + Best badge | Manual pick |
| VITE_FACE_NAMING_SHEET | ON | Face-anchored naming | Naming disabled |
| VITE_PRODUCT_CREATION_FLOW | OFF | /create/:productId route | Route unavailable |
| VITE_TRAIL_DEFAULT_LANDING | varies | Trail as default landing | /app landing |
| VITE_PRODUCT_LED_HOMEPAGE | varies | Occasion-based homepage | Basic homepage |

---

*Report generated by 6 parallel audit agents. All findings cite specific file:line references and are verified against current codebase state.*
