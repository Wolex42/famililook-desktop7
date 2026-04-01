# Keepsake Mobile Design Audit
**Author:** QA Lead Agent
**Date:** 2026-04-01
**Scope:** Systemic review of keepsake product system for mobile -- designed-for-desktop vs mobile-first
**Reference Device:** Samsung Galaxy S22 (412px CSS width)

---

## Section 1: The User Journey on Mobile (412px viewport)

### Step 1: Category Selection
**What the user sees:** Full-screen modal (no border-radius, fills 100dvh). A 2-column grid of 6 category tiles (ProductCategoryGrid). Each tile is ~194px wide with 12px gap. Below: "Classic Cards (digital download)" link.

**Verdict: WORKS WELL.** The 2-column grid was designed with mobile in mind. Tiles have min-height 100px, flex column layout, and scale naturally. Touch targets are comfortable. The "Classic Cards" link at the bottom is small (12px font, no min-height) but functional.

**Issues:**
- PillboxNav shows compact dot indicators (good), but the dots are only 8px tall -- below 44pt touch target for tapping back to a previous step.

### Step 2: Product Selection
**What the user sees:** A vertical list of product buttons, each with icon + label + price. Full-width, 14px padding, 12px border-radius.

**Verdict: WORKS WELL.** This step was clearly designed for single-column layouts. Each product row is a simple flex container that stretches naturally.

**Issues:**
- No issues at 412px. Product descriptions may wrap at 375px but remain readable.

### Step 3: Style Selection
**What the user sees:** StylePicker horizontal scroll strip + a 0.6x scaled preview of the template below.

**Verdict: HYBRID -- functional but compromised.**

**Issues:**
- The template preview is rendered at `transform: scale(0.6)` with `transformOrigin: "top center"`. For an 830px-wide mug template, this means the user sees 830 * 0.6 = 498px of content squeezed into a ~380px container. Horizontal overflow results.
- For a 480px certificate template, the 0.6x preview is 288px wide -- this fits, but text becomes unreadably small (9px font at 0.6x = 5.4px effective).
- The "Continue to Preview" button is sticky at bottom, which works well.

### Step 4: Preview + Purchase
**What the user sees:** The most complex step. Layout switches from `grid-template-columns: 200px 1fr` (desktop) to `1fr` (mobile). Age/Style selectors are hidden from the main layout and moved to a bottom sheet ("Customise" button).

**Verdict: DESKTOP-SQUEEZED. This is the primary problem area.**

**What works on mobile:**
- Grid collapses to single column (good)
- Age/Style/Recipient selectors move to bottom sheet via "Customise" button (good)
- Fixed action bar at bottom with safe-area-inset padding (good)
- 88px spacer div prevents content from being hidden behind fixed bar (good)
- Compact style chip row appears above preview with < > arrows (good idea, but...)

**What is broken/squeezed on mobile:**

1. **Mug templates (830px native) in flat view:** Forced to horizontal scroll at 0.7x scale (581px visible width). User must swipe left-right to see the full design. "Swipe to see full wrap design" hint appears, but this is a poor UX for a purchase preview.

2. **Character mug in mockup view:** Same 0.7x scroll approach. The 3D MugMockup component renders at `width={280}` on mobile, but the artwork inside is 830px scaled down to fit the mug body (~170px visible area). Text on the mug is unreadable at this size.

3. **Large templates (480px, 540px):** CertificateTemplate (480px), CushionTemplate (540px), PetFamilyReport (480px) use FlatPreviewScaler which clamps minimum scale at 0.6. At 412px viewport, the preview container is ~380px after padding. A 480px template at 0.6x = 288px -- fits but is tiny. A 540px template at 0.6x = 324px -- fits but text is illegible.

4. **View toggle buttons (Flat/Product Preview/3D Video):** These use 6px/14px padding with 11px font -- on a row of 3 options, the total width is ~300px which fits, but barely. The buttons do NOT meet 44pt touch target requirements.

5. **Action bar button overflow:** The fixed bottom bar contains up to 5 buttons on Plus tier: Customise + Download PNG + Share + Add to Basket + Buy Now. With `flexWrap: wrap`, these wrap to 2 rows, creating an action bar ~120px tall. Combined with the 88px spacer, this hides ~208px of preview content.

6. **Bottom sheet ("Customise"):** Fixed height of `40vh` = ~356px on a typical 890px tall phone. This is barely enough for Age Style chips + StylePicker + Recipient selector + Variant toggle + Done button. If all character_mug options are visible, the sheet scrolls, but the scrollable area is tight.

---

## Section 2: Component-by-Component Analysis

### KeepsakesModal.jsx (1800+ lines)
- **Native design width:** 640px maxWidth modal container
- **Mobile rendering approach:** Full-screen takeover (borderRadius: 0, height: 100dvh, padding: 0 on overlay). Single-column grid. Bottom sheet for config.
- **Classification: HYBRID** -- structural effort was made (isMobile checks throughout, bottom sheet, compact pillbox, fixed action bar), but the preview area inherits desktop template dimensions.
- **Key mobile hacks:**
  - `isMobile` state var with resize listener (breakpoint: 480px)
  - `overlayMobile` separate state in ModalOverlay (redundant detection)
  - `mobile` separate state in ModalContent (triple detection -- 3 resize listeners for the same thing)
  - Bottom sheet with fixed 40vh height
  - 88px spacer div for fixed action bar
  - Style chip row with < > nav arrows
  - `FlatPreviewScaler` with MIN_SCALE 0.6 and horizontal scroll fallback

### MugCeramicPreview.jsx (SVG)
- **Native design width:** 500px SVG viewBox width, default `width={340}` prop
- **Mobile rendering approach:** SVG viewBox scaling. The width prop is passed as 280 on mobile.
- **What the user sees at 412px:** SVG scales proportionally -- the mug shape, text, and feature chips all shrink linearly. At 280px, the SVG content is 56% of native size.
- **Classification: MOBILE-NATIVE** -- SVG viewBox scaling is the correct approach. Text remains proportional. This is one of the best-adapted components.
- **Issue:** Feature chip text at 280px width becomes 8.5px * 0.56 = ~4.8px effective -- borderline unreadable.

### ProductMockup3D.jsx (SVG-based mockups)
- **Native design width:** Default 320px, but proportional via SVG
- **Mobile rendering approach:** Width prop set to 280 on mobile. SVG shapes scale proportionally. Template artwork is scaled via CSS transform to fit the artwork zone.
- **Classification: DESKTOP-SQUEEZED** for mugs, **MOBILE-NATIVE** for other products
- **Mug mockup at 280px:** Body width is 280 * 0.72 - 280 * 0.12 = 168px. Artwork zone is 168 * 0.92 = 155px. The 830px mug template is scaled to 155/830 = 0.187x. Text designed for 830px at 0.187x is completely unreadable.
- **T-shirt mockup at 280px:** Artwork zone is 280 * 0.44 = 123px. Template (360px native) scaled to 123/360 = 0.34x. Still very small but the t-shirt design is primarily icons and large text, so it works better.
- **Greeting card mockup at 280px:** Artwork width is 268px, template is 300px native. Scale = 0.89x. This works well.

### StylePicker.jsx
- **Native design width:** Fluid (maxWidth: 100%)
- **Mobile rendering approach:** Horizontal scroll with touch scrolling, dot indicators, scroll arrows.
- **Classification: MOBILE-NATIVE** -- this was well designed. WebkitOverflowScrolling touch, scrollbar hidden, 120px min-width buttons, dot pagination.
- **Issue:** Scroll arrow buttons are 28x28px -- below 44pt touch target.

### BasketDrawer.jsx
- **Native design width:** 520px maxWidth
- **Mobile rendering approach:** Bottom-up drawer, 85vh maxHeight, safe-area-inset padding. Quantity buttons are 44x44px. Remove button is 44x44px.
- **Classification: MOBILE-NATIVE** -- this component was designed mobile-first. Touch targets correct, safe area handling, proper drawer pattern.
- **Issue:** Shipping form City/Postcode row uses `flex: 1 1 200px` and `flex: 1 1 140px` -- at 412px with padding, these wrap correctly. At 375px, both fields fill full width. Works fine.

### ProductCategoryGrid.jsx
- **Native design width:** Fluid 2-column grid
- **Mobile rendering approach:** CSS grid with `1fr 1fr`, 12px gap
- **Classification: MOBILE-NATIVE** -- clean, simple, responsive.

### PillboxNav (sub-component)
- **Native design width:** Fluid
- **Mobile rendering approach:** Compact mode with 8px dots and step label text
- **Classification: MOBILE-NATIVE** -- good compact adaptation
- **Issue:** Dot touch targets (8px wide, 20px for current) are too small to tap accurately.

---

## Section 3: Template Dimension Inventory

| # | Template File | Width (px) | Height (px) | Print Dimension | Scale at 412px | Rendering at 412px |
|---|---|---|---|---|---|---|
| 1 | WinnerDeclarationCard.jsx | 320 | auto (~450) | 2.5" x 3.5" card | 320 fits in ~380px container = 1.0x | FITS NATIVELY |
| 2 | FeatureHighlightCard.jsx | 320 | auto (~450) | 2.5" x 3.5" card | 1.0x | FITS NATIVELY |
| 3 | TradingCard.jsx | 290* | auto (~420) | 2.5" x 3.5" card | 1.0x | FITS NATIVELY |
| 4 | PokemonCard.jsx | 290* | auto (~400) | 2.5" x 3.5" card | 1.0x | FITS NATIVELY |
| 5 | PrincessCard.jsx | 320* | auto (~500) | 2.5" x 3.5" card | 1.0x | FITS NATIVELY |
| 6 | VaultCard.jsx | 290* | auto | 2.5" x 3.5" card | 1.0x | FITS NATIVELY |
| 7 | ProudParentCard.jsx | 320 | auto (~400) | Mug/T-shirt | 1.0x | FITS NATIVELY |
| 8 | FamilyBondCard.jsx | 320 | auto (~400) | Mug/T-shirt | 1.0x | FITS NATIVELY |
| 9 | MiniMeCard.jsx | 340 | auto (~450) | Card/Mug/T-shirt | 340/380 = 0.89x | SLIGHTLY SCALED |
| 10 | MugWrapTemplate.jsx | **830** | **345** | 11oz mug (2670x1110px) | 380/830 = 0.46x or 0.7x scroll | BROKEN -- h-scroll or unreadable |
| 11 | MugTimelineTemplate.jsx | **830** | 337 | 11oz mug (8307x3370px) | 0.46x or 0.7x scroll | BROKEN -- h-scroll or unreadable |
| 12 | FamilyMugTemplate.jsx | **830** | 337 | Mum & Dad mugs | 0.46x or 0.7x scroll | BROKEN -- h-scroll or unreadable |
| 13 | CharacterMugTemplate.jsx | **830** | **345** | Character mug (2670x1110px) | 0.7x scroll | BROKEN -- h-scroll |
| 14 | CertificateTemplate.jsx | **480** | **600+** | 16" x 20" fine art | 380/480 = 0.79x | SCALED -- text small but readable |
| 15 | CushionTemplate.jsx | **540** | **540** | 45cm x 45cm cushion | 0.6x clamp + scroll | SQUEEZED -- 324px, text tiny |
| 16 | GreetingCardTemplate.jsx | 300 | 420 | 5" x 7" card | 1.0x | FITS NATIVELY |
| 17 | PostcardTemplate.jsx | 360 | 246 | 6" x 4" postcard | 380/360 = 1.0x | FITS NATIVELY |
| 18 | BodysuitTemplate.jsx | 240 | 300 | Baby bodysuit | 1.0x | FITS NATIVELY |
| 19 | PetFamilyReport.jsx | **480** | **600+** | 16" x 20" | 0.79x | SCALED -- small but works |
| 20 | EasterTemplate.jsx | varies | varies | Multi-product adaptive | Depends on host product | VARIES |
| 21 | MothersDayTemplate.jsx | varies | varies | Multi-product adaptive | Depends on host product | VARIES |
| 22 | EasterCardTemplate.jsx | 300 | 420 | 5" x 7" card | 1.0x | FITS NATIVELY |

**Summary:**
- 12 templates fit at 412px without scaling issues (<=360px native width)
- 2 templates need moderate scaling (480px native) -- workable
- 1 template is borderline (540px cushion) -- text becomes tiny
- **4 templates are fundamentally broken on mobile (830px mug wraps)** -- require horizontal scrolling, which defeats the purpose of a product preview

---

## Section 4: The Core Problem Statement

The fundamental architectural mismatch is this:

**The keepsake system was designed as a print-export pipeline that happens to show a preview, not as a mobile shopping experience that happens to produce print output.**

The template system renders components at their physical print proportions (830px for a mug wrap because a mug wraps 360 degrees, 540px for a cushion, 480px for a 16x20" print). These dimensions are architecturally correct for print -- the html-to-image export needs to capture the full template at the print pixel ratio. But they were never designed to be the customer's primary preview mechanism on a 412px screen.

The result is a layered set of workarounds:
1. **CSS transform scaling** -- shrinks templates to fit, making text unreadable
2. **Horizontal scroll with hint text** -- forces the user to scroll sideways to see their own product, which no mature e-commerce platform does
3. **FlatPreviewScaler with MIN_SCALE clamp** -- prevents templates from shrinking below 0.6x, but adds horizontal scroll as the escape valve
4. **Three separate `isMobile` state variables** -- the modal, overlay, and content each independently detect mobile width via their own resize listeners, a symptom of mobile support being bolted on rather than designed in
5. **Bottom sheet for config** -- a good mobile pattern, but at fixed 40vh height it cannot accommodate all character_mug options without internal scrolling
6. **88px spacer div** -- a hard-coded workaround for the fixed action bar height, which will break if button count or wrapping changes

The mug wrap templates are the worst offenders: 830px wide content shown in a ~380px container. No amount of CSS scaling makes an 830px panoramic design readable at 46% size. The current "scroll at 0.7x" approach means the user sees only 54% of their mug design at any time and must horizontally scroll to see the rest -- while simultaneously being asked to confirm a purchase.

The 3D mockup path has a parallel problem: the MugMockup artwork zone is only ~155px wide at mobile width (280px), so the 830px template is rendered at 18.7% scale. This is not a preview -- it is a thumbnail.

---

## Section 5: Recommended Architecture

### Design Direction: Contextual Preview, Not Scaled Blueprint

Mobile users should see their keepsake **as a finished product**, not as a scaled-down print template. The template is the artifact for the print vendor; the mobile preview should be the artifact for the customer.

### Specific Recommendations

#### 1. Replace Flat Template Preview with Product Photography Composites on Mobile

Instead of rendering the 830px MugWrapTemplate at 0.7x with horizontal scroll, mobile should show a **photograph of a mug** with the design composited onto it. The existing MugCeramicPreview SVG already does this well -- it should be the primary mobile preview for ALL mug products, not just mug_wrap.

What Moonpig, Shutterfly, and Etsy do: They show a product photo (mug on table, card in hand, t-shirt on model) with the user's design mapped onto it. The flat "design view" is a secondary option for users who want to inspect details.

**Mobile default:** Product mockup (MugCeramicPreview for mugs, ProductMockup3D for others)
**Desktop default:** Flat template view with product mockup as secondary tab

This inverts the current priority. The "Flat Design" tab should be the detail view, not the primary view.

#### 2. Replace the 4-Step Modal with Full-Screen Pages on Mobile

The current modal is 640px maxWidth, full-height on mobile. It behaves like a page but is implemented as a modal with its own scroll context, overlay, and focus trap. On mobile, each step should be a full-screen page with a top navigation bar and native back behaviour.

Benefits:
- URL-addressable steps (user can share "look at this mug design" links)
- Native back button works correctly (currently requires pushState hack)
- No overlay/backdrop on mobile (wasted dark pixels behind a full-screen modal)
- No need for the triple `isMobile` resize listener pattern

#### 3. For Mug Products: Show a "Spin Preview" Rather Than a Flat Panorama

A mug wraps 360 degrees. Showing 830px flat is meaningless to a customer. Instead:
- Show the existing 3D video mockup as the primary preview (already exists for mug_wrap)
- Or show 3 static "views" of the mug: front, side-left, side-right -- each rendered by the MugCeramicPreview SVG with different content offsets
- The flat 830px design should only appear on the "export details" screen or as a desktop-only option

#### 4. Collapse the Action Bar to 2 Primary Actions on Mobile

The current 5-button action bar (Customise + Download + Share + Add to Basket + Buy Now) wraps to 2 rows and consumes ~120px of screen height. On mobile:

**Primary action:** "Add to Basket" (full-width button)
**Secondary actions:** A single "..." overflow menu containing Download, Share, Buy Now, Customise

This follows iOS HIG patterns where the primary CTA dominates and secondary actions are tucked away.

#### 5. Templates Should Have a `mobilePreviewWidth` Property

In printProfiles.js, each template has a `templateWidth` property that defines its CSS render width (e.g., 830 for mugs, 480 for certificates). There should be a parallel `mobilePreviewWidth` property that defines the width at which the template renders for mobile preview -- potentially with a simplified layout.

For example, a mug template at `mobilePreviewWidth: 360` could render a single-panel design showing only the "front face" of the mug, rather than the full panoramic wrap.

#### 6. Unify Mobile Detection

The three separate `useState/useEffect` pairs for mobile detection (in KeepsakesModal, ModalOverlay, and ModalContent) should be replaced with a single shared hook (`useMobile()` or `useMediaQuery`) that all components consume via context or direct import.

---

## Appendix A: Template Width Distribution

```
<=300px (fits any phone):   7 templates (cards, bodysuit, greeting card)
301-360px (fits most phones): 4 templates (postcard, mini-me, t-shirt print)
361-480px (needs scaling):    3 templates (certificate, pet report, cushion)
481-830px (BROKEN on mobile): 4 templates (all mug variants)
```

## Appendix B: Files Analysed

| File | Path | Lines |
|------|------|-------|
| KeepsakesModal.jsx | src/components/keepsakes/KeepsakesModal.jsx | ~2109 |
| MugCeramicPreview.jsx | src/components/keepsakes/MugCeramicPreview.jsx | 273 |
| ProductMockup3D.jsx | src/components/keepsakes/ProductMockup3D.jsx | 751 |
| StylePicker.jsx | src/components/keepsakes/StylePicker.jsx | 167 |
| printProfiles.js | src/components/keepsakes/utils/printProfiles.js | 642 |
| BasketDrawer.jsx | src/components/keepsakes/BasketDrawer.jsx | 470 |
| ProductCategoryGrid.jsx | src/components/keepsakes/ProductCategoryGrid.jsx | 67 |
| WinnerDeclarationCard.jsx | templates/ChildCards/ | ~200 |
| FeatureHighlightCard.jsx | templates/ChildCards/ | ~200 |
| TradingCard.jsx | templates/ChildCards/ | ~300 |
| PokemonCard.jsx | templates/ChildCards/ | ~280 |
| PrincessCard.jsx | templates/ChildCards/ | ~300 |
| VaultCard.jsx | templates/ChildCards/ | 42 |
| ProudParentCard.jsx | templates/ParentCards/ | ~200 |
| FamilyBondCard.jsx | templates/ParentCards/ | ~200 |
| MiniMeCard.jsx | templates/ParentCards/ | ~250 |
| MugWrapTemplate.jsx | templates/Products/Drinkware/ | ~200 |
| MugTimelineTemplate.jsx | templates/Products/Drinkware/ | ~200 |
| FamilyMugTemplate.jsx | templates/Products/Drinkware/ | ~200 |
| CharacterMugTemplate.jsx | templates/Products/Drinkware/ | ~400 |
| CertificateTemplate.jsx | templates/Products/WallArt/ | ~250 |
| CushionTemplate.jsx | templates/Products/Home/ | ~200 |
| GreetingCardTemplate.jsx | templates/Products/Cards/ | ~200 |
| PostcardTemplate.jsx | templates/Products/Cards/ | ~200 |
| BodysuitTemplate.jsx | templates/Products/Apparel/ | ~100 |
| PetFamilyReport.jsx | templates/Products/Pets/ | ~200 |
| EasterTemplate.jsx | templates/Seasonal/ | ~200 |
| MothersDayTemplate.jsx | templates/Seasonal/ | ~200 |
| EasterCardTemplate.jsx | templates/Seasonal/ | ~200 |

## Appendix C: Mobile Workaround Inventory

| Workaround | Location (line) | What it does | Why it exists |
|---|---|---|---|
| `isMobile` useState + resize | KeepsakesModal L158-163 | Detects <480px viewport | Mobile layout branching |
| `overlayMobile` useState + resize | ModalOverlay L1640-1645 | Same detection, separate instance | Modal overlay styling |
| `mobile` useState + resize | ModalContent L1673-1678 | Same detection, third instance | Modal content sizing |
| `transform: scale(0.6)` | Step 3 preview L659 | Shrinks template for style preview | Template too wide for mobile |
| `FlatPreviewScaler` MIN_SCALE 0.6 | L1088-1117 | Clamps minimum scale, adds h-scroll | Templates too wide for mobile |
| Mug 0.7x scroll | L956-996, L1044-1083 | Horizontal scroll at 70% scale | 830px template in 380px space |
| 88px spacer div | L1174 | Prevents content hidden by fixed bar | Fixed action bar overlap |
| Bottom sheet 40vh | L1335-1461 | Config panel on mobile | Desktop sidebar won't fit |
| Compact style chips | L792-861 | < > arrows + scroll chips | StylePicker too wide |
| `width={280}` for mockups | L1000 | Smaller mockup on mobile | 360px mockup too wide |

---

*End of report. No code changes were made. This document is analysis only.*
