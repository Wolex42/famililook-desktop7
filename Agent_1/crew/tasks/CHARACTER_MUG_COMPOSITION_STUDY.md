# Task: Character Mug Composition Study
## Date: 30 March 2026 | Priority: P1 | Status: OPEN
## Assigned: Visual Director, Copywriter, FE Lead (collaborative)

---

## Problem Statement

The Character Mug template currently has two extremes:
1. **Old version (3-panel)**: 18 UI elements crammed onto one mug. Overcrowded, no clear message.
2. **New version (Hero Layout)**: 5 elements, bold and clean — but stripped so far back that the child's identity and the family story are lost. A headline saying "MUMMY'S MINI ME" with no child name, no photo context, and no family celebration feels like a generic product, not a personal keepsake.

**The real product is the celebration of the bond between parent and child.** The mug must tell THAT story — not just display data, not just show a cartoon. It needs to feel like: "This is Olivia. She looks like her Mum. Here's the proof. And we're celebrating it."

## What the CEO Said

> "We are celebrating the bond between parents and child. For that analysis one parent won — we celebrate. Or we may want a different message entirely from the analysis. This is where intelligence needs to play a part in making the outcome wholesome. It needs to be modular — pick the items that create the wholesome final picture for the results."

## Design Challenge

Create a **modular composition system** where an intelligence layer selects the right combination of elements for each unique result, producing a mug that is:

- **Personal** — the child's name and photo (if available) are present
- **Celebratory** — the tone is warm, proud, fun — not clinical
- **Clear within 3 seconds** — instant understanding of what this is and who it's for
- **Not overcrowded** — breathing room, less is more
- **Gift-worthy** — someone would photograph this mug and post it
- **Wholesome** — celebrates the family bond, not just "who won"

## Required Outputs

### 1. Visual Director: Element Library + Composition Rules

Define the **complete library of modular elements** that CAN appear on a mug, with sizing, positioning, and visual weight rules:

| Element | Description | When to include | Visual weight |
|---------|-------------|-----------------|---------------|
| Character illustration | Mama/Papa/Cub/Mini/Gran/Gramps | Always | High |
| Hero headline | Bold text: "MUMMY'S MINI ME" | Always | Highest |
| Child's name | "OLIVIA" or "For Olivia" | When childName exists | Medium |
| Child's photo | Circular crop of uploaded photo | When childPhoto exists | High |
| Score line | "72% Mum" | Always (it's the core data) | Medium |
| Feature callout | "Got Mum's Eyes" | When it adds to the story | Low-Medium |
| Speech bubble | "TOLD YOU SO!" | When tone is playful | Low |
| Occasion tag | "Happy Mother's Day" | When occasion is set | Medium |
| Second character | The "losing" parent reacting | When it adds humour | Medium |
| Brand mark | "famililook.com" | Always (tiny) | Lowest |

Rules needed:
- **Maximum elements on any mug**: what's the cap? 6? 7?
- **Minimum elements**: what MUST always be present?
- **Spacing/breathing room rules**: minimum gap between elements
- **Visual hierarchy**: which element dominates in each scenario?
- **Layout variants**: how does the composition change when photo is present vs absent? When occasion is set vs generic? When score is high vs close call?

### 2. Copywriter: Message Strategy by Scenario

Define the **tone and message strategy** for different result scenarios. The mug isn't always about "who won" — sometimes it's about the blend, the surprise, the family bond.

Scenarios to address:

| Scenario | Example | Tone | Message approach |
|----------|---------|------|-----------------|
| Decisive win (70%+) | "78% Mum" | Triumphant, funny | Celebrate the winner. Playful rivalry. "SORRY DAD" energy. |
| Moderate win (60-69%) | "64% Dad" | Warm, proud | Acknowledge the winner warmly. "Dad's influence is strong." |
| Close call (51-59%) | "53% Mum" | Celebratory blend | Don't emphasise winning. "Best of both." "The perfect blend." |
| Gift for winner parent | Mum wins, mug is for Mum | Proud, personal | "YOUR mini me" — direct address to the recipient |
| Gift for losing parent | Dad lost, mug is for Dad | Affectionate, inclusive | "They may look like Mum, but they've got your [feature]" |
| Gift for grandparent | Any result, mug for Gran | Warm, showing off | "Your grandchild — officially adorable" |
| Mother's Day | Any result | Maternal celebration | The bond, not the score |
| Father's Day | Any result | Paternal celebration | The bond, not the score |
| Birthday | Child's birthday | Child-focused celebration | "Look how you've grown" / age milestone |
| Close call — blend message | 51-52% | Unity, togetherness | "The best of Mum AND Dad" — no winner framing at all |

For each scenario, provide:
- Primary headline pool (5-10 options)
- Whether to show score prominently, subtly, or not at all
- Whether to name both parents or just the winner
- Whether speech bubble should be winner's voice, child's voice, or narrator
- Whether photo should be prominent, subtle, or absent

### 3. FE Lead: Modular Composition Engine Spec

Design the **composition engine** — the intelligence layer that takes the analysis data + context and outputs a composition plan:

```
INPUT:
  - data: { winner, winnerPct, winnerLabel, loserLabel, childName, childPhoto, featureVotes, dominantFeature }
  - occasion: "generic" | "mothers_day" | "fathers_day" | "birthday" | "christmas" | "valentines" | "grandparents_day"
  - recipient: "winner_parent" | "loser_parent" | "grandparent" | "self" | "unknown" (NEW — who is this mug FOR?)
  - variant: "default" | "african"

OUTPUT (composition plan):
  - layout: "hero" | "celebration" | "blend" | "gift" (which layout template to use)
  - character: { type, emotion }
  - headline: { text, size: "large" | "medium" }
  - childName: { show: boolean, format: "standalone" | "in_headline" | "in_score" }
  - photo: { show: boolean, size: "large" | "small" | "hidden" }
  - score: { show: boolean, format: "prominent" | "subtle" | "hidden" }
  - featureCallout: { show: boolean, text: string }
  - speechBubble: { show: boolean, text: string, voice: "winner" | "child" | "narrator" }
  - occasion: { show: boolean, text: string }
  - secondCharacter: { show: boolean, type: string, emotion: string }
  - brand: { show: true } // always
```

The engine should have clear rules for each scenario — not random, but deterministic given the inputs. Same inputs → same composition every time.

### 4. All Agents: Layout Variants (Visual Mockups as Code Descriptions)

Define **3-4 layout templates** that the composition engine can choose from:

**Layout A: "Hero" (current)** — character left, bold headline right. For decisive wins, playful tone.

**Layout B: "Celebration"** — character left, child name + photo centre, headline below. For gifts, personal tone.

**Layout C: "Blend"** — two characters (Mama + Papa) flanking a central headline. For close calls, unity tone.

**Layout D: "Gift"** — occasion header top, character + child name centre, personal message below. For seasonal gifts.

Each layout should specify exact panel structure, element positions, and when the composition engine should select it.

## Constraints

- All layouts must fit 830x345px CSS (2670x1110px print)
- Transparent background (prints on white ceramic)
- Maximum 7 elements per layout (hard cap)
- Font sizes must be readable at arm's length on a physical mug
- Must work with both Caucasian and African character variants
- Must degrade gracefully: if childPhoto is missing, layout adjusts; if childName is missing, layout adjusts
- The composition engine must be deterministic — same inputs always produce same output

## Deliverables

1. **Visual Director**: `COMPOSITION_RULES.md` — element library, sizing rules, layout variant specs, spacing rules, visual hierarchy per scenario
2. **Copywriter**: `MESSAGE_STRATEGY.md` — headline pools per scenario, tone guidance, score visibility rules, speech bubble voice rules
3. **FE Lead**: `COMPOSITION_ENGINE_SPEC.md` — TypeScript-style interface for composition plan, selection algorithm, layout template specs with dimensions

## Timeline
- Study + deliverables: next session
- Implementation: after CEO reviews and approves the composition system
- NO code changes until the study is complete and approved
