# Spec: Error Resilience — Never Lose a User to a Fixable Error

> **Author**: CEO + CPO
> **Date**: 2026-04-04
> **Priority**: P0 — Every error at 7 users/day is a permanent loss
> **Status**: SPEC_READY

---

## 1. Principle

**The user should never see an error that the system could have recovered from silently.** If the first attempt fails, try again before showing anything. If retry fails, show a helpful message with a clear action. Never show a dead end.

---

## 2. Current State

- 89 error paths in the codebase
- 62 (70%) block user progress with no auto-recovery
- Only 7 have retry or fallback logic
- Revenue path (checkout) has ZERO retry — a single 422 loses the sale
- Face detection has ZERO retry — one bad response and the photo is "rejected"

---

## 3. The Resilience Layers

### Layer 1: Silent Auto-Retry (user never knows)

For transient errors (network glitch, server busy, timeout), retry automatically before showing any error:

| Endpoint | Retries | Backoff | Already Has? |
|----------|---------|---------|-------------|
| `/detect` | 2 | 1s, 2s | NO |
| `/kinship/analyze` | 3 | 1s, 2s, 4s | YES (kinshipClient.js) |
| `/kinship/group-snapshot` | 2 | 1s, 2s | NO |
| `/payments/create-basket-checkout` | 2 | 1s, 2s | NO |
| `/payments/create-checkout` | 2 | 1s, 2s | NO |
| `/analytics/track` | 1 | 1s | NO (fail silently is fine) |
| PNG export (html-to-image) | 1 | 0s (fallback to html2canvas) | YES (just added) |

Implementation: wrap `fetch` calls in a generic `fetchWithRetry()` utility:
```javascript
async function fetchWithRetry(url, options, { retries = 2, backoff = 1000 } = {}) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, options);
      if (res.ok || res.status < 500) return res; // Client errors don't retry
      if (attempt < retries) await sleep(backoff * Math.pow(2, attempt));
    } catch (err) {
      if (attempt === retries) throw err;
      await sleep(backoff * Math.pow(2, attempt));
    }
  }
}
```

### Layer 2: Smart Fallback (user sees degraded but functional experience)

| Failure | Fallback |
|---------|----------|
| Face detection returns 0 faces | Re-try with original (uncompressed) photo |
| PNG export fails (both libraries) | Offer "Download preview" as low-res screenshot |
| Personalised message API fails | Skip message, proceed without it |
| Currency rates API fails | Use GBP as default (already happens) |
| Ambassador status check fails | Continue as free tier (already happens) |
| Thumbnail crop fails | Show numbered placeholder instead |

### Layer 3: Graceful Error with Clear Action (user sees, but isn't stuck)

Every error that reaches the user MUST include:
1. **What happened** (in plain English, not technical)
2. **What to do** (specific, actionable)
3. **A retry button** (not just "OK" or close)

**Bad:** "Checkout failed (422)" → dead end
**Good:** "Payment couldn't process — we've saved your basket. [Try again] [Contact support]"

**Bad:** "Export failed" → user closes modal, loses work
**Good:** "Couldn't create the print image. [Try again] [Download preview instead]"

### Layer 4: Error Beacon (every failure tracked)

Every error that reaches Layer 3 (user-visible) fires an analytics event:

```javascript
analytics.trackError('checkout_failed', message, {
  endpoint, statusCode, productType, basketSize, userPlan, attempt
});
```

The dashboard `/analytics/summary` includes error breakdown so you can see:
- Which errors are most frequent
- Which errors are on the revenue path
- Which errors increased after a deploy

---

## 4. Priority Implementation (ordered by revenue impact)

### P0: Checkout auto-retry + basket preservation
**Files:** `src/api/orderApi.js`, `src/components/keepsakes/BasketDrawer.jsx`
- Wrap checkout calls in `fetchWithRetry(url, opts, { retries: 2 })`
- If final retry fails: show "Payment couldn't process. Your basket is saved — try again in a moment."
- Basket already persists in localStorage — just don't clear it on error

### P0: Face detection auto-retry
**Files:** `src/layout/UploadSection.jsx` (detectPhoto function)
- On first failure (0 faces or !res.ok): retry once with 1s delay
- On second failure with 0 faces: retry once with original uncompressed photo (skip compressPhoto)
- Only show "No face found" after 3 attempts with 2 different photo versions

### P1: Analysis auto-retry (already exists, verify)
**File:** `src/api/kinshipClient.js`
- Already has 3 retries with exponential backoff — confirm it's working
- Add: if ALL retries fail, preserve photos in state (don't clear uploads)

### P1: Generic fetchWithRetry utility
**File:** `src/utils/fetchWithRetry.js` (NEW)
- Reusable across all API calls
- Configurable retries, backoff, retry-on-status-codes
- Silent retries — no user notification until final failure

### P2: Error messages audit
- Replace all generic "Failed" / "Try again" messages with specific, actionable copy
- Every BLOCKS_PROGRESS error gets a [Retry] button
- No error shows a raw status code to the user

### P2: Error tracking beacon
- Add `analytics.trackError()` calls to every catch block that shows user-facing messages
- Dashboard summary includes error_count, error_rate, top_errors
- Growth Monitor flags error spikes

---

## 5. Files to Change

| File | Change | Priority |
|------|--------|----------|
| `src/utils/fetchWithRetry.js` | **NEW** — reusable retry wrapper | P1 |
| `src/api/orderApi.js` | Use fetchWithRetry for all checkout calls | P0 |
| `src/layout/UploadSection.jsx` | Auto-retry detectPhoto with fallback to uncompressed | P0 |
| `src/components/keepsakes/BasketDrawer.jsx` | Better error message + retry button | P0 |
| `src/components/keepsakes/KeepsakesModal.jsx` | Retry button on export errors | P1 |
| `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` | Same | P1 |
| `src/hooks/useKinshipAnalysis.jsx` | Preserve photos on failure | P1 |
| `src/utils/analytics.js` | trackError already exists — ensure it fires everywhere | P2 |

---

## 6. Acceptance Criteria

- [ ] Checkout 422 → auto-retries 2x → user only sees error after 3rd failure
- [ ] Checkout failure message includes retry button + "basket saved" reassurance
- [ ] Face detection 0 faces → retries with uncompressed photo → only shows "no face" after 3 attempts
- [ ] PNG export failure → html2canvas fallback (already done) → "download preview" option if both fail
- [ ] Every user-visible error tracked via analytics.trackError()
- [ ] No error shows raw HTTP status codes
- [ ] No error is a dead end — always has [Retry] or [alternative action]
- [ ] Photos never cleared from state on analysis failure (user can retry without re-uploading)

---

## 7. Agent Assignments

| Step | Agent | Task |
|------|-------|------|
| 1 | fe_lead | Create `fetchWithRetry.js` utility |
| 2 | fe_lead | Wire fetchWithRetry into orderApi.js checkout calls |
| 3 | fe_lead | Add auto-retry to detectPhoto in UploadSection.jsx |
| 4 | fe_lead | Add retry button + better message to BasketDrawer.jsx |
| 5 | fe_lead | Add retry button to KeepsakesModal + KeepsakeMobileFlow export errors |
| 6 | fe_lead | Preserve photos on analysis failure in useKinshipAnalysis.jsx |
| 7 | qa_lead | Tests: retry works, fallback works, error messages correct, photos preserved |
| 8 | fe_lead | Add trackError to every catch block showing user-facing errors |
