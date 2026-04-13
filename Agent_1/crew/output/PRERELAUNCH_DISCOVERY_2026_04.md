# Pre-Relaunch Discovery — FamiliLook Platform
**Date:** 2026-04-13
**Prepared by:** COO (orchestrates) + Visual Director + Copywriter + Growth Monitor + CMO
**Status:** DRAFT — awaiting CEO approval before any implementation begins

---

## Section 1: Recurring Issues (Prioritised by Frequency + Impact)

### GROUP 1 — Flagged 3+ Times (Systemic)

| # | Issue | Appearances | Status | Pre-Relaunch Action |
|---|-------|-------------|--------|---------------------|
| 1.1 | **Silent catch / swallowed errors** | 7+ documents | PARTIALLY RESOLVED. AppErrorBus live, 23 high-severity migrated. ~40 residual in 24 files. ESLint gate active. | Monitor. No relaunch blocker. |
| 1.2 | **localStorage fragility / quota / thumbnails** | 6+ documents | STRUCTURALLY RESOLVED. AppStorage live, 230+ sites migrated, storage.js deleted. Underlying quota risk wrapped, not eliminated. | Thumbnail base64→IndexedDB migration needed post-relaunch. |
| 1.3 | **Divergent winner/feature/percentage logic** | 6+ documents | RESOLVED. resultsContract Phase 3 complete. All 6 consumers migrated. 209 lines inline derivation removed. | No action needed. |
| 1.4 | **VITE_API_KEY client-side exposure** | 4+ documents | OPEN. Rate limiting exists. Key extractable from bundle. | MEDIUM — server-side proxy long-term. Not a relaunch blocker but noted. |
| 1.5 | **Tier gating spoofable / no cross-product auth** | 5+ documents | PARTIALLY RESOLVED. JWT tier token exists for FamiliMatch. No shared auth. URL param spoofing possible. | HIGH before paid subscriptions go live. Not blocking free-tier relaunch. |
| 1.6 | **Keepsake mobile preview patch cycle** | 5+ documents, 5+ patches | RESOLVED. Parallel component tree approach. File frozen by CEO. | No action needed. |
| 1.7 | **Stale chunk errors on deploy** | 5 documents | RESOLVED. vercel.json no-cache, lazyWithReload.js, reload loop guard. | Adopt pattern in desktop4/desktop6. |
| 1.8 | **desktop4 framer-motion divergence** | 4 documents, deferred 4x | OPEN. ^11.0.0 vs canonical ^12.34.3. | LOW priority. Quick fix when desktop4 is next touched. |

### GROUP 2 — Flagged 2 Times (Recurring Pattern)

| # | Issue | Status | Action |
|---|-------|--------|--------|
| 2.1 | Order success race condition | FIXED (exponential backoff polling) | — |
| 2.2 | Hardcoded currency rates drifting | PARTIALLY FIXED (disclaimer added, rates still hardcoded) | Add staleness detection |
| 2.3 | No route prerequisite guards | PARTIALLY FIXED (error boundaries added, no prerequisite guards) | Add guards for /uno, /room |
| 2.4 | Consent context / localStorage desync | MITIGATED by AppStorage | Monitor |
| 2.5 | Fabricated social proof counters | FIXED (replaced with "Thousands of") | Need real data or remove |
| 2.6 | CI/CD gaps in backend repos | OPEN (desktop5: zero CI, 41 days inactive; desktop7: zero CI) | Add CI pipelines |
| 2.7 | Stripe webhook / order reconciliation fragility | OPEN | Build reconciliation script before keepsake marketing push |
| 2.8 | Prodigi image URL fragility | OPEN (Hetzner restart = failed order) | CDN or base64 upload |
| 2.9 | Back-button / navigation logic duplication | PARTIALLY FIXED | Build useFromParam hook |

### GROUP 3 — Deferred Repeatedly

| # | Issue | Times Deferred | Status |
|---|-------|---------------|--------|
| 3.1 | **CSP blocking ALL analytics** (RPN 640 — HIGHEST OPEN ITEM) | 14+ days since flagged | OPEN. If true, ALL conversion measurement is impossible. MUST verify and fix before relaunch. |
| 3.2 | **Single Hetzner server SPOF** (RPN 560) | Never acted on | OPEN. Add uptime monitoring at minimum. |
| 3.3 | No automated order reconciliation (RPN 216) | Recommended, never built | OPEN |
| 3.4 | Capacitor / mobile app init | Deferred post-relaunch | Expected |
| 3.5 | desktop4 framer-motion alignment | Deferred 4x | OPEN |

### GROUP 4 — "Fixed" But Reappeared

| # | Issue | Pattern |
|---|-------|---------|
| 4.1 | Missing React hook imports (build passes, runtime crashes) | No automated gate |
| 4.2 | KeepsakesModal patch cycle (5+ attempts) | Architecturally resolved via redesign |
| 4.3 | FamiliMatch tier gating bypass | LandingPage check exists, RoomPage route guard does not |
| 4.4 | Consent bypass via URL params | Primary fixed, secondary desync remains |

**Key finding:** Zero P0 or P1 code-level items remain. The three structural modules (AppErrorBus, AppStorage, resultsContract) eliminated the top 3 recurring code issues. Remaining risks are infrastructure-level (SPOF, no monitoring, no reconciliation) and security-level (API key, tier spoofing).

---

## Section 2: Competitor Analysis

### Category A — Family Photo Analysis & Resemblance

**FamiliLook's niche:** "Who does my baby look like?" — surprisingly underserved.

| Competitor | What They Do Better | What They Do Worse | Conversion | Pricing |
|-----------|--------------------|--------------------|------------|---------|
| **Face Match & Baby Similarity (SoftUpper)** | Native mobile app on both stores, quick one-tap "who does baby look like", ancestry/ethnicity estimation | No keepsake output, no game layer, results are disposable entertainment | 3-day free trial → weekly subscription | ~$4-7/week |
| **Fotor AI Baby Generator** | Massive user base from photo platform, generates predicted future baby face, strong SEO | Generates synthetic images (not real resemblance analysis), no physical products | Free tool → Fotor Pro subscription | Free basic; Pro ~$8.99/mo |
| **MakeMeBabies** | Zero-friction web tool, longstanding brand, celebrity face matching | Very dated UI, no AI feature analysis (simple morphing), no mobile app | Ad-supported | Free |

**FamiliLook advantage:** Only product combining scientific 8-feature analysis + physical keepsakes + card games. No competitor does all three.
**FamiliLook weakness:** No mobile app, no viral sharing loop, no install base, no social proof.

### Category B — Personalised Family Keepsakes & Gifts

| Competitor | What They Do Better | What They Do Worse | Conversion |
|-----------|--------------------|--------------------|------------|
| **Moonpig** | Brand trust, massive catalogue, gift-giving UX, delivery tracking, reviews | Generic personalisation (just add text/photo), no AI analysis, no unique value prop | Occasion-driven, £3-40 per item |
| **Snapfish / Photobox** | Photo book expertise, bulk order pricing, frequent discounts | No unique analysis, commodity products | Photo uploads → product builder |
| **Cornish Prints (benchmark)** | Premium quality communication, trust signals (reviews, guarantees), artisan positioning | Small catalogue, no tech, no analysis | Quality imagery → trust → purchase |

**FamiliLook advantage:** Keepsakes are *output of analysis*, not generic photo prints. The mug doesn't just have a photo — it has a story ("72% like Mum — here's the proof").
**FamiliLook weakness:** No product photography, no reviews, no trust signals, no quality guarantees visible.

### Category C — Family Card Games & Physical Products

| Competitor | What They Do Better | What They Do Worse | Conversion | Pricing |
|-----------|--------------------|--------------------|------------|---------|
| **Ivory Graphics (ivory.co.uk)** | 30+ years UK manufacturing, casino-grade card stock, full custom design service | B2B-focused, no consumer app, no AI, customer designs every card manually | Quote-request B2B model, free test pack as lead magnet | Custom quotes (bulk) |
| **Print From Your Sofa** | Consumer-friendly design tool, up to 55 custom photos/deck, 2-day delivery, Trustpilot 4.8/5 | Static photo cards only, no game rules, no AI content, customer curates all photos | Direct e-commerce | From ~£12.99/deck |
| **Boots Photo** | High-street trust, click-and-collect, gift packaging | Very basic (photo on back only), no game design, standard 52-card poker decks only | In-store + online | ~£14.99/deck |

**FamiliLook advantage:** FamiliUno cards are *personalised by AI analysis* — each card shows a family member's features. No competitor generates game content from facial analysis.
**FamiliLook weakness:** No physical product photography showing the card quality. No unboxing content.

### Category D — Face Compatibility & Matching

| Competitor | What They Do Better | What They Do Worse | Conversion | Pricing |
|-----------|--------------------|--------------------|------------|---------|
| **Gradient: You Look Like** | 50M+ installs, viral celebrity lookalike loop, full photo-editing suite bundled | Celebrity-focused not interpersonal, no "match with friend/partner" flow, aggressive paywall, privacy concerns | 3-day free trial → auto-renewing subscription | iOS: $14.99/mo or $57.99/yr; Android: $9.99/mo |
| **Star By Face** | Free web tool, instant celebrity match, no download | Celebrity only (not partner compatibility), no feature breakdown, ad-supported | Ad-supported | Free |
| **FacePair** | Free online face similarity checker, no account required, person-to-person comparison | Very basic percentage only, no feature breakdown, no chemistry labels, no app | Ad-supported | Free |

**FamiliLook (FamiliMatch) advantage:** Only product with real-time duo/group comparison via WebSocket, chemistry labels, 8-feature breakdown.
**FamiliMatch weakness:** Zero traffic, zero social proof, no viral sharing mechanic built into results.

### Category E — Family Engagement Apps

| Competitor | What They Do Better | What They Do Worse | Conversion | Pricing |
|-----------|--------------------|--------------------|------------|---------|
| **FamilyAlbum (Mitene)** | Unlimited free photo storage, 11 free prints/month, 300+ milestone tracker, massive user base, privacy-first | Pure photo storage — no AI, no games, no resemblance analysis, passive engagement | Freemium → Premium upsell (videos, storage) | Free; Premium $5.99/mo; Pro $10.99/mo |
| **Tinybeans** | Strong "private family sharing" brand, milestone tracker, photo books, ad-free premium | 20 uploads/month free, no AI, no games, relies on family posting consistently | Freemium → Tinybeans+ upsell | Free; Tinybeans+ $7.99/mo or $74.99/yr |
| **YouVersion (benchmark)** | 1B+ installs, world-class daily engagement, daily habit via Verse of the Day, 100% free | Not a family product, no photos, no AI, different audience | Donation-funded, no commercial conversion | 100% free (funded by Life.Church) |

### Competitive Moat Summary

| Dimension | Competitors Do This | FamiliLook Does This Differently |
|-----------|-------------------|--------------------------------|
| Resemblance | Simple percentage or celebrity match | 8-feature breakdown, winner determination, order-invariant |
| Keepsakes | Generic photo-on-product (Moonpig, Snapfish) | AI-insight-on-product — unique per family, not replicable |
| Card games | Upload your own photos onto cards (Print From Your Sofa) | Cards auto-generated from analysis data with game rules |
| Compatibility | Celebrity lookalike or basic % (Gradient, FacePair) | 8-feature chemistry analysis with multiplayer modes |
| Engagement | Passive photo albums (FamilyAlbum, Tinybeans) | Active game loop: analyse → play → order → share |

**No single competitor spans all five categories.** FamiliLook's moat is the vertical integration from AI analysis through digital gameplay to physical product fulfilment — each layer feeds the next.

**But competitors win on:** trust (Moonpig, Boots), social proof (Gradient 50M+, FamilyAlbum), install base, viral loops (Gradient celebrity sharing), and product quality communication (Cornish Prints). These are the gaps to close before relaunch.

**Strategic pricing insight:** Gradient charges $14.99/mo for celebrity lookalike. FamiliLook offers more (8-feature family analysis + keepsakes + games) but charges nothing for the core analysis. The product-led pivot is correct — the analysis should stay free; revenue comes from keepsakes where margins are real and competition (for AI-personalised keepsakes) is zero.

---

## Section 3: Analytics & Feedback Findings

### The Funnel (as measured)

```
Visitors (4-9/day, declining) → Page Views (31/day) → CTA Clicks (14 recorded)
                                                              ↓
                                                     Upload Start: 0
                                                              ↓
                                                     Analysis: 0
                                                              ↓
                                                     Purchase: 0
```

**0% upload conversion — ever.** Not a single real user has uploaded photos.

### Baseline Data

| Metric | Value | Date |
|--------|-------|------|
| Peak daily visitors | 9 | 2026-03-28 |
| Latest daily visitors | 4 | 2026-04-02 |
| CTA taps recorded | 14 | 2026-03-28 |
| Trail peeks | 141 | Cumulative |
| Uploads started (real users) | **0** | All time |
| Revenue (real users) | **£0** | All time |
| Revenue (internal/test) | £54.97 | 2026-04-01 to 04-05 |

### Root Cause Analysis (from funnel model)

The upload barrier is a **trust gap**, not a usability gap:
1. **Cold traffic won't upload children's photos** to an unknown brand
2. **Biometric consent modal** reinforces perceived risk even with friendly copy
3. **No social proof** — no reviews, no testimonials, no press mentions
4. **No organic acquisition** — no SEO traffic, no social traffic, no referrals
5. **Value proposition unclear** at the moment of the ask
6. **Traffic too low to measure** — need ~100 visitors/day to detect 1% conversion

### Analytics Gaps (blocking decision-making)

| Gap | Impact | Fix Effort |
|-----|--------|------------|
| CSP may be blocking analytics entirely | ALL measurement impossible | Quick (CSP header fix) — MUST VERIFY |
| No upload funnel step-level tracking | Can't identify where in upload flow users abandon | Medium |
| No session recording / heatmaps | Can't see what users actually do | Quick (Hotjar free tier) |
| No UTM / referral attribution | Can't distinguish traffic sources | Quick |
| No A/B test infrastructure | Can't optimise at current traffic levels anyway | Defer |
| API unreachable during this audit | No data newer than 2026-04-02 | Verify server status |
| FamiliMatch: no baseline data recorded | Unknown traffic/engagement | Wire analytics reporting |

### Break-Even Target

11 visitors/day at 1% blended conversion rate = 3.4 orders/month. Covers £22/month fixed costs. Current traffic is 3x below this minimum.

---

## Section 4: Value Moment Analysis Per Product

### FamiliLook — "The Reveal"

**The value moment:** Seeing "I look 72% like Mum!" with the 8-feature breakdown — the instant curiosity becomes a concrete, shareable answer.

**Are we delivering it?** The result preview on the homepage (`HomePage.jsx:278-320`) shows what users *would* see. But no real user has reached the actual results page because the upload barrier kills the funnel.

**What blocks it:**
- The value moment is *behind* the highest-friction action (uploading 3 photos including a child's face)
- Users must trust the brand before they'll provide biometric data
- The preview shows the *what* but not the *why it matters* (no emotional framing — "This is the mug your dad will use every morning")
- No video of someone else's reveal moment to create vicarious excitement

### FamiliMatch — "The Chemistry Score"

**The value moment:** Seeing your compatibility percentage and chemistry label ("78% — Magnetic Match") with someone you care about.

**Are we delivering it?** The landing page (`LandingPage.jsx:273-297`) shows a placeholder illustration (two grey person icons + a result card), not a real result. The emotional payload is hidden behind consent + upload.

**What blocks it:**
- "AI Facial Compatibility" (`LandingPage.jsx:250`) is the badge copy — technical, not emotional
- "Our AI analyses 8 facial features to discover your facial compatibility in seconds" — tells users what the tech does, not what they'll feel
- No example results, no social proof, no "see what Sarah and Tom got" moment
- Duo/Group (the fun modes) are locked behind Plus — first-time users only get Solo

### FamiliUno — "Holding Your Family's Cards"

**The value moment:** Holding a physical deck of cards with your family members' faces and features on them — the tangible, keep-forever moment.

**Are we delivering it?** No. The deck is accessible only *after* completing an analysis, hidden inside the results carousel as a product shelf item. No standalone entry point from the homepage.

**What blocks it:**
- No product photography showing a real card deck
- No unboxing content
- The occasion card "Holiday / vacation" (`HomePageOccasion.jsx:41-51`) mentions the deck but doesn't show it
- Users must complete the entire analysis flow before they even know the deck exists

### FamiliPoker — PARKED (skip)

---

## Section 5: Copy Audit Findings

### Finding 1: Homepage Tagline Rotation (HIGH IMPACT)

**File:** `HomePage.jsx:41-45`
**Current:** Three taglines rotate every 9 seconds:
1. "Who Do You Look Like Most — Mum or Dad?" / "AI scans 8 facial features to settle it once and for all."
2. "Finally Settle the Family Debate" / "Who do you really take after? Get a feature-by-feature breakdown."
3. "Turn your family photos into cards & treasures" / "Winner cards, memory games, and prints — all from one upload."

**Problem:** User may land during tagline #3 which buries the core value prop. Tagline #1 sub-copy ("AI scans 8 facial features") leads with technology. The CTAs ("See your results in 30 seconds", "Try it free — no sign-up") appear as sub-sub-text in grey — barely visible.

**Recommendation:** Pick ONE headline. Lead with emotion, not technology. CTA should be the second most prominent element on the page.

### Finding 2: Social Proof is Hollow (HIGH IMPACT)

**File:** `HomePage.jsx:256-262`
**Current:** "Thousands of families have discovered their story"

**Problem:** "Thousands of" is a placeholder that replaced a fabricated counter (FMEA FL-011). It communicates nothing and may actively harm trust — users can sense vagueness. There are no reviews, no testimonials, no press logos, no "as seen on" badges.

**Recommendation:** Remove until real social proof exists. Or replace with a specific, verifiable claim ("Built in London. Your photos never leave EU servers. Deleted after analysis.")

### Finding 3: FamiliMatch Landing Copy — Technical, Not Emotional (MEDIUM IMPACT)

**File:** `famililook-desktop6/src/pages/LandingPage.jsx:250, 268-270`
**Current badge:** "AI Facial Compatibility"
**Current sub-head:** "Our AI analyses 8 facial features to discover your facial compatibility in seconds."

**Problem:** Tells the user what the *machine* does, not what *they* will feel. "Facial compatibility" is clinical.

**Recommendation:** "How alike are you really?" / "Compare your faces, discover your chemistry — it takes 10 seconds."

### Finding 4: Occasion Cards Contain Internal Language (MEDIUM IMPACT)

**File:** `HomePageOccasion.jsx:26-109`
**Current examples:**
- "Secondary: framed canvas, greeting card." (line 36) — "Secondary" is product strategy language
- "AOV potential: £14–28" (line 37) — Average Order Value shown to customers
- "Photos needed: 2 (parent + child)" (line 36) — functional, not inviting
- "Strongest social sharing hook — people post this." (line 62) — internal marketing note

**Problem:** These occasion cards read like an internal product brief, not customer-facing copy. The `MetaGrid` component (`HomePageOccasion.jsx:151-195`) displays "Hero product", "Photos needed", "AOV potential" labels directly to users.

**Recommendation:** Rewrite all 6 cards as customer-facing copy. Remove all internal metrics. Replace "Photos needed" with "Just bring 2 photos". Remove "AOV potential" entirely.

### Finding 5: PlansPage Meta Description — Functional, Not Emotional (LOW IMPACT)

**File:** `PlansPage.jsx:22-26`
**Current:** "Choose your FamiliLook plan. Free tier with 3 analyses, Plus for unlimited analyses and card games, Pro for treasure prints and priority support."

**Problem:** Lists features, not outcomes. Who searches for "3 analyses"?

**Recommendation:** "See your family story for free — or go further with unlimited analyses, card games, and keepsake prints."

### Finding 6: Results Carousel Feature Descriptions — Good But Buried

**File:** `MobileResultsCarousel.jsx:49-100`
**Current:** Rich, human-friendly feature descriptions ("Elegantly elongated eye shape", "Classic almond-shaped eyes")

**Assessment:** This is actually good copy. But no user has ever reached it (0% upload conversion). The emotional payoff exists — it's just inaccessible.

### Finding 7: Mug Theme Headers — Functional, Not Celebratory

**File:** `mugThemes.js:72-80`
**Current occasion headers:**
- generic: "YOUR FAMILY RESEMBLANCE"
- heritage_gold: "FAMILY HERITAGE"
- ubuntu: "WE ARE FAMILY"

**Problem:** "YOUR FAMILY RESEMBLANCE" is clinical. It describes what the mug shows, not what it means.

**Recommendation:** "THE PROOF IS IN THE FACE" or "LOOK WHO TAKES AFTER MUM" (personalised by winner).

---

## Section 6: UI/UX Gap Analysis Against Benchmarks

### Benchmark 1: YouVersion — Navigation Feel, Emotional Engagement, Daily Return

| Dimension | YouVersion Standard | FamiliLook Current | Gap |
|-----------|--------------------|--------------------|-----|
| **Navigation structure** | Clean bottom nav, 5 clear tabs, instant switching, consistent across all screens | BottomNav exists (`BottomNav.jsx`) with Home/Settings/Basket, but navigation depth varies wildly — some flows are 4+ levels deep with inconsistent back-button behaviour | HIGH — navigation structure needs flattening and consistency |
| **Emotional engagement** | Every screen has warmth — soft gradients, serif type for quotes, celebration moments, daily verse cards | Homepage has particle effects and shimmer animations but these are decorative, not emotional. Results page has good feature descriptions but no celebration moment on reveal | MEDIUM — needs "wow" moment at result reveal |
| **Visual hierarchy** | One clear action per screen, generous whitespace, content-first (not chrome-first) | Homepage has 3 rotating taglines, event badges, social proof, preview card, occasion cards — too many competing elements. No clear single CTA above fold | HIGH — homepage needs radical simplification |
| **Loading states** | Skeleton screens, smooth transitions, never a blank white screen | Analysis uses spinner emoji (🔬→⏳), no skeleton screens, loading states are functional not delightful | MEDIUM |
| **Daily return hooks** | Daily verse, reading plans, streaks, community | No daily content, no reason to return after analysis. Trail badges exist but are progression-gated not time-gated | LOW priority pre-relaunch |
| **Micro-interactions** | Subtle haptics, smooth page transitions, celebration animations | `hapticLight` exists but only on results. No page transitions. Confetti exists for trail completion but unreachable | MEDIUM |

### Benchmark 2: Cornish Prints UK — Product Presentation, Trust Signals, Quality

| Dimension | Cornish Prints Standard | FamiliLook Current | Gap |
|-----------|------------------------|--------------------|-----|
| **Product photography** | Every product shown in context (mug on kitchen table, print on wall, card in hand). Multiple angles. Lifestyle shots. | ProductShelf uses **SVG illustrations** (`ProductShelf.jsx:24-80`) — cartoon mug, card fan, print rectangle. No real product photos. | CRITICAL — #1 gap. Users cannot visualise what they're buying. |
| **Trust signals** | Customer reviews, star ratings, "100% satisfaction guarantee", secure payment badges, delivery promise | Zero reviews, zero ratings, zero guarantees visible. Only trust signal is "Thousands of families" (vague). | CRITICAL — #2 gap. No reason to trust an unknown brand with money + photos. |
| **Quality communication** | "Museum-quality giclée", "324gsm", paper weight specs, colour accuracy promise, artisan language | Product descriptions exist in `PRODUCT_DISPLAY` (`ProductShelf.jsx:10-19`) — "Full-wrap print · 11oz · dishwasher safe", "324gsm · envelope included". But these are small text in a card, not quality storytelling. | HIGH — specs exist but presentation doesn't communicate premium. |
| **Checkout confidence** | Clear pricing, delivery timeline, return policy, payment options visible, progress indicator | Pricing visible in ProductShelf. No delivery timeline on product cards. Return policy buried in terms. No "order by X for delivery by Y". | HIGH |
| **Product detail pages** | Full page per product with multiple images, specs, reviews, related products | No product detail pages. Products shown only as small cards in a horizontal scroll shelf within results. | HIGH — need standalone product pages |

### Additional Findings from Deep UI Audit

| # | Finding | File | Impact |
|---|---------|------|--------|
| A | **Design token conflict** — `index.css` uses orange `#f5a623` accents while `colors.js` uses violet `#7C3AED`. Focus rings, text selection, `::selection` flash orange in a violet app. | `index.css` vs `theme/colors.js` | MEDIUM — CSS-only fix, outsized perceived-quality improvement |
| B | **All occasion countdown badges are STALE** — Easter (April 5) and Mother's Day UK (March 22) both past. Homepage shows NO occasion badges right now. The product-led conversion lever is invisible. | `HomePage.jsx` lines 14-28 | HIGH — immediate. Add Father's Day (June 21) + make occasions permanent, not time-gated |
| C | **Navigation uses emoji** (`🏠`, `⚙️`) instead of Lucide icons (already imported in project). Inconsistent cross-platform rendering, looks unprofessional. | `BottomNav.jsx`, `HomeTab.jsx`, `SettingsTab.jsx` | MEDIUM — low effort, high perceived quality lift |
| D | **Only 2 bottom nav tabs** (Home, About) — should be 4+ (Home, Trail, Keepsakes, Settings) to surface products as permanent destination | `BottomNav.jsx`, `AppLayout.jsx` | HIGH — products are currently buried behind analysis completion |
| E | **Pricing hidden until step 4 of 4** in KeepsakesModal. Users navigate 3 steps before seeing cost. | `KeepsakesModal.jsx` | HIGH — show price from step 2 onwards |
| F | **Intent selector uses emoji icons** (mirror, baby, family group) that are not universally recognisable at the most critical decision point | `IntentSelector.jsx` | MEDIUM — replace with preview images showing example results |

### Top 10 Most Impactful UI/UX Changes

| Rank | Change | Component/Page | Current State | Benchmark State | Impact |
|------|--------|---------------|---------------|-----------------|--------|
| **1** | **Replace SVG product illustrations with real product photography** | `ProductShelf.jsx`, all keepsake components | Cartoon SVGs of mugs, cards, prints | Lifestyle photography showing products in context | CRITICAL — users can't visualise what they're buying. This alone could unlock purchase intent. |
| **2** | **Add trust signals: reviews, guarantees, security badges** | New component needed, homepage + checkout | Zero trust signals beyond "Thousands of" | Star ratings, review quotes, "satisfaction guarantee", secure payment badges, "photos never stored" | CRITICAL — trust gap is the #1 conversion blocker. |
| **3** | **Simplify homepage to one clear CTA** | `HomePage.jsx` | 3 rotating taglines, event badges, social proof, preview card, occasion cards — 5+ competing elements | One headline, one sub-headline, one button, one example result. Everything else below fold. | HIGH — cognitive overload kills conversion. |
| **4** | **Add celebration/delight moment to result reveal** | `MobileResultsCarousel.jsx`, new animation | Results appear as static cards | Animated reveal: count-up percentage, feature-by-feature dramatic build, confetti on winner announcement, haptic feedback | HIGH — this IS the value moment. It should feel like a game show reveal, not a spreadsheet. |
| **5** | **Create standalone product detail pages** | New pages needed | Products only shown as small cards in results carousel shelf | Full page per product: multiple images, specs, reviews, "order by X get by Y", related products | HIGH — Cornish Prints standard. |
| **6** | **Fix homepage H1 and keyword targeting** | `HomePage.jsx:171-181` | H1 contains only "famili" (brand fragment) | H1: "Who Does Your Baby Look Like?" — targets primary keyword cluster | HIGH — SEO impact. Currently invisible to search engines. |
| **7** | **Add video/GIF showing a real reveal moment** | Homepage, above fold | Static text + example card | 15-second video: someone uploading → seeing result → emotional reaction. Demonstrates value without requiring trust. | HIGH — reduces trust barrier by showing the experience. |
| **8** | **Redesign occasion cards from internal briefs to customer copy** | `HomePageOccasion.jsx` | Internal language: "AOV potential", "Secondary", "Strongest social sharing hook" | Customer language: "The perfect Father's Day gift — show Dad his bond with you" | MEDIUM-HIGH — these cards are the product-led homepage. |
| **9** | **Add delivery timeline to product cards** | `ProductShelf.jsx`, `PRODUCT_DISPLAY` | Specs only: "11oz · dishwasher safe" | "Order today, delivered in 5-7 days" with Prodigi SLA | MEDIUM — checkout confidence. |
| **10** | **Implement skeleton loading screens** | All pages with data fetching | Spinner emoji (⏳) or blank screens during loading | Skeleton screens matching final layout, smooth transitions | MEDIUM — perceived performance + polish. |

---

## Section 7: SEO Audit & Keyword Opportunity

### Current SEO Baseline

**Strengths (already in place):**
- Meta title + description in index.html — keyword-targeted
- Open Graph tags complete (1200×630 image)
- Twitter Card tags complete
- `WebApplication` schema.org structured data
- `FAQPage` schema with 6 high-intent questions — excellent for AI search and featured snippets
- Google Analytics 4 connected
- Google Site Verification active
- sitemap.xml exists (5 URLs)
- robots.txt exists with appropriate blocks
- Canonical tag present
- `useDocumentMeta` hook provides per-page meta tags

**Critical Issues:**

| Issue | Severity | Fix |
|-------|----------|-----|
| **H1 tag contains only "famili"** — zero keyword value | CRITICAL | Change to "Who Does Your Baby Look Like?" |
| **robots.txt blocks AI crawlers** while FAQPage schema targets them — contradictory | HIGH | Unblock GPTBot, ChatGPT-User, Google-Extended, anthropic-ai |
| **SPA rendering** — `useDocumentMeta` updates DOM client-side, invisible to social crawlers and limited for search crawlers | HIGH | Add prerender service or SSR for key pages |
| **4 pages missing `useDocumentMeta`** — /hub, /app, /uno, /vault inherit default meta | MEDIUM | Add hook to each page |
| **Sitemap missing key routes** — /hub, /trail, /occasion/* not in sitemap.xml | MEDIUM | Expand sitemap |
| **robots.txt blocks /uno** — FamiliUno product pages can't be indexed | MEDIUM | Unblock if UNO is a revenue driver |
| **7 images with empty alt text** | LOW | Add descriptive alt text |

### Keyword Opportunity

| Cluster | Example Keywords | Est. Monthly Volume | Competition | FamiliLook Position |
|---------|-----------------|-------------------|-------------|-------------------|
| **Primary (HIGH intent)** | "who does my baby look like app", "baby looks like dad app" | 1K-3K | Very Low | **No presence** — easy win |
| **Informational (TOP funnel)** | "who does my baby look like", "family resemblance genetics" | 8K-15K | Low | **No presence** — highest volume opportunity |
| **Commercial (keepsakes)** | "personalised family mug UK", "family keepsakes personalised" | 1K-3K | High | **No presence** — competitive, long-tail approach needed |
| **Tool queries** | "family resemblance test", "family face analysis" | 2K-5K | Low-Medium | **No presence** — aligned with product |

### SEO Priority Actions

**QUICK WIN (before relaunch):**
1. Fix H1 tag to target primary keyword
2. Unblock AI crawlers in robots.txt
3. Add `useDocumentMeta` to 4 missing pages
4. Expand sitemap.xml with all public routes
5. Unblock /uno in robots.txt

**MEDIUM TERM (first month post-relaunch):**
6. Prerender service for SPA (prerender.io or Vercel prerendering)
7. Create keyword landing pages: `/baby-looks-like`, `/family-resemblance-test`
8. Add Product schema.org for keepsakes
9. Internal linking strategy from homepage to key pages

**LONG TERM (3+ months):**
10. Blog/content hub targeting informational queries
11. Backlink strategy — parenting blogs, gift guides
12. Multi-language hreflang (UK vs US English)

**Single highest-impact SEO change:** Fix the H1 tag. 5-minute change targeting 8K-15K monthly searches with very low competition.

---

## Section 8: Prioritised Fix List — Top 20 Changes

Ranked by **(user impact × conversion impact × inverse effort)**

| Rank | Change | Category | Effort | Expected Impact | Rationale |
|------|--------|----------|--------|----------------|-----------|
| **1** | Fix H1 tag to "Who Does Your Baby Look Like?" | SEO | 5 min | HIGH | Targets 8K-15K/mo searches, zero competition, currently invisible |
| **2** | Unblock AI crawlers in robots.txt | SEO | 2 min | HIGH | FAQPage schema already targets AI search but crawlers are blocked |
| **3** | Verify and fix CSP analytics blocking | Analytics | 1 hour | CRITICAL | If CSP blocks analytics, ALL measurement is impossible. Must verify before anything else |
| **4** | Replace SVG product illustrations with real photography | UI/UX | 2-3 days | CRITICAL | Users cannot visualise products. #1 blocker for purchase intent |
| **5** | Simplify homepage to single clear CTA | Copy/UX | 1 day | HIGH | 5+ competing elements cause cognitive overload. One headline, one button |
| **6** | Add trust signals (security badges, "photos never stored", "EU servers") | Copy/UX | 0.5 day | HIGH | Trust gap is root cause of 0% upload. This directly addresses it |
| **7** | Rewrite occasion cards — remove internal language | Copy | 0.5 day | HIGH | "AOV potential" and "Secondary" are visible to customers |
| **8** | Add `useDocumentMeta` to /hub, /app, /uno, /vault | SEO | 30 min | MEDIUM | 4 pages have no unique meta tags |
| **9** | Expand sitemap.xml + unblock /uno | SEO | 15 min | MEDIUM | Only 5 URLs indexed, revenue pages blocked |
| **10** | Add celebration animation to result reveal | UX | 1-2 days | HIGH | The value moment should feel like a reveal, not a spreadsheet |
| **11** | Rewrite FamiliMatch landing copy (emotional, not technical) | Copy | 0.5 day | MEDIUM | "AI Facial Compatibility" → "How alike are you really?" |
| **12** | Add delivery timeline to product cards | UX | 2 hours | MEDIUM | "Order today, delivered in 5-7 days" — checkout confidence |
| **13** | Replace "Thousands of" social proof with verifiable trust claim | Copy | 30 min | MEDIUM | Vague social proof may harm trust. Replace with specific security claim |
| **14** | Pick ONE homepage headline (stop rotating 3 taglines) | Copy/UX | 30 min | MEDIUM | Users see random tagline on arrival. Lead with the strongest one |
| **15** | Rewrite mug occasion headers from clinical to celebratory | Copy | 1 hour | LOW-MEDIUM | "YOUR FAMILY RESEMBLANCE" → "LOOK WHO TAKES AFTER MUM" |
| **16** | Add video/GIF of a real reveal moment to homepage | UX/Content | 2-3 days | HIGH | Shows value without requiring trust/upload |
| **17** | Create standalone product detail pages for keepsakes | UX | 3-5 days | HIGH | Cornish Prints benchmark. Currently products are small cards in a shelf |
| **18** | Install Hotjar free tier for session recordings | Analytics | 1 hour | MEDIUM | See what users actually do. Currently flying blind |
| **19** | Add UTM parameter capture for traffic attribution | Analytics | 2 hours | MEDIUM | Can't distinguish traffic sources |
| **20** | Add route prerequisite guards (/uno without analysis, /room without tier) | UX/Security | 1 day | LOW-MEDIUM | Users can navigate to broken states |
| **21** | **Fix stale occasion dates** — all countdown badges expired. Add Father's Day June 21. Make occasions permanent. | Copy/UX | 30 min | HIGH | Product-led homepage currently shows zero occasion badges |
| **22** | **Fix design token conflict** — `index.css` orange accents vs `colors.js` violet | UI | 30 min | MEDIUM | Focus rings, text selection flash orange in a violet app |
| **23** | **Replace emoji navigation icons with Lucide icons** | UI | 1 hour | MEDIUM | Cross-platform inconsistency, looks unprofessional |
| **24** | **Expand BottomNav from 2 tabs to 4** (Home, Trail, Keepsakes, Settings) | UX | 0.5-1 day | HIGH | Products buried behind analysis. Should be 1 tap away |
| **25** | **Show pricing from step 2 in KeepsakesModal** | UX | 2 hours | HIGH | Users go through 3 steps before seeing cost |

---

## Summary for CEO

**The platform infrastructure is ready.** 1,444 tests passing, 3 structural modules built and extracted to famililook-shared, 7/7 HIGH audit items resolved, zero P0/P1 code issues.

**The user-facing experience is not ready.** Three critical gaps:

1. **Trust gap** — No social proof, no reviews, no product photography, no quality signals. Users won't upload children's photos to an unknown brand.

2. **Clarity gap** — Homepage has 5+ competing elements, internal language visible to customers, value proposition buried behind technology descriptions.

3. **Visibility gap** — H1 tag has zero keyword value, AI crawlers blocked, 4 pages missing meta tags, only 5 URLs in sitemap. The product is invisible to search.

**The single most important insight:** The technical product works. The emotional product doesn't exist yet. Users need to *feel* something before they'll trust and pay. Every fix in this document moves toward making users feel: curious → safe → delighted → compelled to buy.

**Recommended approach:** Fix items 1-9 (all under 1 day each, many under 30 minutes) before lifting maintenance mode. Items 10-20 form the first sprint post-relaunch.

---

*This document is the brief for all UX, copy, UI, and SEO work before relaunch. Nothing gets fixed without appearing in this document. CEO approves, redirects, or adds to it. No implementation begins until CEO approves.*
