# CHANGE REQUEST -- CR-0008

---

## RISK TIER: P1 (Significant)

**CHANGE TYPE**: Code
**SOURCE**: Sprint 0A -- FamiliMatch Source Restoration (FE Lead + QA Lead agents)
**DATE**: 2026-03-31
**PREPARED BY**: Change & Release Manager

---

## DESCRIPTION

Full source restoration of the FamiliMatch frontend (famililook-desktop6). 15 new files spanning entry point, build config, state management, UI components, and utilities. This rebuilds the FamiliMatch experience from the current desktop6 skeleton (which has 9 existing source files: 3 pages, 2 hooks, 1 API client, 1 analytics util, 2 components).

**What this is NOT:**
- No backend changes (desktop3/desktop7 untouched)
- No frozen contract changes (compare_faces.v1 remains intact)
- No pricing or revenue model changes
- No new dependencies or supplier integrations

## CONTEXT

FamiliMatch is deployed at famililook-desktop6.vercel.app but the source tree is incomplete -- missing core infrastructure files (index.html, vite.config.js, main.jsx, App.jsx), state management (ConsentContext, MatchContext), user-facing components (consent modal, photo upload, onboarding, feature scan animation, results story, room lobby, countdown overlay), and shared utilities (config, constants). This sprint restores these files to make the codebase maintainable and complete.

**Traceability**: Sprint 0A -- FamiliMatch Source Restoration (initiated 2026-03-31)

## ACTION

Create 15 new files in famililook-desktop6:

### Entry Point & Config (4 files)
| File | Purpose | Status |
|------|---------|--------|
| `index.html` | Vite HTML entry point | NEW |
| `vite.config.js` | Vite build configuration | NEW |
| `src/main.jsx` | React DOM root mount | NEW |
| `src/App.jsx` | Router + context providers + page layout | NEW |

### State Management (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `src/state/ConsentContext.jsx` | GDPR/biometric consent state | NEW |
| `src/state/MatchContext.jsx` | Match session state (photos, results, room) | NEW |

### Components (7 files)
| File | Purpose | Status |
|------|---------|--------|
| `src/components/ConsentModal.jsx` | Consent collection UI | NEW |
| `src/components/PhotoUpload.jsx` | Face photo upload + preview | NEW |
| `src/components/OnboardingScreen.jsx` | First-time user onboarding flow | NEW |
| `src/components/FeatureScanAnimation.jsx` | Animated feature comparison visualization | NEW |
| `src/components/ResultsStory.jsx` | Match results narrative display | NEW |
| `src/components/RoomLobby.jsx` | Multi-user room waiting area (Duo/Group) | NEW |
| `src/components/CountdownOverlay.jsx` | Countdown before reveal | NEW |

### Utilities (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `src/utils/config.js` | API URLs, feature flags, environment config | NEW |
| `src/utils/constants.js` | Shared constants (thresholds, labels, colors) | NEW |

---

## VALIDATION CHECKLIST

| # | Check | Status | Detail |
|---|-------|--------|--------|
| 1 | Traceability | PASS | Sprint 0A -- FamiliMatch Source Restoration |
| 2 | Format | PASS | D/C/A format in desktop6/.claude/change_log.md |
| 3 | ops_report | N/A | No ops_agents involved (native crew execution) |
| 4 | Tests | PENDING | Tests to run after implementation (98 existing Vitest) |
| 5 | Contract impact | PASS -- NONE | compare_faces.v1 is frozen and untouched. No backend files modified. |
| 6 | Blast radius | 15 files, single repo (desktop6 only) | No cross-repo impact. Existing 9 source files not modified in this CR. |
| 7 | Working set | PASS | .claude/working_set.txt updated with all 15 files |
| 8 | Scope validation | PASS | validate_scope.py returns exit 0 for all 15 files |
| 9 | Approval chain | PENDING | P1 requires CEO sign-off |
| 10 | Rollback plan | LOW RISK | All 15 files are new additions. Rollback = delete the 15 files. No existing code is modified. |

---

## RISK ASSESSMENT

**Why P1 (not P2):**
- Multi-file change (15 files)
- Partial rewrite scope (rebuilding core FE infrastructure)
- Affects a live deployed product (famililook-desktop6.vercel.app)

**Mitigating factors:**
- All files are NEW (no existing code modified)
- No backend changes
- No frozen contract changes
- No pricing/revenue impact
- No new dependencies
- Simple rollback (delete new files)
- Existing 9 source files remain untouched
- 98 existing Vitest tests provide regression coverage

---

## EXECUTION PLAN

1. FE Lead agent implements all 15 files per existing desktop6 patterns
2. QA Lead agent verifies: existing 98 tests still pass, build succeeds, no contract violations
3. Change Manager logs completion in desktop6/.claude/change_log.md
4. CEO reviews and approves deployment

---

## RECOMMENDATION: APPROVE

All 15 files are new additions with zero modification to existing code. No contract, backend, or pricing impact. Rollback is trivial (delete new files). The restoration completes the desktop6 source tree for maintainability.

**CONDITIONS**: None. Standard P1 execution with test verification before merge.

---

**Prepared by**: Change & Release Manager
**Date**: 2026-03-31
**Awaiting**: CEO approval to proceed to Phase 3 (implementation)
