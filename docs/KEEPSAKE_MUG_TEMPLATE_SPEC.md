# FamiliLook Mug Design System Specification
## Version 1.1 — Pre-Code Master Reference
## Status: AWAITING APPROVAL — no code changes until signed off

---

## 1. Physical Product Constraints (Prodigi Source of Truth)

| Property | Value | Source |
|----------|-------|--------|
| Product | Prodigi GLOBAL-MUG-W, 11oz white ceramic | Verified SKU |
| Print area | 228.6mm x 94.8mm (~229 x 95mm) | Prodigi API |
| Pixel dimensions | **2670 x 1110 px** at 300 DPI | Prodigi API `printAreaSizes.default` |
| Top bleed loss | 1mm (trimmed/not visible) | Prodigi product page |
| Bottom bleed loss | 2mm (trimmed/not visible) | Prodigi product page |
| Top feather zone | 5mm from rim (may distort) | Prodigi product page |
| Bottom feather zone | 4mm from base (may distort) | Prodigi product page |
| Handle gap | ~21mm from each side of handle remains white | Prodigi product page |
| Safe area | 5mm top, 4mm bottom, keep away from handle zones | Prodigi recommendation |
| DPI | 300 DPI | Prodigi spec |
| File format | PNG, transparent supported | Prodigi FAQ |
| Background | **TRANSPARENT** — mug ceramic shows through | Confirmed: transparency respected |
| Colour | Full colour, RGB | Prodigi spec |
| Sizing mode | `fillPrintArea` | Our API integration |

### Corrected values (our code was WRONG)

| Field | Our old code | Prodigi actual | Action |
|-------|-------------|----------------|--------|
| SKU | `GLOBAL-MUG-11OZ` (broken) | `GLOBAL-MUG-W` | Already fixed |
| Canvas px | 2717 x 1134 | **2670 x 1110** | Must fix |
| Bleed | 3mm uniform | 1mm top, 2mm bottom (asymmetric) | Must fix |
| Safe zone | 4mm uniform | 5mm top, 4mm bottom | Must fix |
| Print height mm | 114mm | **94.8mm** | Must fix |

### What the customer receives
A white ceramic mug with multi-coloured text, graphics, and optionally a photo printed directly onto the outer surface. The design wraps approximately 270 degrees around the mug (handle gap at the back). All content is printed in full colour on white ceramic. Transparent areas show the white mug surface.

### What the customer sees
Roughly 40% of the wrap is visible when looking at the mug from the front. The emotional centrepiece (name, headline, photo) **must** sit in the central 35% of the wrap width so it is fully visible without rotating the mug.

---

## 2. Canvas Layout — The Three Panels

The full 2670 x 1110px canvas divides into three horizontal panels:

```
┌──────────────┬─────────────────────────────┬──────────────────┐
│              │                             │                  │
│  LEFT PANEL  │      CENTRE PANEL           │  RIGHT PANEL     │
│  694px (26%) │      1282px (48%)           │  694px (26%)     │
│              │                             │                  │
│  Feature     │  Photo + Headline + Hero    │  Score + Brand   │
│  detail list │      (ALWAYS VISIBLE)       │  Secondary info  │
│              │                             │                  │
└──────────────┴─────────────────────────────┴──────────────────┘
```

**The centre panel is what the customer sees face-on.** It must be fully self-contained — a customer who never rotates the mug gets the complete emotional story.

### Safe margins within each panel

| Edge | Margin | Pixels | Reason |
|------|--------|--------|--------|
| Top | 5mm | 59px | Feather zone |
| Bottom | 4mm | 47px | Feather zone |
| Left edge of canvas | 5mm | 59px | Handle proximity |
| Right edge of canvas | 5mm | 59px | Handle proximity |
| Between panels | 0 | 0 | Panels flow into each other |

Usable content area: **2552 x 1004 px**

---

## 3. Content Elements — Full Inventory

| ID | Element | Required? | Max size | Notes |
|----|---------|-----------|----------|-------|
| A | Occasion header | Yes | 1 line, 25 chars | "HAPPY MOTHER'S DAY" / "FAMILY RESEMBLANCE" etc |
| B | Child/person photo | Optional | 80px circle (print) | If absent, space absorbed by headline |
| C | Child/person name | Yes | 1 line, 20 chars | Below photo or standalone |
| D | Main headline | Yes | 2 lines: "{Parent}, I look" + "more like you" | Largest text, emotional centrepiece |
| E | Hero feature callout | Yes | 1 line + optional sub-caption | "I have your Eyes" in pill badge |
| F | Feature chips (up to 8) | Yes | 4 per row, max 2 rows | Pink = winner parent, grey = other |
| G | Match score | Yes | 1 line: "72% Mum · 28% Dad" | Bold winner, muted loser |
| H | AI special comment | Optional | 2 lines, 50 chars/line | Only if personalisation enabled AND space available |
| I | Brand mark | Yes | "famililook.com" small | Fixed position, very muted |
| J | Top/bottom accent bands | Yes | 8px each | Accent colour strip |

### Mutual exclusions

- **H (AI comment)** is dropped if feature count > 6 — not enough vertical space
- **B (photo)** and **H (AI comment)** cannot both be large — if both present, photo shrinks to 64px
- If child has 8 features, H is **never shown**
- Occasion header is ONE of: seasonal text / "FAMILY RESEMBLANCE" / child's birthday — not multiple

### Always present (non-negotiable)

- C (child name), D (headline), E (hero feature), F (at least 4 chips), G (score), I (brand), J (bands)

---

## 4. Centre Panel Layout (Primary View)

The centre panel is **1282px wide x 1004px usable height**. All measurements in print pixels at 300 DPI.

```
┌─────────────────────────────────────────┐  y=0
│         [J] TOP ACCENT BAND             │  8px
├─────────────────────────────────────────┤  y=67 (after 59px safe margin)
│                                         │
│    [A] OCCASION HEADER                  │  font: 28px caps, tracking 0.25em
│    e.g. "HAPPY MOTHER'S DAY"            │  colour: accent
│                                         │
│    ────── thin rule ──────              │  1px, 60% width, accent 40% opacity
│                                         │
│    [B] PHOTO CIRCLE  (if present)       │  centre-x, r=80px (or 64px if H present)
│        (gap absorbed if absent)         │  border: 2px accent, soft shadow
│                                         │
│    [C] CHILD NAME                       │  font: 32px, italic, muted accent
│                                         │
│    [D1] "{MumLabel}, I look"            │  font: 44px, italic, dark #5A2035
│    [D2] "more like you"                 │  font: 56px, bold, accent #C0364E
│                                         │
│    ────── thin rule ──────              │
│                                         │
│    [E] "I have your {HeroFeature}"      │  pill bg, font: 32px, bold accent
│        sub-caption (if present)         │  font: 22px, muted, max 40 chars
│                                         │
│    ────── thin rule ──────              │
│                                         │
│    [F] FEATURE CHIPS                    │  4 per row, max 2 rows
│        row 1: up to 4 chips             │  chip: 160×52px, r=26px, gap: 16px
│        row 2: up to 4 chips (if >4)     │  accent chips = winner parent
│                                         │  grey chips = other parent
│                                         │
│    [H] AI COMMENT (if space)            │  only if ≤6 features
│        max 2 lines, 50 chars/line       │  font: 26px italic, muted accent
│                                         │
│    [G] SCORE LINE                       │  font: 28px
│        "72% Mum · 28% Dad"             │  accent bold for winner, muted other
│                                         │
│    [I] BRAND LINE                       │  font: 22px, tracking 0.15em
│        "famililook.com"                 │  very muted, 50% opacity
│                                         │
├─────────────────────────────────────────┤
│         [J] BOTTOM ACCENT BAND          │  8px
└─────────────────────────────────────────┘
```

---

## 5. Left Panel Layout (862px wide — visible when mug rotated left)

```
│  Vertical centred content:              │
│                                         │
│  Large decorative feature icon          │  240×240px, 8% opacity (watermark)
│                                         │
│  Feature list — text only               │  All 8 features listed vertically
│  Eyes ·········· 94%  ← Mum            │  font: 28px, two-column dotted
│  Smile ········· 88%  ← Mum            │  accent = winner parent
│  Nose ·········· 76%  ← Dad            │  grey = other parent
│  Face Shape ···· 71%  ← Mum            │
│  Hair ·········· 82%  ← Mum            │
│  Eyebrows ······ 65%  ← Dad            │
│  Skin ·········· 70%  ← Mum            │
│  Ears ·········· 58%  ← Dad            │
│                                         │
│  "Analysed by FamiliLook AI"            │  font: 22px italic, muted
```

---

## 6. Right Panel Layout (862px wide — visible when mug rotated right)

```
│  Vertical centred content:              │
│                                         │
│  Large percentage number                │  font: 180px bold, accent, 12% opacity
│  (watermark — e.g. "72%")              │  decorative only
│                                         │
│  "Analysis date: 25 Mar 2026"           │  font: 22px, muted grey
│  "Person: {childName}"                  │
│  "Compared with: {mumLabel}"            │
│                                         │
│  QR code placeholder (future)           │  160×160px reserved space
│                                         │
│  famililook.com                         │  repeated brand, muted
```

---

## 7. Variant Matrix — How Layout Adapts

| Scenario | Photo | AI Comment | Features | Layout change |
|----------|-------|------------|----------|---------------|
| Full data, ≤6 features | Yes (80px) | Yes (2 lines) | 1-6 chips | Full layout |
| Full data, 7-8 features | Yes (64px) | **Dropped** | 7-8 chips | Photo shrinks, H removed |
| No photo, ≤6 features | No | Yes | 1-6 chips | D+E move up, fonts enlarge slightly |
| No photo, 7-8 features | No | **Dropped** | 7-8 chips | D enlarges to fill space |
| Pairwise (two adults) | Both (2×40px) | Optional | Any | Headline: "You two look alike" |
| Mother's Day | Yes | Optional | Any | Header = "HAPPY MOTHER'S DAY", pink/rose |
| Father's Day | Yes | Optional | Any | Header = "HAPPY FATHER'S DAY", blue/gold |
| Birthday | Yes | Optional | Any | Header = "{name}'s BIRTHDAY", amber/purple |
| Generic | Yes | Optional | Any | Header = "YOUR FAMILY RESEMBLANCE", brand accent |

---

## 8. Typography Scale (Print Pixels at 300 DPI)

| Role | Font | Size | Weight | Colour |
|------|------|------|--------|--------|
| Occasion header | Georgia serif | 28px | 600 | Accent colour |
| Child name | Georgia serif | 32px | 400 italic | Muted accent |
| Headline line 1 | Georgia serif | 44px | 600 italic | Dark #5A2035 |
| Headline line 2 | Georgia serif | 56px | 800 | Primary accent |
| Hero feature | Georgia serif | 32px | 700 | Primary accent |
| Hero sub-caption | System sans | 22px | 400 | Muted #9B6070 |
| Chip label | Georgia serif | 26px | 600/400 | Accent / Grey |
| AI comment | Georgia serif | 26px | 400 italic | Muted accent |
| Score line | Georgia serif | 28px | 400 | Mixed accent/grey |
| Brand line | System sans | 22px | 400 | Very muted, 50% opacity |
| Left panel features | System sans | 28px | 400 | Accent / Grey |
| Right panel watermark | Georgia serif | 180px | 700 | Accent, 12% opacity |

---

## 9. Colour Palette

| Token | Default (Generic) | Mother's Day | Father's Day | Birthday |
|-------|-------------------|-------------|-------------|----------|
| accent-primary | From age theme | #C0364E | #1A6BB5 | #D97706 |
| accent-light | From age theme | #FF6B9D | #6BA3D4 | #F59E0B |
| accent-wash | From age theme | #FCEEF2 | #EEF3FB | #FEF3C7 |
| accent-muted | From age theme | #9B6070 | #5A7A96 | #92400E |
| accent-faint | From age theme | #C9A0AC | #A0B8CC | #D4A574 |
| neutral-chip | #F5F5F5 | #F5F5F5 | #F5F5F5 | #F5F5F5 |
| neutral-text | #888888 | #888888 | #888888 | #888888 |

---

## 10. Family Mug Set

Same physical mug, same print spec. Two mugs ordered — "Mum's Mug" and "Dad's Mug".

```
┌──────────┬────────────────────────────────────────────┬──────────┐
│ PARENT 1 │  CHILD 1    CHILD 2    CHILD 3    CHILD 4  │ PARENT 2 │
│ Photo    │  Photo      Photo      Photo      Photo    │ Photo    │
│ + Name   │  + Name     + Name     + Name     + Name   │ + Name   │
│          │  + Score    + Score    + Score    + Score   │          │
│          │  + Features + Features + Features + Feats  │          │
└──────────┴────────────────────────────────────────────┴──────────┘
```

- Parent anchors: ~420px each (left + right)
- Child columns: remaining ~1830px, divided equally
- Max children: 4 (beyond 4, reduce feature count)
- Feature count per child: 8 (1-2 kids), 6 (3 kids), 4 (4+ kids)
- Mum's Mug accent: #C0364E (rose), Dad's Mug accent: #1A6BB5 (blue)

---

## 11. Print Template Dimensions (MugWrapTemplate.jsx)

| Property | Value | Rationale |
|----------|-------|-----------|
| CSS width | 830px | Existing templateWidth, scales via pixelRatio |
| CSS height | 345px | 830 / (2670/1110) = 345px, matches print aspect ratio |
| Pixel ratio for export | 2670 / 830 = **3.217x** | html-to-image scales CSS to print resolution |
| Background | `transparent` | Vendor confirmed |
| Output | 2670 x 1110 px PNG | Prodigi fillPrintArea |

The print template renders the full 3-panel panoramic wrap as HTML/CSS. It is exported via html-to-image at 3.217x pixel ratio to produce the 2670×1110px PNG sent to Prodigi.

---

## 12. Preview Component Dimensions (MugCeramicPreview.jsx)

The preview is a **separate SVG component** — NOT a scaled-down version of the print template.

| Property | Value | Rationale |
|----------|-------|-----------|
| SVG viewBox | 500 x (dynamic) | Fixed width, height flexes to content |
| Render width | 260px (mobile) / 340px (desktop) | Passed as prop |
| Mug body | 310 x 310px in viewBox | Portrait/square — shows front face only |
| Content shown | Centre panel only | What customer sees without rotating |
| Background | White ceramic SVG | Realistic product appearance |

### Preview vs Print — key differences

| Aspect | Preview (SVG) | Print (HTML/CSS → PNG) |
|--------|---------------|------------------------|
| Shows | Front face (~40% of wrap) | Full 270° wrap |
| Panels | Centre only | Left + Centre + Right |
| Layout | Portrait/vertical | Panoramic/horizontal |
| Font sizes | 9–17px (viewBox scale) | 28–56px (print pixels) |
| Accent bands | Not shown | Top + bottom 8px bands |
| Height | Dynamic (flexes to content) | Fixed 345px CSS / 1110px print |
| Mug visual | SVG ceramic (rim, handle, shadow) | None — flat PNG |

### Preview variant handling

The preview must handle the same variant matrix as the print template (Section 7):

- **No photo**: Photo circle removed, headline moves up, spacing adjusts via sequential Y calculation
- **7-8 features**: AI comment dropped, photo shrinks to 64px circle
- **AI comment present**: Shows 2-line italic text between feature chips and score line (only if ≤6 features)
- **Occasion**: Header text and colour palette driven by `occasion` prop
- **Pairwise**: Two 40px photo circles side by side, headline changes to "You two look alike"

---

## 13. Colour Token System

Both print template and preview use the same colour tokens, resolved from `occasion` prop:

```js
const OCCASION_THEMES = {
  generic:     { primary: /* from ageTheme */, light: ..., wash: ..., muted: ..., faint: ... },
  mothers_day: { primary: "#C0364E", light: "#FF6B9D", wash: "#FCEEF2", muted: "#9B6070", faint: "#C9A0AC" },
  fathers_day: { primary: "#1A6BB5", light: "#6BA3D4", wash: "#EEF3FB", muted: "#5A7A96", faint: "#A0B8CC" },
  birthday:    { primary: "#D97706", light: "#F59E0B", wash: "#FEF3C7", muted: "#92400E", faint: "#D4A574" },
};

const OCCASION_HEADERS = {
  generic:     "YOUR FAMILY RESEMBLANCE",
  mothers_day: "HAPPY MOTHER'S DAY",
  fathers_day: "HAPPY FATHER'S DAY",
  birthday:    "{childName}'s BIRTHDAY",
};
```

---

## 14. What the Code Must Implement

### Files to CREATE:
1. **`MugWrapTemplate.jsx`** — One canonical print template. 830×345px CSS, transparent bg, 3-panel layout (left/centre/right). Accepts `{ data, occasion }` props. No `ageTheme`, no `style` — occasion drives theming.

2. **`mugThemes.js`** — Colour token definitions (`OCCASION_THEMES`, `OCCASION_HEADERS`). Shared by both print template and preview.

### Files to UPDATE:
3. **`MugCeramicPreview.jsx`** — Add `occasion` prop, wire colour tokens from `mugThemes.js`, add variant handling (no-photo, feature count, AI comment).

4. **`KeepsakesModal.jsx`** — Remove mug style variant selector. Mug products skip STYLE step, go straight to PREVIEW. Pass `occasion` to both MugWrapTemplate and MugCeramicPreview.

5. **`templateRegistry.js`** — Single mug entry: `styles: ["default"]`, component = MugWrapTemplate.

6. **`printProfiles.js`** — Correct dimensions: `width_px: 2670`, `height_px: 1110`, `width_mm: 228.6`, `height_mm: 94.8`.

### Files to DELETE (after new template is verified):
7. **`MugTimelineTemplate.jsx`** — Replaced by MugWrapTemplate
8. **`FamilyMugTemplate.jsx`** — Replaced by MugWrapTemplate with family data
9. Remove mothers_day style from mug entries in templateRegistry

---

## 15. Acceptance Criteria

Before the mug template is complete:

- [ ] MugWrapTemplate renders full 2670×1110px canvas with all 3 panels
- [ ] Centre panel is fully self-contained — readable without rotating mug
- [ ] All 9 variant scenarios from Section 7 render without overflow or invisible text
- [ ] MugCeramicPreview shows front-face SVG with real data, readable at 260px mobile width
- [ ] Preview adapts to occasion (generic/mothers_day/fathers_day/birthday)
- [ ] Preview adapts to variants (photo/no-photo, AI comment/none, feature count)
- [ ] Family Mug Set renders 1-4 children with adaptive feature counts
- [ ] Download PNG exports at 2670×1110px with transparent background
- [ ] No hardcoded white text (`#fff`, `rgba(255,255,255,...)`) anywhere
- [ ] printProfiles.js uses correct Prodigi dimensions
- [ ] Style variant selector removed for mug products
- [ ] Old mug templates deleted after verification

---

*This spec is the single source of truth. Implementation begins now.*
