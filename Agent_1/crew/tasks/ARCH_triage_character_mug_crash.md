# Platform Architect Triage — Character Mug Crash (React #426)
**Agent:** Platform Architect
**Date:** 2026-04-07
**Triggered by:** CEO bug report — React error #426 on character mug preview
**Runs:** BEFORE any FE Lead is activated

---

## Why This Goes Through Platform Architect First

`CharacterMugTemplate.jsx` and `compositionEngine.js` have both been touched in CR-0007 (keepsake fixes batch, 2026-04-01). This is their second edit within 30 days. A third edit on either file requires Platform Architect review before FE Lead proceeds — this is the Two-Attempt Halt rule applied proactively.

Additionally, `compositionEngine.js` is a composition engine — it sits between data and rendering. Errors in it propagate to every product that uses it, not just character mugs. Any change to it requires explicit scope assessment.

---

## Your Mission

Read the full data flow for the character mug and confirm:
1. Exactly where `characterOverride` is dropped (the investigation says between KeepsakeMobileFlow state and composeCharacterMug() call)
2. Whether the fix is truly contained to `CharacterMugTemplate.jsx` or requires touching `compositionEngine.js` as well
3. Whether `compositionEngine.js` at its current patch count can absorb another targeted fix, or whether it needs a redesign first
4. What the exact minimal fix looks like — and whether it is safe

---

## What You Must Read (in this order)

1. `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` — where is `characterOverride` stored in state? Where is it passed as a prop?
2. `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` — does it receive `characterOverride` as a prop? Does it pass it to `composeCharacterMug()`?
3. `src/components/keepsakes/utils/compositionEngine.js` — what does `composeCharacterMug()` expect? What happens when `characterType` and `characterEmotion` are missing/undefined? What does it return in that case?
4. `.claude/change_log.md` — how many times has each of these files been patched?

---

## The Known Data Flow (from investigation)

```
CharacterPicker (user selects character + emotion)
    ↓ stored as characterOverride in KeepsakeMobileFlow state
KeepsakeCustomise (receives/displays selection)
    ↓ passed back via onContinue callback
KeepsakeMobileFlow (holds state)
    ↓ ??? — characterOverride allegedly dropped here
CharacterMugTemplate.jsx
    ↓ calls composeCharacterMug({ data, occasion, recipient, variant })
                                  ↑ characterType and characterEmotion MISSING
compositionEngine.js — composeCharacterMug()
    ↓ builds plan with defaults
    ↓ layout function returns plain object somewhere
React crashes: "Objects are not valid as a React child" (#426)
```

Your job is to verify every arrow in this chain by reading the actual code, and identify the exact line where the prop is dropped.

---

## Assessment Output Format

```
PLATFORM ARCHITECT ASSESSMENT — Character Mug Crash (#426)
Date: 2026-04-07

DATA FLOW VERIFIED:
  characterOverride stored in: <file:line>
  characterOverride last seen: <file:line>
  characterOverride dropped at: <file:line — the gap>
  composeCharacterMug() call at: <file:line>
  Missing props confirmed: characterType [YES/NO] characterEmotion [YES/NO]

COMPOSITION ENGINE ASSESSMENT:
  What compositionEngine returns when characterType is undefined: <describe>
  Where the plain object is returned (causing #426): <file:line>
  Is this a targeted fix or does the engine need defensive defaults? <assess>

PATCH COUNT CHECK:
  CharacterMugTemplate.jsx patches in 30 days: <N>
  compositionEngine.js patches in 30 days: <N>
  KeepsakeMobileFlow.jsx patches in 30 days: <N>

SCOPE DECISION:
  Files that MUST change to fix the crash: <list>
  Files that SHOULD change (defensive) but aren't required: <list>
  Files that MUST NOT change in this task: <list>

IS compositionEngine.js SAFE TO PATCH AGAIN?
  Current patch count: <N>
  Assessment: SAFE FOR TARGETED FIX | APPROACHING LIMIT — PATCH ONLY IF REQUIRED | HALT — ROUTE TO REDESIGN

MINIMAL CORRECT FIX:
  Step 1: <file:line — exact change>
  Step 2: <file:line — exact change, if needed>
  Does this fix also prevent future crashes when other props are missing? <yes/no>

SECONDARY BUG IN compositionEngine:
  What returns a plain object instead of a renderable value? <exact location>
  Is fixing the prop-threading sufficient to prevent this, or does the engine
  also need a guard? <assess>

RECOMMENDATION: 
  APPROVE — thread characterOverride prop, engine fix not required
  APPROVE WITH DEFENSIVE GUARD — thread prop AND add engine null guard
  HALT compositionEngine — route that file to /crew redesign, thread prop only
```

---

## Gate: CEO Approval Required

After assessment, present to CEO:

```
GATE: character_mug_crash_scope
PLATFORM ARCHITECT RECOMMENDATION: <from above>
FILES: <approved working set for FE Lead>
PATCH COUNT RISK: <any files approaching limit>
compositionEngine.js STATUS: SAFE | CAUTION | HALT

OPTIONS:
  A. Thread characterOverride only (KeepsakeMobileFlow + CharacterMugTemplate)
  B. Thread + add engine null guard (adds compositionEngine.js to working set)
  C. Thread + route compositionEngine to /crew redesign (parallel track)

DECISION NEEDED: A | B | C
```
