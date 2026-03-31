# Creative Brief: FamiliLook Character Mugs
## CMO Agent — Strategic Product Line Brief
## Date: 30 March 2026 | Status: DRAFT — Awaiting CEO Approval

---

## Executive Summary

FamiliLook Character Mugs are a new product line that combines **illustrated cartoon characters** with **real family analysis data** to create gift-worthy, social-media-viral personalised mugs. They bridge the gap between our current data-rich-but-clinical mug designs and the bold, humorous, character-driven style that is proven to drive TikTok virality (evidenced by Cornish Prints UK, 1000-2000+ likes per post on TikTok Shop).

The key insight: Cornish Prints sells the same generic design to everyone. We sell a design that is **unique to each family** — powered by real AI analysis. Character Mugs wrap that data in a warm, giftable, shareable package.

---

## 1. Concept — Positioning

### Three-way positioning

| Dimension | Current FamiliLook Mugs | Cornish Prints UK | **Character Mugs (NEW)** |
|-----------|------------------------|-------------------|--------------------------|
| Visual style | Clean, data-forward, serif typography | Bold cartoons, hand-drawn feel, all-caps | **Illustrated characters + bold type + real data** |
| Personalisation | High (photo, %, features, AI comment) | None (generic designs) | **High (characters driven by analysis outcome)** |
| Emotional tone | Informative, sentimental | Cheeky, humorous, relatable | **Warm, playful, gift-funny** |
| Social shareability | Low (feels private/clinical) | Very high (one-liners, cartoon characters) | **Very high (personalised one-liners + characters)** |
| Price driver | Data quality | Character appeal | **Both** |
| Gift appeal | Moderate (needs context to understand) | High (instant visual impact) | **High (instant impact + personal meaning)** |

### The pitch in one sentence

> "Character Mugs turn your baby's real resemblance results into a bold, funny, illustrated keepsake that grandparents will show off and TikTok will share."

### Relationship to current mugs

Character Mugs do **not** replace the existing `mug_wrap` or `family_mug_set` products. They are an additional product line — a new `character_mug` entry in `templateRegistry.js` and `printProfiles.js`. Customers who want the data-forward clean style still get it. Character Mugs target the **gift buyer** and **social sharer** who currently bounces because our mugs feel too clinical.

---

## 2. Character System — The FamiliLook Family

### 2.1 Character roster

Define a set of **5 core characters** in a consistent illustrated style:

| Character | Name | Description | When used |
|-----------|------|-------------|-----------|
| Mum | **Mama Bear** | Rounded, warm, expressive eyes, hair bun or natural curls. Holding a cup of tea. | Winner = Mum, or Mother's Day occasion |
| Dad | **Papa Bear** | Rounded, broad shoulders, kind expression, glasses optional. Holding baby/child. | Winner = Dad, or Father's Day occasion |
| Baby | **Little Cub** | Oversized head, huge eyes, dummy/pacifier. Sits on a cushion. | Child age 0-2 in analysis |
| Child | **Mini Me** | Slightly older Little Cub, backpack or toy, cheeky grin. | Child age 3-12 in analysis |
| Grandparent | **Gran/Gramps** | Cosy, reading glasses, cardigan, cup of tea. Warm smile. | Gift recipient = grandparent (occasion tag) |

### 2.2 Style direction

- **Simple, rounded silhouettes** — Mr. Men/Little Miss inspired but not derivative
- **Thick outlines** (3-4px at print scale), filled with flat colour
- **Expressive faces** — 4-5 emotion variants per character (happy, surprised, proud, cheeky, sleeping)
- **No realistic proportions** — these are cartoon mascots, not portraits
- **Colour-neutral skin** — characters use the theme's accent palette, not realistic skin tones (avoids representation issues; the real photos handle identity)
- **SVG format** — scalable, theme-colourable, tiny file size
- **Consistent canvas** — all characters fit within a 300x300px bounding box for layout predictability

### 2.3 How characters interact with real data

Characters do NOT replace the user's photos. They **frame** the data:

- Character stands next to or points at the real child photo
- Character holds a sign/banner with the personalised headline
- Character reacts to the percentage ("Papa Bear looking VERY proud at 78%")
- Feature callout badges float around the character ("Got Mum's Eyes" with an arrow pointing to the character's exaggerated eyes)

The child's real photo remains the emotional centrepiece. The character is the **narrator/presenter** of the data.

---

## 3. Typography Direction

### 3.1 Font system

| Role | Font | Style | Notes |
|------|------|-------|-------|
| **Hero headline** | Rounded bold sans-serif (e.g., Nunito Black, Baloo 2 Bold) | ALL CAPS, large, punchy | The "Cornish Prints" energy — bold, hand-drawn feel |
| **Sub-headline** | Same family, regular weight | Sentence case, smaller | Supporting context |
| **Data labels** | Current Georgia serif (from `mugThemes.js`) | As-is | Maintains brand continuity for the data layer |
| **Brand mark** | System sans, small, muted | As-is | "famililook.com" |

### 3.2 Data-driven headline system

Headlines are **auto-generated** from the analysis result. The template selects the appropriate headline based on winner, percentage, and occasion.

#### When child looks like Mum (high %, winner = parent1/Mum)

| Headline | Trigger condition |
|----------|-------------------|
| `MUMMY'S MINI ME` | winnerPct >= 70, winner = Mum |
| `SORRY DAD, I'M ALL MUM` | winnerPct >= 75, winner = Mum |
| `MUM DID ALL THE WORK` | winnerPct >= 65, winner = Mum |
| `COPY + PASTE: MUM EDITION` | winnerPct >= 70, winner = Mum |
| `LIKE MOTHER, LIKE BABY` | winnerPct >= 60, winner = Mum |
| `MUM'S GREATEST HIT` | winnerPct >= 65, winner = Mum |

#### When child looks like Dad (high %, winner = parent2/Dad)

| Headline | Trigger condition |
|----------|-------------------|
| `DADDY'S DOUBLE` | winnerPct >= 70, winner = Dad |
| `SORRY MUM, THIS ONE'S ALL DAD` | winnerPct >= 75, winner = Dad |
| `DAD'S CTRL+C, CTRL+V` | winnerPct >= 70, winner = Dad |
| `THE APPLE DOESN'T FALL FAR` | winnerPct >= 60, winner = Dad |
| `STRONG GENES, DAD` | winnerPct >= 65, winner = Dad |
| `DAD'S GREATEST HIT` | winnerPct >= 65, winner = Dad |

#### When it's a close call (51-59%)

| Headline | Trigger condition |
|----------|-------------------|
| `THE PERFECT BLEND` | winnerPct <= 55 |
| `BEST OF BOTH` | winnerPct <= 58 |
| `50/50? NOT QUITE...` | winnerPct = 51 or 52 |
| `A LITTLE BIT MUM, A LITTLE BIT DAD` | winnerPct <= 55 |
| `THE GREAT DEBATE` | winnerPct <= 59 |

#### Feature-specific headlines (secondary line, below hero)

| Headline | Trigger |
|----------|---------|
| `GOT MUM'S EYES` | heroFeature = eyes, winner = Mum |
| `DAD'S SMILE, THROUGH AND THROUGH` | heroFeature = smile, winner = Dad |
| `THAT NOSE? 100% MUM` | heroFeature = nose, winner = Mum |
| `HAIR BY DAD` | heroFeature = hair, winner = Dad |
| `MUM'S FACE SHAPE, DAD'S EVERYTHING ELSE` | winner = Dad but face_shape = Mum |
| `THOSE BROWS CAME FROM DAD` | heroFeature = eyebrows, winner = Dad |

#### Occasion-specific overlays (replaces occasion header, keeps data headline)

| Occasion | Header text | Character variant |
|----------|-------------|-------------------|
| Mother's Day | `HAPPY MOTHER'S DAY` | Mama Bear holding flowers |
| Father's Day | `HAPPY FATHER'S DAY` | Papa Bear with "World's Best Dad" mug |
| Birthday | `HAPPY BIRTHDAY {NAME}` | Little Cub/Mini Me with party hat |
| Christmas | `MERRY CHRISTMAS` | All characters in Santa hats |
| Valentine's Day | `TO MY VALENTINE` | Mama Bear + Papa Bear together (pairwise mode) |
| Grandparent's Day | `BEST GRAN/GRAMPS EVER` | Gran/Gramps character with grandchild |

### 3.3 Headline selection algorithm

```
1. Determine winner + winnerPct from analysis data
2. Pick hero headline from winner + pct bracket (randomised from pool to avoid repetition)
3. Pick feature sub-headline from heroFeature + winner
4. If occasion is set, prepend occasion header above hero headline
5. Truncate any headline > 35 chars (should not happen with this system)
```

---

## 4. SKU Matrix — Auto-Generated Variations

The Character Mug line generates variations **automatically** from existing analysis data. No manual design per SKU.

### 4.1 Variable axes

| Axis | Values | Source |
|------|--------|--------|
| **Winner** | Mum, Dad, Blend | `data.winner` / `data.winnerLabel` |
| **Percentage bracket** | High (70-100%), Medium (60-69%), Close (51-59%) | `data.winnerPct` |
| **Hero feature** | eyes, eyebrows, smile, nose, face_shape, skin, hair, ears | First feature from `data.featureVotes` matching winner |
| **Occasion** | generic, mothers_day, fathers_day, birthday, christmas, valentines, grandparents_day | User-selected or seasonal auto-suggest |
| **Character** | Mama Bear, Papa Bear, Little Cub, Mini Me, Gran/Gramps | Auto-selected from winner + child age + occasion |
| **Cultural theme** | default, heritage_gold, carnival_spirit, ubuntu | From existing `mugThemes.js` palette system |

### 4.2 Effective SKU count

```
Winners (3) x Pct brackets (3) x Occasions (7) x Cultural themes (4) = 252 visual variants
```

All from **one template** with parameterised rendering. Zero per-SKU design cost.

Cornish Prints must design each SKU individually. We generate 252+ unique, personalised designs from a single codebase.

### 4.3 Template registry entry (planned)

```js
// New entry in templateRegistry.js
character_mug: {
  styles: ["character_default", "character_heritage", "character_carnival", "character_ubuntu"],
  defaultStyle: "character_default",
  renderWidth: 830,
  renderHeight: 345,
  supportsCustomMessage: true,
  components: {
    character_default: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
    character_heritage: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
    character_carnival: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
    character_ubuntu: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
  },
},
```

### 4.4 Print profile entry (planned)

```js
// New entry in printProfiles.js — same physical product as mug_wrap
[PRODUCT_TYPES.CHARACTER_MUG]: {
  id: "character_mug",
  label: "Character Mug (11oz)",
  icon: "cartoon bear face",
  price: 16.99,  // £2 premium over standard mug (£14.99)
  width_mm: 228.6,
  height_mm: 94.8,
  width_px: 2670,
  height_px: 1110,
  prodigi_sku: "GLOBAL-MUG-W",  // same physical product
  vendors: [{ name: "prodigi", sku: "GLOBAL-MUG-W", priority: 1 }],
  description: "11oz ceramic mug with illustrated character design + personalised analysis",
},
```

---

## 5. Visual Direction

### 5.1 Layout — 2670 x 1110px Prodigi canvas

The Character Mug uses the same 3-panel structure as `MugWrapTemplate.jsx` but with a fundamentally different visual hierarchy:

```
┌───────────────────┬──────────────────────────────────┬───────────────────┐
│                   │                                  │                   │
│   LEFT PANEL      │        CENTRE PANEL              │   RIGHT PANEL     │
│   694px (26%)     │        1282px (48%)              │   694px (26%)     │
│                   │                                  │                   │
│   CHARACTER        │   HERO HEADLINE (bold, caps)     │   FEATURE         │
│   ILLUSTRATION    │   + Feature sub-headline         │   BREAKDOWN       │
│   (full height)   │   + Child PHOTO (circle, large)  │   (chips + icons) │
│                   │   + Score badge                  │   + Occasion art  │
│   Mama/Papa Bear  │   + Brand mark                   │   + Brand         │
│   reacting to     │                                  │                   │
│   the result      │   THIS IS WHAT YOU SEE           │                   │
│                   │   FACE-ON                        │                   │
│                   │                                  │                   │
└───────────────────┴──────────────────────────────────┴───────────────────┘
```

### 5.2 Centre panel hierarchy (what the customer sees face-on)

1. **Occasion header** (if applicable) — small, caps, tracking wide — top
2. **Hero headline** — LARGEST element, bold rounded sans, all-caps, 2 lines max
3. **Child photo** — 100px circle (larger than current 80px), thick accent border
4. **Feature sub-headline** — "Got Mum's Eyes" in pill badge
5. **Score badge** — "72% Mum" in bold gradient pill
6. **Brand mark** — "famililook.com" very small, muted

Key difference from current `MugWrapTemplate`: the headline is the HERO, not the photo. The headline is what makes someone stop scrolling on TikTok. The photo provides the personal connection.

### 5.3 Left panel — Character illustration

- Full-height character illustration (Mama Bear, Papa Bear, etc.)
- Character is **reacting** to the result (proud pose for high %, surprised for close call)
- Speech bubble or thought bubble with a short quip: "Told you so!" / "It's obvious!" / "Hmm, barely..."
- Character coloured in the active theme palette (not fixed colours)

### 5.4 Right panel — Feature breakdown + decorative

- Feature chips (same system as current template, from `mugThemes.js`)
- Small character detail (e.g., Little Cub sleeping if right panel is the "quiet" side)
- Decorative confetti/stars pattern in theme colours at low opacity
- "Analysed by FamiliLook AI" footer

### 5.5 Colour palette

Character Mugs inherit the existing `OCCASION_THEMES` from `mugThemes.js` plus cultural themes:

| Theme | Primary | Light | Wash | Use case |
|-------|---------|-------|------|----------|
| Default (generic) | #C0364E | #E8637A | #FDF0F2 | Standard — no occasion |
| Mother's Day | #C0364E | #FF6B9D | #FCEEF2 | May gifting |
| Father's Day | #1A6BB5 | #6BA3D4 | #EEF3FB | June gifting |
| Birthday | #D97706 | #F59E0B | #FEF3C7 | Year-round |
| Heritage Gold | #C8960C | #E8C84A | #FFF8E1 | Kente-inspired |
| Carnival Spirit | #FF6D00 | #FFB74D | #FFF3E0 | Caribbean celebration |
| Ubuntu | #D84315 | #FF8A65 | #FBE9E7 | Pan-African warmth |

**NEW addition for Character Mugs:**

| Theme | Primary | Light | Wash | Use case |
|-------|---------|-------|------|----------|
| Christmas | #B71C1C | #EF5350 | #FFEBEE | December gifting |
| Valentine's | #AD1457 | #EC407A | #FCE4EC | February — pairwise mode |

### 5.6 Design principles

1. **Bold over subtle** — if text isn't readable at arm's length on a mug, it's too small
2. **Headline first** — the one-liner is the hero, not the data
3. **White space is OK** — transparent background = white ceramic shows through; embrace it
4. **Characters frame, photos anchor** — the cartoon character adds personality; the real photo adds identity
5. **Every mug is a social post** — design as if the customer will photograph it and post it

---

## 6. TikTok / Social Strategy

### 6.1 Content formats

| Format | Description | Hook | Frequency |
|--------|-------------|------|-----------|
| **Reveal video** | Show analysis running, then cut to the mug arriving. Customer opens box. | "We analysed who the baby looks like... then put it on a mug" | 3x/week |
| **Before/After** | Split screen: clinical data view vs Character Mug view | "Same data, completely different vibe" | 1x/week |
| **Gift reaction** | Film grandparent/parent opening the mug as a gift | "My mum's face when she saw the mug..." | UGC, ongoing |
| **Side-by-side** | Baby photo next to the Character Mug illustration | "The resemblance is uncanny... even the cartoon knows" | 2x/week |
| **Trend jack** | Use trending audio with mug reveal | Adapt to whatever is trending | Opportunistic |
| **Process video** | Screen recording of the analysis + mug customisation flow | "How to turn your baby's face into a keepsake in 60 seconds" | 1x/week |
| **Comparison** | Our personalised mug vs a generic mug from another brand | "One is made just for your family. The other is the same for everyone." | 1x/month |

### 6.2 Hooks (first 3 seconds)

- "We used AI to figure out who the baby looks like... then put it on a mug"
- "Sorry Dad, the mug says it's 78% Mum"
- "This mug just ended the 'who does the baby look like' argument"
- "POV: You got Grandma a mug that says exactly which features she passed down"
- "The mug that settles it once and for all"
- "My family thought I was joking until the mug arrived"

### 6.3 Hashtag strategy

**Primary (always use):**
- #FamiliLook
- #CharacterMugs
- #WhoDoTheyLookLike
- #PersonalisedMug

**Reach (rotate):**
- #BabyLooksLike
- #MumsOfTikTok
- #DadsOfTikTok
- #GiftIdeas
- #PersonalisedGifts
- #NewMum
- #NewDad
- #BabyReveal
- #FamilyResemblance

**Seasonal:**
- #MothersDay #MumGift (May)
- #FathersDay #DadGift (June)
- #ChristmasGifts #StockingFiller (Nov-Dec)
- #BirthdayGift (year-round)

### 6.4 UGC strategy

1. **Include a card in every mug box**: "Love your mug? Film an unboxing and tag @famililook for a chance to win a free Family Mug Set!"
2. **Incentive**: Monthly draw — best UGC video wins a free keepsake bundle (cost: ~£30, value: priceless social proof)
3. **Repost permission**: Card includes opt-in text: "By tagging us, you give us permission to repost" (GDPR-compliant, no real child faces in our reposts — we blur/crop to show the mug, not the child)
4. **Creator seeding**: Send free Character Mugs to 20 parenting micro-influencers (5k-50k followers) with a brief: "Film yourself opening the mug. That's it."

### 6.5 TikTok Shop integration

- List Character Mugs on TikTok Shop (when available in UK)
- Use "Shop Here" / "Buy Now" overlays on all product videos
- Social proof overlays on organic posts: "847 families have ordered" (real number, updated weekly)
- Pin a "How to order" video to profile

### 6.6 Platform priority

| Platform | Priority | Content type | Posting cadence |
|----------|----------|-------------|-----------------|
| TikTok | Highest | Short-form video, TikTok Shop | 5x/week |
| Instagram Reels | High | Repurposed TikTok content | 4x/week |
| Instagram Stories | Medium | Behind-the-scenes, polls ("Mum or Dad?") | Daily |
| Facebook | Medium | Gift-focused posts, parent groups | 3x/week |
| Pinterest | Low (long-tail) | Product pins, gift guide boards | 2x/week |

---

## 7. Competitive Moat

### Why Cornish Prints cannot copy this

| Advantage | Explanation |
|-----------|-------------|
| **Data-driven personalisation** | Every mug is unique — generated from real AI face analysis. Cornish Prints would need to build an entire ML pipeline. |
| **252+ auto-generated variants** | One template produces hundreds of unique designs. Cornish Prints designs each SKU manually. |
| **Photo integration** | Real family photos on the mug alongside illustrated characters. Generic brands cannot do this without a personalisation platform. |
| **Feature-specific headlines** | "Got Mum's Eyes" is not a generic tagline — it's computed from the analysis. Cannot be faked at scale. |
| **Percentage accuracy** | "78% Mum" is a real, reproducible result. Customers trust it because they saw the analysis happen. |
| **Network effects** | Every mug is a potential social post. Every social post drives new analyses. New analyses drive new mug orders. Cornish Prints has no flywheel — they sell mugs, full stop. |
| **Occasion engine** | We auto-suggest the right mug at the right time (Mother's Day prompt in April, Father's Day in May). Cornish Prints relies on seasonal browsing. |
| **Cultural themes** | Heritage Gold, Carnival Spirit, Ubuntu — culturally resonant palettes that no generic brand offers. |

### What Cornish Prints does better (and what we learn from them)

| Their strength | Our response |
|----------------|-------------|
| Bold, instantly readable typography | Character Mugs adopt bold rounded sans-serif headlines |
| Simple, repeatable character system | FamiliLook Family characters (5 core, SVG, theme-colourable) |
| Cheeky, relatable humour | Data-driven one-liners that are funny AND personal |
| TikTok-native content | Dedicated TikTok content calendar, UGC strategy, Shop integration |
| Low price point (~£10-12) | We price at £16.99 (justified by personalisation premium) |

---

## 8. Pricing & Positioning

### 8.1 Price ladder

| Product | Price | Positioning |
|---------|-------|-------------|
| Standard Mug (`mug_wrap`) | £14.99 | Data-forward, clean design. For parents who want the full analysis on ceramic. |
| **Character Mug (NEW)** | **£16.99** | Bold, illustrated, gift-ready. For gift buyers and social sharers. |
| Family Mug Set (`family_mug_set`) | £27.99 | Mum & Dad matching pair with all children. Premium family gift. |
| **Character Family Set (FUTURE)** | **£32.99** | Character-illustrated matching pair. Top-tier gift. |

### 8.2 Pricing rationale

- **£2 premium** over standard mug justified by: illustrated characters (perceived higher design value), bold typography (more "giftable"), and social shareability
- **Below £20** keeps it impulse-purchase territory for gift buyers
- **Prodigi COGS unchanged** — same `GLOBAL-MUG-W` SKU, same fulfilment cost. The £2 premium is pure margin.
- **Cornish Prints pricing** is £10-14 for a generic mug. Our £16.99 is justified by personalisation — customers pay more for "made for YOUR family" vs "made for everyone"

### 8.3 Bundling opportunities

| Bundle | Contents | Price | Saving |
|--------|----------|-------|--------|
| Character Mug + Greeting Card | 1 Character Mug + 1 matching greeting card | £19.99 | £3.99 saved |
| Character Mug + Fine Art Print | 1 Character Mug + A4 certificate print | £27.99 | £5.99 saved |
| The Full Character Set | 2 Character Mugs (Mum + Dad) + 1 greeting card | £29.99 | £10.98 saved |

---

## 9. Brand Guardrails

### MUST do

- Use "AI-powered face analysis" or "for entertainment purposes" disclaimer on all marketing materials
- Keep characters warm, playful, family-friendly
- Ensure all headlines are positive/celebratory — even "Sorry Dad" is affectionate, not mean
- Use real analysis data to drive headlines (never fabricate percentages or features)
- Maintain "famililook.com" brand mark on all mugs
- Respect Prodigi print constraints (2670x1110px, transparent PNG, safe zones)
- Follow existing `mugThemes.js` colour token system for consistency

### MUST NOT do

- Make health claims ("Our AI detects genetic traits") — we analyse visual resemblance, not DNA
- Make DNA or ancestry claims of any kind
- Target children under 13 with advertising (COPPA/ICO compliance)
- Use real user photos in marketing materials without explicit written consent
- Show real children's faces in TikTok ads or social posts (use the illustrated characters instead)
- Use language that implies the analysis is scientifically or medically accurate
- Create headlines that are mean-spirited, exclusionary, or could cause family conflict
- Use "50/50" — the system always nudges to show a winner (per BE/FE contract: no 50/50 rule)
- Promote to single-parent families in a way that implies incompleteness
- Reference FamiliPoker (parked product — do not promote)

### Tone of voice examples

| Good | Bad |
|------|-----|
| "Turns out, you're 78% Mum!" | "DNA analysis confirms maternal dominance" |
| "Sorry Dad, this one's all Mum" | "Father's genetic contribution is minimal" |
| "The AI-powered family fun keepsake" | "Scientifically accurate face analysis" |
| "Who do they look like? Now you know!" | "Our algorithm determines parental inheritance" |

---

## 10. Success KPIs

### Launch phase (Weeks 1-4)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Character Mug orders | 100 in first 30 days | Prodigi order count |
| Conversion rate (analysis to Character Mug purchase) | 3% | Analytics: `mug_character_ordered` / `analysis_completed` |
| Average order value | £18+ (with upsells) | Stripe/payment data |
| TikTok video views (organic) | 50,000 total across all Character Mug content | TikTok analytics |
| UGC submissions | 10 tagged videos/photos | Social monitoring |

### Growth phase (Months 2-6)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Character Mug share of total mug revenue | 40%+ | Revenue split: character vs standard |
| TikTok follower growth | +2,000/month | TikTok analytics |
| Social proof (total orders displayed) | 500+ | Running count |
| Repeat purchase rate | 15% (same customer orders 2+ mugs) | Customer cohort analysis |
| Cost per acquisition (paid social) | < £5 | Ad spend / conversions |
| ROAS (paid social) | > 3:1 | Revenue / ad spend |
| Seasonal spike (Mother's/Father's Day) | 3x average weekly orders | Order volume comparison |

### North star metric

**Viral coefficient**: For every Character Mug sold, how many new analyses does the resulting social share generate?

Target: **0.3** (every 10 mugs sold generates 3 new analyses from social sharing). This creates the flywheel that no generic mug brand can replicate.

---

## 11. Implementation Roadmap (Suggested)

| Phase | Scope | Timeline | Dependencies |
|-------|-------|----------|-------------|
| **Phase 1: Character design** | Commission 5 SVG character illustrations (Mama Bear, Papa Bear, Little Cub, Mini Me, Gran/Gramps) with 4-5 emotion variants each | 2 weeks | Visual Director agent to produce illustration briefs; external illustrator or AI generation |
| **Phase 2: Headline engine** | Build headline selection algorithm + full copy bank (50+ headlines) | 1 week | Copywriter agent; this brief as input |
| **Phase 3: Template build** | `CharacterMugTemplate.jsx` — new template following `MugWrapTemplate.jsx` patterns, registered in `templateRegistry.js` and `printProfiles.js` | 2 weeks | Phase 1 + 2 complete; CTO/engineering sign-off |
| **Phase 4: Preview component** | Character Mug preview in `MugCeramicPreview.jsx` or new preview component | 1 week | Phase 3 complete |
| **Phase 5: Content sprint** | 20 TikTok videos, 10 Instagram posts, UGC box insert designed | 2 weeks | Phase 3 complete; Social Media Manager + Copywriter agents |
| **Phase 6: Launch** | Soft launch to existing users, paid social ramp | 1 week | All phases complete; CEO approval |

**Target launch: May 2026** (ahead of Father's Day peak)

---

## 12. Approvals Required

| Approver | What they approve | Status |
|----------|-------------------|--------|
| **CEO** | Pricing (£16.99), new product line go/no-go, budget allocation | PENDING |
| **CTO** | Template architecture, `templateRegistry` changes, Prodigi integration | PENDING |
| **COO** | Fulfilment capacity for projected volumes, box insert logistics | PENDING |
| **Change Manager** | Registered in change system before any code changes | PENDING |
| **Compliance** | Headline copy bank reviewed for claim accuracy | PENDING |

---

## Appendix A: Headline Copy Bank (Full Draft)

### High-Mum headlines (winnerPct >= 60, winner = Mum)
1. MUMMY'S MINI ME
2. SORRY DAD, I'M ALL MUM
3. MUM DID ALL THE WORK
4. COPY + PASTE: MUM EDITION
5. LIKE MOTHER, LIKE BABY
6. MUM'S GREATEST HIT
7. HAVE YOU SEEN MY MUM? APPARENTLY I AM HER
8. MUM'S TWIN, DAD'S FRIEND
9. MADE BY MUM
10. MUM CALLED, SHE WANTS HER FACE BACK

### High-Dad headlines (winnerPct >= 60, winner = Dad)
1. DADDY'S DOUBLE
2. SORRY MUM, THIS ONE'S ALL DAD
3. DAD'S CTRL+C, CTRL+V
4. THE APPLE DOESN'T FALL FAR
5. STRONG GENES, DAD
6. DAD'S GREATEST HIT
7. HAVE YOU SEEN MY DAD? I AM BASICALLY HIM
8. DAD'S TWIN, MUM'S MATE
9. MADE BY DAD
10. DAD CALLED, HE WANTS HIS FACE BACK

### Close-call headlines (winnerPct 51-59)
1. THE PERFECT BLEND
2. BEST OF BOTH
3. 50/50? NOT QUITE...
4. A LITTLE BIT MUM, A LITTLE BIT DAD
5. THE GREAT DEBATE
6. TEAMWORK MAKES THE DREAM WORK
7. YOU BOTH DID GOOD
8. THE VERDICT IS IN... JUST BARELY

### Feature-specific sub-headlines
1. GOT MUM'S EYES (AND THEY KNOW IT)
2. DAD'S SMILE, THROUGH AND THROUGH
3. THAT NOSE? 100% MUM
4. HAIR BY DAD
5. MUM'S FACE SHAPE, NO QUESTION
6. THOSE BROWS? ALL DAD
7. EARS: A GIFT FROM MUM
8. SKIN TONE: DAD'S CONTRIBUTION

---

*This brief was produced by the CMO agent. No code files were modified. All implementation requires CEO approval and CTO sign-off before proceeding.*

*Next action: CEO review and approval, then dispatch to Visual Director agent for character illustration brief.*
