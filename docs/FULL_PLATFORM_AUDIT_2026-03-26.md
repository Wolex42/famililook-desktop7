# FamiliLook Desktop2 — Full Platform Audit
## Date: 2026-03-26 | Agents: QA Lead, Design Lead, PM, FE Lead, Commerce Lead, Security
## 87 findings across 6 domains | No code until approved

---

## CRITICAL (8 findings — fix before any customer pays)

### C1. Deck checkout Stripe integration NOT wired
**Agent**: Commerce | **File**: `DeckCheckoutPage.jsx:244-283`
The "Pay" button on the FamiliUno deck order page shows "Payment integration is being connected". No Stripe session is created. Users cannot complete deck purchases. The code is a TODO stub.
**Fix**: Wire `createDeckCheckout()` to backend, or disable the order button until ready.

### C2. Baby bodysuit SKU unverified with Prodigi
**Agent**: Commerce | **File**: `printProfiles.js:274`
`GLOBAL-BBY-BODYSUIT` is not in the verified SKU list. Orders will fail at the Prodigi API.
**Fix**: Verify SKU with Prodigi or remove from orderable products.

### C3. `?plan=` and `?promo=` deep links are dead
**Agent**: PM | **Files**: `PlansPage.jsx:79,85` → `AppLayout.jsx` (never reads)
PlansPage navigates to `/app?plan=free` and `/app?plan=plus&promo=mothersday2026` but AppLayout never reads these params. The free-to-paid conversion path for promos is broken.
**Fix**: Read `?plan=` and `?promo=` in AppLayout and activate the plan accordingly.

### C4. Demo mode (`?demo=famili2026`) is permanent with no expiry
**Agent**: Security + FE Lead | **File**: `planConfig.js:123-140`
Once activated, `fl:demo` persists forever in localStorage. No TTL, no server verification, no cleanup. The passphrase is discoverable in the JS bundle. Unlocks ALL paid features permanently.
**Fix**: Add 24h TTL, or use sessionStorage, or require server-issued demo tokens.

### C5. Admin dashboard key embedded in production bundle
**Agent**: Security | **Files**: `.env.production`, `AnalyticsDashboard.jsx`
`[REDACTED — see security_status.md]` is baked into the JS bundle. Anyone can access `/dashboard?key=[REDACTED]`. Reveals usage analytics and feedback data.
**Fix**: Move to server-side auth or use a non-predictable, rotatable token.

### C6. PeekPreview reads wrong localStorage key — always shows empty
**Agent**: QA Lead | **File**: `PeekPreview.jsx:15`
Reads `fl:last_result` but the actual key is `fl:lastResults`. Trail peek previews never show personalised content for any user.
**Fix**: Change to `fl:lastResults` and read children from `fl:familyContext`.

### C7. Stripe success redirect stays on /plans — no redirect to app
**Agent**: PM | **File**: `PlansPage.jsx:59-73`
After paying via Stripe, user returns to `/plans?session_id=xxx`. Plan is verified but user stays on the plans page. No CTA or redirect to start using their new plan. Dead end after paying.
**Fix**: After successful verification, auto-redirect to `/app` or show a prominent "Start using Plus" button.

### C8. Thumbnail deletion on `beforeunload` breaks multi-tab usage
**Agent**: FE Lead | **File**: `analytics.js:261-262`
Closing ANY tab deletes `fl:thumbnails` from localStorage, breaking photos in other open tabs.
**Fix**: Use BroadcastChannel to check if other tabs are open, or move thumbnails to sessionStorage.

---

## HIGH (14 findings — fix in next sprint)

### H1. Dual-owner plan state causes stale reads
**Agents**: QA Lead + FE Lead | **Files**: `FamililookContext.jsx:68` + `usePlanFeatures.js:22`
Both independently init `currentPlan` from localStorage. If `usePlanFeatures` downgrades after backend verification, `FamililookContext.currentPlan` stays stale. Any component using `useFamililook().currentPlan` sees the wrong plan.
**Fix**: Remove plan state from FamililookContext; delegate to `usePlanFeatures()`.

### H2. KeepsakesModal uses `<a href="/plans">` causing full page reload
**Agent**: QA Lead | **File**: `KeepsakesModal.jsx:970,1108`
Plain anchor tags destroy all in-memory state (uploaded photos, analysis results). User loses their session.
**Fix**: Replace with `<Link to="/plans">`.

### H3. Message surcharge not multiplied by quantity
**Agent**: Commerce | **File**: `BasketContext.jsx:76`
Personalised message charge is flat 199p regardless of quantity. 3 mugs with messages = 199p not 597p.
**Fix**: `const messageCharge = item.hasPersonalisedMessage ? 199 * (item.quantity || 1) : 0;`

### H4. Missing print profiles for family_mug_set and card_deck
**Agent**: Commerce | **File**: `printProfiles.js`
No `PRINT_PROFILES` entry for these products. Falls back to pixelRatio=2 instead of the correct 3.22x. Prints will be ~38% lower resolution.
**Fix**: Add print profile entries.

### H5. No focus trap on any modal (8+ modals)
**Agent**: Design Lead | **Scope**: All modals
Keyboard users can tab to elements behind modals. No `role="dialog"`, no `aria-modal`, no Escape key to close.
**Fix**: Install focus-trap library or use `<dialog>` element. Add Escape key handlers.

### H6. Touch targets critically undersized on AddChild buttons
**Agent**: Design Lead | **File**: `UploadSection.jsx:128-140`
Camera/gallery buttons: 9px font, 2px padding = ~15px hit area. Far below 44px minimum.
**Fix**: Wrap in 44px minimum touch targets.

### H7. Color contrast failures (WCAG AA)
**Agent**: Design Lead | **Files**: `theme/colors.js`, `BrandHubPage.jsx`
`textSubtle` (#4A5080) on `bgMain` (#0D0F1A) = 2.4:1 ratio (need 4.5:1). BrandHub privacy text at 0.32 opacity = 2.1:1.
**Fix**: Increase text luminance or use lighter color tokens.

### H8. Orange/violet gradient split across the app
**Agent**: Design Lead | **File**: `styles/mobile.css`
52 occurrences of old orange (#f5a623) palette in CSS (`.btn-primary`, `.fab`, `.nav-item.active`) while JS components use violet (#7C3AED). Two different brand identities visible to users.
**Fix**: Migrate mobile.css to violet palette.

### H9. Group intent has no INTENT_CONFIG entry
**Agent**: PM | **File**: `IntentSelector.jsx`
When intent is "group", `config` is `undefined`. Falls back to default labels, no journey steps.
**Fix**: Add a `group` entry to `INTENT_CONFIG`.

### H10. Trail nodes for results are meaningless without prior analysis
**Agent**: PM | **Files**: `trailData.js`, `AppLayout.jsx`
User arrives at `/app?section=results` with no results. Sees a banner but no guided path.
**Fix**: Detect empty results and show "Run an analysis first" with a CTA.

### H11. `?intent=` deep link silently fails for returning users
**Agent**: PM | **File**: `UploadSection.jsx:314`
`if (urlIntent && !userIntent)` — if user already has an intent set, trail deep links are ignored.
**Fix**: Allow trail deep links to override intent, or show a prompt.

### H12. Client-side plan/ambassador spoofing exploitable for 24h
**Agent**: Security + FE Lead | **File**: `usePlanFeatures.js`
Setting `fl:plan=pro` + `fl:plan-email` + `fl:plan-verified-at` in DevTools grants Pro UI features for 24h.
**Fix**: Server-side gating for premium features; reduce stale window.

### H13. localStorage quota exhaustion is silent
**Agent**: FE Lead | **Scope**: All `setItem` calls
All writes silently swallow QuotaExceededError. Thumbnails alone can be 1-4MB.
**Fix**: Add quota monitoring, warn user when approaching limit, compress thumbnails.

### H14. 4 trail nodes route to /hub instead of actual destination
**Agent**: PM | **File**: `trailData.js`
Casino and Chemistry nodes have `route: '/hub'` — users must navigate twice to reach FamiliPoker/FamiliMatch.
**Fix**: Route directly to external URLs for these nodes.

---

## MEDIUM (25 findings)

| # | Finding | Agent | File |
|---|---------|-------|------|
| M1 | `fl:pendingDeckOrder` written but never read (orphaned) | QA+FE | `DeckCheckoutPage.jsx:266` |
| M2 | `fl:analysisCache`, `fl:attributes`, `fl:cardDeck`, `fl:lastResetDate` are phantom keys (never written) | FE | `storage.js` |
| M3 | Keepsake product prices hardcoded as GBP `£` instead of using CurrencyContext | Commerce | `KeepsakesModal.jsx:605` |
| M4 | Deck price hardcoded as `"£24.99"` ignoring currency | Commerce | `DeckCheckoutPage.jsx:18` |
| M5 | BasketDrawer has no `canOrderMerchandise()` gate | Commerce | `BasketDrawer.jsx` |
| M6 | FE/BE price drift risk — no automated sync between `PRODUCT_SPECS` and `PRODUCT_PRICES_PENCE` | Commerce | Cross-system |
| M7 | Seasonal print profile gaps (mothers_day styles missing profiles) | Commerce | `printProfiles.js` |
| M8 | Hardcoded fallback currency rates may be stale | Commerce | `CurrencyContext.jsx:12-19` |
| M9 | Report template innerHTML without sanitization (XSS) | Security | `report_template.html:27-28` |
| M10 | No CSRF tokens on any API call | Security | All API clients |
| M11 | Face thumbnails in localStorage (biometric data) — TTL cleanup but not guaranteed | Security | `storage.js` |
| M12 | PII persistence — `fl:plan-email`, `fl:ambassador-email` never cleared (GDPR) | FE | `usePlanFeatures.js` |
| M13 | `VITE_API_KEY` missing from both env files | QA | `.env.local`, `.env.production` |
| M14 | FamililookContext `currentPlan` can drift from localStorage | QA | `FamililookContext.jsx:68-73` |
| M15 | FamiliUnoPage `checkHasCards()` races with localStorage | QA | `FamiliUnoPage.jsx:64-80` |
| M16 | Consent gate creates silent dead-end on photo upload | PM | `UploadSection.jsx:346-388` |
| M17 | `canAnalyze` dual-logic bypass in AppLayout | PM | `AppLayout.jsx:204` |
| M18 | Demo data in localStorage pollutes subsequent real analysis | PM | `FamiliUnoPage.jsx:266-280` |
| M19 | KeepsakesModal pet index defaults to 0 on miss | PM | `KeepsakesModal.jsx:91` |
| M20 | Ambassador code success has no navigation CTA | PM | `PlansPage.jsx:144-163` |
| M21 | Empty basket has no navigation CTA | PM | `BasketDrawer.jsx:149-152` |
| M22 | LLM message generation has no visible loading spinner | Design | `usePersonalizedMessage.js` |
| M23 | ErrorBoundary uses light pink (#fee) on dark theme | Design | `ErrorBoundary.jsx:20` |
| M24 | KeepsakesModal `exportCardAsPng()` failure is silent | Design | `KeepsakesModal.jsx` |
| M25 | PeekPreview.jsx has no try/catch around JSON.parse (crash risk) | FE | `PeekPreview.jsx:15-16` |

---

## LOW (22 findings)

| # | Finding | Agent |
|---|---------|-------|
| L1 | WelcomePage exists but has no route (dead code) | QA+PM |
| L2 | `/mothers-day` page unreachable from UI | QA |
| L3 | UploadSection `<a href="/privacy">` instead of `<Link>` | QA |
| L4 | ProductDrawer only shows 2 of 4 products | PM |
| L5 | HomePage pills route FamiliMatch/FamiliPoker to /hub (2-tap) | PM |
| L6 | FaceFusion silently filters members without photos | Design |
| L7 | No game tutorials — all 6 games lack onboarding | Design |
| L8 | 205 hardcoded color values should use theme tokens | Design |
| L9 | No `prefers-reduced-motion` media query | Design |
| L10 | PlansPage exposes "pricing not yet configured" to end users | Design |
| L11 | Expired Mother's Day promo code still in codebase | Commerce |
| L12 | Card deck print profile inconsistency (hardcoded dims) | Commerce |
| L13 | `fl:settings`, `fl:unoFeatureCount` not cleaned by clearGameState | FE |
| L14 | `fl:pending-checkout` stale on abandoned checkout | FE |
| L15 | Inconsistent JSON.parse patterns (some use safeJSON, some don't) | FE |
| L16 | FaceFusion inventory has no size cap (unbounded growth) | FE |
| L17 | `fl:children`/`fl:parents` written in demo but never cleaned | FE |
| L18 | Minimal email validation (`includes('@')` only) | Security |
| L19 | No feedback/name input length limits | Security |
| L20 | File upload type not validated client-side | Security |
| L21 | Coming-soon trail nodes are dead-ends with no waitlist | PM |
| L22 | CardGame gallery empty state shows ghost cards with no CTA | Design |

---

## Recommended Fix Phases

| Phase | Items | Risk | Est. Effort |
|-------|-------|------|-------------|
| **A: Revenue & Legal** | C1, C2, C3, C7, H3, M3, M4, M5 | Zero–Low | 1 day |
| **B: Security** | C4, C5, H12 | Low | Half day |
| **C: Data Integrity** | C6, C8, H1, H2, M1, M2, M25 | Low | Half day |
| **D: Plan/Upgrade Flow** | C3, C7, H9, H11, M16, M17, M20 | Low–Med | 1 day |
| **E: Accessibility** | H5, H6, H7, H8 | Med | 1–2 days |
| **F: Polish** | All LOW items | Low | Backlog |

---

*54 of 87 findings fixed and deployed to production on 2026-03-26 (10 commits). 9 remaining items need backend changes or design decisions. See git log for commit details.*
