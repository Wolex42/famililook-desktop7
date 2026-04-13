# Task Briefing: KS-02 — Order Success Race Condition Fix
**Agent:** FE Lead Beta
**Track:** Parallel B
**Date:** 2026-04-07
**Risk Tier:** P1 — Significant (payment succeeded, user sees error)
**Audit Reference:** KS-02 (CRITICAL)

---

## Mission

Fix a confirmed race condition on the order success page. Stripe redirects the user back to the app with an `order_id` immediately after payment. However, the Prodigi webhook that actually creates the order record on the backend may not have processed yet. The current code calls `getOrderStatus()` once — if it returns 404 (order not yet in the system), the user sees "Something went wrong" despite their payment having succeeded. This is a trust-destroying UX failure.

---

## Working Set (ONLY this file may be edited)

```
famililook-desktop2/src/pages/OrderSuccessPage.jsx
```

No other files. If you discover the fix requires touching any other file, STOP and escalate to the orchestrator.

---

## What You Must Read First (before writing any code)

1. `src/pages/OrderSuccessPage.jsx` — read the ENTIRE file. Map the full flow: how `order_id` is extracted from the URL, how `getOrderStatus()` is called, what happens on 404 vs success vs other errors.
2. Check: what does `getOrderStatus()` return? Where is it defined? Read that file too (read-only — do not edit it).
3. Check `.claude/change_log.md` — has OrderSuccessPage.jsx been patched before? If 2+ times, issue Two-Attempt Halt.

---

## Root Cause (from audit)

`OrderSuccessPage.jsx:52-68`: `getOrderStatus()` is called once after Stripe redirect. If the Prodigi webhook hasn't processed yet (common — webhooks are async), the backend returns 404. The current code treats 404 as a failure and shows "Something went wrong." The user's payment has succeeded; only the order record is delayed.

---

## What the Fix Must Do

Replace the single `getOrderStatus()` call with a **retry loop with exponential backoff**:

```javascript
// Retry configuration
const MAX_ATTEMPTS = 5;
const BASE_DELAY_MS = 1500; // 1.5s, 3s, 6s, 12s, 24s

async function pollOrderStatus(orderId, signal) {
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    try {
      const status = await getOrderStatus(orderId, { signal });
      if (status && status.ok) return status;
      
      // 404 specifically = webhook not yet processed, retry
      if (status?.status === 404 && attempt < MAX_ATTEMPTS - 1) {
        await delay(BASE_DELAY_MS * Math.pow(2, attempt));
        continue;
      }
      
      // Other errors = genuine failure, don't retry
      return null;
    } catch (err) {
      if (err.name === 'AbortError') return null;
      if (attempt === MAX_ATTEMPTS - 1) return null;
      await delay(BASE_DELAY_MS * Math.pow(2, attempt));
    }
  }
  return null;
}
```

While polling is in progress, show a **reassuring loading state** — not a spinner alone:

```
✓ Payment received
  Setting up your order... (this takes a few seconds)
  [progress indicator]
```

If all retries fail (genuine backend problem after 5 attempts + ~45s total wait):
- Show a **specific message**: "Your payment was successful. Your order is being processed — you'll receive a confirmation email shortly."
- Do NOT show generic "Something went wrong"
- Do NOT imply the payment failed

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Run: `python .claude/validate_scope.py "src/pages/OrderSuccessPage.jsx" --mode edit`
- [ ] Returns exit 0
- [ ] Check change_log: has this file been patched 2+ times? If yes → Two-Attempt Halt

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification: `grep -E "use[A-Z][a-zA-Z]+" src/pages/OrderSuccessPage.jsx | grep -v "^import"`
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS

---

## Tests to Write

Add or update test in:
`src/pages/__tests__/OrderSuccessPage.test.jsx`

Test cases:
1. **Happy path — immediate success**: `getOrderStatus` returns success on first call → success page renders
2. **Webhook delay — success after retry**: `getOrderStatus` returns 404 twice, then success → success page renders (no error shown during retry)
3. **Genuine failure**: `getOrderStatus` returns 404 all 5 attempts → reassuring message shown (not generic error, payment confirmed)
4. **Component unmount during poll**: poll starts, component unmounts → no state update after unmount (no React warning)

---

## Definition of Done

- [ ] Retry loop implemented with exponential backoff (5 attempts, 1.5s base)
- [ ] Reassuring loading state shown during polling
- [ ] Failure state shows payment-confirmed message, not generic error
- [ ] Abort on unmount (no state update after unmount)
- [ ] Tests written for all 4 cases above
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added to `.claude/change_log.md`

---

## Handoff to QA Lead (after done)

```
HANDOFF: FE Lead Beta → QA Lead
Task: KS-02 Order Success Race Condition
Files changed:
  - src/pages/OrderSuccessPage.jsx (retry loop + reassuring UX)
Test evidence: <paste npm run test:run output>
Build: PASS
Open items: None — this is not a mobile UI fix, no device verification needed
```

---

## Constraints

- Do NOT edit any file outside the working set
- Do NOT modify `getOrderStatus()` itself — only how OrderSuccessPage.jsx calls it
- Do NOT add new npm dependencies
- Do NOT modify backend files
- Do NOT show "Something went wrong" as the final state when payment succeeded
- Payment must never be implied to have failed when it succeeded
