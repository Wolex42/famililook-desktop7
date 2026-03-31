# Character Mug Design Options — Visual Director Assessment
## Date: 30 March 2026 | Status: OPTIONS B & C ARCHIVED — Option A approved for implementation

---

## Context

The Character Mug template (CharacterMugTemplate.jsx) currently uses a 3-panel layout (26/48/26%) cramming ~18 UI elements onto the mug surface. With the new high-quality character illustrations (Caucasian + African families, 56 PNGs), the layout needs simplifying to let the characters and headlines breathe.

Reference: Cornish Prints UK uses 3-4 elements max per mug — bold headline, character, accent. That simplicity is what drives TikTok virality and gift appeal.

---

## OPTION A: "Hero Layout" — APPROVED ✅

### Concept
Drop the right panel. Use a 40/60 split. Maximum 5 elements. Character and headline dominate.

### Layout (830x345px CSS → 2670x1110px print)
```
┌──────────────────────┬─────────────────────────────────────┐
│                      │                                     │
│    CHARACTER          │   HERO HEADLINE (massive, bold)     │
│    (full height,      │                                     │
│     40% width,        │   "MUMMY'S MINI ME"                │
│     overlapping       │                                     │
│     slightly into     │   72% Mum · Got Mum's Eyes         │
│     centre panel)     │                                     │
│                      │   [photo circle — optional]         │
│    Speech bubble      │                                     │
│    "TOLD YOU SO!"     │   famililook.com                    │
│                      │                                     │
└──────────────────────┴─────────────────────────────────────┘
```

### Design Rules
1. **Character panel**: 40% width (~332px CSS). Character renders at full height, may overlap into centre panel by 20-30px for visual integration
2. **Hero headline**: 3x current size (~36-44px CSS → 116-142px print). ALL CAPS, bold rounded sans. Dominant visual element. Max 2 lines.
3. **Score + feature line**: Single combined line beneath headline: "72% Mum · Got Mum's Eyes". ~12px CSS.
4. **Photo circle**: Optional. Only rendered if `data.childPhoto` exists. 60px circle.
5. **Brand**: "famililook.com" bottom-right, small, muted.
6. **Speech bubble**: Positioned relative to character, overlapping panels if needed.
7. **REMOVED**: Feature chips, feature list, right panel, occasion header (folded into headline), percentage watermark, analysis metadata, divider line.

### Element Count: 5 (character, headline, score line, speech bubble, brand)
### Cornish Prints equivalent: 3-4

### Emotion Intelligence Upgrade
```js
function getEmotionForData(data, occasion) {
  // Occasion overrides
  if (occasion === "mothers_day" || occasion === "fathers_day") return "proud";
  if (occasion === "christmas") return "celebrating";
  if (occasion === "grandparents_day") return "showing_off";
  if (occasion === "valentines") return "loving";

  // Percentage-based (default)
  const pct = data.winnerPct || 51;
  if (pct >= 75) return "celebrating";
  if (pct >= 65) return "proud";
  if (pct >= 55) return "cheeky";
  return "surprised";
}

function getCharacterForData(data, occasion) {
  // Occasion overrides
  if (occasion === "grandparents_day") return "gran"; // or "gramps"
  if (occasion === "birthday") {
    // Use age-appropriate character
    return data.childAge <= 2 ? "cub" : "mini";
  }

  // Winner-based (default)
  const parentType = normaliseParent(data.winnerLabel);
  if (parentType === "mum") return "mama";
  if (parentType === "dad") return "papa";
  return "mama";
}
```

### Character-appropriate emotion remapping
| Character | Avoid | Remap to |
|-----------|-------|----------|
| Gran/Gramps | cheeky | showing_off |
| Cub | celebrating | giggling |
| Cub | cheeky | curious |
| Mini | loving | pointing |

---

## OPTION B: "Cornish Style" — ARCHIVED 📦

### Concept
Single unified composition — no panels. Character and text compose as one scene. Maximum social shareability.

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│         [Character on left, leaning into text]               │
│                                                              │
│              SORRY DAD,                                      │
│              I'M ALL MUM                                     │
│                                                              │
│              ── 72% Mum ──                                   │
│              Got Mum's Eyes                                  │
│                                                              │
│         [Speech bubble: "TOLD YOU SO!"]                      │
│                                                              │
│                                    famililook.com            │
└──────────────────────────────────────────────────────────────┘
```

### Design Rules
1. No panel divisions — single canvas, free-form composition
2. Character positioned left-of-centre, angled toward the text
3. Headline positioned right-of-centre, vertically centred
4. Character may overlap/interact with headline text (e.g., pointing at it)
5. Score displayed as a decorative divider line: "── 72% Mum ──"
6. Feature callout as single subtext line
7. Photo NOT on the mug — used on product page/social post instead
8. Brand mark bottom-right corner

### Element Count: 4 (character, headline, score, brand)
### Cornish Prints equivalent: 3

### Implementation Notes
- Requires absolute positioning for character (not flexbox panels)
- Character size/position varies by character type (standing vs seated)
- Gran/Gramps in armchairs need different composition than standing Mama/Papa
- Text wrapping around character shape is complex
- Highest visual impact but most complex to implement
- Best for social media screenshots / TikTok content

### When to implement
- If Option A proves successful and we want an even bolder variant
- As a "social share" export format (separate from the print mug)
- For seasonal limited editions where we want maximum viral impact

---

## OPTION C: "Simplified 3-Panel" — ARCHIVED 📦

### Concept
Keep the existing 3-panel structure but drastically simplify centre and right panels. Least disruptive change.

### Changes from Current
| Element | Current | Option C |
|---------|---------|----------|
| Feature chips (centre) | 8 chips | **REMOVED** (redundant with right panel) |
| Occasion header | Separate element | **Folded into headline** |
| Hero headline | 18-22px | **30px** (50% bigger) |
| Feature list (right) | All 8 features | **Top 3 winning features only** |
| Percentage watermark (right) | 60px, 6% opacity | **REMOVED** |
| Analysis metadata (right) | 3 lines | **1 line** (name + date) |
| Character panel | 26% width | **30% width** |
| Decorative elements | None | **Add confetti/stars behind character** |

### Layout
```
┌─────────────────┬────────────────────────────┬─────────────────┐
│                 │                            │                 │
│  CHARACTER       │  HERO HEADLINE (bigger)    │  TOP 3 FEATURES │
│  (30% width,    │                            │  Eyes → Mum     │
│   full height)  │  72% Mum                   │  Smile → Mum    │
│                 │  Got Mum's Eyes            │  Nose → Mum     │
│  Speech bubble  │                            │                 │
│                 │  [photo circle]            │  famililook.com │
│  confetti bg    │  famililook.com            │                 │
│                 │                            │                 │
└─────────────────┴────────────────────────────┴─────────────────┘
```

### Element Count: ~10 (reduced from ~18)
### Implementation Effort: Lowest — modify existing template, no structural change

### When to implement
- If Option A feels too minimal for users who want data visibility
- As an alternative style in the style picker (e.g., "Character Detailed" vs "Character Bold")
- For the "data-loving parent" persona who wants features visible on the mug

---

## EMOTION INTELLIGENCE — Applies to All Options

### Current Logic (too simple)
```js
75%+ → celebrating | 65-74% → proud | 55-64% → cheeky | 51-54% → surprised
```

### Proposed Logic (context-aware)

#### Layer 1: Occasion Override
| Occasion | Forced Emotion | Why |
|----------|---------------|-----|
| mothers_day | proud | Warm, dignified |
| fathers_day | proud | Same |
| christmas | celebrating | Festive energy |
| grandparents_day | showing_off | "Look at my grandchild" |
| valentines | loving | Romance |
| birthday | celebrating | Party energy |
| easter | cheeky | Playful spring |

#### Layer 2: Character Appropriateness
| Character | Emotion requested | Remapped to | Reason |
|-----------|-------------------|-------------|--------|
| gran | cheeky | showing_off | Grandmothers don't do "cheeky" — they show off |
| gramps | cheeky | showing_off | Same |
| cub | celebrating | giggling | Babies don't celebrate — they giggle |
| cub | cheeky | curious | Babies aren't cheeky — they're curious |
| cub | proud | happy | Babies don't look "proud" — they look happy |
| mini | loving | pointing | Kids don't do "loving" — they point excitedly |

#### Layer 3: Feature-Driven Flavour (optional, future)
| Dominant Feature | Suggested Emotion Bonus | Why |
|-----------------|------------------------|-----|
| smile | cheeky | "That smile is cheeky" |
| eyes | surprised | Wide-eyed connection |
| hair | proud | Showing it off |
| ears | cheeky | Playful feature |

---

## FONT RECOMMENDATIONS — Applies to All Options

### Current
- Headlines: `'Arial Rounded MT Bold', 'Nunito', Arial, sans-serif`
- Body: `Georgia, 'Times New Roman', serif`

### Recommended (for Character Mugs specifically)
- **Headlines**: `'Nunito Black', 'Baloo 2', 'Arial Rounded MT Bold', sans-serif` — rounder, warmer, more playful. Nunito is a Google Font (free, web-safe).
- **Score/sub-headline**: Same family, regular weight
- **Body/data**: Keep Georgia serif for continuity with standard mugs
- **Brand mark**: System sans, extra-light

### Font Loading
Nunito is already commonly available. If we add it as a Google Font import, it loads from cache for most users. Alternatively, stick with Arial Rounded MT Bold which is already specified — it's close enough and requires no loading.

---

## COLOUR COORDINATION — Applies to All Options

### Problem
The character illustrations have their own internal colour palette (rose/plum for Caucasian, teal/gold for African). The mug theme palette (from mugThemes.js) may clash.

### Solution: Theme-Character Harmony Matrix
| Mug Theme | Default Variant | African Variant | Notes |
|-----------|----------------|-----------------|-------|
| generic (rose) | ✅ Perfect match | ⚠️ Teal on rose — check contrast | May need theme-tinted overlay |
| heritage_gold | ⚠️ Rose on gold — warm | ✅ Perfect match | Gold theme + teal/gold characters |
| carnival_spirit | ⚠️ Rose on orange — warm | ✅ Good match | Orange theme + teal characters |
| ubuntu | ⚠️ Rose on terracotta | ✅ Perfect match | Earth tones + warm brown |
| fathers_day (blue) | ✅ Good contrast | ✅ Teal on blue — harmonious | Both work well |
| christmas (red) | ✅ Rose on red — family | ⚠️ Teal on red — Christmas colours! | Actually works perfectly |

### Recommendation
- Default/generic/mothers_day/valentines → auto-select Caucasian variant
- Heritage/carnival/ubuntu → auto-select African variant (already implemented)
- Fathers_day/christmas/birthday → either works — let user choose or randomise
