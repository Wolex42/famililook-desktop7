# MODULE SPEC — AppErrorBus

**Platform Architect — 2026-04-09**
**Version:** 1.0
**Status:** SPEC COMPLETE — Awaiting CEO approval

---

## 1. PROBLEM CATEGORY

**Class of bugs eliminated:** Silent catch blocks that swallow errors, leaving users with unresponsive UI and developers with no diagnostic signal.

**Current instance count:** 23 locations audited. After code verification:

- **19 ACTIVE silent catches** still present in the codebase
- **4 ALREADY ADDRESSED** (FacePicker.jsx shows inline error; DropLane.jsx sets `it.error`; OrderSuccessPage.jsx has retry+polling logic; OrderModal.jsx surfaces `orderError` to UI)

**Impact:** When a silent catch fires in production, the user sees nothing. They tap a button and nothing happens. They upload a photo and it silently fails. Their basket fails to save and they lose items. There is no telemetry to diagnose the issue.

**Root cause:** No centralised error reporting mechanism exists. Each developer writes their own `catch {}` because there is no easier alternative. The result is 19 independent decisions to swallow errors, each made in isolation, each invisible.

---

## 2. VERIFIED AUDIT — All 23 Locations

### Status Key
- **ACTIVE** = Silent catch still present, needs AppErrorBus migration
- **PARTIAL** = Some error handling exists but should also report to AppErrorBus
- **RESOLVED** = Already shows error to user (but may optionally report for telemetry)

| # | File | Line(s) | Current Pattern | Status | Severity | Domain |
|---|------|---------|----------------|--------|----------|--------|
| 1 | `components/upload/FacePicker.jsx` | 85-87 | `setCropError()` + `console.warn` — shows inline error | RESOLVED | -- | Upload |
| 2 | `layout/UploadSection.jsx` | 501, 538, 583, 601, 1309, 1324 | `try { URL.revokeObjectURL(...) } catch { /* noop */ }` x6 | ACTIVE (low) | Low | Upload |
| 3 | `components/upload/DropLane.jsx` | 92-95 | Sets `it.error = "Face detection failed"` + `logger.warn` | PARTIAL | Medium | Upload |
| 4 | `utils/imageProcessing.js` | 115-137 | Fallback detection with null embeddings, `logger.error` on both failures | PARTIAL | High | Upload |
| 5 | `state/detectConfig.js` | 10, 19 | `catch { return fallback }` on parse, `catch { /* quota */ }` on save | ACTIVE | Low | Upload |
| 6 | `state/FamililookContext.jsx` | 25, 35, 43, 109, 112, 125, 157, 170, 183 | 9 silent catches — sessionStorage persist, localStorage reads, plan reads | ACTIVE | Medium | State |
| 7 | `components/ui/AgeGateModal.jsx` | 16, 26, 123, 127, 133 | 5 silent catches — COPPA/age gate localStorage reads/writes | ACTIVE | Medium | Upload |
| 8 | `hooks/useKinshipAnalysis.jsx` | 297 | `catch { /* ignore */ }` on `fl:groupSnapshot` parse | ACTIVE | Low | Analysis |
| 9 | `hooks/useKinshipAnalysis.jsx` | 541 | `catch { /* ignore */ }` on `fl:groupSnapshot` persist | ACTIVE | Low | Analysis |
| 10 | `hooks/useKinshipAnalysis.jsx` | 678-679 | Pet analysis catch — `logger.warn` only, no user feedback | ACTIVE | Medium | Analysis |
| 11 | `api/kinshipClient.js` | 65 | `catch { /* ignore */ }` on plan/email header reads | ACTIVE | Low | Analysis |
| 12 | `layout/MobileResultsSection.jsx` | 332-334 | Feature count invariant logged but not enforced | ACTIVE | High | Analysis |
| 13 | `state/BasketContext.jsx` | 16, 24 | `catch { return [] }` on load, `catch { /* Storage full */ }` on save | ACTIVE | High | Commerce |
| 14 | `api/orderApi.js` | 22-31 | Timeout abort via `fetchWithTimeout` — abort not surfaced distinctly | PARTIAL | High | Commerce |
| 15 | `pages/OrderSuccessPage.jsx` | 52-98 | 404 race handled with polling + exponential backoff | RESOLVED | -- | Commerce |
| 16 | `components/keepsakes/KeepsakesModal.jsx` | 488-494 | Returns "No analysis data" message but no toast/bus report | PARTIAL | Medium | Commerce |
| 17 | `components/keepsakes/OrderModal.jsx` | 141-144 | `console.error` + sets `orderError` state — shows error to user | RESOLVED | -- | Commerce |
| 18 | `game/CardGame.jsx` | 671-675 | `buildDeck` fail logged + shows empty deck, no user message | ACTIVE | Medium | Games |
| 19 | `game/FaceFusion/FaceFusion.jsx` | 71-73, 86-88 | Two silent catches — buildDeck fail + outer catch sets empty array | ACTIVE | Medium | Games |
| 20 | `game/deckBuilder.js` | 222-226 | Module-level `PERSON_FEATURE_CACHE` object, cleared on `buildDeck()` call (line 860) | RESOLVED | -- | Games |
| 21 | `hooks/usePlanFeatures.js` | 103, 117, 122-125, 168-173 | Silent catches on ambassador localStorage + network `.catch()` with no user signal | ACTIVE | Medium | State |
| 22 | `hooks/usePlanFeatures.js` | 128-134 | Ambassador revocation race — network error falls back to stale cache for 24h | ACTIVE | Medium | State |
| 23 | `utils/analytics.js` | 264-267, 272-282 | Tab counter + beforeunload cleanup — 3 silent catches | ACTIVE | Low | State |

### Summary

| Status | Count |
|--------|-------|
| ACTIVE | 15 |
| PARTIAL (needs report call added) | 4 |
| RESOLVED (optional telemetry) | 4 |
| **Total to migrate** | **19** (15 ACTIVE + 4 PARTIAL) |

---

## 3. MODULE INTERFACE

### 3.1 Architecture Decision: Lightweight Event Emitter

**NOT Zustand** — Zustand is not in the project's dependencies. Adding it solely for AppErrorBus would violate the "no new dependencies" constraint.

**Chosen pattern:** Vanilla JS module with a subscriber list. This is:
- Zero-dependency (works with any React version)
- Tree-shakeable (unused imports are eliminated)
- Testable in isolation (no React context needed for unit tests)
- Compatible with the existing `Toast.jsx` system

### 3.2 File Location

```
src/infrastructure/AppErrorBus.js     (new directory, new file)
src/components/ui/ErrorToast.jsx      (new file — consumes from AppErrorBus)
```

### 3.3 Type Definitions (JSDoc)

```javascript
/**
 * @typedef {'low' | 'medium' | 'high' | 'critical'} ErrorSeverity
 *
 * @typedef {Object} ErrorReport
 * @property {string}         message    - Human-readable error description
 * @property {string}         context    - Which component/module reported it (e.g. "BasketContext.save")
 * @property {ErrorSeverity}  severity   - Determines user visibility + auto-dismiss behaviour
 * @property {string}         [code]     - Optional machine-readable code (e.g. "STORAGE_FULL", "NETWORK_TIMEOUT")
 * @property {Error}          [cause]    - Optional original Error object for dev console
 * @property {Object}         [meta]     - Optional metadata (file, line, retry count, etc.)
 *
 * @typedef {Object} StoredError
 * @property {string}         id         - Unique ID (crypto.randomUUID or Date.now fallback)
 * @property {ErrorReport}    report     - The original report
 * @property {number}         timestamp  - Date.now() when reported
 * @property {boolean}        dismissed  - Whether user/auto has dismissed it
 */
```

### 3.4 Public API

```javascript
// ─── Reporting ──────────────────────────────────────────────────
AppErrorBus.report(report: ErrorReport): string
// Returns the error ID. Adds to internal queue.
// In DEV mode: always logs to console (severity-coloured).
// In PROD mode: low = console only; medium/high/critical = toast.
// Deduplication: if an identical (message + context + code) error was reported
// within the last 5 seconds, it is silently dropped (prevents flood).

// ─── Reading ────────────────────────────────────────────────────
AppErrorBus.getActive(): StoredError[]
// Returns all non-dismissed errors, sorted newest-first.
// Capped at MAX_ACTIVE (20). Oldest are auto-pruned.

AppErrorBus.getAll(): StoredError[]
// Returns full history (capped at MAX_HISTORY = 50), including dismissed.
// Useful for dev panel / diagnostics.

// ─── Dismissal ──────────────────────────────────────────────────
AppErrorBus.dismiss(id: string): void
// Marks a specific error as dismissed. Notifies subscribers.

AppErrorBus.clear(): void
// Marks ALL errors as dismissed. Notifies subscribers.

// ─── Subscription ───────────────────────────────────────────────
AppErrorBus.subscribe(callback: (errors: StoredError[]) => void): () => void
// Subscribe to changes. Returns an unsubscribe function.
// Callback receives the current active errors array.
// Used by ErrorToast component to re-render on new errors.

// ─── Dev tools ──────────────────────────────────────────────────
AppErrorBus.getStats(): { total: number, active: number, bySeverity: Record<ErrorSeverity, number> }
// Summary for dev panel or console inspection.
// Only meaningful in DEV mode; returns zeros in PROD (tree-shaken).
```

### 3.5 Severity Levels — Behaviour Matrix

| Severity | User Toast | Auto-Dismiss | Console (DEV) | Console (PROD) | Example |
|----------|-----------|-------------|---------------|----------------|---------|
| `low` | No | N/A | `console.debug` (grey) | No | `revokeObjectURL` fail, config parse fail |
| `medium` | Yes (4s) | Yes (4s) | `console.warn` (yellow) | No | Session persist fail, age gate storage fail |
| `high` | Yes (8s) | Yes (8s) | `console.error` (red) | `console.error` | Basket save fail, feature invariant violation |
| `critical` | Yes (sticky) | No — requires dismiss | `console.error` (red) | `console.error` | Network timeout on order, analysis crash |

### 3.6 Deduplication Logic

An error is considered a duplicate if ALL of the following match within a 5-second window:
- `message` (exact string match)
- `context` (exact string match)
- `code` (exact string match, or both undefined)

Duplicate errors increment a `count` field on the existing `StoredError` rather than creating a new entry. The toast shows "(x2)", "(x3)" etc. if count > 1.

### 3.7 ErrorToast Component Specification

```jsx
// src/components/ui/ErrorToast.jsx
//
// Renders active medium/high/critical errors from AppErrorBus.
// Does NOT replace the existing Toast.jsx system — that system handles
// success/info toasts from user actions (e.g. "Added to basket").
// ErrorToast handles system-level error reporting only.
//
// Placement: fixed, bottom-right on desktop, bottom-center on mobile.
// Max visible: 3 toasts. Overflow queued (shown after dismiss/auto-dismiss).
// Stacking: newest on top, 8px gap.
// Animation: slide-up entry, slide-down exit (framer-motion already in deps).
//
// Props: none (reads from AppErrorBus.subscribe internally).
// Must be rendered once at app root level (inside AppLayout.jsx).

function ErrorToast() {
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    return AppErrorBus.subscribe((active) => {
      // Only show medium+ to user
      setErrors(active.filter(e => e.report.severity !== 'low').slice(0, 3));
    });
  }, []);

  // ... render logic using severity-based styling
}
```

**Styling per severity:**

| Severity | Background | Icon | Border |
|----------|-----------|------|--------|
| `medium` | `rgba(245, 158, 11, 0.95)` (amber) | `AlertTriangle` | `#f59e0b` |
| `high` | `rgba(239, 68, 68, 0.95)` (red) | `AlertCircle` | `#ef4444` |
| `critical` | `rgba(220, 38, 38, 0.95)` (dark red) | `XCircle` | `#dc2626` |

### 3.8 Relationship to Existing Error Handling

| Existing system | Handles | AppErrorBus relationship |
|----------------|---------|-------------------------|
| `ErrorBoundary.jsx` | Synchronous render crashes (class component `componentDidCatch`) | **Separate concern.** ErrorBoundary catches React render errors. AppErrorBus catches async/caught errors. They do not overlap. ErrorBoundary MAY optionally call `AppErrorBus.report()` in `componentDidCatch` for telemetry, but this is Phase 4 (optional). |
| `Toast.jsx` / `useToast()` | User-action feedback (success, info, warning) | **Separate concern.** Toast.jsx is for intentional user feedback ("Added to basket", "Copied link"). ErrorToast is for system-level error reporting. They coexist. Different z-index and position. |
| Inline error states (e.g. `setCropError` in FacePicker) | Component-local error display | **Complementary.** If a component already shows an inline error, AppErrorBus report is optional (for telemetry). If a component has NO inline error display, AppErrorBus report is REQUIRED. |

### 3.9 Recommendation on FacePicker.jsx (Finding #1)

FacePicker.jsx already shows an inline error via `setCropError()` and logs to console. **Recommendation: Do NOT add AppErrorBus.report() here in Phase 2.** The inline error is the correct UX for this interaction. However, in Phase 3, adding a `low` severity report is acceptable for telemetry completeness. This is optional.

---

## 4. ADOPTION RULE

**Once AppErrorBus ships (Phase 1 complete), the following is FORBIDDEN:**

### Rule A: No bare catch blocks
```javascript
// FORBIDDEN after Phase 1:
try { ... } catch { /* noop */ }
try { ... } catch { /* ignore */ }
try { ... } catch { /* quota */ }
try { ... } catch (e) { console.log(e); }
try { ... } catch (e) { console.warn(e); }

// REQUIRED:
try { ... } catch (e) {
  AppErrorBus.report({
    message: 'Human-readable description of what failed',
    context: 'ComponentName.methodName',
    severity: 'low',  // or medium/high/critical
    cause: e,
  });
}
```

### Rule B: No `.catch(() => {})` on Promises
```javascript
// FORBIDDEN:
fetchSomething().catch(() => {});

// REQUIRED:
fetchSomething().catch((e) => {
  AppErrorBus.report({ message: '...', context: '...', severity: '...', cause: e });
});
```

### Rule C: Minimum viable report
Every `AppErrorBus.report()` call MUST include at minimum:
- `message` — a string a human can understand without reading code
- `context` — the file + function name (e.g. `"BasketContext.saveBasket"`)
- `severity` — one of `low | medium | high | critical`

### Enforcement
- **Change Manager** — reviews all PRs for bare catch blocks. Rejects any PR that introduces a new bare catch after AppErrorBus ships.
- **QA Lead** — verifies that migration phases are complete. Blocks release if active silent catches remain in migrated files.
- **ESLint rule** (Phase 4) — `no-bare-catch` custom rule that flags `catch {}` and `catch { /* ... */ }` patterns. Auto-fixable with a template that imports AppErrorBus.

---

## 5. MIGRATION PATH

### Phase 1: Build Module + ErrorToast (1 session)

**Deliverables:**
1. Create `src/infrastructure/AppErrorBus.js` — full module per Section 3 spec
2. Create `src/components/ui/ErrorToast.jsx` — consumer component per Section 3.7
3. Wire `<ErrorToast />` into `src/layout/AppLayout.jsx` (single render point)
4. Unit tests for AppErrorBus (see Section 7)
5. Unit tests for ErrorToast (see Section 7)

**Zero migration in Phase 1.** No existing catch blocks are changed. This phase only builds and tests the module.

### Phase 2: Migrate High-Severity Catches (1 session)

Migrate the catches that have the most user impact first. These are the ones where the user loses data, loses money, or gets a broken experience with zero feedback.

**Phase 2 files (7 locations, 4 files):**

| Priority | File | Lines | What changes | Severity |
|----------|------|-------|-------------|----------|
| P1 | `state/BasketContext.jsx` | 16, 24 | Storage-full catch reports `high` — user's basket items are silently lost | `high` |
| P2 | `layout/MobileResultsSection.jsx` | 332-334 | Feature count invariant violation reports `high` — contract breach | `high` |
| P3 | `utils/imageProcessing.js` | 115-137 | Fallback detection reports `high` — embeddings are null, analysis quality degraded | `high` |
| P4 | `game/CardGame.jsx` | 671-675 | `buildDeck` failure reports `medium` — user sees blank deck with no explanation | `medium` |
| P5 | `game/FaceFusion/FaceFusion.jsx` | 71-73, 86-88 | Both catches report `medium` — game shows empty state | `medium` |
| P6 | `hooks/useKinshipAnalysis.jsx` | 678-679 | Pet analysis failure reports `medium` — user doesn't know pet analysis failed | `medium` |
| P7 | `api/kinshipClient.js` | 65 | Plan header read failure reports `low` — non-user-facing but affects tier | `low` |

### Phase 3: Full Migration (1 session)

Migrate all remaining 12 ACTIVE locations. These are lower-severity catches that are still silent but have less direct user impact.

**Phase 3 files (12 locations, 6 files):**

| File | Lines | Count | Severity |
|------|-------|-------|----------|
| `layout/UploadSection.jsx` | 501, 538, 583, 601, 1309, 1324 | 6 | `low` (revokeObjectURL is fire-and-forget) |
| `state/FamililookContext.jsx` | 25, 35, 43, 109, 112, 125, 157, 170, 183 | 9 | `low` to `medium` (sessionStorage persist) |
| `components/ui/AgeGateModal.jsx` | 16, 26, 123, 127, 133 | 5 | `medium` (COPPA gate — if localStorage unavailable, user can't confirm age) |
| `state/detectConfig.js` | 10, 19 | 2 | `low` (config cache miss is non-fatal) |
| `hooks/useKinshipAnalysis.jsx` | 297, 541 | 2 | `low` (snapshot persist is convenience cache) |
| `hooks/usePlanFeatures.js` | 103, 117, 122-125 | 3 | `medium` (ambassador state management) |
| `utils/analytics.js` | 264-267, 272-282 | 3 | `low` (tab counter cleanup) |

### Phase 4: Lint Rule + Optional Telemetry (0.5 session)

1. Add ESLint rule to `.eslintrc` / `eslint.config.js`:
   - Custom rule or use `eslint-plugin-no-catch-all` pattern
   - Flag any `catch` block that does not contain `AppErrorBus.report`
   - Severity: `error` (blocks CI)
2. Optionally add `low` severity reports to the 4 RESOLVED locations for telemetry
3. Optionally wire `ErrorBoundary.componentDidCatch` to `AppErrorBus.report({ severity: 'critical' })`

---

## 6. FILES AFFECTED — Complete List

### New Files (Phase 1)
| File | Purpose |
|------|---------|
| `src/infrastructure/AppErrorBus.js` | Core error bus module |
| `src/components/ui/ErrorToast.jsx` | Toast consumer component |
| `src/infrastructure/__tests__/AppErrorBus.test.js` | Unit tests |
| `src/components/ui/__tests__/ErrorToast.test.jsx` | Component tests |

### Modified Files (Phase 1)
| File | Change |
|------|--------|
| `src/layout/AppLayout.jsx` | Add `<ErrorToast />` render (1 line) |

### Modified Files (Phase 2)
| File | Lines Changed |
|------|--------------|
| `state/BasketContext.jsx` | Lines 16, 24 |
| `layout/MobileResultsSection.jsx` | Lines 332-334 |
| `utils/imageProcessing.js` | Lines 115-137 |
| `game/CardGame.jsx` | Lines 671-675 |
| `game/FaceFusion/FaceFusion.jsx` | Lines 71-73, 86-88 |
| `hooks/useKinshipAnalysis.jsx` | Lines 678-679 |
| `api/kinshipClient.js` | Line 65 |

### Modified Files (Phase 3)
| File | Lines Changed |
|------|--------------|
| `layout/UploadSection.jsx` | Lines 501, 538, 583, 601, 1309, 1324 |
| `state/FamililookContext.jsx` | Lines 25, 35, 43, 109, 112, 125, 157, 170, 183 |
| `components/ui/AgeGateModal.jsx` | Lines 16, 26, 123, 127, 133 |
| `state/detectConfig.js` | Lines 10, 19 |
| `hooks/useKinshipAnalysis.jsx` | Lines 297, 541 |
| `hooks/usePlanFeatures.js` | Lines 103, 117, 122-125 |
| `utils/analytics.js` | Lines 264-267, 272-282 |

### Modified Files (Phase 4)
| File | Change |
|------|--------|
| `eslint.config.js` | Add custom `no-bare-catch` rule |
| `components/ui/ErrorBoundary.jsx` | Optional: add `AppErrorBus.report` in `componentDidCatch` |

---

## 7. TEST REQUIREMENTS

### 7.1 Unit Tests — AppErrorBus (`AppErrorBus.test.js`)

**Must test:**

1. **report() stores error** — call `report()`, verify `getActive()` returns it with correct fields
2. **report() assigns unique ID** — two sequential reports have different IDs
3. **report() notifies subscribers** — subscribe, report, verify callback fired with correct data
4. **Deduplication** — report same (message, context, code) twice within 5s, verify only 1 entry with `count: 2`
5. **Deduplication expiry** — report, wait 5s (fake timer), report same, verify 2 entries
6. **dismiss() marks dismissed** — report, dismiss by ID, verify `getActive()` is empty but `getAll()` still has it
7. **clear() dismisses all** — report 3 errors, `clear()`, verify `getActive()` returns empty
8. **MAX_ACTIVE cap (20)** — report 25 errors, verify `getActive().length === 20`, oldest pruned
9. **MAX_HISTORY cap (50)** — report 55 errors, verify `getAll().length === 50`
10. **Unsubscribe works** — subscribe, unsubscribe, report, verify callback NOT fired
11. **Multiple subscribers** — 2 subscribers, report, both notified. Unsubscribe one, report again, only remaining subscriber notified
12. **getStats()** — report mix of severities, verify counts match

### 7.2 Unit Tests — ErrorToast (`ErrorToast.test.jsx`)

**Must test:**

1. **Renders nothing when no errors** — mount, verify no toast elements
2. **Renders toast on medium+ error** — report `medium` error, verify toast appears with message
3. **Does NOT render low severity** — report `low` error, verify no toast
4. **Max 3 visible** — report 5 `medium` errors, verify only 3 rendered
5. **Auto-dismiss medium after 4s** — report `medium`, advance timer 4s, verify toast gone
6. **Auto-dismiss high after 8s** — report `high`, advance timer 8s, verify toast gone
7. **Critical does NOT auto-dismiss** — report `critical`, advance timer 30s, verify still visible
8. **Manual dismiss** — report `high`, click dismiss button, verify toast removed
9. **Severity styling** — verify `medium` has amber style, `high` has red, `critical` has dark red
10. **Dedup count shown** — report same error 3x, verify toast shows "(x3)"

### 7.3 Integration Tests

1. **BasketContext + AppErrorBus** — mock `localStorage.setItem` to throw `QuotaExceededError`, add item to basket, verify `AppErrorBus.getActive()` has a `high` severity error
2. **CardGame + AppErrorBus** — mock `buildDeck` to throw, verify `medium` error reported
3. **ErrorToast in AppLayout** — render full AppLayout, report `high` error, verify toast visible in DOM

---

## 8. SECONDARY FAILURE RISKS

### Risk 1: Error Flood
**Scenario:** A loop or repeated render causes hundreds of `report()` calls per second.
**Mitigation:** Deduplication (5s window, same message+context+code = single entry). MAX_ACTIVE cap of 20. If `getActive().length === 20`, new reports still stored in history but do NOT trigger a new toast — only the queue counter increments.

### Risk 2: Toast Stacking
**Scenario:** Multiple high/critical errors stack and cover the entire viewport on mobile.
**Mitigation:** Max 3 visible toasts. Overflow is queued. Each dismiss reveals the next queued toast. On mobile (viewport < 640px), max 2 visible.

### Risk 3: Memory Leak from Uncleared Errors
**Scenario:** Long-running session accumulates thousands of errors in history.
**Mitigation:** MAX_HISTORY = 50. Oldest entries are pruned on every `report()` call. No WeakRef or closure leaks because subscribers are simple function references, cleaned up by the returned unsubscribe function.

### Risk 4: Subscriber Leak
**Scenario:** Component mounts/unmounts rapidly without calling unsubscribe.
**Mitigation:** `subscribe()` returns an unsubscribe function. ErrorToast uses it in `useEffect` cleanup. The module also has a safety check: if subscriber count exceeds 10, log a dev warning (likely a leak).

### Risk 5: beforeunload Race
**Scenario:** `analytics.js` reports an error in `beforeunload` handler, but the page is already unloading.
**Mitigation:** `report()` is synchronous (no async work). It writes to an in-memory array. The toast won't render during unload, but the report is still logged to console in dev mode. This is acceptable — `beforeunload` errors are diagnostic-only.

### Risk 6: Circular Error
**Scenario:** ErrorToast itself throws during render, causing ErrorBoundary to catch it, which reports to AppErrorBus, which triggers ErrorToast re-render, which throws again.
**Mitigation:** ErrorToast MUST be wrapped in its own `ErrorBoundary` with a static fallback (no AppErrorBus reporting from within ErrorToast's own boundary). The module also has a re-entrancy guard: if `report()` is called while already inside a `report()` call, the inner call is queued via `queueMicrotask` rather than executing synchronously.

### Risk 7: Import Cost
**Scenario:** Tree-shaking doesn't work and the module is included in chunks that don't need it.
**Mitigation:** Module is a plain JS file with named exports. No side effects at import time (the module-level `errors` array is a simple `let`). Vite's tree-shaking handles this correctly. The `ErrorToast` component is only imported in `AppLayout.jsx`.

---

## 9. BUILD ESTIMATE

| Phase | Sessions | FE Lead Work |
|-------|----------|-------------|
| Phase 1: Module + ErrorToast + Tests | 1 | Build AppErrorBus.js, ErrorToast.jsx, wire into AppLayout, write 22 tests |
| Phase 2: High-severity migration | 1 | Modify 7 files (7 locations), add import + report calls, verify existing tests pass |
| Phase 3: Full migration | 1 | Modify 7 files (25 locations), same pattern as Phase 2, verify all tests pass |
| Phase 4: Lint rule | 0.5 | Add ESLint custom rule, optional telemetry additions |
| **Total** | **3.5 sessions** | |

**Dependencies:** None. AppErrorBus has zero external dependencies. ErrorToast uses `framer-motion` (already installed) and `lucide-react` (already installed).

**Risk to existing tests:** LOW. Phases 2-3 only ADD `AppErrorBus.report()` calls inside existing catch blocks. No logic is changed. No return values are modified. Existing tests should pass without modification. New tests are additive.

---

## 10. IMPLEMENTATION NOTES FOR FE LEAD

### Do:
- Keep the module as a plain ES module (no class, no React context for the bus itself)
- Use `crypto.randomUUID()` for IDs (fallback to `Date.now() + Math.random()` for test environments)
- Use `Object.freeze()` on returned `StoredError` objects to prevent mutation
- Use `structuredClone()` when returning arrays from `getActive()` / `getAll()` to prevent external mutation of internal state
- Keep ErrorToast positioned at `z-index: 9999` (above modals at `z-index: 2000`)

### Do Not:
- Do NOT use React context for the bus. The bus must be importable from non-React code (e.g. `orderApi.js`, `analytics.js`)
- Do NOT persist errors to localStorage. Errors are session-scoped (in-memory only)
- Do NOT add network calls (no Sentry, no remote logging). That is a future concern
- Do NOT modify the existing `Toast.jsx` or `useToast()` system. They serve different purposes
- Do NOT add `AppErrorBus.report()` to any catch block where the error is INTENTIONALLY swallowed (e.g. `revokeObjectURL` failures are genuinely harmless — report as `low` for telemetry but do not elevate)

### Severity Assignment Guidelines:
- **low**: The catch is defensive programming. Failure has no user-visible effect. (revokeObjectURL, config cache miss, analytics tab counter)
- **medium**: The user might notice something is wrong but can still use the app. (session persist fail, age gate storage, game empty state)
- **high**: The user loses data or gets incorrect results. (basket save fail, feature invariant violation, fallback detection with null embeddings)
- **critical**: The user's transaction fails or the app is in an unrecoverable state. (order API timeout, analysis crash with no fallback)

---

## APPENDIX A: Example Migration — BasketContext.jsx

**Before (current code, line 24):**
```javascript
function saveBasket(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {
    // Storage full — silent fail
  }
}
```

**After (Phase 2 migration):**
```javascript
import { AppErrorBus } from '../infrastructure/AppErrorBus';

function saveBasket(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch (e) {
    AppErrorBus.report({
      message: 'Could not save your basket — storage may be full. Your items are still in memory but may not survive a page refresh.',
      context: 'BasketContext.saveBasket',
      severity: 'high',
      code: 'STORAGE_FULL',
      cause: e,
    });
  }
}
```

**Key points:**
- The catch named the error (`e`) instead of swallowing it
- The message is user-readable (not "QuotaExceededError")
- The severity is `high` because the user loses basket data on refresh
- The `code` field enables programmatic filtering if needed later
- The `cause` field preserves the original error for dev console

---

## APPENDIX B: Example Migration — UploadSection.jsx (Low Severity)

**Before (current code, line 501):**
```javascript
if (next[index]?.previewUrl) try { URL.revokeObjectURL(next[index].previewUrl); } catch { /* noop */ }
```

**After (Phase 3 migration):**
```javascript
if (next[index]?.previewUrl) try {
  URL.revokeObjectURL(next[index].previewUrl);
} catch (e) {
  AppErrorBus.report({
    message: 'Failed to revoke preview URL',
    context: 'UploadSection.handleParentUpload',
    severity: 'low',
    cause: e,
  });
}
```

**Key point:** This is `low` severity — no toast is shown. The report exists solely for dev-mode console logging and telemetry completeness. The user is never interrupted for a `revokeObjectURL` failure.

---

**END OF SPEC**

**Next step:** CEO approval required. Upon approval, FE Lead implements Phase 1. QA Lead reviews Phase 1 tests before Phase 2 begins.
