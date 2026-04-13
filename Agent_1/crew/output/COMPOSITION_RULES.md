===============================================
  VISUAL DIRECTION — Character Mug Composition Rules
===============================================

PRODUCT: FamiliLook Character Mug (Prodigi GLOBAL-MUG-W, 11oz white ceramic)
PRINT TARGET: 2670 x 1110px @ 300 DPI, transparent PNG on white ceramic
CSS CANVAS: 830 x 345px (3.217x pixelRatio for export)
CONTEXT: Physical ceramic mug — viewed at arm's length (~50cm), held in one hand
DATE: 30 March 2026
STATUS: AWAITING CEO APPROVAL — no code changes until signed off

---

## 1. DESIGN PHILOSOPHY

The product celebrates the bond between parent and child. Every composition
must answer three questions within 3 seconds:

1. WHO is this about? (child's name / photo)
2. WHAT happened? (they look like Mum/Dad)
3. WHY should I care? (it's personal, warm, funny, gift-worthy)

If any composition feels generic — like it could be for anyone — it has failed.
If it feels clinical — like a lab report — it has failed. The mug is a keepsake,
a conversation starter, a gift someone photographs and shares.

---

## 2. CANVAS DIMENSIONS & SAFE AREAS

All measurements in CSS pixels unless stated otherwise. Multiply by 3.217 for print.

```
Full canvas:    830 x 345 px (CSS)
                2670 x 1110 px (print @ 300 DPI)

Safe margins:
  Top:          18px CSS  (59px print) — Prodigi feather zone (5mm)
  Bottom:       15px CSS  (47px print) — Prodigi feather zone (4mm)
  Left edge:    18px CSS  (59px print) — handle proximity
  Right edge:   18px CSS  (59px print) — handle proximity

Usable area:   794 x 312 px CSS  (2552 x 1004 px print)
```

**Visible face zone**: The customer sees roughly 40% of the wrap when looking
straight at the mug. The emotional centrepiece MUST sit in the central 35% of
the wrap width (x: 270–560 CSS, approximately 290px wide) so it is fully
readable without rotating the mug.

---

## 3. ELEMENT LIBRARY

Every element that CAN appear on the Character Mug, with exact specifications.

### 3.1 Character Illustration (Primary)

| Property | Value |
|----------|-------|
| Type | Standing parent: mama, papa. Standing child: mini. Infant: cub. Seated: gran, gramps (in armchairs) |
| Format | PNG, transparent background, pre-rendered illustration |
| CSS height | 290px (standing characters), 260px (seated gran/gramps — armchair adds width, not height) |
| CSS max-width | Standing: 280px. Seated: 320px (armchair is wider than standing figure) |
| Print height | ~933px (standing), ~836px (seated) |
| Alignment | Bottom-aligned to canvas bottom (feet/chair base at y=345 minus bottom safe = y=330) |
| Horizontal pos | Left-anchored or right-anchored depending on layout |
| Visual weight | HIGH |
| Overflow | Character may bleed 18px into adjacent panel (CHAR_OVERLAP) |
| Object-fit | `contain`, `object-position: bottom center` |
| Variants | 2 per character: default (Caucasian), african. Same pose, different illustration. SAME position and size rules. |

**Emotions available per character:**

| Character | Emotions | Default |
|-----------|----------|---------|
| mama | proud, surprised, cheeky, celebrating, loving | proud |
| papa | proud, surprised, cheeky, celebrating, loving | proud |
| cub | happy, sleeping, surprised, giggling, curious | happy |
| mini | proud, cheeky, surprised, celebrating | proud |
| gran | proud, surprised, loving, showing_off, laughing | proud |
| gramps | proud, surprised, loving, showing_off, laughing | proud |

**Emotion remapping rules** (gran/gramps/cub don't have all emotions):
- gran/gramps + "cheeky" -> "showing_off"
- cub + "celebrating" -> "giggling"
- cub + "cheeky" -> "curious"

### 3.2 Hero Headline

| Property | Value |
|----------|-------|
| Content | 1-2 lines, ALL CAPS, max 35 characters (excl. newlines). Selected by headline engine from 60+ options. |
| Font | Nunito, 900 weight (Black) |
| CSS font-size | 42px (no photo), 36px (with photo), 32px (with occasion header) |
| Print font-size | ~135px / ~116px / ~103px |
| Line height | 0.92 (tight — headline reads as a block) |
| Letter spacing | -0.02em |
| Colour | Theme dark token (e.g. #5A2035 for generic/mothers_day) |
| Text transform | uppercase |
| Max width | Panel width minus padding |
| Visual weight | HIGHEST — this is what the viewer reads first |
| Wrapping | `white-space: pre-line` — newlines in headline data are honoured |

### 3.3 Child's Name

| Property | Value |
|----------|-------|
| Content | Child's first name, max 20 characters. All caps or title case depending on format. |
| Font | Nunito, 700 weight |
| CSS font-size | 14px (standalone), integrated into headline when using `{child}` template |
| Print font-size | ~45px |
| Colour | Theme primary token |
| Letter spacing | 0.04em |
| Visual weight | MEDIUM |
| Formats | "standalone" — rendered as separate element below or above headline. "in_headline" — baked into headline text via `{child}` template. "in_score" — appended to score line. |
| Fallback | If childName is empty/null, element is omitted entirely. Layout reclaims space. |

### 3.4 Child's Photo

| Property | Value |
|----------|-------|
| Content | Circular crop of uploaded child photo |
| CSS size | 56px diameter (standard), 44px (compact), 72px (large/celebration layout) |
| Print size | ~180px / ~142px / ~232px diameter |
| Shape | Circle (`border-radius: 50%`) |
| Border | 2px solid, theme primary colour |
| Object-fit | `cover` |
| Visual weight | HIGH (draws the eye — it's a real face) |
| Fallback | If childPhoto is null, element is omitted. Layout reclaims space — headline may enlarge, score may move up. |

### 3.5 Score Line

| Property | Value |
|----------|-------|
| Content | "{pct}% {winnerLabel} . Got {winnerLabel}'s {feature}" — single line |
| Font | Nunito, 700 weight |
| CSS font-size | 12px |
| Print font-size | ~39px |
| Colour | Theme primary token |
| Letter spacing | 0.02em |
| Overflow | `text-overflow: ellipsis`, `white-space: nowrap` |
| Visual weight | MEDIUM |
| Formats | "prominent" — full size, below headline. "subtle" — 10px, muted colour. "hidden" — omitted (occasion layouts may hide). |

### 3.6 Feature Callout

| Property | Value |
|----------|-------|
| Content | "GOT MUM'S EYES" or similar — from feature sub-headline bank |
| Font | Nunito, 600 weight |
| CSS font-size | 10px |
| Print font-size | ~32px |
| Colour | Theme primary, 80% opacity |
| Max length | 50 characters |
| Visual weight | LOW-MEDIUM |
| Usage | Adds personality. Complements headline. Optional in compact layouts. |

### 3.7 Speech Bubble

| Property | Value |
|----------|-------|
| Content | Short quip: "TOLD YOU SO!", "I KNEW IT!", etc. Max ~20 chars. |
| CSS dimensions | Auto width, max 100px. Padding: 2px 6px |
| Font | Nunito, 700 weight, 6.5px |
| Print font-size | ~21px |
| Background | #FFFFFF |
| Border | 1.5px solid, theme primary |
| Border radius | 8px |
| Tail | CSS triangle, 4px, pointing down-left toward character's head |
| Position | Near top-right of character panel, overlapping character illustration |
| z-index | 3 (above character) |
| Visual weight | LOW (decorative, adds humour) |
| Fallback | Omitted if layout is "blend" or "gift" with formal occasion |

### 3.8 Occasion Tag

| Property | Value |
|----------|-------|
| Content | "HAPPY MOTHER'S DAY", "HAPPY BIRTHDAY OLIVIA", etc. Max 30 chars. |
| Font | Nunito, 600 weight |
| CSS font-size | 11px |
| Print font-size | ~35px |
| Colour | Theme primary |
| Letter spacing | 0.08em |
| Text transform | uppercase |
| Position | Top of content panel, above headline |
| Visual weight | MEDIUM |
| Usage | Only when occasion is set and not "generic". Displaces headline downward. |

### 3.9 Second Character (Loser/Reactor)

| Property | Value |
|----------|-------|
| Type | The non-winning parent character, or complementary character |
| CSS height | 200px (smaller than primary — it's the reactor, not the hero) |
| CSS max-width | 200px |
| Alignment | Opposite side from primary character |
| Emotion | "surprised" (high win), "cheeky" (medium win), matched to primary for blend |
| Visual weight | MEDIUM |
| Usage | Blend layout (both parents flanking), or humorous reaction in high-win scenarios |

### 3.10 Brand Mark

| Property | Value |
|----------|-------|
| Content | "famililook.com" |
| Font | system-ui, 300 weight |
| CSS font-size | 5.5px |
| Print font-size | ~18px |
| Colour | Theme faint token, 45% opacity |
| Position | Absolute bottom-right of canvas, 8px up, 14px in |
| Letter spacing | 0.12em |
| Visual weight | LOWEST — must be present but nearly invisible |
| Required | ALWAYS present on every layout |

### 3.11 Accent Bands (Top + Bottom)

| Property | Value |
|----------|-------|
| CSS height | 2px each |
| Print height | ~6px |
| Background | Gradient: transparent 10% -> theme light 60% opacity 30% -> theme primary 50% -> theme light 60% opacity 70% -> transparent 90% |
| Position | Absolute top: 0 and bottom: 0, full width |
| Visual weight | LOWEST — subtle framing only |
| Required | ALWAYS present on every layout |

---

## 4. LAYOUT VARIANT SPECIFICATIONS

Four layout templates. The composition engine selects one based on inputs.
All layouts share the same 830x345px CSS canvas with transparent background.

### 4.1 Layout A: "Hero" — Character + Bold Headline

**When selected**: Decisive wins (65%+), playful tone, no occasion set, generic gift.
**Element count**: 5-6

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [accent band - 2px]                                                                 │
├────────────────────────────┬────────────────────────────────────────────────────────┤
│                            │                                                        │
│                            │   [HERO HEADLINE]           <- 42px (no photo)         │
│                            │   "MUMMY'S                     36px (with photo)       │
│     [CHARACTER]            │    MINI ME"                                             │
│     mama_proud             │                                                        │
│     290px tall             │   [SCORE LINE]              <- 12px                    │
│     bottom-aligned         │   "72% Mum . Got Mum's Eyes"                           │
│                            │                                                        │
│     [SPEECH BUBBLE]        │   [CHILD PHOTO]             <- 56px circle (if exists) │
│     top-right of char      │                                                        │
│                            │                           [brand] famililook.com        │
├────────────────────────────┴────────────────────────────────────────────────────────┤
│ [accent band - 2px]                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

LEFT PANEL:  40% width = 332px CSS / 1068px print
RIGHT PANEL: 60% width = 498px CSS / 1602px print
Character overlap into right: 18px
```

**Right panel padding**: 24px top, 28px right, 20px bottom, 32px left (CSS)

**Element stack (top to bottom in right panel)**:
1. Hero headline (flex: auto)
2. Score line (12px gap below headline)
3. Child photo (12px gap below score, only if exists)
4. Brand mark (absolute positioned, bottom-right)

**Visual hierarchy**:
1. Hero headline (largest text, dark colour, first read)
2. Character illustration (large visual, draws the eye)
3. Score line (supporting data)
4. Child photo (personal touch, if present)
5. Speech bubble (humour layer)
6. Brand mark (barely visible)

### 4.2 Layout B: "Celebration" — Character + Child Identity Centre Stage

**When selected**: Gift for a specific person, childName AND childPhoto both present, moderate win (55-69%), personal/warm tone.
**Element count**: 6-7

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [accent band - 2px]                                                                 │
├──────────────────┬──────────────────────────────────────────┬────────────────────────┤
│                  │                                          │                        │
│                  │   [CHILD NAME]        <- 14px, primary   │                        │
│                  │   "OLIVIA"                                │                        │
│                  │                                          │                        │
│   [CHARACTER]    │   [CHILD PHOTO]       <- 72px circle     │   [FEATURE CALLOUT]   │
│   mama_proud     │                                          │   "Got Mum's Eyes"    │
│   260px tall     │   [HERO HEADLINE]     <- 32px            │   10px, rotated -3deg │
│   bottom-aligned │   "MUMMY'S MINI ME"                      │                        │
│                  │                                          │   [SCORE LINE]         │
│                  │   [SCORE LINE]        <- 10px, subtle    │   subtle, 10px         │
│                  │                                          │                        │
│                  │                      [brand]              │                        │
├──────────────────┴──────────────────────────────────────────┴────────────────────────┤
│ [accent band - 2px]                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

LEFT PANEL:   30% = 249px CSS — character
CENTRE PANEL: 45% = 373px CSS — child identity + headline
RIGHT PANEL:  25% = 208px CSS — supporting detail
```

**Visual hierarchy**:
1. Child photo (real face, centre of canvas, draws the eye)
2. Child name (directly above photo)
3. Hero headline (below photo, medium size)
4. Character illustration (supporting — the character celebrates the child)
5. Feature callout (bonus detail, right side)
6. Score line (subtle)
7. Brand mark

### 4.3 Layout C: "Blend" — Two Characters Flanking Central Message

**When selected**: Close call (51-59%), blend/unknown winner, "best of both" messaging.
**Element count**: 5-6

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [accent band - 2px]                                                                 │
├──────────────┬──────────────────────────────────────────────────┬────────────────────┤
│              │                                                  │                    │
│              │   [HERO HEADLINE]            <- 36px             │                    │
│              │   "THE PERFECT                                   │                    │
│  [CHAR A]    │    BLEND"                                        │  [CHAR B]          │
│  mama_proud  │                                                  │  papa_surprised    │
│  240px tall  │   [CHILD NAME]               <- 14px (if exists) │  240px tall        │
│              │   "OLIVIA"                                       │                    │
│              │                                                  │                    │
│              │   [SCORE LINE]               <- 10px, subtle     │                    │
│              │   "53% Mum . 47% Dad"                            │                    │
│              │                                                  │                    │
│              │                  [brand]                          │                    │
├──────────────┴──────────────────────────────────────────────────┴────────────────────┤
│ [accent band - 2px]                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

LEFT PANEL:   25% = 208px CSS — character A (winner parent)
CENTRE PANEL: 50% = 414px CSS — headline + child identity
RIGHT PANEL:  25% = 208px CSS — character B (other parent)
```

**Character sizing in Blend**: Both characters are 240px tall (smaller than Hero's 290px)
to give the central message breathing room. Both bottom-aligned.

**Visual hierarchy**:
1. Hero headline (centre, largest text)
2. Character A — mama/papa (left)
3. Character B — papa/mama (right, mirrored position)
4. Child name (supporting, below headline)
5. Score line (subtle — blend messages de-emphasise the score)
6. Brand mark

### 4.4 Layout D: "Gift" — Occasion Header + Personal Message

**When selected**: Occasion is set (mothers_day, fathers_day, birthday, christmas, valentines, grandparents_day), OR recipient is grandparent.
**Element count**: 6-7

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [accent band - 2px]                                                                 │
├──────────────────┬──────────────────────────────────────────────────────────────────┤
│                  │   [OCCASION HEADER]      <- 11px, primary, tracking 0.08em       │
│                  │   "HAPPY MOTHER'S DAY"                                           │
│                  │   ──────────────────     <- 1px rule, 60% width, primary 30%     │
│                  │                                                                  │
│   [CHARACTER]    │   [CHILD NAME]           <- 14px (if exists)                     │
│   mama_proud     │   "OLIVIA"                                                       │
│   or gran_proud  │                                                                  │
│   260px tall     │   [HERO HEADLINE]        <- 32px (smaller — room for occasion)   │
│   bottom-aligned │   "MUMMY'S MINI ME"                                              │
│                  │                                                                  │
│                  │   [SCORE LINE]           <- 10px, subtle                         │
│                  │                                                                  │
│                  │   [CHILD PHOTO]          <- 44px circle (compact)                │
│                  │                                                                  │
│                  │                         [brand]                                   │
├──────────────────┴──────────────────────────────────────────────────────────────────┤
│ [accent band - 2px]                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

LEFT PANEL:  35% = 291px CSS — character
RIGHT PANEL: 65% = 539px CSS — occasion header + content stack
```

**Right panel vertical stack** (top to bottom):
1. Occasion header (11px, uppercase, tracked)
2. Thin rule separator (1px, theme primary at 30% opacity, 60% of panel width)
3. Child name (14px, if exists)
4. Hero headline (32px — reduced to make room for occasion header)
5. Score line (10px, subtle)
6. Child photo (44px, compact — if exists)
7. Brand mark (absolute bottom-right)

**Visual hierarchy**:
1. Occasion header (establishes context — "this is a Mother's Day gift")
2. Hero headline (the message)
3. Character illustration (celebratory tone)
4. Child name (personal touch)
5. Child photo (if present)
6. Score line (supporting)
7. Brand mark

---

## 5. SPACING & BREATHING ROOM RULES

### 5.1 Minimum Gaps (CSS pixels)

| Between | Minimum gap | Notes |
|---------|-------------|-------|
| Headline and score line | 10px | Core reading flow — keep tight |
| Score line and photo | 12px | Separation between text and image |
| Headline and occasion header | 8px | Including thin rule (1px + 4px padding each side) |
| Character and panel edge | 0px | Characters can touch/bleed panel boundaries |
| Character and adjacent text | 18px (CHAR_OVERLAP) | Character overlaps but text has padding |
| Any text and canvas edge | 18px minimum | Safe area enforcement |
| Photo and any text below | 8px | Breathing room under circular photo |
| Feature callout and other text | 6px | Small element, tight is fine |
| Speech bubble and character top | 6px | Bubble should float near head |
| Brand mark and bottom edge | 8px | Above bottom safe area |
| Brand mark and right edge | 14px | Clear of right safe area |
| Accent band and nearest content | 16px (top), 13px (bottom) | Band + safe area combined |

### 5.2 Panel Padding (CSS pixels)

| Panel | Top | Right | Bottom | Left |
|-------|-----|-------|--------|------|
| Hero right panel | 24 | 28 | 20 | 32 |
| Celebration centre panel | 20 | 16 | 16 | 16 |
| Celebration right panel | 24 | 18 | 16 | 12 |
| Blend centre panel | 20 | 20 | 16 | 20 |
| Gift right panel | 16 | 24 | 16 | 28 |

### 5.3 Typography Minimum Sizes for Arm's Length Readability

These are absolute minimums for the physical mug. Below these, text is unreadable at arm's length on a curved ceramic surface.

| Element | Min CSS px | Min print px | Approx. physical mm |
|---------|-----------|-------------|-------------------|
| Hero headline | 28px | 90px | ~7.6mm cap height |
| Child name | 12px | 39px | ~3.3mm |
| Score line | 9px | 29px | ~2.4mm |
| Feature callout | 9px | 29px | ~2.4mm |
| Occasion header | 10px | 32px | ~2.7mm |
| Speech bubble | 6px | 19px | ~1.6mm (acceptable — decorative, not essential reading) |
| Brand mark | 5px | 16px | ~1.4mm (intentionally small — branding, not content) |

---

## 6. VISUAL HIERARCHY BY SCENARIO

Visual hierarchy = what the viewer sees FIRST, SECOND, THIRD when glancing at the mug.

### 6.1 Decisive Win (70%+)

| Rank | Element | Why |
|------|---------|-----|
| 1 | Hero headline | "MUMMY'S MINI ME" — bold, large, instant message |
| 2 | Character | Mama celebrating — emotional resonance |
| 3 | Score line | "78% Mum" — the proof |
| 4 | Speech bubble | "TOLD YOU SO!" — humour layer |
| 5 | Child photo | Personal anchor (if present) |
| 6 | Brand | Nearly invisible |

**Layout**: Hero (A)

### 6.2 Moderate Win (60-69%)

| Rank | Element | Why |
|------|---------|-----|
| 1 | Child photo | Real face draws the eye — this is personal |
| 2 | Child name | "OLIVIA" — establishes who this is about |
| 3 | Hero headline | Warm message, medium size |
| 4 | Character | Proud pose — supportive, not dominant |
| 5 | Feature callout | "Got Mum's Eyes" — nice detail |
| 6 | Score line | Subtle |
| 7 | Brand | Nearly invisible |

**Layout**: Celebration (B) if childPhoto+childName exist, otherwise Hero (A)

### 6.3 Close Call (51-59%)

| Rank | Element | Why |
|------|---------|-----|
| 1 | Hero headline | "THE PERFECT BLEND" — unity message dominates |
| 2 | Character A (left) | Both parents share the stage |
| 3 | Character B (right) | Equality of presence |
| 4 | Child name | "OLIVIA" — who the blend is |
| 5 | Score line | Very subtle — don't emphasise the margin |
| 6 | Brand | Nearly invisible |

**Layout**: Blend (C)

### 6.4 Seasonal Gift (any percentage)

| Rank | Element | Why |
|------|---------|-----|
| 1 | Occasion header | "HAPPY MOTHER'S DAY" — context first |
| 2 | Hero headline | The personalised message |
| 3 | Character | Celebratory emotion |
| 4 | Child name | Personal touch |
| 5 | Child photo | (compact) |
| 6 | Score line | Subtle — gift tone, not data tone |
| 7 | Brand | Nearly invisible |

**Layout**: Gift (D)

---

## 7. COMPOSITION CAPS

### 7.1 Maximum Elements Per Layout

**Hard cap: 7 elements maximum on any single mug layout.**

Accent bands and brand mark are always present and do not count toward the cap
(they are structural/mandatory, not compositional choices).

| Layout | Max elements (excl. bands + brand) | Typical count |
|--------|-----------------------------------|---------------|
| Hero (A) | 5 | 4-5 |
| Celebration (B) | 7 | 6-7 |
| Blend (C) | 5 | 4-5 |
| Gift (D) | 7 | 5-7 |

### 7.2 Minimum Required Elements Per Layout

**Every layout MUST include AT MINIMUM:**

| Element | Required? | Notes |
|---------|-----------|-------|
| Character illustration (primary) | YES | Always. Defines the product. |
| Hero headline | YES | Always. The core message. |
| Score line | YES (can be "subtle" or "hidden" format) | In blend/gift layouts, may be de-emphasised but present. |
| Brand mark | YES | Always. Non-negotiable. |
| Accent bands | YES | Always. Top and bottom. |

**Total minimum**: 3 compositional elements (character + headline + score) plus 2 structural (brand + bands) = 5 rendered items.

### 7.3 Optional Elements (composition engine decides)

| Element | Included when... |
|---------|-----------------|
| Child name | `childName` is not null/empty |
| Child photo | `childPhoto` is not null/empty |
| Speech bubble | Layout is Hero or Celebration, and tone is playful |
| Occasion header | `occasion` is not "generic" |
| Feature callout | Layout is Celebration or Gift, and there's room |
| Second character | Layout is Blend only |

---

## 8. GRACEFUL DEGRADATION

### 8.1 When childPhoto Is Missing

| Layout | Adaptation |
|--------|-----------|
| Hero (A) | Photo element removed. Headline enlarges: 42px -> 48px. Score line moves up. More breathing room. |
| Celebration (B) | Falls back to Hero (A) layout — Celebration layout requires photo as its centrepiece. |
| Blend (C) | No change — Blend layout does not use photo. |
| Gift (D) | Photo element removed. Score line moves up. Headline can grow to 36px. |

### 8.2 When childName Is Missing

| Layout | Adaptation |
|--------|-----------|
| Hero (A) | Name element removed (it wasn't prominent anyway). Headline templates with `{child}` fall back to non-child variants. |
| Celebration (B) | Falls back to Hero (A) — Celebration requires both name AND photo for the personal identity centrepiece. |
| Blend (C) | Name element removed from centre stack. Headline fills the space. |
| Gift (D) | Name element removed. Occasion header + headline carry the message. Birthday occasions fall back to generic header. |

### 8.3 When Both childPhoto AND childName Are Missing

All layouts fall back to Hero (A) with enlarged headline (48px).
The mug message relies entirely on headline + character + score.
Headline engine avoids `{child}` templates. Score line becomes the personal anchor.

### 8.4 When Occasion Is "generic"

Gift (D) layout is never selected. Occasion header element is never rendered.
All other layouts proceed normally. More vertical space available for headline.

### 8.5 Degradation Priority (what gets cut first)

When space is tight (e.g., long occasion header + long child name + photo):

1. Feature callout — cut first (lowest priority optional)
2. Speech bubble — cut second (decorative only)
3. Photo size reduces — 72px -> 56px -> 44px -> hidden
4. Headline font shrinks — 42 -> 36 -> 32 -> 28 (never below 28)
5. Score format changes — "prominent" -> "subtle" -> never fully hidden

**Never cut**: Character, Headline, Brand, Accent bands.

---

## 9. CHARACTER SIZING RULES

### 9.1 Standing Characters (mama, papa, mini, cub)

```
Bounding box:  280 x 290 px CSS (900 x 933 px print)
Anchor:        Bottom-centre of panel
Feet position: y = 330 CSS (15px above canvas bottom, within safe area)
Head position: y = 40 CSS (approximately — varies by illustration)
```

Standing characters are full-body illustrations with feet firmly planted. They
fill roughly 84% of the canvas height. On the physical mug, a standing character
is approximately 77mm tall — clearly visible and recognisable.

### 9.2 Seated Characters (gran, gramps)

```
Bounding box:  320 x 260 px CSS (1029 x 836 px print)
Anchor:        Bottom-centre of panel
Chair base:    y = 330 CSS
```

Gran and Gramps are illustrated seated in armchairs. The armchair adds
approximately 40px of width on each side compared to standing characters.
They are 30px shorter than standing characters because of the seated posture,
but wider because of the chair.

**Impact on layout**: The wider bounding box means the character panel may need
5-10% more width allocation when gran/gramps are selected. The composition
engine should allocate:

| Character type | Left panel width (Hero layout) |
|---------------|-------------------------------|
| Standing (mama/papa/mini/cub) | 40% = 332px |
| Seated (gran/gramps) | 43% = 357px |

The right panel adjusts accordingly (57% = 473px for seated).

### 9.3 Infant Characters (cub)

Cub is smaller in illustration — a baby/toddler proportioned figure. Despite
using the same 290px bounding box as standing adults, the visible figure area
is approximately 60-70% of the box (the rest is transparent). The visual
weight is therefore lower than mama/papa.

**Compensation**: When cub is the primary character, the headline should be
slightly larger (+4px) to compensate for the reduced character visual mass.

### 9.4 Secondary Characters (in Blend layout)

```
Bounding box:  200 x 240 px CSS (643 x 772 px print)
Anchor:        Bottom-centre of their panel
```

Both characters in Blend layout are smaller than the primary character in
Hero layout. This is intentional — neither parent dominates. The central
message is the star.

---

## 10. VARIANT HANDLING: CAUCASIAN vs AFRICAN

**Rule: The two character variants (default/Caucasian and african) MUST use
identical positioning, sizing, and layout rules.**

The variant affects ONLY:
- Which PNG file is loaded (e.g., `mama_proud.png` vs `mama_proud_african.png`)
- African occasions (`heritage_gold`, `carnival_spirit`, `ubuntu`) auto-select
  the `african` variant unless user explicitly chose `default`

The variant does NOT affect:
- Character bounding box dimensions
- Panel width allocations
- Element positions
- Font sizes
- Colour tokens (those come from the occasion theme, not the variant)
- Any spacing or composition rules

Both variants are illustrated to the same proportions and bounding box.
If a future illustration violates this (e.g., one variant's armchair is wider),
the illustration must be corrected — the layout system must not branch on variant.

---

## 11. COLOUR PALETTE INTEGRATION

The composition system does not define its own colours. All colour values
are drawn from the occasion theme system in `mugThemes.js`.

### 11.1 Token Usage Map

| Element | Colour token | Example (generic) |
|---------|-------------|-------------------|
| Hero headline | `theme.dark` | #5A2035 |
| Score line | `theme.primary` | #C0364E |
| Child name | `theme.primary` | #C0364E |
| Occasion header | `theme.primary` | #C0364E |
| Feature callout | `theme.primary` at 80% | #C0364E CC |
| Speech bubble text | `theme.dark` | #5A2035 |
| Speech bubble border | `theme.primary` | #C0364E |
| Speech bubble bg | `#FFFFFF` | (always white — reads on ceramic) |
| Photo border | `theme.primary` | #C0364E |
| Brand mark | `theme.faint` at 45% | #C9A0AC 73 |
| Accent bands | gradient of `theme.light` + `theme.primary` | #E8637A / #C0364E |

### 11.2 Available Occasion Themes

| Occasion key | Primary | Dark | Character |
|-------------|---------|------|-----------|
| generic | #C0364E | #5A2035 | Warm rose |
| mothers_day | #C0364E | #5A2035 | Rose pink |
| fathers_day | #1A6BB5 | #1A3A5C | Navy blue |
| birthday | #D97706 | #78350F | Amber gold |
| heritage_gold | #C8960C | #1A0F00 | Kente gold |
| carnival_spirit | #FF6D00 | #1A1A2E | Carnival orange |
| ubuntu | #D84315 | #3E2723 | Terracotta |

### 11.3 Contrast Requirements

All text on the mug prints on white ceramic (transparent background = white).
Minimum contrast ratios:

| Element | Min contrast ratio vs white |
|---------|---------------------------|
| Headline | 7:1 (WCAG AAA for large text) |
| Score/name/callout | 4.5:1 (WCAG AA) |
| Brand mark | 1.5:1 (intentionally low — decorative) |

All current theme `dark` and `primary` tokens pass these thresholds against white.

---

## 12. COMPOSITION ENGINE SELECTION LOGIC

This section defines WHEN each layout is selected. The composition engine
(FE Lead's responsibility) implements this logic — this document specifies
the visual rules the engine must follow.

### 12.1 Layout Selection Matrix

| Condition | Layout |
|-----------|--------|
| occasion != "generic" | Gift (D) |
| winnerPct <= 59 OR winner == "blend"/"unknown" | Blend (C) |
| childPhoto AND childName AND winnerPct 60-69 | Celebration (B) |
| All other cases | Hero (A) |

**Priority order** (first match wins):
1. Gift (D) — occasion overrides everything
2. Blend (C) — close call / blend overrides personal layouts
3. Celebration (B) — requires both photo and name plus moderate win
4. Hero (A) — default fallback, always works

### 12.2 Character Selection Rules

| Input | Primary character | Secondary character |
|-------|------------------|-------------------|
| winner = mum-alias | mama | papa (Blend only) |
| winner = dad-alias | papa | mama (Blend only) |
| winner = custom label | mama (default) | papa (Blend only) |
| recipient = grandparent | gran or gramps | - |
| occasion = grandparents_day | gran or gramps | - |
| Blend layout | mama (left) | papa (right) |

Gran/Gramps override mama/papa when the mug is specifically for a grandparent.

### 12.3 Emotion Selection Rules

| Condition | Emotion |
|-----------|---------|
| mothers_day / fathers_day | proud |
| christmas / birthday | celebrating |
| grandparents_day / heritage themes | showing_off |
| valentines | loving |
| winnerPct >= 75 (no occasion) | celebrating |
| winnerPct 65-74 | proud |
| winnerPct 55-64 | cheeky |
| winnerPct <= 54 | surprised |

Remapping applies after selection (Section 3.1 emotion remapping rules).

---

## 13. PRINT QUALITY CHECKLIST

Before any layout is approved for production:

- [ ] All text readable at arm's length on a physical 11oz mug
- [ ] No element overlaps another element's text (characters may overlap panels, but never obscure text)
- [ ] Transparent background verified — no stray white rectangles
- [ ] Accent bands render edge-to-edge
- [ ] Character feet/chair base within safe area (not in feather zone)
- [ ] Headline does not exceed 35 characters (excluding newlines)
- [ ] Score line does not overflow panel width (ellipsis if needed)
- [ ] Child photo circle has clean mask (no jagged edges at 3.217x)
- [ ] Brand mark visible but not prominent
- [ ] Works identically with default and african character variants
- [ ] Cultural themes (heritage_gold, carnival_spirit, ubuntu) use correct colour tokens
- [ ] No text uses white (#fff) or near-white colours (invisible on ceramic)

---

## 14. SUMMARY TABLE: ALL LAYOUTS AT A GLANCE

| Property | Hero (A) | Celebration (B) | Blend (C) | Gift (D) |
|----------|----------|-----------------|-----------|----------|
| Panels | 2 (40/60) | 3 (30/45/25) | 3 (25/50/25) | 2 (35/65) |
| Primary char size | 290px | 260px | 240px | 260px |
| Second char | No | No | Yes (240px) | No |
| Headline size | 42px (36 w/photo) | 32px | 36px | 32px |
| Photo size | 56px or none | 72px (required) | None | 44px or none |
| Child name | Optional | Required | Optional | Optional |
| Occasion header | No | No | No | Yes (required) |
| Speech bubble | Yes | Yes | No | Optional |
| Feature callout | No | Yes | No | Optional |
| Score format | Prominent | Subtle | Subtle | Subtle |
| Max elements | 5 | 7 | 5 | 7 |
| Tone | Bold, playful | Warm, personal | Unity, togetherness | Celebratory, gifty |

---

## REFERENCES

- Prodigi GLOBAL-MUG-W product spec (228.6 x 94.8mm, 2670 x 1110px)
- `docs/KEEPSAKE_MUG_TEMPLATE_SPEC.md` — physical constraints, typography, colour tokens
- `docs/CULTURAL_THEMES_SPEC.md` — Heritage Gold, Carnival Spirit, Ubuntu palettes
- `docs/AGE_STYLE_DIFFERENTIATION_SPEC.md` — age-specific visual treatment (not applied to character mug — character mug uses its own system)
- `src/assets/characters/index.js` — character image registry, getCharacterImage() API
- `src/components/keepsakes/utils/mugThemes.js` — OCCASION_THEMES, colour tokens
- `src/components/keepsakes/utils/characterHeadlines.js` — headline engine, 60+ headline options
- `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` — current Hero layout implementation (Layout A baseline)

===============================================
  END OF VISUAL DIRECTION — COMPOSITION RULES
  Visual Director | 30 March 2026
===============================================
