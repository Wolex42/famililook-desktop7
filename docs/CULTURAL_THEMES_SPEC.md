# Cultural Celebration Themes — Specification
## Black/African/Caribbean Heritage Design Options
## Date: 25 March 2026 — No code until approved

---

## Principle

These are **design styles**, not demographic labels. Any family can choose any theme. They appear alongside existing styles (Certificate, Elegant, Easter) in the StylePicker. Never auto-suggested from photo analysis. Always user-selected.

---

## 1. Three Proposed Themes

### Heritage Gold (Pan-African / Kente-Inspired)

**Concept**: West African textile heritage. Kente cloth = family unity, royalty, pride.

| Token | Hex | Reference |
|-------|-----|-----------|
| primary | `#C8960C` | Kente gold warp thread |
| secondary | `#1B5E20` | Adinkra green (earth/growth) |
| accent | `#B71C1C` | Heritage red (blood/ancestry) |
| text | `#1A0F00` | Deep umber |
| textLight | `#5D4037` | Warm cocoa |
| wash | `#FFF8E1` | Gold wash |
| dark | `#1A0F00` | Rich dark |

**Font**: Cormorant Garamond (Google Fonts, free) — elegant, heritage gravitas
**Header**: "FAMILY HERITAGE"
**Icon**: 🌟
**Description**: "Kente-inspired gold & green"

**Decorative motifs** (SVG):
- **Abusua Pa** (Adinkra: "good family") — stylised tree/cross, corner ornaments
- **Sankofa** (Adinkra: "go back and get it") — bird turning head backward, footer stamp
- **Kente strip border** — horizontal bands of gold/green/red/black geometric rectangles
- **Nkonsonkonson** (Adinkra: "chain link") — interlocking chains, section dividers

**Occasion alignment**: Black History Month, Kwanzaa, year-round heritage

---

### Carnival Spirit (Caribbean Heritage)

**Concept**: Vibrant energy of Caribbean carnival. Notting Hill, Trinidad, Junkanoo.

| Token | Hex | Reference |
|-------|-----|-----------|
| primary | `#FF6D00` | Carnival orange (feather warmth) |
| secondary | `#00BFA5` | Caribbean teal (ocean/island) |
| accent | `#AA00FF` | Masquerade purple |
| text | `#1A1A2E` | Deep navy |
| textLight | `#4A148C` | Plum |
| wash | `#FFF3E0` | Sunset wash |
| dark | `#1A1A2E` | Navy |

**Font**: Quicksand (already loaded) — rounded, warm, approachable
**Header**: "CELEBRATE FAMILY"
**Icon**: 🎉
**Description**: "Vibrant Caribbean celebration"

**Decorative motifs**:
- **Tropical hibiscus** — 5-petal flower, corner decoration
- **Carnival feather fan** — radiating curved arcs, background watermark
- **Dotted wave border** — sinusoidal wave with dot accents (sea + beadwork)
- **Sun burst** — radial lines, background element

**Occasion alignment**: Carnival season, Juneteenth, summer, birthdays

---

### Ubuntu (Southern African / Ndebele-Inspired)

**Concept**: "I am because we are" — Ubuntu philosophy = FamiliLook's core message.

| Token | Hex | Reference |
|-------|-----|-----------|
| primary | `#D84315` | Ndebele terracotta |
| secondary | `#0277BD` | Ndebele sky blue |
| accent | `#F9A825` | Savanna gold |
| text | `#212121` | Charcoal |
| textLight | `#5D4037` | Earth brown |
| wash | `#FBE9E7` | Terracotta wash |
| dark | `#3E2723` | Dark earth |

**Font**: Playfair Display (already loaded) — clean, dignified
**Header**: "WE ARE FAMILY"
**Icon**: 🌍
**Description**: "Warm earth tones, family bond"

**Decorative motifs**:
- **Ndebele geometric border** — bold interlocking triangles + rectangles in primary/secondary/accent
- **Ubuntu hands** — two stylised hands forming a circle/heart
- **Baobab tree silhouette** — family roots and longevity, watermark
- **Concentric circles** — pottery motif for unity, section dividers

**Occasion alignment**: Heritage Day, Kwanzaa, year-round family celebration

---

## 2. Skin Tone Emoji Support

**Current state**: Feature emoji (👃👂💇) use default yellow. Nose, hair, ears accept Fitzpatrick modifiers.

**Proposed**: Add optional `skinTone` prop to EmojiIcon in FeatureIcons.jsx.

| Modifier | Code | Approx. Tone |
|----------|------|-------------|
| Type 1-2 | U+1F3FB | Light |
| Type 3 | U+1F3FC | Medium-Light |
| Type 4 | U+1F3FD | Medium |
| Type 5 | U+1F3FE | Medium-Dark |
| Type 6 | U+1F3FF | Dark |

**User selection**: 5-swatch picker, shown once, saved to `localStorage fl:skinTone`. Opt-in, never auto-detected from photos.

---

## 3. Where These Go in the Codebase

| File | Change |
|------|--------|
| `mugThemes.js` | Add 3 entries to OCCASION_THEMES + OCCASION_HEADERS |
| `templateRegistry.js` | Add 3 TEMPLATE_STYLES entries. Register on: greeting_card, postcard, fine_art_print, framed_canvas, cushion |
| `FeatureIcons.jsx` | Add FITZPATRICK modifiers + skinTone prop to EmojiIcon |
| **NEW** `CulturalMotifs.jsx` | 8 SVG motif components (Adinkra, Kente, Ndebele, Hibiscus, etc.) |
| **NEW** `CulturalHeritageTemplate.jsx` | Shared template that renders appropriate palette + motifs based on culturalTheme prop |

**No changes to**: ageThemes.js, StylePicker.jsx (auto-discovers new styles), backend, BE/FE contract

---

## 4. Sensitivity Rules (NON-NEGOTIABLE)

1. **Always user-selected, never auto-suggested from photo analysis**
2. **Names describe aesthetics, not demographics**: "Heritage Gold" not "African Theme"
3. **Any family can choose any theme** — not gated by appearance
4. **Cultural elements used correctly**: Adinkra symbols have documented meanings. Include tooltip explaining each symbol's meaning on the keepsake
5. **No mixing unrelated cultures**: Adinkra stays on Heritage Gold, Ndebele stays on Ubuntu, Hibiscus stays on Carnival Spirit
6. **Iterative rollout**: Start with Heritage Gold (strongest family alignment), gather feedback before adding others

---

## 5. Rollout Order

| Phase | What | Risk |
|-------|------|------|
| 1 | Heritage Gold theme (mugThemes + templateRegistry + CulturalHeritageTemplate) | LOW |
| 2 | Skin tone emoji picker (FeatureIcons + localStorage) | LOW |
| 3 | Carnival Spirit + Ubuntu themes | LOW |
| 4 | CulturalMotifs.jsx decorative SVGs | MEDIUM (design quality) |

---

*This spec is for your review. No code until approved.*
