# Phase B: Occasion-Led Homepage — Agent Implementation Brief

> **Author**: CEO (strategic spec) + CPO (implementation)
> **Date**: 2026-04-02
> **Priority**: P0 — Revenue-critical
> **Status**: APPROVED — build this
> **Reference**: `docs/OCCASION_MAPPING_SPEC.html` (the CEO's design, this is the source of truth)

---

## What You Are Building

A new homepage component `HomePageOccasion.jsx` that shows 6 occasion cards matching the CEO's design (saved at `docs/OCCASION_MAPPING_SPEC.html`). Each card is a direct funnel into the existing upload + analysis + keepsake purchase flow, with the hero product PRE-SELECTED so the user skips the catalogue.

**No new upload flow. No new backend. No new products. No new routes (except the homepage swap).**

---

## Step 0 — Read Before Writing

Agents MUST read these files first and confirm understanding:

1. `docs/OCCASION_MAPPING_SPEC.html` — the CEO's occasion-to-product mapping (6 cards with exact copy, hero products, photo counts, AOV targets)
2. `src/theme/colors.js` — full design system (colors, spacing, radius, typography, shadows)
3. `src/styles/mobile.css` — CSS custom properties (--nav-height, --bottom-clearance, z-index layers)
4. `src/pages/HomePage.jsx` — current homepage (DO NOT MODIFY — archive, flag-gate)
5. `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` — needs `initialProduct` prop
6. `src/components/keepsakes/OrderModal.jsx` — already has `selectedProductType` prop (skip catalogue)

---

## Mobile-First Dimensions (NON-NEGOTIABLE)

This is a mobile app. All dimensions MUST work on these devices:

| Device | Width | Test Priority |
|--------|-------|--------------|
| iPhone SE | 375px | PRIMARY — smallest target |
| iPhone 14 | 390px | PRIMARY |
| Samsung S22 | 412px | PRIMARY |
| iPhone 14 Pro Max | 430px | SECONDARY |
| Desktop | 1024px+ | Cards in 2-column grid |

**Layout rules:**
- Cards stack vertically on mobile (single column, full width minus 32px padding)
- 2-column grid on desktop (>700px)
- 16px gap between cards
- 16px horizontal padding (page edges)
- Card content padding: 20px
- Card border-radius: 14px (matches `radius.lg` = 16px, use 14px to match CEO spec)
- All interactive elements: 48px minimum touch height
- Bottom clearance: `var(--bottom-clearance)` to clear bottom nav + FAB
- No horizontal scroll anywhere

---

## Design System — Dark Theme Adaptation

The CEO's spec uses a light theme (white cards on #F7F5F0). Adapt to FamiliLook's dark theme:

| CEO Spec | Dark Theme |
|----------|------------|
| `--bg: #F7F5F0` | `colors.bgMain (#0D0F1A)` |
| `--surface: #FFFFFF` | `colors.bgElevated (#1E2235)` |
| `--border: #E4E0D8` | `colors.borderMedium (rgba(255,255,255,0.10))` |
| `--text-primary: #1A1814` | `colors.textPrimary (#E8EAF6)` |
| `--text-secondary: #6B6760` | `colors.textSecondary (#B8BDD6)` |
| `--text-tertiary: #9E9B96` | `colors.textMuted (#8B92A8)` |

**Tag badge colours — KEEP the CEO's colours**, they provide visual differentiation on dark:

| Tag | Background | Text |
|-----|-----------|------|
| Gift giving (violet) | `rgba(91,63,212,0.15)` | `#A78BFA` |
| Family activity (teal) | `rgba(26,122,94,0.15)` | `#34D399` |
| Game night (amber) | `rgba(176,92,16,0.15)` | `#FBBF24` |
| New arrival (coral) | `rgba(194,59,59,0.15)` | `#F87171` |
| Milestone (blue) | `rgba(43,95,166,0.15)` | `#60A5FA` |
| Viral hook (purple) | `rgba(123,63,168,0.15)` | `#C084FC` |

**Typography:** Use system font stack from mobile.css (not Syne/DM Sans — those aren't loaded in the app).

---

## The 6 Occasion Cards — Exact Content

Copy and structure from CEO's `docs/OCCASION_MAPPING_SPEC.html`:

### Card 1: Father's / Mother's Day
- **Tag**: Gift giving (violet)
- **Title**: Father's / Mother's Day
- **Description**: Lead with the mug. "Show your dad his bond with you, printed on something he'll use every morning." Secondary: framed canvas, greeting card.
- **Hero product**: Ceramic mug
- **Photos needed**: 2 (parent + child)
- **AOV potential**: £14–28
- **CTA**: "Make this gift →"
- **On tap**: → `/app?intent=child&product=mug_wrap`

### Card 2: Holiday / vacation
- **Tag**: Family activity (teal)
- **Title**: Holiday / vacation
- **Description**: "Pack something the whole family made together." Uno deck with everyone's face on the cards. Puzzle. Card deck. Sells the activity, not the print.
- **Hero product**: Uno / card deck
- **Photos needed**: 3–6 (family)
- **AOV potential**: £25–50
- **CTA**: "Make your deck →"
- **On tap**: → `/app?intent=group&product=card_deck`

### Card 3: Family poker / games
- **Tag**: Game night (amber)
- **Title**: Family poker / games
- **Description**: "Play poker with your family, with your family on the cards." FamiliPoker crossover. Strongest social sharing hook — people post this.
- **Hero product**: Poker / playing cards
- **Photos needed**: 2–8
- **AOV potential**: £10–25
- **CTA**: "Start game night →"
- **On tap**: → `/app?intent=self&product=card_deck` (or route to FamiliPoker if cross-app)

### Card 4: New baby / birth
- **Tag**: New arrival (coral)
- **Title**: New baby / birth
- **Description**: "Who does the baby look like?" is the natural first question every family asks. This is FamiliLook's strongest emotional hook — lead with it as an occasion.
- **Hero product**: Keepsake print / card
- **Photos needed**: 2–3
- **AOV potential**: £7–25
- **CTA**: "Discover your bond →"
- **On tap**: → `/app?intent=child&product=fine_art_print`

### Card 5: Birthday / graduation
- **Tag**: Milestone (blue)
- **Title**: Birthday / graduation
- **Description**: "A gift that shows exactly where they came from." Cushion, framed canvas, mug set. Higher spend occasions — don't undersell with low entry price.
- **Hero product**: Canvas / cushion / mug set
- **Photos needed**: 2–4
- **AOV potential**: £28–40
- **CTA**: "Create their gift →"
- **On tap**: → `/app?intent=child&product=cushion`

### Card 6: Just curious — the free play (FEATURED)
- **Tag**: Viral hook (purple)
- **Title**: Just curious — the free play
- **Description**: Keep the free "see your bond" result as the top of funnel. But the moment they see the score, serve the occasion cards directly: "Turn this into something real."
- **Featured card** — violet border (`colors.accentPrimary`), slightly different background
- **Meta**: Role: Acquisition | Converts to: Any product | Change needed: Results page CTA
- **CTA**: "Try it free →"
- **On tap**: → `/app?intent=self` (no product pre-select — free discovery path)

---

## Card Layout — Mobile (375px–430px)

```
┌─ Card (width: 100%, padding: 20px, border-radius: 14px) ───────┐
│                                                                   │
│  ┌─ Tag badge (inline-block, padding: 4px 10px, radius: 20px) ─┐│
│  │ Gift giving                                                   ││
│  └───────────────────────────────────────────────────────────────┘│
│                                                                   │
│  Father's / Mother's Day           ← title: 18px / 700          │
│                                                                   │
│  Lead with the mug. "Show your     ← desc: 13.5px / 300         │
│  dad his bond with you..."         ← color: textSecondary       │
│                                                                   │
│  ─────────────────────────────     ← divider: borderMedium      │
│                                                                   │
│  Hero product    Photos needed     ← meta labels: 11px / muted  │
│  Ceramic mug     2 (parent+child)  ← meta values: 13px / 600    │
│                                                                   │
│  AOV potential                                                    │
│  £14–28                                                           │
│                                                                   │
│  ┌─ CTA button (full width, 48px height, violet gradient) ─────┐│
│  │              Make this gift →                                 ││
│  └───────────────────────────────────────────────────────────────┘│
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Product Pre-Select Flow

When user taps a card with a `product` param:

1. URL becomes `/app?intent=child&product=mug_wrap`
2. Existing `UploadSection.jsx` reads intent as normal
3. **NEW**: `product` query param stored in state (e.g. `occasionProduct`)
4. Upload + analysis runs normally
5. When analysis completes and results render:
   - If `occasionProduct` is set → auto-open keepsake flow with that product
   - Desktop: `<OrderModal selectedProductType={occasionProduct} />`
   - Mobile: `<KeepsakeMobileFlow initialProduct={occasionProduct} />` (**NEW PROP**)
6. User lands directly on Customise screen (skip catalogue)
7. Customise → Preview → Basket → Stripe

### KeepsakeMobileFlow Change Required

Add `initialProduct` prop:

```jsx
function KeepsakeMobileFlowInner({
  onClose,
  childIndex,
  petIndex,
  pairwiseLink,
  personAPhoto,
  personBPhoto,
  onCardGenerated,
  initialProduct,        // NEW — pre-selected product ID (skips catalogue)
}) {
  const [screen, setScreen] = useState(initialProduct ? "customise" : "catalogue");
  const [selectedProduct, setSelectedProduct] = useState(initialProduct || null);
```

That's the only change to the keepsake flow.

---

## File Plan

| File | Action | Description |
|------|--------|-------------|
| `src/pages/HomePageOccasion.jsx` | **NEW** | 6 occasion cards, dark theme, mobile-first |
| `src/pages/HomePage.jsx` | **NO CHANGE** | Archived, rendered when flag OFF |
| `src/App.jsx` or `src/AppRouter.jsx` | **MODIFY** | Flag gate: `VITE_PRODUCT_LED_HOMEPAGE ? HomePageOccasion : HomePage` |
| `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` | **MODIFY** | Add `initialProduct` prop (2 lines changed) |
| `src/layout/MobileResultsSection.jsx` | **MODIFY** | Read `product` from URL, pass to keepsake flow |
| `tests/pages/HomePageOccasion.test.jsx` | **NEW** | 6 cards render, CTAs link correctly, mobile responsive |
| `tests/keepsakes/initialProduct.test.jsx` | **NEW** | KeepsakeMobileFlow skips catalogue when initialProduct set |

---

## Feature Flag

`VITE_PRODUCT_LED_HOMEPAGE` — when `"true"`, homepage renders `HomePageOccasion`. When absent/false, renders existing `HomePage`.

---

## Agent Assignments

| Step | Agent | Task | Gate |
|------|-------|------|------|
| 0 | qa_lead | Baseline tests for HomePage rendering + KeepsakeMobileFlow catalogue start | BLOCKS all feature work |
| 1 | fe_lead | Create `HomePageOccasion.jsx` — 6 cards from OCCASION_MAPPING_SPEC.html, dark theme, mobile-first | Step 0 |
| 2 | fe_lead | Add `initialProduct` prop to `KeepsakeMobileFlow.jsx` (2 lines) | Step 0 |
| 3 | fe_lead | Wire product pre-select: URL param → state → keepsake flow auto-open | Steps 1-2 |
| 4 | fe_lead | Flag-gate homepage in AppRouter.jsx | Step 1 |
| 5 | qa_lead | Feature tests: 6 cards render, CTAs correct, mobile dimensions, flag isolation, initialProduct skip | Steps 1-4 |
| 6 | qa_lead | Full test suite + build verification | Step 5 |

---

## Acceptance Criteria

- [ ] 6 occasion cards render on mobile (375px) without horizontal scroll
- [ ] Each card shows: tag badge, title, description, meta (hero product, photos, AOV), CTA button
- [ ] Card 6 ("Just curious") has featured styling (violet border)
- [ ] Tapping each card navigates to `/app` with correct `intent` + `product` params
- [ ] After analysis, keepsake flow opens with pre-selected product (skip catalogue)
- [ ] Mobile: KeepsakeMobileFlow starts at "customise" when `initialProduct` set
- [ ] Desktop: OrderModal starts at step 2 when `selectedProductType` set
- [ ] "Just curious" card (no product param) → normal results → OccasionShelf (already deployed)
- [ ] Flag OFF = existing HomePage renders identically
- [ ] 48px minimum touch targets on all CTAs
- [ ] Bottom clearance for nav bar (var(--bottom-clearance))
- [ ] No new npm packages
- [ ] All existing tests pass + new tests pass
- [ ] Build succeeds, bundle within 50KB of current

---

## YouVersion / Cornish Prints Standards

- Cards should feel like YouVersion plan cards — clean, elevated, one action each
- Product references should feel premium (Cornish Prints quality), not novelty
- Information hierarchy: occasion name → emotional hook → product → price → CTA
- Progressive disclosure: 6 cards visible, detail on tap
- Smooth transitions, native feel, no web-app jank
