# Keepsake Mobile Shopping Experience -- Technical Implementation Plan

**Author:** Frontend Lead Agent
**Date:** 2026-04-01
**Input:** `Agent_1/crew/output/keepsake_mobile_design_audit.md` (QA Lead, 2026-04-01)
**Status:** PLAN -- awaiting CEO approval before implementation

---

## Executive Summary

The current `KeepsakesModal.jsx` (2100+ lines) renders a desktop-first modal with mobile workarounds bolted on. The audit identified 4 fundamentally broken templates on mobile (830px mug wraps), triple mobile-detection, and a preview system designed for print export rather than shopping.

This plan proposes a **parallel mobile component tree** that coexists with the desktop modal. No desktop functionality is touched. The mobile flow renders full-screen pages with product mockup previews, a collapsed action bar, and native navigation. Shared logic is extracted into hooks that both paths consume.

**Estimated effort:** ~1,200 LOC new code, ~200 LOC extracted into shared hooks, ~150 LOC removed from KeepsakesModal (mobile workarounds in Phase 4).

---

## 1. Component Structure

### Desktop (unchanged)
```
KeepsakesModal.jsx          -- existing 2100-line modal (desktop only after Phase 4)
  ModalOverlay              -- internal sub-component
  ModalContent              -- internal sub-component
  PillboxNav                -- internal sub-component
```

### Mobile (new)
```
src/components/keepsakes/mobile/
  KeepsakeMobileFlow.jsx    -- state machine + AnimatePresence router (~250 LOC)
  KeepsakeCatalogue.jsx     -- category grid + product list (Steps 1+2 combined) (~200 LOC)
  KeepsakeCustomise.jsx     -- style/age/recipient selection + live thumbnail (~250 LOC)
  KeepsakePreview.jsx       -- full-screen product mockup + purchase CTA (~300 LOC)
  MobileActionBar.jsx       -- 2-button action bar with overflow menu (~120 LOC)
  MobileHeader.jsx          -- back arrow + title + close (~80 LOC)
```

### Component Hierarchy
```
KeepsakeMobileFlow (state manager)
  ├── MobileHeader (back + title + close)
  ├── AnimatePresence
  │   ├── KeepsakeCatalogue (ProductCategoryGrid + product list)
  │   ├── KeepsakeCustomise (StylePicker + AgeBracketSelector + live thumbnail)
  │   └── KeepsakePreview (product mockup + template ref for export)
  └── MobileActionBar (Add to Basket + overflow menu)
```

### Why Steps 1+2 Are Combined

On mobile, the Category -> Product flow is two very short screens (6 category tiles, then 1-3 product rows). Combining them into a single scrollable catalogue avoids a screen transition for 2 seconds of content. The user sees category headers with products listed under each, and taps directly on a product. This matches mobile shopping patterns (Amazon, Etsy, Moonpig all show browseable product grids, not step-by-step wizards).

If a category has only one product (e.g., Pets -> Pet Family Report), tapping the category auto-selects the product and advances to Customise.

---

## 2. Routing Strategy

### Recommendation: Internal State Machine (not React Router)

| Option | Pros | Cons |
|--------|------|------|
| **React Router** (`/keepsakes/*`) | URL-addressable, native back button, shareable links | Requires context providers at route level, breaks current data flow (analysis data is in parent component state, not global), adds routes to AppRouter.jsx, complicates the modal-vs-page duality |
| **Internal state machine** | Zero routing changes, data stays in parent props, simpler to implement, can still use `history.pushState` for back button | Not URL-addressable, no deep linking to a specific step |
| **Framer Motion AnimatePresence** | Beautiful page-like transitions between steps | Not a routing solution on its own -- still needs a state machine underneath |

**Decision: State machine + AnimatePresence + pushState.**

Rationale:
1. The keepsake flow is opened from `MobileResultsSection.jsx` and `GroupSnapshotSection.jsx` via `isOpen` prop with `childIndex`, `pairwiseLink`, etc. These are parent-owned state. React Router routes would require lifting this data into a global store or URL params, which is a larger refactor than justified.
2. `history.pushState` already exists in the current modal (line 176-180 of KeepsakesModal.jsx). The mobile flow will use the same pattern: push state on each step transition, pop to go back.
3. AnimatePresence provides the iOS-like slide transitions that make it feel like page navigation without actual routing.

### State Machine Definition

```js
const MOBILE_STEPS = {
  CATALOGUE: 'catalogue',    // combined category + product browsing
  CUSTOMISE: 'customise',    // style + age + recipient selection
  PREVIEW: 'preview',        // product mockup + purchase
};
```

Transitions:
- `CATALOGUE -> CUSTOMISE`: on product selection (auto-selects default style)
- `CUSTOMISE -> PREVIEW`: on "Continue to Preview" tap
- Any step -> previous step: on back button or swipe-back gesture
- Any step -> closed: on X button

Each transition pushes a history entry. `popstate` listener moves backward through the step stack. If at CATALOGUE and user presses back, the flow closes entirely (returns to results screen).

---

## 3. Shared Logic

The following logic is currently embedded in `KeepsakesModal.jsx` and must be extracted into importable hooks/utilities so both desktop and mobile paths consume the same source of truth.

### Already Extracted (no work needed)
| Hook/Utility | File | Used By |
|---|---|---|
| `useKeepsakeData` | `hooks/useKeepsakeData.js` | Both |
| `useFamilyKeepsakeData` | `hooks/useFamilyKeepsakeData.js` | Both |
| `useGroupPairwiseKeepsakeData` | `hooks/useGroupPairwiseKeepsakeData.js` | Both |
| `usePetKeepsakeData` | `hooks/usePetKeepsakeData.js` | Both |
| `usePersonalizedMessage` | `hooks/usePersonalizedMessage.js` | Both |
| `exportCardAsPng` | `utils/cardExport.js` | Both |
| `exportAndDownloadCard` | `utils/cardExport.js` | Both |
| `generateKeepsakeFilename` | `utils/cardExport.js` | Both |
| `PRODUCT_SPECS` | `utils/printProfiles.js` | Both |
| `PRODUCT_TEMPLATE_REGISTRY` | `utils/templateRegistry.js` | Both |
| `getTemplateComponent` | `utils/templateRegistry.js` | Both |
| `PRODUCT_CATEGORIES` | `utils/productCatalog.js` | Both |
| `getCategoryProducts` | `utils/productCatalog.js` | Both |
| `AGE_BRACKETS, getAgeTheme` | `utils/ageThemes.js` | Both |
| `StylePicker` | `StylePicker.jsx` | Both |
| `ProductCategoryGrid` | `ProductCategoryGrid.jsx` | Both |
| `MugCeramicPreview` | `MugCeramicPreview.jsx` | Both |
| `ProductMockup3D` | `ProductMockup3D.jsx` | Both |
| `BasketContext (useBasket)` | `state/BasketContext.jsx` | Both |
| `usePlanFeatures` | `hooks/usePlanFeatures.js` | Both |
| `useCurrency` | `state/CurrencyContext.jsx` | Both |

### Needs Extraction (Phase 3)

#### 3a. `useKeepsakeFlow` hook (~60 LOC)

Extract the navigation state machine currently inline in KeepsakesModal (lines 122-317):

```js
// src/components/keepsakes/hooks/useKeepsakeFlow.js
export function useKeepsakeFlow() {
  // selectedCategory, selectedProduct, selectedStyle
  // selectedAge, selectedRecipient, selectedVariantOverride
  // navHistory, step
  // handleSelectCategory, handleSelectProduct, handleSelectStyle, handleBack
  // resolvedRecipient, resolvedVariant
  // resolvedComponent, previewStyleProp
  // isFamilyProduct (derived from selectedProduct)
  // templateData (data + personalised message merge)
}
```

This hook owns the **what is selected** state. Both desktop and mobile consume it.

#### 3b. `useKeepsakeExport` hook (~50 LOC)

Extract export/share/add-to-basket logic currently inline (lines 320-483):

```js
// src/components/keepsakes/hooks/useKeepsakeExport.js
export function useKeepsakeExport(cardRef, data, options) {
  // handleExport, handleShare, handleAddToBasket, handleOpenOrder
  // isExporting, isAdding, isOrdering
  // previewUrl, showOrderModal
  // error
}
```

#### 3c. `useKeepsakeDataResolver` hook (~20 LOC)

Extract the mode-detection + data-source selection (lines 101-131):

```js
// src/components/keepsakes/hooks/useKeepsakeDataResolver.js
export function useKeepsakeDataResolver({ childIndex, pairwiseLink, personAPhoto, personBPhoto, petIndex }) {
  // Returns: { data, isPairwiseMode, isPetMode, isFamilyProduct }
  // Internally calls useKeepsakeData, useGroupPairwiseKeepsakeData, usePetKeepsakeData, useFamilyKeepsakeData
}
```

### Not Shared (desktop-only, will stay in KeepsakesModal)

| Logic | Reason |
|---|---|
| `ModalOverlay` sub-component | Desktop modal pattern, not needed on mobile |
| `ModalContent` sub-component | Desktop modal sizing, not needed on mobile |
| `PillboxNav` sub-component | Desktop pillbox buttons (mobile has its own progress indicator) |
| Triple `isMobile` detection | Removed entirely in Phase 4 |
| `FlatPreviewScaler` | Desktop flat preview; mobile uses mockup-first |
| `useFocusTrap` ref | Desktop modal accessibility; mobile full-screen has native focus |
| Bottom sheet config (`showConfig`) | Replaced by dedicated KeepsakeCustomise screen |

---

## 4. Template Preview Strategy (Mobile Screen 3: KeepsakePreview)

The core principle from the audit: **mobile users see the finished product, not a scaled-down print template.** The template component still renders off-screen (hidden, at full resolution) for export. What the user sees on-screen is a product mockup.

### Per-Product Preview Rendering

| Product | Native Width | Mobile Preview Component | Preview Width | Notes |
|---|---|---|---|---|
| **Mug Wrap** | 830px | `MugCeramicPreview` SVG | 340px | SVG viewBox scaling. Shows "front face" of the mug. User sees a ceramic mug, not an 830px panorama. The 830px template renders off-screen in a hidden div for export only. |
| **Family Mug Set** | 830px | `MugCeramicPreview` SVG | 340px | Same approach. Show one mug at a time with a "Mum's / Dad's" tab toggle. |
| **Character Mug** | 830px | `MugCeramicPreview` SVG | 340px | Character illustration composited onto ceramic mug SVG. Already works well at 280px per audit; 340px is even better. |
| **Cards** (290-340px) | 290-340px | Direct template render | Native size, centred | Cards fit natively at 412px. Render the actual template component at 1:1 scale, centred in the preview area. No scaling needed. |
| **Certificate / Fine Art** | 480px | `ProductMockup3D` (framed) | 340px | Show the certificate inside a frame mockup. The 480px template at 340/480 = 0.71x inside a frame context is acceptable because frames have margins. |
| **Cushion** | 540px | `ProductMockup3D` (cushion) | 340px | ProductMockup3D cushion mockup at 340px. Artwork zone is large enough for the design to be visible. |
| **T-Shirt** | 360px | `ProductMockup3D` (t-shirt) | 340px | T-shirt mockup. Artwork zone at 340px width is 340 * 0.44 = 150px, acceptable for bold designs. |
| **Postcard** | 360px | Direct template render | 340px (0.94x) | Near-native. Slight scale, fully readable. |
| **Greeting Card** | 300px | Direct template render | 300px native | Fits perfectly. |
| **Bodysuit** | 240px | Direct template render | 240px native | Fits perfectly. |
| **Pet Report** | 480px | `ProductMockup3D` (framed) | 340px | Same as certificate -- framed mockup. |

### Hidden Export Template

For products where the preview is a mockup (mugs, cushions, t-shirts), the actual template component must still render at full resolution for png export. This is done via a hidden container:

```jsx
{/* Off-screen template for export — not visible to user */}
<div
  ref={cardRef}
  style={{ position: 'absolute', left: '-9999px', top: 0 }}
  aria-hidden="true"
>
  <TemplateComponent {...templateProps} />
</div>
```

This pattern already exists conceptually in the codebase (templates render at print dimensions regardless of viewport). The mobile flow just makes it explicit: the preview is the mockup, the export source is the hidden template.

### 3D Video Mockup

For `mug_wrap`, the existing video mockup (`/mockups/Mother_s_Day_Mug_Animation_Render (1).mp4`) should be available as a "3D Preview" toggle on the preview screen. Tapping it plays the video in the preview area. This is already implemented in the desktop modal and can be reused.

---

## 5. Migration Path

### Phase 1: Create Mobile Components (estimated 3-4 days)
**Goal:** Build the new mobile component tree alongside the existing modal. Zero changes to KeepsakesModal.jsx.

Files created:
```
src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx
src/components/keepsakes/mobile/KeepsakeCatalogue.jsx
src/components/keepsakes/mobile/KeepsakeCustomise.jsx
src/components/keepsakes/mobile/KeepsakePreview.jsx
src/components/keepsakes/mobile/MobileActionBar.jsx
src/components/keepsakes/mobile/MobileHeader.jsx
```

The mobile components initially duplicate some logic from KeepsakesModal (navigation state, export handlers). This is intentional -- we get the mobile flow working first, then extract shared logic.

Tests created:
```
src/components/keepsakes/mobile/__tests__/KeepsakeMobileFlow.test.jsx
src/components/keepsakes/mobile/__tests__/KeepsakeCatalogue.test.jsx
src/components/keepsakes/mobile/__tests__/KeepsakePreview.test.jsx
```

### Phase 2: Gate at Entry Point (estimated 1 day)
**Goal:** Route mobile users to the new flow, desktop users to the existing modal.

The gate lives in the **parent components** that render `<KeepsakesModal>`:
- `src/layout/MobileResultsSection.jsx` (line 559)
- `src/layout/GroupSnapshotSection.jsx`

```jsx
// In MobileResultsSection.jsx
import { KeepsakesModal } from "../components/keepsakes/KeepsakesModal.jsx";
import { KeepsakeMobileFlow } from "../components/keepsakes/mobile/KeepsakeMobileFlow.jsx";

// Gate: same props, different component
const isMobileViewport = window.innerWidth < 480;
// ... later in JSX:
{isMobileViewport ? (
  <KeepsakeMobileFlow
    isOpen={showKeepsakes}
    onClose={() => setShowKeepsakes(false)}
    childIndex={selectedChildIndex}
    pairwiseLink={pairwiseLink}
    personAPhoto={personAPhoto}
    personBPhoto={personBPhoto}
    onCardGenerated={handleCardGenerated}
  />
) : (
  <KeepsakesModal
    isOpen={showKeepsakes}
    onClose={() => setShowKeepsakes(false)}
    childIndex={selectedChildIndex}
    // ...same props
  />
)}
```

**Important:** The gate uses the same prop interface. `KeepsakeMobileFlow` accepts the same props as `KeepsakesModal`. This ensures the parent component does not need to know which path is active.

The `isMobileViewport` check should use the same `useState` + `useEffect` resize pattern already used in KeepsakesModal, but only in the parent -- not repeated in every sub-component.

### Phase 3: Extract Shared Hooks (estimated 2 days)
**Goal:** DRY up duplicated logic between desktop and mobile.

Create:
```
src/components/keepsakes/hooks/useKeepsakeFlow.js
src/components/keepsakes/hooks/useKeepsakeExport.js
src/components/keepsakes/hooks/useKeepsakeDataResolver.js
```

Refactor both `KeepsakesModal.jsx` and `KeepsakeMobileFlow.jsx` to consume these hooks. This is a refactor-only phase -- zero user-visible changes.

### Phase 4: Clean Up Desktop Modal (estimated 1 day)
**Goal:** Remove all mobile workarounds from KeepsakesModal.jsx, simplifying it to desktop-only.

Removals from KeepsakesModal.jsx:
- `isMobile` useState + useEffect (line 158-163) -- **remove**
- `overlayMobile` useState + useEffect in ModalOverlay (line 1640-1645) -- **remove**, always render desktop layout
- `mobile` useState + useEffect in ModalContent (line 1673-1678) -- **remove**, always use desktop max dimensions
- Bottom sheet config (`showConfig` state, 40vh drawer) -- **remove**
- 88px spacer div (line 1174) -- **remove**
- Compact style chips with arrows (line 792-861) -- **remove**
- `width={280}` mobile mockup override (line 1000) -- **remove**, always use desktop width
- Mug 0.7x horizontal scroll fallback (line 956-996) -- **remove**
- FlatPreviewScaler MIN_SCALE 0.6 horizontal scroll (line 1088-1117) -- **simplify** (keep desktop scaling, remove scroll fallback)

Estimated reduction: ~150 lines removed from KeepsakesModal.jsx, making it ~1950 lines. The component becomes cleaner and easier to maintain as a desktop-only modal.

---

## 6. File Structure

### Final State (after all 4 phases)

```
src/components/keepsakes/
  KeepsakesModal.jsx              -- DESKTOP ONLY (simplified to ~1950 lines)
  MugCeramicPreview.jsx           -- shared (SVG mug mockup)
  ProductMockup3D.jsx             -- shared (SVG product mockups)
  StylePicker.jsx                 -- shared (horizontal style selector)
  ProductCategoryGrid.jsx         -- shared (2-col category tiles)
  BasketDrawer.jsx                -- shared (bottom drawer basket)
  BasketBadge.jsx                 -- shared
  FreeKeepsakesPanel.jsx          -- shared
  OrderModal.jsx                  -- shared (order placement)

  hooks/
    useKeepsakeData.js            -- existing, shared
    useFamilyKeepsakeData.js      -- existing, shared
    useGroupPairwiseKeepsakeData.js -- existing, shared
    usePetKeepsakeData.js         -- existing, shared
    usePersonalizedMessage.js     -- existing, shared
    useKeepsakeFlow.js            -- NEW: navigation state machine (Phase 3)
    useKeepsakeExport.js          -- NEW: export/share/basket logic (Phase 3)
    useKeepsakeDataResolver.js    -- NEW: mode detection + data source (Phase 3)

  mobile/
    KeepsakeMobileFlow.jsx        -- NEW: state machine + AnimatePresence
    KeepsakeCatalogue.jsx         -- NEW: category + product browsing
    KeepsakeCustomise.jsx         -- NEW: style/age/recipient selection
    KeepsakePreview.jsx           -- NEW: product mockup + purchase CTA
    MobileActionBar.jsx           -- NEW: 2-button action bar + overflow
    MobileHeader.jsx              -- NEW: back + title + close

    __tests__/
      KeepsakeMobileFlow.test.jsx
      KeepsakeCatalogue.test.jsx
      KeepsakePreview.test.jsx

  templates/                      -- UNCHANGED (all template files stay exactly as they are)
  utils/                          -- UNCHANGED (all utility files stay exactly as they are)
```

---

## 7. Detailed Component Specifications

### 7a. KeepsakeMobileFlow.jsx

**Responsibility:** Top-level mobile container. Renders full-screen (100dvh). Owns the step state machine. Passes data and handlers down to child screens.

```jsx
// Props: same as KeepsakesModal
// { isOpen, onClose, childIndex, petIndex, pairwiseLink, personAPhoto, personBPhoto, onCardGenerated }

// Internal state:
// - step: 'catalogue' | 'customise' | 'preview'
// - selectedCategory, selectedProduct, selectedStyle, selectedAge
// - selectedRecipient, selectedVariantOverride
// - navHistory: string[] (for back navigation)

// Renders:
// - Fixed MobileHeader at top
// - AnimatePresence child screen (slide-left/right transitions)
// - Fixed MobileActionBar at bottom (only on preview step)
```

Uses `useKeepsakeDataResolver` for data, `useKeepsakeExport` for actions. Browser `popstate` listener for hardware back button.

**Safe area handling:** Uses `env(safe-area-inset-top)` and `env(safe-area-inset-bottom)` for notch/home-indicator phones.

### 7b. KeepsakeCatalogue.jsx

**Responsibility:** Product browsing. Shows all categories with products listed under each header.

Layout:
```
[Category Header: Wall Art]
  [Fine Art Print - from 24.99]  [Framed Canvas - from 34.99]

[Category Header: Cards]
  [Playing Card - 9.99]  [Card Deck - 19.99]  [Greeting Card - 7.99]  [Postcard - 5.99]

[Category Header: Drinkware]
  [Ceramic Mug - 14.99]  [Character Mug - 16.99]  [Family Mug Set - 29.99]
...
```

Each product tile shows:
- Product mockup image (or emoji icon as fallback)
- Product name
- Price
- 44px minimum touch target

Single-column scrollable list grouped by category. Touch targets are full-width rows (same pattern as current Step 2).

### 7c. KeepsakeCustomise.jsx

**Responsibility:** Style + age + recipient selection with a live thumbnail preview.

Layout (top to bottom):
1. **Style selector:** `StylePicker` component (horizontal scroll strip, already mobile-native)
2. **Age bracket:** Horizontal chip row (baby/child/teen/adult -- already exists in KeepsakesModal)
3. **Recipient** (character_mug only): chip row (Self/For Mum/For Dad/Grandparent)
4. **Variant** (character_mug only): chip row
5. **Live thumbnail:** Small preview of the current template at ~200px width, centered. This is a quick visual check, not the main preview -- that comes on the next screen.
6. **"Continue to Preview" button:** Full-width, sticky at bottom, 50px height, violet background.

The personalise toggle (with LLM message generation) also lives on this screen.

### 7d. KeepsakePreview.jsx

**Responsibility:** The money screen. Shows the product mockup large and clear, with purchase actions.

Layout:
1. **Product mockup** (fills available space, centred):
   - Mugs: `MugCeramicPreview` at `width={340}`
   - Cards <= 340px: direct template render at 1:1
   - Larger products: `ProductMockup3D` at `width={340}`
2. **Product name + price** below the mockup
3. **View toggle** (if applicable): "Product View" / "Design View" / "3D Video"
   - "Design View" shows the flat template in a horizontally scrollable container (for users who want to inspect details)
   - "3D Video" plays the MP4 mockup (mugs only)
4. **Hidden export template** (off-screen div with `ref={cardRef}`)

### 7e. MobileActionBar.jsx

**Responsibility:** Fixed bottom bar with primary CTA + overflow.

Layout:
```
┌─────────────────────────────────────┐
│  [+]  Add to Basket          [...]  │
│                                      │
│  env(safe-area-inset-bottom) pad     │
└─────────────────────────────────────┘
```

- **Primary:** "Add to Basket" -- full-width minus overflow button. 50px height. Violet background. White text.
- **Overflow (...):** 50x50px button. Tapping opens a bottom sheet with:
  - Download PNG
  - Share
  - Buy Now (direct order)
  - Customise (goes back to KeepsakeCustomise)

This replaces the current 5-button wrapping bar that consumes 120px+ of screen height.

If `!canOrderMerchandise()` (free tier), the primary button changes to "Download PNG" and the overflow contains only "Share".

### 7f. MobileHeader.jsx

**Responsibility:** Top bar with back arrow, title, and close button.

```
┌─────────────────────────────────────┐
│  ← Ceramic Mug            ×        │
│     For Sophie                      │
└─────────────────────────────────────┘
```

- Back arrow: 44x44px touch target. Calls `onBack` prop.
- Title: product name (or "Create Keepsake" on catalogue screen).
- Subtitle: child name / "For Sophie".
- Close (X): 44x44px touch target. Calls `onClose` prop.

Height: 56px (plus safe-area-inset-top).

---

## 8. AnimatePresence Transition Spec

Transitions between mobile steps use Framer Motion `AnimatePresence` with directional slides:

```jsx
const slideVariants = {
  enter: (direction) => ({
    x: direction > 0 ? '100%' : '-100%',
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction) => ({
    x: direction > 0 ? '-100%' : '100%',
    opacity: 0,
  }),
};

// direction = 1 for forward, -1 for backward
```

Transition config: `{ type: 'tween', duration: 0.25, ease: 'easeInOut' }`

This gives the native iOS page-push feel. Duration is 250ms to match iOS standard transitions.

---

## 9. Risk Assessment

### What Could Break

| Risk | Impact | Mitigation |
|---|---|---|
| Desktop modal regresses during Phase 3 (hook extraction) | HIGH -- desktop keepsakes stop working | Phase 3 is refactor-only. Run full test suite after every extraction. Desktop modal gets hooks injected one at a time with A/B verification. |
| Export PNG fails from hidden off-screen template | HIGH -- users cannot download or order | Test `html-to-image` with `position: absolute; left: -9999px`. This is a known-working pattern. The element must be in the DOM, not `display: none`. |
| `useBasket` context not available in mobile flow | MEDIUM -- add-to-basket fails | KeepsakeMobileFlow renders inside the same provider tree as KeepsakesModal (both are children of `MobileResultsSection` which is inside `BasketProvider`). No change needed. |
| `history.pushState` conflicts with AppRouter | LOW -- URL bar shows wrong path | The current modal already uses pushState (line 176). The mobile flow uses the same pattern. No new conflict introduced. |
| Animation jank on lower-end Android devices | LOW -- choppy transitions | Use `will-change: transform` on animated elements. AnimatePresence with `mode="wait"` prevents simultaneous old+new renders. Test on a budget Android device. |
| StylePicker scroll arrows too small on mobile | LOW -- existing issue, not made worse | The audit noted 28x28px arrows. The mobile flow reuses StylePicker as-is for Phase 1. A follow-up task can enlarge the arrows to 44px. |

### What Existing Functionality Is NOT Affected

- Desktop keepsake modal: untouched until Phase 4, and Phase 4 only removes mobile workarounds
- Template rendering for print export: identical pipeline (same `cardRef`, same `exportCardAsPng`)
- Basket integration: same `useBasket` hook, same `addItem` call signature
- Order flow: same `OrderModal` component, same `handleOpenOrder` logic
- Classic cards (legacy digital download): remain in KeepsakesModal desktop-only
- ProductShelf / MerchandiseModal: unrelated components, not touched

### Tests Required

#### Unit Tests (Vitest + React Testing Library)

1. **KeepsakeMobileFlow.test.jsx**
   - Renders when `isOpen=true`, does not render when `isOpen=false`
   - Step transitions: catalogue -> customise -> preview
   - Back navigation returns to previous step
   - Close callback fires on X tap
   - Correct data hook is called based on props (individual vs pairwise vs pet)

2. **KeepsakeCatalogue.test.jsx**
   - Renders all product categories
   - Product tap calls onSelectProduct with correct ID
   - Single-product categories auto-advance
   - Free tier shows upgrade prompt

3. **KeepsakePreview.test.jsx**
   - Mug products render MugCeramicPreview (not flat template)
   - Card products render template directly (not mockup)
   - Hidden export template has correct ref
   - Add to Basket calls basket.addItem with correct payload
   - Download triggers exportAndDownloadCard

4. **MobileActionBar.test.jsx**
   - Primary CTA is "Add to Basket" on Plus tier
   - Primary CTA is "Download PNG" on free tier
   - Overflow menu opens on ... tap
   - All overflow actions fire correct callbacks

#### E2E Tests (Playwright)

1. Mobile viewport (412px): open keepsake flow -> browse catalogue -> select mug -> customise -> preview -> add to basket
2. Mobile viewport: back navigation works at every step
3. Mobile viewport: hardware back button (popstate) goes back one step
4. Mobile viewport: mug preview shows ceramic mockup (not 830px scroll)
5. Desktop viewport (1024px): still opens KeepsakesModal (gate works)

---

## 10. Estimated LOC

| Component | New LOC | Notes |
|---|---|---|
| KeepsakeMobileFlow.jsx | ~250 | State machine, AnimatePresence, data resolution |
| KeepsakeCatalogue.jsx | ~200 | Category headers + product rows |
| KeepsakeCustomise.jsx | ~250 | Style/age/recipient + thumbnail |
| KeepsakePreview.jsx | ~300 | Mockup preview + hidden export template |
| MobileActionBar.jsx | ~120 | 2-button bar + overflow sheet |
| MobileHeader.jsx | ~80 | Back + title + close |
| useKeepsakeFlow.js | ~60 | Extracted navigation state |
| useKeepsakeExport.js | ~50 | Extracted export/share/basket |
| useKeepsakeDataResolver.js | ~20 | Extracted data source selection |
| Tests | ~300 | Unit tests for mobile components |
| **Total new** | **~1,630** | |
| **Removed from KeepsakesModal** | **~-150** | Mobile workarounds (Phase 4) |
| **Net change** | **~+1,480** | |

---

## 11. Dependencies

### No New npm Dependencies

The mobile flow uses only packages already in `desktop2/package.json`:
- `react`, `react-dom` (components)
- `framer-motion` (AnimatePresence, motion.div)
- `lucide-react` (icons -- Share2, Download, ShoppingCart, MoreHorizontal, ChevronLeft, X)
- `html-to-image` (dynamic import, already used by cardExport.js)

### No Backend Changes

The mobile flow consumes exactly the same API responses and data structures as the desktop modal. No new endpoints, no schema changes, no backend permission needed.

---

## 12. Open Questions for CEO

1. **Classic Cards on mobile:** The legacy card flow (WinnerDeclarationCard, TradingCard, etc.) is digital-download only and works well on mobile as-is (cards are 290-320px, fit natively). Should classic cards remain in the desktop modal on mobile, or should they be integrated into the mobile flow's catalogue?

   **Recommendation:** Keep them in the mobile flow catalogue under a "Digital Download" section. They render natively at mobile width so no special handling is needed.

2. **Phase 4 timing:** Should Phase 4 (cleanup of desktop modal) happen immediately after Phase 3, or should it wait for a monitoring period to confirm the mobile flow is stable?

   **Recommendation:** Wait 7 days after Phase 2 deploy. Monitor analytics for mobile keepsake conversions before removing desktop fallback code.

3. **Product photography:** The audit recommends showing "product photography composites" (mug on table, card in hand). Do we have or plan to commission product photography, or should we rely on the SVG mockups (`MugCeramicPreview`, `ProductMockup3D`) as the mockup layer?

   **Recommendation:** SVG mockups for launch. They are resolution-independent and already exist. Product photography can be a future enhancement.

---

*End of plan. No code changes were made. This document is architecture only.*
