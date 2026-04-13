# Task Briefing: ST-01 — Analysis Abort Race Condition Fix
**Agent:** Platform Architect → (gate) → FE Lead Epsilon
**Track:** Sequential (protected file)
**Date:** 2026-04-07
**Risk Tier:** P1 — Significant (protected file: useKinshipAnalysis.jsx)
**Audit Reference:** ST-01 (CRITICAL)

---

## Overview

This task runs sequentially because `useKinshipAnalysis.jsx` is a protected file requiring Platform Architect review before any code is written.

**Step 1:** Platform Architect reads the file, assesses the fix scope, and confirms it is a targeted single-line guard (not an architectural change requiring redesign).
**Step 2:** CEO gate — Platform Architect presents findings and recommendation.
**Step 3 (if approved):** FE Lead Epsilon implements exactly to Platform Architect's spec.

---

# STEP 1: Platform Architect Assessment

## Platform Architect Mission

Read `useKinshipAnalysis.jsx` in full. Assess:
1. Is `ST-01` (no `signal.aborted` check before setState) a targeted fix or does it expose a deeper pattern?
2. How many other places in this file set state after an async operation without checking signal.aborted?
3. Does the fix require touching FamililookContext.jsx or MobileResultsSection.jsx? (If yes — additional protected file reviews needed)
4. What is the exact line and what does the minimal correct fix look like?
5. Is this file a candidate for `resultsContract.js` migration? (Do not do that migration now — just flag it)

## What Platform Architect Must Read

1. `src/hooks/useKinshipAnalysis.jsx` (or `.js`) — read the ENTIRE file
2. Focus on: how AbortController is created, how the signal is passed to fetch, what happens at line 414 where state is set after the response arrives
3. Map ALL places in the file where setState or similar state updates occur after awaiting an API call

## Platform Architect Output Format

```
PLATFORM ARCHITECT ASSESSMENT — ST-01
File: useKinshipAnalysis.jsx
Date: 2026-04-07

FINDING:
  Root cause confirmed: <yes/no — describe>
  Line(s) affected: <list>
  Pattern type: TARGETED FIX | SYSTEMIC (multiple instances)

SCOPE OF FIX:
  Minimal correct fix: <exact description>
  Additional instances of same pattern: <count and locations>
  Other files required: YES (<list>) | NO

ARCHITECTURAL NOTE:
  This file is a resultsContract.js migration candidate: YES | NO
  Migration complexity: <brief assessment — not for this task>
  Protected file bypass risk: <does this fix change any logic, or purely add a guard?>

SPEC FOR FE LEAD EPSILON:
  <exact description of what to implement — specific lines, exact pattern>
  
  Example guard pattern:
  // BEFORE (vulnerable)
  setAnalysisResults(data);
  
  // AFTER (safe)
  if (!signal.aborted) {
    setAnalysisResults(data);
  }

RECOMMENDATION: APPROVE FIX | SCOPE TOO LARGE — NEEDS REDESIGN | BLOCKED (reason)
```

---

# GATE: CEO Approval Required

Platform Architect presents assessment to CEO before FE Lead Epsilon is activated.

```
GATE: st01_protected_file_approval
FILE: useKinshipAnalysis.jsx (protected)
PLATFORM ARCHITECT RECOMMENDATION: <from assessment>
SCOPE: <targeted / systemic>
OTHER FILES NEEDED: <yes/no>
RISK: <assessment>

OPTIONS:
  A. Approve targeted fix (guard at line 414 only) — FE Lead Epsilon proceeds
  B. Approve systemic fix (all N instances) — FE Lead Epsilon proceeds with broader scope
  C. Hold — route to /crew redesign first

DECISION NEEDED FROM CEO: A | B | C
```

---

# STEP 3: FE Lead Epsilon Implementation

**(Activate only after CEO approves)**

## Working Set

```
famililook-desktop2/src/hooks/useKinshipAnalysis.jsx
```
*(or .js — confirm the exact filename)*

No other files unless CEO approved option B or C above.

## Mission

Implement exactly what Platform Architect specified. No interpretation. No additional changes.

The fix is a guard that checks `signal.aborted` before calling setState after an async operation resolves. This prevents a cancelled analysis from overwriting a new analysis that the user has already started.

## Root Cause (from audit)

`useKinshipAnalysis.jsx:414`: After the API call returns, the code calls setState unconditionally. If the user:
1. Clicks Analyze → API call starts (signal A)
2. Cancels → signal A is aborted
3. Clicks Analyze again → API call starts (signal B)
4. Signal A's response arrives late → setState fires → overwrites signal B's (correct, fresh) result

The fix: check `signal.aborted` before any setState call that follows an awaited API response.

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Platform Architect assessment received and CEO has approved
- [ ] Run: `python .claude/validate_scope.py "src/hooks/useKinshipAnalysis.jsx" --mode edit`
- [ ] Returns exit 0
- [ ] Check change_log: has this file been patched 2+ times? If yes → report to Platform Architect before proceeding

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification: `grep -E "use[A-Z][a-zA-Z]+" src/hooks/useKinshipAnalysis.jsx | grep -v "^import"`
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS

## Tests to Write

Add or update test in the useKinshipAnalysis test suite:

Test cases:
1. **Normal analysis**: single analyze call → results set correctly
2. **Abort then re-analyze**: analyze → abort → analyze again → only second result is stored (first is discarded)
3. **Concurrent requests**: two requests fire, first aborted, second completes → only second result stored

## Definition of Done

- [ ] Platform Architect spec implemented exactly (no interpretation)
- [ ] signal.aborted check in place at line 414 (and any additional lines approved by CEO)
- [ ] Tests written for abort race scenario
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added to `.claude/change_log.md`
- [ ] Platform Architect notified of completion (for architectural records)

## Handoff to QA Lead (after done)

```
HANDOFF: FE Lead Epsilon → QA Lead
Task: ST-01 Analysis Abort Race Condition
Files changed:
  - src/hooks/useKinshipAnalysis.jsx (signal.aborted guard added)
Platform Architect spec followed: YES
Instances fixed: <N> (as per CEO-approved scope)
Test evidence: <paste npm run test:run output>
Build: PASS
Open items: resultsContract.js migration flagged by Platform Architect — not done in this task
```

---

## Constraints

- Do NOT implement anything beyond what Platform Architect specified and CEO approved
- Do NOT change any result derivation logic (winner, percentages, feature votes) — this fix is purely a guard
- Do NOT edit FamililookContext.jsx or MobileResultsSection.jsx in this task
- Do NOT add new npm dependencies
- Do NOT modify backend files
