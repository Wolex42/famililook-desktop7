# Task Briefing: NV-03 — Chunk Reload Loop Guard Fix
**Agent:** FE Lead Delta
**Track:** Parallel D
**Date:** 2026-04-07
**Risk Tier:** P2 — Standard (infinite loop on private browsers)
**Audit Reference:** NV-03 (HIGH)

---

## Mission

Fix a confirmed infinite reload loop in ErrorBoundary. When a chunk load error occurs (e.g. after a deploy invalidates cached JS chunks), ErrorBoundary attempts to reload the page once using sessionStorage to track whether it has already reloaded. On private/incognito browsers where sessionStorage is unavailable, writing to sessionStorage throws, the reload counter is never set, and the page reloads forever. Users on private browsers are completely locked out.

---

## Working Set (ONLY this file may be edited)

```
famililook-desktop2/src/components/ui/ErrorBoundary.jsx
```

No other files. If you discover the fix requires touching any other file, STOP and escalate.

---

## What You Must Read First (before writing any code)

1. `src/components/ui/ErrorBoundary.jsx` — read the ENTIRE file. Understand:
   - How chunk errors are detected (what string pattern is matched)
   - How sessionStorage is used to track the reload attempt
   - What the current reload logic does at lines 30-35
   - What the "Refresh Page" and "Try Again" buttons do
2. Check `.claude/change_log.md` — has ErrorBoundary.jsx been patched 2+ times? If yes → Two-Attempt Halt.

---

## Root Cause (from audit)

`ErrorBoundary.jsx:30-35`: The reload-once logic writes a flag to sessionStorage before reloading. On private browsers, `sessionStorage.setItem()` throws `SecurityError`. The catch does not handle this, so the flag is never written, the reload fires, the same error occurs, the same reload fires — infinite loop.

---

## What the Fix Must Do

Wrap all sessionStorage access in availability checks. The pattern:

```javascript
// Safe sessionStorage wrapper — call this instead of sessionStorage directly
function safeSessionGet(key) {
  try {
    return sessionStorage.getItem(key);
  } catch {
    return null; // private browser or storage unavailable
  }
}

function safeSessionSet(key, value) {
  try {
    sessionStorage.setItem(key, value);
    return true;
  } catch {
    return false; // private browser — cannot persist flag
  }
}
```

The reload-once logic must then handle the case where `safeSessionSet` returns false (private browser — cannot track):

```javascript
function attemptChunkReload() {
  const alreadyReloaded = safeSessionGet('chunk_reload_attempted');
  if (alreadyReloaded) {
    // Already tried — do not reload again. Show the error UI.
    return false;
  }
  
  const flagSet = safeSessionSet('chunk_reload_attempted', '1');
  if (!flagSet) {
    // Private browser — sessionStorage unavailable.
    // Reload once anyway (best effort), but we cannot prevent a second reload.
    // Accept this limitation — better than guaranteed infinite loop.
    // Show a note in the error UI if this is a concern.
    window.location.reload();
    return true;
  }
  
  window.location.reload();
  return true;
}
```

Additionally, per the lessons learnt (Lesson 8), verify:
- **"Refresh Page" is the PRIMARY button** (first, prominent)
- **"Try Again" is secondary** (for non-chunk errors where React state reset makes sense)
- The error message shown to users is **"Something went wrong. This usually resolves with a page refresh."** — NOT raw error strings like `useCallback is not defined`

The audit showed the ErrorBoundary already has error display (added in a previous fix). Verify the raw error message is NOT shown to end users in production. If `process.env.NODE_ENV !== 'production'` gate exists, keep it. If it's showing raw errors in production, add the gate.

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Run: `python .claude/validate_scope.py "src/components/ui/ErrorBoundary.jsx" --mode edit`
- [ ] Returns exit 0
- [ ] Check change_log: has this file been patched 2+ times? If yes → Two-Attempt Halt

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] ErrorBoundary is a class component — no hook import check needed (class components don't use hooks)
- [ ] Verify "Refresh Page" is primary CTA and "Try Again" is secondary
- [ ] Verify raw error strings not shown in production
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS

---

## Tests to Write

Add or update test in:
`src/components/ui/__tests__/ErrorBoundary.test.jsx`

Test cases:
1. **sessionStorage available**: chunk error → sessionStorage flag set → page reload attempted once (mock `window.location.reload`)
2. **sessionStorage unavailable (private browser)**: `sessionStorage.setItem` throws → reload attempted once, does not loop (verify reload called exactly once)
3. **Already reloaded flag set**: `safeSessionGet` returns `'1'` → reload NOT attempted → error UI shown
4. **Non-chunk error**: regular JS error → no reload → error UI shown with Refresh Page as primary CTA
5. **Raw error not exposed**: error message in UI does not contain raw JS error strings in production mode

---

## Definition of Done

- [ ] sessionStorage access wrapped in try-catch (safeSessionGet / safeSessionSet)
- [ ] Private browser case handled — reload fires once, does not loop
- [ ] "Already reloaded" flag correctly gates second reload
- [ ] "Refresh Page" is primary CTA, "Try Again" is secondary
- [ ] Raw error strings not shown in production
- [ ] Tests written for all 5 cases
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added to `.claude/change_log.md`

---

## Handoff to QA Lead (after done)

```
HANDOFF: FE Lead Delta → QA Lead
Task: NV-03 Chunk Reload Loop Guard
Files changed:
  - src/components/ui/ErrorBoundary.jsx (sessionStorage safety + CTA order)
Test evidence: <paste npm run test:run output>
Build: PASS
Open items: Private browser behaviour cannot be fully tested without a real browser in private mode — CEO should verify on device
```

---

## Constraints

- Do NOT edit any file outside the working set
- Do NOT convert ErrorBoundary from class component to functional — this is intentional (ErrorBoundary requires class component in React)
- Do NOT add new npm dependencies
- Do NOT modify backend files
- The solution must handle both the sessionStorage-available and sessionStorage-unavailable cases
- Do NOT remove the "Try Again" button — just make "Refresh Page" the primary action
