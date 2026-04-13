# Age Style Differentiation Specification
## Version 1.0 — Pre-Code. No changes until approved.
## Date: 25 March 2026

---

## Problem

The Age Style selector offers 6 options (Infant, Toddler, Child, Tween, Teen, Adult) but the customer sees almost no visual difference between them. Changing age style shifts a border colour by a few shades — nothing else. This makes the feature feel broken and the product feel cheap.

The infrastructure for rich age differentiation EXISTS in the codebase but is not wired into the product templates:
- `ageThemes.js` defines 6 distinct themes with different fonts, colours, border radii, font sizes, and decoration names
- `FeatureIcons.jsx` has a 3-tier icon system (emoji for kids, line-art for tweens/teens, premium SVG for adults) — never called with the `ageGroup` prop
- Theme decorations (`stars`, `clouds`, `geometric`, `neon`, `elegant`) are defined but never rendered

---

## What the customer should experience

### Infant (0–2) — "Soft & Sweet"
**Feeling**: Gentle, precious, pastel nursery

| Element | Specification |
|---------|--------------|
| Background | Soft pastel gradient (pink → blue → yellow) |
| Photo frame | Large circle (biggest of all ages), thick soft pink border, cloud-like shadow |
| Font | Comic Neue / Comic Sans — round, friendly |
| Feature icons | Emoji tier (native emoji: 👁️ 😊 👃) — big, playful |
| Feature chips | Rounded pills with pastel fills, large padding |
| Score badge | Pill shape, pastel gradient, rounded |
| Decorations | Tiny stars ✦ and hearts ♥ scattered around photo |
| Border radius | 24px (most rounded) |
| Headline | Larger text, simpler language: "I look just like Mummy!" |
| Overall density | Low — lots of whitespace, few elements, big and simple |

### Toddler (2–4) — "Playful & Bright"
**Feeling**: Energetic, colourful, birthday party

| Element | Specification |
|---------|--------------|
| Background | Bright coral → blue → yellow gradient |
| Photo frame | Large circle, bright coral border, playful shadow |
| Font | Quicksand — rounded, bouncy |
| Feature icons | Emoji tier — same as infant but slightly smaller |
| Feature chips | Bright coloured pills, slightly smaller than infant |
| Score badge | Bright gradient, fun shape |
| Decorations | Tiny balloons 🎈 and stars scattered |
| Border radius | 20px |
| Headline | "I look like Mummy!" — energetic tone |
| Overall density | Low-medium — still spacious but more content |

### Child (4–8) — "Pokémon Fun"
**Feeling**: Exciting, collectible, game card

| Element | Specification |
|---------|--------------|
| Background | Pokemon yellow → orange gradient |
| Photo frame | Rounded square (16px radius), thick orange border, energy glow |
| Font | Fredoka One — bold, fun, game-like |
| Feature icons | Emoji tier — bright, recognisable |
| Feature chips | Badge-like with slight depth shadow, orange accents |
| Score badge | Bold, game-UI style with glow effect |
| Decorations | Sparkle ✦ and energy bolt ⚡ accents |
| Border radius | 16px |
| Headline | "I look like Mum!" — confident, excited |
| Overall density | Medium — balanced content and decoration |

### Tween (8–12) — "Cool & Stylish"
**Feeling**: Trendy, confident, social media

| Element | Specification |
|---------|--------------|
| Background | Purple → indigo → teal gradient |
| Photo frame | Rounded square (14px), purple gradient border, geometric shadow |
| Font | Nunito — clean, modern, slightly playful |
| Feature icons | **Teen tier** — single-colour line-art SVGs, purple accent |
| Feature chips | Flat design, purple/teal accent, modern feel |
| Score badge | Flat pill, gradient fill, clean typography |
| Decorations | Geometric shapes (triangles, hexagons) at low opacity |
| Border radius | 14px |
| Headline | "I look like Mum" — matter-of-fact, cool |
| Overall density | Medium-high — more data visible, less decoration |

### Teen (12–18) — "Modern & Sleek"
**Feeling**: Dark mode, neon accents, gaming HUD

| Element | Specification |
|---------|--------------|
| Background | Dark navy → deep blue gradient (#1A1A2E → #0F3460) |
| Photo frame | Sharp rounded square (12px), neon indigo border, subtle glow |
| Font | Inter — clean, professional |
| Feature icons | **Teen tier** — line-art SVGs, indigo/pink neon accents |
| Feature chips | Dark glass-morphism pills, neon text, subtle border |
| Score badge | Neon gradient, dark background, tech feel |
| Decorations | Minimal — thin neon lines, no scatter elements |
| Border radius | 12px |
| Text colour | Light on dark (#ECEFF1 on dark bg) |
| Headline | "I look like Mum" — minimal, no exclamation |
| Overall density | High — data-focused, compact, sophisticated |

### Adult (18+) — "Elegant & Sophisticated"
**Feeling**: Premium, gold accents, certificate quality

| Element | Specification |
|---------|--------------|
| Background | Navy → deep navy gradient (#1E3A5F → #0D2137) |
| Photo frame | Circle or oval, gold border, elegant shadow |
| Font | Playfair Display — serif, sophisticated, editorial |
| Feature icons | **Premium tier** — detailed gradient SVGs with anatomical detail |
| Feature chips | Elegant thin-border pills, gold accent on dark, subtle |
| Score badge | Gold gradient on dark, serif typography |
| Decorations | Ornate thin-line flourishes at corners |
| Border radius | 8px (sharpest) |
| Text colour | White/cream on dark (#FFFFFF, #B8B8B8) |
| Headline | "I look like Mum" — understated, elegant italic |
| Overall density | High — refined, lots of data, premium feel |

---

## What changes per product template

### Rule: Each template reads theme properties and applies them

Every product template already receives `ageTheme` as a prop. The fix is to USE the properties it already has.

### Changes required per element:

**1. Feature Icons — pass ageGroup prop**

Current (every template):
```jsx
<FeatureIcon feature={key} size={12} />
```

Fixed:
```jsx
<FeatureIcon feature={key} size={12} ageGroup={ageTheme.id} />
```

This single change activates the 3-tier icon system: emoji for kids, line-art for tweens/teens, premium SVG for adults. Affects every template that renders feature icons.

**2. Font family — use theme font**

Current (most templates): Mix of hardcoded fonts and `theme.fontFamily` on the wrapper only.

Fixed: Apply `theme.fontFamily` to headlines, names, and messages — not just the wrapper. Key text elements need explicit `fontFamily: ageTheme.fontFamily`.

**3. Photo frame shape — use theme borderRadius**

Current: Hardcoded `borderRadius: "50%"` (always circle) or hardcoded `"16px"`.

Fixed: Use `ageTheme.borderRadius` for photo frames. Result: 24px round for infant → 8px sharp for adult.

**4. Colours — use theme palette instead of hardcoded accents**

Current: Most templates use `theme.colors.primary` for the main accent but hardcode everything else.

Fixed: Use `theme.colors.primary` for accent, `theme.colors.secondary` for secondary, `theme.colors.text` for text, `theme.colors.cardBorder` for borders, `theme.colors.cardBg` for background gradients.

**5. Decorations — render age-appropriate scatter elements**

Current: Not rendered anywhere.

Fixed: Add a small `Decorations` sub-component that renders 3-4 tiny elements based on `ageTheme.decorations`. Each decoration type maps to a small SVG or emoji:
- `stars` → tiny ✦ at random positions, low opacity
- `hearts` → tiny ♥
- `balloons` → tiny 🎈
- `geometric` → small triangles/hexagons
- `neon` → thin glowing lines
- `elegant` → thin ornate corners
- `minimal` → nothing (teen)

Keep decorations subtle — they're flavour, not the main content.

**6. Font sizes — use theme fontSize**

Current: Hardcoded `fontSize: "16px"` etc.

Fixed: Use `ageTheme.fontSize.title` for headlines, `ageTheme.fontSize.subtitle` for names, `ageTheme.fontSize.body` for features/scores.

**7. Card shadow and border — use theme cardStyle**

Current: Hardcoded or using `theme.colors.cardBorder` only.

Fixed: Apply `ageTheme.cardStyle.boxShadow` and `border: ${ageTheme.cardStyle.borderWidth} solid ${ageTheme.colors.cardBorder}`.

---

## IMPORTANT: Teen and Adult themes use DARK backgrounds

The teen and adult themes define dark card backgrounds (`#1A1A2E`, `#1E3A5F`) with light text (`#ECEFF1`, `#FFFFFF`). This means:

- For **paper products** (greeting cards, postcards, fine art prints, certificates) — the dark background IS part of the design. The card prints with the dark background. Text is light. This is correct and looks premium.
- For **surface products** (mugs, t-shirts, cushions) — the dark background must NOT render (transparent bg for vendor). But the light text from teen/adult themes would then be invisible on white surfaces.

**Resolution**: Surface product templates must override text colours when `ageTheme.id === "teen" || ageTheme.id === "adult"` AND the product requires transparent background. Use a helper:

```js
function resolveTextColor(ageTheme, isTransparentProduct) {
  if (isTransparentProduct && (ageTheme.id === "teen" || ageTheme.id === "adult")) {
    return { text: "#1a1a1a", textLight: "#666666" };
  }
  return { text: ageTheme.colors.text, textLight: ageTheme.colors.textLight };
}
```

Paper products always use theme colours as-is. Surface products override light-on-dark to dark-on-transparent for teen/adult.

---

## Files to change

| File | Changes |
|------|---------|
| **PostcardTemplate.jsx** | Apply theme font, borderRadius, colours, fontSize, ageGroup to FeatureIcon |
| **GreetingCardTemplate.jsx** | Same + decorations |
| **CertificateTemplate.jsx** | Same (already uses some theme props) |
| **CushionTemplate.jsx** | Same + transparent bg override for teen/adult |
| **BodysuitTemplate.jsx** | Same (already uses theme) + ageGroup on FeatureIcon |
| **MugWrapTemplate.jsx** | ageGroup on FeatureIcon + transparent override for teen/adult |
| **MugCeramicPreview.jsx** | age-aware icon rendering |
| **PetFamilyReport.jsx** | Same |
| **EasterCardTemplate.jsx** | ageGroup on FeatureIcon |
| **MothersDayTemplate.jsx** | ageGroup on FeatureIcon |
| **FamilyMugTemplate.jsx** | Same + transparent override |

### Files NOT changed
- `ageThemes.js` — already correct
- `FeatureIcons.jsx` — already correct, just needs to be called with `ageGroup`
- Legacy card templates (TradingCard, PokemonCard, etc.) — these already have their own rich theming

---

## Implementation order

1. **Phase 1 — Quick wins (1 change, big impact)**
   - Add `ageGroup={ageTheme.id}` to every `<FeatureIcon>` call in all product templates
   - This alone activates emoji/line-art/premium icons across the board

2. **Phase 2 — Font and sizing**
   - Apply `ageTheme.fontFamily` to key text elements
   - Apply `ageTheme.fontSize` to headlines, names, scores
   - Apply `ageTheme.borderRadius` to photo frames and cards

3. **Phase 3 — Colour depth**
   - Apply full theme colour palette (primary, secondary, cardBg, cardBorder)
   - Add transparent-product override for teen/adult themes
   - Apply `ageTheme.cardStyle` (shadow, border width)

4. **Phase 4 — Decorations**
   - Create `AgeDecorations` component
   - Add to templates that benefit from scatter elements
   - Keep subtle — decorations enhance, not dominate

---

## Acceptance criteria

- [ ] Selecting Infant vs Adult shows dramatically different visual identity
- [ ] Feature icons change tier: emoji (infant/toddler/child) → line-art (tween/teen) → premium SVG (adult)
- [ ] Font changes noticeably: rounded playful (infant) → clean modern (teen) → serif elegant (adult)
- [ ] Photo frame shape varies: big round (infant) → sharp square (adult)
- [ ] Colours are dramatically different, not just a shade shift
- [ ] Teen/adult dark themes render correctly on paper products (dark bg + light text)
- [ ] Teen/adult on surface products (mugs, cushions, t-shirts) override to dark text on transparent
- [ ] No invisible text on any product × age combination

---

*This spec is the single source of truth. No code until approved.*
