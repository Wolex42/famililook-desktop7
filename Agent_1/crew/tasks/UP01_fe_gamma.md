# Task Briefing: UP-01 — FacePicker Silent Crop Failure Fix
**Agent:** FE Lead Gamma
**Track:** Parallel C
**Date:** 2026-04-07
**Risk Tier:** P2 — Standard (silent UX failure, no crash)
**Audit Reference:** UP-01 (CRITICAL)

---

## Mission

Fix a confirmed silent failure in FacePicker. When a user selects a face from a multi-face photo and the crop operation fails, the modal silently closes with no explanation. The user sees the modal disappear and has no idea why — no error, no retry option. This is classified as CRITICAL because it breaks a core user flow with zero feedback.

This fix is also the first real-world use case for `AppErrorBus` — however, since AppErrorBus is not yet built, this fix must use the existing toast/notification system. When AppErrorBus is built, this catch block will be migrated. For now: surface the error using whatever toast mechanism already exists in the codebase.

---

## Working Set (ONLY this file may be edited)

```
famililook-desktop2/src/components/FacePicker.jsx
```

No other files. If you discover the fix requires touching any other file, STOP and escalate to the orchestrator.

---

## What You Must Read First (before writing any code)

1. `src/components/FacePicker.jsx` — read the ENTIRE file. Understand the full component: how it opens, how crop is triggered, what the catch block at lines 83-84 currently does, what `onClose` does.
2. Find the existing toast/notification system. Search: `grep -r "toast\|showToast\|addToast\|notify\|useToast" src/ --include="*.jsx" --include="*.js" -l`. Read whichever file defines the toast API — understand how to call it.
3. Check `.claude/change_log.md` — has FacePicker.jsx been patched 2+ times? If yes → Two-Attempt Halt.

**Do not invent a new toast system. Use whatever is already there.**

---

## Root Cause (from audit)

`FacePicker.jsx:83-84`:
```javascript
} catch {
  onClose(); // modal closes, no message, user confused
}
```

The crop operation can fail for several reasons (canvas error, invalid image bounds, memory pressure). The current catch swallows all of them.

---

## What the Fix Must Do

Replace the silent catch with a user-visible error message AND keep the modal open so the user can retry:

```javascript
} catch (err) {
  // Surface error using existing toast system
  showToast({
    message: "Couldn't crop that face — please try selecting it again.",
    type: "error"
  });
  // Do NOT call onClose() — keep modal open so user can retry
  // Log for debugging (not console.error in prod, use whatever logging exists)
  console.warn("[FacePicker] crop failed:", err?.message);
}
```

The exact toast call will depend on what the existing toast system exposes — adapt the call to match the existing API exactly. Do not invent a new API.

**Key UX requirement:** The modal must stay open after a crop failure. The user must be able to try again. `onClose()` must NOT be called in the catch block.

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Run: `python .claude/validate_scope.py "src/components/FacePicker.jsx" --mode edit`
- [ ] Returns exit 0
- [ ] Check change_log: has this file been patched 2+ times? If yes → Two-Attempt Halt
- [ ] Identified the existing toast system (grep result + read the API)

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification: `grep -E "use[A-Z][a-zA-Z]+" src/components/FacePicker.jsx | grep -v "^import"`
- [ ] Verify toast hook/function is imported if it's a hook
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS

---

## Tests to Write

Add or update test in:
`src/components/__tests__/FacePicker.test.jsx`

Test cases:
1. **Happy path**: crop succeeds → `onClose` called with cropped file, no toast shown
2. **Crop failure**: crop throws → toast error shown, `onClose` NOT called, modal stays open
3. **Retry after failure**: crop fails then user tries again successfully → works correctly

---

## Definition of Done

- [ ] Silent catch replaced with toast error message
- [ ] Modal stays open on crop failure (user can retry)
- [ ] `onClose()` not called in catch block
- [ ] Existing toast system used (no new system invented)
- [ ] Toast import added if needed (verified in hook import check)
- [ ] Tests written for all 3 cases
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added to `.claude/change_log.md`
- [ ] Note in change log: "AppErrorBus migration pending — this catch block is a candidate for migration when AppErrorBus is built"

---

## Handoff to QA Lead (after done)

```
HANDOFF: FE Lead Gamma → QA Lead
Task: UP-01 FacePicker Silent Crop Failure
Files changed:
  - src/components/FacePicker.jsx (catch replaced with toast + modal stays open)
Toast system used: <name of toast function/hook found in codebase>
Test evidence: <paste npm run test:run output>
Build: PASS
AppErrorBus note: This catch is a migration candidate when AppErrorBus is built
Open items: None
```

---

## Constraints

- Do NOT edit any file outside the working set
- Do NOT invent a new toast or notification system — use what exists
- Do NOT call onClose() in the catch block
- Do NOT add new npm dependencies
- Do NOT modify backend files
- If no toast system exists at all in the codebase, STOP and report to orchestrator — do not invent one
