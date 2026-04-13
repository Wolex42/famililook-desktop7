# GAP-11: Modal Focus Management Audit

**Date:** 2026-03-31
**Agent:** Frontend Lead
**Hook:** `src/hooks/useFocusTrap.js` (desktop2)

## Summary

`useFocusTrap(isActive)` returns a `trapRef` to assign to the modal container. It traps Tab/Shift+Tab cycling, auto-focuses the first focusable element on open, and restores focus on close.

Only **1 out of 10** audited modal-like components currently uses the hook.

## Audit Results

| # | Modal | Repo | File | Focus Trap? | `aria-modal`? | `role="dialog"`? | Escape Dismiss? | Status |
|---|-------|------|------|-------------|---------------|-------------------|-----------------|--------|
| 1 | KeepsakesModal | desktop2 | `src/components/keepsakes/KeepsakesModal.jsx` | YES | YES | YES | YES | COMPLIANT |
| 2 | CoppaAgeGate | desktop2 | `src/components/ui/AgeGateModal.jsx` | NO | NO | NO | NO | NEEDS FIX |
| 3 | AgeGateModal (18+) | desktop2 | `src/components/ui/AgeGateModal.jsx` | NO | NO | NO | NO | NEEDS FIX |
| 4 | ConsentBanner | desktop2 | `src/components/ui/ConsentBanner.jsx` | NO | NO | NO | NO | LOW PRIORITY (banner, not modal) |
| 5 | UpgradeOverlay | desktop2 | `src/components/ui/UpgradeOverlay.jsx` | NO | NO | NO | NO | LOW PRIORITY (inline overlay, not fixed modal) |
| 6 | FeedbackModal | desktop2 | `src/components/modals/FeedbackModal.jsx` | NO | NO | NO | NO (backdrop click only) | NEEDS FIX |
| 7 | OrderModal | desktop2 | `src/components/keepsakes/OrderModal.jsx` | NO | NO | NO | NO | NEEDS FIX |
| 8 | FacePicker | desktop2 | `src/components/upload/FacePicker.jsx` | NO | NO | NO | NO | NEEDS FIX |
| 9 | AgeGateModal | desktop4 | `src/components/ui/AgeGateModal.jsx` | NO | NO | NO | NO | NEEDS FIX |
| 10 | ErrorBoundary | desktop4 | `src/components/ui/ErrorBoundary.jsx` | N/A | N/A | N/A | N/A | NOT A MODAL (inline error) |
| 11 | ConsentModal | desktop6 | `src/components/ConsentModal.jsx` | NO | NO | NO | NO | NEEDS FIX |

## Remediation Plan

### Priority 1 — Full-screen blocking modals (accessibility + compliance)

These are `position: fixed` overlays that block all interaction. They **must** have focus trap, `role="dialog"`, `aria-modal="true"`, and Escape dismiss.

1. **CoppaAgeGate** (desktop2) — COPPA compliance gate. Add `useFocusTrap`, `role="dialog"`, `aria-modal="true"`. Escape should call `onDecline`.
2. **AgeGateModal (18+)** (desktop2) — Same file, same treatment.
3. **FeedbackModal** (desktop2) — Full-screen survey. Add `useFocusTrap`, `role="dialog"`, `aria-modal="true"`. Already has backdrop-click dismiss; add Escape key handler.
4. **OrderModal** (desktop2) — Checkout flow. Add `useFocusTrap`, `role="dialog"`, `aria-modal="true"`, Escape dismiss.
5. **FacePicker** (desktop2) — Face selection overlay. Add `useFocusTrap`, `role="dialog"`, `aria-modal="true"`, Escape dismiss.
6. **ConsentModal** (desktop6) — BIPA consent gate. Add `useFocusTrap`, `role="dialog"`, `aria-modal="true"`. Note: Escape should call `handleDecline` (navigates away).
7. **AgeGateModal** (desktop4) — Same pattern as desktop2 version. Add focus trap, ARIA attributes, Escape dismiss.

### Priority 2 — Banners and inline overlays (nice-to-have)

8. **ConsentBanner** (desktop2) — Bottom-sticky banner, not a blocking modal. Focus trap is optional but `role="region"` + `aria-label` would improve screen reader experience. Not urgent.
9. **UpgradeOverlay** (desktop2) — Inline content overlay (not `position: fixed`). Not a modal in the ARIA sense. No focus trap needed. Could add `role="alert"` for screen readers.

### Not applicable

10. **ErrorBoundary** (desktop4) — React error boundary rendering inline error text. Not a modal. No changes needed.

## Implementation Pattern

For each modal that needs the fix, the changes are:

```jsx
// 1. Import the hook
import { useFocusTrap } from "../../hooks/useFocusTrap.js";

// 2. Call it (isActive = true when modal is visible)
const trapRef = useFocusTrap(isOpen);

// 3. Attach ref + ARIA to the modal container div
<div ref={trapRef} role="dialog" aria-modal="true" aria-label="Modal Title">

// 4. Add Escape key handler (if not already present)
useEffect(() => {
  const handler = (e) => { if (e.key === "Escape") onClose?.(); };
  document.addEventListener("keydown", handler);
  return () => document.removeEventListener("keydown", handler);
}, [onClose]);
```

For desktop4 and desktop6, `useFocusTrap.js` would need to be copied from desktop2 since these are independent repos (not submodules).

## Notes

- The `useFocusTrap` hook file location for desktop2: `src/hooks/useFocusTrap.js`
- desktop4 and desktop6 do **not** have this hook — it must be added as a new file
- KeepsakesModal is the only modal that currently meets WCAG 2.1 focus management requirements
- All 7 Priority 1 fixes are straightforward (same pattern, ~10 lines each)
