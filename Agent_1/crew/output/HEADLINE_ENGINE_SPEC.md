# Headline Engine Specification — Character Mug Product Line

**Author**: Copywriter Agent
**Date**: 30 March 2026
**Status**: READY FOR FE LEAD IMPLEMENTATION
**Input**: CHARACTER_MUG_CREATIVE_BRIEF.md (CMO, CEO-approved)
**Consumer**: `CharacterMugTemplate.jsx` (to be built by FE Lead)

---

## 1. Data Inputs

The headline selection algorithm receives these fields from the keepsake data layer (`useKeepsakeData.js`):

| Field | Type | Source | Example |
|-------|------|--------|---------|
| `winner` | `"parent1"` \| `"parent2"` \| `"blend"` \| `"unknown"` | `data.winner` | `"parent1"` |
| `winnerPct` | `integer` 51-100 | `data.winnerPct` | `72` |
| `winnerLabel` | `string` | `data.winnerLabel` | `"Mum"`, `"Dad"`, `"Nana"`, custom name |
| `loserLabel` | `string` | `data.loserLabel` | `"Dad"` |
| `childName` | `string` \| `null` | `data.childName` | `"Olivia"` |
| `dominantFeature` | `string` (one of 8 feature keys) | `data.dominantFeature` | `"eyes"` |
| `featureVotes` | `Record<string, "parent1"\|"parent2">` | `data.featureVotes` | `{ eyes: "parent1", ... }` |
| `occasion` | `string` | User-selected or seasonal | `"mothers_day"` |

### Derived values (computed by the selection algorithm)

| Derived | Logic |
|---------|-------|
| `pctBracket` | `"high"` if winnerPct >= 70, `"medium"` if 60-69, `"close"` if 51-59 |
| `winnerIsMum` | `true` if winnerLabel normalises to Mum/Mom/Mummy/Mama/Mother (case-insensitive) |
| `winnerIsDad` | `true` if winnerLabel normalises to Dad/Daddy/Papa/Father (case-insensitive) |
| `isBlend` | `true` if winner === "blend" or winner === "unknown"` |
| `heroFeature` | Alias for `dominantFeature` — the first feature matching the winner |

### Parent label normalisation

```
MUM_ALIASES = ["mum", "mom", "mummy", "mommy", "mama", "mother", "ma"]
DAD_ALIASES = ["dad", "daddy", "papa", "father", "pa", "dada"]

function normaliseParent(label):
  lower = label.toLowerCase().trim()
  if lower in MUM_ALIASES → return "mum"
  if lower in DAD_ALIASES → return "dad"
  return "custom"
```

When `normaliseParent` returns `"custom"`, headlines use the `{winnerLabel}` template literal instead of hardcoded "MUM"/"DAD". See Section 6 for resolution logic.

---

## 2. Hero Headline Bank

All headlines are stored in ALL CAPS as they render on the mug.
`{child}` = `childName` (uppercased at render). `{winner}` = `winnerLabel` (uppercased at render).

**HARD LIMIT: 35 characters maximum per headline (including resolved template literals).**

### 2.1 Winner = Mum, High Percentage (70-100)

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H001 | MUMMY'S MINI ME | 15 | Universal favourite |
| H002 | SORRY DAD, I'M ALL MUM | 22 | Cheeky, high-confidence |
| H003 | MUM DID ALL THE WORK | 20 | Playful brag |
| H004 | COPY + PASTE: MUM EDITION | 25 | Tech-culture reference |
| H005 | MUM'S GREATEST HIT | 18 | Music metaphor |
| H006 | MADE BY MUM | 11 | Short, punchy |
| H007 | {child}: MUM'S MINI ME | 22* | Personalised (*+name) |
| H008 | MUM'S TWIN | 10 | Ultra-short |
| H009 | 100% MUM ENERGY | 15 | Confident, bold |
| H010 | MUMMY RUNS DEEP | 15 | Warm, poetic |
| H011 | ALL MUM, NO DOUBT | 16 | Decisive |
| H012 | MUM WINS. AGAIN. | 15 | Competitive edge |

### 2.2 Winner = Mum, Medium Percentage (60-69)

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H013 | LIKE MOTHER, LIKE BABY | 21 | Classic warmth |
| H014 | MOSTLY MUM | 10 | Understated |
| H015 | MUM'S SIDE IS STRONG | 19 | Confident without overselling |
| H016 | LEANING MUM | 11 | Playful shorthand |
| H017 | MUM TAKES THE LEAD | 18 | Competitive but fair |

### 2.3 Winner = Dad, High Percentage (70-100)

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H018 | DADDY'S DOUBLE | 14 | Alliterative, punchy |
| H019 | SORRY MUM, THIS ONE'S DAD | 25 | Cheeky mirror of H002 |
| H020 | DAD'S CTRL+C, CTRL+V | 20 | Tech-culture reference |
| H021 | STRONG GENES, DAD | 16 | Flattering |
| H022 | DAD'S GREATEST HIT | 18 | Music metaphor |
| H023 | MADE BY DAD | 11 | Short, punchy |
| H024 | {child}: DAD'S DOUBLE | 21* | Personalised (*+name) |
| H025 | DAD'S TWIN | 10 | Ultra-short |
| H026 | 100% DAD ENERGY | 15 | Confident, bold |
| H027 | DAD STAMP: APPROVED | 18 | Official/playful |
| H028 | ALL DAD, NO QUESTION | 19 | Decisive |
| H029 | DAD WINS. FINALLY. | 17 | Self-deprecating humour |

### 2.4 Winner = Dad, Medium Percentage (60-69)

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H030 | THE APPLE DOESN'T FALL FAR | 26 | Classic proverb |
| H031 | MOSTLY DAD | 10 | Understated |
| H032 | DAD'S SIDE IS STRONG | 19 | Confident without overselling |
| H033 | LEANING DAD | 11 | Playful shorthand |
| H034 | DAD TAKES THE LEAD | 18 | Competitive but fair |

### 2.5 Close Call (51-59)

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H035 | THE PERFECT BLEND | 17 | Warm, balanced |
| H036 | BEST OF BOTH | 12 | Classic, universally loved |
| H037 | NOT QUITE 50/50 | 14 | Playful nod to the rule |
| H038 | THE GREAT DEBATE | 16 | Conversation-starter |
| H039 | TEAMWORK MAKES THE BABY | 23 | Humorous twist |
| H040 | YOU BOTH DID GOOD | 17 | Affirming |
| H041 | THE VERDICT: JUST BARELY | 24 | Dramatic reveal |
| H042 | A BIT OF BOTH | 13 | Simple, warm |
| H043 | TOO CLOSE TO CALL | 17 | Suspenseful |
| H044 | PERFECTLY BLENDED | 17 | Positive spin on closeness |
| H045 | THEY GOT THE BEST BITS | 22 | Compliment to both |

### 2.6 Blend / Unknown

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H046 | BEST OF BOTH WORLDS | 19 | Universal |
| H047 | A UNIQUE MIX | 12 | Celebratory |
| H048 | ONE OF A KIND | 13 | Emphasis on uniqueness |
| H049 | PERFECTLY BLENDED | 17 | Warm |
| H050 | THE FAMILY RECIPE | 17 | Food metaphor |

### 2.7 Custom Parent Name Headlines

When the winner label does not match Mum/Dad aliases, use template-literal headlines:

| ID | Copy | Chars | Notes |
|----|------|-------|-------|
| H051 | {winner}'S MINI ME | 18* | Universal fallback (*+name) |
| H052 | ALL {winner} | 12* | Short, confident (*+name) |
| H053 | {child} LOOKS LIKE {winner} | 27* | Explicit, clear (*+names) |
| H054 | MADE BY {winner} | 16* | Short (*+name) |
| H055 | {winner}'S GREATEST HIT | 23* | Music metaphor (*+name) |
| H056 | {winner}'S DOUBLE | 17* | Alliterative (*+name) |
| H057 | {winner} WINS | 12* | Competitive (*+name) |
| H058 | {winner}'S TWIN | 14* | Ultra-short (*+name) |
| H059 | HELLO, MINI {winner} | 20* | Warm greeting (*+name) |
| H060 | {winner} CALLED IT | 18* | Smug confirmation (*+name) |

*Character counts marked with * are base counts before template literal resolution. The selection algorithm MUST verify the resolved headline is <= 35 characters. See Section 6 fallback logic.*

### 2.8 Full Count Verification

| Category | Count |
|----------|-------|
| Mum High (70-100) | 12 |
| Mum Medium (60-69) | 5 |
| Dad High (70-100) | 12 |
| Dad Medium (60-69) | 5 |
| Close Call (51-59) | 11 |
| Blend/Unknown | 5 |
| Custom Parent Name | 10 |
| **Total** | **60** |

---

## 3. Feature Sub-headline Bank

Sub-headlines appear below the hero headline, referencing the dominant inherited feature. Max **50 characters**. Template literals: `{winner}` = winnerLabel, `{loser}` = loserLabel.

### 3.1 Eyes

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F001 | GOT {winner}'S EYES | 19* | Either |
| F002 | THOSE EYES? ALL {winner} | 24* | Either |
| F003 | {winner}'S EYES, NO QUESTION | 28* | Either |

### 3.2 Eyebrows

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F004 | THOSE BROWS? ALL {winner} | 25* | Either |
| F005 | {winner}'S BROWS ON POINT | 25* | Either |
| F006 | EYEBROWS: COURTESY OF {winner} | 30* | Either |

### 3.3 Smile

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F007 | {winner}'S SMILE, THROUGH AND THROUGH | 37* | Either |
| F008 | THAT SMILE IS ALL {winner} | 26* | Either |
| F009 | GRINNING LIKE {winner} | 22* | Either |

### 3.4 Nose

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F010 | THAT NOSE? 100% {winner} | 24* | Either |
| F011 | NOSE BY {winner} | 15* | Either |
| F012 | {winner}'S NOSE, ON THE NOSE | 27* | Either |

### 3.5 Face Shape

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F013 | {winner}'S FACE SHAPE, NO DOUBT | 30* | Either |
| F014 | FACE SHAPE: A GIFT FROM {winner} | 31* | Either |
| F015 | SHAPED LIKE {winner} | 20* | Either |

### 3.6 Skin

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F016 | {winner}'S GLOW | 15* | Either |
| F017 | SKIN: {winner}'S CONTRIBUTION | 29* | Either |
| F018 | GLOWING LIKE {winner} | 21* | Either |

### 3.7 Hair

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F019 | HAIR BY {winner} | 15* | Either |
| F020 | {winner}'S LOCKS | 15* | Either |
| F021 | THAT HAIR IS ALL {winner} | 25* | Either |

### 3.8 Ears

| ID | Copy | Chars | Winner |
|----|------|-------|--------|
| F022 | EARS: A GIFT FROM {winner} | 26* | Either |
| F023 | {winner}'S EARS, UNMISTAKABLY | 29* | Either |
| F024 | THOSE EARS? ALL {winner} | 24* | Either |

### 3.9 Sub-headline Summary

8 features x 3 variants each = **24 sub-headlines**. All use `{winner}` template literal so they work for Mum, Dad, or custom parent names.

---

## 4. Occasion Header Bank

Occasion headers appear above the hero headline. Max **30 characters**. Template literal: `{child}` = childName (uppercased).

| ID | Copy | Chars | Occasion |
|----|------|-------|----------|
| O001 | *(no header)* | 0 | `generic` |
| O002 | HAPPY MOTHER'S DAY | 18 | `mothers_day` |
| O003 | HAPPY FATHER'S DAY | 18 | `fathers_day` |
| O004 | HAPPY BIRTHDAY {child} | 22* | `birthday` |
| O005 | HAPPY BIRTHDAY | 14 | `birthday` (no name fallback) |
| O006 | MERRY CHRISTMAS | 15 | `christmas` |
| O007 | TO MY VALENTINE | 15 | `valentines` |
| O008 | BEST GRANDPARENT EVER | 21 | `grandparents_day` |
| O009 | FAMILY HERITAGE | 15 | `heritage_gold` |
| O010 | CELEBRATE FAMILY | 16 | `carnival_spirit` |
| O011 | WE ARE FAMILY | 13 | `ubuntu` |

**Notes:**
- `generic` renders no occasion header (clean look).
- `birthday` uses O004 if `childName` is available and resolved length <= 30 chars; otherwise falls back to O005.
- Cultural themes (`heritage_gold`, `carnival_spirit`, `ubuntu`) use the same headers as `mugThemes.js` for consistency.

---

## 5. Character Speech Bubbles

Short quips inside character speech bubbles. Max **20 characters** (speech bubbles are small).

### 5.1 Winner Character — Proud Reactions

| ID | Copy | Chars | Trigger |
|----|------|-------|---------|
| S001 | TOLD YOU SO! | 12 | winnerPct >= 70 |
| S002 | IT'S OBVIOUS! | 13 | winnerPct >= 70 |
| S003 | THAT'S MY BABY! | 15 | winnerPct >= 65 |
| S004 | I KNEW IT! | 10 | winnerPct >= 60 |
| S005 | LOOK AT US! | 11 | winnerPct >= 60 |
| S006 | MY MINI ME! | 11 | winnerPct >= 70 |
| S007 | NO SURPRISE! | 12 | winnerPct >= 75 |

### 5.2 Losing Parent Character — Playful Reactions

| ID | Copy | Chars | Trigger |
|----|------|-------|---------|
| S008 | WAIT, REALLY? | 13 | winnerPct >= 70 |
| S009 | I SEE IT... | 11 | winnerPct >= 60 |
| S010 | NEXT TIME! | 10 | winnerPct >= 60 |
| S011 | HMM, BARELY... | 14 | winnerPct < 60 |
| S012 | I WANT A RECOUNT | 16 | winnerPct >= 65 |
| S013 | FAIR ENOUGH | 11 | winnerPct >= 60 |
| S014 | NOT CONVINCED! | 14 | winnerPct >= 70 |

### 5.3 Close Call Reactions (either character)

| ID | Copy | Chars | Trigger |
|----|------|-------|---------|
| S015 | SO CLOSE! | 9 | winnerPct <= 55 |
| S016 | IT'S A TIE... ISH | 17 | winnerPct <= 55 |
| S017 | COULD GO EITHER WAY | 19 | winnerPct <= 55 |
| S018 | SQUINT AND SEE ME | 17 | winnerPct <= 58 |
| S019 | WE BOTH WIN! | 12 | winnerPct <= 55 |

### 5.4 Summary

| Category | Count |
|----------|-------|
| Winner proud | 7 |
| Loser playful | 7 |
| Close call | 5 |
| **Total** | **19** |

---

## 6. Selection Algorithm

### 6.1 Pseudocode

```
function selectHeadlines(input):
  { winner, winnerPct, winnerLabel, loserLabel, childName, dominantFeature, featureVotes, occasion } = input

  // ── Step 1: Normalise parent identity ──
  parentType = normaliseParent(winnerLabel)   // "mum" | "dad" | "custom"
  isBlend = (winner === "blend" || winner === "unknown")

  // ── Step 2: Determine percentage bracket ──
  if isBlend:
    pctBracket = "blend"
  else if winnerPct >= 70:
    pctBracket = "high"
  else if winnerPct >= 60:
    pctBracket = "medium"
  else:
    pctBracket = "close"

  // ── Step 3: Build candidate pool for hero headline ──
  if isBlend:
    pool = HEADLINES.blend                         // H046-H050
  else if pctBracket === "close":
    pool = HEADLINES.close_call                    // H035-H045
  else if parentType === "mum":
    pool = HEADLINES.mum[pctBracket]               // H001-H012 or H013-H017
  else if parentType === "dad":
    pool = HEADLINES.dad[pctBracket]               // H018-H029 or H030-H034
  else:
    pool = HEADLINES.custom                        // H051-H060

  // ── Step 4: Deterministic random selection (seeded) ──
  seed = hashString(childName || "FamiliLook" + winnerPct)
  index = seed % pool.length
  heroHeadline = pool[index]

  // ── Step 5: Resolve template literals ──
  heroHeadline = resolveTemplates(heroHeadline, {
    child: (childName || "").toUpperCase(),
    winner: winnerLabel.toUpperCase(),
  })

  // ── Step 6: Verify character limit ──
  if heroHeadline.length > 35:
    // Try next headline in pool
    for i in range(1, pool.length):
      candidate = resolveTemplates(pool[(index + i) % pool.length], ...)
      if candidate.length <= 35:
        heroHeadline = candidate
        break
    // Ultimate fallback if all exceed 35 chars
    if heroHeadline.length > 35:
      heroHeadline = truncateAtWord(heroHeadline, 35)

  // ── Step 7: Select feature sub-headline ──
  featureKey = dominantFeature || "eyes"
  featurePool = SUBHEADLINES[featureKey]           // F001-F024 filtered by feature
  featureIndex = seed % featurePool.length
  featureSubline = resolveTemplates(featurePool[featureIndex], {
    winner: winnerLabel.toUpperCase(),
    loser: loserLabel.toUpperCase(),
  })

  // Verify 50-char limit
  if featureSubline.length > 50:
    featureSubline = truncateAtWord(featureSubline, 50)

  // ── Step 8: Select occasion header ──
  if occasion === "generic" || !occasion:
    occasionHeader = null
  else if occasion === "birthday" && childName:
    candidate = "HAPPY BIRTHDAY " + childName.toUpperCase()
    occasionHeader = candidate.length <= 30 ? candidate : "HAPPY BIRTHDAY"
  else:
    occasionHeader = OCCASION_HEADERS[occasion] || null

  // ── Step 9: Select speech bubbles ──
  if isBlend || pctBracket === "close":
    winnerBubble = pickSeeded(SPEECH.close_call, seed)
    loserBubble = pickSeeded(SPEECH.close_call, seed + 1)
  else:
    winnerBubble = pickSeeded(SPEECH.winner_proud, seed)
    loserBubble = pickSeeded(SPEECH.loser_playful, seed)

  // ── Step 10: Return ──
  return {
    heroHeadline,       // string, <= 35 chars, ALL CAPS
    featureSubline,     // string, <= 50 chars, ALL CAPS
    occasionHeader,     // string | null, <= 30 chars, ALL CAPS
    winnerBubble,       // string, <= 20 chars, ALL CAPS
    loserBubble,        // string, <= 20 chars, ALL CAPS
  }
```

### 6.2 Hash Function (Deterministic Seed)

The seed ensures the same child always gets the same headline (no flickering on re-renders, consistent across previews and print exports).

```javascript
function hashString(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash + str.charCodeAt(i)) & 0x7fffffff;
  }
  return hash;
}
```

This is a djb2 hash — fast, deterministic, decent distribution. No crypto required.

### 6.3 Template Literal Resolution

```javascript
function resolveTemplates(text, vars) {
  return text
    .replace(/\{child\}/g, vars.child || "")
    .replace(/\{winner\}/g, vars.winner || "")
    .replace(/\{loser\}/g, vars.loser || "");
}
```

### 6.4 Fallback Logic

| Condition | Fallback |
|-----------|----------|
| `childName` is null/empty | Omit `{child}` from headline; skip H007, H024, H053. Seed uses `"FamiliLook" + winnerPct`. |
| `winnerLabel` is null/empty | Use `"PARENT"` as winnerLabel. |
| Resolved headline > 35 chars | Iterate pool to find one that fits. If none fit, `truncateAtWord()` from `mugThemes.js`. |
| `dominantFeature` is missing | Default to `"eyes"`. |
| `occasion` not recognised | Treat as `"generic"` (no header). |
| `winner` is `"blend"` or `"unknown"` | Use blend pool (H046-H050). Speech bubbles use close-call set. |

### 6.5 Pick Helper

```javascript
function pickSeeded(pool, seed) {
  return pool[seed % pool.length];
}
```

---

## 7. Tone Validation Checklist

Every headline in this bank has been checked against these rules. Any future additions MUST pass all items before being added.

### 7.1 Mandatory Rules

- [ ] **Positive/celebratory** — The headline must make the recipient feel good. "Sorry Dad" is affectionate teasing, not insult.
- [ ] **No scientific accuracy claims** — Never use "DNA", "genetic", "inherited genes", "scientifically proven", or similar language.
- [ ] **No mean-spiritedness toward the "losing" parent** — The loser is teased gently, never mocked. "Next time!" is fine. "You contributed nothing" is not.
- [ ] **Gender-neutral parent framing** — Headlines must work for any gender combination (two mums, two dads, non-binary parents). The `{winner}` template literal handles this automatically. Hardcoded "MUM"/"DAD" headlines only trigger when the label explicitly matches.
- [ ] **No 50/50 language** — Never display or imply an exact 50/50 split. "Not quite 50/50" is acceptable because it explicitly breaks the tie. "50/50" alone is not.
- [ ] **Max character limits respected** — Hero: 35. Sub-headline: 50. Occasion: 30. Speech bubble: 20. Verified after template resolution.
- [ ] **No health/DNA/ancestry claims** — We analyse visual resemblance. Headlines must reflect this.
- [ ] **No under-13 targeting** — Copy addresses parents/gift-buyers, never children directly.
- [ ] **Works at arm's length** — If you cannot read it on a mug at normal drinking distance, it is too long or too clever. Clarity over cleverness.
- [ ] **No single-parent incompleteness** — Never imply a family is incomplete. "Best of both" works even if only one parent was in the analysis.

### 7.2 Recommended Style

- Prefer puns, wordplay, and cultural references over plain statements.
- Contractions are fine ("I'M", "DOESN'T", "IT'S") — they feel natural in ALL CAPS.
- Exclamation marks are optional but effective for speech bubbles.
- Avoid question marks in hero headlines (they weaken confidence).

---

## 8. A/B Test Recommendations

### 8.1 Priority Tests (launch week)

| Test | Variant A | Variant B | Hypothesis | Metric |
|------|-----------|-----------|------------|--------|
| **T1: Punchy vs Classic** | H001 "MUMMY'S MINI ME" | H003 "MUM DID ALL THE WORK" | Punchy possessives outperform longer phrases on click-to-buy | Conversion rate (preview to cart) |
| **T2: Cheeky vs Warm** | H002 "SORRY DAD, I'M ALL MUM" | H005 "MUM'S GREATEST HIT" | Cheeky "sorry" hook drives more social shares but warm may convert better | Share rate + conversion rate |
| **T3: Short vs Descriptive** | H018 "DADDY'S DOUBLE" (14ch) | H020 "DAD'S CTRL+C, CTRL+V" (20ch) | Shorter headlines are more readable on ceramic; longer ones more shareable on social | Mug order rate |
| **T4: Close call framing** | H035 "THE PERFECT BLEND" | H038 "THE GREAT DEBATE" | Positive framing converts better than competitive framing for close-call results | Conversion rate for 51-59% results |
| **T5: Personalised vs Generic** | H007 "{child}: MUM'S MINI ME" | H001 "MUMMY'S MINI ME" | Adding the child's name increases perceived personalisation and conversion | Conversion rate |

### 8.2 Test Implementation

- Use the seeded hash (Section 6.2) with an additional A/B salt: `hashString(childName + "ab_test_v1")`.
- Even hash = Variant A, Odd hash = Variant B. This ensures consistent assignment per child.
- Track events: `headline_variant_shown`, `headline_variant_converted` with the headline ID as a property.

### 8.3 Expected Performance Rankings (Hypothesis)

Based on competitor analysis (Cornish Prints UK top sellers) and gift-buying psychology:

1. **Highest conversion**: Short possessives (H001, H018) — instant recognition, gift-ready.
2. **Highest share rate**: Cheeky "sorry" variants (H002, H019) — conversation starters on social.
3. **Best for close calls**: "THE PERFECT BLEND" (H035) — positive spin, no losers.
4. **Best for repeat buyers**: Personalised `{child}` variants (H007, H024) — each child gets a unique mug.
5. **Best for Father's Day**: "DAD WINS. FINALLY." (H029) — self-deprecating dad humour, highly shareable.

### 8.4 Seasonal Test Calendar

| Period | Test Focus |
|--------|-----------|
| May (Mother's Day) | Mum-winner headlines + mothers_day occasion header |
| June (Father's Day) | Dad-winner headlines + fathers_day occasion header |
| Nov-Dec (Christmas) | Gift-focused framing, christmas occasion header |
| Year-round | Close-call and blend headlines (birthday occasion) |

---

## Appendix A: Quick Reference — Headline Pool Sizes

| Pool | IDs | Count | Trigger |
|------|-----|-------|---------|
| Mum High | H001-H012 | 12 | winner=mum, pct >= 70 |
| Mum Medium | H013-H017 | 5 | winner=mum, pct 60-69 |
| Dad High | H018-H029 | 12 | winner=dad, pct >= 70 |
| Dad Medium | H030-H034 | 5 | winner=dad, pct 60-69 |
| Close Call | H035-H045 | 11 | pct 51-59 |
| Blend | H046-H050 | 5 | winner=blend/unknown |
| Custom | H051-H060 | 10 | winner label not mum/dad |
| Sub-headlines | F001-F024 | 24 | 8 features x 3 variants |
| Occasion | O001-O011 | 11 | 7 occasions + cultural themes |
| Speech: winner | S001-S007 | 7 | Winner character |
| Speech: loser | S008-S014 | 7 | Loser character |
| Speech: close | S015-S019 | 5 | Close call |
| **Grand total** | | **120** | |

## Appendix B: Integration Notes for FE Lead

1. **Data source**: All inputs come from `useKeepsakeData(childIndex)` — no new data fetching required.
2. **Occasion**: Not currently in `useKeepsakeData`. The template should accept `occasion` as a prop (same pattern as `MugWrapTemplate.jsx` line 25).
3. **Existing utilities**: `truncateAtWord()`, `getOccasionHeader()`, `getOccasionTheme()`, and `FEATURE_LABELS` from `mugThemes.js` are reusable. The headline engine adds a new `selectHeadlines()` function alongside these.
4. **File location**: Suggested placement for the headline engine: `famililook-desktop2/src/components/keepsakes/utils/headlineEngine.js` — co-located with `mugThemes.js`.
5. **No BE changes**: The headline engine is entirely frontend. It consumes existing BE data. No API contract changes required.
6. **Character count verification**: The `resolveTemplates` + length check + fallback cascade is critical. Long child names (e.g., "BARTHOLOMEW") can push personalised headlines over the limit. The algorithm must always produce a valid headline.

---

*This specification was produced by the Copywriter agent. No source code files were modified. Implementation requires FE Lead to build `headlineEngine.js` and consume it from `CharacterMugTemplate.jsx`.*

*Next action: FE Lead implements the selection algorithm and wires it into the Character Mug template.*
