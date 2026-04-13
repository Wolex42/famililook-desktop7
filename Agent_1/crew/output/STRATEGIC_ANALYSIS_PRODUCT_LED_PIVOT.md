# Strategic Marketing Analysis: Product-Led Pivot

**Author:** CMO (Agent Persona)
**Date:** 2026-04-01
**Status:** CEO-approved pivot. Analysis for execution planning.

---

## Executive Summary

FamiliLook has 7 daily users, 0 uploads, and GBP 0 revenue after 5 conversion fixes that produced no measurable impact. The root cause is structural: asking users to upload family photos into an unknown AI tool is a trust-and-motivation barrier that no amount of copy or CTA optimisation will solve.

The pivot reframes the entire platform around three entry points ("doors") that each lead with a concrete value proposition before requesting photos. This analysis covers positioning, funnel modelling, occasion mapping, pricing, channel strategy, and risk assessment.

---

## 1. Positioning Analysis

### Competitive Frame Shift

| Dimension | Before (Process-Led) | After (Product-Led) |
|-----------|---------------------|---------------------|
| **Category** | AI face analysis tool | Personalised family gifts + games |
| **Competitors** | FaceApp, MyHeritage, Gradient | Moonpig, Shutterfly, Not On The High Street, Personalised Memento |
| **User intent** | "Analyse my face" (curiosity, low urgency) | "Buy something for Mum" (occasion-driven, high urgency) |
| **Willingness to upload** | Low (no clear payoff) | High (required to make the gift) |
| **Pricing anchor** | Free AI tool (subscription feels expensive) | GBP 14.99 mug (subscription feels like a discount) |
| **Purchase trigger** | Post-analysis upsell (user already satisfied) | Pre-analysis intent (user came to buy) |

### Risks of This Positioning Shift

1. **Inventory-less personalisation is hard to explain.** Users expect personalised gifts to involve choosing text/photos for a template. "AI analyses your family bond and puts it on a mug" requires a 10-second education moment. If that moment fails, bounce.
2. **Moonpig owns the occasion-gift mental model.** We are not competing on selection (they have 10,000+ products). We compete on uniqueness: "No one else can put your genetic bond score on a mug."
3. **SEO shift takes 3-6 months.** Current domain authority is negligible. Ranking for "personalised mug" is a GBP 2-5 CPC keyword dominated by established players. Paid must carry acquisition in the short term.
4. **Product quality risk.** Prodigi fulfilment is live but untested at scale. First negative review on a GBP 14.99 mug kills trust for a micro-brand.
5. **Door 2 ("Find out") cannibalises Door 1 ("Make something").** If free analysis is too satisfying, users never reach the product page. Must design the free flow to leave a gap that products fill (e.g., watermarked results, "get this on a mug" CTA on every result card).

### Defensible Advantage

The AI engine (desktop3) performs calibrated 8-feature facial inheritance analysis that no personalised gift competitor can replicate. Moonpig lets you upload a photo onto a mug. We let you upload 3 photos and generate "You inherited Mum's eyes, Dad's smile, and 72% of Mum's features" and put THAT on a mug. The analysis IS the product. This is a genuine technical moat — replicating it requires ML infrastructure, calibrated feature models, and the kinship analysis pipeline.

**Competitive positioning statement:** "The only gifts that know your family."

---

## 2. Funnel Modelling (Three Doors)

### Baseline Reality
- 7 daily users (organic)
- 31 page views / day
- 0 uploads, 0 analyses, 0 purchases
- 5 conversion fixes deployed 5 days ago: no measurable impact

### Door 1: "Make Something" (Product-Led)

**User intent:** "I want a gift for [person] for [occasion]."

| Stage | Metric | Conservative | Optimistic | Notes |
|-------|--------|-------------|-----------|-------|
| Traffic source | Primary | Paid social + Google Shopping | Same | Occasion-driven; SEO takes months |
| Landing | Visitors/day | 50 (paid) | 200 (paid) | At GBP 0.50-1.50 CPC |
| Landing to Product View | CVR | 40% | 60% | Product cards with prices are immediately visible |
| Product View to Upload | CVR | 15% | 25% | "Make your gift" framing; upload is a means to an end |
| Upload to Results | CVR | 85% | 95% | Once committed, low drop-off |
| Results to Purchase | CVR | 20% | 35% | Product is pre-selected; results reinforce intent |
| **End-to-end Landing to Purchase** | **CVR** | **1.0%** | **5.0%** | |
| AOV | GBP | 18.00 | 24.00 | Mug + message surcharge or multi-item |
| Viral coefficient | k | 0.05 | 0.15 | Low: gifts are private. Some "look what I got" shares |

**Revenue per 100 paid visitors:** GBP 18-120
**Revenue generation speed:** FASTEST. Users arrive with purchase intent.

### Door 2: "Find Out" (Curiosity-Led)

**User intent:** "Who do I look like — Mum or Dad?"

| Stage | Metric | Conservative | Optimistic | Notes |
|-------|--------|-------------|-----------|-------|
| Traffic source | Primary | Organic social, viral shares, SEO (long-term) | Same | "Which parent do you look like?" is shareable |
| Landing | Visitors/day | 20 (organic+viral) | 100 | Viral loops if sharing works |
| Landing to Upload | CVR | 8% | 20% | Free, curiosity-driven. Still requires 3 photos |
| Upload to Results | CVR | 80% | 90% | Processing anxiety causes some drop-off |
| Results to Product View | CVR | 25% | 40% | "Get this on a mug" CTA on results page |
| Product View to Purchase | CVR | 8% | 15% | Impulse buy; not pre-intended |
| **End-to-end Landing to Purchase** | **CVR** | **0.13%** | **1.1%** | |
| AOV | GBP | 16.00 | 20.00 | Single item impulse |
| Viral coefficient | k | 0.2 | 0.5 | HIGH: results are inherently shareable ("I'm 72% Mum!") |

**Revenue per 100 organic visitors:** GBP 2-22
**Volume generation speed:** HIGHEST (if viral loop activates). Revenue is secondary.

### Door 3: "How Well Do You Match?" (FamiliMatch Solo)

**User intent:** "How similar are our faces?"

| Stage | Metric | Conservative | Optimistic | Notes |
|-------|--------|-------------|-----------|-------|
| Traffic source | Primary | Paid social (TikTok, Instagram), viral | Same | "Compare your face with your bestie" |
| Landing | Visitors/day | 100 (paid) | 500 | Lowest CPC: fun, non-committal |
| Landing to Upload | CVR | 20% | 40% | Only 2 photos. No family context needed. Lowest friction |
| Upload to Results | CVR | 90% | 95% | Very fast processing; minimal drop-off |
| Results to Share | CVR | 15% | 30% | "We're 78% alike!" is highly shareable |
| Results to Product View | CVR | 5% | 12% | Products less natural fit for Match |
| Product View to Purchase | CVR | 5% | 10% | Novelty purchase (matching mugs?) |
| **End-to-end Landing to Purchase** | **CVR** | **0.05%** | **0.46%** | |
| AOV | GBP | 14.99 | 18.00 | Single mug or postcard |
| Viral coefficient | k | 0.3 | 0.8 | HIGHEST: social content, friend tags, duets |

**Revenue per 100 paid visitors:** GBP 0.70-8.30
**CPA efficiency:** BEST for user acquisition. WORST for direct revenue.
**Strategic role:** Top-of-funnel volume driver. Feeds Doors 1 and 2 via retargeting.

### Summary: Which Door Wins?

| Objective | Winner |
|-----------|--------|
| Revenue fastest | Door 1 ("Make Something") |
| Volume fastest | Door 3 ("How Well Do You Match?") |
| Highest LTV per user | Door 1 (purchase-intent users) |
| Lowest CPA | Door 3 (fun + viral) |
| Best viral loop | Door 3, then Door 2 |
| Best for brand building | Door 2 ("Find Out" — the core IP) |

**Recommended allocation of first GBP 500 ad spend:**
- 50% Door 3 (build audience, test viral loop, collect retargeting pixels)
- 35% Door 1 (validate purchase conversion, test occasion messaging)
- 15% Door 2 (organic-first; paid only to amplify viral content)

---

## 3. Occasion Calendar Alignment (April-September 2026)

| Month | Occasion | Primary Door | Hero Products | Campaign Start | Spend Weight |
|-------|----------|-------------|---------------|----------------|-------------|
| **April** | Easter (Apr 5) | Door 2 | Family analysis (free), postcards (GBP 3.99) | NOW (already late) | Light — test only |
| **April** | Spring break | Door 3 | FamiliMatch Solo (friends comparing) | Apr 1-14 | Medium |
| **May** | Mother's Day UK (Mar 22 — PASSED) | -- | -- | -- | -- |
| **May** | Mother's Day US (May 10) | Door 1 | Character Mug (GBP 16.99), Family Mug Set (GBP 27.99), Framed Canvas (GBP 39.99) | Apr 20 | HEAVY |
| **May** | Eid al-Fitr (late Mar/early Apr — check date) | Door 1 | Greeting cards (GBP 6.99), cushions (GBP 29.99) | 2 weeks before | Medium |
| **June** | Father's Day UK+US (Jun 21) | Door 1 | Ceramic Mug (GBP 14.99), T-Shirt (GBP 19.99), Card Deck (GBP 24.99) | Jun 1 | HEAVY |
| **June** | End of school year | Door 2 | "Who do your kids look like?" — postcards, greeting cards | Jun 8 | Light |
| **July** | Summer holidays | Door 3 | FamiliMatch — "Road trip game: compare everyone" | Jul 1 | Medium |
| **July** | Best Friend Day (Jul 30) | Door 3 | "How well do you match your bestie?" — matching mugs | Jul 16 | Medium |
| **August** | Grandparents Day prep (Sep 7) | Door 1 | Fine Art Print (GBP 24.99), Framed Canvas (GBP 39.99), Family Mug Set | Aug 18 | Heavy |
| **August** | Back to school | Door 2 | "Before they grow up — capture who they look like" | Aug 15 | Light |
| **September** | Grandparents Day (Sep 7) | Door 1 | Premium keepsakes (canvas, mug set, cushion) | Aug 18 (see above) | HEAVY |

### Key Insight: Mother's Day US (May 10) is the First Real Test

- 39 days away. Enough time to build the Door 1 landing page and run 2 weeks of paid ads.
- Hero product: Character Mug ("Mum, I got your eyes" printed with analysis results).
- Target CPA: GBP 5.00. Target ROAS: 3x (GBP 15 AOV / GBP 5 CPA).
- If this campaign converts at >0.5% end-to-end, the pivot is validated.

---

## 4. Pricing Strategy

### Current Model (Subscription-First)

```
Free tier:    2 analyses, watermarked keepsakes, no ordering
Plus GBP 3.99/mo:  Unlimited analyses, ordering unlocked, 10% off
Pro GBP 7.99/mo:   Plus + peer lobby, explain-why, 15% off
```

**Problem:** A user who wants to buy a GBP 14.99 mug must first subscribe to Plus (GBP 3.99/mo), making the real cost GBP 18.98 for the first mug. This is a conversion killer. The subscription feels like a tax, not a benefit.

### Proposed Model (Product-First)

```
Free tier:    2 analyses, CAN order keepsakes at full price
Plus GBP 3.99/mo:  Unlimited analyses, 10% off all products, group photos
Pro GBP 7.99/mo:   Plus + peer lobby, explain-why, 15% off
```

**Key change:** Remove the ordering gate from Free tier. Anyone can buy a mug. Subscription becomes a discount programme, not a paywall.

### LTV Analysis: Gated vs Ungated Purchasing

#### Scenario A: Subscription Required to Purchase (Current)

| Metric | Value | Calculation |
|--------|-------|-------------|
| Visitor to subscriber | 0.5% | Industry avg for micro-brand SaaS |
| Subscriber to purchaser | 15% | Must still navigate to products |
| Monthly churn | 20% | No habit loop established |
| Avg subscription duration | 5 months | 1/churn rate |
| Subscription LTV | GBP 19.95 | 5 x GBP 3.99 |
| Product purchases per subscriber | 1.5 | Over lifetime |
| Product AOV | GBP 18.00 | |
| Product LTV | GBP 27.00 | 1.5 x GBP 18.00 |
| **Total LTV per subscriber** | **GBP 46.95** | |
| **LTV per visitor** | **GBP 0.23** | 0.5% x GBP 46.95 |

#### Scenario B: One-Off Purchases Allowed (Proposed)

| Metric | Value | Calculation |
|--------|-------|-------------|
| Visitor to first purchase | 1.0% | 2x conversion (no subscription gate) |
| First purchase AOV | GBP 18.00 | |
| Repeat purchase rate | 25% | Occasion-driven returns |
| Repeat purchases per buyer | 1.8 | Over 12 months |
| Total product LTV per buyer | GBP 32.40 | 1.8 x GBP 18.00 |
| Buyer to subscriber upgrade | 20% | "Save 10% on your next order" |
| Subscription LTV (upgraders) | GBP 15.96 | 4 months avg x GBP 3.99 |
| **Blended LTV per buyer** | **GBP 35.59** | GBP 32.40 + (20% x GBP 15.96) |
| **LTV per visitor** | **GBP 0.36** | 1.0% x GBP 35.59 |

#### Verdict

| Model | LTV per Visitor | Conversion Rate | Revenue at 100 visitors/day (30 days) |
|-------|----------------|-----------------|---------------------------------------|
| Gated (current) | GBP 0.23 | 0.5% | GBP 690 |
| Ungated (proposed) | GBP 0.36 | 1.0% | GBP 1,080 |

**Recommendation: Remove the subscription gate for purchasing. Allow one-off purchases on Free tier.**

The 56% increase in LTV per visitor comes from doubling the conversion rate by removing friction. The subscription revenue loss is more than offset by product revenue gains.

**Implementation priority:**
1. Remove `canOrderMerchandise()` gate from Free tier (or make it always return true for single-item purchases)
2. Add "Subscribe for 10% off" upsell on the basket/checkout page
3. Add post-purchase email: "You saved GBP 0.00 on this order. Plus members save GBP X.XX."

---

## 5. Channel Strategy

### Budget Reality

With 7 daily organic users and GBP 0 revenue, the ad budget is likely GBP 500-2,000 for initial testing. Every pound must be measurable.

### Channel Allocation

| Channel | Door | Budget % | CPC Estimate | Creative Strategy | KPI |
|---------|------|----------|-------------|-------------------|-----|
| **TikTok Ads** | Door 3 | 30% | GBP 0.15-0.40 | UGC-style: "I compared my face with my bestie and we're 87% alike" | Installs, shares |
| **Instagram Reels** | Door 3 + Door 1 | 25% | GBP 0.30-0.80 | Split: fun comparisons (Door 3) + "Mum I got your eyes" gift reveal (Door 1) | Link clicks, purchases |
| **Facebook Ads** | Door 1 | 25% | GBP 0.40-1.00 | Occasion-driven: "Mother's Day gift she's never seen before" with product mockups | ROAS, purchases |
| **Google Shopping** | Door 1 | 15% | GBP 0.80-2.00 | Product listing ads: "Personalised Family Mug GBP 14.99" | ROAS, purchases |
| **Google Search** | Door 2 | 5% | GBP 1.00-3.00 | Brand + curiosity: "who do I look like mum or dad" | Uploads, analyses |

### Creative Strategy by Channel

**TikTok (Door 3 primary)**
- Format: 15-second UGC vertical video
- Hook (0-3s): "Wait till you see how alike we look..."
- Reveal (3-10s): Screen recording of FamiliMatch comparison loading, result reveal
- CTA (10-15s): "Try it with YOUR friend — link in bio"
- Targeting: 18-30, interests: friendship, selfies, face filters
- Why TikTok: Lowest CPM for entertainment content. Door 3 IS entertainment.

**Instagram (Door 3 + Door 1)**
- Reels for Door 3: Same UGC approach as TikTok, cross-posted
- Stories for Door 1: Product-focused. Show the mug, the analysis on it, the reaction.
- Carousel for Door 1: "3 steps to the most unique gift ever" — (1) Upload 3 photos (2) See who they look like (3) Get it on a mug
- Targeting: 25-45 for Door 1 (gift buyers), 18-30 for Door 3

**Facebook (Door 1 primary)**
- Format: Single image + carousel ads
- Audience: Women 30-55 (primary gift purchasers), parents, "interested in: Moonpig, Not On The High Street"
- Copy: Occasion-specific. "This Mother's Day, give her something no one else can: proof that you got her smile."
- Retargeting: Anyone who visited Door 3 but didn't convert on Door 1

**Google Shopping (Door 1)**
- Product feed: Personalised Family Mug, Character Mug, Family Mug Set, T-Shirt, Card Deck
- Titles optimised: "Personalised Family Bond Mug - AI-Analysed Features - GBP 14.99"
- Requires: Merchant Center setup, product feed, GTINs (or exempt as custom products)

**Google Search (Door 2 — minimal spend)**
- Keywords: "who do I look like mum or dad", "which parent do I look like", "family resemblance test"
- These are long-tail, low-volume, but high-intent and low-competition
- Expected: 5-20 clicks/day at GBP 1-2 CPC

### Retargeting Flow (Cross-Door)

```
Door 3 visitor (fun) --[pixel]--> Facebook/Instagram retargeting
  --> Door 1 ad: "Loved comparing? Now make a gift from it"
  --> Door 2 ad: "Curious which parent you look like?"

Door 2 visitor (curiosity) --[pixel]--> Retarget with Door 1
  --> "Your results would look amazing on a mug"

Door 1 visitor (intent) --[pixel]--> Cart abandonment retarget
  --> "Still thinking about that mug? Here's 10% off"
```

This cross-door retargeting is where the three-door strategy compounds. Door 3 fills the top of funnel cheaply. Door 1 monetises the warm audience.

---

## 6. Risk Assessment

### What Could Go Wrong

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Users still won't upload even for gifts** | Medium | Critical | Door 3 (2 photos, fun context) validates upload willingness at lowest friction. If Door 3 fails, the photo barrier is truly insurmountable and we need pre-generated demo products. |
| **Prodigi fulfilment issues at scale** | Low | High | Order 5 test products ourselves first. Set up webhook monitoring for failed prints. Have customer service playbook ready. |
| **Paid ads burn budget with no conversions** | Medium | Medium | Cap daily spend at GBP 10/channel. Kill any ad set with 0 conversions after 500 impressions. A/B test aggressively in week 1. |
| **Competitors copy the concept** | Low (short-term) | Low | The ML pipeline is the moat. Moonpig can't replicate 8-feature calibrated analysis. They'd need 6+ months to build equivalent. |
| **"Personalised gift" SEO is unwinnable** | High | Medium | Don't fight for generic terms. Own the niche: "family resemblance gift", "who do I look like mug". Long-tail is winnable. |
| **Door 1 cannibalises Door 2 (fewer free analyses)** | Low | Low | Good problem. If people skip free analysis and go straight to buying, revenue increases. |
| **Brand confusion across 3 doors** | Medium | Medium | Each door needs its own landing page with clear value prop. Do NOT try to explain all 3 on one homepage. |
| **Subscription revenue drops** | High | Low | Current subscription revenue is GBP 0. Nothing to lose. Product revenue replaces it. |

### Success Metrics: 7-Day and 30-Day Signals

#### 7-Day Signals (by Apr 8)

| Metric | Signal: Working | Signal: Failing | Source |
|--------|----------------|-----------------|--------|
| Uploads | >5 total across all doors | 0 (same as before) | Analytics dashboard |
| Door 3 upload rate | >10% of visitors upload | <5% | Analytics |
| Door 1 product views | >20% of Door 1 visitors view a product | <10% | Analytics |
| Ad CTR | >1.5% (TikTok), >0.8% (Facebook) | <0.5% | Ad platforms |
| Time on site | >90 seconds average | <30 seconds | Analytics |
| Shares from Door 3 | >2% of result viewers share | 0 shares | Analytics |

#### 30-Day Signals (by May 1)

| Metric | Signal: Working | Signal: Failing | Source |
|--------|----------------|-----------------|--------|
| Revenue | >GBP 50 total | GBP 0 | Stripe |
| Uploads per day | >5/day average | <1/day average | Analytics |
| Purchase conversion (Door 1) | >0.5% end-to-end | <0.1% | Analytics + Stripe |
| Viral coefficient (Door 3) | k > 0.1 | k < 0.02 | Referral tracking |
| CAC (blended) | <GBP 15 | >GBP 50 | Ad spend / purchases |
| Returning visitors | >10% return within 7 days | <2% | Analytics |
| Mother's Day US pre-orders | >10 orders by May 5 | 0 orders | Stripe |

### Kill Criteria

**Revert to old approach if ALL of the following are true after 30 days:**

1. Total uploads across all 3 doors: < 10 (proves the photo barrier exists regardless of framing)
2. Total revenue: GBP 0 (proves product-led framing does not convert)
3. Door 3 viral coefficient: k < 0.02 (proves the fun/social angle does not generate shares)
4. Ad spend exhausted with CPA > GBP 50 per upload (proves paid acquisition is not viable)

**Do NOT revert if any single door shows promise.** The three-door strategy allows independent A/B testing. Kill underperforming doors, double down on working ones.

**If we revert:** The fallback is a content-led strategy (blog posts, YouTube videos about family resemblance science) to build organic traffic over 6-12 months before attempting conversion again. This is slower but has near-zero marginal cost.

---

## 7. Immediate Action Plan (Next 14 Days)

| Day | Action | Owner | Dependency |
|-----|--------|-------|------------|
| 1-3 | Build Door 1 landing page: product grid with prices, occasion messaging, "Make your gift" CTA | FE Lead | Design spec |
| 1-3 | Build Door 3 landing page: "Compare your faces" with 2-photo upload | FE Lead | Already exists (FamiliMatch Solo) — needs landing page wrapper |
| 1-3 | Remove subscription gate for purchasing (allow Free tier to buy) | FE Lead + BE Lead | Backend permission required |
| 4-5 | Create 5 TikTok ad creatives (Door 3: friend comparison UGC-style) | Marketing | Screen recordings needed |
| 4-5 | Create 3 Facebook/Instagram ad creatives (Door 1: Mother's Day gift) | Marketing | Product mockup images needed |
| 5-7 | Set up Meta Ads + TikTok Ads accounts, pixel installation, conversion tracking | Marketing | GBP 500 initial budget |
| 7-10 | Launch Door 3 campaign (TikTok + Instagram) at GBP 10/day | Marketing | Creatives approved |
| 7-10 | Launch Door 1 campaign (Facebook + Google Shopping) at GBP 10/day | Marketing | Landing page live |
| 10-14 | Analyse first 7 days of data. Kill losing ad sets. Scale winners. | CMO + Growth Monitor | Analytics dashboard |
| 14 | Go/no-go decision on Mother's Day US campaign scale-up | CEO + CMO | 7-day metrics |

### Budget Summary (First 30 Days)

| Line Item | Amount |
|-----------|--------|
| TikTok Ads (Door 3) | GBP 150 |
| Instagram/Facebook Ads (Door 1 + 3) | GBP 200 |
| Google Shopping (Door 1) | GBP 100 |
| Google Search (Door 2) | GBP 50 |
| **Total** | **GBP 500** |

**Expected outcomes at GBP 500 spend:**
- Conservative: 800-1,500 visitors, 10-30 uploads, 1-5 purchases (GBP 15-90 revenue)
- Optimistic: 2,000-4,000 visitors, 80-200 uploads, 10-40 purchases (GBP 150-720 revenue)

---

## 8. Key Strategic Conclusions

1. **Door 1 is the revenue engine.** It has the highest per-visitor value because users arrive with purchase intent. Mother's Day US (May 10) is the first real test.

2. **Door 3 is the acquisition engine.** It has the lowest friction (2 photos, no family context, pure fun) and highest viral potential. It feeds Doors 1 and 2 via retargeting.

3. **Door 2 is the brand engine.** "Who do I look like?" is the core IP and the most defensible positioning. It should be the organic/SEO play while Doors 1 and 3 carry paid.

4. **Remove the subscription gate immediately.** Requiring GBP 3.99/month before allowing a GBP 14.99 purchase is the second-biggest conversion killer after the upload barrier. Product-first pricing increases LTV per visitor by 56%.

5. **The pivot is low-risk because the baseline is zero.** Current revenue is GBP 0. Current uploads are 0. Any measurable conversion is an improvement. The kill criteria require all three doors to fail simultaneously before reverting.

6. **The 39-day window to Mother's Day US is the forcing function.** It creates urgency for implementation, provides a natural campaign hook, and gives us the first real revenue data point. If we miss this window, the next major occasion is Father's Day (June 21) — 81 days away.

---

*This analysis should be reviewed by the CEO and used as the basis for the Door 1 and Door 3 landing page specs. The Growth Monitor agent should track all metrics listed in Section 6 daily starting from campaign launch.*
