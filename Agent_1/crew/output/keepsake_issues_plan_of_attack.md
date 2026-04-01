# Keepsake Product Issues — Plan of Attack
**Date:** 2026-04-01
**Status:** Documented, awaiting CEO prioritisation

---

## Issue 1: Card Products in Keepsake Catalogue
**FMEA:** FMEA-KSK-01 | S:4 O:10 D:2 | RPN: 80
**Impact:** User confusion — cards appear in keepsake catalogue but FamiliUno delivers this product

### Root Cause
`standard_card` and `card_deck` are defined in `productCatalog.js` under the "Cards" category. `card_deck` has `useLegacyTemplates: true` with empty `components: {}` — preview cannot render.

### Fix
- Filter `standard_card` and `card_deck` from `productCatalog.js` catalogue (keep `greeting_card` and `postcard`)
- OR add a `hideFromCatalogue: true` flag to both entries
- Keep the templates/specs for FamiliUno's deck ordering pipeline (don't delete them)

### Files to Modify
- `src/components/keepsakes/utils/productCatalog.js` — add filter
- `src/components/keepsakes/mobile/KeepsakeCatalogue.jsx` — respect filter

### Effort: XS (30 minutes)

---

## Issue 2: Mug Text Overflow + Preview Clipping
**FMEA:** FMEA-KSK-02 | S:7 O:6 D:3 | RPN: 126
**Impact:** Text spills outside containers on mug graphics. User sees broken layout.

### Root Cause
- **MugCeramicPreview.jsx:** SVG hero text (child name + feature callout) has NO `clipPath`. Long names overflow the 170px rect.
- **CharacterMugTemplate.jsx:** Headlines truncated at 35 chars but rendered at 36-42px uppercase Nunito Black. Celebration layout panel is 341px — 35 uppercase chars at 42px overflow.
- **CertificateTemplate.jsx:** `overflow: hidden` + `minHeight: 600px` clips personalised message content.

### Fix (per file)
1. MugCeramicPreview: Add `<clipPath>` to SVG containing the hero text area
2. CharacterMugTemplate: Reduce max chars from 35 to 25 for uppercase headlines, OR reduce font-size to 28px on narrow panels, OR add `overflow: hidden` + `textOverflow: ellipsis`
3. CertificateTemplate: Change `minHeight` to `min-content` or increase to accommodate message

### Files to Modify
- `src/components/keepsakes/MugCeramicPreview.jsx` — SVG clipPath
- `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` — headline overflow
- `src/components/keepsakes/templates/Products/Drinkware/MugWrapTemplate.jsx` — verify same issue
- `src/components/keepsakes/templates/Products/WallArt/CertificateTemplate.jsx` — minHeight

### Effort: M (2-3 hours)

---

## Issue 3: AI Personalised Message Renders Nowhere
**FMEA:** FMEA-KSK-03 | S:9 O:6 D:2 | RPN: 108
**Impact:** Users toggle the feature, pay the £1.99 surcharge, and get NOTHING visible on their product. Revenue + trust risk.

### Root Cause
- `CharacterMugTemplate` has `supportsCustomMessage: true` in templateRegistry
- The toggle appears in the desktop modal AND the mobile flow
- But the template component **NEVER reads `data.customMessage`** — it's ignored
- Mobile flow (KeepsakeCustomise) shows the toggle for ALL products, not just supported ones

### Fix (2 phases)
**Phase 1 — Guard rail (XS):**
- Mobile flow: only show personalised message toggle when template has `supportsCustomMessage: true`
- Read templateRegistry to check support before rendering toggle

**Phase 2 — Implement rendering (M):**
- CharacterMugTemplate: Add a message zone (below headline or on back panel)
- Visual Director needs to specify: where on the mug? What font size? What max length?
- Must work across all 4 layout variants (Celebration, Heritage, Carnival, Ubuntu)
- MugCeramicPreview: Also needs to show the message in SVG preview

### Files to Modify
Phase 1:
- `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` — gate toggle on supportsCustomMessage
- `src/components/keepsakes/KeepsakesModal.jsx` — verify desktop already gates (it does)

Phase 2:
- `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` — add message rendering
- `src/components/keepsakes/MugCeramicPreview.jsx` — add message to SVG preview
- Visual Direction spec needed first

### Effort: Phase 1 XS, Phase 2 M (needs Visual Director spec)

---

## Issue 4: Transparent Export vs Preview Backing
**FMEA:** FMEA-KSK-04 | S:5 O:8 D:3 | RPN: 120
**Impact:** Templates with transparent backgrounds are hard to see on dark preview screen. Light text invisible.

### Current State
| Template | Has Own Background | Export BG | Preview Problem |
|----------|-------------------|-----------|-----------------|
| MugWrap | transparent | #FFFFFF (correct) | OK — dark text |
| CharacterMug | transparent | #FFFFFF (correct) | OK — dark text |
| Certificate | #FDFBF5 (beige) | transparent | OK — has own bg |
| GreetingCard | #FDFBF5 (beige) | transparent | OK — has own bg |
| Postcard | #FDFBF5 (beige) | transparent | OK — has own bg |
| Cushion | transparent | transparent | **PROBLEM — light text on dark bg** |
| Bodysuit | transparent | transparent | Minor — mostly dark text |

### Root Cause
CushionTemplate uses `theme.colors.textLight` (light gray) for feature badges on a transparent background. On the dark preview screen, this text is invisible.

### Fix
- Preview wrapper: add a subtle light backing (e.g., `rgba(255,255,255,0.05)` or a checkered transparency pattern) behind templates that have `transparent` background
- OR: CushionTemplate specifically should use darker text for its feature badges
- Export pipeline: keep transparent — the backing is preview-only

### Files to Modify
- `src/components/keepsakes/KeepsakesModal.jsx` — preview container gets backing for transparent templates
- `src/components/keepsakes/mobile/KeepsakePreview.jsx` — same backing
- `src/components/keepsakes/templates/Products/Home/CushionTemplate.jsx` — fix badge text colour

### Effort: S (1 hour)

---

## Prioritised Execution Order

| Priority | Issue | RPN | Why First |
|----------|-------|-----|-----------|
| 1 | Issue 3 Phase 1 (guard toggle) | 108 | Users paying for invisible feature — revenue risk |
| 2 | Issue 1 (remove cards) | 80 | Quick win, removes confusion |
| 3 | Issue 2 (text overflow) | 126 | Visual quality — what users see when deciding to buy |
| 4 | Issue 4 (preview backing) | 120 | Visibility of products on preview screen |
| 5 | Issue 3 Phase 2 (implement message) | 108 | Needs Visual Director spec first |

**Total effort:** ~4-5 hours for Issues 1-4. Issue 3 Phase 2 is separate sprint.

---

*Documented by QA Lead + Visual Director — 2026-04-01*
*Awaiting CEO prioritisation before implementation*
