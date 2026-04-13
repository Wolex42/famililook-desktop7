# Lessons Learnt — FML Platform Development
**Period:** 2026-03-31 to 2026-04-02
**Author:** CEO Review + Agent Team Analysis
**Purpose:** Prevent recurrence, raise standards, build robustness

---

## Lesson 1: CSS Hiding Is Not Structural Removal

**Incident:** Sprint 4A agents used `display: none` to hide age cards on mobile. Tests passed. Build passed. The fix didn't work on real phones because `isMobile` JavaScript check was unreliable.

**Root Cause:** Agents treated "visually hidden" as "fixed". CSS hiding depends on runtime conditions (viewport measurement timing, modal container width vs window width). Structural removal from the render tree (`{!isMobile && (...)}`) is deterministic.

**Standard Raised:**
- **Rule:** Never use `display: none` for responsive layout changes. Use conditional rendering to remove elements from the React tree.
- **Verification:** After any mobile UI fix, grep for the element and verify it only exists inside conditional blocks.
- **Memory:** `feedback_agent_visual_verification.md`

---

## Lesson 2: Missing Imports Pass Build But Crash at Runtime

**Incident:** PlansPage.jsx used `useCallback` without importing it. `npm run build` passed. `npm run test:run` passed. Every user navigating to /plans saw the ErrorBoundary crash.

**Root Cause:** Vite tree-shakes unused code at build time. If a hook is used inside a function that Vite doesn't statically analyse as a top-level call, the build succeeds but the runtime throws `ReferenceError`. Tests only catch this if the specific component is rendered in a test.

**Standard Raised:**
- **Rule:** After editing ANY file's imports, run a blast radius scan: grep for every React hook usage in that file and verify the import line includes it.
- **Rule:** Every user-reachable page/route should have at least one render test that would catch missing imports.
- **Pre-deploy gate:** Add "hook import verification" to the blast radius scan checklist.
- **Memory:** `feedback_flawless_navigation.md`

---

## Lesson 3: Every Deploy Breaks Cached Users

**Incident:** Every Vercel deployment changed chunk hashes. Users with cached `index.html` referenced old chunk filenames that no longer existed. "Failed to fetch dynamically imported module" crashed the app.

**Root Cause:** No explicit `Cache-Control` header on `index.html`. Vercel's default was ambiguous. Browser cached the HTML, which pointed to stale JS chunks.

**Standard Raised:**
- **Rule:** `index.html` must ALWAYS have `no-cache, no-store, must-revalidate`. Hashed assets keep `immutable` 1-year cache.
- **Rule:** `lazyWithReload` must cache-bust on reload (`?_cb=timestamp`) and return a never-resolving promise during reload to prevent React rendering stale state.
- **Preventive action:** This is now Layer 6 in the Master Regression Matrix (Deployment Cache Headers).

---

## Lesson 4: Print Templates Are Not Mobile Previews

**Incident:** Mug templates (830px for print production) were CSS-scaled to 0.41x on 375px phones. Text became illegible. Multiple patch attempts (0.7x scale, horizontal scroll, display:none on selectors) each introduced new issues.

**Root Cause:** The keepsake system was designed as a print-export pipeline that shows previews, not as a mobile shopping experience. Shrinking a print layout into a phone screen will never work regardless of scaling approach.

**Standard Raised:**
- **Rule:** Mobile product previews should show PRODUCT MOCKUPS (how the item looks in real life), not scaled-down print layouts.
- **Rule:** When a design problem requires more than 2 patch attempts, stop patching and redesign the architecture. The mobile keepsake flow was correctly redesigned as 3 full-screen pages with a parallel component tree.
- **Preventive action:** Visual Director and Copywriter must spec visual fixes BEFORE FE Lead implements. No ad-hoc graphic design decisions in code.

---

## Lesson 5: Single File Owner Per Sprint

**Incident:** KeepsakesModal.jsx was edited by Sprint 4A agent, post-sprint agent, and mobile audit agent. Each added patches on top of patches. The file grew to 1800+ lines with conflicting mobile detection approaches (`isMobile`, `overlayMobile`, `mobile`, `compact`).

**Root Cause:** No ownership boundary. Multiple agents edited the same file across different sessions without reading the full context of previous changes.

**Standard Raised:**
- **Rule:** One agent owns a file for the duration of a sprint/task. Other agents can READ but not EDIT.
- **Rule:** If a file exceeds 500 lines and handles both desktop and mobile, split it into separate components.
- **Preventive action:** The keepsake mobile flow is now a parallel component tree (`mobile/`) — desktop modal is untouched.

---

## Lesson 6: Agents Must Not Self-Certify Visual Fixes

**Incident:** Agents marked MOB-05/06/07/08 as "FIXED" based on code change + test pass. The fixes didn't work on real phones. The CEO had to test and report back.

**Root Cause:** No visual verification capability. Agents can read/write code and run tests but cannot render the app on a phone simulator. "Tests pass" ≠ "visually fixed".

**Standard Raised:**
- **Rule:** For ANY mobile UI fix, agents must say "applied but UNVERIFIED on device" — never mark as FIXED until CEO confirms on a real device.
- **Rule:** Add the component to a Playwright test that renders at 375px and checks for specific DOM presence/absence.
- **Preventive action:** Acceptance criteria must include a device verification step owned by the CEO.

---

## Lesson 7: Design Agents Must Spec Before Engineering Agents Implement

**Incident:** FE Lead was making graphic design decisions about text sizing, backing colours, and layout adjustments on mug templates. These are Visual Director and Copywriter responsibilities.

**Root Cause:** The workflow skipped design agents and went straight to code. No spec meant the FE Lead guessed at visual values.

**Standard Raised:**
- **Rule:** The `/crew fix` workflow for visual issues must include Visual Director (colour/layout spec) and Copywriter (text constraints) BEFORE FE Lead implements.
- **Rule:** FE Lead implements EXACTLY to spec — no ad-hoc design decisions.
- **Preventive action:** Updated bug_fix workflow understanding — visual issues route through design agents.

---

## Lesson 8: ErrorBoundary Must Guide, Not Block

**Incident:** ErrorBoundary showed "Something went wrong: useCallback is not defined" with a red "Try Again" button. Try Again just reset React state, which re-crashed immediately. Users were completely stuck.

**Root Cause:** ErrorBoundary was designed to catch and display errors, not to recover from them. The primary action ("Try Again") was wrong for chunk errors — a page refresh was needed.

**Standard Raised:**
- **Rule:** ErrorBoundary's primary action must be "Refresh Page" (clears cached chunks). "Try Again" is secondary.
- **Rule:** Never show raw error messages to users (`useCallback is not defined` is meaningless to them). Show "Something went wrong. This usually resolves with a page refresh."
- **Preventive action:** ErrorBoundary now has Refresh Page as primary CTA, removes raw error messages.

---

## Lesson 9: Reactive Patching Creates More Problems Than It Solves

**Incident:** The keepsake mobile preview went through 5+ patch attempts (display:none, scale 0.7x, overflow scroll, sticky footer, fixed footer) over multiple sessions. Each patch introduced new issues. The final solution was a full architectural redesign (Option B → 3 full-screen pages).

**Root Cause:** Pressure to deploy fast led to incremental patches instead of understanding the root problem. The root problem was architectural (print pipeline forced into mobile screen), not a CSS bug.

**Standard Raised:**
- **Rule:** If a fix requires more than 2 attempts, STOP. Document the failure modes. Get the QA Lead to do a systemic review. Get the Visual Director to spec a proper solution. Only then implement.
- **Rule:** Never commit a fix to production without the CEO testing on device first (for mobile UI issues).
- **Preventive action:** The orchestrator workflow now requires CEO device sign-off for mobile UI changes.

---

## Lesson 10: Documentation Must Be Updated Atomically With Code

**Incident:** Multiple times the CEO asked "are all docs updated?" and the answer was no. FMEA, Master Matrix, change logs, and memory files were updated as afterthoughts, sometimes missing entirely.

**Root Cause:** Documentation updates were treated as a separate step rather than part of the commit. Agents focused on the code fix and forgot the docs.

**Standard Raised:**
- **Rule:** Every commit that fixes an FMEA item must also update the FMEA status in the SAME session.
- **Rule:** The Change Manager's Step 5 (close) is NOT optional — it must run after every fix, not "later".
- **Rule:** Memory files must be updated before the session ends, not in the next session.
- **Preventive action:** Add documentation checklist to the pre-commit process: FMEA updated? Change log updated? Memory updated?

---

## Operational Improvements Implemented

| Improvement | Where | Status |
|-------------|-------|--------|
| Structural removal over CSS hiding | feedback_agent_visual_verification.md | ACTIVE |
| Blast radius scanning pre-deploy | Master Regression Matrix Layer 5 | ACTIVE |
| No-cache on index.html | vercel.json | DEPLOYED |
| Cache-bust lazyWithReload | lazyWithReload.js | DEPLOYED |
| Pre-commit hook on all FE repos | desktop2/4/6 .git/hooks/ | INSTALLED |
| FMEA regression gate script | scripts/check_fmea_regressions.py | CREATED |
| Mobile keepsake parallel component tree | src/components/keepsakes/mobile/ | DEPLOYED |
| Visual Director specs before FE implementation | Workflow understanding | ACTIVE |
| Cornish Prints UK quality benchmark | reference_cornish_prints.md | SAVED |
| Feature flag kill switch for mobile flow | isMobileKeepsakeFlow() | DEPLOYED |

---

## Standards Checklist (For Every Future Fix)

Before committing ANY change:
- [ ] All React hooks imported? (grep for usage vs import)
- [ ] No `display: none` for responsive hiding? (use conditional rendering)
- [ ] Mobile UI verified on device by CEO? (or marked "unverified")
- [ ] Visual spec from Visual Director? (for visual issues)
- [ ] Copy spec from Copywriter? (for text changes)
- [ ] FMEA updated with new failure mode or status change?
- [ ] Change log appended?
- [ ] Memory files updated?
- [ ] Tests pass + build passes?
- [ ] Blast radius scan clean?

---

*Lessons Learnt v1.0 — 2026-04-02*
*Next review: 2026-04-07 (7-day monitoring sign-off)*
