# Character Illustration Brief — FamiliLook Character Mug Line
## Visual Director Agent | Date: 30 March 2026
## Status: READY FOR ILLUSTRATOR — CEO-approved creative brief as input

---

## Purpose

This document provides everything an illustrator (human or AI) needs to create the 5 core FamiliLook characters. It specifies exact dimensions, proportions, colour mappings, emotion variants, props, layout placements, SVG technical requirements, and theme adaptation rules.

**Input source**: CHARACTER_MUG_CREATIVE_BRIEF.md (CMO, CEO-approved)
**Print target**: Prodigi GLOBAL-MUG-W, 2670 x 1110px at 300 DPI, transparent PNG
**Viewing contexts**: Mug at arm's length (~50cm), TikTok thumbnail (~3cm), product grid (~2cm)

---

## 1. CHARACTER SHEETS

### 1.0 Universal Style Rules (All 5 Characters)

| Property | Specification |
|----------|---------------|
| Art style | Simple, rounded silhouettes — Mr. Men simplicity meets Duolingo expressiveness meets Cornish Prints warmth |
| Line quality | Smooth, confident, uniform-width strokes. No sketchy/hand-drawn wobble. Slightly rounded endpoints (round cap, round join). |
| Corner radius | All body shapes use generous radii (min 8px at 300px canvas). No sharp corners on bodies. |
| Fill style | Flat colour fills only. No gradients within character bodies. No textures. No halftones. |
| Outlines | Single solid outline in `dark` token colour from active theme. No double lines, no coloured outlines. |
| Eyes | Simple dot-and-highlight style. Black pupil dot + single white highlight dot. NO detailed iris/sclera. Expressive via size and position only. |
| Mouth | Simple curved line or open shape. No teeth detail (except cheeky grin = 2-3 simple tooth shapes). No lip detail. |
| Hands | Mitten-style (no individual fingers). Simple rounded paddle shape. |
| Feet | Simple rounded stumps or hidden by body. No shoe detail unless a specific prop (e.g., Mini Me trainers). |
| Skin/body colour | Uses theme `primary` or `light` token. NOT realistic skin tones. Real photos handle identity; characters are theme-coloured mascots. |
| Outline colour | Uses theme `dark` token |
| Cheek blush | Optional small circle in `light` token at 40% opacity on each cheek |

### 1.1 Mama Bear

**Role**: Appears when winner = Mum, or Mother's Day occasion.

| Property | Value |
|----------|-------|
| Bounding box | 300 x 300px (master SVG artboard) |
| Head-to-body ratio | 1:1.2 (large head, slightly longer body) |
| Head shape | Wide circle/oval, slightly wider than tall |
| Body shape | Pear/bell shape — rounded, warm, approachable |
| Hair | Bun on top of head (circle atop the head circle) OR natural curly cloud shape. Both variants needed. |
| Arms | Short rounded arms extending from upper body. Mitten hands. |
| Legs | Short stumpy legs, feet barely visible below bell body |
| Outline weight (print) | 8px at 300x300 master artboard (scales to ~71px at full 2670px print width if character fills left panel) |
| Outline weight (screen) | 2px at 80px rendered size |
| Default colour fills | Body: theme `primary`, Hair: theme `dark`, Bun/curls: theme `dark`, Cheeks: theme `light` at 40% opacity |
| Signature prop | Cup of tea (simple cylinder + handle + steam wiggles) |
| Distinguishing feature | Expressive large eyes with thick lash line (2 simple curved strokes above each eye) |

**Emotion variants required:**

| Variant ID | Expression | Pose | When used |
|------------|------------|------|-----------|
| `mama_proud` | Big smile, eyes squeezed happy | Standing tall, one hand on hip, other holding tea | winnerPct >= 70, winner = Mum |
| `mama_surprised` | O-shaped mouth, wide eyes | Both hands on cheeks (Home Alone pose) | Close call (51-59%) |
| `mama_cheeky` | Side smile, one eyebrow raised, wink | Leaning forward, pointing at headline | winnerPct >= 75, "SORRY DAD" headlines |
| `mama_loving` | Gentle closed-eye smile | Holding/cradling gesture (for use with Little Cub) | Mother's Day occasion |
| `mama_celebrating` | Wide open smile, eyes sparkly | Arms raised in the air, tea cup in one hand | Birthday / high percentage celebration |

**Occasion props (layered ON TOP of base emotion):**

| Occasion | Prop addition |
|----------|---------------|
| Mother's Day | Bouquet of flowers in free hand (simple 3-circle flower shapes) |
| Christmas | Santa hat replaces hair bun/curls |
| Birthday | Party hat (triangle, polka dots in `light` token) |
| Valentine's | Small heart floating above head |

---

### 1.2 Papa Bear

**Role**: Appears when winner = Dad, or Father's Day occasion.

| Property | Value |
|----------|-------|
| Bounding box | 300 x 300px |
| Head-to-body ratio | 1:1.4 (large head, slightly taller/broader body than Mama) |
| Head shape | Circle, slightly wider than Mama's |
| Body shape | Rectangle with very rounded corners — broad shoulders, straight sides, rounded bottom |
| Hair | Short flat-top or bald (both variants). Optional: 2-3 lines of hair on top. |
| Arms | Slightly longer than Mama's. Same mitten hands. |
| Legs | Short stumpy legs, same style as Mama |
| Glasses | Optional prop variant: simple round frames (circle + thin arms). Needed as both with/without. |
| Outline weight (print) | 8px at 300x300 master |
| Outline weight (screen) | 2px at 80px |
| Default colour fills | Body: theme `primary`, Hair: theme `dark` at 60% opacity, Glasses frames: theme `dark` |
| Signature prop | Holding baby/child (simplified Mini Me or Little Cub shape tucked in arm) |
| Distinguishing feature | Broad shoulders, kind thick eyebrows (2 rounded rectangle strokes) |

**Emotion variants required:**

| Variant ID | Expression | Pose | When used |
|------------|------------|------|-----------|
| `papa_proud` | Broad grin, chest puffed out | Standing with arms crossed (confident) | winnerPct >= 70, winner = Dad |
| `papa_surprised` | Raised eyebrows, mouth open | Scratching head with one hand | Close call (51-59%) |
| `papa_cheeky` | Smirk, one eyebrow up | Pointing at headline with finger guns | winnerPct >= 75, "SORRY MUM" headlines |
| `papa_loving` | Gentle smile, soft eyes | Holding Little Cub in arms | Father's Day occasion |
| `papa_celebrating` | Wide grin, eyes closed happy | Fist pump, one arm raised | Birthday / high percentage |

**Occasion props:**

| Occasion | Prop addition |
|----------|---------------|
| Father's Day | "World's Best Dad" mini mug in hand (meta!) |
| Christmas | Santa hat on head |
| Birthday | Party hat |
| Valentine's | Standing next to Mama Bear (paired pose) |

---

### 1.3 Little Cub

**Role**: Represents the child being analysed, age 0-2.

| Property | Value |
|----------|-------|
| Bounding box | 300 x 300px (but character is SMALLER within it — ~200x200px centred, leaving room for props) |
| Head-to-body ratio | 1:0.6 (oversized head, tiny body — classic baby proportions) |
| Head shape | Perfect circle, largest element |
| Body shape | Tiny bean/oval beneath head. Almost a head on a cushion. |
| Arms | Tiny rounded stubs |
| Legs | Hidden — sitting on cushion or swaddled |
| Outline weight (print) | 6px at 300x300 master (slightly thinner = more delicate) |
| Outline weight (screen) | 1.5px at 80px |
| Default colour fills | Body: theme `wash` (lightest token), Head: theme `light`, Cheeks: theme `primary` at 30% opacity |
| Signature prop | Dummy/pacifier (simple circle + shield shape) + sitting on a cushion (rounded rectangle beneath) |
| Distinguishing feature | Enormous eyes (40% of head width), single tuft of hair (one curved stroke on top) |

**Emotion variants required:**

| Variant ID | Expression | Pose | When used |
|------------|------------|------|-----------|
| `cub_happy` | Big round eyes, tiny smile | Sitting on cushion, arms out | Default — any result |
| `cub_sleeping` | Eyes closed (curved lines), peaceful | Lying on cushion, blanket shape | Right panel quiet accent |
| `cub_surprised` | Huge round eyes, O mouth | Sitting up, arms raised | Close call percentage |
| `cub_giggling` | Scrunched happy eyes, open mouth laugh | Bouncing on cushion | High percentage celebration |
| `cub_curious` | One eye bigger than other, head tilted | Reaching toward something | Pointing at data element |

**Occasion props:**

| Occasion | Prop addition |
|----------|---------------|
| Birthday | Tiny party hat on tuft of hair, single balloon string in hand |
| Christmas | Tiny elf hat, wrapped present box next to cushion |
| Mother's Day | (Not primary character — appears as accent) |
| Father's Day | (Not primary character — appears as accent) |

---

### 1.4 Mini Me

**Role**: Represents the child being analysed, age 3-12.

| Property | Value |
|----------|-------|
| Bounding box | 300 x 300px |
| Head-to-body ratio | 1:1.0 (large head, equal body — child proportions, not baby) |
| Head shape | Circle, same style as Little Cub but slightly less dominant |
| Body shape | Small rectangle with rounded corners. Visible arms and legs. |
| Arms | Short but functional — can hold things, point, wave |
| Legs | Short legs with simple round feet |
| Outline weight (print) | 7px at 300x300 master |
| Outline weight (screen) | 2px at 80px |
| Default colour fills | Body: theme `light`, Hair: theme `dark`, Clothing detail: theme `primary` |
| Signature prop | Backpack (simple rounded shape on back) OR toy (teddy bear shape in hand) |
| Distinguishing feature | Cheeky grin (asymmetric smile, one corner higher), messy hair (3-4 spiky strokes) |

**Emotion variants required:**

| Variant ID | Expression | Pose | When used |
|------------|------------|------|-----------|
| `mini_proud` | Big grin, thumbs up | Standing with one arm doing thumbs up | winnerPct >= 65 |
| `mini_cheeky` | Tongue out, wink | Leaning to one side, arms behind back | "SORRY DAD/MUM" headlines |
| `mini_surprised` | Wide eyes, raised eyebrows | Hands on head | Close call |
| `mini_pointing` | Determined smile | Pointing at something with extended arm | Pointing at headline/data |
| `mini_celebrating` | Huge smile, jumping | Both feet off ground, arms up | Birthday / high percentage |

**Occasion props:**

| Occasion | Prop addition |
|----------|---------------|
| Birthday | Party hat, holding balloon |
| Christmas | Santa hat, holding candy cane |
| Generic | Backpack default |

---

### 1.5 Gran/Gramps

**Role**: Appears when gift recipient is tagged as grandparent.

| Property | Value |
|----------|-------|
| Bounding box | 300 x 300px |
| Head-to-body ratio | 1:1.3 (slightly hunched, cosy proportions) |
| Head shape | Circle, slightly smaller than Mama/Papa (gentler presence) |
| Body shape | Soft rounded rectangle. Cardigan lines (2 vertical lines down front). Slightly hunched upper body. |
| Hair | Gran: soft bun (smaller than Mama's, lower position) or short wavy. Gramps: bald/thin on top, tufts on sides. |
| Arms | Holding cup of tea (default), or resting on lap |
| Legs | Short, seated in armchair (chair = simple rounded rectangle behind/beneath) |
| Glasses | Always present — smaller round frames than Papa. Reading glasses sit lower on nose. |
| Outline weight (print) | 7px at 300x300 master |
| Outline weight (screen) | 2px at 80px |
| Default colour fills | Body: theme `muted`, Cardigan: theme `wash`, Hair: theme `faint`, Glasses: theme `dark` |
| Signature prop | Cup of tea + reading glasses + armchair |
| Distinguishing feature | Warm crinkled-eye smile (small curved lines at eye corners), cardigan button detail (2-3 small circles) |

**NOTE**: Gran and Gramps are TWO sub-variants of the same character slot:
- `gran_*` variants: bun/wavy hair, slightly smaller frame
- `gramps_*` variants: bald/tufts, slightly broader frame, thicker eyebrows
Both share the same poses and emotion set.

**Emotion variants required:**

| Variant ID | Expression | Pose | When used |
|------------|------------|------|-----------|
| `gran_proud` / `gramps_proud` | Beaming smile, crinkled eyes | Sitting in chair, holding tea, leaning forward | Default grandparent mug |
| `gran_surprised` / `gramps_surprised` | Raised glasses, wide eyes | Glasses pushed up on forehead, mouth open | Close call percentage |
| `gran_loving` / `gramps_loving` | Gentle closed-eye smile | Arms open for hug | Grandparent's Day |
| `gran_showing_off` / `gramps_showing_off` | Proud grin, chest out | Holding mug out toward viewer (showing the mug on the mug — meta!) | Social sharing context |
| `gran_laughing` / `gramps_laughing` | Head tilted back, open mouth | Slapping knee, tea sloshing | Funny headline reaction |

**Occasion props:**

| Occasion | Prop addition |
|----------|---------------|
| Grandparent's Day | "Best Gran/Gramps Ever" banner held across lap |
| Christmas | Knitted Christmas jumper pattern on cardigan (simple zigzag line) |
| Birthday | Party hat balanced on reading glasses |

---

## 2. MUG LAYOUT SPEC

### 2.1 Full Canvas — 2670 x 1110px (Prodigi GLOBAL-MUG-W)

```
           LEFT PANEL              CENTRE PANEL                RIGHT PANEL
           694px (26%)             1282px (48%)                694px (26%)
     ┌─────────────────────┬───────────────────────────────┬─────────────────────┐
     │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│                               │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ y=0
     │▓▓ TOP SAFE (59px) ▓│    TOP SAFE ZONE (59px)       │▓▓ TOP SAFE (59px) ▓│ y=59
  59 ├─────────────────────┼───────────────────────────────┼─────────────────────┤
     │                     │                               │                     │
     │   ┌─────────────┐   │   [A] OCCASION HEADER         │   ┌─────────┐       │
     │   │             │   │       caps, 28px, tracking     │   │ sleeping│       │
     │   │  CHARACTER   │   │   ─────── thin rule ───────   │   │  cub    │       │
     │   │  ILLUSTRATION│   │                               │   │ accent  │       │
     │   │             │   │   [B] CHILD PHOTO (100px r)   │   │ 200x300 │       │
     │   │  Full height │   │       thick accent border     │   └─────────┘       │
     │   │  ~576x992px │   │                               │                     │
     │   │             │   │   [C] CHILD NAME              │   confetti/stars     │
     │   │  Mama/Papa  │   │       32px italic              │   pattern at        │
     │   │  Bear       │   │                               │   8% opacity        │
     │   │  reacting   │   │   [D] HERO HEADLINE           │                     │
     │   │  to result  │   │       56px bold caps rounded   │   "Analysed by      │
     │   │             │   │       e.g. MUMMY'S MINI ME    │    FamiliLook AI"   │
     │   │  Speech     │   │                               │                     │
     │   │  bubble     │   │   [E] FEATURE SUB-HEADLINE    │   Feature chips     │
     │   │  "Told you  │   │       "Got Mum's Eyes" pill   │   (secondary        │
     │   │   so!"      │   │                               │    display)         │
     │   │             │   │   [F] SCORE BADGE             │                     │
     │   │             │   │       "72% Mum" gradient pill  │   Brand mark        │
     │   └─────────────┘   │                               │   "famililook.com"  │
     │                     │   [I] BRAND famililook.com     │                     │
     │                     │                               │                     │
1051 ├─────────────────────┼───────────────────────────────┼─────────────────────┤
     │▓▓ BOT SAFE (47px) ▓│    BOT SAFE ZONE (47px)       │▓▓ BOT SAFE (47px) ▓│ y=1063
     │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│                               │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ y=1110
     └─────────────────────┴───────────────────────────────┴─────────────────────┘
  x: 0                  694                             1976                  2670
```

### 2.2 Left Panel — Character Placement

| Property | Value | Notes |
|----------|-------|-------|
| Panel bounds | x: 59, y: 59, w: 576, h: 992 | After safe margins |
| Character bounding box | x: 89, y: 109, w: 506, h: 800 | Centred within panel, leaving breathing room |
| Speech bubble zone | x: 89, y: 59, w: 506, h: 150 | Above character head OR beside head |
| Character anchor point | Bottom-centre of bounding box | Character "stands" at bottom, head is at top |
| Vertical alignment | Bottom-aligned | Character feet at y=909, head grows upward |

**Speech bubble spec:**
- Rounded rectangle: 300x100px, border-radius 40px
- Tail: triangular pointer toward character's mouth
- Background: theme `wash` at 90% opacity
- Text: theme `dark`, 28px bold, max 20 characters
- Placement: upper-right of character, overlapping slightly into centre panel is OK

### 2.3 Centre Panel — Photo and Headline Relationship to Character

The character in the left panel should appear to be PRESENTING the centre panel content:

- **`mama_cheeky` / `papa_cheeky`**: Character's pointing hand extends to x=694 (panel boundary), directing eye toward the headline
- **`mama_proud` / `papa_proud`**: Character faces right (toward centre), body angled ~15 degrees
- Character NEVER overlaps the photo circle or headline text
- A subtle visual connector (dotted line, arrow, or character's extended arm) can bridge the gap between panels

### 2.4 Right Panel — Decorative Character Usage

| Element | Placement |
|---------|-----------|
| Accent character (e.g., `cub_sleeping`) | x: 2036, y: 109, w: 200, h: 300 — upper portion |
| Confetti/stars pattern | Scattered across full right panel, 8% opacity, theme `light` and `primary` |
| Feature chips | Below accent character, centred in panel |
| Brand mark | x: 2036, y: 980, centred in panel bottom |

### 2.5 Prodigi Safe Zones Reminder

| Zone | Pixels | Rule |
|------|--------|------|
| Top bleed (trimmed) | 0-12px | Content will be CUT — no content here |
| Top feather | 12-59px | Content may DISTORT — no critical content |
| Bottom bleed (trimmed) | 1086-1110px | Content will be CUT |
| Bottom feather | 1063-1086px | Content may DISTORT |
| Left handle proximity | 0-59px | May be hidden by handle — no critical content |
| Right handle proximity | 2611-2670px | May be hidden by handle |

---

## 3. SVG TECHNICAL REQUIREMENTS

### 3.1 ViewBox and Artboard

| Property | Value |
|----------|-------|
| Master SVG viewBox | `0 0 300 300` |
| Coordinate system | Origin top-left, y increases downward |
| Units | Unitless (SVG user units), map to px at export |
| Artboard padding | 10 units on all sides (character content within 10,10 to 290,290) |

### 3.2 Layer Naming Convention

Each character SVG must use the following group (`<g>`) naming:

```xml
<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Layer order: back to front -->
  <g id="props-back">         <!-- Props behind character (cushion, chair, etc.) -->
  <g id="body">               <!-- Main body shape -->
  <g id="body-detail">        <!-- Cardigan lines, clothing detail -->
  <g id="arms">               <!-- Both arms -->
  <g id="head">               <!-- Head circle/oval -->
  <g id="hair">               <!-- Hair, bun, curls -->
  <g id="face">               <!-- Eyes, mouth, eyebrows, blush -->
  <g id="glasses">            <!-- Glasses if applicable (hidden by default for non-glasses characters) -->
  <g id="props-front">        <!-- Props in front (tea cup, sign, flowers, etc.) -->
  <g id="occasion-overlay">   <!-- Seasonal props: santa hat, party hat, etc. (hidden by default) -->
  <g id="speech-bubble">      <!-- Speech bubble (separate, positioned outside character for flexibility) -->
</svg>
```

### 3.3 Colour Token Integration

Characters use CSS custom properties for all fills, allowing runtime theme switching:

```xml
<!-- In the SVG, use CSS variables as fill values -->
<style>
  .fill-primary   { fill: var(--fl-primary, #C0364E); }
  .fill-light     { fill: var(--fl-light, #E8637A); }
  .fill-wash      { fill: var(--fl-wash, #FDF0F2); }
  .fill-muted     { fill: var(--fl-muted, #9B6070); }
  .fill-faint     { fill: var(--fl-faint, #C9A0AC); }
  .fill-dark      { fill: var(--fl-dark, #5A2035); }
  .fill-neutral   { fill: var(--fl-neutral, #F5F5F5); }
  .stroke-dark    { stroke: var(--fl-dark, #5A2035); }
  .fill-blush     { fill: var(--fl-light, #E8637A); opacity: 0.4; }
  /* Fixed fills (never change with theme) */
  .fill-eye       { fill: #1A1A1A; }
  .fill-eye-highlight { fill: #FFFFFF; }
  .fill-steam     { fill: none; stroke: var(--fl-faint, #C9A0AC); stroke-width: 2; opacity: 0.6; }
</style>
```

**At render time**, the React component sets CSS custom properties from `mugThemes.js`:

```
Map:
  --fl-primary  ← OCCASION_THEMES[occasion].primary
  --fl-light    ← OCCASION_THEMES[occasion].light
  --fl-wash     ← OCCASION_THEMES[occasion].wash
  --fl-muted    ← OCCASION_THEMES[occasion].muted
  --fl-faint    ← OCCASION_THEMES[occasion].faint
  --fl-dark     ← OCCASION_THEMES[occasion].dark
  --fl-neutral  ← NEUTRAL.chip
```

### 3.4 File Naming Convention

```
characters/
  mama_bear/
    mama_proud.svg
    mama_surprised.svg
    mama_cheeky.svg
    mama_loving.svg
    mama_celebrating.svg
  papa_bear/
    papa_proud.svg
    papa_surprised.svg
    papa_cheeky.svg
    papa_loving.svg
    papa_celebrating.svg
  little_cub/
    cub_happy.svg
    cub_sleeping.svg
    cub_surprised.svg
    cub_giggling.svg
    cub_curious.svg
  mini_me/
    mini_proud.svg
    mini_cheeky.svg
    mini_surprised.svg
    mini_pointing.svg
    mini_celebrating.svg
  gran/
    gran_proud.svg
    gran_surprised.svg
    gran_loving.svg
    gran_showing_off.svg
    gran_laughing.svg
  gramps/
    gramps_proud.svg
    gramps_surprised.svg
    gramps_loving.svg
    gramps_showing_off.svg
    gramps_laughing.svg
  occasion_props/
    santa_hat.svg
    party_hat.svg
    flowers_bouquet.svg
    heart_floating.svg
    balloon_single.svg
    candy_cane.svg
    best_dad_mug.svg
    best_gran_banner.svg
    best_gramps_banner.svg
    elf_hat.svg
    present_box.svg
    christmas_jumper_pattern.svg
```

**Total SVG assets: 30 character variants + 12 occasion props = 42 files**

### 3.5 Accessibility Considerations

Each SVG must include:

```xml
<svg role="img" aria-label="Mama Bear looking proud, holding a cup of tea">
  <title>Mama Bear — Proud</title>
  <desc>An illustrated cartoon bear character with a warm expression, standing confidently with one hand on hip and the other holding a steaming cup of tea. Used on FamiliLook personalised mugs to represent the mother.</desc>
  ...
</svg>
```

- `role="img"` on the root `<svg>` element
- `<title>` with character name and emotion
- `<desc>` with full description for screen readers
- `aria-label` on the `<svg>` element matching the `<title>` content

---

## 4. THEME ADAPTATION MATRIX

### 4.1 What Changes Per Theme

| SVG Class | generic | mothers_day | fathers_day | birthday | heritage_gold | carnival_spirit | ubuntu |
|-----------|---------|-------------|-------------|----------|---------------|-----------------|--------|
| `.fill-primary` (body) | #C0364E | #C0364E | #1A6BB5 | #D97706 | #C8960C | #FF6D00 | #D84315 |
| `.fill-light` (cheeks, accents) | #E8637A | #FF6B9D | #6BA3D4 | #F59E0B | #E8C84A | #FFB74D | #FF8A65 |
| `.fill-wash` (Little Cub body, bg) | #FDF0F2 | #FCEEF2 | #EEF3FB | #FEF3C7 | #FFF8E1 | #FFF3E0 | #FBE9E7 |
| `.fill-muted` (Gran body, text) | #9B6070 | #9B6070 | #5A7A96 | #92400E | #5D4037 | #E65100 | #5D4037 |
| `.fill-faint` (Gran hair, steam) | #C9A0AC | #C9A0AC | #A0B8CC | #D4A574 | #A1887F | #FFCC80 | #BCAAA4 |
| `.fill-dark` (outlines, hair) | #5A2035 | #5A2035 | #1A3A5C | #78350F | #1A0F00 | #1A1A2E | #3E2723 |

### 4.2 What Stays Constant (All Themes)

| Element | Fill | Reason |
|---------|------|--------|
| Eye pupils | #1A1A1A | Must always read as eyes regardless of theme |
| Eye highlights | #FFFFFF | White dot must pop on any colour |
| Speech bubble background | theme `wash` at 90% | Legibility |
| Speech bubble text | theme `dark` | Legibility |
| Outline stroke | theme `dark` | Defines character shape on any background |

### 4.3 Theme Colour Swatches (Visual Reference for Illustrator)

```
GENERIC (Default)
  ████ #C0364E  primary (rose)
  ████ #E8637A  light
  ████ #FDF0F2  wash
  ████ #9B6070  muted
  ████ #C9A0AC  faint
  ████ #5A2035  dark (outlines)

MOTHERS DAY
  ████ #C0364E  primary (rose — same as generic)
  ████ #FF6B9D  light (more pink)
  ████ #FCEEF2  wash
  ████ #9B6070  muted
  ████ #C9A0AC  faint
  ████ #5A2035  dark

FATHERS DAY
  ████ #1A6BB5  primary (steel blue)
  ████ #6BA3D4  light
  ████ #EEF3FB  wash
  ████ #5A7A96  muted
  ████ #A0B8CC  faint
  ████ #1A3A5C  dark

BIRTHDAY
  ████ #D97706  primary (amber)
  ████ #F59E0B  light
  ████ #FEF3C7  wash
  ████ #92400E  muted
  ████ #D4A574  faint
  ████ #78350F  dark

HERITAGE GOLD
  ████ #C8960C  primary (kente gold)
  ████ #E8C84A  light
  ████ #FFF8E1  wash
  ████ #5D4037  muted (warm cocoa)
  ████ #A1887F  faint
  ████ #1A0F00  dark (deep umber)

CARNIVAL SPIRIT
  ████ #FF6D00  primary (carnival orange)
  ████ #FFB74D  light
  ████ #FFF3E0  wash
  ████ #E65100  muted
  ████ #FFCC80  faint
  ████ #1A1A2E  dark (deep navy)

UBUNTU
  ████ #D84315  primary (ndebele terracotta)
  ████ #FF8A65  light
  ████ #FBE9E7  wash
  ████ #5D4037  muted (earth brown)
  ████ #BCAAA4  faint
  ████ #3E2723  dark (dark earth)
```

### 4.4 Planned Additional Themes (Not Yet in mugThemes.js)

These are specified in the CMO brief for future addition. Illustrator should be aware but these are NOT immediate priority:

| Theme | Primary | Dark | Notes |
|-------|---------|------|-------|
| Christmas | #B71C1C | #4A0000 | December gifting |
| Valentine's | #AD1457 | #560027 | February, pairwise mode |

---

## 5. SIZE VARIANTS

Characters must render cleanly at 4 sizes. The master 300x300 SVG scales to all.

### 5.1 Full Size — Left Panel Hero

| Property | Value |
|----------|-------|
| Context | Left panel of mug wrap template |
| Rendered size | ~506 x 800px within the 576x992px usable panel area |
| SVG scaling | viewBox 300x300 scaled to fit height, centred horizontally |
| Outline weight at this size | ~13px effective (8px at 300 master, scaled up ~1.6x proportional to width, but outline scales with viewBox) |
| Detail level | Full detail visible — speech bubble text readable, props clear, facial expression clear |
| Key test | Can you read the speech bubble text at arm's length on a physical mug? Target: 28px print text = ~9mm tall |

### 5.2 Medium — Right Panel Accent

| Property | Value |
|----------|-------|
| Context | Right panel decorative accent (e.g., `cub_sleeping`) |
| Rendered size | ~200 x 300px |
| SVG scaling | viewBox 300x300 scaled to 200px wide |
| Outline weight at this size | ~5px effective |
| Detail level | Expression and prop recognisable, but fine detail (cardigan buttons, steam wiggles) may merge — that is OK |
| Key test | Is the character immediately recognisable as "a sleeping baby" at a glance? |

### 5.3 Small — Feature Badge Companion

| Property | Value |
|----------|-------|
| Context | Next to a feature chip or as a list bullet |
| Rendered size | ~80 x 80px |
| SVG scaling | viewBox 300x300 scaled to 80px |
| Outline weight at this size | ~2px effective |
| Detail level | Character silhouette and colour only. Expression may not be legible. Props may not be distinguishable. |
| Key test | Is the silhouette instantly "bear character" and not a blob? |
| Design implication | At this size, character should be recognisable from SILHOUETTE ALONE. Ensure the silhouette of each character is distinct (Mama = bun on head, Papa = broad shoulders, Cub = huge head on cushion, Mini Me = spiky hair + backpack, Gran/Gramps = armchair shape). |

### 5.4 Thumbnail — Product Grid

| Property | Value |
|----------|-------|
| Context | Product selection grid, cart icon, TikTok Shop thumbnail |
| Rendered size | ~40 x 40px |
| SVG scaling | viewBox 300x300 scaled to 40px |
| Outline weight at this size | ~1px effective |
| Detail level | Colour blob with recognisable shape only. No text, no detail. |
| Key test | Does it look intentional or does it look like a rendering error? |
| Design implication | At 40px, only the HEAD of the character should be visible. Consider providing a `_head` variant (viewBox cropped to head only: `100 20 100 100`) for thumbnail use. |

### 5.5 Head-Only Variant

For thumbnail and small contexts, provide a head-only crop for each character:

```
characters/
  mama_bear/
    mama_head.svg          ← viewBox cropped to head area only
  papa_bear/
    papa_head.svg
  little_cub/
    cub_head.svg
  mini_me/
    mini_head.svg
  gran/
    gran_head.svg
  gramps/
    gramps_head.svg
```

**Head-only SVG spec:**
- viewBox: cropped to include head, hair, and face only (approx `50 0 200 180` from master)
- Include: head shape, hair, eyes, mouth, glasses (if applicable), blush
- Exclude: body, arms, legs, props, speech bubble
- Total: 6 additional SVGs

**Revised total: 42 character/prop files + 6 head-only files = 48 SVG assets**

---

## 6. CHARACTER INTERACTION POSES

### 6.1 Pointing at Headline

**Characters**: `mama_cheeky`, `papa_cheeky`, `mini_pointing`

```
  Character                 Headline
  ┌──────────┐
  │          ├──── arm extends ────→  MUMMY'S MINI ME
  │  :)  *   │                        ~~~~~~~~~~~~~~~~
  │  /|\     │
  │  / \     │
  └──────────┘
```

- The pointing arm extends to the RIGHT edge of the character bounding box (x=290 in master SVG)
- At full mug render, the arm tip aligns with x=694 (left panel right edge)
- The arm is a simple tapered rectangle, ending in a mitten hand with index finger extended (one rounded protrusion from the mitten)
- Angle: ~15 degrees above horizontal, pointing up-right toward where headline sits

### 6.2 Holding a Sign/Banner

**Characters**: `gran_showing_off`, `gramps_showing_off`

```
  ┌──────────────────────────────┐
  │  "BEST GRAN EVER"           │  ← banner
  └──────────┬───────────────────┘
             │
         ┌───┴───┐
         │  :D   │  ← character holds banner above head
         │  /|\  │
         │  / \  │
         └───────┘
```

- Banner is a separate `<g>` within `props-front` layer
- Banner dimensions: 240 x 60 units in master SVG (positioned above head)
- Banner shape: rounded rectangle, fill: theme `wash`, border: 2px theme `primary`
- Banner text: theme `dark`, 24 unit font size, centred
- Character's arms raise upward to hold banner corners

### 6.3 Reacting to Percentage

| Percentage Range | Character Emotion | Speech Bubble Text |
|------------------|-------------------|--------------------|
| 75-100% | `_proud` or `_celebrating` | "Told you so!" / "Obviously!" / "No surprise there!" |
| 65-74% | `_proud` | "Yep, that's mine!" / "I can see it!" |
| 55-64% | `_cheeky` | "Just about!" / "Close one!" |
| 51-54% | `_surprised` | "Hmm, barely..." / "That was close!" / "Phew!" |

Speech bubble text is selected randomly from the pool matching the percentage bracket.

### 6.4 Standing Next to Photo Frame

**Characters**: Any full-size character in left panel

```
  ┌──────────┐   gap   ┌────────────────┐
  │          │  24px   │    ○           │
  │  Character│ ←───→  │   Photo        │
  │          │         │    circle      │
  │          │         │                │
  └──────────┘         └────────────────┘
  LEFT PANEL            CENTRE PANEL
```

- Minimum 24px gap (at print resolution) between character right edge and centre panel photo
- Character should be looking RIGHT (toward the photo/headline)
- Character's body is angled 10-15 degrees toward centre (not facing directly forward)

### 6.5 Speech Bubble Positions

**Three valid positions** (the React component selects based on available space):

```
Position A: Upper-right          Position B: Upper-left         Position C: Right-middle
(default for left panel)         (for right panel accent)       (for compact layout)

    ┌───────────┐                   ┌───────────┐
    │  text     │                   │  text     │                     ┌───────────┐
    └─────┬─────┘                   └─────┬─────┘                     │  text     │
          │                               │                       ┌───┤           │
     ┌────┴──┐                       ┌────┴──┐               ┌────┴──┐└───────────┘
     │ char  │                       │ char  │               │ char  │
     └───────┘                       └───────┘               └───────┘
```

**Speech bubble SVG spec:**
- Shape: rounded rectangle, border-radius 20 units
- Tail: 15-unit equilateral triangle pointing toward character's head
- Padding: 12 units inside
- Min width: 100 units, max width: 220 units
- Max text: 20 characters (enforced by React component, not SVG)
- Font: bold, 20 units, theme `dark` fill
- Background: theme `wash` at 90% opacity
- Border: 1.5 units, theme `light`

---

## 7. REFERENCE IMAGERY DIRECTION

### 7.1 What the Style IS Like

| Reference | What to Take From It |
|-----------|---------------------|
| **Mr. Men / Little Miss** (Roger Hargreaves) | Simple geometric body shapes. Each character is a single shape (circle, rectangle, triangle) with arms, legs, and a face. Instantly recognisable silhouettes. Bold flat colour fills. Thick outlines. |
| **Cornish Prints UK** (TikTok mug brand) | Bold, funny, hand-drawn characters on mugs. Simple enough to read at arm's length. Characters FRAME a funny text headline. The character is the supporting act, the text is the star. |
| **Duolingo owl** | Expressive with minimal features. Huge eyes, simple beak, flat colours. Emotion conveyed through eye shape and body position, not facial detail. Friendly and warm, never threatening. |
| **Pusheen** (cat character) | Rounded, squishy proportions. Short limbs. Large head relative to body. Simple dot eyes with expression in the brow/cheek. Props (food, cushions) are as characterful as the character itself. |
| **Molang** (Korean rabbit) | Maximum cuteness from minimum lines. Dot eyes, pink cheeks, bean body. The simplicity IS the appeal. |

### 7.2 What the Style is NOT Like

| Anti-Reference | Why NOT |
|----------------|---------|
| **Realistic illustration** | Characters must be CARTOONS. No anatomical accuracy, no realistic proportions, no shading/lighting. Real photos handle identity. |
| **Anime/manga** | No large detailed eyes with iris/pupil/highlight detail. No pointy chins. No dramatic hair. Too complex for mug readability. |
| **Clip art** | No thin lines, no gradients, no 3D effects, no dated Microsoft Office energy. Must feel contemporary and designed, not stock. |
| **Corporate mascots** | No suits, no ties, no "business bear". These are FAMILY characters — warm, domestic, cosy. |
| **Pixar/Disney 3D** | No 3D rendering, no complex lighting, no subsurface scattering. Flat 2D only. |
| **South Park / Family Guy** | No edge, no adult humour visual cues, no crude shapes. Family-friendly always. |

### 7.3 Line Quality

- **Weight**: Uniform stroke width throughout. No thick-to-thin variation (not brush-like).
- **Endpoints**: Round cap (`stroke-linecap: round`), round join (`stroke-linejoin: round`)
- **Corners**: All corners rounded. No sharp angles on body shapes.
- **Confidence**: Lines are decisive and clean. No sketchy double-lines or wobbly hand-drawn effect.
- **Colour**: Always theme `dark` token. Never coloured outlines, never no-outline.

### 7.4 Fill Style

- **Flat fills only**: No gradients within shapes. No textures. No patterns within fills.
- **Opacity**: Most fills at 100%. Blush cheeks at 40%. Steam at 60%. Decorative elements at 8%.
- **White space**: Characters do NOT fill their entire bounding box. Generous padding around the character creates breathing room. Target: character occupies 70-75% of the 300x300 artboard.

### 7.5 Emotion Conveyed Through

| Method | Example | Priority |
|--------|---------|----------|
| **Eye shape** | Happy = squished arcs. Surprised = large circles. Cheeky = one eye smaller (wink). | Highest — eyes are the primary expression tool |
| **Mouth shape** | Smile = upward arc. Surprised = O shape. Cheeky = asymmetric curve. | High |
| **Body position** | Proud = upright, chest out. Surprised = leaning back. Celebrating = arms up. | Medium |
| **Eyebrow angle** | Proud = slight raise. Surprised = high arch. Cheeky = one up, one down. | Medium |
| **Prop position** | Tea cup raised = celebrating. Tea cup down = relaxed. Tea sloshing = laughing. | Supporting |
| **Head tilt** | Curious = tilted 15 degrees. Loving = tilted 10 degrees toward other character. | Supporting |

---

## 8. DELIVERABLE CHECKLIST

The illustrator should deliver:

- [ ] **30 character emotion SVGs** (5 characters x 5 emotions + Gran/Gramps split = 30)
- [ ] **6 head-only SVGs** (1 per character, Gran + Gramps separate)
- [ ] **12 occasion prop SVGs** (santa hat, party hat, flowers, heart, balloon, candy cane, best dad mug, best gran banner, best gramps banner, elf hat, present box, christmas jumper pattern)
- [ ] All SVGs use CSS custom properties for fills (as specified in Section 3.3)
- [ ] All SVGs use the layer naming convention (Section 3.2)
- [ ] All SVGs include accessibility markup (Section 3.5)
- [ ] All SVGs fit within 300x300 viewBox
- [ ] Characters are recognisable as silhouettes at 40x40px (Section 5.4)
- [ ] Speech bubble text area is separate and content-agnostic (text injected at runtime)
- [ ] Occasion props are separate SVG files that can be composited onto any emotion variant
- [ ] All files follow the naming convention in Section 3.4

**Total deliverable count: 48 SVG files**

---

## 9. PRODUCTION NOTES

### File Size Targets

| SVG | Target File Size | Notes |
|-----|-----------------|-------|
| Character emotion (full) | < 8 KB | Simple shapes = small files. If over 8KB, simplify paths. |
| Head-only | < 3 KB | Subset of full character |
| Occasion prop | < 4 KB | Simple single-object shapes |
| Total bundle | < 300 KB | All 48 files. Loaded lazily per character selection. |

### Path Optimisation

- Use `<circle>`, `<rect>`, `<ellipse>` primitives where possible (smaller than `<path>`)
- Run through SVGO (SVG Optimizer) with preset-default, keeping `viewBox` and `id` attributes
- Remove any editor metadata (Illustrator, Figma, Inkscape comments)
- No embedded fonts — all text is injected at runtime by React
- No embedded images — pure vector only

### Colour Validation

Before final delivery, the illustrator should render each character against ALL 7 theme palettes and verify:
1. Character outline is always visible against transparent (white ceramic) background
2. Fill colours have sufficient contrast with outline colour
3. Eye pupils are always visible against any head fill colour
4. Speech bubble text is always readable against bubble background
5. Blush cheeks are visible but subtle on any primary fill

---

*This brief was produced by the Visual Director agent. No source code files were modified. Implementation of the character SVGs and their integration into the CharacterMugTemplate is a Phase 1 deliverable per the CMO roadmap.*

*Next actions:*
1. *Illustrator receives this brief and produces 48 SVG assets*
2. *FE Lead receives assets and builds CharacterMugTemplate.jsx*
3. *Copywriter provides speech bubble text pools for each percentage bracket*
