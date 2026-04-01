# QA Verification: Keepsake Bug Batch — Fix Validation

**Date:** 2026-04-01
**Author:** QA Lead Agent
**Workflow:** bug_fix Step 4 — Verify Fixes Against Acceptance Criteria
**Tests:** 1090 passed. Build succeeded.

---

## FIX 1 — KSK-04: Transparent Preview Backing

### Verification Method
Read `KeepsakeCustomise.jsx` and `KeepsakePreview.jsx` in full. Checked the `!isMug && !isCard` branch in both files.

### Findings

**KeepsakeCustomise.jsx (lines 237-258):**
The `!isMug && !isCard` branch now wraps `ProductMockup3D` in a container with:
```jsx
background: "#F7F6F4",
borderRadius: "16px",
padding: "12px",
border: "1px solid #E8E6E3",
boxShadow: "0 2px 12px rgba(0, 0, 0, 0.08)",
```
This provides a warm off-white backing behind all transparent templates (CushionTemplate, etc.) on the dark `#0D0F1A` page background.

**KeepsakePreview.jsx (lines 265-286):**
Identical backing container applied in the preview step:
```jsx
background: "#F7F6F4",
borderRadius: "16px",
padding: "12px",
border: "1px solid #E8E6E3",
boxShadow: "0 2px 12px rgba(0, 0, 0, 0.08)",
```

### Acceptance Criteria Check

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| AC-1 | CushionTemplate text visible on dark preview backgrounds | **PASS** | `#F7F6F4` backing ensures all theme-coloured text (dark grays, primaries) is readable — line 239 (Customise), line 267 (Preview) |
| AC-2 | Feature badge labels readable on dark preview background | **PASS** | Backing container surrounds the entire ProductMockup3D, so all child elements render against light background |
| AC-3 | Preview area has subtle backing for transparent templates | **PASS** | Both files use `#F7F6F4` with `16px` border radius, `12px` padding, subtle border and shadow |
| AC-4 | Export transparency NOT affected | **PASS** | The backing is applied only to the preview wrapper div, not to the template itself. CushionTemplate still renders with `background: "transparent"`. The export pipeline (cardExport.js) renders from the template ref, not from this preview wrapper. |
| AC-5 | Match badge text visible | **PASS** | White on gradient, unchanged |

**FIX 1 VERDICT: PASS**

---

## FIX 2 — KSK-02: Mug Text Overflow

### Verification Method
Read `CharacterMugTemplate.jsx`, `characterHeadlines.js`, and `MugCeramicPreview.jsx` in full.

### Findings

**CharacterMugTemplate.jsx — Headline `overflow: hidden` on all 4 layouts:**

| Layout | Line | `overflow: hidden` present? |
|--------|------|-----------------------------|
| HeroLayout (A) | 236 | **YES** — `overflow: "hidden"` in headline div style |
| CelebrationLayout (B) | 357 | **YES** — `overflow: "hidden"` in headline div style |
| BlendLayout (C) | 455 | **YES** — `overflow: "hidden"` in headline div style |
| GiftLayout (D) | 604 | **YES** — `overflow: "hidden"` in headline div style |

All 4 headline divs also have `maxWidth: "100%"` and `whiteSpace: "pre-line"`, so overflow-hidden acts as a safety net if text exceeds the container width.

**characterHeadlines.js — MAX_HEADLINE_CHARS and safeName():**

- `MAX_HEADLINE_CHARS = 28` confirmed at line 117
- `safeName()` at lines 101-105:
  - Names <= 12 chars: used as-is
  - Names 13+ chars with hyphen: first segment extracted (e.g. "CHRISTOPHER-JAMES" -> "CHRISTOPHER")
  - Names 13+ chars without hyphen: returns `null` (signals to skip name-bearing templates)
- `hasNamePlaceholder()` at lines 112-114 filters out `{child}` and `{winner}` templates when safeName returns null
- SHORT_FALLBACK pool at lines 526-537 has 10 entries: "MINI ME", "FAMILY\nGENES", "LOOK\nALIKE", "CHIP OFF\nTHE BLOCK", "SPITTING\nIMAGE", "FAMILY\nTIES", "IT'S A\nMATCH", "JUST LIKE\nYOU", "THE PROOF\nIS HERE", "LIKE PARENT\nLIKE CHILD"
- Character count check at lines 515-539: if resolved headline exceeds 28 chars (excluding newlines), iterates pool for a shorter alternative, then falls back to SHORT_FALLBACK

**MugCeramicPreview.jsx — Hero rect and truncation:**

- Hero feature callout rect at line 193: `x={artCx - 100}`, `width="200"` — that is 200px wide (was 170px per the QA assessment, now widened to 200px)
- Hero description truncation at line 199: `truncateAtWord(heroDetail.description, 18)` — limit is 18 chars (was 22 per assessment, now reduced to 18)
- Clip path `mugHeroTextClip` at lines 105-107 constrains all hero text to `mugX+12` through `mugW-24` = 286px effective width

### Acceptance Criteria Check

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| AC-1 | SVG hero text does not visually overflow mug body bounds | **PASS** | Rect widened to 200px (line 193), description truncated at 18 chars (line 199), clip path catches any residual overflow |
| AC-2 | CharacterMugTemplate headline does not overflow its container | **PASS** | `overflow: "hidden"` on all 4 layout headline divs (lines 236, 357, 455, 604) |
| AC-3 | Feature subline truncated before visual overflow | **PASS** | 50-char limit at characterHeadlines.js line 547-548 |
| AC-4 | Score line and speech bubble overflow-safe | **PASS** | ScoreLine has `overflow: "hidden"` + `textOverflow: "ellipsis"` (lines 171-172), SpeechBubble has same (lines 78-79) |
| AC-5 | SVG hero text rect width matches actual text bounding box | **PASS** | Widened from 170px to 200px, combined with 18-char truncation, fits within 286px clip path |
| AC-6 | CharacterMugTemplate headline containers have `overflow: hidden` | **PASS** | Confirmed on all 4 layouts |
| AC-7 | MAX_HEADLINE_CHARS is 28 | **PASS** | Line 117 |
| AC-8 | safeName() handles long names | **PASS** | Lines 101-105, hyphenated names split, single long names trigger template filtering |
| AC-9 | SHORT_FALLBACK pool expanded | **PASS** | 10 entries at lines 526-537 |

**FIX 2 VERDICT: PASS**

---

## FIX 3 — KSK-01: Card Products Removed from Catalogue

### Verification Method
Read `productCatalog.js` in full.

### Findings

**productCatalog.js line 27 — `cards.products` array:**
```js
products: [PRODUCT_TYPES.GREETING_CARD, PRODUCT_TYPES.POSTCARD],
```

`PRODUCT_TYPES.STANDARD_CARD` and `PRODUCT_TYPES.CARD_DECK` are **not present** in the array. Only `GREETING_CARD` and `POSTCARD` remain.

This was the hardening fix recommended in the QA assessment (AC-6). The intent is now explicit in the data structure — card products that should not appear in the catalogue are not listed, rather than relying on a runtime `hideFromCatalogue` filter.

### Acceptance Criteria Check

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| AC-1 | `standard_card` NOT in `PRODUCT_CATEGORIES.cards.products` | **PASS** | Line 27 — only GREETING_CARD and POSTCARD listed |
| AC-2 | `card_deck` NOT in `PRODUCT_CATEGORIES.cards.products` | **PASS** | Line 27 — only GREETING_CARD and POSTCARD listed |
| AC-3 | `greeting_card` remains in cards category | **PASS** | `PRODUCT_TYPES.GREETING_CARD` present at line 27 |
| AC-4 | `postcard` remains in cards category | **PASS** | `PRODUCT_TYPES.POSTCARD` present at line 27 |
| AC-5 | FamiliUno deck ordering pipeline unaffected | **PASS** | Deck ordering uses `card_deck` product type directly via QPMarkets flow, not via category browsing. Removing from `PRODUCT_CATEGORIES` does not affect the QPMarkets order path. |

**FIX 3 VERDICT: PASS**

---

## Overall Verification Summary

| Fix | Issue ID | Description | Verdict |
|-----|----------|-------------|---------|
| FIX 1 | KSK-04 | Transparent preview backing | **PASS** |
| FIX 2 | KSK-02 | Mug text overflow | **PASS** |
| FIX 3 | KSK-01 | Card products in catalogue | **PASS** |

**Tests:** 1090 passed, 0 failed.
**Build:** Succeeded.

---

## Regression Assessment

| Risk Area | Status | Notes |
|-----------|--------|-------|
| Export pipeline (KSK-04 fix) | SAFE | Backing div is preview-only, not part of export DOM tree |
| Mug headline rendering (KSK-02 fix) | SAFE | `overflow: hidden` is a safety net; 28-char engine limit + safeName() prevent most overflows before CSS is involved |
| FamiliUno deck ordering (KSK-01 fix) | SAFE | QPMarkets flow references `card_deck` product type directly, independent of category membership |
| Other keepsake products | SAFE | No changes to wall art, apparel, home, pet, or digital categories |

---

## FINAL VERDICT: ALL 3 FIXES PASS

All acceptance criteria met. No regression risks identified. Ready for deployment.

**QA Lead sign-off:** Verification complete. All 3 fixes validated against original assessment criteria with specific line-number evidence.
