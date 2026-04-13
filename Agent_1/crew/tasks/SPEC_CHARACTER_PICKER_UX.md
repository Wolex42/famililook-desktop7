# Spec: Character Illustration Picker UX
## Date: 05 April 2026 | Author: Visual Director | Status: DRAFT
## Product: Character Mug (KeepsakeCustomise flow)

---

## Design Goal

Let users browse and select character illustrations while preserving the smart defaults
from compositionEngine.js. Most users should get a great result automatically; customisation
is an opt-in layer that increases personal attachment and encourages repeat purchases.

---

## 1. Placement in the Customise Flow

The picker sits AFTER the Recipient selector and BEFORE the Character Style (Classic/Heritage)
toggle. Rationale: the recipient determines the smart default character (mama for "For Mum",
gramps for "Grandparent"), so the picker must load after that choice is made.

Current order with the picker inserted:
1. Design Style chips (default, heritage, carnival, ubuntu)
2. Age Theme chips (infant, child, teen)
3. Recipient selector ("For Me", "For Mum", etc.)
4. **Character Picker** (NEW)
5. Character Style variant (Classic / Heritage)
6. Personalised message toggle

The picker does NOT get its own step or screen. It lives inline in the scrollable customisation
area, consistent with the existing chip-based pattern. No modal, no separate page.

---

## 2. Browsing Experience: Featured Card + Emotion Strip

The picker has two tiers, collapsed by default:

**Tier 1 — Featured Card (always visible)**
A single card (approx 280px wide, 100px tall) showing the auto-selected character at full
size on the left, with its name and emotion label on the right ("Mama - Proud"). A subtle
"Change character" link sits below the label. The card has a soft violet glow border when
it matches the smart default, reinforcing that this is already a good choice.

**Tier 2 — Emotion Strip (revealed on tap of "Change character")**
A horizontal scrollable row of circular thumbnails (56px diameter, 8px gap), showing every
available emotion for the CURRENT character type. The auto-selected emotion has a violet
ring; others have a 1px dark border. Tapping a thumbnail selects that emotion and updates
the mug preview instantly.

Below the emotion strip, a secondary row of role chips (Mama, Papa, Cub, Mini, Gran, Gramps)
allows switching character type entirely. These are text-only pills, 40px height, matching
the existing chip style. The currently selected type has the violet highlight.

This two-tier approach avoids overwhelming users with a 66-illustration grid while still
making the full catalogue reachable in two taps.

---

## 3. Smart Defaults

When the customise screen loads, compositionEngine.js runs and determines the optimal
character type + emotion + variant. The picker pre-selects this result. The Featured Card
shows a small "Auto-selected" badge (10px uppercase label, #9090B0 colour) to signal
that the system has made an intelligent choice.

If the user changes any picker value, the badge changes to "Your pick" in violet. If they
want to revert, a "Reset to best match" ghost button appears at the end of the emotion
strip, restoring the engine's original selection.

---

## 4. Context-Aware Filtering

**Recipient-driven ordering:**
When recipient is "For Mum" -> mama illustrations appear first in the role chips, and the
emotion strip shows mama emotions. Papa, Cub, etc. are still accessible but further along.
When recipient is "Grandparent" -> gran/gramps lead. When "For Me" -> cub/mini lead
(the child's perspective).

**Ethnicity-aware defaults:**
When Character Style is set to "Heritage" (african variant), all thumbnails in the emotion
strip show the african variant PNGs. When set to "Classic", they show default PNGs. The
variant toggle already exists and sits below the picker, so changing it automatically
refreshes every thumbnail in the strip. No separate filtering control needed.

**Occasion-driven emotion sorting:**
When the occasion context is "birthday" or "christmas", celebrating/giggling emotions sort
to the front of the strip. When "valentines", loving sorts first. The auto-selected emotion
from the engine already accounts for this, so sorting reinforces rather than contradicts it.

---

## 5. Emotion Selection Model

Emotions are NOT a separate step. Each circular thumbnail in the emotion strip IS a character
shown in a specific emotion. The user sees the illustration itself, not an abstract label.
The emotion name appears as a caption below each circle ("Proud", "Cheeky", "Celebrating").

This means: one tap to preview an emotion. No dropdowns, no multi-step drill-down.

Characters that lack a given emotion (e.g. gran has no "loving_african" asset) simply do not
show that thumbnail. The strip only renders emotions where a valid PNG exists for the current
character type + variant combination.

---

## 6. Preview Integration

Every selection change triggers an immediate mug preview update. The MugCeramicPreview
component already receives composition data; the picker simply overrides the `character`
field in the composition plan with the user's selection before passing it down.

**Transition:** When the character changes, the mug preview cross-fades (200ms opacity
transition) rather than popping. This gives a smooth, native-feeling update consistent
with the YouVersion card transition feel.

**Scroll behaviour:** The preview area (top 50% of screen) remains visible while the user
scrolls through the picker section. The existing sticky preview pattern handles this.

---

## 7. Delight Factor

**Bounce-in on select:** When a user taps a new emotion thumbnail, the selected circle
scales from 1.0 to 1.08 and back over 250ms (CSS spring ease). Subtle but tactile.

**Character reaction:** When switching between characters (e.g. Mama to Papa), the outgoing
character slides left and fades while the incoming character slides in from the right on
the Featured Card. 300ms transition. Feels like flipping through a cast of characters.

**Emotion label animation:** The emotion caption under the Featured Card fades and slides
up when changing, replaced by the new label sliding up from below. Micro-interaction that
adds polish without slowing the user down.

**"Try them all" nudge:** If the user has not interacted with the picker after 3 seconds
of it being visible, a one-time subtle shimmer passes across the "Change character" link.
Draws attention without being intrusive. Shows once per session, never repeats.

---

## 8. Accessibility

- All thumbnails have `alt` text: "{character} looking {emotion}" (e.g. "Mama looking proud")
- Role chips are a radio group with `role="radiogroup"` and `aria-label="Character type"`
- Emotion strip is keyboard-navigable with arrow keys
- Minimum 44px touch target on all interactive elements (thumbnails are 56px, chips are 40px
  height but full-width tap area extends to 44px via padding)
- Colour contrast: violet ring on dark background exceeds 4.5:1

---

## Asset Inventory (56 confirmed PNGs)

| Type    | Emotions (default)                                      | African variant |
|---------|---------------------------------------------------------|-----------------|
| mama    | celebrating, cheeky, loving, proud, surprised           | Yes (5+5=10)    |
| papa    | celebrating, cheeky, loving, proud, surprised           | Yes (5+5=10)    |
| cub     | curious, giggling, happy, sleeping, surprised           | Yes (5+5=10)    |
| mini    | celebrating, cheeky, proud, surprised                   | Yes (4+4=8)     |
| gran    | laughing, loving*, proud, showing_off, surprised        | Yes (4+5=9)*    |
| gramps  | laughing, loving, proud, showing_off, surprised         | Yes (5+5=10)    |

*gran_loving_african.png not found in assets — strip must handle this gap gracefully.

Total: 56 PNGs across 6 types, 2 variants.

---

## Out of Scope

- Multi-character selection (picking both characters for blend layout) — future iteration
- Custom illustration uploads — not planned
- Character animation/movement on the mug itself — static PNGs only
- Changes to compositionEngine.js logic — this spec is purely UX layer
