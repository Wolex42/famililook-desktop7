# QA Lead Assessment: Biometric Consent Modal Stuck Bug

**Date:** 2026-04-05
**Assessor:** QA Lead (Agent Persona)
**File under review:** `famililook-desktop2/src/layout/UploadSection.jsx`
**Verdict:** PASS (with one required addition for COPPA gate)

---

## 1. Root Cause Verification — CONFIRMED

The stale closure diagnosis is correct. Here is the exact execution trace:

1. User uploads photo -> `detectPhoto(file)` is called (line 512/559/914)
2. `consent.biometric` is `false` -> `detectPhoto` stores file in `pendingFileRef.current`, shows consent modal, returns early (lines 388-391)
3. User taps "Start My Analysis" -> `handleConsentAccept` fires (line 445)
4. `updateConsent({ biometric: true })` is called -> React schedules a state update via `setConsentState` in ConsentContext (line 34). localStorage is written synchronously.
5. `setTimeout(() => detectPhoto(file), 100)` is called (line 451)

**The problem:** `handleConsentAccept` has `detectPhoto` in its dependency array (line 453). But `detectPhoto` itself depends on `consent` (line 443). At the moment `handleConsentAccept` was created, it captured the `detectPhoto` that has `consent.biometric === false` in its closure. The `updateConsent` call triggers a re-render that will produce a NEW `detectPhoto` and a NEW `handleConsentAccept`, but the OLD `handleConsentAccept` (the one currently executing) still holds a reference to the OLD `detectPhoto`.

The 100ms `setTimeout` does NOT help because:
- React batches state updates and may not have re-rendered within 100ms
- Even if React re-renders, the already-queued `setTimeout` callback captures the old `detectPhoto` reference — it does not magically pick up the new one
- So `detectPhoto` runs with `consent.biometric === false`, hits line 388, and shows the modal again

Result: infinite loop of modal appearing -> user taps accept -> modal reappears.

## 2. Proposed Fix Evaluation — CORRECT AND SAFE

The proposed fix adds a `skipConsent` parameter:

```javascript
const detectPhoto = useCallback(async (file, { skipConsent = false } = {}) => {
  // ...
  if (!skipConsent && !consent.biometric) {
    setShowUploadConsent(true);
    return { level: "info", ... };
  }
```

**Safety analysis:**

- **Can a non-consented photo reach the server?** NO. The `skipConsent` parameter is only passed from `handleConsentAccept` (line 451) and the COPPA gate handler (line 635). Both are gated behind explicit user actions (tapping "Start My Analysis" or confirming age). By the time `skipConsent: true` is passed, `updateConsent({ biometric: true })` has already been called and localStorage has been written synchronously.
- **Server-side check:** `getBiometricHeaders()` (config.js line 31) reads `fl:consent` directly from localStorage, NOT from React state. Since `updateConsent` writes to localStorage synchronously via `saveConsent()` (ConsentContext.jsx line 23) BEFORE the setTimeout fires, the `X-Biometric-Consent: granted` header will be present on the `/detect` request. The server receives correct consent proof.
- **COPPA gate still runs first:** The `promptCoppaIfNeeded()` check (line 385) runs BEFORE the consent check, so COPPA is never bypassed.

**Verdict on skipConsent:** This is the right fix. It is explicit, minimal, and self-documenting.

## 3. Alternative Approaches Considered

### Alternative A: Use a `useRef` for consent

```javascript
const consentRef = useRef(consent);
useEffect(() => { consentRef.current = consent; }, [consent]);
```

Then check `consentRef.current.biometric` inside `detectPhoto`.

**Pros:** No extra parameter, always reads latest value.
**Cons:**
- Introduces a ref that shadows state — two sources of truth for consent
- Still has a race condition: the `useEffect` that updates the ref runs AFTER render, so the ref might not be updated when the setTimeout fires 100ms later (React render + effect could take >100ms under load)
- Less explicit — future developers won't understand why a ref exists alongside state

**Assessment:** Fragile. Rejected.

### Alternative B: Read localStorage directly in `detectPhoto`

```javascript
const raw = JSON.parse(localStorage.getItem('fl:consent') || '{}');
if (!raw.biometric) { ... }
```

**Pros:** Always gets the latest persisted value.
**Cons:**
- Bypasses React state entirely — creates inconsistency between what React knows and what the function checks
- Couples `detectPhoto` directly to localStorage key names
- `getBiometricHeaders()` already does this for the HTTP call, so there's no safety gap to fill

**Assessment:** Works but architecturally worse. Rejected.

### Alternative C: Move consent check out of `detectPhoto` entirely

Have callers check consent before calling `detectPhoto`, and `detectPhoto` assumes consent is granted.

**Cons:** Every call site (7 total) must add consent gating. Easy to miss one. Current design is defense-in-depth.

**Assessment:** Increases surface area for consent bypass bugs. Rejected.

**Conclusion:** The `skipConsent` parameter is the cleanest solution. It is explicit, contained, and does not change the default behavior for any existing call site.

## 4. Call Site Inventory — No Breaking Changes

Every call site of `detectPhoto` and whether the new optional parameter affects it:

| Line | Call Site | Context | Impact |
|------|-----------|---------|--------|
| 451 | `handleConsentAccept` | After consent granted | NEEDS `{ skipConsent: true }` |
| 512 | `handleParentUpload` | Normal upload flow | No change (default `skipConsent: false`) |
| 559 | `handleChildUpload` | Normal upload flow | No change |
| 635 | COPPA gate `onConfirm` | After age confirmed | NEEDS `{ skipConsent: true }` (see section 6) |
| 914 | Child re-upload inline | PhotoSlot re-upload | No change |
| 1312 | FacePicker parent crop | After face selection | No change |
| 1327 | FacePicker child crop | After face selection | No change |

The default parameter `{ skipConsent = false } = {}` means all existing call sites that pass only `(file)` are unaffected. **Zero breaking changes.**

## 5. Downstream Effects — No State Inconsistency

After `detectPhoto` succeeds, it returns a quality object: `{ level, faceCount, faces, message }`. Every call site then stores this in state via `setParents` or `setChildren`. This flow is identical whether `skipConsent` is true or false — the parameter only affects the early-return gate, not the return value shape or downstream state writes.

No state inconsistency risk.

## 6. COPPA Gate — SAME BUG, NEEDS SAME FIX

Lines 630-636:
```javascript
<CoppaAgeGate onConfirm={() => {
  confirmAge();
  if (pendingFileRef.current) {
    const file = pendingFileRef.current;
    pendingFileRef.current = null;
    setTimeout(() => detectPhoto(file), 100);
  }
}} onDecline={declineAge} />
```

This has an analogous stale closure issue, but with a twist:

- `confirmAge()` writes to localStorage (line 26 of AgeGateModal.jsx) and sets `showCoppaGate = false`
- `detectPhoto` depends on `promptCoppaIfNeeded` (line 443), which calls `isAgeConfirmed()` (line 15), which reads from localStorage directly (`localStorage.getItem(COPPA_KEY) === 'true'`)
- Since `confirmAge` writes to localStorage **synchronously**, and `isAgeConfirmed` reads localStorage **synchronously**, the COPPA check PASSES even with the stale closure

**However**, the biometric consent check (line 388) is the NEXT gate. If the user has not yet granted biometric consent when the COPPA gate fires, `detectPhoto` will hit `if (!consent.biometric)` and show the consent modal — which is the CORRECT behavior (user needs to pass both gates sequentially).

**But if the user has already granted biometric consent before COPPA fires** (unlikely but possible if consent was granted in a previous session but COPPA was cleared), the stale closure is not a problem because `consent.biometric` was already `true` when `detectPhoto` was created.

**The real scenario where COPPA + consent interact:**
1. Fresh user uploads photo -> COPPA gate shown (consent.biometric = false)
2. User confirms 13+ -> `confirmAge()` + `detectPhoto(file)` via setTimeout
3. `detectPhoto` passes COPPA check (localStorage), hits consent check (React state), consent is false -> shows consent modal
4. User grants consent -> `handleConsentAccept` -> `detectPhoto` again with stale closure -> STUCK

This is the same bug, just with an extra step. The fix must also pass `{ skipConsent: true }` from the COPPA handler **only if consent is already granted at that point**. Actually, re-reading the flow: the COPPA handler should NOT skip consent — it should let `detectPhoto` show the consent modal if needed. The skipConsent fix in `handleConsentAccept` will then handle the final replay correctly.

**Revised assessment:** The COPPA gate handler at line 635 does NOT need `{ skipConsent: true }`. It correctly lets `detectPhoto` show the consent modal if biometric consent hasn't been granted yet. The `handleConsentAccept` handler (line 451) is the one that needs `{ skipConsent: true }`, and it will be the final replay that succeeds.

**Wait — re-examining:** What if consent WAS already granted (returning user who cleared COPPA cookie but not consent)?

1. Upload photo -> COPPA gate shown
2. `detectPhoto` stored file in `pendingFileRef`, returned early at COPPA check
3. User confirms 13+ -> COPPA handler fires `detectPhoto(file)` via setTimeout
4. The `detectPhoto` in the closure was created when COPPA gate was not yet confirmed, but `consent.biometric` was already `true` at that point
5. So `detectPhoto` passes COPPA (reads localStorage) and passes consent (closure had `true`) -> proceeds to `/detect`

This works. No fix needed for this case.

**Final COPPA assessment:** The COPPA handler at line 635 does NOT need `{ skipConsent: true }`. The stale closure bug only manifests in `handleConsentAccept` because that's where `consent` changes from false to true mid-execution.

## 7. Existing Tests — Insufficient Coverage

- `tests/consent/ConsentContext.test.jsx` tests the ConsentContext hook in isolation (load, update, persist). It does NOT test the interaction between consent state and `detectPhoto`.
- No integration test exists for the consent modal flow (upload -> consent prompt -> accept -> detection proceeds).
- No test for the stale closure scenario.

**Would existing tests catch this bug?** No. The ConsentContext tests verify that `updateConsent` works correctly, but the bug is in how UploadSection's `useCallback` captures stale state — a component-level integration concern.

**Would existing tests break with the fix?** No. The fix adds an optional parameter with a default value. No existing test calls `detectPhoto` directly.

**Recommendation:** After implementing the fix, add an integration test that:
1. Mounts UploadSection with `consent.biometric = false`
2. Triggers a photo upload
3. Verifies consent modal appears
4. Simulates "Start My Analysis" tap
5. Verifies `/detect` API is called (not the modal reappearing)

---

## Final Verdict: PASS

The proposed `skipConsent` parameter fix is:

- **Correct:** Solves the stale closure root cause
- **Safe:** Cannot bypass consent (localStorage already written, `getBiometricHeaders` reads from localStorage)
- **Minimal:** One new optional parameter, two call sites changed
- **Non-breaking:** All 7 existing call sites use the default `false` value
- **COPPA-safe:** COPPA gate handler does NOT need the parameter

### Required changes (2 lines):

1. **Line 383:** `const detectPhoto = useCallback(async (file)` -> `const detectPhoto = useCallback(async (file, { skipConsent = false } = {})`
2. **Line 388:** `if (!consent.biometric)` -> `if (!skipConsent && !consent.biometric)`
3. **Line 451:** `setTimeout(() => detectPhoto(file), 100)` -> `setTimeout(() => detectPhoto(file, { skipConsent: true }), 100)`

### NOT required:
- COPPA handler at line 635 does NOT need `{ skipConsent: true }`
- No other call sites need changes

### Recommended follow-up:
- Add integration test for consent modal accept -> detection flow
- Consider reducing the setTimeout from 100ms to 0 (or using `queueMicrotask`) since the delay was meant to wait for state update but `skipConsent` makes that unnecessary
