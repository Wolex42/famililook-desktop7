# Copywriter Brief — Character Mug UX Copy
**Agent:** Copywriter
**Track:** Parallel to Visual Director (activates together)
**Date:** 2026-04-07
**Dependency:** Visual Director spec must be read before finalising copy — character counts must fit the Visual Director's layout dimensions

---

## Context

The CEO reported that the character mug flow is confusing — users don't understand what they're building or how their analysis results connect to the character. Visual Director is speccing three new UI moments. You write the copy for each.

**Read the Visual Director's output first** (`crew/output/VISUAL_DIRECTION_character_mug_ux.md`) before finalising anything. The Visual Director defines the container sizes — you must fit within them.

---

## What You Must Read First

1. `crew/output/VISUAL_DIRECTION_character_mug_ux.md` — the Visual Director's layout spec (read after it's produced)
2. `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` — understand the current screen context and any copy already present
3. `src/components/keepsakes/utils/mugThemes.js` — existing copy patterns (OCCASION_HEADERS, FEATURE_LABELS) — match the tone
4. The CEO bug report — read the exact words used: "not clear how characters could be rendered on the mugs", "how it would merge with results"

---

## The Three Copy Jobs

### Copy Job 1 — Product Explanation Moment

The user sees this before or during CharacterPicker. They don't yet understand what a character mug is.

**What it must communicate** (Visual Director will specify which):
- What the product looks like (a mug with a personalised cartoon character on it)
- That the character represents their family member
- That it's made just for them based on their family

**Constraints:**
- Headline: max 35 characters (must be readable at a glance)
- Body: max 2 lines, ~60-70 characters per line
- Tone: warm, celebratory, FamiliLook voice — NOT clinical, NOT technical
- No mention of AI, algorithms, or analysis
- Must work without knowing who the winner is (shown before results connection)

**Provide:** 2 headline variants + 2 body variants (A/B)

### Copy Job 2 — Results-to-Character Bridge

The user has seen results. "Emma looks 65% like Mum." Now they're choosing a character mug. This moment connects the two.

**What it must communicate:**
- Their child shares [X]% of their features with [parent]
- The character represents that parent
- This mug celebrates that resemblance

**Data available to personalise:**
- `winner` — "parent1" or "parent2" (maps to Mum/Dad or the parent's name)
- `winnerPct` — e.g. 65
- `childName` — e.g. "Emma" (if provided)

**Template variants needed:**
- Named child + named winner: e.g. "Emma got Mum's look — 65% match"
- Named child + unnamed winner: e.g. "Emma takes after Mum — 65%"
- No child name: e.g. "65% Mum — capture it on a mug"
- Blend result: e.g. "A perfect blend — celebrate both sides"

**Constraints:**
- Single line, max 50 characters (this is a chip/banner, not a paragraph)
- Tone: celebratory, warm, factual but emotional
- No 50/50 — there is always a winner (per contract rules)
- No health/DNA claims

**Provide:** All 4 template variants above, each with an A/B option

### Copy Job 3 — Preview CTA Button

The button that takes the user to see their mug preview / add to basket.

**Current state:** Unknown — read KeepsakePreview.jsx to find what the current label is.

**What it must communicate:**
- Action: see how the mug will look, or add it to basket
- Value: this is the moment they commit

**Constraints:**
- Max 20 characters (button label)
- Active voice
- No "Submit", "Continue", "Next" — too transactional

**Provide:** 3 label variants

---

## Output Format

```
===============================================
  COPY BANK — Character Mug UX Clarity
  Copywriter — 2026-04-07
===============================================

PRODUCT: FamiliLook — Character Mug (mobile flow)
VISUAL SPEC REFERENCE: VISUAL_DIRECTION_character_mug_ux.md

───────────────────────────────────────────────
COPY JOB 1 — PRODUCT EXPLANATION MOMENT
Container: <from Visual Director spec>
───────────────────────────────────────────────

HEADLINES (max 35 chars — verified):
  H01-A | <copy> | <N chars> | Variant A
  H01-B | <copy> | <N chars> | Variant B

BODY TEXT (max 2 lines, ~65 chars/line — verified):
  B01-A | <line 1> | <N chars>
         | <line 2> | <N chars>
  B01-B | <line 1> | <N chars>
         | <line 2> | <N chars>

DISMISS LABEL:
  D01 | <copy> | <N chars> | e.g. "Got it"

───────────────────────────────────────────────
COPY JOB 2 — RESULTS-TO-CHARACTER BRIDGE
Container: <from Visual Director spec — single line max 50 chars>
───────────────────────────────────────────────

TEMPLATE: Named child + named winner (pct shown)
  T01-A | "{childName} got {winnerName}'s look — {pct}%" | <N chars template> | A
  T01-B | <variant> | <N chars> | B

TEMPLATE: Named child + unnamed winner
  T02-A | <copy> | <N chars> | A
  T02-B | <copy> | <N chars> | B

TEMPLATE: No child name
  T03-A | <copy> | <N chars> | A
  T03-B | <copy> | <N chars> | B

TEMPLATE: Blend result
  T04-A | <copy> | <N chars> | A
  T04-B | <copy> | <N chars> | B

───────────────────────────────────────────────
COPY JOB 3 — PREVIEW CTA BUTTON
Max 20 chars — verified
───────────────────────────────────────────────
  CTA-01 | <copy> | <N chars>
  CTA-02 | <copy> | <N chars>
  CTA-03 | <copy> | <N chars>

───────────────────────────────────────────────
IMPLEMENTATION NOTES FOR FE LEAD:
  Use exact strings as written — do not paraphrase or shorten
  Template strings use {variable} notation — FE Lead replaces at render time
  [Any conditional logic notes]

BRAND COMPLIANCE:
  No health/DNA claims: ✅
  No 50/50 language: ✅
  "for entertainment" disclaimer: N/A (in-app UI, not marketing)
  FamiliPoker content: N/A
  VERDICT: PASS
===============================================
```

Save to: `Agent_1/crew/output/COPY_BANK_character_mug_ux.md`
