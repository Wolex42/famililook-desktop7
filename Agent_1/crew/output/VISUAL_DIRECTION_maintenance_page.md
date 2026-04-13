===============================================
  VISUAL DIRECTION — FamiliLook Maintenance Notice Board
  Visual Director — 2026-04-09
===============================================

PRODUCT: FamiliLook (temporary homepage replacement — ~2 weeks)
PRINT TARGET: N/A
MOBILE TARGET: 375px primary, scaling to 1440px desktop
CONTEXT: Replaces famililook.com homepage during maintenance window.
         Single standalone page. No router, no SPA shell needed.

CRITICAL DISTINCTION:
  This spec is for: STANDALONE WEB PAGE (not a component inside the existing app)
  It must feel like a natural extension of the existing FamiliLook site.
  Uses the exact same colour palette, dark background, violet accents, and
  warm-premium tone. Not a "sorry" page — a purposeful, confident pause.

---

## VISUAL HIERARCHY

  1. FamiliLook wordmark + headline — immediate brand recognition
  2. "Back in ~2 weeks" badge — reassurance, not alarm
  3. Prologue card — the emotional core, why this matters
  4. Feedback form — the actionable element, collects intent
  5. Footer — legal, social presence

---

## FULL-PAGE LAYOUT — Mobile (375px)

```
┌─────────────────────────────────────┐  375px viewport
│          safe-area-inset-top        │
│                                     │
│  ┌─────────────────────────────┐    │
│  │      SECTION 1 — HEADER     │    │
│  │                              │    │
│  │   ╔═══════════════════════╗  │    │
│  │   ║   FamiliLook wordmark ║  │    │  wordmark: 140px wide
│  │   ╚═══════════════════════╝  │    │
│  │          16px gap            │    │
│  │   ┌─────────────────────┐   │    │
│  │   │  HEADLINE (2 lines) │   │    │  h1: 26px / 700
│  │   └─────────────────────┘   │    │
│  │          12px gap            │    │
│  │      ╭──────────────╮       │    │
│  │      │ Back in ~2   │       │    │  chip: 14px / 500
│  │      │   weeks      │       │    │  bg: rgba(124,58,237,0.15)
│  │      ╰──────────────╯       │    │  text: #A78BFA
│  │                              │    │
│  └──────────────────────────────┘    │
│              32px gap                │
│  ┌──────────────────────────────┐   │
│  │    SECTION 2 — PROLOGUE      │   │
│  │    CARD                      │   │
│  │                              │   │  card bg: linear-gradient(
│  │   padding: 28px 24px         │   │    160deg,
│  │                              │   │    rgba(124,58,237,0.18) 0%,
│  │   ┌──────────────────────┐   │   │    rgba(79,70,229,0.10) 100%)
│  │   │  84 words across     │   │   │  border: 1px solid
│  │   │  4 short paragraphs  │   │   │    rgba(124,58,237,0.25)
│  │   │                      │   │   │  radius: 16px
│  │   │  16px body text      │   │   │
│  │   │  line-height: 1.65   │   │   │
│  │   │  paragraph-gap: 14px │   │   │
│  │   └──────────────────────┘   │   │
│  │                              │   │
│  │  Optional: subtle abstract   │   │
│  │  connection motif (SVG)      │   │
│  │  bottom-right, 80x80px,     │   │
│  │  opacity 0.08                │   │
│  │                              │   │
│  └──────────────────────────────┘   │
│              32px gap                │
│  ┌──────────────────────────────┐   │
│  │    SECTION 3 — FEEDBACK      │   │
│  │    FORM                      │   │
│  │                              │   │
│  │  "Share your thoughts"       │   │  h2: 22px / 600
│  │  subtitle                    │   │  body: 14px / 400
│  │          16px gap            │   │
│  │  ┌──────────────────────┐   │   │
│  │  │  Feedback textarea   │   │   │  min-h: 140px
│  │  │  placeholder text    │   │   │  bg: #1E2235
│  │  │                      │   │   │  border: 1px solid
│  │  │                      │   │   │    rgba(255,255,255,0.10)
│  │  │                      │   │   │  border-focus:
│  │  │                      │   │   │    rgba(124,58,237,0.4)
│  │  └──────────────────────┘   │   │
│  │  "0 / 300 words"  (right)   │   │  12px / 400, #8B92A8
│  │          16px gap            │   │
│  │  ┌──────────────────────┐   │   │
│  │  │  Name (optional)     │   │   │  h: 48px
│  │  └──────────────────────┘   │   │
│  │          12px gap            │   │
│  │  ┌──────────────────────┐   │   │
│  │  │  Email (required)    │   │   │  h: 48px
│  │  │  "For early access"  │   │   │  helper: 12px, #8B92A8
│  │  └──────────────────────┘   │   │
│  │          20px gap            │   │
│  │  ┌──────────────────────┐   │   │
│  │  │   SUBMIT BUTTON      │   │   │  h: 52px, min-touch 44pt
│  │  │   gradient primary   │   │   │  bg: gradientPrimary
│  │  └──────────────────────┘   │   │
│  │                              │   │
│  └──────────────────────────────┘   │
│              48px gap                │
│  ┌──────────────────────────────┐   │
│  │    SECTION 5 — FOOTER        │   │
│  │    © JCMA Group Ltd          │   │  12px / 400, #8B92A8
│  │    Social icons (if any)     │   │  icon size: 20px, gap: 16px
│  └──────────────────────────────┘   │
│          safe-area-inset-bottom     │
└─────────────────────────────────────┘
```

---

## FULL-PAGE LAYOUT — Desktop (>700px, max 640px content)

```
┌──────────────────────────────────────────────────────┐
│                  full viewport width                   │
│          background: #0D0F1A (bgMain)                 │
│                                                        │
│     ┌──────────────────────────────────────┐          │
│     │      max-width: 640px, centered       │          │
│     │                                        │          │
│     │    [SECTION 1 — HEADER]               │          │
│     │    wordmark: 160px wide               │          │
│     │    headline: 32px / 700               │          │
│     │                                        │          │
│     │    [SECTION 2 — PROLOGUE CARD]        │          │
│     │    padding: 36px 32px                 │          │
│     │                                        │          │
│     │    [SECTION 3 — FEEDBACK FORM]        │          │
│     │    textarea min-h: 160px              │          │
│     │    Name + Email side-by-side:         │          │
│     │    ┌─────────┐  12px  ┌──────────┐   │          │
│     │    │  Name    │  gap   │  Email   │   │          │
│     │    └─────────┘        └──────────┘   │          │
│     │                                        │          │
│     │    [SECTION 5 — FOOTER]               │          │
│     └──────────────────────────────────────┘          │
│                                                        │
└──────────────────────────────────────────────────────┘
```

---

## SECTION 4 — ADMIN PANEL (hidden — ?admin=true only)

Appears between Section 3 and Section 5 when URL contains `?admin=true`.

```
┌──────────────────────────────────────┐
│  ADMIN — Recent Feedback             │  h3: 18px / 600
│  Auto-refreshes every 60s            │  caption: 12px, #8B92A8
│                                      │
│  ┌──────────────────────────────┐   │
│  │  TABLE (horizontal scroll    │   │  bg: #1E2235
│  │  allowed on mobile ONLY for  │   │  border: 1px solid
│  │  this table — page itself    │   │    rgba(255,255,255,0.10)
│  │  must not scroll horiz.)     │   │  radius: 12px
│  │                              │   │
│  │  Country | Region | Type |   │   │  header: 12px / 600
│  │  Time    | Feedback (50ch)   │   │    text: #B8BDD6
│  │  ────────┼────────┼──────┼   │   │    bg: rgba(124,58,237,0.08)
│  │  GB      | London | New  |   │   │
│  │  10:42   | "I really lov…"  │   │  rows: 13px / 400
│  │  ...     | ...    | ...  |   │   │    text: #E8EAF6
│  │                              │   │  alternating row:
│  └──────────────────────────────┘   │    rgba(255,255,255,0.02)
│                                      │
│  "Showing 20 most recent"           │  caption: 12px, #8B92A8
└──────────────────────────────────────┘
```

Table columns:
| Column   | Width (min) | Content                          |
|----------|-------------|----------------------------------|
| Country  | 48px        | 2-letter ISO code or flag emoji  |
| Region   | 80px        | City/region string               |
| Type     | 64px        | "New" or "Returning" badge       |
| Time     | 56px        | HH:MM format, local to viewer    |
| Feedback | 1fr (rest)  | First 50 chars, ellipsis overflow |

"New" badge: `bg: rgba(16,185,129,0.15)`, `text: #10B981`, radius 20px, padding 2px 8px, 11px font.
"Returning" badge: `bg: rgba(167,139,250,0.15)`, `text: #A78BFA`, same dimensions.

---

## COLOUR PALETTE (existing FamiliLook tokens — NO new colours)

| Token               | Hex / Value                                              | Usage on this page                    |
|----------------------|----------------------------------------------------------|---------------------------------------|
| bgMain               | `#0D0F1A`                                                | Page background                       |
| bgElevated           | `#1E2235`                                                | Form inputs, admin table bg           |
| bgCard               | `#161828`                                                | Not used directly (prologue uses gradient) |
| accentPrimary        | `#7C3AED`                                                | Gradient start, focus rings, chip bg  |
| accentSecondary      | `#4F46E5`                                                | Gradient end                          |
| accentPrimaryLight   | `#A78BFA`                                                | Chip text, "~2 weeks" badge text      |
| gradientPrimary      | `linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%)`     | Submit button, wordmark underline     |
| textPrimary          | `#E8EAF6`                                                | Headlines, form labels, body text     |
| textSecondary        | `#B8BDD6`                                                | Prologue body, form subtitle          |
| textMuted            | `#8B92A8`                                                | Word counter, helper text, footer     |
| borderMedium         | `rgba(255,255,255,0.10)`                                 | Input borders, card borders           |
| borderFocus          | `rgba(124,58,237,0.4)`                                   | Input focus state                     |
| overlayLight         | `rgba(255,255,255,0.04)`                                 | Subtle hover states                   |
| shadowMd             | `0 4px 12px rgba(0,0,0,0.4)`                            | Prologue card shadow                  |
| shadowGlow           | `0 0 20px rgba(124,58,237,0.3)`                          | Submit button hover glow              |

Prologue card gradient (composed from existing tokens):
  `linear-gradient(160deg, rgba(124,58,237,0.18) 0%, rgba(79,70,229,0.10) 100%)`
  — This is accentPrimary and accentSecondary at low opacity. No new colours.

---

## TYPOGRAPHY

| Element               | Font                              | Weight | Size   | Line-height | Colour     | Case      |
|------------------------|-----------------------------------|--------|--------|-------------|------------|-----------|
| Wordmark               | Inter, system stack fallback*     | 800    | 28px   | 1.1         | #E8EAF6    | Normal    |
| Headline (mobile)      | Inter, system stack fallback      | 700    | 26px   | 1.25        | #E8EAF6    | Normal    |
| Headline (desktop)     | Inter, system stack fallback      | 700    | 32px   | 1.25        | #E8EAF6    | Normal    |
| "~2 weeks" badge       | Inter, system stack fallback      | 500    | 14px   | 1.3         | #A78BFA    | Normal    |
| Prologue body          | Inter, system stack fallback      | 400    | 16px   | 1.65        | #B8BDD6    | Normal    |
| Section heading (h2)   | Inter, system stack fallback      | 600    | 22px   | 1.3         | #E8EAF6    | Normal    |
| Form subtitle          | Inter, system stack fallback      | 400    | 14px   | 1.5         | #B8BDD6    | Normal    |
| Input label            | Inter, system stack fallback      | 500    | 13px   | 1.3         | #E8EAF6    | Normal    |
| Input text             | Inter, system stack fallback      | 400    | 16px   | 1.5         | #E8EAF6    | Normal    |
| Input placeholder      | Inter, system stack fallback      | 400    | 16px   | 1.5         | #8B92A8    | Normal    |
| Word counter           | Inter, system stack fallback      | 400    | 12px   | 1.4         | #8B92A8    | Normal    |
| Helper text            | Inter, system stack fallback      | 400    | 12px   | 1.4         | #8B92A8    | Normal    |
| Submit button          | Inter, system stack fallback      | 600    | 16px   | 1.0         | #FFFFFF    | Normal    |
| Footer                 | Inter, system stack fallback      | 400    | 12px   | 1.4         | #8B92A8    | Normal    |
| Admin table header     | Inter, system stack fallback      | 600    | 12px   | 1.3         | #B8BDD6    | Uppercase |
| Admin table cell       | Inter, system stack fallback      | 400    | 13px   | 1.4         | #E8EAF6    | Normal    |

*System stack fallback: `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`

Font loading: `<link>` to Google Fonts Inter (weights 400, 500, 600, 700, 800) in the HTML `<head>`. If Inter fails to load, the system stack provides identical vertical metrics.

---

## SPACING (all values in px, 8pt grid)

| Element                              | Value     |
|--------------------------------------|-----------|
| Page horizontal padding (mobile)     | 20px      |
| Page horizontal padding (desktop)    | 0px (content max-width handles it) |
| Content max-width                    | 640px     |
| Content centering                    | `margin: 0 auto` |
| Safe area top                        | `env(safe-area-inset-top, 0px)` |
| Safe area bottom                     | `env(safe-area-inset-bottom, 0px)` |
| Header top padding                   | 48px      |
| Wordmark to headline gap             | 16px      |
| Headline to badge gap                | 12px      |
| Header to prologue gap               | 32px      |
| Prologue card padding (mobile)       | 28px top/bottom, 24px left/right |
| Prologue card padding (desktop)      | 36px top/bottom, 32px left/right |
| Prologue paragraph gap               | 14px (margin-bottom between `<p>`) |
| Prologue card border-radius          | 16px      |
| Prologue to form gap                 | 32px      |
| Form section heading to subtitle     | 6px       |
| Form subtitle to first field         | 16px      |
| Textarea min-height (mobile)         | 140px     |
| Textarea min-height (desktop)        | 160px     |
| Textarea to word counter gap         | 6px       |
| Word counter to name field gap       | 16px      |
| Name to email field gap              | 12px      |
| Email to submit button gap           | 20px      |
| Input height                         | 48px      |
| Input padding                        | 0 16px    |
| Input border-radius                  | 12px      |
| Input border                         | 1px solid rgba(255,255,255,0.10) |
| Input focus border                   | 1px solid rgba(124,58,237,0.4) |
| Input focus shadow                   | 0 0 0 3px rgba(124,58,237,0.15) |
| Submit button height                 | 52px      |
| Submit button border-radius          | 12px      |
| Form to footer gap                   | 48px      |
| Footer bottom padding                | 32px + safe-area-inset-bottom |
| Badge ("~2 weeks") padding           | 6px 16px  |
| Badge border-radius                  | 9999px (pill) |

---

## COMPONENT SPECIFICATIONS

### 1. Wordmark

The FamiliLook wordmark is text-based (not an image logo in the current site).

```
  FamiliLook
```

- Font: Inter 800 (ExtraBold), 28px
- Colour: #E8EAF6
- Letter-spacing: -0.02em (tight, premium feel)
- Optional: 3px gradient underline below wordmark (gradientPrimary), width 60px, centered, border-radius 2px
- Centered horizontally

### 2. "Back in ~2 weeks" Badge

```
  ╭────────────────────╮
  │  Back in ~2 weeks  │
  ╰────────────────────╯
```

- Background: `rgba(124,58,237,0.15)` (accentPrimary at 15% — matches existing TagBadge pattern)
- Text colour: `#A78BFA` (accentPrimaryLight)
- Font: Inter 500, 14px
- Padding: 6px 16px
- Border-radius: 9999px (pill)
- Border: `1px solid rgba(124,58,237,0.20)`
- Centered horizontally
- No animation — static, calm

### 3. Prologue Card

- Background: `linear-gradient(160deg, rgba(124,58,237,0.18) 0%, rgba(79,70,229,0.10) 100%)`
- Border: `1px solid rgba(124,58,237,0.25)`
- Border-radius: 16px
- Box-shadow: `0 4px 12px rgba(0,0,0,0.4)` (shadowMd)
- Inner padding: 28px 24px (mobile), 36px 32px (desktop)
- Text: Inter 400, 16px, line-height 1.65, colour #B8BDD6
- Paragraph spacing: 14px margin-bottom (not margin-top, so last paragraph has no trailing space)
- Width: 100% of content column

At 375px with 20px page padding: card content width = 375 - 40 (page padding) - 48 (card padding L+R) = 287px.
At 16px font / 1.65 line-height, 84 words across 4 paragraphs fits comfortably in ~220px height.
Total card height (estimated): ~276px. Generous — text will not feel cramped.

Optional motif: Abstract SVG of two overlapping circles (connection/family metaphor).
Position: bottom-right of card, 80x80px bounding box, `opacity: 0.08`, colour: #7C3AED.
This is decorative only — do not use if it crowds the text at mobile width.
Implementation: inline SVG or background-image, `pointer-events: none`.

### 4. Feedback Form

**Pre-submit state:**

Section heading: "Share your thoughts"
Subtitle: "What would make FamiliLook even better for your family?"
(Copywriter may adjust this — spec the visual container, not the copy.)

**Textarea:**
- Width: 100%
- Min-height: 140px (mobile), 160px (desktop)
- Max-height: 300px (allow growth, then scroll)
- Resize: vertical only
- Background: #1E2235
- Border: 1px solid rgba(255,255,255,0.10)
- Border-radius: 12px
- Padding: 16px
- Font: Inter 400, 16px, line-height 1.5, colour #E8EAF6
- Placeholder: "What features, products, or improvements would you love to see?" — colour #8B92A8
- Focus: border changes to rgba(124,58,237,0.4), outer glow 0 0 0 3px rgba(124,58,237,0.15)
- `maxlength` attribute NOT set (enforced via JS word count, not char count)

**Word counter:**
- Text: "{n} / 300 words"
- Font: Inter 400, 12px, colour #8B92A8
- Alignment: right
- Colour shift: when n > 280, colour becomes #F5A623 (accentWarning). When n > 300, colour becomes #EF4444 (accentError) and submit is disabled.
- Margin-top: 6px from textarea

**Name field:**
- Label: "Name" with "(optional)" in #8B92A8
- Input: height 48px, same styling as textarea borders/bg
- Placeholder: "Your name"

**Email field:**
- Label: "Email"
- Input: height 48px, same styling
- Placeholder: "you@example.com"
- Helper text below: "We'll notify you when FamiliLook is back" — 12px, #8B92A8, margin-top 4px
- Validation: basic email pattern, red border (#EF4444) on invalid blur
- Required: `required` attribute + asterisk in label colour #EF4444

**Desktop layout (>700px):** Name and Email fields sit side-by-side in a 2-column grid with 12px gap.
**Mobile (<700px):** Name and Email stack vertically with 12px gap.

**Submit button:**
- Width: 100%
- Height: 52px (exceeds 44pt touch target)
- Background: `linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%)` (gradientPrimary)
- Text: "Submit feedback" — Inter 600, 16px, #FFFFFF
- Border: none
- Border-radius: 12px
- Box-shadow: `0 4px 12px rgba(0,0,0,0.4)` (shadowMd)
- Cursor: pointer
- Hover (desktop): box-shadow adds glow `0 0 20px rgba(124,58,237,0.3)`
- Active/pressed: `transform: scale(0.98)`, shadow reduces to shadowSm
- Disabled state (word count >300 or email invalid): opacity 0.5, cursor not-allowed
- Loading state: text replaced with spinner (20px, white, 1s rotation), button stays full width

**Post-submit state:**
- The entire form (heading, subtitle, all fields, button) is replaced by a confirmation card.
- Confirmation card uses same container dimensions, padding 28px 24px.
- Content:
  - Checkmark icon: 48px circle, bg gradientPrimary, white checkmark SVG inside (24px)
  - Heading: "Thank you" — Inter 600, 22px, #E8EAF6
  - Body: "We've saved your feedback and we'll let you know when we're back." — Inter 400, 16px, #B8BDD6
- Transition: fade-in 300ms ease (opacity 0 → 1, translateY 8px → 0)

### 5. Footer

- Top border: `1px solid rgba(255,255,255,0.06)` (borderSoft)
- Padding: 24px 0 32px 0 (+ safe-area-inset-bottom)
- Text: "© 2026 JCMA Group Ltd" — Inter 400, 12px, #8B92A8
- Centered
- Social links (if applicable): row of icon links, 20px icon size, 16px gap between, colour #8B92A8, hover colour #E8EAF6
- Touch target for social icons: 44px × 44px (icon centered within invisible hit area)

---

## INTERACTION STATES

| Element            | Default                | Hover (desktop)            | Focus                         | Active/Pressed          |
|--------------------|------------------------|----------------------------|-------------------------------|-------------------------|
| Submit button      | gradientPrimary        | + glow shadow              | + glow shadow + 2px outline   | scale(0.98), shadow sm  |
| Text input         | border: borderMedium   | border: rgba(255,255,255,0.15) | border: borderFocus + ring | —                       |
| Textarea           | border: borderMedium   | border: rgba(255,255,255,0.15) | border: borderFocus + ring | —                       |
| Social icon        | #8B92A8                | #E8EAF6                    | outline: 2px #A78BFA          | opacity 0.8             |
| Admin table row    | transparent            | rgba(255,255,255,0.04)     | —                             | —                       |

Focus ring spec (all interactive elements):
  `outline: 2px solid #A78BFA; outline-offset: 2px;`
  This ensures keyboard navigation visibility on the dark background.

---

## MOBILE KEYBOARD BEHAVIOUR

When the mobile keyboard opens (textarea or inputs focused):
- The page must scroll so the focused field is visible above the keyboard
- Do NOT use `position: fixed` on the form — it will be obscured
- The submit button must remain reachable by scrolling (not pinned to bottom)
- Use `padding-bottom: 300px` on the page container to ensure scroll room when keyboard is open
- `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">` to prevent zoom on input focus (iOS)

---

## ANIMATIONS (minimal — this is a calm page)

| Animation          | Trigger        | Spec                                          |
|--------------------|----------------|------------------------------------------------|
| Page fade-in       | Page load      | opacity 0 → 1, 400ms ease, 100ms delay        |
| Prologue card      | Page load      | opacity 0 → 1, translateY 12px → 0, 500ms ease, 200ms delay |
| Form section       | Page load      | opacity 0 → 1, translateY 12px → 0, 500ms ease, 350ms delay |
| Confirmation       | Form submit    | opacity 0 → 1, translateY 8px → 0, 300ms ease |
| Submit spinner     | Submitting     | rotate 360deg, 1s linear infinite              |

No breathing animations, no particles, no shimmer. This page is quiet and purposeful.

---

## ADMIN PANEL DETAILS

- Visibility: `display: none` by default. Shown only when `URLSearchParams` contains `admin=true`.
- No authentication layer in this spec (short-lived page). If needed, add a simple password prompt — out of scope for visual spec.
- Table container: `overflow-x: auto` (allows horizontal scroll within the table wrapper only).
- Auto-refresh: `setInterval` fetch every 60000ms. Show "Updated 10:42" timestamp below table, 12px, #8B92A8.
- Empty state: "No feedback yet" centered in table area, Inter 400, 14px, #8B92A8.
- Max rows shown: 20 (most recent first, sorted by time descending).

---

## RESPONSIVE BREAKPOINTS

| Breakpoint  | Changes                                                    |
|-------------|------------------------------------------------------------|
| < 375px     | Page padding reduces to 16px. Headline stays 26px.        |
| 375–700px   | Primary mobile layout as specced above.                    |
| > 700px     | Headline scales to 32px. Name/Email go side-by-side.       |
|             | Prologue card padding increases to 36px 32px.              |
|             | Content max-width: 640px, centered.                        |
| > 1024px    | No further changes. 640px content column stays centered.   |

---

## IMPLEMENTATION NOTES FOR FE LEAD

1. This is a standalone HTML page or minimal React app — does NOT live inside the existing desktop2 SPA router. It replaces the entire site temporarily.
2. Use inline styles (consistent with HomePageOccasion.jsx pattern) — no Tailwind dependency needed for a standalone page.
3. Import Inter from Google Fonts via `<link>` in the HTML head.
4. All colour values come from `src/theme/colors.js` tokens. Reference hex values directly since this page is standalone.
5. Form submission target: backend API endpoint TBD (FE Lead to confirm with backend). For the visual spec, assume a POST to `/api/maintenance-feedback` returning `{ ok: true }`.
6. Word counter logic: split on whitespace, filter empty strings, count. Do NOT use character count.
7. Admin panel geolocation (country/region): derive from IP server-side, not client-side. The admin table just displays what the API returns.
8. "New" vs "Returning" user type: based on whether the submitter's email has been seen before (backend logic).
9. The `?admin=true` param should be checked via `new URLSearchParams(window.location.search).get('admin') === 'true'`.
10. No cookies, no localStorage, no analytics on this page. It is a maintenance page — minimal footprint.
11. Ensure `<html lang="en">` and proper `<meta>` tags for SEO (page title: "FamiliLook — We'll Be Right Back", description: "FamiliLook is being upgraded. Share your feedback and we'll notify you when we're back.").
12. Test at 375px with iOS Safari keyboard open — the textarea and submit button must remain reachable.

---

## ASSETS REQUIRED

1. **Inter font** — Google Fonts link, weights 400/500/600/700/800
2. **Checkmark SVG** — 24px white checkmark for confirmation circle (simple polyline, stroke-width 2.5)
3. **Optional: Connection motif SVG** — two overlapping circles, single colour (#7C3AED), 80x80px viewBox. Only if it does not crowd prologue text at 375px. FE Lead may omit.
4. **Social icons** (if applicable) — standard SVG icons for Twitter/X, Instagram, etc. 20px, monochrome.

No photographs. No illustrations of people. No stock imagery.

---

## CHECKLIST (Visual Director sign-off)

- [x] All dimensions in pixels
- [x] All colours in hex (existing palette only — zero new colours)
- [x] All fonts named with weight, size, line-height
- [x] Layout shown in ASCII diagrams (mobile + desktop)
- [x] Mobile touch targets >= 44pt (submit: 52px, inputs: 48px, social: 44px hit area)
- [x] No horizontal scroll (except admin table wrapper)
- [x] No real photos of people
- [x] Keyboard behaviour addressed
- [x] Admin panel specced with table layout
- [x] Animations minimal and purposeful
- [x] Post-submit state specced
- [x] Responsive breakpoints defined
- [x] Implementation notes for FE Lead complete

===============================================
  END OF VISUAL DIRECTION
  Ready for FE Lead implementation
===============================================
