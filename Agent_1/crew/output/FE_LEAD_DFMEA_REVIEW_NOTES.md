# FE Lead — DFMEA V2 Review Notes
## Date: 30 March 2026 | Status: Ready for QA Lead cross-reference

---

## 1. Missing PNGs (2 confirmed)

| File | Variant | When requested | Fallback |
|------|---------|---------------|----------|
| `cub_curious.png` | default | `remapEmotion("cub", "cheeky")` → curious | Silent fallback to `cub_happy.png` |
| `gran_loving_african.png` | african | valentines / loser_parent occasions | Silent fallback to `gran_proud_african.png` |

Both are NOT imported in index.js (confirmed — no build error), but the composition engine CAN request them. The fallback works silently — wrong emotion displayed, no crash.

---

## 2. Critical Architecture Gap: Recipient is Dead Code

`recipient` is hardcoded to `"unknown"` in ALL 4 call sites in KeepsakesModal (lines ~802, ~829, ~872, and the character mug preview branches). This means:

- **Gift layout** for grandparents → never triggered
- **Celebration layout** for winner_parent → never triggered
- **Blend layout** for loser_parent → never triggered
- **110+ recipient-specific headlines** (winner_parent, loser_parent, grandparent pools) → unreachable
- **Losing parent inclusive messaging** ("THEY MAY LOOK LIKE MUM, BUT...") → dead code

The entire recipient-driven personalisation system is implemented but **unreachable in production**. No UI exists for the user to select who the mug is for.

---

## 3. Prop Interface Map (Current State Post-P0 Fixes)

### KeepsakesModal → CharacterMugTemplate (visible preview)

```
Step 3 style preview:
  occasion: CHARACTER_MUG_STYLE_MAP[selectedStyle]?.occasion || "generic"
  variant: CHARACTER_MUG_STYLE_MAP[selectedStyle]?.variant || "default"
  recipient: "unknown"  ← HARDCODED
  ageTheme: ageTheme
  data: templateData

Step 4 mockup view:
  Same as above

Step 4 flat view:
  Same as above
```

### KeepsakesModal → CharacterMugTemplate (hidden cardRef for export)

```
  occasion: CHARACTER_MUG_STYLE_MAP[selectedStyle]?.occasion || "generic"
  variant: CHARACTER_MUG_STYLE_MAP[selectedStyle]?.variant || "default"
  recipient: "unknown"  ← HARDCODED
  ageTheme: ageTheme
  data: templateData
```

### CharacterMugTemplate → compositionEngine

```
composeCharacterMug({
  data: { winner, winnerPct, winnerLabel, loserLabel, childName, childPhoto, featureVotes, dominantFeature },
  occasion: "generic" | "heritage_gold" | "carnival_spirit" | "ubuntu",
  recipient: "unknown",  ← ALWAYS THIS
  variant: "default" | "african",
})
```

### compositionEngine → characterHeadlines

```
selectHeadlines({
  winner, winnerPct, winnerLabel, loserLabel, childName, dominantFeature, featureVotes, occasion
})
// NOTE: recipient is NOT passed to selectHeadlines — it's handled internally by compositionEngine
// via getRecipientHeadlinePool()
```

---

## 4. Dead Assets Bundled

These PNGs are imported and shipped to users but the composition engine NEVER produces the emotion that would select them:

| PNG | Why dead |
|-----|----------|
| `mini_cheeky.png` | `remapEmotion("mini", "cheeky")` passes through — CAN be selected. NOT dead. |
| `cub_sleeping.png` / `cub_sleeping_african.png` | No code path in `getEmotionForData()` or `remapEmotion()` ever produces "sleeping". Only reachable if manually passed as prop. |
| `gran_laughing.png` / `gran_laughing_african.png` | No code path produces "laughing". Only "showing_off", "proud", "loving", "surprised" are reachable for gran. |
| `gramps_laughing.png` / `gramps_laughing_african.png` | Same — "laughing" unreachable for gramps. |

These 8 PNGs (~12MB total) are bundled but never displayed. Not a bug — they're future-ready for when emotion selection is expanded — but they increase bundle size.

---

## 5. Top Items for DFMEA V2 to Flag

| Priority | Finding | Impact |
|----------|---------|--------|
| **HIGH** | No recipient selector UI — entire personalisation system is dead code | The biggest selling point (bespoke mugs for different family members) has no way to activate |
| **HIGH** | Zero unit tests for compositionEngine.js and the recipient headline pools | Any refactor could break layout selection, emotion remapping, or headline resolution without detection |
| **HIGH** | Transparent PNG export not validated E2E with Prodigi | Could discover colour/compositing issues only after first customer order |
| **MEDIUM** | Silent PNG fallback for 2 missing emotions | Wrong emotion displayed (curious→happy, loving→proud) — subtle but incorrect |
| **MEDIUM** | Leading colon in headlines when childName is empty and headline starts with `{child}:` | ":\nMUM'S MINI ME" renders with orphan colon |
| **LOW** | 8 dead PNGs (~12MB) shipped in bundle | Performance impact, no functional issue |
| **LOW** | `cub_sleeping` and `gran/gramps_laughing` emotions unreachable by engine | Assets exist but no code path activates them |

---

## 6. Fragile Code Paths

1. **`CHARACTER_MUG_STYLE_MAP` sync risk** — if a new style is added to `templateRegistry.js` but not to `CHARACTER_MUG_STYLE_MAP` in KeepsakesModal, it silently falls back to "generic"/"default". No validation.

2. **`resolvedComponent` for character_mug** — the lazy import resolves to CharacterMugTemplate for ALL 4 styles (they share the same component). The differentiation happens entirely through props. If the prop mapping breaks, all styles render identically with no visible error.

3. **`getOccasionTheme()` fallback** — returns `OCCASION_THEMES.generic` for any unrecognised string. Silently masks occasion mapping errors.

4. **html-to-image with Vite static imports** — `cacheBust: true` in cardExport.js may cause double-fetch of character PNGs. Untested interaction.
