# CR-0012 Visual Direction — Family Identity Profiles
> Visual Director sign-off required before FE Lead implementation.
> Sub-phase A (composition engine) has no UI — omitted.

---

## Sub-phase B: Identity Sheet (Upload Flow)

Appears inline below the photo slot after upload, matching `FaceNamingSheet` pattern (not a viewport-fixed modal).

### Sheet Container
- **Background:** `colors.bgElevated` (#1E2235)
- **Border:** 1px solid `colors.borderMedium` (rgba 255,255,255,0.10)
- **Border-radius:** `radius.lg` (16px)
- **Padding:** 8px 16px 16px (matches FaceNamingSheet)
- **Box-shadow:** 0 2px 12px rgba(0,0,0,0.3)
- **Animation:** slideUp 280ms cubic-bezier(0.32, 0.72, 0, 1) — iOS spring feel

### Handle Bar
- 40px wide, 4px tall, `colors.borderMedium`, centered, 8px vertical padding

### Header Row
- **Thumbnail:** 48x48px, `radius.sm` (8px), object-fit cover, 3px border `colors.accentSuccess`
- **Title:** `typography.body` (16px/600) `colors.textPrimary` — shows person name
- **Subtitle:** `typography.caption` (12px/400) `colors.textSecondary` — `[COPY: role-and-age-summary]`
- **Done button:** minHeight 44px, minWidth 44px, `colors.accentPrimary` bg, white text, 15px/600, `radius.sm`

### Name Input
- **Label:** `typography.label` (13px/500) `colors.textSecondary`, letterSpacing 0.02em
- **Field:** height 44px, `colors.bgCard` bg, 1px `colors.borderMedium` border, `radius.sm`, 16px font
- **Focus:** border changes to `colors.borderFocus` (rgba 124,58,237,0.4)

### Role Chip Row
- **Section label:** 12px/700 `#9090B0`, uppercase, letterSpacing 0.5px, marginBottom 10px — `[COPY: role-section-label]`
- **Layout:** horizontal scroll, gap 8px, scrollbarWidth none, WebkitOverflowScrolling touch, paddingBottom 4px
- **Chip size:** minHeight 44px, padding 8px 14px, flexShrink 0
- **Chip radius:** 10px
- **Unselected:** 1px solid #2a2a4e, bg #1a1a2e, text 13px/400 #B0B0C8
- **Selected:** 2px solid `colors.accentPrimary`, bg rgba(124,58,237,0.2), text 13px/600 #FFFFFF
- **Transition:** all 0.15s ease
- **Roles:** Mum, Dad, Child, Grandparent, Sibling, Other — each chip has an emoji prefix

### Age Bracket Segmented Control
- **Section label:** same as Role (12px/700 uppercase #9090B0) — `[COPY: age-section-label]`
- **Layout:** 3 equal-width buttons in a flex row, gap 8px
- **Button:** flex 1, minHeight 44px, padding 6px 8px, radius 10px
- **Unselected:** 1px solid #2a2a4e, bg #1a1a2e, text 13px/400 #B0B0C8
- **Selected:** 2px solid `colors.accentPrimary`, bg rgba(124,58,237,0.2), text 13px/600 #FFFFFF
- **Brackets:** Infant (icon), Child (icon), Teen (icon) — matches AGE_CHIPS in KeepsakeCustomise

### Variant Selector (Cultural Themes)
- **Section label:** same pattern — `[COPY: variant-section-label]`
- **Layout:** horizontal scroll, gap 8px
- **Thumbnail:** 64x64px, radius 10px, object-fit cover
- **Unselected:** 2px solid transparent
- **Selected:** 2px solid `colors.accentPrimary`, box-shadow `shadows.glow`
- **Label below thumbnail:** 11px/500 centered, `colors.textSecondary`; selected: `colors.textPrimary`
- **Touch target:** entire 64px width + label row >= 44px height (passes HIG)

---

## Sub-phase C: Character Picker (Keepsake Customise)

Inserted into KeepsakeCustomise's scrollable content area, below the live preview and above style chips.

### Featured Card
- **Dimensions:** 100% width (respects 16px side padding), height 180px
- **Border-radius:** `radius.lg` (16px)
- **Background:** `colors.gradientCard` (180deg #1E2235 to #161828)
- **Border:** 1px solid `colors.borderMedium`
- **Interior:** character portrait left (120x160px, object-fit cover, radius 12px), info right
- **Info block:** name 18px/600 `colors.textPrimary`, role badge below, emotion label below that
- **Badge (auto/manual):** see Badge Styling below

### Emotion Strip
- **Section label:** 12px/700 uppercase #9090B0, letterSpacing 0.5px — `[COPY: emotion-strip-label]`
- **Layout:** horizontal scroll, gap 8px, paddingBottom 4px, scrollbarWidth none
- **Thumbnail:** 56x56px, radius 10px, object-fit cover, flexShrink 0
- **Unselected:** 2px solid transparent, opacity 0.6
- **Selected:** 2px solid `colors.accentPrimary`, opacity 1, box-shadow `shadows.glow`
- **Label below:** 10px/500 centered, `colors.textMuted`; selected: `colors.textPrimary`
- **Transition:** opacity 0.2s ease, border-color 0.15s ease

### Role Chip Row (in picker)
- Identical spec to Sub-phase B Role Chip Row (reuse the same component)

### Badge Styling
- **"Auto-selected" badge:** `[COPY: auto-selected-badge]`
  - Background: rgba(16,185,129,0.15) — green tint
  - Text: 11px/600 `colors.accentSuccess` (#10B981)
  - Padding: 2px 8px, radius full (9999px)
  - Icon: small sparkle/wand prefix
- **"Your pick" badge:** `[COPY: your-pick-badge]`
  - Background: rgba(124,58,237,0.15) — violet tint
  - Text: 11px/600 `colors.accentPrimary` (#7C3AED)
  - Padding: 2px 8px, radius full (9999px)

### Transition Animations
- **Character swap:** crossfade 200ms ease-out on the Featured Card portrait
- **Emotion change:** portrait crossfade 150ms, emotion strip scroll-into-view (smooth)
- **Role change:** chip row updates instantly (no animation needed — selection highlight is sufficient)

---

## Shared Constraints

| Rule | Value | Source |
|---|---|---|
| Min touch target | 44px height AND width | CLAUDE.md / iOS HIG |
| Font family | Inter, system-ui, sans-serif | KeepsakeCustomise |
| 8pt grid | All spacing multiples of 8 (except 4px for xs) | colors.js spacing |
| No horizontal page scroll | overflow hidden on body; only chip rows scroll | Existing pattern |
| Colour tokens only | No raw hex outside colors.js unless matching existing inline values (#9090B0, #2a2a4e, #1a1a2e, #B0B0C8) | Design system |
| Dark theme only | All surfaces use bgMain/bgCard/bgElevated | Existing |

---

## Copy Placeholders (for Copywriter)

| ID | Context | Max chars |
|---|---|---|
| `[COPY: role-section-label]` | Label above role chips in Identity Sheet | 20 |
| `[COPY: age-section-label]` | Label above age segmented control | 20 |
| `[COPY: variant-section-label]` | Label above cultural variant thumbnails | 25 |
| `[COPY: role-and-age-summary]` | Subtitle under person name in sheet header | 40 |
| `[COPY: emotion-strip-label]` | Label above emotion thumbnails in character picker | 20 |
| `[COPY: auto-selected-badge]` | Badge text when engine auto-picks a character | 15 |
| `[COPY: your-pick-badge]` | Badge text when user manually picks a character | 12 |
