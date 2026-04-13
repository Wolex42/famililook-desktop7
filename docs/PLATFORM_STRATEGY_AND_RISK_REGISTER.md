# FamiliLook Platform — Strategy & Risk Register

**Version:** 2.0
**Date:** 2026-03-07 (updated from 2026-02-23)
**Author:** Francis Aroyehun
**Status:** Investor-ready — commerce layer LIVE, products deployed, governance audited

---

## Table of Contents

1. [Product Portfolio](#1-product-portfolio)
2. [Legal & Regulatory](#2-legal--regulatory)
3. [IP & Trademark](#3-ip--trademark)
4. [Branding & Naming](#4-branding--naming)
5. [Revenue Strategy](#5-revenue-strategy)
6. [Market Competition](#6-market-competition)
7. [Marketing & Placement](#7-marketing--placement)
8. [Advertising Strategy](#8-advertising-strategy)
9. [Infrastructure & Scalability](#9-infrastructure--scalability)
10. [Risk Register](#10-risk-register)
11. [Decision Log](#11-decision-log)

---

## 1. Product Portfolio

Four products, one engine — presented via a brand hub at **famililook.com**:

```
  [FamiliLook]     [FamiliUno]
  [FamiliPoker]    [FamiliMatch]
```

| # | Product | Audience | One-Liner | Physical Product | Status |
|---|---------|----------|-----------|-----------------|--------|
| 1 | **FamiliLook** | Families | "Which parent does your child look like? Play card games with the results." | Keepsake prints via Prodigi (certificates, mugs, framed cards, cushions, puzzles, T-shirts, baby bodysuits, Family Mug Set) | **LIVE** (famililook.com) — Stripe checkout + Prodigi ordering operational |
| 2 | **FamiliUno** | Families | "Order a real Uno-style card game printed with your family faces" | Full Uno-style card game sets via QPMarkets API | **In Development** (FE live, ordering backend complete, pending API key) |
| 3 | **FamiliPoker** | Adults 18+ | "Play poker & blackjack with your family's face cards" | Physical card decks (future) | Deployed (famililook-desktop4.vercel.app) |
| 4 | **FamiliMatch** | Singles/couples/friends | "How compatible are your faces? Compare, fuse, reveal" | — | Deployed (famililook-desktop6.vercel.app) |

Full technical architecture: [PLATFORM_ARCHITECTURE.md](PLATFORM_ARCHITECTURE.md)

---

## 2. Legal & Regulatory

### 2.1 Jurisdiction Map

| Regulation | Applies To | Key Requirements | Status |
|------------|-----------|-----------------|--------|
| **GDPR** (EU/UK) | All 3 products | Lawful basis, consent, DPIA, right to erasure, DPO | PARTIAL — see `legal/LEGAL_REVIEW_PACK.md` |
| **COPPA** (US) | FamiliLook | Parental consent for under-13 data, age gate | PARTIAL — 13+ age gate deployed 2026-03-27 |
| **BIPA** (Illinois, US) | Dating Product | Written consent before biometric collection, retention policy, $5K/person cap | NOT IMPLEMENTED |
| **EU AI Act** (Feb 2025) | All 3 products | No untargeted scraping, no race/orientation categorisation from biometrics | COMPLIANT (we don't categorise) |
| **UK Age Appropriate Design Code** | FamiliLook | High privacy defaults for under-18s, data minimisation | PARTIAL |
| **App Store Guidelines** | Casino Product | Apple 5.3 (gambling), must not simulate real gambling | SEE NAMING RISK |

### 2.2 Biometric Data Classification

**Critical question:** Are 512-dimensional face embeddings "biometric data"?

| Jurisdiction | Classification | Implication |
|-------------|---------------|-------------|
| EU (GDPR Art. 9) | Likely yes — "biometric data" = data resulting from processing relating to physical characteristics that allows unique identification | Requires **explicit consent** (not just legitimate interest) |
| Illinois (BIPA) | Yes — "biometric identifier" includes face geometry scans | Requires **written informed consent**, published retention schedule, $5K/person statutory damages |
| UK GDPR | Likely yes — same as EU | Same as EU |
| Texas, Washington | Less stringent biometric laws | Still require notice and consent |

**Current exposure:** desktop3 processes face embeddings server-side. This is biometric processing under most frameworks. The planned Gen 2 client-side architecture (processing in-browser) would significantly reduce exposure but does NOT eliminate it — the browser still processes biometric data, and the Dating Product must send photos to the server for comparison.

### 2.3 Product-Specific Legal Requirements

#### FamiliLook (Families)
- [x] COPPA-compliant age gate (US market) — deployed 2026-03-27
- [ ] Verifiable parental consent mechanism
- [ ] GDPR consent banner with granular categories (analytics, processing)
- [ ] Accurate privacy claims (homepage claims were corrected 2026-02)
- [ ] Published data retention policy
- [x] Data Protection Impact Assessment (DPIA) — docs/DPIA_FAMILILOOK.md (2026-03-27)

#### Casino Product (Adults)
- [ ] Age verification (18+ gate)
- [ ] Clear "no real money gambling" disclosure
- [ ] Terms that disclaim any resemblance to actual gambling
- [ ] Apple/Google Store compliance for simulated casino games
- [ ] Separate privacy policy

#### Dating Product (FamiliMatch — Gen 3)
- [x] BIPA-compliant written consent before any facial analysis — **IMPLEMENTED** (`ConsentContext.jsx` consent modal, blocks all functionality until accepted)
- [ ] Published biometric data retention schedule (recommendation: "processed and discarded within the session, never stored") — behaviour implemented, formal document not yet published
- [x] Explicit opt-in for face comparison ("I consent to my photo being compared with another person's photo") — **IMPLEMENTED** (consent modal + voluntary photo upload action)
- [x] Mutual consent mechanism (both parties agree before comparison) — **IMPLEMENTED** (Duo/Group: each player must consent + upload independently; comparison only starts when all ready)
- [x] No storage of photos or embeddings on server (RAM-only, discard on room close) — **IMPLEMENTED** (desktop7 rooms.py auto-deletes all data on room close; desktop3 processes in-memory only)
- [x] Data breach notification procedures — Incident Response Plan written at docs/INCIDENT_RESPONSE_PLAN.md (2026-03-27)
- [x] Prohibition on race/orientation categorisation from facial features (EU AI Act) — **COMPLIANT** (scoring is similarity-based, no demographic categorisation)
- [ ] Separate privacy policy and terms
- [ ] DPIA (mandatory for biometric processing in dating context)

### 2.4 Legal Precedents to Watch

| Case | Relevance |
|------|-----------|
| **Rosenbach v. Six Flags (2019)** | BIPA violations actionable without proving actual harm — procedural failures alone are enough |
| **Victoria Milan BIPA class action (2024)** | Dating app sued for collecting facial geometry via selfie verification without consent |
| **Tea dating app data breach (2025)** | Multiple class actions after facial scan data breach — shows litigation risk |
| **Clearview AI settlement ($51.75M, 2025)** | Scraping facial images without consent — class received 23% equity stake |
| **2024 BIPA Amendment** | Caps damages at $5K per person (not per scan) — reduces but doesn't eliminate exposure |

### 2.5 Recommended Legal Actions

**Before any launch:**

| Priority | Action | Timeline | Cost Estimate |
|----------|--------|----------|--------------|
| P0 | Engage IP/privacy counsel (biometric specialist) | Immediate | Retainer |
| P0 | File trademark applications (see Section 3) | Immediate | ~$500-1500 per class per jurisdiction |
| P0 | Conduct DPIA for all three products | Before launch | Counsel-led |
| P1 | COPPA compliance for FamiliLook (age gate + parental consent) | Before US launch | Dev + legal review |
| P1 | BIPA consent flow for Dating Product | Before launch | Dev + legal review |
| P1 | Publish biometric data retention policy | Before launch | Counsel drafts |
| P2 | Consider cyber liability insurance | Before public launch | ~$1-5K/year |
| P2 | NDA template for contractors accessing backend code | Before hiring | Counsel drafts |

---

## 3. IP & Trademark

### 3.1 Current IP Protection Status

| Asset | Protection | Status | Action Needed |
|-------|-----------|--------|--------------|
| "Famililook" / "FamiliLook" name | Trademark | **NOT REGISTERED** | File immediately |
| famililook.com domain | Domain reg | Active (GoDaddy → Cloudflare) | Secure .co.uk, .app |
| Kinship voting algorithm | Trade secret | Private repo only | Consider provisional patent |
| Calibration dataset (654 faces) | Trade secret / DB right | Private repo only | Document formally |
| Feature label taxonomy (8×5 grid) | Copyright | Automatic | Document creation date |
| Source code (all repos) | Copyright | Automatic | Copyright headers in files |
| Card/keepsake designs | Copyright / Design right | Automatic | Consider design registration |
| Multiplayer protocol | Trade secret | Private repo only | — |
| Casino game mechanics (Feature Poker, Feature 21) | Copyright (code) | Automatic | Game mechanics not patentable |
| Compatibility scoring system | Trade secret | **BUILT** (desktop6 `matchClient.js` + desktop3 `/compare/faces`) | Document as trade secret — 5-tier chemistry labels, hybrid embedding+feature blended scoring (0.6/0.4), calibrated 8-feature symmetric comparison via dedicated `/compare/faces` endpoint. Frozen API contract at `contracts/compare_faces.v1.schema.json`. |

### 3.2 Trademark Filing Strategy

**Classes to register in:**

| Class | Description | Products |
|-------|-------------|----------|
| Class 9 | Computer software, mobile apps | All three |
| Class 41 | Entertainment, games, amusement | Casino Product, Dating Product |
| Class 42 | SaaS, platform services | All three (if B2B API planned) |
| Class 45 | Social introduction, dating services | Dating Product |

**Jurisdictions (priority order):**

| Jurisdiction | Why | Cost (approx) |
|-------------|-----|---------------|
| UK (UKIPO) | Home jurisdiction | ~$300/class |
| EU (EUIPO) | Covers 27 member states | ~$900/class |
| US (USPTO) | Largest market | ~$350/class |
| International (Madrid Protocol) | Broader protection | ~$800+ per designated country |

**Names to register:**
1. "FamiliLook" / "Famililook" — definitely (currently unregistered)
2. Casino product name — once decided (see Section 4)
3. Dating product name — once decided (see Section 4)
4. "Feature Poker" / "Feature 21" — consider for game names

### 3.3 Domain Strategy

| Domain | Status | Action |
|--------|--------|--------|
| famililook.com | Active | Maintain |
| famililook.co.uk | ? | Secure |
| famililook.app | ? | Secure |
| [casino-product].com | — | Secure when name decided |
| [dating-product].com | — | Secure when name decided |
| [dating-product].app | — | Secure when name decided |

### 3.4 Patent Considerations

| Innovation | Patentable? | Recommendation |
|-----------|-------------|----------------|
| Kinship voting algorithm (per-feature similarity, margin tie-breaking, order-invariant fingerprinting) | Possibly — novel method, but software patents are weak in UK/EU | File provisional (US) to establish priority date, then evaluate full filing |
| Compatibility scoring (embedding + feature hybrid) | Probably not — combines known techniques | Trade secret |
| Face fusion in dating context | No — Delaunay triangulation is well-known | Trade secret for specific implementation |
| Feature-based card game mechanics | No — game mechanics not patentable | Copyright on code |

**Estimated cost for US provisional patent:** $2,000-5,000 (with patent attorney)
**Deadline pressure:** If any of these concepts are publicly disclosed (beta launch, blog post, conference talk), the 12-month provisional window starts ticking (US) or is lost entirely (EU — absolute novelty requirement).

---

## 4. Branding & Naming

### 4.1 Naming Analysis — RESOLVED (2026-02-24)

**Rejected names and reasons:**

| Rejected Name | Reason | Risk |
|---------------|--------|------|
| FaceCasino | Apple Guideline 5.3 flags "casino" keyword — enhanced review, potential rejection | App Store |
| FaceMatch | Prior dating app (HotScore/FaceMatch, 2013-2014, now Moxy) — common-law trademark rights | IP |
| FamiliLook Casino | "Casino" keyword risk + ties gambling connotation to family brand | App Store + Brand |

**Chosen names:**

| Product | Chosen Name | Rationale |
|---------|-------------|-----------|
| Casino card games (Gen 2) | **FamiliPoker** | "Famili-" brand family consistency. "Poker" is accurate (Feature Poker is core game). No App Store "casino" keyword trigger. No trademark conflicts found. |
| Compatibility product (Gen 3) | **FamiliMatch** | "Famili-" brand family consistency. "Match" is generic enough to avoid FaceMatch trademark collision. Describes core function (matching/comparing). Conduct formal trademark search before launch. |

> **Action:** Formal trademark search still needed for both names before filing applications.
| TwinFlame | Spiritual connection | Check | Trendy dating term, but may attract wrong audience |
| FaceChemistry | Science of attraction | Check | Ties to "chemistry labels" in scoring system |

### 4.3 Brand Architecture Decision

**Option A: Unified brand (FamiliLook umbrella)**
```
FamiliLook              (parent brand)
├── FamiliLook           (family app)
├── FamiliLook Arena     (casino games)
└── FamiliLook Chemistry (dating)
```
- Pro: One brand to build, cross-promotion easy
- Con: Family/dating/gambling under one roof is confusing and risky

**Option B: Separate brands, shared engine**
```
FamiliLook              (family app)
[Casino Brand]          (separate identity)
[Dating Brand]          (separate identity)
"Powered by FamiliLook" (subtle engine credit)
```
- Pro: Each product positioned for its audience, no cross-contamination
- Con: Three brands to build, higher marketing cost

**Option C: Two brands (family + adult)**
```
FamiliLook              (family app)
[Adult Brand]           (casino + dating combined)
```
- Pro: Only two brands, adults get one destination
- Con: Casino games and dating are different use cases

**Recommendation: Option B.** The audiences are too different to share branding. A parent researching "FamiliLook" should not find dating or casino content. A dater should not see children's faces in the brand. Complete separation protects all three products.

### 4.4 Branding Decisions Needed

| Decision | Options | Impact | Deadline |
|----------|---------|--------|----------|
| Casino product name | See alternatives above | Trademark filing, domain, App Store listing | Before development begins |
| Dating product name | See alternatives above | Trademark filing, domain, App Store listing | Before development begins |
| Brand architecture | A (unified) / B (separate) / C (two) | Marketing strategy, legal structure, app store accounts | Before any public launch |
| Visual identity | Shared design language or fully distinct? | Design cost, brand recognition | Before development begins |
| App store accounts | One developer account or separate per product? | Revenue isolation, review risk isolation | Before first submission |

---

## 5. Revenue Strategy

### 5.1 Revenue Model Per Product

#### FamiliLook (Family App) — LIVE with Commerce

| Tier | Price | Features | Status |
|------|-------|----------|--------|
| **Free** | $0 | 1 analysis/day, 3 games, basic results | LIVE |
| **Premium** | $4.99/month or $29.99/year | Unlimited analysis, all 6 games, group photos | LIVE (Stripe subscription) |
| **Keepsakes** | $7.99-$34.99 per item | Physical printed keepsakes via Prodigi | **LIVE** (Stripe checkout) |
| **Personalised Message** | +$1.99 surcharge | LLM-generated personalised message on keepsake | LIVE |

**Live product prices (GBP):**

| Product | Price | Prodigi SKU |
|---------|-------|-------------|
| Fine Art Print (8x10) | $9.99 | GLOBAL-FAP-8X10 |
| Fine Art Print (16x20) | $19.99 | GLOBAL-FAP-16x20 |
| Framed Canvas (12x16) | $34.99 | GLOBAL-FRA-SLIMCAN-12x16 |
| Ceramic Mug (panoramic) | $14.99 | GLOBAL-MUG-W |
| Family Mug Set (Mum + Dad pair) | $27.99 | GLOBAL-MUG-W (x2) |
| T-Shirt | $19.99 | GLOBAL-TEE-GIL-5000 |
| Baby Bodysuit | $14.99 | GLOBAL-TEE-GIL-5000 |
| Cushion (16x16) | $24.99 | GLOBAL-CUSH-16X16-CAN-DUAL |
| Jigsaw Puzzle (252pc) | $24.99 | JIGSAW-PUZZLE-252 |
| Greeting Card | $7.99 | CLASSIC-GRE-FEDR-7X5-BLA |
| Postcard | $4.99 | CLASSIC-POST-GLOS-6X4 |

**Revenue per user estimate:** $0.50-2.00/month blended (90% free, 8% premium, 2% keepsake buyers)

#### FamiliUno (Physical Card Game Orders)

| Model | Price | Notes |
|-------|-------|-------|
| **Card pack order** | $19.99-39.99 | Full Uno-style family card game printed with your family faces. Price depends on card count + quality tier. |
| **Re-order / update pack** | $14.99-24.99 | Re-order after adding new family members |
| **Deluxe edition** | $49.99+ | Premium card stock, custom box, keepsake tin |

**Revenue model:** Pure transactional — no subscription. High AOV (average order value), low frequency. Revenue depends on conversion from FamiliLook users who completed an analysis. Margin depends on card supplier pricing (TBD).

**Revenue per converted user estimate:** $20-40 one-time, ~10-20% of FamiliLook premium users convert.

#### Casino Product (Adults)

| Model | Price | Features |
|-------|-------|----------|
| **Free** | $0 | Feature Poker (1 AI opponent), Feature 21 (basic) |
| **Premium** | $6.99/month | All AI opponents, multiplayer rooms, tournament mode |
| **Chip packs** | $0.99-9.99 | In-game currency for betting (no real money cashout) |
| **Cosmetics** | $1.99-4.99 | Card backs, table themes, avatar effects |

**Revenue per user estimate:** $1.50-5.00/month blended (heavy IAP potential)

#### Dating Product

| Model | Price | Features |
|-------|-------|----------|
| **Free** | $0 | 2 solo comparisons/day, basic score |
| **Premium** | $9.99/month or $59.99/year | Unlimited comparisons, HD face fusion, duo rooms, group rooms, save/share results |
| **Boost** | $2.99 one-time | Priority room creation, custom room themes |

**Revenue per user estimate:** $2.00-8.00/month blended (dating users have high willingness to pay)

### 5.2 Revenue Projections (Conservative)

| Product | Users (Month 6) | Revenue/User/Month | Monthly Revenue |
|---------|-----------------|-------------------|-----------------|
| FamiliLook | 5,000 | $1.00 | $5,000 |
| FamiliUno | 500 orders | $30 AOV (one-time) | $2,500 (order revenue) |
| Casino Product | 1,000 | $3.00 | $3,000 |
| Dating Product | 2,000 | $5.00 | $10,000 |
| **Total** | **8,500** | — | **$20,500** |

### 5.3 Payment Infrastructure — OPERATIONAL

| Provider | Products | Status | Notes |
|----------|----------|--------|-------|
| **Stripe** | Keepsake orders, subscriptions, basket checkout | **LIVE** | Server-side price validation, Adaptive Pricing for multi-currency, webhook integration |
| **Prodigi API** | Physical keepsake fulfilment | **LIVE** | Print-on-demand, verified SKUs, HMAC webhook callbacks, image serving endpoint |
| **QPMarkets API** | FamiliUno physical card game sets | **Pending** | `CardPrintClient` in vendor_client.py, contract finalised, awaiting API key |
| **Apple IAP / Google Play Billing** | Casino chips, premium subscriptions (native) | **Planned** | Required when native apps launch; 30% cut |

**Commerce architecture (live):**
- `CurrencyContext.jsx` — 8 countries, hardcoded rates, `formatPrice()` helper
- `BasketContext.jsx` — multi-item cart, localStorage persistence, MAX_ITEMS=20
- `BasketDrawer.jsx` — slide-up checkout with shipping form
- `OrderModal.jsx` — single-item Stripe checkout
- `POST /payments/create-basket-checkout` — multi-item Stripe session, per-item order records
- `POST /payments/create-checkout-session` — single-item Stripe session
- `POST /webhooks/stripe` — payment confirmation, triggers Prodigi order
- `POST /webhooks/print-status` — HMAC-verified Prodigi status callbacks
- `PRODUCT_PRICES_PENCE` dict in payments.py — server-side price authority (prevents FE tampering)

### 5.4 Revenue Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| App Store 30% cut on IAP | Reduces margin significantly | Web-based payment option for subscriptions |
| Low conversion (free → premium) | Revenue below projections | A/B test paywall placement, free trial periods |
| Churn (dating apps have 70%+ monthly churn) | Unsustainable user acquisition cost | Focus on group rooms (social retention), face fusion sharing (organic growth) |
| Prodigi fulfillment issues | Keepsake revenue at risk | Multiple fulfillment partners, quality testing |

---

## 6. Market Competition

### 6.1 Competitive Landscape — Family Analysis

| Competitor | What They Do | Threat Level | Our Advantage |
|-----------|-------------|-------------|---------------|
| **Gradient** (face app) | Celebrity lookalike, ethnicity estimation | Low | We do parent-child comparison, not celebrity matching |
| **FaceApp** | Age/gender filters, entertainment | Low | Different use case — we analyse inheritance |
| **Baby Generator apps** (10+) | Predict baby appearance | Low | We analyse real children, they predict hypothetical babies |
| **23andMe / Ancestry** | DNA-based inheritance | Medium | They require DNA kits ($99+); we use photos (free/instant) |
| **No direct competitor** | Feature-level kinship voting | — | We are unique in 8-feature categorical analysis |

### 6.2 Competitive Landscape — Casino Card Games

| Competitor | What They Do | Threat Level | Our Advantage |
|-----------|-------------|-------------|---------------|
| **Zynga Poker** | Mobile poker (millions of users) | Low | They use generic cards; our cards are your family's faces |
| **PokerStars Play** | Simulated poker | Low | No personalisation |
| **Blackjack 21** (various) | Standard blackjack | Low | No family data, no feature bonuses |
| **No direct competitor** | Family face card games | — | Unique: your family members ARE the cards |

### 6.3 Competitive Landscape — Dating/Compatibility

| Competitor | What They Do | Threat Level | Our Advantage |
|-----------|-------------|-------------|---------------|
| **iris Dating** | Learns your facial attraction preferences, matches you | **Medium-High** | They learn preference; we compare faces directly. Different approach. |
| **SCiMatch** | Face-print personality matching, compatibility % | **High** | Most similar concept — but they predict personality, we compare features visually |
| **Tinder/Bumble/Hinge** | Swipe-based with AI enhancements | Low | Different category — we're a utility/game, not a dating marketplace |
| **Baby Generator apps** | Face fusion for couples | Low | Standalone novelty; we integrate into a social experience |

### 6.4 Our Competitive Moat

| Layer | Defensibility | Strength |
|-------|-------------|----------|
| **Proprietary kinship algorithm** | Trade secret / potential patent | Strong — years of development, 654-face calibration dataset |
| **8-feature calibration system** | Trade secret | Strong — custom taxonomy, one-word labels, percentile bands |
| **Cross-product engine** | Code reuse advantage | Medium — competitors would need to build 3 separate products |
| **Face fusion in social context** | Implementation, not concept | Weak — others can build face morphing |
| **Family emotional connection** | Brand positioning | Strong — "your actual family" is more compelling than stock photos |
| **Room-based simultaneous reveal** | Implementation | Medium — novel UX but reproducible |

### 6.5 Competitive Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| SCiMatch adds feature comparison | Medium | High | Speed to market, build community, patent filing |
| iris Dating adds face fusion | Medium | Medium | Our fusion is family-data-integrated, theirs would be standalone |
| Tinder/Bumble acquires a face comparison startup | Low | High | Be the acquisition target, or build defensible user base first |
| Open-source face comparison tool emerges | Medium | Medium | Our value is the calibrated taxonomy + game integration, not raw comparison |
| Baby generator app adds compatibility scoring | High | Medium | Their audience is entertainment; ours is dating/social |

---

## 7. Marketing & Placement

### 7.1 Distribution Channels

| Channel | FamiliLook | Casino Product | Dating Product |
|---------|:----------:|:--------------:|:--------------:|
| Apple App Store | Yes | Yes | Yes |
| Google Play Store | Yes | Yes | Yes |
| Web app (PWA) | Yes (current) | Yes | Yes |
| Social media (organic) | Instagram, TikTok, Facebook | TikTok, YouTube | TikTok, Instagram |
| Influencer marketing | Family/parenting creators | Gaming creators | Dating/lifestyle creators |
| Word of mouth | Family gatherings | Game nights | Friend groups |

### 7.2 Go-To-Market Strategy Per Product

#### FamiliLook (LIVE)
- **Current:** Organic + beta testers
- **Next:** Parenting influencer partnerships, Facebook family groups, school/nursery partnerships
- **Viral mechanic:** "Look who [child] looks like!" — shareable result screenshots

#### Casino Product
- **Launch:** Soft launch with existing FamiliLook users who have family data
- **Growth:** Gaming YouTubers, TikTok poker content, game night promotion
- **Viral mechanic:** "Beat your Dad at Feature Poker" — competitive family moments

#### Dating Product
- **Launch:** TikTok campaign — "How compatible are you? Face fusion reveals all"
- **Growth:** Dating influencers, couples challenge videos, group party format
- **Viral mechanic:** Face fusion screenshots — "Look what we'd look like combined" is inherently shareable
- **Group rooms** are the growth engine — one person invites 5 friends, each of whom invites 5 more

### 7.3 App Store Optimisation (ASO)

| Product | Primary Keywords | Category |
|---------|-----------------|----------|
| FamiliLook | family resemblance, look like parents, family face comparison | Entertainment / Lifestyle |
| Casino Product | family card game, feature poker, family game night | Games / Card |
| Dating Product | face compatibility, face fusion couples, who do you look like | Entertainment / Social / Lifestyle |

**NOT "Dating" category for launch** — the dating category is brutally competitive. Position as entertainment/social first, move to dating category once traction is proven.

### 7.4 Content Marketing

| Content Type | Platform | Product | Example |
|-------------|----------|---------|---------|
| "Who do they look like?" reveals | TikTok, Instagram Reels | FamiliLook | Parent films child's reaction to results |
| Celebrity face fusion | TikTok | Dating Product | "I fused my face with [celebrity]" |
| Group compatibility challenge | TikTok, YouTube Shorts | Dating Product | "Which friend am I most compatible with?" |
| Game night highlights | TikTok, YouTube | Casino Product | Family playing Feature Poker, reactions |
| Before/after couples | Instagram | Dating Product | "We scored 85% — Feature Twins!" |

---

## 8. Advertising Strategy

### 8.1 Paid Acquisition

| Channel | CPI (est.) | Product | Budget Priority |
|---------|-----------|---------|----------------|
| TikTok Ads | $1.50-3.00 | Dating Product | High — best ROI for viral content |
| Instagram/Facebook Ads | $2.00-4.00 | FamiliLook | Medium — family audience targeting |
| Google App Campaigns | $1.00-2.50 | All | Medium — intent-based |
| Apple Search Ads | $2.00-5.00 | All | Low initially — expensive but high intent |
| Influencer partnerships | $200-2000/post | Dating + Casino | High — authentic content outperforms ads |

### 8.2 User Acquisition Economics

| Metric | FamiliLook | Casino | Dating |
|--------|:----------:|:------:|:------:|
| Target CPI | $2.00 | $3.00 | $2.50 |
| Free-to-Premium conversion | 8% | 12% | 15% |
| Monthly ARPU | $1.00 | $3.00 | $5.00 |
| Payback period | 25 months | 8 months | 3 months |
| Target LTV | $12 | $36 | $30 |
| LTV:CAC ratio | 6:1 | 12:1 | 12:1 |

**Dating Product has the best unit economics** — highest ARPU, shortest payback, viral sharing reduces effective CPI.

### 8.3 Advertising Policies to Watch

| Platform | Restriction | Impact |
|----------|------------|--------|
| Apple | No gambling promotion in non-gambling apps | Cannot cross-promote casino product inside FamiliLook |
| Facebook/Meta | Facial recognition ads heavily restricted | Cannot use "we scan your face" messaging — frame as "compare features" |
| TikTok | Strict on dating app ads for under-18 | Must age-gate dating product ads |
| Google | Biometric data collection requires disclosure | Ad copy must mention facial analysis |

---

## 9. Infrastructure & Scalability

### 9.1 Current Infrastructure

```
Hetzner CPX22 — 2 vCPU, 4 GB RAM, 80 GB SSD
Helsinki, EU jurisdiction
Monthly cost: ~$15

├── desktop3 (analysis engine) — ~2 GB RAM (ML models)
├── desktop5 (game server) — ~200 MB RAM
├── desktop7 (match server) — ~200 MB RAM (built, port 8030)
├── Caddy (reverse proxy) — ~100 MB RAM
└── OS overhead — ~400 MB
```

### 9.2 Capacity Analysis

| Service | Bottleneck | Current Capacity | At Limit |
|---------|-----------|-----------------|----------|
| desktop3 (analysis) | CPU (ML inference) | ~50 concurrent analyses | ~200 users uploading simultaneously |
| desktop5 (game rooms) | RAM (WebSocket connections) | ~10,000 rooms | ~40,000 players |
| desktop7 (match rooms) | CPU (calls desktop3) | ~30 concurrent rooms (each triggers 7+ API calls) | ~100 users in rooms simultaneously |
| Caddy (proxy) | Connections | ~50,000 concurrent | Not a bottleneck |

**desktop7 is the bottleneck** — each match room triggers 7+ calls to desktop3 (detect, embed, attributes for each face, plus morph). A duo room takes ~5-10 seconds of desktop3 CPU time. Group rooms (6 players = 15 pairwise comparisons) take ~30-60 seconds.

### 9.3 Scaling Plan

| Phase | Trigger | Action | Cost |
|-------|---------|--------|------|
| **Phase 0** (now) | <200 DAU | Single CPX22, all services | $15/month |
| **Phase 1** | 200-1000 DAU | Upgrade to CPX32 (4 vCPU, 8 GB) | $30/month |
| **Phase 2** | 1000-5000 DAU | Split: dedicated ML VPS (CPX42) + relay VPS (CPX22) | $70/month |
| **Phase 3** | 5000+ DAU | ML load balancer (2-3 desktop3 instances), separate game/match VPS | $150-300/month |
| **Phase 4** | 50,000+ DAU | Kubernetes cluster, auto-scaling, CDN for static assets | $500-2000/month |

### 9.4 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Analysis response time (single face) | <3 seconds | ~2-4 seconds |
| Match room reveal time (duo) | <10 seconds | Built — ~5-10 seconds (desktop7 + desktop3 round-trip) |
| Match room reveal time (group of 6) | <60 seconds | Built — ~30-60 seconds (15 pairwise comparisons) |
| Game server message latency | <100ms | ~20-50ms |
| Frontend load time (first paint) | <2 seconds | ~1.5 seconds |
| Uptime | 99.5% | No formal SLA yet |

### 9.5 Infrastructure Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| Single VPS failure | All products down | Low (Hetzner 99.9% SLA) | Daily backups, documented rebuild procedure |
| ML model memory leak | desktop3 crashes | Medium | Health check + auto-restart (Docker restart policy) |
| WebSocket connection storm (viral moment) | Game/match servers overwhelmed | Low-Medium | Connection limits per IP, rate limiting, upgrade path ready |
| SSL certificate expiry | HTTPS fails | Low | Caddy auto-renews via Let's Encrypt |
| desktop3 CPU saturation (too many match rooms) | Slow analysis, poor UX | Medium | Queue system for match rooms, "please wait" UI, priority for paid users |

### 9.6 Disaster Recovery

| Component | Backup | Recovery Time |
|-----------|--------|--------------|
| desktop3 code | GitHub (private repo) | 5 minutes (git pull + docker build) |
| desktop5 code | GitHub (private repo) | 5 minutes |
| desktop6 code | GitHub (private repo) | 5 minutes (static deploy to Vercel) |
| desktop7 code | GitHub (private repo) | 5 minutes (Docker rebuild) |
| ML models | Bundled in Docker image | Automatic with rebuild |
| Calibration data | In repo | Automatic with rebuild |
| User data | None on server (localStorage + RAM only) | N/A — nothing to recover |
| Analytics JSONL | Server disk only | Lost if VPS destroyed — acceptable for analytics |

---

## 10. Risk Register

### 10.1 Critical Risks (Must Address Before Launch)

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R1 | BIPA class action — dating product processes biometric data without written consent | Legal | Low (consent flow implemented) | Critical ($5K/person if bypassed) | Written consent before any facial analysis — `ConsentContext.jsx` (BIPA modal, blocks all functionality until accepted). Session-only, RAM-only processing documented in TARA-FM-002. Formal retention policy document still pending. | Dev + Legal counsel | **IMPLEMENTED** — `ConsentContext.jsx`; formal retention policy doc pending |
| R2 | ~~"FaceMatch" name infringement~~ — RESOLVED: renamed to FamiliMatch (avoids prior dating app "FaceMatch" trademark) | IP | Low (resolved) | Low | Formal trademark search for "FamiliMatch" before filing | Founder | **RESOLVED** — renamed 2026-02-24 |
| R3 | ~~Apple rejects "FaceCasino"~~ — RESOLVED: renamed to FamiliPoker (no "casino" keyword) | Operations | Low (resolved) | Low | No "casino" keyword in FamiliPoker. Formal search pending. | Founder | **RESOLVED** — renamed 2026-02-24 |
| R4 | COPPA violation — FamiliLook processes children's biometric data without parental consent | Legal | Medium | Critical (FTC enforcement) | Implement age gate + verifiable parental consent | Legal + Dev | PARTIAL — age gate implemented 2026-03-27, verifiable parental consent still pending |
| R5 | No trademark registration — competitor or troll registers "FamiliLook" | IP | Medium | High (forced rebrand) | File trademark applications immediately | Founder | NOT STARTED |

### 10.2 High Risks

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R6 | Family brand contaminated by dating/casino association | Brand | Medium | High | Separate brand identities (Option B architecture) | Founder | DECISION NEEDED |
| R7 | Competitor (SCiMatch or iris) adds face comparison feature | Market | Medium | High | Speed to market, patent filing, build community | Founder + Dev | MONITORING |
| R8 | desktop3 CPU bottleneck under match room load | Technical | Medium | Medium (poor UX, user churn) | Queue system, "please wait" UI, scaling plan ready | Dev | NOT STARTED |
| R9 | Low free-to-premium conversion | Revenue | Medium | High (unsustainable) | A/B test paywalls, offer free trials, focus on viral growth | Product | NOT STARTED |
| R10 | Data breach exposes user photos/embeddings | Security | Low | Critical (lawsuits, trust destroyed) | RAM-only processing, no disk writes, TLS enforcement, security headers on all Vercel deployments, source maps disabled, API key auth, robots.txt blocks scrapers | Dev | **STRENGTHENED** (IP protection deployed 2026-02-27) |

### 10.2b Gen 3 Specific Risks (NEW)

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R19 | WebSocket connection unreliable on mobile networks | Technical | Medium | High (Duo/Group mode fails) | Reconnection logic in useMatchConnection.js, graceful fallback to Solo mode | Dev | IMPLEMENTED |
| R20 | desktop3 latency under concurrent match rooms | Technical | Medium | Medium (slow reveals, user abandons) | Queue system for rooms, "analyzing..." progress UI, priority for paid rooms | Dev | PARTIAL (progress UI done) |
| R21 | Face morph quality perceived as low/uncanny | Product | Medium | Medium (core feature disappoints) | Morph is "bonus reveal" not core result; chemistry labels + feature comparison carry the experience | Product | IN DESIGN |
| R22 | FamiliMatch consent modal creates friction → user abandons | Product | Medium | High (dating audience has zero patience) | Minimal consent flow (one-tap), explain value clearly, only shown once per session | Dev | IMPLEMENTED |
| R23 | Room code guessed/brute-forced by stranger | Security | Very Low | High (non-consenting participant) | 6-char alphanumeric codes (2.18B combinations), cryptographic RNG (`secrets`), 5/min rate limit, rooms expire after inactivity | Dev | **MITIGATED (2026-02-27)** |

### 10.2c Commerce & Fulfilment Risks (NEW — March 2026)

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R24 | Stripe account suspension (policy violation or dispute rate) | Financial | Low | Critical (all revenue blocked) | Maintain low dispute rate, respond to Stripe inquiries promptly, keep backup payment provider on radar | Founder | MONITORING |
| R25 | Prodigi fulfilment delays or quality issues | Operations | Medium | Medium (refund requests, brand damage) | Quality-tested samples before launch; webhook monitoring for stuck orders; document alternative vendors (Printful, Gooten) | Dev | MONITORING |
| R26 | Currency conversion complaints (hardcoded rates vs actual) | Revenue | Medium | Medium (chargebacks, trust loss) | DFMEA FM-16 (RPN 120); add prominent "approximate" disclaimer or fetch live rates | Dev | **ACTION REQUIRED** |
| R27 | LLM-generated keepsake content is offensive or inaccurate | Brand | Low | Medium (printed on physical product, refund + brand damage) | User preview gate, LLM prompt constraints, consider content moderation layer | Dev | PARTIAL (preview implemented) |
| R28 | Order fulfilment leak — keepsake images accessible via URL enumeration | Security | Very Low | Medium (family photos exposed) | UUID order IDs (2^128), no directory listing; consider signed URLs for defense-in-depth | Dev | ACCEPTABLE |

### 10.3 Medium Risks

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R11 | App Store rejection for biometric processing without disclosure | Operations | Medium | Medium (delays launch) | Declare biometric data usage in App Store privacy labels; consent flow in onboarding | Dev | NOT STARTED |
| R12 | Discrimination allegations — scoring suggests some faces are "better" | Reputation | Low-Medium | High | Frame as "similarity" not "attractiveness"; chemistry labels are positive in all bands ("Opposites Attract" not "Incompatible") | Product | IN DESIGN |
| R13 | EU AI Act compliance — biometric categorisation restrictions | Legal | Low | Medium | We compare features, not categorise by race/orientation. Document this position. | Legal | NEEDS REVIEW |
| R14 | InsightFace model weight provenance challenged | Legal | Low | Medium | Monitor InsightFace community; have fallback model (client-side face-api.js) | Dev | MONITORING |
| R15 | Viral moment overwhelms infrastructure before scaling | Technical | Low | High | Auto-scaling alerts, documented upgrade procedure (~30 minutes) | Dev | PARTIAL |

### 10.4 Low Risks

| # | Risk | Category | Probability | Impact | Mitigation | Owner | Status |
|---|------|----------|------------|--------|------------|-------|--------|
| R16 | Patent troll targets face comparison approach | Legal | Low | Medium | Document prior art; consider defensive patent publication | Legal | NOT STARTED |
| R17 | Key person dependency (sole developer) | Operational | Ongoing | High | Document everything (CLAUDE.md, architecture docs, this document) | Founder | ONGOING |
| R18 | Hetzner datacenter incident (Helsinki) | Technical | Very Low | High | Regular backups, ability to redeploy to any VPS in <30 minutes | Dev | PARTIAL |

---

## 11. Decision Log

Decisions that must be made before proceeding. Track approvals here.

| # | Decision | Options | Recommendation | Decided? | Date | Choice |
|---|----------|---------|---------------|----------|------|--------|
| D1 | Casino product name | FaceDeck / FamiliBattle / Feature Royale / FamiliArena / other | FaceDeck or FamiliArena (clean, no app store risk) | **YES** | 2026-02-24 | **FamiliPoker** |
| D2 | Dating product name | LookAlike / FuseMe / BlendDate / FaceChemistry / other | FaceChemistry or LookAlike (ties to product features) | **YES** | 2026-02-24 | **FamiliMatch** |
| D3 | Brand architecture | A (unified) / B (separate) / C (two brands) | B (fully separate brands) | NO | — | — |
| D4 | Trademark filing jurisdictions | UK only / UK+EU / UK+EU+US | UK+EU+US (all three markets) | NO | — | — |
| D5 | Patent filing for kinship algorithm | File provisional (US) / Trade secret only / Skip | File US provisional to preserve option | NO | — | — |
| D6 | Legal counsel engagement | Solo / Part-time retainer / Full engagement | Part-time retainer (IP + biometric specialist) | NO | — | — |
| D7 | Cyber liability insurance | Yes / No / Defer | Yes, before public launch | NO | — | — |
| D8 | App store accounts | One account all products / Separate per product | Separate per product (isolation) | NO | — | — |
| D9 | Payment provider | Apple IAP only / Stripe + IAP / Stripe web only | Stripe + IAP (maximise margin) | **YES** | 2026-03-06 | **Stripe (web) — LIVE** for keepsakes + subscriptions. IAP deferred until native apps. |
| D10 | Dating product launch market | UK first / US first / Both | UK first (GDPR known, avoid BIPA initially) | NO | — | — |

---

## Appendix A: Legal Document Checklist

| Document | FamiliLook | Casino | Dating | Status |
|----------|:----------:|:------:|:------:|--------|
| Privacy Policy | Yes | Needed | Needed | FamiliLook: exists, needs update |
| Terms of Service | Yes | Needed | Needed | FamiliLook: exists, needs update |
| Cookie Policy | Needed | Needed | Needed | Not created |
| DPIA (Data Protection Impact Assessment) | Needed | Needed | Needed | Created — docs/DPIA_FAMILILOOK.md (2026-03-27) |
| Biometric consent form | N/A | N/A | Needed | **Implemented in-app** (ConsentContext.jsx); formal document pending |
| Parental consent mechanism | Needed (COPPA) | N/A | N/A | Not created |
| NDA template | Needed | Needed | Needed | Not created |
| Contributor agreement | If open-source | If open-source | If open-source | N/A |
| App Store privacy labels | Needed | Needed | Needed | FamiliLook: not submitted |
| NOTICE file (Apache 2.0 attribution) | Needed | Needed | Needed | Not created |
| Data processing agreement (Hetzner) | Needed | Needed | Needed | Not created |

---

## Appendix B: Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Platform Architecture | [docs/PLATFORM_ARCHITECTURE.md](PLATFORM_ARCHITECTURE.md) | Technical architecture for all 4 products |
| SWOT Analysis | [docs/SWOT_ANALYSIS.md](SWOT_ANALYSIS.md) | Strategic positioning (March 2026) |
| TARA | [docs/TARA_facematch.md](TARA_facematch.md) | Threat analysis (T-01 to T-14) |
| DFMEA | [docs/DFMEA_facematch.md](DFMEA_facematch.md) | Failure modes (FM-01 to FM-16) |
| Security Assessment | [docs/SECURITY_ASSESSMENT_2026-02-27.md](SECURITY_ASSESSMENT_2026-02-27.md) | Consolidated security findings |
| Advertising & Campaigns | [docs/ADVERTISING_AND_CAMPAIGNS.md](ADVERTISING_AND_CAMPAIGNS.md) | Marketing strategy and campaigns |
| Legal Review Pack | [legal/LEGAL_REVIEW_PACK.md](../legal/LEGAL_REVIEW_PACK.md) | GDPR, COPPA, data flow analysis |
| IP Review Pack | [legal/IP_REVIEW_PACK.md](../legal/IP_REVIEW_PACK.md) | IP assets, open-source audit, patent considerations |
| Capacitor Mobile Plan | [docs/CAPACITOR_MOBILE_DEPLOYMENT_PLAN.md](CAPACITOR_MOBILE_DEPLOYMENT_PLAN.md) | Native mobile deployment strategy |
| Gen2 Features PRD | famililook-desktop4/docs/PRD_GEN2_FEATURES.md | Casino product feature requirements |
