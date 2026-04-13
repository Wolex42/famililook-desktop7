# Visual Director Brief — Character Mug UX Clarity
**Agent:** Visual Director
**Track:** Parallel to crash fix (runs independently)
**Date:** 2026-04-07
**Parent:** CEO report — "not clear how characters render on mugs" + "how it would merge with results"

---

## Your Mission

The CEO reported two UX clarity failures in the character mug flow:

1. **"Not clear how characters could be rendered on the mugs"** — the user doesn't understand what the character mug product IS or how their character selection becomes a physical mug
2. **"How it would merge with results"** — after running analysis and seeing results (winner, features, percentages), the connection to character mug is invisible. The user doesn't understand that the winning parent's character represents the child's resemblance.

You need to spec:
- A **product explanation moment** — shown before or during CharacterPicker, explaining what the user is building
- A **results-to-character bridge** — a visual/copy moment that connects "your child looks like Mum (65%)" to "here's Mum's character, customised to reflect that"
- A **preview button position fix** — the preview CTA is too far down. Spec where it should be.

You do NOT write copy. Copywriter does that. You spec the visual structure, placement, and hierarchy. Copywriter fills the words.

---

## What You Must Read First

1. `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` — understand the full screen sequence (what screens exist, in what order)
2. `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` — this is the screen where character selection happens. What does it currently show? What is above and below the fold?
3. `src/components/keepsakes/mobile/CharacterPicker.jsx` — what does the picker UI look like? How does it present the character options?
4. `src/components/keepsakes/mobile/KeepsakePreview.jsx` — where is the preview/add-to-basket CTA currently positioned?
5. The audit finding KS-07 — plan gate silent close. If a free user hits the order button, nothing happens. Your spec should also address what the plan gate shows (but do not design the upgrade flow — flag it for a separate task).

---

## What You Must NOT Do

- Write copy (that is Copywriter's job — you spec the container, they fill the words)
- Write code
- Change the character selection logic
- Design the analysis-to-character auto-selection feature (that is a future feature — for now, spec the explanation of the manual connection)

---

## The Three Things to Spec

### Spec 1 — Product Explanation Moment

Where in the flow does the user first need to understand what a character mug IS?

Options to assess and recommend one:
- **Option A**: A dismissable banner at the top of the KeepsakeCustomise screen when `product === 'character_mug'`
- **Option B**: A brief intro screen before CharacterPicker opens (a modal or inline card)
- **Option C**: A tooltip/info icon next to "Character Mug" in the catalogue that expands

Spec whichever you recommend:
- Exact position (px from top, or relative to what element)
- Visual treatment (card, banner, modal, tooltip)
- What visual elements it contains (illustration placeholder, headline zone, body zone, dismiss)
- Dimensions and spacing
- When it dismisses (once per session? permanently after first view?)

### Spec 2 — Results-to-Character Bridge

When the user arrives at the character mug flow from the results page, they've just seen "Emma looks 65% like Mum." The character mug is supposed to celebrate that. Currently there is no visible connection.

Spec a **bridge moment** — a single visual element that connects the two:
- Where it appears (top of KeepsakeCustomise? Above CharacterPicker? Inline card?)
- What it shows (the winner's name, the percentage, an icon or colour that matches the results page palette)
- Exact dimensions, colours (use existing brand tokens — violet #7C3AED, green chip colours from the 2026 colour system)
- What happens if there are no analysis results (user came directly, not from results) — graceful omission or default state

### Spec 3 — Preview CTA Position Fix

The "Add to Basket" / preview button is too far down the page. CEO had to scroll excessively to reach it.

Two approaches — assess and recommend one:
- **Option A**: Sticky bottom bar — fixed position at bottom of viewport, always visible
- **Option B**: Move the preview section higher in the scroll order (above character customisation options)

Spec your recommendation:
- Exact position, height, z-index behaviour
- What the bar/button contains (CTA label zone, price zone)
- How it interacts with the mobile keyboard (if any inputs are on screen)
- Safe area insets for iOS (bottom padding for home indicator)

---

## Output Format

```
═══════════════════════════════════════════════════════
  VISUAL DIRECTION — Character Mug UX Clarity
  Visual Director — 2026-04-07
═══════════════════════════════════════════════════════

PRODUCT: FamiliLook — Character Mug (mobile flow)
SCREENS AFFECTED: KeepsakeCustomise, CharacterPicker entry, KeepsakePreview

───────────────────────────────────────────────────────
SPEC 1 — PRODUCT EXPLANATION MOMENT
───────────────────────────────────────────────────────
PLACEMENT: <screen name, position>
TREATMENT: <card | banner | modal | tooltip>
TRIGGER: <when shown>
DISMISS: <how/when>

LAYOUT:
  ┌──────────────────────────────┐
  │  [illustration placeholder]  │  40px × 40px
  │  [headline zone]             │  font: Inter Bold 16pt
  │  [body zone — 2 lines max]   │  font: Inter Regular 13pt
  │  [dismiss button]            │  44pt touch target
  └──────────────────────────────┘

DIMENSIONS: <width × height>
COLOURS:
  Background: <hex>
  Border/accent: <hex>
  Text: <hex>

ANIMATION: <fade in | slide up | none>
COPY BRIEF FOR COPYWRITER: <what the headline should communicate — not the words>

───────────────────────────────────────────────────────
SPEC 2 — RESULTS-TO-CHARACTER BRIDGE
───────────────────────────────────────────────────────
PLACEMENT: <screen, position>
SHOWN WHEN: <analysis results exist | always | conditional>
HIDDEN WHEN: <no results>

LAYOUT:
  ┌──────────────────────────────┐
  │  [winner icon/chip]  [pct]   │
  │  [bridge message zone]       │
  └──────────────────────────────┘

DIMENSIONS: <width × height>
COLOURS:
  Chip: <hex — from existing green chip system>
  Background: <hex>
  Text: <hex>

COPY BRIEF FOR COPYWRITER: <what this moment should communicate>

───────────────────────────────────────────────────────
SPEC 3 — PREVIEW CTA POSITION FIX
───────────────────────────────────────────────────────
SOLUTION: Option A (sticky bar) | Option B (moved higher)
REASON: <why this option>

LAYOUT:
  ┌──────────────────────────────┐
  │  [price zone]  [CTA button]  │
  └──────────────────────────────┘  height: 72px + safe area

POSITION: fixed bottom: 0
Z-INDEX: <value>
PADDING: bottom: calc(16px + env(safe-area-inset-bottom))
CONTENT PADDING: paddingBottom: 88px on scroll container (prevents content hidden behind bar)
COLOURS:
  Background: <hex>
  CTA button: <hex — violet primary>
  Price text: <hex>

COPY BRIEF FOR COPYWRITER: <CTA label guidance>

───────────────────────────────────────────────────────
IMPLEMENTATION NOTES FOR FE LEAD:
  - All new elements use Tailwind (not inline styles — these are UI, not print templates)
  - Touch targets minimum 44pt
  - Safe area insets required on sticky bar
  - [Any other constraints]

ASSETS REQUIRED:
  1. <any new illustrations or icons needed>
═══════════════════════════════════════════════════════
```

Save to: `Agent_1/crew/output/VISUAL_DIRECTION_character_mug_ux.md`
