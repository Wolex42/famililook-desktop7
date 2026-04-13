# Keepsake Product Issues Investigation

**Date:** 2026-04-01
**Authors:** QA Lead Agent, Visual Director Agent
**Scope:** Three keepsake catalogue/template issues — investigation and planning only (no fixes applied)

---

## Issue 1: Card Products in Keepsake Catalogue

### Current State

The keepsake catalogue (`KeepsakeCatalogue.jsx`) displays a "Cards" category containing **four products**:

| Product ID | Label | Price | Vendor | Notes |
|---|---|---|---|---|
| `standard_card` | Playing Card (2.5" x 3.5") | 9.99 | QPMarkets | Individual card |
| `card_deck` | FamiliUno Card Deck (52 cards) | 24.99 | QPMarkets | Full deck — badge "52 cards" |
| `greeting_card` | Greeting Card (5" x 7") | 6.99 | QPMarkets/Prodigi | Folded greeting card — LEGITIMATE keepsake |
| `postcard` | Postcard (6" x 4") | 3.99 | QPMarkets/Prodigi | Postcard — LEGITIMATE keepsake |

The card products are defined in:
- `productCatalog.js` line 26: `products: [PRODUCT_TYPES.STANDARD_CARD, PRODUCT_TYPES.CARD_DECK, PRODUCT_TYPES.GREETING_CARD, PRODUCT_TYPES.POSTCARD]`
- `printProfiles.js` lines 51-72 (`standard_card`) and lines 303-324 (`card_deck`)
- `templateRegistry.js` lines 256-275 — both `standard_card` and `card_deck` use `useLegacyTemplates: true` with empty `components: {}`

The `card_deck` entry in `KeepsakeCatalogue.jsx` also has a specific badge on line 67: `card_deck: "52 cards"`.

### Root Cause

**Duplication of FamiliUno's core product.** The `card_deck` product (52-card personalised FamiliUno deck) is the primary deliverable of FamiliUno, which has its own ordering flow via QPMarkets. Listing it again in the keepsake catalogue:

1. Creates confusion — users see the same product in two places
2. The keepsake template for `card_deck` uses `useLegacyTemplates: true` with an empty `components: {}` object, meaning there is no actual template to render a preview
3. The `standard_card` is similarly problematic — it uses legacy templates (vault_card, trading_card, etc.) which are individual card designs, not a purchasable standalone playing card product

### Impact

- **User confusion**: Two paths to order the same card deck product
- **Broken preview**: `card_deck` has no renderable components in the template registry (`components: {}`) — tapping it in the catalogue will fail to show a preview
- **`standard_card` preview works** via legacy templates but selling individual playing cards as a standalone product is questionable when the full deck is the FamiliUno product

### Recommended Fix

**Remove `standard_card` and `card_deck` from the keepsake catalogue** while preserving `greeting_card` and `postcard` (which are legitimate keepsake products).

Option A (filter at catalogue level — minimal change):
- In `productCatalog.js`, remove `PRODUCT_TYPES.STANDARD_CARD` and `PRODUCT_TYPES.CARD_DECK` from the `cards` category products array
- Remove `card_deck` badge from `KeepsakeCatalogue.jsx` line 67

Option B (filter at display level — safer):
- Add a `hidden: true` flag to `standard_card` and `card_deck` in `PRODUCT_SPECS`
- Filter hidden products in `getCategoryProducts()`

**Do NOT delete the `standard_card` or `card_deck` entries from `PRODUCT_SPECS` or `PRINT_PROFILES`** — they are still used by legacy card templates and FamiliUno's QPMarkets ordering flow.

### Files to Modify

| File | Change |
|---|---|
| `famililook-desktop2/src/components/keepsakes/utils/productCatalog.js` | Remove `STANDARD_CARD` and `CARD_DECK` from cards category products array |
| `famililook-desktop2/src/components/keepsakes/mobile/KeepsakeCatalogue.jsx` | Remove `card_deck` badge entry (line 67) |

### Effort Estimate

**Small** — 2 lines changed, 1 line removed. No test changes needed (existing tests don't assert catalogue product count). Risk: low — only affects catalogue display, not ordering or export pipelines.

---

## Issue 2: Product Preview Content Not Fully Visible + Mug Text Overflow

### Current State

Two related sub-issues:

#### 2a: Wall Art Preview Content Clipped

`CertificateTemplate.jsx` renders at 480px CSS width with a `minHeight: 600px` container. The template uses `overflow: hidden` on the outer container (line 49). Content stacks vertically:
- Header (32px top padding + ~60px content)
- Photo circle (160px + 16px margin)
- Child name (24px)
- Primary message (15px)
- Match percentage badge (~36px)
- Feature grid (8 features in 2 columns, ~6px gap, ~40px per row = ~160px)
- Feature count summary (~50px)
- Optional personalised message (variable)
- Footer (~40px)

**Total minimum height: ~560px** without personalised message, ~600px with. The container has `minHeight: 600px` so basic content fits, but:
- On mobile preview, these templates are scaled down to fit the viewport (typically ~340px wide). The aspect ratio is preserved but the preview container in the mobile flow may clip the bottom.
- The `infographic` variant adds bar charts that are taller than the grid variant.
- When a personalised message is enabled, the content exceeds 600px and the `overflow: hidden` clips it silently.

#### 2b: Mug Text Overflow (Pillbox Overflow)

**MugCeramicPreview.jsx** (SVG preview shown to customer):
- The hero feature callout box is a fixed `170px` wide rect (line 188: `width="170"`) with text rendered at `fontSize="9.5"`.
- Text content is: `"I have your {heroLabel} . {truncateAtWord(heroDetail.description, 28)}"` (line 194)
- `truncateAtWord()` truncates at 28 characters. However, the **combined text** ("I have your " + heroLabel + " . " + 28-char description) can exceed the 170px rect width.
- SVG `<text>` elements do NOT clip or wrap — they overflow their containing `<rect>` and bleed into adjacent areas.
- **No `clipPath` or `textLength` constraint** is applied to this text element.

**CharacterMugTemplate.jsx** (print template, 830x345px):
- Headline text uses `whiteSpace: "pre-line"` and `maxWidth: "100%"` but no explicit text truncation or overflow handling.
- The headline comes from `composeCharacterMug()` which does call `truncateAtWord(text, 35)` (compositionEngine.js line 223) — so headlines are capped at 35 chars.
- However, the font size is 36-42px at `fontWeight: 900` with `textTransform: "uppercase"` and `lineHeight: 0.92`. At these sizes, 35 uppercase characters in Nunito Bold easily exceed the panel width (498px for Hero layout, 373px for Celebration, etc.).
- The container has `overflow: hidden` at the root level (line 659), so text is clipped rather than overflowing — but the user loses content.

**MugWrapTemplate.jsx** (print template, 830x345px):
- Centre panel is 398px wide with 8px horizontal padding each side = 382px usable.
- Headline "more like you" at 22px/800 weight fits.
- Hero feature callout uses `truncateAtWord(heroDetail.description, 28)` — same 28-char limit.
- The callout pill has no `maxWidth` or `overflow` constraint. At `fontSize: 9px` and `fontWeight: 700`, the combined string can overflow the pill's padding boundaries.
- Feature chips use `flexWrap: "wrap"` which is correct, but very long feature labels could overflow individual chips (unlikely with standard 8 features).

### Dimensions and Overflow Points

| Component | Container Width | Font Size | Max Text Length | Overflow Point |
|---|---|---|---|---|
| MugCeramicPreview hero callout | 170px SVG rect | 9.5px | ~50 chars combined | >35 chars combined at 9.5px Georgia |
| CharacterMugTemplate headline (Hero) | 498px - 60px padding = 438px | 36-42px uppercase | 35 chars | >18 uppercase chars at 42px Nunito Black |
| CharacterMugTemplate headline (Celebration) | 373px - 32px padding = 341px | 32-36px uppercase | 35 chars | >15 uppercase chars at 36px Nunito Black |
| MugWrapTemplate hero callout | 382px usable | 9px | ~50 chars combined | Unlikely to overflow at this size |
| CertificateTemplate with personalised msg | 480px, minHeight 600px | Various | 150 chars body | Content exceeds 600px, clipped by overflow:hidden |

### Root Cause

1. **SVG text has no native overflow control** — the MugCeramicPreview renders text in SVG `<text>` elements inside decorative `<rect>` elements, but SVG rects do not clip text unless a `<clipPath>` is explicitly applied.
2. **Headline truncation is calibrated for lowercase** — the 35-character limit in `compositionEngine.js` was set assuming mixed-case text, but the headline is rendered `textTransform: "uppercase"`, which is significantly wider per character.
3. **CertificateTemplate uses fixed minHeight** — when personalised message adds ~60-80px of content, total exceeds 600px and `overflow: hidden` clips the footer.

### Recommended Fix

1. **MugCeramicPreview**: Add a `<clipPath>` to the hero callout rect and apply it to the text, OR reduce the truncation limit from 28 to 20 characters, OR add `textLength` attribute to the SVG `<text>` element to force fitting.

2. **CharacterMugTemplate**: Reduce headline truncation from 35 to 25 characters in `compositionEngine.js`, OR add `overflow: hidden` + `textOverflow: ellipsis` to the headline div (already has `maxWidth: "100%"` but lacks the overflow properties), OR reduce font size for long headlines.

3. **CertificateTemplate**: Change `minHeight: "600px"` to `minHeight: "auto"` or increase to accommodate personalised message content. Alternatively, calculate height dynamically based on content presence.

4. **MugWrapTemplate hero callout**: Add `maxWidth: "90%"`, `overflow: "hidden"`, `textOverflow: "ellipsis"`, `whiteSpace: "nowrap"` to the callout pill div.

### Files to Modify

| File | Change |
|---|---|
| `famililook-desktop2/src/components/keepsakes/MugCeramicPreview.jsx` | Add clipPath to hero callout text (lines 188-195) |
| `famililook-desktop2/src/components/keepsakes/utils/compositionEngine.js` | Reduce headline truncation limit or add uppercase-aware calculation |
| `famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` | Add overflow handling to headline divs in all 4 layouts |
| `famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/MugWrapTemplate.jsx` | Add overflow constraints to hero callout pill |
| `famililook-desktop2/src/components/keepsakes/templates/Products/WallArt/CertificateTemplate.jsx` | Fix container height to accommodate personalised message |

### Effort Estimate

**Medium** — 5 files, ~15 line changes. Requires visual verification on multiple product types and screen sizes. The SVG clipPath change in MugCeramicPreview needs careful coordinate calculation. Risk: medium — visual changes to print output need Prodigi sample verification.

---

## Issue 3: AI-Generated Comments (Personalised Message) Have No Place to Render

### Current State

#### What the system produces

The `usePersonalizedMessage` hook (`hooks/usePersonalizedMessage.js`) generates an object with three fields:

```
{ headline: string, body: string, caption: string }
```

- In dev mode: returns a mock message after 800ms delay
- In production: calls `/generate/personalised-message` API endpoint
- User can edit all three fields via `updateField()`
- Toggle on/off via `toggle()`
- Cached per unique input combination

#### Where the toggle exists

**Desktop flow** (`KeepsakesModal.jsx`):
- Toggle rendered at line 1164-1168, gated by: `PRODUCT_TEMPLATE_REGISTRY[selectedProduct]?.supportsCustomMessage`
- `PersonaliseToggle` component at line 1894 shows toggle switch + editable fields when enabled
- Data injected into template via `useMemo` at lines 210-213: merges `personalise.message` into `data.customMessage`

**Mobile flow** (`KeepsakeMobileFlow.jsx` + `KeepsakeCustomise.jsx`):
- `usePersonalizedMessage()` instantiated at line 123 of `KeepsakeMobileFlow.jsx`
- Passed to `KeepsakeCustomise` at line 478 as `personalise` prop
- Toggle rendered at line 519 of `KeepsakeCustomise.jsx` — **NOT gated by `supportsCustomMessage`** — shows for ALL products when `personalise` prop is truthy
- Data injected at lines 352-354 of `KeepsakeMobileFlow.jsx`

#### Which templates CAN display it

Templates that read `data.customMessage` and render it visually:

| Template | Product Types | Max Body Length | Renders headline? | Renders caption? |
|---|---|---|---|---|
| CertificateTemplate | fine_art_print, framed_canvas, jigsaw_puzzle | 150 chars | Yes | Yes |
| MugWrapTemplate | mug_wrap | 100 chars | No (body only) | No |
| MugCeramicPreview | (preview only, not print) | 60 chars | No (body only) | No |
| MugTimelineTemplate | mug_wrap (timeline variant) | Uses body | Yes | Yes |
| CushionTemplate | cushion | 80 chars | No (body only) | No |
| GreetingCardTemplate | greeting_card | Full body | Yes (as headline) | Yes (as subtitle) |
| PostcardTemplate | postcard | 80 chars | No (body only) | No |
| MothersDayTemplate | fine_art_print, framed_canvas, cushion, greeting_card, postcard (mothers_day style) | 100 chars | No (body only) | No |
| EasterTemplate | (easter variants) | 100 chars | No (body only) | No |
| EasterCardTemplate | greeting_card (easter style) | 35 chars headline | Yes | No |

#### Which templates CANNOT display it

| Template | Product Types | `supportsCustomMessage` in registry? |
|---|---|---|
| CharacterMugTemplate | character_mug | **Yes** (registry line 295) but **NO `data.customMessage` rendering in the component** |
| FamilyMugTemplate | family_mug_set | **Yes** (registry line 282) — needs verification |
| BodysuitTemplate | baby_bodysuit, tshirt_print | No |
| PetFamilyReport | pet_family_report | No |
| Legacy card templates | standard_card, card_deck | No |

#### Critical Finding: CharacterMugTemplate

`CharacterMugTemplate.jsx` is registered with `supportsCustomMessage: true` (templateRegistry.js line 295), meaning the desktop modal WILL show the personalise toggle for character mugs. The user can generate and edit a personalised message. However, **the CharacterMugTemplate component never reads or renders `data.customMessage`**. The message is generated, stored, passed to the order manifest, but **invisible on the product**.

Grep for `customMessage` in CharacterMugTemplate returns zero matches. The composition engine (`composeCharacterMug()`) does not surface the custom message in the plan. The four layout variants (Hero, Celebration, Blend, Gift) have no placeholder for it.

#### Mobile Flow Gap

In the mobile flow, the personalise toggle in `KeepsakeCustomise.jsx` is rendered whenever the `personalise` prop is truthy (line 519: `{personalise && (`). It is NOT gated by `supportsCustomMessage`. This means:

- For products like `baby_bodysuit`, `tshirt_print`, `pet_family_report` — the toggle appears, the user can generate a message, but the template will never render it
- The message IS included in the order manifest (vendorManifest.js line 94), so Prodigi receives metadata that has no visual representation on the product

### Root Cause

1. **CharacterMugTemplate was added after the personalise system** — the `supportsCustomMessage: true` flag was set in the registry (perhaps cargo-culted from mug_wrap) but the component was never updated to render `data.customMessage`
2. **Mobile flow lacks the `supportsCustomMessage` gate** that the desktop flow has at KeepsakesModal.jsx line 1164
3. **No contract enforcement** — there is no test verifying that `supportsCustomMessage: true` in the registry implies the component actually reads and renders `data.customMessage`

### Recommended Fix

**Phase 1 (guard rails — prevent user confusion):**
1. In `KeepsakeCustomise.jsx`, gate the personalise toggle on `PRODUCT_TEMPLATE_REGISTRY[productId]?.supportsCustomMessage` (matching the desktop flow)
2. Remove `supportsCustomMessage: true` from `character_mug` in `templateRegistry.js` UNTIL the template is updated to render it
3. Verify `family_mug_set` template (FamilyMugTemplate) actually renders `data.customMessage` — if not, remove its `supportsCustomMessage` flag too

**Phase 2 (add rendering support):**
1. Add a personalised message zone to CharacterMugTemplate — Visual Director recommends placing it in the right panel of Hero/Gift layouts or centre panel of Celebration/Blend layouts, as a small italic line below the score line
2. Ensure all templates with `supportsCustomMessage: true` have a consistent rendering location

**Phase 3 (test enforcement):**
1. Add a unit test that iterates all products with `supportsCustomMessage: true` in the registry and verifies the default component for each product contains a `customMessage` reference in its source

### Files to Modify

| File | Change |
|---|---|
| `famililook-desktop2/src/components/keepsakes/mobile/KeepsakeCustomise.jsx` | Gate personalise toggle on `supportsCustomMessage` |
| `famililook-desktop2/src/components/keepsakes/utils/templateRegistry.js` | Remove `supportsCustomMessage: true` from `character_mug` (and `family_mug_set` if unverified) |
| `famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` | (Phase 2) Add `data.customMessage` rendering zone |
| `famililook-desktop2/src/components/keepsakes/utils/compositionEngine.js` | (Phase 2) Surface `customMessage` in composition plan |

### Effort Estimate

**Phase 1:** Small — 3-4 line changes across 2 files. Low risk.
**Phase 2:** Medium — requires Visual Director layout spec for message placement on CharacterMugTemplate, plus implementation across 4 layout variants. Needs print sample verification.
**Phase 3:** Small — 1 new test file.

---

## Summary Table

| Issue | Severity | Effort | Priority |
|---|---|---|---|
| 1. Card products in keepsake catalogue | Medium (user confusion + broken preview) | Small | P2 |
| 2a. Wall art preview content clipped | Medium (content hidden from user) | Medium | P2 |
| 2b. Mug text overflow | High (visible on printed product) | Medium | P1 |
| 3. Personalised message has no render target | Medium (user pays for invisible feature) | Small (Phase 1) / Medium (Phase 2) | P1 (Phase 1), P2 (Phase 2) |

**Recommended execution order:**
1. Issue 3 Phase 1 (guard rails) — prevents users paying for invisible feature
2. Issue 1 (remove card products) — quick win, removes confusion
3. Issue 2b (mug text overflow) — affects print quality of paid products
4. Issue 2a (wall art clipping) — affects preview only, not print output
5. Issue 3 Phase 2 (add rendering) — adds value but not blocking
