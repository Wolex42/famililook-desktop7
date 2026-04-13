# Funnel Model & KPI Framework — FamiliLook Three-Door Pivot

**Author:** Growth Monitor Agent  
**Date:** 2026-04-02  
**Status:** Active — review weekly  
**Data sources:** /analytics/summary (2026-04-02), baseline (2026-03-28), commerce_status.md

---

## 1. Current Funnel Diagnosis

### Raw Data (2026-04-02)

| Metric | Mar 28 | Apr 2 | Delta |
|---|---|---|---|
| Unique visitors/day | 9 | 4 | -56% |
| Sessions/day | 54 | 12 | -78% |
| Page views/day | 122 | 31 | -75% |
| CTA taps ("Try It Now") | 14 | not tracked separately | — |
| Uploads started | 0 | 0 | no change |
| Uploads completed | 0 | 0 | no change |
| Analyses (real) | 0 | 0 | no change |
| Orders | 0 | 0 | no change |
| Revenue | £0 | £0 | no change |

### Where Users Drop Off

The funnel has a **cliff at the upload step**. Every metric upstream of upload shows activity:

```
Page views (31) → App page visits (11) → Plans page visits (8) → Upload started (0)
                                                                     ^^^^^^^^^^^^^
                                                                     CLIFF: 100% drop
```

Users are browsing (31 page views across 12 sessions = 2.6 pages/session), visiting the app page (11 views), checking plans (8 views), even launching games (6 launches) and viewing kinship group snapshots (7). But **zero** users cross the upload boundary.

### The Engagement-Conversion Gap

| Activity | Count | Converts to Upload? |
|---|---|---|
| App page visits | 11 | No |
| Plans page views | 8 | No |
| Game launches | 6 | No |
| Kinship group snapshots | 7 | No |
| UNO page views | 6 | No |
| Ambassador codes redeemed | 1 | No |

Users are engaged enough to explore 5+ features but not motivated enough to upload family photos. This is a **trust/value gap**, not a usability gap.

### Why the 5 Fixes (Mar 28) Did Not Move the Needle

The 5 fixes (CR-0006) addressed:
1. Result preview on homepage — DEPLOYED
2. Direct CTA to /app?intent=child — DEPLOYED
3. Friendlier biometric consent modal — DEPLOYED
4. Social proof counter — DEPLOYED
5. Concrete value props — DEPLOYED

**Why they failed (5 days later, still 0 uploads):**

1. **Traffic volume too low to measure.** At 4-9 visitors/day, even a 20% conversion rate yields 0-1 uploads. The fixes may have improved intent, but the sample is too small to detect it. You need ~100 visitors to see even one upload at a 1% conversion rate.

2. **Trust barrier not addressed.** The fixes improved *what* users see, but not *why they should trust a new brand with family photos*. No reviews, no press mentions, no social proof from real users (counter shows zero), no recognisable trust signals (e.g., "Used by X families").

3. **The ask is too high for cold traffic.** Uploading family photos (including children's faces) to an unknown website requires a level of trust that homepage copy alone cannot build. The biometric consent modal, even rewritten, reminds users of the risk.

4. **No organic acquisition channel.** All current traffic appears to be direct/internal. Without SEO, paid ads, social referrals, or word-of-mouth, the visitor pool is not refreshing — the same few people are returning and not converting.

5. **Value proposition is unclear at the moment of ask.** Users can see *what* the product does (feature analysis) but not *why it matters to them personally*. "Who does your child look like?" is a curiosity hook, but the landing page answers it abstractly rather than creating an "I need to know" moment.

---

## 2. Three-Door Funnel Models

### Assumptions
- Cold traffic (no brand awareness)
- Mobile-first (80%+ mobile based on typical consumer app traffic)
- UK/US market
- No paid promotion unless specified
- Conversion rates benchmarked against similar photo-upload consumer apps (e.g., face filter apps, heritage photo apps)

### Door 1: Product-Led (Buy a Mug -> Upload -> Analysis -> Product)

**Entry point:** "Get a personalised family mug" (£14.99)  
**Psychology:** Purchase intent arrives with the user. The mug is the goal; the upload is a means.

| Step | Per 100 visitors | Conv. Rate | Notes |
|---|---|---|---|
| Landing page (mug product page) | 100 | — | User arrives wanting a product |
| CTA click ("Personalise Your Mug") | 30 | 30% | Physical product pages convert at 2-5% overall, but CTA click is just engagement — not purchase |
| Upload started (begin photo upload) | 12 | 40% of clicks | Product motivation reduces photo upload friction |
| Upload completed (all required photos) | 8 | 67% of started | Some abandon multi-photo upload (need 2-3 photos) |
| Analysis success | 7 | 88% | Technical success rate (face detection + analysis) |
| Product view (mug preview with results) | 6 | 86% | Most want to see their personalised product |
| Add to basket | 3 | 50% | Price check, comparison shopping |
| Purchase complete | 2 | 67% | Stripe checkout completion rate for known-intent buyers |

**Door 1 output per 100 visitors:** 2 purchases  
**Estimated AOV:** £17.50 (mug + possible message surcharge)  
**Revenue per 100 visitors:** £35.00

### Door 2: Discovery-Led (Who Do I Look Like? -> Upload -> Analysis -> Products)

**Entry point:** "Who does your child look like — Mum or Dad?"  
**Psychology:** Curiosity-driven. No purchase intent. Must convert curiosity into action, then action into purchase.

| Step | Per 100 visitors | Conv. Rate | Notes |
|---|---|---|---|
| Landing page (homepage) | 100 | — | Curiosity hook |
| CTA click ("Try It Free") | 18 | 18% | Curiosity CTAs get clicks, but "free" signals low commitment |
| Upload started | 4 | 22% of clicks | This is the cliff. Biometric consent + multi-photo upload for an unknown brand. Benchmarked against face-app upload rates for new users. |
| Upload completed | 3 | 75% of started | Once committed, most finish |
| Analysis success | 2.7 | 90% | High technical success |
| Product view (keepsakes/games) | 1.4 | 52% | Some users get their answer and leave satisfied |
| Add to basket | 0.3 | 21% | Impulse purchase from a free-entry funnel |
| Purchase complete | 0.2 | 67% | |

**Door 2 output per 100 visitors:** 0.2 purchases  
**Estimated AOV:** £12.00 (mix of postcards, games, occasional mugs)  
**Revenue per 100 visitors:** £2.40

**Note:** Door 2 also generates subscription potential. Of the 2.7 who complete analysis, ~0.3 (11%) may subscribe to Plus for group photos and ongoing features. At £3.99/mo, this adds £1.20 in first-month revenue per 100 visitors, bringing total to ~£3.60.

### Door 3: Match-Led (How Well Do You Match? -> 2 Photos -> Instant Result -> Share)

**Entry point:** "How compatible are your faces?" (FamiliMatch)  
**Psychology:** Social entertainment. Low barrier (2 photos, not family photos). Shareability drives virality.

| Step | Per 100 visitors | Conv. Rate | Notes |
|---|---|---|---|
| Landing page (Match homepage) | 100 | — | Social/fun hook |
| CTA click ("Find Out Now") | 35 | 35% | Higher than Door 2 because the ask is lighter (2 selfies, not family photos) |
| Upload started (photo 1) | 18 | 51% of clicks | Selfie upload has much lower trust barrier than child photos |
| Upload completed (both photos) | 14 | 78% of started | 2 photos is manageable |
| Analysis success (comparison result) | 13 | 93% | High technical success for pair comparison |
| Share result | 5 | 38% | Key viral metric — shareable result card |
| Product view (from result page) | 2 | 15% | Match doesn't have a natural product upsell yet |
| Add to basket | 0.4 | 20% | |
| Purchase complete | 0.25 | 63% | |

**Door 3 output per 100 visitors:** 0.25 purchases  
**Estimated AOV:** £8.00 (postcards, prints — lower-intent buyers)  
**Revenue per 100 visitors:** £2.00

**BUT** Door 3's value is in viral acquisition, not direct revenue. See Section 6.

### Summary: Revenue per 100 Visitors by Door

| Door | Purchases | AOV | Revenue | Primary Value |
|---|---|---|---|---|
| 1: Product-Led | 2.0 | £17.50 | £35.00 | Direct revenue |
| 2: Discovery-Led | 0.2 + 0.3 subs | £12.00 / £3.99 | £3.60 | Analysis engagement + subscriptions |
| 3: Match-Led | 0.25 | £8.00 | £2.00 | Viral acquisition (5 shares per 100 visitors) |

---

## 3. Revenue Projections (30/60/90 Day)

### Key Variables

| Variable | Value | Source |
|---|---|---|
| Current daily visitors | 4-9 | Analytics |
| Current daily revenue | £0 | Analytics |
| Target weekly revenue | £50 | Brief |
| Average order value (blended) | £14.00 | Weighted across doors |
| Blended purchase rate | ~1% of all visitors | Conservative estimate across doors |

### Target: £50/week Revenue

£50/week = £7.14/day = **0.51 orders/day** at £14 AOV.

At a blended 1% purchase rate: need **51 unique visitors/day**.

At current 4 visitors/day, we are **12.75x short** of the minimum viable traffic.

### Traffic Scenarios

| Scenario | Daily Visitors | Weekly Revenue | How to Get There |
|---|---|---|---|
| Current state | 4 | £0 | Organic only, no conversion |
| 10x organic growth | 40 | £28 | SEO + social + referrals (60-90 days) |
| Paid traffic burst | 80 | £56 | £3-5 CPM Facebook/Instagram ads |
| Paid + viral (Door 3) | 120 | £84 | Paid acquisition + viral K=0.5 multiplier |
| Break-even target | 51 | £50 | Minimum viable traffic level |

### 30-Day Projection (Conservative)

**Assumptions:** £200 paid ad budget, Door 1 landing page live, Door 3 sharing enabled.

| Metric | Week 1 | Week 2 | Week 3 | Week 4 | Total |
|---|---|---|---|---|---|
| Daily visitors (organic) | 5 | 8 | 12 | 15 | — |
| Daily visitors (paid) | 20 | 25 | 25 | 25 | — |
| Daily visitors (viral) | 0 | 2 | 5 | 8 | — |
| **Total daily visitors** | 25 | 35 | 42 | 48 | — |
| Daily orders | 0.25 | 0.35 | 0.42 | 0.48 | — |
| **Weekly revenue** | £1.75 | £2.45 | £2.94 | £3.36 | **£10.50** |

**Reality check:** At 30 days, we are unlikely to hit £50/week. The funnel needs to mature, trust signals need to accumulate (reviews, social proof), and organic traffic needs to build.

### 60-Day Projection

| Metric | Month 2 Avg/Day | Weekly Revenue |
|---|---|---|
| Organic visitors | 25 | — |
| Paid visitors | 30 | — |
| Viral (Door 3) | 15 | — |
| **Total** | 70 | — |
| Orders/day | 0.7 | — |
| **Weekly revenue** | — | **£34.30** |

### 90-Day Projection

| Metric | Month 3 Avg/Day | Weekly Revenue |
|---|---|---|
| Organic visitors | 45 | — |
| Paid visitors | 30 | — |
| Viral (Door 3) | 30 | — |
| **Total** | 105 | — |
| Orders/day | 1.05 | — |
| **Weekly revenue** | — | **£51.45** |

**The £50/week target is achievable at ~90 days if paid + viral channels are activated within the next 2 weeks.**

### Which Door Contributes What?

| Door | % of Traffic (Month 3) | % of Revenue | Notes |
|---|---|---|---|
| 1: Product-Led | 20% | 65% | Highest per-visitor revenue |
| 2: Discovery-Led | 45% | 15% | Most organic traffic, lowest conversion |
| 3: Match-Led | 35% | 20% | Revenue is indirect (viral brings Door 1/2 traffic) |

### Target AOV

| Current AOV | Target AOV (30d) | Target AOV (90d) |
|---|---|---|
| £0 (no orders) | £12.00 | £16.00 |

To increase AOV:
- Bundle suggestions (mug + postcard = £18.98 -> bundle £16.99)
- Message personalisation surcharge (£1.99) on every keepsake
- Cross-sell FamiliUno deck (£12.99) alongside keepsakes
- Upsell from postcard (£3.99) to framed canvas (£39.99) with preview

### Break-Even Analysis

| Cost | Monthly |
|---|---|
| Hetzner server | £15 |
| Domain + SSL | £2 |
| Claude API (Haiku for messages) | ~£5 |
| Prodigi per-order cost | ~40% of product price |
| Stripe fees | 1.4% + 20p per transaction |
| **Fixed costs** | ~£22/month |
| **Variable cost per order** | ~£7.50 (avg: 40% COGS + Stripe) |

At £14 AOV and ~£7.50 variable cost per order:
- **Gross margin per order:** £6.50
- **Orders to cover fixed costs:** 22/6.50 = **3.4 orders/month**
- **Break-even traffic:** ~340 visitors/month (at 1% blended conversion)
- **Break-even daily visitors:** ~11/day

**Current traffic (4/day = 120/month) is below break-even, but only by 3x.** This is within reach with modest paid spend.

---

## 4. KPI Dashboard — 7 Daily Metrics

### The 7 KPIs

| # | KPI | Definition | Type | Current Baseline | 7-Day Target | 30-Day Target | Alert Threshold |
|---|---|---|---|---|---|---|---|
| 1 | **Unique Visitors** | Distinct users per day (all doors) | Leading | 4 | 15 | 50 | <5 for 3 consecutive days |
| 2 | **Upload Conversion Rate** | uploads_started / CTA_clicks * 100 | Leading | 0% | 5% | 15% | 0% for 7 consecutive days after fixes |
| 3 | **Upload Completion Rate** | uploads_completed / uploads_started * 100 | Leading | N/A (no uploads) | 60% | 75% | <40% (indicates UX problem) |
| 4 | **Analysis Success Rate** | analyses_success / uploads_completed * 100 | Operational | N/A | 85% | 90% | <70% (indicates backend problem) |
| 5 | **Share Rate (Door 3)** | shares / match_completions * 100 | Leading | 0% | 10% | 25% | <5% (viral loop broken) |
| 6 | **Orders per Day** | Completed Stripe payments | Lagging | 0 | 0.1 | 0.5 | 0 for 14 consecutive days after traffic >20/day |
| 7 | **Revenue per Visitor (RPV)** | total_revenue / unique_visitors | Lagging | £0 | £0.05 | £0.15 | <£0.05 after 30 days (unit economics broken) |

### Leading vs Lagging

| Leading (predict future revenue) | Lagging (confirm past performance) |
|---|---|
| Unique Visitors | Orders per Day |
| Upload Conversion Rate | Revenue per Visitor |
| Upload Completion Rate | |
| Share Rate | |
| Analysis Success Rate (operational) | |

### "Pivot is Failing" Alert Triggers

The three-door pivot should be declared **failing** if ANY of these conditions hold after 30 days of active effort (including paid traffic):

1. **Upload conversion rate stays at 0%** with >200 cumulative visitors — the trust/value proposition is fundamentally broken
2. **Revenue per visitor <£0.02** after 500+ cumulative visitors — the monetisation model doesn't work
3. **Share rate (Door 3) <3%** after 100+ match completions — the viral loop will not compound
4. **Daily visitors plateau <10/day** despite £200+ ad spend — the targeting or creative is wrong
5. **AOV <£8** after 10+ orders — the product mix skews too cheap to sustain

---

## 5. A/B Test Plan

### What to Test First (Priority Order)

| Priority | Test | Hypothesis | Primary Metric |
|---|---|---|---|
| 1 | **Upload page: social proof vs no social proof** | Showing "347 families analysed" (seeded count) increases upload starts by 2x | Upload conversion rate |
| 2 | **CTA copy: "See Your Results" vs "Try It Free"** | Outcome-focused copy converts better than effort-focused copy | CTA click rate |
| 3 | **Door 1 vs Door 2 landing page** | Product-led landing (mug preview) converts better than discovery-led (curiosity hook) | Revenue per visitor |
| 4 | **Biometric consent: inline vs modal** | Inline consent (checkbox below upload) converts better than interrupting modal | Upload completion rate |
| 5 | **Match result page: share CTA placement** | Above-fold share button vs below results | Share rate |

### Statistical Significance Requirements

For a standard A/B test with:
- Baseline conversion rate: 1% (optimistic, since current is 0%)
- Minimum detectable effect (MDE): 100% relative lift (1% -> 2%)
- Significance level: 95%
- Power: 80%

**Required sample size per variant: ~3,800 visitors**  
**Total for A/B test: ~7,600 visitors**

At 4 visitors/day, this would take **1,900 days (5.2 years)**. This is obviously not viable.

### How to Get Enough Data at 7 Users/Day

**Option A: Paid Traffic Burst (Recommended)**

| Parameter | Value |
|---|---|
| Platform | Instagram/Facebook (photo-centric audience) |
| Daily budget | £10-15/day |
| Estimated CPM | £3-5 (UK family demographic) |
| Estimated CPC | £0.30-0.50 |
| Daily clicks | 20-50 |
| Test duration | 14 days |
| Total test visitors | 280-700 |
| Total cost | £140-210 |

At 500 visitors over 14 days, we cannot reach statistical significance for small effects. Instead:

**Option B: Sequential Testing with Aggressive MDE**

Accept a larger MDE (300% relative lift, i.e., 1% -> 4%) to reduce sample size:
- Required per variant: ~400 visitors
- Total: ~800 visitors
- At 35 visitors/day (paid + organic): **23 days per test**

**Option C: Qualitative + Directional Testing**

With <100 visitors/week:
- Run tests as 100% rollouts (not A/B splits)
- Measure week-over-week change
- Use qualitative signals (session recordings via Hotjar free tier, user interviews)
- Make decisions directionally (did uploads go from 0 to >0?) rather than statistically

**Recommendation:** Use Option C for the first 30 days. The immediate goal is to move uploads from 0 to >0. Any change that achieves this is signal enough. Switch to Option B once daily traffic exceeds 30.

### Test Sequence (First 60 Days)

| Week | Test | Method |
|---|---|---|
| 1-2 | Door 1 product-led landing page (100% rollout) | Week-over-week comparison |
| 2-3 | Seeded social proof counter (100% rollout) | Week-over-week comparison |
| 3-4 | Inline consent vs modal (100% rollout) | Week-over-week comparison |
| 5-8 | First A/B test: CTA copy (if traffic >30/day) | Sequential test, 300% MDE |

---

## 6. Viral Coefficient Estimate (Door 3: Match)

### The Viral Loop

```
User completes Match comparison
        |
        v
User sees shareable result card ("You're 78% compatible!")
        |
        v
User shares to Instagram/WhatsApp/TikTok (Share Rate)
        |
        v
Friends see shared link (Impressions)
        |
        v
Friends click link (CTR on shared link)
        |
        v
Friends land on Match page
        |
        v
Friends complete their own comparison (Completion Rate)
        |
        v
Cycle repeats
```

### Model Parameters

| Parameter | Conservative | Moderate | Optimistic | Benchmark Source |
|---|---|---|---|---|
| Share rate (% who share result) | 8% | 15% | 30% | Face filter apps: 10-25% |
| Impressions per share | 50 | 120 | 300 | Instagram Story: ~100, WhatsApp: ~20, TikTok: 200-1000 |
| CTR on shared link | 3% | 6% | 12% | Social link CTR: 2-8% |
| Completion rate (clicked -> completed) | 25% | 35% | 50% | Low-friction 2-photo upload |

### K-Factor Calculation

**K = Share Rate x Impressions per Share x CTR x Completion Rate**

But K-factor is typically expressed as: **K = invitations sent per user x conversion rate per invitation**

Reframing:
- **Invitations per user** = Share Rate x Impressions per Share x CTR = effective invitations that reach a potential new user
- **Conversion per invitation** = Completion Rate (they complete their own match)

| Scenario | Share Rate | Imp/Share | CTR | Completion | K-Factor |
|---|---|---|---|---|---|
| Conservative | 8% | 50 | 3% | 25% | 0.08 x 50 x 0.03 x 0.25 = **0.03** |
| Moderate | 15% | 120 | 6% | 35% | 0.15 x 120 x 0.06 x 0.35 = **0.38** |
| Optimistic | 30% | 300 | 12% | 50% | 0.30 x 300 x 0.12 x 0.50 = **5.40** |

### Interpretation

| K-Factor | Meaning | Growth Type |
|---|---|---|
| K < 0.1 | No viral effect. Each user generates <0.1 new users. | Linear (paid-only) |
| K = 0.3-0.5 | Viral amplifier. Each paid user brings 0.3-0.5 extra users for free. | Amplified paid |
| K = 1.0 | Self-sustaining. Each user brings 1 new user. | Organic viral |
| K > 1.0 | Exponential growth. | Explosive (unsustainable) |

**At what K-factor does Door 3 become self-sustaining?**

K >= 1.0. This requires:
- Share rate >= 20% AND
- Impressions >= 150 AND  
- CTR >= 8% AND
- Completion >= 42%

This is achievable only with a **genuinely entertaining, visually shareable result** (think: "We're 92% Feature Twins!" with a merged face image) AND a frictionless share-to-complete loop (no app install, instant mobile web experience).

### Realistic Viral Trajectory

Starting with 10 Match completions/day (from paid traffic):

| Day | Organic from Viral (K=0.03) | Organic from Viral (K=0.38) |
|---|---|---|
| 1 | 10.3 total | 13.8 total |
| 7 | 10.3 total | 15.2 total |
| 30 | 10.3 total | 16.1 total |
| 90 | 10.3 total | 16.1 total |

At K=0.03 (conservative), viral is irrelevant.  
At K=0.38 (moderate), viral adds ~38% more users for free — a meaningful cost reduction on paid acquisition.

**To reach K=1.0, focus engineering effort on:**
1. One-tap share to Instagram Stories with pre-formatted result card
2. Shared link opens directly to a pre-filled comparison (friend's photo already loaded, recipient just adds theirs)
3. Result card designed for maximum curiosity ("You won't believe our score...")
4. WhatsApp deep-link with preview image (Open Graph tags)

---

## 7. Action Plan — Next 14 Days

| Day | Action | Owner | KPI Impact |
|---|---|---|---|
| 1-2 | Build Door 1 landing page (product-led mug page) | FE Lead | Revenue per visitor |
| 1-2 | Implement upload funnel event tracking (each step as separate analytics event) | FE Lead | All funnel KPIs |
| 3-4 | Add seeded social proof ("347+ families analysed") | FE Lead | Upload conversion rate |
| 3-4 | Build shareable result card for Door 3 (Match) | FE Lead | Share rate |
| 5-7 | Set up £10/day Instagram ad campaign targeting UK parents 25-40 | Marketing Lead | Unique visitors |
| 5-7 | Set up Hotjar free tier for session recordings | Growth Monitor | Qualitative insights |
| 8-10 | Review first week of paid traffic data. Adjust targeting. | Growth Monitor | All |
| 10-12 | Implement inline consent experiment (replace modal) | FE Lead | Upload completion rate |
| 12-14 | First weekly funnel report with real conversion data | Growth Monitor | — |

### Success Criteria at Day 14

| Metric | Minimum Acceptable | Good | Excellent |
|---|---|---|---|
| Daily visitors | 20 | 40 | 60+ |
| Uploads started (cumulative) | 5 | 15 | 30+ |
| Uploads completed (cumulative) | 3 | 10 | 20+ |
| First real order | 0 (acceptable) | 1 | 3+ |
| Match shares | 2 | 8 | 20+ |

---

## 8. Honest Assessment

**The hard truth:** At 4 visitors/day and 0% upload conversion, no amount of funnel optimisation will generate revenue. The platform has two independent problems:

1. **No traffic.** The product is invisible. SEO is non-existent for a new domain. No social presence. No word-of-mouth (zero users have completed the product).

2. **No conversion.** Even the visitors who arrive are not uploading. The trust gap for family photo upload on an unknown brand is enormous.

**These must be solved in parallel, not sequentially.** Fixing the funnel without traffic means testing in a vacuum. Driving traffic without fixing the funnel means burning ad budget.

**The fastest path to first revenue:**
- Door 1 (product-led) has the shortest path because purchase intent arrives with the user. A parent who wants a personalised family mug is already motivated to upload photos.
- Door 3 (match-led) has the lowest friction and highest share potential, but weakest monetisation. Use it as a traffic multiplier, not a revenue driver.
- Door 2 (discovery-led) is the long game. It depends on brand trust that takes months to build.

**Spend the first £200 on Door 1 Instagram ads showing the physical mug product. Not the analysis. Not the games. The mug.**

---

*Next review: 2026-04-09 (7-day checkpoint)*  
*Escalation trigger: 0 uploads after 14 days with paid traffic active*
