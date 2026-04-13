===============================================
  VISUAL DIRECTION — Keepsake Fixes (KSK-01, KSK-02, KSK-04)
===============================================

PRODUCT: FamiliLook Keepsakes (Cushion, Bodysuit, Character Mug, Cards)
PRINT TARGET: Prodigi — various SKUs (Cushion 5400x5400px, Mug Wrap 2670x1110px, Bodysuit 240x300 CSS)
CONTEXT: Mobile preview on dark (#0D0F1A) background AND physical print output
AUTHOR: Visual Director
DATE: 2026-04-01
QA REF: Agent_1/crew/output/keepsake_fixes_qa_assessment.md

---

## FIX 1 — KSK-04: TRANSPARENT TEMPLATE PREVIEW BACKING

### Problem Statement

Templates with `background: "transparent"` (CushionTemplate, BodysuitTemplate) are designed for
print export where transparency is correct — the manufacturer applies the design to the substrate.
However, the mobile preview renders these templates on the dark `#0D0F1A` page background, making
all dark-coloured text (child name, subtitle, non-winner feature labels) invisible.

### Visual Direction: UNIVERSAL PREVIEW BACKING

**Approach:** Option A from QA assessment — a universal preview backing container in
`KeepsakeCustomise.jsx` that wraps all non-mug, non-card templates. This fixes the problem for
ALL transparent templates (current and future) without modifying individual template files.

**Do NOT modify the template `background: "transparent"` value.** The templates must remain
transparent for print export. The fix is purely in the preview wrapper.

### COLOUR PALETTE

| Token | Hex | Usage |
|-------|-----|-------|
| Preview backing | `#F7F6F4` | Warm off-white, simulates the feel of fabric/paper substrate |
| Backing border | `#E8E6E3` | 1px subtle border to separate backing from dark page |
| Drop shadow | `rgba(0, 0, 0, 0.08)` | Soft lift to distinguish the preview from the page |

**Why `#F7F6F4` and not pure white:**
- Pure white (`#FFFFFF`) creates harsh contrast against the `#0D0F1A` page and looks like a broken rect
- `#F7F6F4` is a warm neutral that reads as "product surface" rather than "error state"
- It harmonises with the mug ceramic colour (`#f9f9f7`) already used in MugCeramicPreview
- It provides sufficient contrast for ALL age-theme text colours (darkest: `#1A1A1A`, lightest: `#6B7280`)

**Universality:** This single backing colour works for ALL products because:
- Cushion templates use age-theme text colours designed for light backgrounds
- Bodysuit templates use age-theme text colours designed for light backgrounds
- Any future transparent template will also assume a light substrate

### LAYOUT SPEC

```
+--------------------------------------------------+
|  #0D0F1A  (page background)                      |
|                                                   |
|   +------------------------------------------+   |
|   |  padding: 12px                           |   |
|   |  background: #F7F6F4                     |   |
|   |  borderRadius: 16px                      |   |
|   |  border: 1px solid #E8E6E3               |   |
|   |  boxShadow: 0 2px 12px rgba(0,0,0,0.08) |   |
|   |                                           |   |
|   |   +------------------------------------+  |   |
|   |   |                                    |  |   |
|   |   |   ProductMockup3D                  |  |   |
|   |   |   (renders template inside)        |  |   |
|   |   |                                    |  |   |
|   |   +------------------------------------+  |   |
|   |                                           |   |
|   +------------------------------------------+   |
|                                                   |
+--------------------------------------------------+
```

### DIMENSIONS

| Property | Value | Rationale |
|----------|-------|-----------|
| `padding` | `12px` | Enough breathing room without wasting mobile viewport |
| `borderRadius` | `16px` | Matches iOS card radius convention, consistent with KeepsakeCatalogue cards |
| `border` | `1px solid #E8E6E3` | Defines edge without being heavy |
| `boxShadow` | `0 2px 12px rgba(0, 0, 0, 0.08)` | Subtle lift, not a hard drop shadow |

### WHERE TO APPLY

In `KeepsakeCustomise.jsx`, the wrapper at line 237 (`{!isMug && !isCard && (...)}`) should gain
a containing `<div>` with the backing styles. The backing wraps `ProductMockup3D`, NOT the
individual template.

```
BEFORE:
  {!isMug && !isCard && (
    <ProductMockup3D ...>
      <TemplateComponent ... />
    </ProductMockup3D>
  )}

AFTER:
  {!isMug && !isCard && (
    <div style={{
      background: "#F7F6F4",
      borderRadius: "16px",
      padding: "12px",
      border: "1px solid #E8E6E3",
      boxShadow: "0 2px 12px rgba(0, 0, 0, 0.08)",
    }}>
      <ProductMockup3D ...>
        <TemplateComponent ... />
      </ProductMockup3D>
    </div>
  )}
```

### VISUAL HIERARCHY (preview context)

1. **Child photo / feature icon** — the centre of the template, draws the eye first
2. **Child name + winner badge** — identity and result
3. **Feature badges** — detail layer
4. **Preview backing** — should be invisible as "design" — it reads as "surface" not "element"

### WHAT MUST NOT CHANGE

- Template `background: "transparent"` — untouched
- Print export pipeline — the backing is preview-only DOM, not in the export path
- Badge text colours — the backing provides sufficient contrast, no colour overrides needed
- The `theme.colors.text`, `theme.colors.textLight`, and `theme.colors.primary` values remain as-is

### CULTURAL THEME COMPATIBILITY

All 4 cultural themes have text colours designed for light backgrounds:
- **Heritage Gold:** dark text `#1A0F00` on `#F7F6F4` = excellent contrast (WCAG AAA)
- **Carnival Spirit:** dark text `#1A1A2E` on `#F7F6F4` = excellent contrast (WCAG AAA)
- **Ubuntu:** dark text `#3E2723` on `#F7F6F4` = excellent contrast (WCAG AAA)
- **Generic/Celebration:** dark text `#1A1A1A` on `#F7F6F4` = excellent contrast (WCAG AAA)

No per-theme adaptation needed. The universal backing works across all themes.

---

## FIX 2 — KSK-02: MUG HEADLINE TEXT OVERFLOW

This fix has two parts: (A) the print template headline containers, and (B) the SVG preview hero callout.

### PART A: CharacterMugTemplate Headline Containers

### Problem Statement

The headline `<div>` in all 4 layouts has `whiteSpace: "pre-line"` and `maxWidth: "100%"` but
NO `overflow: hidden`. If the headline engine's 35-char limit is exceeded by edge-case custom
names after template variable resolution, text overflows the panel boundary.

### Visual Direction: OVERFLOW GUARD + RESPONSIVE FONT SIZING

**Strategy:** Two-layer defence.
1. CSS overflow guard on all headline containers (safety net)
2. Font size step-down for long headlines (graceful degradation)

**Do NOT truncate with ellipsis.** Headlines are the hero visual element on a mug — an ellipsis
on a printed ceramic product looks broken, not designed. Instead, the headline engine already
provides short fallbacks. The CSS guard is a last resort that clips cleanly.

### TYPOGRAPHY SPEC — HEADLINE

| Layout | Panel Width (CSS px) | Standard Font Size | Long Text Font Size (>28 chars) | Minimum Font Size |
|--------|---------------------|--------------------|---------------------------------|-------------------|
| Hero (A) | 498px (60% of 830) | 42px (no photo) / 36px (with photo) | 32px (no photo) / 28px (with photo) | 28px |
| Celebration (B) | 373px (45% of 830) | 32px (with occasion) / 36px (without) | 28px (with occasion) / 30px (without) | 26px |
| Blend (C) | 414px (50% of 830) | 36px | 30px | 28px |
| Gift (D) | 539px (65% of 830) | 32px (with occasion) / 36px (without) | 28px (with occasion) / 30px (without) | 26px |

**Character count threshold for step-down:** 28 characters (excluding newlines).
This is below the engine's 35-char hard limit, giving a comfortable buffer.

**How the FE Lead should determine the font size:**
```
charCount = headline.text.replace(/\n/g, "").length
if charCount > 28:
  use "Long Text Font Size" from table above
else:
  use "Standard Font Size" from table above
```

**Minimum readable font size for mug print at 300 DPI:**
- At 3.217x pixel ratio, 26px CSS = ~84px at export = 0.28 inches at 300 DPI
- 0.28 inches (7mm) uppercase Nunito bold is clearly legible on ceramic at arm's length
- Do NOT go below 26px CSS (83px export) for ANY headline text

### OVERFLOW CSS SPEC — ALL 4 LAYOUTS

Add the following properties to the headline `<div>` style in HeroLayout (line 219),
CelebrationLayout (line 339), BlendLayout (line 437), and GiftLayout (line 584):

```
overflow: "hidden"
```

This single property addition is the safety net. Combined with `maxWidth: "100%"` already present,
it ensures text that somehow exceeds the container is clipped rather than overflowing.

**Do NOT add `textOverflow: "ellipsis"` to headlines.** The headline uses `whiteSpace: "pre-line"`
(multi-line), and `textOverflow: "ellipsis"` only works with `whiteSpace: "nowrap"`. Adding it
would be a no-op at best and confusing at worst.

### PART B: MugCeramicPreview SVG Hero Callout

### Problem Statement

The hero feature callout rect is hardcoded at 170px wide, but text content varies. The clip path
catches overflow but creates a hard mid-glyph crop — visually jarring.

### Visual Direction: WIDEN RECT + TIGHTEN TRUNCATION

| Element | Current | Specified |
|---------|---------|-----------|
| Hero callout rect width | 170px (`artCx - 85` to `artCx + 85`) | 200px (`artCx - 100` to `artCx + 100`) |
| Hero description truncation | `truncateAtWord(..., 22)` | `truncateAtWord(..., 18)` |
| Hero callout rect height | 22px | 22px (unchanged) |
| Hero text fontSize | 9.5 | 9.5 (unchanged) |

**Rationale:**
- Widening from 170px to 200px gives 30px more text room while staying within the mug body
  (mug body width = 310px, hero rect at 200px leaves 55px margin each side)
- Tightening truncation from 22 to 18 characters ensures the description portion fits within
  the widened rect even with the longest `heroLabel` ("Face Shape" = 10 chars)
- Combined: "I have your Face Shape . Almond-shaped, wi..." becomes
  "I have your Face Shape . Almond-shaped..." — fits cleanly in 200px at 9.5px font

**Layout change in MugCeramicPreview.jsx (line 193):**
```
BEFORE:  <rect x={artCx - 85}  y={yHeroBox - 14} width="170" ...
AFTER:   <rect x={artCx - 100} y={yHeroBox - 14} width="200" ...
```

**Truncation change in MugCeramicPreview.jsx (line 199):**
```
BEFORE:  truncateAtWord(heroDetail.description, 22)
AFTER:   truncateAtWord(heroDetail.description, 18)
```

### VISUAL HIERARCHY (mug preview)

1. **"Mum, I look more like you"** — the headline, largest text, centred
2. **Score line** — "67% Mum . 33% Dad"
3. **Hero feature callout** — pill-shaped highlight, theme wash fill
4. **Feature chips** — 8 small rectangles
5. **Brand mark** — smallest, most transparent

The hero callout pill (item 3) should feel like a comfortable badge, not a cramped label.
The 200px width gives it breathing room proportional to its visual importance.

### WHAT MUST NOT CHANGE

- The `clipPath="url(#mugHeroTextClip)"` on the hero `<g>` — keep as safety net
- Feature chip layout — already correct
- Score line and brand mark — already guarded
- The headline engine's 35-char limit — keep as the primary defence
- `whiteSpace: "pre-line"` on print template headlines — required for two-line headlines

---

## FIX 3 — KSK-01: CARD PRODUCTS IN CATALOGUE

### Visual Direction: CONTENT CURATION DECISION

### Current State (confirmed by QA)

- `standard_card` and `card_deck` have `hideFromCatalogue: true` — they do NOT render in the grid
- `greeting_card` and `postcard` DO render in the catalogue under the "Cards" category
- FamiliUno deck ordering uses `card_deck` directly via QPMarkets flow, not through catalogue browse

### Decision: KEEP "CARDS" CATEGORY, REMOVE HIDDEN PRODUCTS FROM ARRAY

**Category name:** Keep as "Cards" — do NOT rename to "Stationery".

**Rationale:**
- "Cards" is the natural user-facing term for greeting cards and postcards
- Users searching for "birthday card" or "postcard" will find the category intuitively
- "Stationery" implies writing paper, envelopes, notebooks — a mismatch for our products
- The FamiliUno card deck is in a completely separate user flow (game results -> order deck)
  and never appears alongside greeting cards. There is no realistic confusion vector.

**Hardening fix:** Remove `PRODUCT_TYPES.STANDARD_CARD` and `PRODUCT_TYPES.CARD_DECK` from
the `cards.products` array in `productCatalog.js` line 26.

```
BEFORE:
products: [PRODUCT_TYPES.STANDARD_CARD, PRODUCT_TYPES.CARD_DECK, PRODUCT_TYPES.GREETING_CARD, PRODUCT_TYPES.POSTCARD],

AFTER:
products: [PRODUCT_TYPES.GREETING_CARD, PRODUCT_TYPES.POSTCARD],
```

This makes the intent explicit in the data structure rather than relying on a runtime filter.
The `hideFromCatalogue` flag remains on the product specs as a secondary guard.

### Visual Distinction: Keepsake Cards vs FamiliUno Cards

No visual distinction is needed because:
1. They never appear in the same UI context
2. Greeting cards and postcards show in the Keepsakes catalogue flow
3. FamiliUno deck shows only in the game results -> order flow
4. Different branding (violet FamiliLook vs green-blue FamiliUno) already differentiates them
5. Different product imagery (family resemblance results vs playing card backs) differentiates them

**If in future both appear in the same UI** (e.g., a combined "My Orders" page), differentiate with:
- FamiliLook keepsake cards: violet `#7C3AED` accent badge "Keepsake"
- FamiliUno card deck: green `#30d158` accent badge "Game Deck"
- But this is a future concern, not needed now.

---

## ASSETS REQUIRED

None. All fixes use existing colour tokens and CSS properties. No new illustrations,
icons, or assets are needed.

---

## IMPLEMENTATION PRIORITY (by RPN from QA assessment)

| Priority | Issue | RPN | Files to Modify |
|----------|-------|-----|-----------------|
| 1 | KSK-04 — Preview backing | 448 | `KeepsakeCustomise.jsx` |
| 2 | KSK-02 — Mug headline overflow | 192 | `CharacterMugTemplate.jsx`, `MugCeramicPreview.jsx` |
| 3 | KSK-01 — Card products cleanup | 40 | `productCatalog.js` |

---

## REGRESSION CHECKLIST (for FE Lead after implementation)

- [ ] CushionTemplate preview: child name visible on mobile
- [ ] CushionTemplate preview: feature badge labels visible on mobile
- [ ] CushionTemplate preview: match badge still visible (white on gradient)
- [ ] BodysuitTemplate preview: text visible on mobile (if rendered via ProductMockup3D)
- [ ] CushionTemplate EXPORT: still has transparent background (NOT the backing colour)
- [ ] CharacterMugTemplate: headline with 35-char name does not overflow
- [ ] CharacterMugTemplate: headline with 15-char name still renders at standard size
- [ ] MugCeramicPreview: hero callout pill visually contains all text
- [ ] MugCeramicPreview: hero callout pill does not overlap mug body edges
- [ ] Catalogue: greeting_card and postcard still appear
- [ ] Catalogue: standard_card and card_deck do NOT appear
- [ ] FamiliUno deck ordering: still works (QPMarkets flow unaffected)
- [ ] All 4 cultural themes: cushion preview text readable
- [ ] All 4 mug layouts: headline contained within panel

===============================================
  END OF VISUAL DIRECTION
===============================================
