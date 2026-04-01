# Keepsake Fixes — Copy Spec: Headline Character Limits

**Author**: Copywriter (Native Persona)
**Date**: 2026-04-01
**Status**: SPEC — for Visual Director + FE Lead implementation
**Related**: `characterHeadlines.js`, `compositionEngine.js`, `CharacterMugTemplate.jsx`

---

## 1. Current State

### How Headlines Are Generated

The headline system lives in `characterHeadlines.js` and is orchestrated by `compositionEngine.js`. The flow:

1. **normaliseParent()** maps the winner label (e.g. "Mummy", "Papa", "Grandma") to one of 17 recognised role types or "custom"
2. **selectHeadlines()** picks from categorised pools based on:
   - Parent type (mum / dad / custom)
   - Percentage bracket (high >= 70%, medium >= 60%, close < 60%, blend)
   - Recipient context (winner_parent, loser_parent, grandparent, self)
3. **Deterministic selection** via djb2 hash seeded on `childName + winnerPct` — same inputs always produce the same headline
4. **Template resolution** substitutes `{child}`, `{winner}`, `{loser}`, `{feature}` placeholders with actual names (uppercased)
5. **35-char enforcement** (ignoring `\n` line breaks) — if the selected headline exceeds 35 chars, the engine walks the pool for a shorter alternative, then falls back to a SHORT_FALLBACK pool

### Current Pools

| Pool | Count | Purpose |
|------|-------|---------|
| `HEADLINES.mum.high` | 12 | Strong mum resemblance (>= 70%) |
| `HEADLINES.mum.medium` | 5 | Moderate mum resemblance (60-69%) |
| `HEADLINES.dad.high` | 12 | Strong dad resemblance (>= 70%) |
| `HEADLINES.dad.medium` | 5 | Moderate dad resemblance (60-69%) |
| `HEADLINES.close` | 11 | Close call (< 60%) |
| `HEADLINES.blend` | 5 | Blend / unknown |
| `HEADLINES.custom` | 10 | Custom parent names (uses `{winner}` placeholder) |
| `RECIPIENT_HEADLINES.winner_parent.*` | ~30 | Mug made FOR the winning parent |
| `RECIPIENT_HEADLINES.loser_parent.*` | ~22 | Mug made FOR the losing parent |
| `RECIPIENT_HEADLINES.grandparent` | 8 | Mug made FOR a grandparent |
| `RECIPIENT_HEADLINES.blend` | 5 | Blend override at 51-52% |
| `SUBHEADLINES.*` | 24 (3 per feature) | Feature-specific sub-headlines |
| `CHARACTER_OCCASION_HEADERS` | 9 | Occasion banners |
| `SPEECH.*` | 19 | Speech bubble text |
| `SHORT_FALLBACK` | 5 | Ultimate safety net |

### Current Max Character Constraint

- **Hero headlines**: 35 characters total (newlines excluded from count)
- **Feature sub-headlines**: 50 characters (truncated via `truncateAtWord()`)
- **Occasion headers**: 30 characters
- **Speech bubbles**: No formal limit (all are under 20 chars)
- **Truncation method**: `truncateAtWord()` adds ellipsis character (U+2026) at word boundary

---

## 2. The Problem

The 35-char total limit does not account for **per-line width**. Headlines use `\n` to create two-line layouts, and the rendering engine uses `white-space: pre-line`. A headline like `"TEAMWORK MAKES\nTHE BABY"` has 23 chars total but its first line is 15 chars — which may fit comfortably. However, a headline like `"CHRISTOPHER-JAMES: MUMS MINI ME"` (31 chars, no line break) renders as a single line that overflows narrower panels.

The real constraint is **pixels per line**, not total characters.

---

## 3. Layout Panel Widths (from CharacterMugTemplate.jsx)

| Layout | Panel | CSS Width | Padding (L+R) | Usable Text Width |
|--------|-------|-----------|----------------|-------------------|
| **A: Hero** | Right (60%) | 498px | 32 + 28 = 60px | **438px** |
| **B: Celebration** | Centre (45%) | 373px | 16 + 16 = 32px | **341px** |
| **C: Blend** | Centre (50%) | 414px | 20 + 20 = 40px | **374px** |
| **D: Gift** | Right (65%) | 539px | 28 + 24 = 52px | **487px** |

### Font Sizes Per Layout

| Layout | Condition | Font Size |
|--------|-----------|-----------|
| Hero (large) | No photo | 42px |
| Hero (large) | With photo | 36px |
| Celebration (medium) | With occasion | 32px |
| Celebration (medium) | No occasion | 36px |
| Blend | Always | 36px |
| Gift (medium) | With occasion | 32px |
| Gift (medium) | No occasion | 36px |

**Font**: Nunito, weight 900 (Black), uppercase, letter-spacing -0.02em

---

## 4. Recommended Max Character Limits Per Line

Using measured Nunito Black uppercase average character widths (accounting for -0.02em tracking):

| Font Size | Avg Char Width (uppercase) | Notes |
|-----------|---------------------------|-------|
| 42px | ~25px | Wide chars (M, W) ~32px; narrow (I, J) ~15px |
| 36px | ~21px | Wide ~27px; narrow ~13px |
| 32px | ~19px | Wide ~24px; narrow ~11px |

### Per-Layout Max Characters Per Line

| Layout | Usable Width | Font Size | Max Chars/Line | Recommended Safe Limit |
|--------|-------------|-----------|----------------|----------------------|
| **Hero (no photo)** | 438px | 42px | ~17 | **15 chars/line** |
| **Hero (with photo)** | 438px | 36px | ~20 | **18 chars/line** |
| **Celebration (occasion)** | 341px | 32px | ~17 | **16 chars/line** |
| **Celebration (no occasion)** | 341px | 36px | ~16 | **14 chars/line** |
| **Blend** | 374px | 36px | ~17 | **16 chars/line** |
| **Gift (occasion)** | 487px | 32px | ~25 | **22 chars/line** |
| **Gift (no occasion)** | 487px | 36px | ~23 | **20 chars/line** |

### Universal Safe Limits (must-not-exceed)

The **narrowest case** is Celebration without occasion: 341px at 36px Nunito Black.

| Constraint | Current | Recommended |
|------------|---------|-------------|
| **Max total chars** (newlines excluded) | 35 | **28** |
| **Max chars per single line** | No limit | **16** |
| **Max chars per line (standard panels)** | No limit | **18** |
| **Max chars per line (narrow/Celebration)** | No limit | **14** |

---

## 5. Truncation Strategy: Shorter Alternative, NOT Ellipsis

**Recommendation: NEVER truncate with "..." on mug headlines.**

Reasons:
1. Mugs are gift products. Ellipsis looks unfinished, cheap, and broken to the buyer.
2. The existing `SHORT_FALLBACK` pool pattern is correct — use a shorter pre-written alternative instead.
3. The `truncateAtWord()` function should remain for sub-headlines only (feature callouts, where truncation is less visible).

**Implementation rule:**
- If no headline in the selected pool fits both the total AND per-line limit, the engine must fall through to `SHORT_FALLBACK` (already exists).
- `SHORT_FALLBACK` entries must ALL have per-line lengths under 14 chars. Current pool passes this check.

---

## 6. Headline Pool Audit — Entries That Commonly Exceed Limits

### Headlines That Exceed 16 chars/line (Celebration-unsafe)

These will overflow the Celebration panel (341px at 36px):

| Headline | Longest Line | Chars | Status |
|----------|-------------|-------|--------|
| `SORRY DAD, I'M ALL MUM` | (single line in template) | 22 | EXCEEDS (needs `\n`) |
| `MUM DID ALL THE WORK` | (single line) | 20 | EXCEEDS |
| `COPY + PASTE: MUM EDITION` | `COPY + PASTE:` / `MUM EDITION` | 14 / 11 | OK (has `\n`) |
| `SORRY MUM, THIS ONE'S DAD` | (single line in template) | 25 | EXCEEDS (needs `\n`) |
| `DAD'S CTRL+C, CTRL+V` | `DAD'S` / `CTRL+C, CTRL+V` | 5 / 14 | OK |
| `ALL DAD, NO QUESTION` | (single line) | 19 | EXCEEDS |
| `DAD STAMP: APPROVED` | (single line in template) | 19 | EXCEEDS |
| `TEAMWORK MAKES THE BABY` | `TEAMWORK MAKES` / `THE BABY` | 14 / 8 | OK |
| `THE VERDICT: JUST BARELY` | `THE VERDICT:` / `JUST BARELY` | 12 / 11 | OK |

### Custom Pool Entries That Overflow With Long Names

With a 10+ char custom name (e.g. "ELIZABETH"), these `{winner}` templates produce overlong lines:

| Template | With "ELIZABETH" | Longest Line |
|----------|-----------------|-------------|
| `{child} LOOKS LIKE {winner}` | 29 total, single-line risk | EXCEEDS |
| `{winner}'S GREATEST HIT` | 21 chars, no `\n` | EXCEEDS |
| `HELLO, MINI {winner}` | 19 single line | EXCEEDS |
| `{winner} CALLED IT` | 18 single line | BORDERLINE |

### Sub-Headlines That Exceed 50-Char Limit With Long Names

| Template | With "CHRISTOPHER-JAMES" | Total |
|----------|------------------------|-------|
| `{winner}'S SMILE, THROUGH AND THROUGH` | 45 | OK (under 50) |
| `EYEBROWS: COURTESY OF {winner}` | 39 | OK |
| `{winner}'S FACE SHAPE, NO DOUBT` | 39 | OK |
| `FACE SHAPE: A GIFT FROM {winner}` | 41 | OK |

Sub-headlines are safe at 50 chars but should be reviewed if the sub-headline panel narrows.

---

## 7. Long Name Fallback Strategy

**Question**: When names are very long (e.g. "Christopher-James", 17 chars), should we truncate the name or use an initial?

**Recommendation: Tiered approach, NEVER truncate mid-name.**

### Tier 1: Short Name (1-8 chars) — Use as-is
Examples: "Olivia", "Max", "James"
- All template substitutions work within limits

### Tier 2: Medium Name (9-12 chars) — Use as-is, but restrict to safe templates
Examples: "Charlotte", "Elizabeth", "Alexander"
- Skip templates where `{winner}` or `{child}` appears mid-line (e.g. `{child} LOOKS LIKE {winner}`)
- Prefer templates where name is on its own line or at the start

### Tier 3: Long Name (13+ chars) — Use first name only OR fall through to non-name headline
Examples: "Christopher-James", "Mary-Elizabeth"
- If name contains a hyphen: use first segment ("Christopher" = 11 chars, still Tier 2)
- If name is a single long word: skip all `{child}`/`{winner}` templates, use generic pool
- NEVER truncate to "Christoph..." — it looks broken on a gift product
- NEVER use initials ("C-J") — too impersonal for a keepsake

### Implementation Pseudocode
```
function safeName(name) {
  if (name.length <= 12) return name;
  if (name.includes('-')) return name.split('-')[0]; // First part of hyphenated
  return null; // Signal: skip name-bearing templates
}
```

When `safeName()` returns `null`, the headline engine should select from pools that do not contain `{child}` or `{winner}` placeholders (i.e. `HEADLINES.close`, `HEADLINES.blend`, or `SHORT_FALLBACK`).

---

## 8. Revised SHORT_FALLBACK Pool

The existing SHORT_FALLBACK is good but should be expanded for variety. All entries must be under 14 chars per line:

```
CURRENT (keep all):
  "MINI ME"              — 7 chars
  "FAMILY\nGENES"        — 6/5 chars
  "LOOK\nALIKE"          — 4/5 chars
  "CHIP OFF\nTHE BLOCK"  — 8/9 chars
  "SPITTING\nIMAGE"      — 8/5 chars

PROPOSED ADDITIONS:
  "FAMILY\nTIES"         — 6/4 chars
  "IT'S A\nMATCH"        — 6/5 chars
  "JUST LIKE\nYOU"       — 9/3 chars
  "THE PROOF\nIS HERE"   — 9/7 chars
  "DNA DON'T\nLIE"       — 9/3 chars
```

(Note: "DNA DON'T LIE" is borderline on brand guardrails — we do not make DNA claims. Replace with "GENES DON'T LIE" if compliance flags it. 14 chars per line, still safe.)

**Alternative to "DNA DON'T LIE":**
  `"LIKE PARENT\nLIKE CHILD"` — 11/10 chars, warm, no DNA claim.

---

## 9. Summary of Recommendations

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | Add per-line character limit enforcement (max 16 chars/line for Celebration, 18 for standard) | FE Lead | P1 |
| 2 | Reduce total char limit from 35 to 28 | FE Lead | P1 |
| 3 | Add `\n` line breaks to single-line headlines that exceed 14 chars | Copywriter (this spec) | P1 |
| 4 | Implement `safeName()` tiered name handling | FE Lead | P1 |
| 5 | Expand SHORT_FALLBACK pool with 4-5 new entries | Copywriter (above) | P2 |
| 6 | Remove `truncateAtWord()` from headline path (keep for sub-headlines only) | FE Lead | P2 |
| 7 | Audit all `{winner}` / `{child}` templates against 12-char name worst case | Copywriter + QA | P2 |

---

## 10. Headline Rewrites Needed (P1)

These existing headlines need `\n` breaks added to comply with the 16 chars/line limit:

```
BEFORE                              AFTER                           Max Line
─────────────────────────────────── ─────────────────────────────── ────────
"SORRY DAD, I'M ALL MUM"           "SORRY DAD,\nI'M ALL MUM"       11
"MUM DID ALL THE WORK"             "MUM DID\nALL THE WORK"         12  (already exists as this!)
"ALL MUM, NO DOUBT"                "ALL MUM,\nNO DOUBT"            8   (already exists!)
"SORRY MUM, THIS ONE'S DAD"        "SORRY MUM,\nTHIS ONE'S DAD"   13
"ALL DAD, NO QUESTION"             "ALL DAD,\nNO QUESTION"         11
"DAD STAMP: APPROVED"              "DAD STAMP:\nAPPROVED"          10
"MOSTLY MUM"                       — OK as single line (10)        —
"MOSTLY DAD"                       — OK as single line (10)        —
"LEANING MUM"                      — OK as single line (11)        —
"LEANING DAD"                      — OK as single line (11)        —
"A UNIQUE MIX"                     — OK as single line (12)        —
"ONE OF A KIND"                    — OK as single line (13)        —
```

Note: several of these already have `\n` in the source. The audit confirms most are correctly split. The ones flagged above are the only fixes needed.

---

**End of Spec**
