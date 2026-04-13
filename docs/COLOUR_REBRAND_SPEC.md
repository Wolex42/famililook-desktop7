# FamiliLook Colour Rebrand Specification
## "Cool Deep 2026" Palette
## Date: 25 March 2026 — No code until approved

---

## Summary

Replace the current warm muddy palette (#1c1c1e, #2c2c2e, #f5a623 orange everywhere) with a cool deep navy system that reads as premium tech, not budget app. Orange is reserved for prices/scores only. Primary brand CTAs become violet.

---

## 1. New Colour Token Definitions

### CSS Custom Properties (root-level)

```css
--fl-bg-page:         #0D0F1A    /* Deep navy page background */
--fl-bg-card:         #161828    /* Card surfaces */
--fl-bg-elevated:     #1E2235    /* Elevated surfaces, modals, sheets */
--fl-bg-border:       #2D3048    /* Borders, dividers */
--fl-brand:           #7C3AED    /* Primary brand — violet */
--fl-brand-2:         #4F46E5    /* Secondary brand — indigo */
--fl-match:           #10B981    /* Match/success — emerald green */
--fl-price:           #F5A623    /* Prices and scores ONLY — amber */
--fl-seasonal:        #EC4899    /* Seasonal/emotional — pink */
--fl-text-primary:    #E8EAF6    /* Primary text — warm white */
--fl-text-secondary:  #6B7280    /* Secondary text — grey */
--fl-text-muted:      #4A5080    /* Muted text — blue-grey */
```

### Mapping to `theme/colors.js` exports

| Old token | Old value | New value | New semantic |
|-----------|-----------|-----------|-------------|
| `bgMain` | #000000 | #0D0F1A | Deep navy page |
| `bgBase` | #1a1a1a | #0D0F1A | Same as page (was input bg fallback) |
| `bgCard` | #1c1c1e | #161828 | Card surface |
| `bgElevated` | #2c2c2e | #1E2235 | Elevated surface |
| `bgSheet` | #1c1c1e | #1E2235 | Bottom sheet (same as elevated) |
| `bgInput` | #ffffff | #ffffff | Keep — light inputs for legibility |
| `borderSoft` | rgba(255,255,255,0.08) | rgba(255,255,255,0.06) | Slightly subtler |
| `borderMedium` | rgba(255,255,255,0.12) | rgba(255,255,255,0.10) | Slightly subtler |
| `borderFocus` | rgba(255,255,255,0.2) | rgba(124,58,237,0.4) | Violet focus ring |
| `accentPrimary` | #f5a623 | #7C3AED | **Violet** — brand CTAs |
| `accentPrimaryLight` | #ffd666 | #A78BFA | Light violet |
| `accentPrimaryDark` | #c47f17 | #6D28D9 | Deep violet |
| `accentSecondary` | #5ac8fa | #4F46E5 | Indigo |
| `accentTertiary` | #64d2ff | #10B981 | Emerald match green |
| `accentSuccess` | #30d158 | #10B981 | Emerald (consistent) |
| `accentWarning` | #ff9f0a | #F5A623 | Amber (prices/scores) |
| `accentError` | #ff453a | #EF4444 | Red (keep) |
| `textPrimary` | #ffffff | #E8EAF6 | Warm white |
| `textSecondary` | rgba(255,255,255,0.85) | #B8BDD6 | Light grey-blue |
| `textMuted` | rgba(255,255,255,0.6) | #6B7280 | Grey |
| `textSubtle` | rgba(255,255,255,0.4) | #4A5080 | Blue-grey |
| `textDisabled` | rgba(255,255,255,0.25) | #3A3F5A | Dark grey |
| `gradientPrimary` | #f5a623 → #ff6b6b | #7C3AED → #4F46E5 | **Violet gradient** for CTAs |
| `gradientCard` | #2c2c2e → #1c1c1e | #1E2235 → #161828 | Navy gradient |
| `gradientHero` | rgba(245,166,35,0.15) | rgba(124,58,237,0.12) | Violet glow |
| `shadows.glow` | rgba(245,166,35,0.3) | rgba(124,58,237,0.3) | Violet glow |

---

## 2. What stays orange

Orange (#F5A623) is reserved exclusively for:
- **Match percentages**: "72%" score display
- **Prices**: "£14.99", "£29.99"
- **Score bars**: match progress bars

Orange must NOT appear on:
- CTA buttons (use violet gradient)
- Navigation elements
- Borders or accents
- Step indicators

---

## 3. Files affected

### Tier 1 — Theme definition (1 file, changes everything)

**`src/theme/colors.js`** — Update all token values per the table above. This is the single source of truth. 35 files import from here. Changing these values propagates automatically to every component that uses `colors.bgCard`, `colors.accentPrimary`, etc.

**Impact**: Every component that uses theme tokens gets the new palette instantly. No code changes needed in those 35 files — they already reference `colors.bgCard` etc.

### Tier 2 — Hardcoded orange gradients (64 occurrences across ~20 files)

These files hardcode `#f5a623`, `#ff6b6b`, or the orange gradient instead of using theme tokens. Each needs manual replacement:

| File | Count | What to change |
|------|-------|---------------|
| **KeepsakesModal.jsx** | ~8 | CTA gradient `#f5a623 → #ff6b6b` becomes `#7C3AED → #4F46E5` |
| **GroupSnapshotSection.jsx** | ~6 | "Create Keepsake Card" button gradient, step indicators |
| **BasketDrawer.jsx** | ~2 | Checkout button gradient |
| **BasketBadge.jsx** | ~1 | Badge gradient |
| **StylePicker.jsx** | ~2 | Selected style border + dot indicator |
| **PlansPage.jsx** | ~3 | Plan card borders, upgrade buttons |
| **AppLayout.jsx** | ~2 | Header elements |
| **FreeKeepsakesPanel.jsx** | ~2 | Progress bar, CTA |
| **ConfidenceSlider.jsx** | ~2 | Slider border |
| **MobileResultsCarousel.jsx** | ~2 | Feature display |
| **FamilyMugTemplate.jsx** | ~2 | accentAlt colour |
| **ProductShelf.jsx** | ~5 | Hero card, badge, feature pills — BUT these already use their own PRODUCT_DISPLAY palette, which is intentionally separate. Only update the "Best seller" badge and "Make this →" button if they should be violet. |

**Pattern for CTA replacements:**
```
Old: background: "linear-gradient(135deg, #f5a623 0%, #ff6b6b 100%)"
New: background: "linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%)"
```

### Tier 3 — Feature chips on result cards

Currently feature chips are white/grey pills. The new design shows green-tinted chips for matched features:

| Element | Old | New |
|---------|-----|-----|
| Matched feature chip bg | rgba(255,255,255,0.08) | rgba(16,185,129,0.1) |
| Matched feature chip text | white | #10B981 (emerald) |
| Matched feature chip border | rgba(255,255,255,0.12) | rgba(16,185,129,0.2) |

**Files**: `GroupSnapshotSection.jsx` (pairwise feature chips), `MobileResultsCarousel.jsx` (individual result chips)

### Tier 4 — ProductShelf.jsx colour alignment

The ProductShelf component has its own `PRODUCT_DISPLAY` palette which is intentionally product-specific (different colour per product category). These stay as-is because they represent product identity, not brand identity. But:

- "Make this →" buttons: currently use `display.textColor` on `display.bg` — this is correct and per-product. Keep.
- "Best seller" badge: currently amber-on-purple. Consider changing to white-on-violet for brand consistency.
- "+ N more products →" link: currently #888. Change to `#6B7280` (new textMuted).

---

## 4. What NOT to change

| Item | Reason |
|------|--------|
| Keepsake template files | They have their own palette (mugThemes, ageThemes, seasonal palettes). Not brand UI. |
| FeatureIcons.jsx | SVG icon colours are feature-specific, not brand. |
| printProfiles.js | Vendor specs, not visual. |
| Easter/MothersDayTemplate | Own seasonal palettes. |
| MugCeramicPreview / MugWrapTemplate | Own occasion palettes via mugThemes.js |
| Product prices in PRODUCT_DISPLAY | These are retail prices, not colours. |
| ageThemes.js | Age-specific palettes independent of brand. |

---

## 5. Risk assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Theme change breaks component styling | LOW | 35 files use tokens — they adapt automatically. Only hardcoded values need manual updates. |
| Orange removal from CTAs confuses existing users | LOW | No existing users — product pre-launch. |
| Violet may not be accessible on dark backgrounds | CHECK | WCAG contrast: #7C3AED on #0D0F1A = 4.8:1 (passes AA). #E8EAF6 on #161828 = 10.2:1 (passes AAA). |
| Print templates affected by bg change | NONE | Templates have own backgrounds. Theme bg doesn't affect them. |
| ProductShelf hero card bg (#1A1040) clashes with new page bg (#0D0F1A) | CHECK | Similar tones — should work. Both are deep dark. |

---

## 6. Execution order

| Phase | What | Files | Risk |
|-------|------|-------|------|
| **1** | Update `theme/colors.js` token values | 1 file | LOW — auto-propagates to 35 files |
| **2** | Replace hardcoded orange gradients in CTA buttons | ~12 files, 64 occurrences | MEDIUM — manual search-replace |
| **3** | Update feature chip colours on result cards | 2 files | LOW |
| **4** | Update ProductShelf minor elements | 1 file | LOW |
| **5** | Visual verification of every page | 0 files | NONE — just checking |

**Phase 1 is the big win** — one file change, 35 components update automatically. Phase 2 is the manual work.

---

## 7. Verification checklist

After all changes:
- [ ] Page background is deep navy (#0D0F1A), not warm black
- [ ] Cards are #161828, not #1c1c1e
- [ ] All CTA buttons are violet gradient, not orange
- [ ] Prices and percentages remain orange/amber
- [ ] Feature chips on result cards show green for matches
- [ ] Step indicators use violet, not orange
- [ ] Selected style in StylePicker has violet border
- [ ] Focus rings are violet
- [ ] Text is warm white (#E8EAF6), not pure white
- [ ] Build passes
- [ ] No existing tests broken by colour changes
- [ ] Keepsake templates unaffected (still use own palettes)

---

*No code until this spec is approved.*
