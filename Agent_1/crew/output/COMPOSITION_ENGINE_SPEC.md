# Composition Engine Specification -- Character Mug Product Line

**Author**: FE Lead Agent
**Date**: 30 March 2026
**Status**: READY FOR CEO REVIEW
**Input**: CHARACTER_MUG_COMPOSITION_STUDY.md (task), characterHeadlines.js (existing headline engine), CharacterMugTemplate.jsx (current Hero layout)
**Depends on**: COMPOSITION_RULES.md (Visual Director), MESSAGE_STRATEGY.md (Copywriter)
**Consumer**: Future CharacterMugTemplate.jsx refactor (after CEO approval)

---

## 1. Overview

The Composition Engine is a **pure, deterministic function** that accepts analysis data, occasion, recipient, and variant -- and returns a complete **CompositionPlan** describing every element on the mug. It is the intelligence layer between raw analysis data and the visual template.

The engine does NOT render anything. It produces a data object that the template consumes. This separation means:
- The engine can be unit-tested without rendering
- New layouts can be added by extending the engine's decision tree
- The template only needs to read the plan, never make content decisions

**Determinism guarantee**: The engine uses the existing `djb2` hash from `characterHeadlines.js` for all seeded selections. No `Math.random()`, no `Date.now()`, no external state. Same inputs always produce the same CompositionPlan.

---

## 2. TypeScript-Style Interfaces

### 2.1 Engine Input

```typescript
interface CompositionInput {
  /** Analysis result data */
  data: AnalysisData;

  /** Occasion context -- drives theme, tone, and occasion elements */
  occasion: Occasion;

  /** Who is this mug FOR? Drives tone, headline selection, and element choices */
  recipient: Recipient;

  /** Character art variant */
  variant: "default" | "african";
}

interface AnalysisData {
  /** Which parent won: "parent1" | "parent2" | "blend" | "unknown" */
  winner: "parent1" | "parent2" | "blend" | "unknown";

  /** Winner percentage, integer 51-100. Backend-authoritative. */
  winnerPct: number;

  /** Display label for winning parent, e.g. "Mum", "Dad", custom name */
  winnerLabel: string;

  /** Display label for losing parent */
  loserLabel: string;

  /** Child's name, or null if not provided */
  childName: string | null;

  /** Child's photo URL (data URI or blob URL), or null */
  childPhoto: string | null;

  /** Feature vote map: { eyes: "parent1", nose: "parent2", ... } -- always 8 entries */
  featureVotes: Record<FeatureKey, "parent1" | "parent2">;

  /** The dominant feature (first feature matching winner), e.g. "eyes" */
  dominantFeature: FeatureKey;
}

type FeatureKey =
  | "eyes"
  | "eyebrows"
  | "smile"
  | "nose"
  | "face_shape"
  | "skin"
  | "hair"
  | "ears";

type Occasion =
  | "generic"
  | "mothers_day"
  | "fathers_day"
  | "birthday"
  | "christmas"
  | "valentines"
  | "grandparents_day";

type Recipient =
  | "winner_parent"   // The mug is for the parent who won
  | "loser_parent"    // The mug is for the parent who lost
  | "grandparent"     // The mug is for a grandparent
  | "self"            // The parent buying for themselves
  | "unknown";        // Default -- no specific recipient context
```

### 2.2 Engine Output (CompositionPlan)

```typescript
interface CompositionPlan {
  /** Which layout template to render */
  layout: LayoutType;

  /** Primary character illustration */
  character: CharacterPlan;

  /** Hero headline -- the dominant text element */
  headline: HeadlinePlan;

  /** Child's name display */
  childName: ChildNamePlan;

  /** Child's photo display */
  photo: PhotoPlan;

  /** Score line (percentage + feature) */
  score: ScorePlan;

  /** Feature callout -- "Got Mum's Eyes" etc. */
  featureCallout: FeatureCalloutPlan;

  /** Speech bubble near the primary character */
  speechBubble: SpeechBubblePlan;

  /** Occasion tag -- "Happy Mother's Day" etc. */
  occasionTag: OccasionTagPlan;

  /** Second character (the "other" parent) */
  secondCharacter: SecondCharacterPlan;

  /** Brand mark -- always present */
  brand: BrandPlan;

  /** Total visible element count (for validation -- hard cap 7) */
  elementCount: number;

  /** Debug: explains why this composition was chosen */
  _reasoning: string;
}

type LayoutType = "hero" | "celebration" | "blend" | "gift";

interface CharacterPlan {
  /** Character type */
  type: "mama" | "papa" | "cub" | "mini" | "gran" | "gramps";

  /** Emotion/pose */
  emotion: string;

  /** Resolved variant for asset lookup */
  variant: "default" | "african";
}

interface HeadlinePlan {
  /** The headline text, with \n for line breaks */
  text: string;

  /** Font size tier -- template maps to exact px values per layout */
  size: "large" | "medium" | "small";
}

interface ChildNamePlan {
  /** Whether to show the child's name at all */
  show: boolean;

  /** How the name is displayed */
  format: "standalone" | "in_headline" | "in_score";

  /** The resolved text (e.g. "OLIVIA", "For Olivia") -- null when show=false */
  text: string | null;
}

interface PhotoPlan {
  /** Whether to show the photo */
  show: boolean;

  /** Size tier -- template maps to exact px values */
  size: "large" | "small" | "hidden";
}

interface ScorePlan {
  /** Whether to show the score */
  show: boolean;

  /** How prominent the score is */
  format: "prominent" | "subtle" | "hidden";

  /** The resolved score text, e.g. "72% Mum" or "72% Mum . Got Mum's Eyes" */
  text: string | null;
}

interface FeatureCalloutPlan {
  /** Whether to show a standalone feature callout */
  show: boolean;

  /** The resolved text, e.g. "GOT MUM'S EYES" */
  text: string | null;
}

interface SpeechBubblePlan {
  /** Whether to show the speech bubble */
  show: boolean;

  /** The bubble text */
  text: string | null;

  /** Whose voice the bubble represents */
  voice: "winner" | "loser" | "child" | "narrator";
}

interface OccasionTagPlan {
  /** Whether to show the occasion tag */
  show: boolean;

  /** The tag text, e.g. "HAPPY MOTHER'S DAY" */
  text: string | null;
}

interface SecondCharacterPlan {
  /** Whether to show a second character */
  show: boolean;

  /** Character type for the second character */
  type: "mama" | "papa" | "cub" | "mini" | "gran" | "gramps" | null;

  /** Emotion for the second character */
  emotion: string | null;

  /** Variant for the second character */
  variant: "default" | "african";
}

interface BrandPlan {
  /** Always true -- brand mark is mandatory */
  show: true;

  /** The brand text */
  text: "famililook.com";
}
```

---

## 3. Layout Templates

Each layout has a fixed panel structure, mandatory elements, optional elements, and excluded elements. All layouts render at **830x345px CSS** (2670x1110px at print resolution). Transparent background.

### 3.1 Layout A: "Hero"

**When selected**: Decisive wins (70%+), playful tone, any recipient except grandparent.

**Panel structure**: 40% left (character) / 60% right (content). Character bleeds 18px into the content panel.

| Element | Status | Position |
|---------|--------|----------|
| Character | **Mandatory** | Left panel, bottom-aligned |
| Headline | **Mandatory** | Right panel, vertically centred, large |
| Score line | **Mandatory** | Right panel, below headline, subtle |
| Speech bubble | **Optional** | Above character, top-right of left panel |
| Photo | **Optional** | Right panel, below score line, small circle |
| Brand | **Mandatory** | Bottom-right corner |
| Occasion tag | Excluded | -- |
| Second character | Excluded | -- |
| Feature callout | Excluded | (merged into score line) |
| Child name | **Optional** | In headline (template literal) or standalone below headline |

**Max elements**: 6 (character + headline + score + bubble + photo + brand)

### 3.2 Layout B: "Celebration"

**When selected**: Gift for the winner parent, or moderate wins (60-69%) when recipient is known.

**Panel structure**: 30% left (character) / 40% centre (personal content) / 30% right (data).

| Element | Status | Position |
|---------|--------|----------|
| Character | **Mandatory** | Left panel, bottom-aligned |
| Headline | **Mandatory** | Centre panel, medium size |
| Child name | **Mandatory** (if available) | Centre panel, above headline, standalone |
| Photo | **Optional** | Centre panel, above child name, large circle |
| Score line | **Mandatory** | Right panel, subtle |
| Feature callout | **Optional** | Right panel, below score |
| Brand | **Mandatory** | Bottom-right corner |
| Speech bubble | Excluded | -- |
| Second character | Excluded | -- |
| Occasion tag | Excluded | -- |

**Max elements**: 7 (character + headline + name + photo + score + callout + brand)

### 3.3 Layout C: "Blend"

**When selected**: Close calls (51-59%), blend/unknown winners, or any result where recipient is "loser_parent".

**Panel structure**: 25% left (character A) / 50% centre (headline + shared content) / 25% right (character B).

| Element | Status | Position |
|---------|--------|----------|
| Character (winner) | **Mandatory** | Left panel, bottom-aligned |
| Second character (loser) | **Mandatory** | Right panel, bottom-aligned, mirrored |
| Headline | **Mandatory** | Centre, large, unity-focused |
| Child name | **Optional** | Centre, below headline |
| Score line | **Optional** | Centre, below name, subtle |
| Brand | **Mandatory** | Bottom-centre |
| Photo | Excluded | -- |
| Speech bubble | Excluded | -- |
| Occasion tag | Excluded | -- |
| Feature callout | Excluded | -- |

**Max elements**: 6 (charA + charB + headline + name + score + brand)

### 3.4 Layout D: "Gift"

**When selected**: Any occasion other than "generic", or recipient is "grandparent".

**Panel structure**: Full-width stacked: occasion header top / character + personal content centre / brand bottom.

| Element | Status | Position |
|---------|--------|----------|
| Occasion tag | **Mandatory** | Top banner, full width |
| Character | **Mandatory** | Centre-left, medium size |
| Headline | **Mandatory** | Centre-right, medium |
| Child name | **Optional** | Below headline |
| Photo | **Optional** | Next to character, small |
| Score line | **Optional** | Below child name, subtle |
| Brand | **Mandatory** | Bottom-right |
| Speech bubble | Excluded | -- |
| Second character | Excluded | -- |
| Feature callout | Excluded | -- |

**Max elements**: 7 (occasion + character + headline + name + photo + score + brand)

---

## 4. Composition Engine Algorithm

The engine is a deterministic decision tree. Each step narrows the choices until a complete CompositionPlan is produced.

### 4.1 Step 1: Derive Context

```
FUNCTION deriveContext(input: CompositionInput) -> DerivedContext:

  parentType = normaliseParent(input.data.winnerLabel)  // "mum" | "dad" | "custom"
  isBlend = (input.data.winner === "blend" || input.data.winner === "unknown")

  IF isBlend:
    pctBracket = "blend"
  ELSE IF input.data.winnerPct >= 70:
    pctBracket = "high"
  ELSE IF input.data.winnerPct >= 60:
    pctBracket = "medium"
  ELSE:
    pctBracket = "close"

  hasChildName = (input.data.childName !== null && input.data.childName.trim() !== "")
  hasChildPhoto = (input.data.childPhoto !== null && input.data.childPhoto !== "")
  hasOccasion = (input.occasion !== "generic")

  RETURN { parentType, isBlend, pctBracket, hasChildName, hasChildPhoto, hasOccasion }
```

### 4.2 Step 2: Select Layout

The layout is chosen by a priority-ordered rule set. First matching rule wins.

```
FUNCTION selectLayout(input, ctx: DerivedContext) -> LayoutType:

  // Rule 1: Gift layout for seasonal occasions (except generic)
  IF ctx.hasOccasion AND input.occasion !== "generic":
    RETURN "gift"

  // Rule 2: Gift layout for grandparent recipient
  IF input.recipient === "grandparent":
    RETURN "gift"

  // Rule 3: Blend layout for close calls and blends
  IF ctx.pctBracket === "close" OR ctx.pctBracket === "blend":
    RETURN "blend"

  // Rule 4: Blend layout when mug is for the losing parent
  IF input.recipient === "loser_parent":
    RETURN "blend"

  // Rule 5: Celebration layout when recipient is winner_parent and photo exists
  IF input.recipient === "winner_parent" AND ctx.hasChildPhoto:
    RETURN "celebration"

  // Rule 6: Celebration layout for moderate wins with known recipient
  IF ctx.pctBracket === "medium" AND input.recipient !== "unknown":
    RETURN "celebration"

  // Rule 7: Default -- Hero layout for decisive wins
  RETURN "hero"
```

### 4.3 Step 3: Select Primary Character

```
FUNCTION selectCharacter(input, ctx, layout) -> CharacterPlan:

  // Determine character type
  IF input.recipient === "grandparent":
    type = (ctx.parentType === "mum") ? "gran" : "gramps"
  ELSE IF layout === "celebration" AND ctx.hasChildPhoto:
    // Winner parent character celebrating with child context
    type = (ctx.parentType === "mum") ? "mama" : "papa"
  ELSE:
    type = (ctx.parentType === "mum") ? "mama" : "papa"
    // Custom parents default to "mama" (matches current behaviour)

  // Determine emotion
  emotion = selectEmotion(input, ctx, type)

  // Remap emotion for character compatibility
  emotion = remapEmotion(type, emotion)

  // Resolve variant
  variant = input.variant
  IF variant is unset AND input.occasion in ["heritage_gold", "carnival_spirit", "ubuntu"]:
    variant = "african"
  ELSE IF variant is unset:
    variant = "default"

  RETURN { type, emotion, variant }
```

#### Emotion Selection Sub-algorithm

```
FUNCTION selectEmotion(input, ctx, charType) -> string:

  // Layer 1: Recipient-driven overrides
  IF input.recipient === "winner_parent":
    RETURN "proud"
  IF input.recipient === "grandparent":
    RETURN "showing_off"
  IF input.recipient === "loser_parent":
    RETURN "loving"    // Warm, not defeated

  // Layer 2: Occasion-driven overrides
  IF input.occasion === "mothers_day" OR input.occasion === "fathers_day":
    RETURN "proud"
  IF input.occasion === "birthday" OR input.occasion === "christmas":
    RETURN "celebrating"
  IF input.occasion === "valentines":
    RETURN "loving"
  IF input.occasion === "grandparents_day":
    RETURN "showing_off"

  // Layer 3: Percentage-driven
  IF ctx.pctBracket === "high":     RETURN "celebrating"
  IF ctx.pctBracket === "medium":   RETURN "proud"
  IF ctx.pctBracket === "close":    RETURN "cheeky"
  IF ctx.pctBracket === "blend":    RETURN "surprised"

  RETURN "proud"  // fallback
```

#### Emotion Remapping (unchanged from current implementation)

```
FUNCTION remapEmotion(charType, emotion) -> string:
  IF (charType === "gran" OR charType === "gramps") AND emotion === "cheeky":
    RETURN "showing_off"
  IF charType === "cub" AND emotion === "celebrating":
    RETURN "giggling"
  IF charType === "cub" AND emotion === "cheeky":
    RETURN "curious"
  RETURN emotion
```

### 4.4 Step 4: Select Second Character (Blend layout only)

```
FUNCTION selectSecondCharacter(input, ctx, layout) -> SecondCharacterPlan:

  IF layout !== "blend":
    RETURN { show: false, type: null, emotion: null, variant: input.variant || "default" }

  // Second character is the "other" parent
  loserType = normaliseParent(input.data.loserLabel)

  IF loserType === "mum":
    type = "mama"
  ELSE IF loserType === "dad":
    type = "papa"
  ELSE:
    // For custom labels, use opposite of primary character
    type = (ctx.parentType === "mum") ? "papa" : "mama"

  // Loser emotion depends on pctBracket
  IF ctx.pctBracket === "close" OR ctx.pctBracket === "blend":
    emotion = "cheeky"     // Playful -- "we both contributed"
  ELSE:
    emotion = "surprised"  // Lighthearted reaction

  emotion = remapEmotion(type, emotion)

  RETURN { show: true, type, emotion, variant: input.variant || "default" }
```

### 4.5 Step 5: Select Headline

The headline is produced by calling the existing `selectHeadlines()` function from `characterHeadlines.js`, plus new recipient-aware pools.

```
FUNCTION selectHeadline(input, ctx, layout) -> HeadlinePlan:

  // Check if a recipient-specific pool should override
  recipientPool = getRecipientHeadlinePool(input.recipient, ctx)

  IF recipientPool !== null:
    // Use seeded selection from recipient pool
    seed = djb2Hash((input.data.childName || "FamiliLook") + input.data.winnerPct + input.recipient)
    text = recipientPool[abs(seed) % recipientPool.length]
    text = resolveTemplates(text, {
      child: (input.data.childName || "").toUpperCase(),
      winner: (input.data.winnerLabel || "PARENT").toUpperCase(),
      loser: (input.data.loserLabel || "PARENT").toUpperCase(),
    })
  ELSE:
    // Delegate to existing selectHeadlines() for generic/default behaviour
    headlines = selectHeadlines({
      winner: input.data.winner,
      winnerPct: input.data.winnerPct,
      winnerLabel: input.data.winnerLabel,
      loserLabel: input.data.loserLabel,
      childName: input.data.childName,
      dominantFeature: input.data.dominantFeature,
      occasion: input.occasion,
    })
    text = headlines.heroHeadline

  // Determine size based on layout
  IF layout === "hero":
    size = "large"
  ELSE IF layout === "blend":
    size = "large"
  ELSE:
    size = "medium"

  // Enforce 35-char limit (ignoring newlines)
  IF text.replace(/\n/g, "").length > 35:
    text = truncateAtWord(text.replace(/\n/g, " "), 35)

  RETURN { text, size }
```

### 4.6 Step 6: Compose Remaining Elements

```
FUNCTION composeElements(input, ctx, layout) -> Partial<CompositionPlan>:

  // ── Child Name ──
  childName = { show: false, format: "standalone", text: null }
  IF ctx.hasChildName:
    IF layout === "hero":
      // Check if headline already contains child name
      IF headline.text contains input.data.childName.toUpperCase():
        childName = { show: true, format: "in_headline", text: null }
      ELSE:
        childName = { show: true, format: "standalone", text: input.data.childName.toUpperCase() }
    ELSE IF layout === "celebration":
      childName = { show: true, format: "standalone", text: "For " + input.data.childName }
    ELSE IF layout === "blend":
      childName = { show: true, format: "standalone", text: input.data.childName.toUpperCase() }
    ELSE IF layout === "gift":
      childName = { show: true, format: "standalone", text: input.data.childName.toUpperCase() }

  // ── Photo ──
  photo = { show: false, size: "hidden" }
  IF ctx.hasChildPhoto:
    IF layout === "hero":
      photo = { show: true, size: "small" }
    ELSE IF layout === "celebration":
      photo = { show: true, size: "large" }
    ELSE IF layout === "gift":
      photo = { show: true, size: "small" }
    // Blend layout: photo excluded

  // ── Score Line ──
  featureLabel = FEATURE_LABELS[input.data.dominantFeature] || input.data.dominantFeature
  scoreFull = input.data.winnerPct + "% " + input.data.winnerLabel + " . Got " + input.data.winnerLabel + "'s " + featureLabel
  scoreShort = input.data.winnerPct + "% " + input.data.winnerLabel

  score = { show: true, format: "subtle", text: scoreFull }

  IF layout === "hero":
    score = { show: true, format: "subtle", text: scoreFull }
  ELSE IF layout === "celebration":
    score = { show: true, format: "subtle", text: scoreShort }
  ELSE IF layout === "blend":
    // For blends, show the score only if it's not a true blend
    IF ctx.isBlend:
      score = { show: false, format: "hidden", text: null }
    ELSE:
      score = { show: true, format: "subtle", text: scoreShort }
  ELSE IF layout === "gift":
    // Occasion mugs: score is secondary to the message
    IF input.recipient === "grandparent":
      score = { show: true, format: "subtle", text: scoreShort }
    ELSE:
      score = { show: true, format: "subtle", text: scoreFull }

  // ── Feature Callout ──
  featureCallout = { show: false, text: null }
  IF layout === "celebration":
    featureCallout = { show: true, text: headlines.featureSubline }

  // ── Speech Bubble ──
  speechBubble = { show: false, text: null, voice: "winner" }
  IF layout === "hero":
    speechBubble = { show: true, text: headlines.winnerBubble, voice: "winner" }

  // ── Occasion Tag ──
  occasionTag = { show: false, text: null }
  IF layout === "gift" AND ctx.hasOccasion:
    occasionTag = { show: true, text: headlines.occasionHeader }

  // ── Brand ──
  brand = { show: true, text: "famililook.com" }

  RETURN { childName, photo, score, featureCallout, speechBubble, occasionTag, brand }
```

### 4.7 Step 7: Validate Element Count

```
FUNCTION validateElementCount(plan: CompositionPlan) -> CompositionPlan:

  count = 0
  IF plan.character.type:              count += 1  // Always: +1
  IF plan.headline.text:               count += 1  // Always: +1
  IF plan.childName.show AND plan.childName.format === "standalone":  count += 1
  IF plan.photo.show:                  count += 1
  IF plan.score.show:                  count += 1
  IF plan.featureCallout.show:         count += 1
  IF plan.speechBubble.show:           count += 1
  IF plan.occasionTag.show:            count += 1
  IF plan.secondCharacter.show:        count += 1
  // brand counts as 1 but is mandatory
  count += 1

  // Hard cap: 7 elements. Shed lowest-priority elements.
  // Priority order (lowest = shed first):
  //   featureCallout < speechBubble < photo < score < childName < secondCharacter < character < headline < brand < occasionTag
  WHILE count > 7:
    IF plan.featureCallout.show:
      plan.featureCallout = { show: false, text: null }; count -= 1; CONTINUE
    IF plan.speechBubble.show:
      plan.speechBubble = { show: false, text: null, voice: "winner" }; count -= 1; CONTINUE
    IF plan.photo.show:
      plan.photo = { show: false, size: "hidden" }; count -= 1; CONTINUE
    IF plan.score.show:
      plan.score = { show: false, format: "hidden", text: null }; count -= 1; CONTINUE
    BREAK  // Never shed headline, character, brand, or occasion tag

  plan.elementCount = count
  RETURN plan
```

### 4.8 Full Pipeline

```
FUNCTION composeCharacterMug(input: CompositionInput) -> CompositionPlan:

  // Step 1: Derive context
  ctx = deriveContext(input)

  // Step 2: Select layout
  layout = selectLayout(input, ctx)

  // Step 3: Select primary character
  character = selectCharacter(input, ctx, layout)

  // Step 4: Select second character
  secondCharacter = selectSecondCharacter(input, ctx, layout)

  // Step 5: Select headline (calls into characterHeadlines.js)
  headlines = selectHeadlines({ ...input.data, occasion: input.occasion })
  headline = selectHeadline(input, ctx, layout)

  // Step 6: Compose remaining elements
  elements = composeElements(input, ctx, layout)

  // Step 7: Assemble plan
  plan = {
    layout,
    character,
    headline,
    ...elements,
    secondCharacter,
    _reasoning: buildReasoning(input, ctx, layout),
  }

  // Step 8: Validate and enforce element cap
  plan = validateElementCount(plan)

  RETURN plan
```

---

## 5. Recipient Logic

The `recipient` field is a new concept. It answers: "Who is this mug being purchased FOR?" This fundamentally changes the mug's tone and message.

### 5.1 Recipient Behaviour Matrix

| Recipient | Tone | Headline Pool | Score Visibility | Character Choice | Photo Use |
|-----------|------|---------------|-----------------|-----------------|-----------|
| `winner_parent` | Triumphant, direct address | `RECIPIENT_WINNER` pool | Prominent -- it validates them | Winner parent character, proud | Large if available |
| `loser_parent` | Warm, inclusive, affectionate | `RECIPIENT_LOSER` pool | Subtle -- don't rub it in | Both characters (Blend layout) | Hidden |
| `grandparent` | Warm, showing off grandchild | `RECIPIENT_GRANDPARENT` pool | Subtle | Gran/Gramps character | Small if available |
| `self` | Fun, self-referential | Standard pools (no override) | Standard | Winner parent character | Standard |
| `unknown` | Default behaviour | Standard pools (no override) | Standard | Winner parent character | Standard |

### 5.2 How Recipient Overrides Work

The recipient does NOT bypass the engine. Instead, it applies as a **modifier** at two points:

1. **Layout selection** (Step 2): `grandparent` forces Gift layout. `loser_parent` forces Blend layout.
2. **Headline pool override** (Step 5): If a recipient-specific pool exists, it takes priority over the standard pool.

All other elements (score, photo, etc.) are still derived by the standard rules -- the layout choice naturally adjusts them.

### 5.3 Why This Matters Per Recipient

**winner_parent** ("Mum wins, mug is for Mum"):
The mug speaks TO them. "YOUR mini me." "Look what YOU made." The score validates THEIR genes. The child's photo shows THEIR child looking like THEM. Maximum celebration.

**loser_parent** ("Mum wins, mug is for Dad"):
The mug must NOT feel like a trophy for the other side. Instead, it highlights the features the child DID get from this parent. "They may look like Mum, but those eyes? ALL YOU." Both characters appear -- togetherness, not defeat. Score is subtle.

**grandparent** ("Any result, mug is for Gran"):
The mug shows off the grandchild. The analysis result is secondary. "YOUR grandchild -- officially adorable." Character is Gran/Gramps, not Mama/Papa. Photo (if available) is prominent because grandparents want to see the child.

**self** ("Parent buying for themselves"):
Standard behaviour. No special overrides. The parent is buying to commemorate the result, so the standard celebration or blend tone applies.

**unknown** ("Default"):
Standard behaviour. No recipient-specific customisation. Safest default.

---

## 6. Headline Integration with characterHeadlines.js

### 6.1 Current System (No Changes Required)

The existing `selectHeadlines()` function in `characterHeadlines.js` already handles:
- Parent normalisation (mum/dad/custom)
- Percentage bracket classification (high/medium/close/blend)
- Hero headline selection from gendered pools
- Feature sub-headline generation
- Occasion header resolution
- Speech bubble selection (winner/loser/close_call)
- Deterministic seeded selection via `djb2` hash
- Template literal resolution (`{child}`, `{winner}`, `{loser}`)
- 35-character limit enforcement

The composition engine calls `selectHeadlines()` for its standard headline, sub-headline, occasion header, and speech bubbles.

### 6.2 NEW Headline Pools (Recipient-Specific)

These pools are NEW and must be added to `characterHeadlines.js` alongside the existing `HEADLINES` object. They follow the exact same template literal pattern (`{child}`, `{winner}`, `{loser}`).

```javascript
const RECIPIENT_HEADLINES = {

  // ── For the winning parent ──────────────────────────────────────
  winner_parent: {
    mum: {
      high: [
        "YOUR\nMINI ME",
        "YOU DID THIS,\nMUM",
        "LOOK WHAT\nYOU MADE",
        "YOUR GREATEST\nCREATION",
        "PROOF YOU'RE\nAMAZING",
        "{child} IS\nALL YOU",
        "YOUR GENES\nWON",
        "THEY'RE YOUR\nTWIN",
      ],
      medium: [
        "MOSTLY YOU,\nMUM",
        "YOUR SIDE\nIS STRONG",
        "THEY TAKE\nAFTER YOU",
        "YOUR INFLUENCE\nIS SHOWING",
        "LOOK FAMILIAR,\nMUM?",
      ],
    },
    dad: {
      high: [
        "YOUR\nMINI ME",
        "YOU DID THIS,\nDAD",
        "LOOK WHAT\nYOU MADE",
        "YOUR GREATEST\nCREATION",
        "PROOF YOU'RE\nAMAZING",
        "{child} IS\nALL YOU",
        "YOUR GENES\nWON",
        "THEY'RE YOUR\nTWIN",
      ],
      medium: [
        "MOSTLY YOU,\nDAD",
        "YOUR SIDE\nIS STRONG",
        "THEY TAKE\nAFTER YOU",
        "YOUR INFLUENCE\nIS SHOWING",
        "LOOK FAMILIAR,\nDAD?",
      ],
    },
    custom: [
      "YOUR\nMINI ME",
      "YOU DID THIS,\n{winner}",
      "LOOK WHAT\nYOU MADE",
      "{child} IS\nALL YOU",
      "YOUR GENES\nWON",
    ],
  },

  // ── For the losing parent ───────────────────────────────────────
  loser_parent: {
    mum: [
      "THEY MAY LOOK\nLIKE DAD, BUT...",
      "YOUR {feature}\nTHOUGH",
      "DAD'S FACE,\nMUM'S HEART",
      "BEST OF BOTH,\nTHANKS TO YOU",
      "YOU'RE IN THERE\nTOO, MUM",
      "YOUR MARK\nIS THERE",
      "THEY GOT THE\nBEST OF YOU",
    ],
    dad: [
      "THEY MAY LOOK\nLIKE MUM, BUT...",
      "YOUR {feature}\nTHOUGH",
      "MUM'S FACE,\nDAD'S SPIRIT",
      "BEST OF BOTH,\nTHANKS TO YOU",
      "YOU'RE IN THERE\nTOO, DAD",
      "YOUR MARK\nIS THERE",
      "THEY GOT THE\nBEST OF YOU",
    ],
    custom: [
      "THEY MAY LOOK\nLIKE {winner}, BUT...",
      "BEST OF BOTH,\nTHANKS TO YOU",
      "YOU'RE IN\nTHERE TOO",
      "YOUR MARK\nIS THERE",
      "THEY GOT THE\nBEST OF YOU",
    ],
  },

  // ── For grandparents ────────────────────────────────────────────
  grandparent: [
    "YOUR\nGRANDCHILD",
    "OFFICIALLY\nADORABLE",
    "LOOK WHO'S\nGROWING UP",
    "YOUR FAMILY\nLEGACY",
    "RUNS IN\nTHE FAMILY",
    "GUESS WHO\n{child} LOOKS LIKE",
    "THE FAMILY\nTRADITION",
    "YOUR GENES\nLIVE ON",
  ],
};
```

### 6.3 Recipient Pool Selection Logic

```
FUNCTION getRecipientHeadlinePool(recipient, ctx) -> string[] | null:

  IF recipient === "self" OR recipient === "unknown":
    RETURN null  // Use standard selectHeadlines()

  IF recipient === "winner_parent":
    pool = RECIPIENT_HEADLINES.winner_parent
    IF ctx.parentType === "mum":
      RETURN pool.mum[ctx.pctBracket] || pool.mum.medium
    ELSE IF ctx.parentType === "dad":
      RETURN pool.dad[ctx.pctBracket] || pool.dad.medium
    ELSE:
      RETURN pool.custom

  IF recipient === "loser_parent":
    pool = RECIPIENT_HEADLINES.loser_parent
    loserType = normaliseParent(input.data.loserLabel)
    IF loserType === "mum":
      RETURN pool.mum
    ELSE IF loserType === "dad":
      RETURN pool.dad
    ELSE:
      RETURN pool.custom

  IF recipient === "grandparent":
    RETURN RECIPIENT_HEADLINES.grandparent

  RETURN null
```

### 6.4 Template Literal Extension

The existing resolver handles `{child}`, `{winner}`, `{loser}`. The `loser_parent` pool introduces `{feature}` -- the loser parent's best feature. This requires one addition to `resolveTemplates()`:

```javascript
// New template variable:
// {feature} = the FEATURE LABEL of the losing parent's strongest feature
//             e.g. "EYES", "SMILE"

function resolveTemplates(text, vars) {
  return text
    .replace(/\{child\}/g, vars.child || "")
    .replace(/\{winner\}/g, vars.winner || "")
    .replace(/\{loser\}/g, vars.loser || "")
    .replace(/\{feature\}/g, vars.feature || "");  // NEW
}
```

The `feature` variable is derived from the loser's best feature: the first entry in `featureVotes` where the value does NOT match `data.winner`.

---

## 7. Degradation Rules

When optional data is missing, the engine must produce a valid composition that still feels complete. No blank spaces, no placeholder text, no broken layouts.

### 7.1 childName is null

| Layout | Behaviour |
|--------|-----------|
| Hero | Headline uses non-personalised variant (e.g. "MUMMY'S MINI ME" instead of "OLIVIA: MUMMY'S MINI ME"). `childName.show = false`. |
| Celebration | Centre panel omits name line. Photo (if present) sits above headline directly. |
| Blend | Centre panel omits name line. No visual gap. |
| Gift | Occasion tag + headline only. Birthday occasion falls back to "HAPPY BIRTHDAY" without name. |

### 7.2 childPhoto is null

| Layout | Behaviour |
|--------|-----------|
| Hero | Headline gets `size: "large"` (42px instead of 36px). No photo element. Score line has more breathing room. |
| Celebration | Falls back to Hero layout if no photo AND no childName. Otherwise, centre panel shows name + headline without photo. |
| Blend | No change (photo is already excluded from Blend). |
| Gift | No change (photo is optional in Gift). Character gets more horizontal space. |

### 7.3 Both childName AND childPhoto are null

| Layout | Behaviour |
|--------|-----------|
| Hero | Standard Hero with maximum headline size. Feels bold and product-focused: "MUMMY'S MINI ME" + score + character. |
| Celebration | **Downgrades to Hero layout.** Celebration without personal content has no justification. |
| Blend | Standard Blend. Two characters + unity headline still work without child context. |
| Gift | Standard Gift. Occasion tag + character + headline is still gift-worthy. Score subtly placed. |

### 7.4 Degradation Decision Tree

```
FUNCTION applyDegradation(plan, ctx) -> CompositionPlan:

  // Celebration requires at least childName OR childPhoto
  IF plan.layout === "celebration" AND NOT ctx.hasChildName AND NOT ctx.hasChildPhoto:
    plan.layout = "hero"
    plan = recomposeForLayout(plan, "hero")
    plan._reasoning += " | Degraded celebration->hero: no child data"

  // Gift layout: birthday without childName loses personalisation
  IF plan.layout === "gift" AND input.occasion === "birthday" AND NOT ctx.hasChildName:
    plan.occasionTag.text = "HAPPY BIRTHDAY"  // Remove name placeholder

  // Hero without photo: increase headline size
  IF plan.layout === "hero" AND NOT ctx.hasChildPhoto:
    plan.headline.size = "large"

  RETURN plan
```

---

## 8. Determinism Guarantee

### 8.1 Seed Construction

All seeded selections use the existing `djb2` hash from `characterHeadlines.js`:

```
seed = djb2Hash(seedString)
index = abs(seed) % pool.length
```

The seed string varies by selection type to avoid correlated picks:

| Selection | Seed String |
|-----------|-------------|
| Hero headline | `(childName \|\| "FamiliLook") + winnerPct` |
| Recipient headline | `(childName \|\| "FamiliLook") + winnerPct + recipient` |
| Feature sub-headline | Same as hero headline (current behaviour) |
| Speech bubble (winner) | Same as hero headline (current behaviour) |
| Speech bubble (loser) | Same as hero headline + 1 (current behaviour) |

### 8.2 What is NOT Seeded

The following are determined by explicit rules, not random selection:
- Layout selection (deterministic decision tree)
- Character type (derived from winner label)
- Character emotion (deterministic priority chain)
- Element visibility (deterministic per-layout rules)
- Element count validation (deterministic priority shedding)
- Score text (computed from data)
- Occasion header text (lookup table)

### 8.3 Invariant

```
FOR ANY input I:
  composeCharacterMug(I) === composeCharacterMug(I)
  // Deep equality. Always. No exceptions.
```

No `Math.random()`. No `Date.now()`. No side effects. No external state reads. The function is pure.

---

## 9. Modularity and Extension Points

### 9.1 Adding a New Layout

1. Add the layout type to the `LayoutType` union: e.g. `"duo_gift"`
2. Add a row to Section 3 defining panel structure and element matrix
3. Add a rule to `selectLayout()` in Section 4.2 (insert at correct priority)
4. Add element composition rules for the new layout in `composeElements()` (Section 4.6)
5. The template renderer reads `plan.layout` and picks the corresponding JSX panel structure

### 9.2 Adding a New Recipient

1. Add the recipient string to the `Recipient` type union
2. Add a row to the Recipient Behaviour Matrix (Section 5.1)
3. Add headline pool entries in `RECIPIENT_HEADLINES` (Section 6.2)
4. Add selection logic in `getRecipientHeadlinePool()` (Section 6.3)
5. Add any layout overrides in `selectLayout()` if the recipient forces a specific layout

### 9.3 Adding a New Occasion

1. Add the occasion string to the `Occasion` type union
2. Add a colour palette entry in `mugThemes.js` -> `OCCASION_THEMES`
3. Add a header text entry in `characterHeadlines.js` -> `CHARACTER_OCCASION_HEADERS`
4. Add emotion override in `selectEmotion()` if the occasion has a specific mood
5. No other engine changes needed -- the Gift layout and occasion tag handle it automatically

### 9.4 Adding New Elements

1. Add the element interface to `CompositionPlan` (Section 2.2)
2. Add element to each layout's element matrix (Section 3)
3. Add composition logic in `composeElements()` (Section 4.6)
4. Add the element to `validateElementCount()` with a priority level (Section 4.7)
5. The template renderer reads the new field and renders it in the appropriate position

---

## 10. Implementation Checklist

When implementing this spec, the developer should:

- [ ] Create `composeCharacterMug()` as a pure function in a new file `compositionEngine.js` alongside `characterHeadlines.js`
- [ ] Add `RECIPIENT_HEADLINES` to `characterHeadlines.js`
- [ ] Add `{feature}` template variable support to `resolveTemplates()`
- [ ] Export `getRecipientHeadlinePool()` from `characterHeadlines.js`
- [ ] Create layout-specific JSX panel components inside `CharacterMugTemplate.jsx` (Hero, Celebration, Blend, Gift)
- [ ] Wire `composeCharacterMug()` into `CharacterMugTemplate.jsx` as the first step before rendering
- [ ] Add `recipient` to the keepsake data flow (new prop on the template, selectable in the keepsake UI)
- [ ] Write unit tests for `composeCharacterMug()` covering all recipient x occasion x pctBracket combinations
- [ ] Verify determinism: same inputs produce same output across 1000 runs
- [ ] Verify element cap: no composition ever exceeds 7 visible elements
- [ ] Verify degradation: all null-data scenarios produce valid, non-broken compositions

---

## Appendix A: Worked Examples

### Example 1: Decisive win, no recipient context

**Input**: `{ winner: "parent1", winnerPct: 78, winnerLabel: "Mum", loserLabel: "Dad", childName: "Olivia", childPhoto: "blob:...", dominantFeature: "eyes" }`, occasion: "generic", recipient: "unknown", variant: "default"

**Engine trace**:
- Context: parentType=mum, pctBracket=high, hasChildName=true, hasChildPhoto=true, hasOccasion=false
- Layout: Rule 7 matches -> **hero**
- Character: mama, emotion=celebrating (high pct), remapped=celebrating
- Headline: Standard pool HEADLINES.mum.high, seeded -> e.g. "OLIVIA:\nMUM'S MINI ME", size=large->medium (photo present)
- Photo: show=true, size=small
- Score: "78% Mum . Got Mum's Eyes", format=subtle
- Speech bubble: winner_proud pool -> e.g. "TOLD YOU SO!"
- Element count: character + headline + score + photo + bubble + brand = 6 (under cap)

### Example 2: Close call, mug for losing parent

**Input**: `{ winner: "parent1", winnerPct: 53, winnerLabel: "Mum", loserLabel: "Dad", childName: "Leo", childPhoto: null, dominantFeature: "smile" }`, occasion: "generic", recipient: "loser_parent", variant: "default"

**Engine trace**:
- Context: parentType=mum, pctBracket=close, hasChildName=true, hasChildPhoto=false, hasOccasion=false
- Layout: Rule 3 (close call) -> **blend**. Rule 4 (loser_parent) would also match.
- Character: mama, emotion=loving (loser_parent override), remapped=loving
- Second character: papa, emotion=cheeky (close call), remapped=cheeky
- Headline: Recipient pool RECIPIENT_LOSER.dad -> e.g. "MUM'S FACE,\nDAD'S SPIRIT", size=large
- ChildName: show=true, format=standalone, text="LEO"
- Score: show=true, format=subtle, text="53% Mum"
- Photo: excluded (blend layout)
- Speech bubble: excluded (blend layout)
- Element count: charA + charB + headline + name + score + brand = 6 (under cap)

### Example 3: Mother's Day gift for grandparent

**Input**: `{ winner: "parent2", winnerPct: 65, winnerLabel: "Dad", loserLabel: "Mum", childName: null, childPhoto: null, dominantFeature: "nose" }`, occasion: "mothers_day", recipient: "grandparent", variant: "default"

**Engine trace**:
- Context: parentType=dad, pctBracket=medium, hasChildName=false, hasChildPhoto=false, hasOccasion=true
- Layout: Rule 1 (has occasion) -> **gift**
- Character: gran (grandparent override), emotion=showing_off, remapped=showing_off
- Headline: Recipient pool RECIPIENT_GRANDPARENT -> e.g. "YOUR FAMILY\nLEGACY", size=medium
- Occasion tag: "HAPPY MOTHER'S DAY"
- ChildName: show=false (null)
- Photo: show=false (null)
- Score: show=true, format=subtle, text="65% Dad"
- Element count: occasion + character + headline + score + brand = 5 (under cap)

---

## Appendix B: Decision Tree Summary (Quick Reference)

```
                          ┌──────────────┐
                          │ Has Occasion?│
                          └──────┬───────┘
                           yes   │   no
                     ┌───────────┘   └───────────────────────┐
                     v                                        v
                ┌─────────┐                         ┌──────────────────┐
                │  GIFT   │                         │ Recipient =      │
                └─────────┘                         │ grandparent?     │
                                                    └────────┬─────────┘
                                                     yes     │    no
                                               ┌─────────────┘    └──────────────┐
                                               v                                  v
                                          ┌─────────┐                   ┌───────────────┐
                                          │  GIFT   │                   │ pctBracket =  │
                                          └─────────┘                   │ close/blend?  │
                                                                        └───────┬───────┘
                                                                     yes  │       no
                                                               ┌──────────┘       └──────────┐
                                                               v                              v
                                                          ┌─────────┐              ┌──────────────────┐
                                                          │  BLEND  │              │ recipient =      │
                                                          └─────────┘              │ loser_parent?    │
                                                                                   └────────┬─────────┘
                                                                                    yes     │    no
                                                                              ┌─────────────┘    └──────┐
                                                                              v                          v
                                                                         ┌─────────┐          ┌──────────────┐
                                                                         │  BLEND  │          │ winner_parent│
                                                                         └─────────┘          │ + photo?     │
                                                                                              └──────┬───────┘
                                                                                           yes │      no
                                                                                    ┌──────────┘      └────┐
                                                                                    v                      v
                                                                              ┌─────────────┐        ┌─────────┐
                                                                              │ CELEBRATION │        │  HERO   │
                                                                              └─────────────┘        └─────────┘
```

---

**End of specification.**
