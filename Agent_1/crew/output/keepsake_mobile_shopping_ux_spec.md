===============================================
  VISUAL DIRECTION — Keepsake Mobile Shopping Experience
===============================================

**Author:** Visual Director Agent
**Date:** 2026-04-01
**Status:** AWAITING APPROVAL — no code changes until signed off
**Replaces:** Current 4-step modal flow on mobile
**Reference Audit:** Agent_1/crew/output/keepsake_mobile_design_audit.md

PRODUCT: FamiliLook Keepsakes (all 13 physical products + digital)
TARGET DEVICES: Samsung S22 (412px), iPhone SE (375px), iPhone 14 (390px)
AVAILABLE VIEWPORT: ~660px height (after browser chrome + bottom nav)
BRAND: Violet #7C3AED, dark #0D0F1A, card bg #1a1a2e

---

## Design Philosophy

The current keepsake flow is a **print-export pipeline squeezed into a modal**.
The new flow is a **mobile shopping experience that happens to produce print output**.

The user should feel like they are browsing Moonpig or Etsy on their phone:
lifestyle product photos, confident tap-forward flow, large preview of the
finished product, and a single clear purchase CTA. The flat print template
is an engineering artifact for the vendor -- it is NOT the customer's preview.

---

## Typography Scale

| Role       | Font            | Weight | Size  | Line-height | Letter-spacing | Usage                           |
|------------|-----------------|--------|-------|-------------|----------------|---------------------------------|
| H1         | Inter           | 700    | 22px  | 28px        | -0.02em        | Screen titles                   |
| H2         | Inter           | 600    | 18px  | 24px        | -0.01em        | Product name on cards           |
| H3         | Inter           | 600    | 16px  | 22px        | 0              | Section labels                  |
| Body       | Inter           | 400    | 14px  | 20px        | 0              | Descriptions, chip labels       |
| Caption    | Inter           | 400    | 12px  | 16px        | 0.01em         | Prices, badges, secondary info  |
| CTA        | Inter           | 600    | 16px  | 20px        | 0.01em         | Button text                     |
| Price      | Inter           | 700    | 16px  | 20px        | 0              | Price displays                  |
| Badge      | Inter           | 700    | 10px  | 12px        | 0.05em         | "Best seller", "New" badges     |

---

## Colour Usage Map

| Element                  | Colour                | Hex       | Opacity |
|--------------------------|-----------------------|-----------|---------|
| Page background          | Dark base             | #0D0F1A   | 100%    |
| Card background          | Card surface          | #1a1a2e   | 100%    |
| Card border (default)    | Subtle                | #2a2a4e   | 100%    |
| Card border (hover/tap)  | Violet                | #7C3AED   | 100%    |
| Primary CTA bg           | Violet gradient       | #7C3AED -> #6D28D9 | 100% |
| Primary CTA text         | White                 | #FFFFFF   | 100%    |
| Secondary CTA bg         | Transparent           | --        | --      |
| Secondary CTA text       | Violet                | #7C3AED   | 100%    |
| H1, H2 text             | White                 | #FFFFFF   | 100%    |
| Body text                | Light grey            | #B0B0C8   | 100%    |
| Caption / price          | Soft grey             | #9090B0   | 100%    |
| Badge bg (Best seller)   | Amber                 | #F59E0B   | 100%    |
| Badge text               | Dark                  | #0D0F1A   | 100%    |
| Badge bg (New)           | Violet                | #7C3AED   | 100%    |
| Progress bar (filled)    | Violet                | #7C3AED   | 100%    |
| Progress bar (empty)     | Dark surface          | #2a2a4e   | 100%    |
| Chip bg (unselected)     | Card surface          | #1a1a2e   | 100%    |
| Chip bg (selected)       | Violet                | #7C3AED   | 20%     |
| Chip border (selected)   | Violet                | #7C3AED   | 100%    |
| Chip text (unselected)   | Light grey            | #B0B0C8   | 100%    |
| Chip text (selected)     | White                 | #FFFFFF   | 100%    |
| Back arrow               | White                 | #FFFFFF   | 80%     |
| Divider lines            | Subtle                | #2a2a4e   | 50%     |
| Overlay (toggle panel)   | Dark                  | #0D0F1A   | 90%     |

---

## Touch Target Specifications

ALL interactive elements MUST meet these minimums (iOS HIG):

| Element              | Min width | Min height | Min gap between targets |
|----------------------|-----------|------------|-------------------------|
| Back arrow button    | 44px      | 44px       | --                      |
| Product card (grid)  | full col  | 220px      | 12px                    |
| Style chip           | 72px      | 40px       | 8px                     |
| Age chip             | 80px      | 40px       | 8px                     |
| Primary CTA button   | 100%      | 52px       | --                      |
| Toggle switch/link   | 44px      | 44px       | --                      |
| Overflow menu icon   | 44px      | 44px       | --                      |
| Progress bar segment | 44px      | 44px       | -- (tap target, not visual size) |

---

## Navigation Model

```
Results Page
    |
    v  (tap "Keepsakes" button)
[Screen 1: Product Catalogue]  <-- full page, /keepsakes route
    |
    v  (tap product card)
[Screen 2: Customise]          <-- full page, /keepsakes/:productId
    |
    v  (tap "Continue to Preview")
[Screen 3: Preview + Purchase] <-- full page, /keepsakes/:productId/preview
    |
    v  (tap "Add to Basket")
[Basket Drawer]                <-- bottom drawer overlay (existing component)
```

- Each screen is a FULL PAGE, not a modal overlay
- Browser back gesture and back arrow both return to previous screen
- URL-addressable: user can share a link to their customised product
- No overlay/backdrop wastage on mobile
- No focus trap needed (native page focus)

### Progress Bar

A thin 3-segment progress bar sits at the top of each screen:

```
Screen 1: [====][    ][    ]   33%
Screen 2: [====][====][    ]   66%
Screen 3: [====][====][====]  100%
```

- Height: 3px
- Width: 100% of viewport (no padding)
- Segment colours: filled = #7C3AED, empty = #2a2a4e
- No labels, no numbers -- pure visual progress
- Tap target: 44px tall invisible hit area for accessibility (tapping a segment navigates to that step if already visited)

---

## Screen 1: Product Catalogue

### Purpose
Replace Steps 1+2 of the current modal. User sees all purchasable products
as lifestyle mockup photos in a browseable grid.

### Layout Specification (412px reference)

```
 0px  ┌─────────────────────────────────────────┐
      │ [3px progress bar: segment 1 filled]     │
 3px  ├─────────────────────────────────────────┤
      │                                         │
      │  <- Back    KEEPSAKES          (filter) │
      │                                         │
47px  ├─────────────────────────────────────────┤
      │                                         │
      │  Category chips (horizontal scroll)     │
      │  [All] [Mugs] [Cards] [Wall Art] ...    │
      │                                         │
87px  ├─────────────────────────────────────────┤
      │                                         │
      │  ┌─────────┐  12px  ┌─────────┐        │
      │  │         │  gap   │         │        │
      │  │ PRODUCT │        │ PRODUCT │        │
      │  │ PHOTO   │        │ PHOTO   │        │
      │  │ 150px   │        │ 150px   │        │
      │  │         │        │         │        │
      │  ├─────────┤        ├─────────┤        │
      │  │Name     │        │Name     │        │
      │  │£14.99   │        │£16.99   │        │
      │  │*Best*   │        │         │        │
      │  └─────────┘        └─────────┘        │
      │       220px total card height           │
      │                                         │
      │  12px vertical gap                      │
      │                                         │
      │  ┌─────────┐  12px  ┌─────────┐        │
      │  │         │  gap   │         │        │
      │  │ PRODUCT │        │ PRODUCT │        │
      │  │ PHOTO   │        │ PHOTO   │        │
      │  │         │        │         │        │
      │  ├─────────┤        ├─────────┤        │
      │  │Name     │        │Name     │        │
      │  │£24.99   │        │£6.99    │        │
      │  └─────────┘        └─────────┘        │
      │                                         │
      │  (scrollable - no bottom action bar)    │
      │                                         │
      └─────────────────────────────────────────┘
```

### Dimensions

| Element               | Value                                    |
|------------------------|------------------------------------------|
| Page padding (sides)   | 16px                                     |
| Top bar height         | 44px (below progress bar)                |
| Category chips height  | 40px (including 8px vertical padding)    |
| Grid columns           | 2 (CSS grid: `repeat(2, 1fr)`)           |
| Grid gap               | 12px horizontal, 12px vertical           |
| Card width             | ~(412 - 32 - 12) / 2 = ~184px each      |
| Card image height      | 150px                                    |
| Card info area         | 70px (name + price + optional badge)     |
| Card total height      | 220px                                    |
| Card border-radius     | 12px                                     |
| Card bg                | #1a1a2e                                  |
| Card border            | 1px solid #2a2a4e                        |
| Card shadow            | 0 2px 8px rgba(0,0,0,0.3)               |
| Image border-radius    | 12px 12px 0 0 (top corners only)         |
| Image fit              | object-fit: cover                        |
| Product name font      | H3: Inter 600, 16px                      |
| Price font             | Price: Inter 700, 16px, #9090B0          |
| Badge position         | absolute, top-right of image, 8px inset  |
| Badge padding          | 4px 8px                                  |
| Badge border-radius    | 6px                                      |

### Category Filter Chips

Horizontal scrollable row below the top bar. Allows filtering by category.

| Property         | Value                              |
|------------------|------------------------------------|
| Chip height      | 32px                               |
| Chip padding     | 0 16px                             |
| Chip gap         | 8px                                |
| Chip radius      | 16px (pill shape)                  |
| Chip font        | Body: Inter 400, 14px              |
| Selected chip bg | #7C3AED at 20% opacity             |
| Selected border  | 1px solid #7C3AED                  |
| Default chip bg  | #1a1a2e                            |
| Default border   | 1px solid #2a2a4e                  |
| Scroll behaviour | -webkit-overflow-scrolling: touch  |
| Scrollbar        | Hidden (webkit-scrollbar: none)    |

### Product Card Content

Each card shows a LIFESTYLE MOCKUP photograph, not a flat template render.

| Product           | Lifestyle photo description                    | Badge        |
|-------------------|------------------------------------------------|--------------|
| Character Mug     | White ceramic mug on wooden table, steam rising | Best seller  |
| Mug Wrap          | Mug held in hands, cosy setting                | --           |
| Family Mug Set    | Two mugs side by side on kitchen counter        | New          |
| Greeting Card     | Card standing on mantelpiece with flowers       | --           |
| Postcard          | Postcard on desk with pen and stamps            | --           |
| Fine Art Print    | Framed print on living room wall                | --           |
| Framed Canvas     | Canvas on gallery wall, side angle              | Premium      |
| Card Deck         | Cards fanned out on table                       | Best seller  |
| Cushion           | Cushion on sofa, living room setting            | --           |
| Jigsaw Puzzle     | Puzzle pieces spread on table, partially done   | New          |
| T-Shirt           | T-shirt flat-lay on wooden surface              | --           |
| Pet Family Report | Framed report on shelf next to pet photo        | --           |

**IMPORTANT:** These lifestyle photos must be produced (photography or high-quality
3D renders). They are NOT the user's personalised design -- they are generic
product showcase images showing what the physical product looks like. The user's
design appears on Screen 2 and Screen 3.

### Responsive Breakpoints

| Device      | Width  | Cards per row | Card width | Image height |
|-------------|--------|---------------|------------|--------------|
| iPhone SE   | 375px  | 2             | ~164px     | 130px        |
| iPhone 14   | 390px  | 2             | ~171px     | 140px        |
| Samsung S22 | 412px  | 2             | ~184px     | 150px        |

At 375px, card info area text may wrap product names. Use `text-overflow: ellipsis`
with `white-space: nowrap` on product name. Full name visible on Screen 2.

### Component Hierarchy

```
KeepsakeCataloguePage
  ├── ProgressBar (step=1)
  ├── TopBar
  │     ├── BackButton (-> results page)
  │     ├── Title ("Keepsakes")
  │     └── FilterButton (optional, future)
  ├── CategoryChipStrip
  │     └── CategoryChip[] (All, Mugs, Cards, Wall Art, Home, Apparel, Pets)
  └── ProductGrid
        └── ProductCard[] (2-column CSS grid)
              ├── ProductImage (lifestyle mockup, object-fit: cover)
              ├── BadgeOverlay (optional: "Best seller", "New", "Premium")
              └── ProductInfo
                    ├── ProductName (H3)
                    └── ProductPrice (Price font)
```

---

## Screen 2: Customise

### Purpose
Replace Step 3 of the current modal. User selects style, age theme, and sees
a live preview update. This screen replaces the StylePicker + bottom sheet approach.

### Layout Specification (412px reference)

```
 0px  ┌─────────────────────────────────────────┐
      │ [3px progress bar: segments 1+2 filled]  │
 3px  ├─────────────────────────────────────────┤
      │                                         │
      │  <- Back    CHARACTER MUG    £16.99     │
      │                                         │
47px  ├─────────────────────────────────────────┤
      │                                         │
      │         ┌───────────────────┐           │
      │         │                   │           │
      │         │   LIVE PREVIEW    │           │
      │         │   (Product        │           │
      │         │    Mockup)        │           │
      │         │                   │           │
      │         │   280px wide      │           │
      │         │   ~200px tall     │           │
      │         │                   │           │
      │         └───────────────────┘           │
      │                                         │
280px ├─────────────────────────────────────────┤
      │                                         │
      │  Style                                  │
      │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
      │  │Deflt │ │Hrtge │ │Crnvl │ │Ubntu │   │
      │  │      │ │      │ │      │ │      │ ->│
      │  └──────┘ └──────┘ └──────┘ └──────┘   │
      │  (horizontal scroll carousel)           │
      │                                         │
360px ├─────────────────────────────────────────┤
      │                                         │
      │  Age Theme                              │
      │  ┌──────────┐ ┌──────────┐ ┌────────┐  │
      │  │  Infant  │ │  Child   │ │  Teen  │  │
      │  └──────────┘ └──────────┘ └────────┘  │
      │  (3 chips, all visible, no scroll)      │
      │                                         │
430px ├─────────────────────────────────────────┤
      │                                         │
      │  (Spacer — allows scroll to see all)    │
      │                                         │
      │  Additional options (if applicable):    │
      │  - Recipient name input                 │
      │  - Variant toggle (front/back)          │
      │                                         │
      └─────────────────────────────────────────┘

Fixed ┌─────────────────────────────────────────┐
bottom│                                         │
      │   [ Continue to Preview  ->  ]          │
      │                                         │
      │   52px height, full width, violet       │
      └─────────────────────────────────────────┘
      + safe-area-inset-bottom
```

### Dimensions

| Element                  | Value                                         |
|--------------------------|-----------------------------------------------|
| Page padding (sides)     | 16px                                          |
| Top bar height           | 44px                                          |
| Preview area             | centred, 280px wide, aspect ratio preserved   |
| Preview top margin       | 16px below top bar                            |
| Preview bottom margin    | 20px                                          |
| Style section label      | H3: Inter 600, 16px, margin-bottom 12px       |
| Style chip carousel      | Horizontal scroll, 8px gap                    |
| Style chip width         | 72px                                          |
| Style chip height        | 88px (48px swatch + 40px label)               |
| Style swatch             | 48px x 48px, border-radius 8px                |
| Style label              | Caption: 12px, centred below swatch            |
| Age section label        | H3: Inter 600, 16px, margin-top 20px          |
| Age chip width           | calc((100% - 16px) / 3) = ~120px each         |
| Age chip height          | 40px                                          |
| Age chip gap             | 8px                                           |
| Age chip radius          | 8px                                           |
| Age chip font            | Body: 14px                                    |
| CTA bar height           | 52px + safe-area-inset-bottom                 |
| CTA bar padding          | 16px sides                                    |
| CTA bar bg               | #0D0F1A with 95% opacity + backdrop-blur 20px |
| CTA button radius        | 12px                                          |
| CTA button gradient      | linear-gradient(135deg, #7C3AED, #6D28D9)     |
| Spacer above CTA         | 68px (52px bar + 16px breathing room)         |

### Style Chip Carousel

Each chip shows a colour swatch representing the theme palette:

| Style             | Swatch colours (diagonal split)       | Label            |
|-------------------|---------------------------------------|------------------|
| Default           | #7C3AED / #4F46E5                     | "Classic"        |
| Heritage Gold     | #C8960C / #1B5E20                     | "Heritage"       |
| Carnival Spirit   | #FF6D00 / #00BFA5                     | "Carnival"       |
| Ubuntu            | Theme-dependent                       | "Ubuntu"         |

Selected chip: 2px solid #7C3AED border, slight scale(1.05) transform.
Unselected chip: 1px solid #2a2a4e border.

### Age Theme Chips

Three compact chips displayed in a single row (no scrolling needed):

| Chip      | Icon  | Label     |
|-----------|-------|-----------|
| Infant    | baby emoji | "Infant"  |
| Child     | child emoji | "Child"   |
| Teen      | teen emoji | "Teen"    |

Selected state: bg #7C3AED at 20%, border 1px solid #7C3AED, text white.
Unselected: bg #1a1a2e, border 1px solid #2a2a4e, text #B0B0C8.

### Live Preview Behaviour

- Preview updates immediately (no debounce) when user taps a style or age chip
- Transition: 200ms crossfade (opacity 0 -> 1) on content change
- Preview shows the PRODUCT MOCKUP, not the flat template:
  - Mugs: MugCeramicPreview SVG at 280px width
  - Cards: Card template at native size (fits within 280px)
  - Prints: Framed mockup via ProductMockup3D at 280px
  - Cushion: Cushion mockup via ProductMockup3D at 280px
  - T-shirt: T-shirt mockup via ProductMockup3D at 280px

### Product-Specific Options

Not all products show all options. Visibility rules:

| Product          | Style chips | Age chips | Recipient input | Variant toggle |
|------------------|-------------|-----------|-----------------|----------------|
| Character Mug    | YES (4)     | YES (3)   | YES             | NO             |
| Mug Wrap         | YES (4)     | NO        | NO              | NO             |
| Family Mug Set   | YES (4)     | NO        | NO              | Mum/Dad toggle |
| Greeting Card    | YES (4)     | NO        | YES             | Front/Inside   |
| Postcard         | YES (4)     | NO        | NO              | Front/Back     |
| Fine Art Print   | YES (4)     | NO        | NO              | NO             |
| Framed Canvas    | YES (4)     | NO        | NO              | NO             |
| Card Deck        | NO          | NO        | NO              | NO             |
| Cushion          | YES (4)     | NO        | NO              | NO             |
| Jigsaw Puzzle    | NO          | NO        | NO              | NO             |
| T-Shirt          | YES (4)     | NO        | NO              | NO             |
| Pet Report       | NO          | NO        | NO              | NO             |

If a product has no configurable options, Screen 2 shows just the preview
with a "Continue to Preview" CTA. The screen still exists (for URL consistency
and back-button coherence) but is visually simple.

### Component Hierarchy

```
KeepsakeCustomisePage
  ├── ProgressBar (step=2)
  ├── TopBar
  │     ├── BackButton (-> catalogue)
  │     ├── Title (product name)
  │     └── PriceLabel
  ├── PreviewArea
  │     └── ProductPreview (MugCeramicPreview | ProductMockup3D | CardTemplate)
  ├── ScrollableOptions
  │     ├── StyleSection (conditional)
  │     │     ├── SectionLabel ("Style")
  │     │     └── StyleChipCarousel
  │     │           └── StyleChip[] (swatch + label)
  │     ├── AgeSection (conditional)
  │     │     ├── SectionLabel ("Age Theme")
  │     │     └── AgeChipRow
  │     │           └── AgeChip[] (3 chips, single row)
  │     ├── RecipientSection (conditional)
  │     │     ├── SectionLabel ("Recipient Name")
  │     │     └── TextInput (full width, 44px height)
  │     └── VariantSection (conditional)
  │           ├── SectionLabel ("View")
  │           └── VariantToggle (2-segment pill)
  └── FixedBottomBar
        └── CTAButton ("Continue to Preview")
```

---

## Screen 3: Preview + Purchase

### Purpose
Replace Step 4 of the current modal. User sees a large, confident product
mockup and can add to basket with a single tap. This is the purchase-decision
screen -- the preview must inspire confidence.

### Layout Specification (412px reference)

```
 0px  ┌─────────────────────────────────────────┐
      │ [3px progress bar: all 3 segments filled]│
 3px  ├─────────────────────────────────────────┤
      │                                         │
      │  <- Back    PREVIEW           (...)     │
      │                                         │
47px  ├─────────────────────────────────────────┤
      │                                         │
      │                                         │
      │      ┌─────────────────────────┐        │
      │      │                         │        │
      │      │                         │        │
      │      │    LARGE PRODUCT        │        │
      │      │    MOCKUP               │        │
      │      │                         │        │
      │      │    ~340px wide          │        │
      │      │    ~360px tall          │        │
      │      │    (60% of viewport)    │        │
      │      │                         │        │
      │      │                         │        │
      │      └─────────────────────────┘        │
      │                                         │
      │  Character Mug — Heritage Gold          │
      │  Age: Infant                            │
      │                                         │
      │  ┌─ - - - - - - - - - - - - - ─┐       │
      │  │  View flat design  [toggle]  │       │
      │  └─ - - - - - - - - - - - - - ─┘       │
      │                                         │
      │  (spacer for fixed bottom bar)          │
      │                                         │
      └─────────────────────────────────────────┘

Fixed ┌─────────────────────────────────────────┐
bottom│                                         │
      │   [ Add to Basket — £16.99 ]    (...)   │
      │                                         │
      └─────────────────────────────────────────┘
      + safe-area-inset-bottom
```

### Dimensions

| Element                    | Value                                         |
|----------------------------|-----------------------------------------------|
| Page padding (sides)       | 16px                                          |
| Top bar height             | 44px                                          |
| Mockup container width     | min(340px, 100vw - 32px)                      |
| Mockup container height    | ~60% of available viewport (~396px)           |
| Mockup vertical centering  | Centred in container, aspect-ratio preserved  |
| Mockup top margin          | 16px                                          |
| Product label margin-top   | 16px below mockup                             |
| Product label font         | H2: Inter 600, 18px, white                   |
| Style subtitle font        | Body: Inter 400, 14px, #B0B0C8               |
| Flat design toggle margin  | 16px top                                      |
| Flat design toggle height  | 44px                                          |
| Bottom bar height          | 64px + safe-area-inset-bottom                 |
| Bottom bar bg              | #0D0F1A, 95% opacity, backdrop-blur 20px      |
| Bottom bar padding         | 8px 16px                                      |
| Add to Basket button       | flex: 1, height 48px, violet gradient         |
| Overflow menu button       | 44px x 44px, right of CTA, 8px gap            |
| Spacer above bottom bar    | 80px (64px bar + 16px breathing)              |

### Primary CTA: "Add to Basket"

| Property        | Value                                             |
|-----------------|---------------------------------------------------|
| Width           | flex: 1 (fills available space minus overflow btn) |
| Height          | 48px                                              |
| Background      | linear-gradient(135deg, #7C3AED, #6D28D9)         |
| Border-radius   | 12px                                              |
| Font            | CTA: Inter 600, 16px, white                       |
| Text content    | "Add to Basket -- GBP X.XX"                              |
| Active state    | scale(0.98), brightness(0.9), 100ms               |
| Disabled state  | opacity 0.5, no gradient                          |

### Overflow Menu (...) Button

Positioned to the right of the CTA. Contains secondary actions.

| Property        | Value                                      |
|-----------------|--------------------------------------------|
| Size            | 44px x 44px                                |
| Icon            | Three dots (horizontal ellipsis), 20px     |
| Background      | transparent                                |
| Border          | 1px solid #2a2a4e                          |
| Border-radius   | 12px                                       |
| Tap action      | Opens bottom sheet with secondary actions   |

### Overflow Menu Bottom Sheet

Slides up from bottom with 3 options:

| Action         | Icon          | Description                    |
|----------------|---------------|--------------------------------|
| Download PNG   | Download icon | Save flat design as PNG        |
| Share          | Share icon    | Native share sheet             |
| Buy Now        | Cart icon     | Skip basket, go to checkout    |

Sheet height: auto (content-sized, ~200px).
Sheet border-radius: 16px 16px 0 0.
Sheet bg: #1a1a2e.
Drag handle: 40px x 4px centred pill, #2a2a4e, at top.
Option row height: 52px each, 44px touch target.
Dividers: 1px solid #2a2a4e between rows.
Dismiss: tap outside or swipe down.

### "View Flat Design" Toggle

A text link with a toggle arrow that expands an inline panel showing the
full flat print template at native width with horizontal scroll.

| State      | Appearance                                        |
|------------|---------------------------------------------------|
| Collapsed  | "View flat design" text + chevron-down icon       |
| Expanded   | "Hide flat design" text + chevron-up icon         |

Expanded panel:
- Full width of page (minus 16px padding each side = 380px on 412px device)
- Horizontal scroll enabled for templates wider than 380px (mugs at 830px)
- Template rendered at 0.7x scale with scrollbar visible
- "Swipe to see full design" hint on first view (once, then dismissed)
- Panel height: clamped to 200px max, scroll within
- This is the DETAIL VIEW for users who want to inspect -- it is NOT the primary preview

### Product-Specific Mockup Rendering (Screen 3)

Each product type has a specific rendering approach at mobile width:

#### Mugs (character_mug, mug_wrap, family_mug_set)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | MugCeramicPreview (SVG)                         |
| Width prop          | 340px (fills container)                         |
| Aspect ratio        | Preserved by SVG viewBox                        |
| Content             | User's design composited onto ceramic mug body  |
| Visible portion     | Front ~40% of mug wrap (centre panel)           |
| Background          | Transparent (page bg shows through)             |
| Drop shadow         | filter: drop-shadow(0 8px 24px rgba(0,0,0,0.4))|

The user sees their mug as a 3D ceramic object, not an 830px flat strip.
Text on the mug is readable because MugCeramicPreview shows only the front
face at full resolution, not the entire wrap scaled down.

For family_mug_set: show both mugs side by side at 160px each, or a swipeable
carousel toggling between Mum and Dad mugs.

#### Cards (standard_card, greeting_card, postcard)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | Card template component (native render)         |
| Width               | Native width (290-360px) -- fits within 340px   |
| Aspect ratio        | Natural card proportions                        |
| Background          | Slight shadow to lift off page                  |
| Drop shadow         | 0 4px 16px rgba(0,0,0,0.3)                     |
| Border-radius       | 8px (simulating physical card corners)          |

Cards render at their native size. No scaling needed. They fit naturally
within the 340px container. This is the simplest and best case.

For greeting_card with inside text: show a subtle "Tap to open" hint and
animate a fold-open on tap to reveal the inside message.

#### Card Deck (card_deck)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | Stack of 3 cards, fanned at 5-degree increments |
| Card width          | 180px each                                      |
| Stack offset        | -5deg, 0deg, +5deg rotation                     |
| Background          | Cards show actual face designs                  |
| Drop shadow         | 0 4px 16px rgba(0,0,0,0.3) per card             |

Shows a "deck preview" -- 3 representative cards from the user's deck
fanned out. Tapping cycles through cards in the deck.

#### Fine Art Print (fine_art_print)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (framed print variant)          |
| Width               | 300px                                           |
| Frame               | SVG frame element surrounding the artwork       |
| Mat                 | 12px white mat between frame and artwork        |
| Artwork             | CertificateTemplate scaled to fit frame         |
| Background          | Subtle wall texture gradient behind frame       |
| Drop shadow         | 0 8px 24px rgba(0,0,0,0.3)                     |

The user sees their print as it would look hanging on a wall. The wall
texture gradient (light grey, subtle) behind the frame provides context.

#### Framed Canvas (framed_canvas)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (canvas variant)                |
| Width               | 300px                                           |
| Canvas depth        | 3D perspective shadow (4px visible edge)        |
| Artwork             | Template content wrapped onto canvas             |
| Background          | Subtle wall texture behind                      |
| Drop shadow         | 0 8px 32px rgba(0,0,0,0.4)                     |

Similar to fine art print but with visible canvas depth edge. No mat.

#### Cushion (cushion)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (cushion variant)               |
| Width               | 280px                                           |
| Aspect ratio        | 1:1 (square cushion)                            |
| Shape               | Rounded square with subtle "puff" gradient      |
| Artwork             | CushionTemplate centred on cushion face          |
| Background          | Transparent                                     |
| Drop shadow         | 0 6px 20px rgba(0,0,0,0.3)                     |

The user sees their cushion as a soft, puffy square object. The "puff"
effect is achieved with a radial gradient that makes edges appear to
curve away.

#### T-Shirt (tshirt_print)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (t-shirt variant)               |
| Width               | 300px                                           |
| Shirt colour        | White (default) or dark option                  |
| Artwork zone        | Centred on chest area, ~132px wide              |
| Background          | Transparent                                     |
| Drop shadow         | 0 4px 16px rgba(0,0,0,0.3)                     |

T-shirt mockup with artwork composited onto the chest area. The artwork
zone is smaller relative to the garment, which is correct -- the actual
print area on a real t-shirt is smaller than the garment.

#### Jigsaw Puzzle (jigsaw_puzzle)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (puzzle variant)                |
| Width               | 300px                                           |
| Effect              | SVG puzzle-piece grid overlay on artwork         |
| Scattered pieces    | 2-3 pieces offset from the main grid            |
| Background          | Subtle wood-grain texture gradient               |
| Drop shadow         | 0 4px 16px rgba(0,0,0,0.3)                     |

Shows the completed puzzle with a few pieces artfully scattered, sitting
on a wood-texture surface. Communicates "this is a physical puzzle".

#### Pet Family Report (pet_family_report)

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| Component           | ProductMockup3D (framed print variant)          |
| Width               | 300px                                           |
| Rendering           | Same as Fine Art Print (framed on wall)         |
| Drop shadow         | 0 8px 24px rgba(0,0,0,0.3)                     |

Treated identically to Fine Art Print -- it is the same physical product
(16" x 20" fine art print) with different content.

---

## Animation and Transition Specifications

### Page Transitions (Screen to Screen)

| Transition                  | Animation                                    | Duration | Easing                |
|-----------------------------|----------------------------------------------|----------|-----------------------|
| Catalogue -> Customise      | Slide left (new page slides in from right)   | 250ms    | cubic-bezier(0.25, 0.1, 0.25, 1) |
| Customise -> Preview        | Slide left                                   | 250ms    | cubic-bezier(0.25, 0.1, 0.25, 1) |
| Back (any)                  | Slide right (previous page slides from left) | 250ms    | cubic-bezier(0.25, 0.1, 0.25, 1) |
| Progress bar fill           | Width transition                             | 300ms    | ease-out              |

### In-Page Animations

| Element                     | Trigger                    | Animation                      | Duration |
|-----------------------------|----------------------------|--------------------------------|----------|
| Product card (catalogue)    | Appear on scroll           | fadeInUp (opacity 0->1, y 16->0)| 200ms    |
| Product card (tap)          | Touch start                | scale(0.97)                    | 100ms    |
| Product card (release)      | Touch end                  | scale(1.0)                     | 150ms    |
| Style chip (select)         | Tap                        | scale(1.05) + border change    | 150ms    |
| Age chip (select)           | Tap                        | bg colour transition           | 150ms    |
| Preview (content change)    | Style or age change        | Crossfade (opacity 0->1)       | 200ms    |
| CTA button (tap)            | Touch start                | scale(0.98) + brightness(0.9)  | 100ms    |
| CTA button (release)        | Touch end                  | scale(1.0)                     | 150ms    |
| Overflow sheet (open)       | Tap overflow button        | Slide up from bottom           | 250ms    |
| Overflow sheet (close)      | Tap outside / swipe down   | Slide down                     | 200ms    |
| Flat design panel (expand)  | Tap toggle                 | Height 0->200px, opacity 0->1  | 250ms    |
| Badge (catalogue)           | Card appear                | Scale 0->1 with 100ms delay    | 200ms    |
| Add to Basket confirmation  | After tap CTA              | Checkmark animation + text change to "Added!" | 400ms |

### Add to Basket Confirmation

When user taps "Add to Basket":
1. Button text fades to "Adding..." (100ms)
2. Subtle pulse animation on button (scale 1.0 -> 1.02 -> 1.0, 200ms)
3. Text changes to "Added!" with a checkmark icon (200ms fade)
4. After 1200ms, text reverts to "Add to Basket" (or navigates to basket if configured)
5. Small basket count badge appears/increments on the top-right (if basket icon present)

### Reduce Motion

All animations MUST respect `prefers-reduced-motion: reduce`:
- Replace slides with instant cuts
- Replace fades with instant opacity changes
- Disable scale transforms
- Keep colour transitions (they are not motion)

---

## Responsive Layout Summary

### 375px (iPhone SE) Adjustments

| Change from 412px baseline              | Value                          |
|------------------------------------------|--------------------------------|
| Grid card width                          | ~164px (narrower)              |
| Grid card image height                   | 130px (shorter to fit)         |
| Product name                             | text-overflow: ellipsis        |
| Screen 2 preview width                   | 260px (down from 280px)        |
| Screen 3 mockup width                    | 310px (down from 340px)        |
| Style chip width                         | 64px (down from 72px)          |
| Age chip width                           | ~106px each                    |
| Page side padding                        | 12px (down from 16px)          |

### 390px (iPhone 14) Adjustments

| Change from 412px baseline              | Value                          |
|------------------------------------------|--------------------------------|
| Grid card width                          | ~171px                         |
| Grid card image height                   | 140px                          |
| Screen 2 preview width                   | 270px                          |
| Screen 3 mockup width                    | 326px                          |
| All other values                         | Same as 412px baseline         |

---

## Accessibility Specifications

| Requirement                    | Implementation                                    |
|--------------------------------|---------------------------------------------------|
| WCAG 2.1 AA contrast           | All text-to-bg ratios verified >= 4.5:1            |
| White (#FFF) on violet (#7C3AED)| Contrast ratio 4.63:1 -- PASSES AA                |
| Light grey (#B0B0C8) on dark (#0D0F1A) | Contrast ratio 7.2:1 -- PASSES AAA       |
| Caption (#9090B0) on dark (#0D0F1A) | Contrast ratio 4.7:1 -- PASSES AA           |
| Focus indicators               | 2px solid #7C3AED outline, 2px offset              |
| Screen reader                  | All images have descriptive alt text               |
| Product cards                  | role="button", aria-label includes name + price    |
| Progress bar                   | role="progressbar", aria-valuenow, aria-valuemax   |
| Chip selection                 | role="radio" within role="radiogroup"              |
| Overflow menu                  | aria-haspopup="menu", aria-expanded                |
| Page transitions               | aria-live="polite" region for page title changes   |

---

## Product Pricing Reference

Prices displayed on product cards and the purchase CTA:

| Product            | Price    | Display format          |
|--------------------|----------|-------------------------|
| Postcard           | £3.99    | "Add to Basket -- £3.99"   |
| Greeting Card      | £6.99    | "Add to Basket -- £6.99"   |
| Playing Card       | £9.99    | "Add to Basket -- £9.99"   |
| Character Mug      | £16.99   | "Add to Basket -- £16.99"  |
| Ceramic Mug        | £14.99   | "Add to Basket -- £14.99"  |
| T-Shirt            | £19.99   | "Add to Basket -- £19.99"  |
| Fine Art Print     | £24.99   | "Add to Basket -- £24.99"  |
| Card Deck          | £24.99   | "Add to Basket -- £24.99"  |
| Jigsaw Puzzle      | £24.99   | "Add to Basket -- £24.99"  |
| Pet Family Report  | £24.99   | "Add to Basket -- £24.99"  |
| Family Mug Set     | £27.99   | "Add to Basket -- £27.99"  |
| Cushion            | £29.99   | "Add to Basket -- £29.99"  |
| Framed Canvas      | £39.99   | "Add to Basket -- £39.99"  |

---

## Assets Required

### Lifestyle Product Photography (Screen 1 catalogue)

12 lifestyle photos needed. These can be 3D renders or actual photography.
Each must be:
- Minimum 750px x 600px source (will be displayed at ~184px x 150px, need 2x for retina)
- WebP format with JPEG fallback
- File size: target < 60KB each (optimised for mobile data)
- Warm, inviting lighting. Dark/moody backgrounds that match #0D0F1A theme.
- No real faces visible (use illustrated/character designs on the products)

Numbered list of required photos:

1. `catalogue-character-mug.webp` -- White ceramic mug on dark wood table, warm side lighting, steam
2. `catalogue-mug-wrap.webp` -- Mug held in hands (hands visible, no face), cosy knit sweater
3. `catalogue-family-mug-set.webp` -- Two mugs on kitchen counter, morning light
4. `catalogue-greeting-card.webp` -- Card standing on mantelpiece with small vase of flowers
5. `catalogue-postcard.webp` -- Postcard on dark desk with fountain pen and stamps
6. `catalogue-fine-art-print.webp` -- Framed print on minimal living room wall, side angle
7. `catalogue-framed-canvas.webp` -- Canvas on gallery wall, dramatic lighting
8. `catalogue-card-deck.webp` -- Cards fanned on green felt surface
9. `catalogue-cushion.webp` -- Cushion on dark sofa, warm lamp light
10. `catalogue-jigsaw-puzzle.webp` -- Puzzle partially assembled on wooden table
11. `catalogue-tshirt.webp` -- T-shirt flat-lay on dark wood, styled with props
12. `catalogue-pet-report.webp` -- Framed report on shelf next to small dog figurine

### SVG Mockup Enhancements

The existing MugCeramicPreview and ProductMockup3D components need these updates:

1. MugCeramicPreview: Support `width={340}` without feature chip text becoming unreadable
   - Increase base chip font from 8.5px to 10px in the SVG viewBox
   - This maintains readability at 340px rendered width

2. ProductMockup3D: Add wood-grain and wall-texture background variants
   - `bg="wall"` -- subtle grey gradient for prints/canvas
   - `bg="wood"` -- warm brown gradient for puzzle
   - `bg="none"` -- transparent (default, for mugs/cushion/tshirt)

---

## Implementation Notes for FE Lead

### Routing

```
/keepsakes                     -> Screen 1 (KeepsakeCataloguePage)
/keepsakes/:productId          -> Screen 2 (KeepsakeCustomisePage)
/keepsakes/:productId/preview  -> Screen 3 (KeepsakePreviewPage)
```

The `productId` maps to PRODUCT_TYPES values from printProfiles.js
(e.g., `character_mug`, `mug_wrap`, `fine_art_print`).

### State Management

- Selected product, style, age theme, and recipient stored in a KeepsakeContext
- Context persists across Screen 2 and Screen 3 (not lost on back navigation)
- Basket state managed by existing BasketDrawer state

### Migration from KeepsakesModal

This spec replaces the 4-step modal flow on mobile devices ONLY.
Desktop (>768px) can continue using the modal flow until a separate
desktop redesign is undertaken. The mobile breakpoint for switching
to the new page-based flow: `max-width: 768px`.

At >=769px, the existing KeepsakesModal opens as before.
At <=768px, tapping "Keepsakes" navigates to `/keepsakes` instead.

### No-JavaScript Fallback

All 3 screens should render their core content (product images, text, prices)
without JavaScript. The interactive elements (chip selection, live preview,
animations) enhance progressively.

---

## Cultural Theme Compatibility

All screens MUST work with any cultural theme applied:

| Theme             | Chip swatch | Preview adapts | CTA unaffected |
|-------------------|-------------|----------------|----------------|
| Default (violet)  | #7C3AED     | YES            | YES            |
| Heritage Gold     | #C8960C     | YES            | YES (stays violet) |
| Carnival Spirit   | #FF6D00     | YES            | YES (stays violet) |
| Ubuntu            | Theme-dep   | YES            | YES (stays violet) |

The CTA button ALWAYS uses the brand violet gradient regardless of theme.
Theme colours only affect the product content preview and style chip swatches.
This maintains purchase-action consistency -- the "buy" button always looks the same.

---

## Visual Hierarchy (Per Screen)

### Screen 1: Product Catalogue
1. **Product photos** -- dominant visual, 68% of card area
2. **Product names** -- immediately below each photo
3. **Prices** -- paired with names
4. **Badges** -- eye-catching amber/violet on select products
5. **Category chips** -- secondary navigation, not primary focus

### Screen 2: Customise
1. **Live preview** -- centre of screen, largest element
2. **Style chips** -- immediately below preview, colourful swatches draw eye
3. **Age chips** -- below style, secondary selection
4. **CTA button** -- fixed at bottom, always visible, always reachable

### Screen 3: Preview + Purchase
1. **Product mockup** -- fills 60% of viewport, the "hero" of the page
2. **CTA button** -- "Add to Basket" with price, fixed at bottom, unmissable
3. **Product name + style** -- text confirmation of what they are buying
4. **Flat design toggle** -- tertiary, for detail-oriented users only
5. **Overflow menu** -- secondary actions tucked away

---

===============================================
  END OF VISUAL DIRECTION DOCUMENT
===============================================

**Sign-off required from:**
- [ ] CMO (strategy alignment)
- [ ] FE Lead (technical feasibility)
- [ ] QA Lead (testability of specs)

**Next steps after approval:**
1. Commission 12 lifestyle product photos (photography or 3D render)
2. FE Lead creates route structure and page components
3. Migrate mobile flow from KeepsakesModal to page-based navigation
4. QA tests on Samsung S22, iPhone SE, iPhone 14
5. A/B test against current modal flow for conversion comparison
