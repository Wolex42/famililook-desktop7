# Keepsake System — Master Fix Plan
## Consolidated from Design Lead + UX Researcher + QA Lead audits
## Date: 25 March 2026 — No code until approved

---

## Current State: 3 WORKS, 15 DEGRADED, 3 BROKEN out of 21 product paths

---

## PRIORITY 1: Revenue & Legal (fix before any customer pays)

### P1.1 — Plan gate bypass in Classic Cards mode
**Severity**: CRITICAL — free users can order physical products
**What happens**: Classic Cards footer has "Add to Basket" and "Buy Now" with NO `canOrderMerchandise()` check. Modern flow has the gate (line 896). Classic flow does not (lines 1067-1078).
**Fix**: Add `canOrderMerchandise()` check to classic mode footer, matching the modern flow. Show "Upgrade to Plus" link for free users.
**Files**: KeepsakesModal.jsx lines 1067-1078
**Risk**: Zero — adding a conditional wrapper

### P1.2 — Personalised message charges £1.99 on templates that ignore it
**Severity**: CRITICAL — consumer rights issue, charging for invisible feature
**What happens**: PersonaliseToggle appears on ALL products. 14 of 20 templates ignore `data.customMessage`. Customer pays £1.99, message never appears on the product.
**Fix**: Hide the PersonaliseToggle when the active template does not support customMessage. Add a `supportsCustomMessage` flag to each templateRegistry entry.
**Templates that support it**: GreetingCardTemplate, GreetingCardInterior, MugWrapTemplate, MugTimelineTemplate, EasterCardTemplate, MugCeramicPreview
**Templates that don't**: Everything else (14 templates)
**Files**: templateRegistry.js (add flag), KeepsakesModal.jsx (conditionally render toggle)
**Risk**: Low — hiding a toggle, no template changes

### P1.3 — Card Deck product renders wrong content
**Severity**: HIGH — misleading product
**What happens**: `card_deck` has `useLegacyTemplates: true` but no entry in `CARD_COMPONENTS`. Customer selects Card Deck, sees a random Winner Declaration card.
**Fix**: Remove `card_deck` from the Cards category in productCatalog.js. Card deck ordering should go through the dedicated DeckCheckoutPage, not the keepsakes modal.
**Files**: productCatalog.js line 26
**Risk**: Zero — removing a broken entry

---

## PRIORITY 2: Preview Layout (what the customer sees before buying)

### P2.1 — Universal contain-fit scaling for flat view
**Severity**: HIGH — 7 products clip on mobile, 2 clip on desktop
**What happens**: Templates render at native CSS dimensions (up to 830px). The preview container is ~544px desktop, ~300px mobile. Wider templates get clipped by `overflow: hidden`.
**Fix**: Wrap all flat-view templates in a scaling container:
```jsx
const containerRef = useRef(null);
const [containerWidth, setContainerWidth] = useState(400);
// On mount/resize, measure containerRef.current.offsetWidth

const { renderWidth, renderHeight } = PRODUCT_TEMPLATE_REGISTRY[selectedProduct];
const scale = Math.min(1, containerWidth / renderWidth);

<div ref={containerRef} style={{ width: "100%", overflow: "hidden" }}>
  <div style={{
    width: renderWidth,
    transformOrigin: "top center",
    transform: `scale(${scale})`,
    marginBottom: scale < 1 ? -(renderHeight * (1 - scale)) : 0,
  }}>
    {/* template renders here */}
  </div>
</div>
```
**Works for ALL products** — no per-product branching. Never enlarges (capped at 1.0). Collapses dead vertical space.
**Files**: KeepsakesModal.jsx (flat view block, ~lines 795-810)
**Risk**: Low — CSS transform only, no template changes

### P2.2 — Mug flat view should use SVG ceramic preview
**Severity**: MEDIUM — mug flat view clips 830px panoramic strip
**What happens**: MugWrapTemplate at 830px is always wider than the container. Even with scaling, the panoramic strip at 0.36x is barely legible.
**Fix**: For mug_wrap and family_mug_set, the flat view should render MugCeramicPreview (SVG, viewBox-based, scales perfectly) instead of the HTML panoramic strip. The hidden cardRef still uses MugWrapTemplate for export.
**Files**: KeepsakesModal.jsx (flat view mug special case)
**Risk**: Low — MugCeramicPreview already works

### P2.3 — Mockup text illegibility caption
**Severity**: LOW — T-shirt/bodysuit/cushion mockups have text at 3-5px effective size
**What happens**: The mockup artwork zone is physically small (44% of mockup width for T-shirts). At 360px mockup width, artwork is 158px — template text at 10px becomes 4.4px.
**Fix**: Add a small caption below mockup views where scale < 0.5: "Tap 'Flat Design' to see full details". This is what Shutterfly, Vistaprint, etc. do.
**Files**: KeepsakesModal.jsx (after mockup render block)
**Risk**: Zero — adding text

### P2.4 — Revert `overflow: visible` back to `overflow: hidden`
**Severity**: HIGH — current state has content bleeding outside the preview container
**What happens**: I changed overflow to visible to fix card cutoff, but this made content bleed outside the rounded container, looking worse.
**Fix**: Revert to `overflow: hidden`. The contain-fit scaling (P2.1) will prevent content from being clipped because it scales to fit first.
**Files**: KeepsakesModal.jsx line 706
**Risk**: Zero — reverting to previous state

---

## PRIORITY 3: Personalised Message on More Templates

### P3.1 — Fix mug personalised message (hidden when 8 features)
**Severity**: HIGH — customer pays £1.99, message invisible on standard analyses
**What happens**: `hasAIComment = Boolean(data.customMessage?.body) && featureCount <= 6`. All standard analyses have 8 features, so condition is always false.
**Fix**: Remove the `featureCount <= 6` gate. Show the personalised message always when present. If vertical space is tight, reduce feature chip rows from 2 to 1 and use the saved space for the message.
**Files**: MugWrapTemplate.jsx line 41, MugCeramicPreview.jsx line 26
**Risk**: Low — removing a condition, may need minor layout adjustment

### P3.2 — Add customMessage support to product templates that have space
Templates with physical space for a message but currently ignoring it:
- **PostcardTemplate** — add message below the feature list (right side has vertical space)
- **CertificateTemplate** — add message below the feature grid (used for fine_art, framed_canvas, jigsaw)
- **CushionTemplate** — add message below the match badge (centre has space)
- **MothersDayTemplate** — add message below the feature grid
- **EasterTemplate** — add message below the score line

**Files**: Each template file
**Risk**: Medium — layout changes to 5 templates. Do one at a time, verify each before moving to next.

---

## PRIORITY 4: Template Rendering Bugs

### P4.1 — CushionTemplate ring assumes exactly 8 features
**What happens**: `angle = (index * (360 / 8) - 90)` hardcodes 8. Fewer features = gaps, more = overlaps.
**Fix**: Replace `8` with `featureEntries.length`.
**Files**: CushionTemplate.jsx line 129
**Risk**: Zero

### P4.2 — Missing ageGroup on 2 remaining FeatureIcon calls
**What happens**: MugWrapTemplate line 86 and FamilyMugTemplate line 365 don't pass ageGroup.
**Fix**: MugWrapTemplate doesn't receive ageTheme (uses occasion system). Skip. FamilyMugTemplate needs ageTheme threaded through to ChildColumn.
**Files**: FamilyMugTemplate.jsx
**Risk**: Low

### P4.3 — T-shirt style selection is cosmetic only
**What happens**: BodysuitTemplate doesn't accept `style` prop. Portrait and Playful render identically.
**Fix**: Either (a) remove the style picker for tshirt_print by changing to single style, or (b) add style handling to BodysuitTemplate.
**Recommendation**: Option (a) — honest about capability.
**Files**: templateRegistry.js (tshirt_print styles array)
**Risk**: Zero

### P4.4 — MugWrapTemplate flat view receives wrong props
**What happens**: Flat view passes `{ data, ageTheme, style }` but MugWrapTemplate expects `{ data, occasion }`. Works by accident (occasion defaults to "generic").
**Fix**: Pass correct props: `{ data, occasion: "generic" }` in the flat view.
**Files**: KeepsakesModal.jsx (flat view createElement for mug)
**Risk**: Zero

---

## PRIORITY 5: Navigation Polish

### P5.1 — Navigation history already implemented
The navHistory stack was added earlier in this session. Verify it works for all paths:
- Cards → Standard Card → Back → should return to Cards product list ✓
- Pets → Style → Back → should return to Category ✓
- Preview → Back → should return to Style or Product ✓

### P5.2 — Reset showMockup on forward navigation
Already implemented: `setShowMockup(false)` added to `handleSelectCategory` and `handleSelectProduct`.

---

## Execution Order

| Phase | Items | Estimated Changes | Risk |
|-------|-------|------------------|------|
| **Phase A** (do now) | P1.1, P1.2, P1.3, P2.4 | 4 small edits | Zero |
| **Phase B** (do next) | P2.1, P2.2, P2.3 | 1 scaling wrapper + 2 special cases | Low |
| **Phase C** (then) | P3.1, P4.1, P4.3, P4.4 | 4 targeted fixes | Low |
| **Phase D** (last) | P3.2 | 5 templates get customMessage support, one at a time | Medium |
| **Skip** | P4.2 (FamilyMug ageGroup threading), P5.1-5.2 (already done) | — | — |

---

## Files Changed Per Phase

**Phase A** (4 files):
- KeepsakesModal.jsx — plan gate + personalise toggle visibility + overflow revert
- templateRegistry.js — add `supportsCustomMessage` flag
- productCatalog.js — remove card_deck

**Phase B** (1 file):
- KeepsakesModal.jsx — contain-fit scaling wrapper + mug flat SVG + mockup caption

**Phase C** (4 files):
- MugWrapTemplate.jsx — remove featureCount gate
- MugCeramicPreview.jsx — remove featureCount gate
- CushionTemplate.jsx — fix ring calculation
- templateRegistry.js — tshirt to single style

**Phase D** (5 files, one at a time):
- PostcardTemplate.jsx
- CertificateTemplate.jsx
- CushionTemplate.jsx
- MothersDayTemplate.jsx
- EasterTemplate.jsx

---

*This plan is the single source of truth. No code until Phase A is approved.*
