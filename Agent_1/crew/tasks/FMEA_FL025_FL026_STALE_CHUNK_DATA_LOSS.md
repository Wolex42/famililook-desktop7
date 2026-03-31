# Task: Fix FMEA-FL-025 + FMEA-FL-026 — Stale Chunk Error & Data Loss on Cancel

**Assigned to**: FE Lead
**Priority**: P1 (FL-025), P2 (FL-026)
**Product**: FamiliLook (famililook-desktop2)
**Date**: 2026-03-31

---

## Background

Two production failures observed on https://www.famililook.com:

1. **FL-025**: After a Vercel deploy, users with cached pages get "Failed to fetch dynamically imported module" crash when entering keepsakes. The `CertificateTemplate-D0Hcl63s.js` chunk no longer exists — Vercel serves HTML fallback, causing a MIME type error. The ErrorBoundary catches it but "Try Again" just re-renders (doesn't reload the page), leaving the user stuck.

2. **FL-026**: When the user cancels out of keepsakes (or hits the above error and recovers), ALL analysis data is lost — photos, results, feature votes, winner. User is sent back to the photo upload screen and must start over.

---

## Fix 1: FL-025 — Stale Chunk Recovery (P1)

### Root Cause
- `templateRegistry.js` uses bare `lazy()` for 30+ template imports
- `AppRouter.jsx` already has `lazyWithReload()` wrapper that handles this for route-level pages — but templates are NOT covered
- The `ErrorBoundary.jsx` "Try Again" button calls `setState({ err: null })` which re-renders but does NOT reload the page, so the stale chunk error just recurs

### Required Changes

#### 1a. Export `lazyWithReload` from AppRouter (or move to shared utility)
Move `lazyWithReload()` to a shared location so templateRegistry can import it:
- Create `src/utils/lazyWithReload.js` with the existing logic from AppRouter.jsx:22-34
- Update AppRouter.jsx to import from the shared utility
- Update templateRegistry.js to wrap ALL `lazy()` calls with `lazyWithReload()`

#### 1b. Improve ErrorBoundary recovery
In `src/components/ui/ErrorBoundary.jsx`:
- Detect chunk load errors (message contains "Failed to fetch dynamically imported module" or "Loading chunk")
- For chunk errors: "Try Again" should call `window.location.reload()` instead of just resetting state
- Use the same sessionStorage guard (`fl:chunk-reload`) to prevent infinite reload loops
- If already reloaded once and still failing, show "Please refresh the page" message

### Files to modify
- `src/utils/lazyWithReload.js` (NEW — extract from AppRouter)
- `src/AppRouter.jsx` (import from shared utility)
- `src/components/keepsakes/utils/templateRegistry.js` (wrap all lazy() with lazyWithReload())
- `src/components/ui/ErrorBoundary.jsx` (chunk error detection + reload)

---

## Fix 2: FL-026 — Analysis State Persistence (P2)

### Root Cause
- Analysis results exist only in React state (`FamililookContext.jsx`)
- Any unmount, error recovery, or navigation destroys the data
- No persistence layer to sessionStorage

### Required Changes

#### 2a. Persist analysis results after successful analysis
In `src/state/FamililookContext.jsx`:
- After analysis completes successfully, write results to `sessionStorage` under key `fl:analysis-cache`
- Store: `analysisResults`, `uploadedPhotos` (as base64 or blob URLs), `parentNames`, `childNames`
- On context mount, check for `fl:analysis-cache` and restore if present

#### 2b. Clear cache only on explicit new analysis
- Clear `fl:analysis-cache` when user explicitly starts a new analysis (clicks "New Analysis" or re-uploads)
- Do NOT clear on error boundary reset, cancel, or navigation
- Clear on session end (sessionStorage handles this automatically)

#### 2c. Handle photos carefully
- Photo blobs may be too large for sessionStorage (5MB limit)
- Strategy: persist analysis results + metadata only; re-fetch photos from object URLs if still available
- If photos are gone, show results without photos (they have the data, just not the images)
- Consider: store thumbnail versions (canvas resize to ~200px) for sessionStorage

### Files to modify
- `src/state/FamililookContext.jsx` (add persistence logic)
- `src/components/ui/ErrorBoundary.jsx` (do NOT clear sessionStorage on reset)

---

## Testing Requirements

### FL-025 Tests
- Unit test: `lazyWithReload` returns a lazy component
- Unit test: `lazyWithReload` retries import on failure
- Unit test: `lazyWithReload` only reloads once (sessionStorage guard)
- Unit test: ErrorBoundary detects chunk errors and offers reload
- Manual: deploy new build, visit old cached page, verify auto-reload works

### FL-026 Tests
- Unit test: analysis results persisted to sessionStorage after analysis
- Unit test: results restored from sessionStorage on mount
- Unit test: cache cleared on new analysis, not on cancel
- Manual: complete analysis, close keepsakes modal, verify results still present
- Manual: complete analysis, refresh page, verify results restored

---

## Constraints
- Do NOT modify any backend files
- Do NOT break existing `lazyWithReload` behavior in AppRouter
- Do NOT persist sensitive biometric data — only analysis results (feature votes, percentages, winner)
- sessionStorage key must follow existing `fl:` prefix convention
- All changes must pass `npm run test:run` and `npm run build`

---

## FMEA Traceability
- FL-025: `docs/DFMEA_facematch.md` section FL-025, `docs/MASTER_REGRESSION_MATRIX.md` row FL-5.4
- FL-026: `docs/DFMEA_facematch.md` section FL-026, `docs/MASTER_REGRESSION_MATRIX.md` row FL-3.6
- After fix, update both docs with post-fix RPN and sprint reference
