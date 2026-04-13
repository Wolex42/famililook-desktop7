# Execution Plan — FML Platform Objectives
**Author:** COO (Claude Code native persona)
**Date:** 2026-04-14
**Status:** APPROVED (2026-04-14) — two CEO amendments applied

**Amendment 1:** Web relaunch first. Sprint F (mobile) follows relaunch, not before it.
**Amendment 2:** Sprint E runs in parallel with Sprint B. Backend permission granted explicitly at start of each Sprint E session.

---

## Current State (verified, not recalled)

| Metric | Value |
|--------|-------|
| desktop2 tests | 1,444 (quality floor) |
| desktop6 tests | 51 |
| desktop3 backend tests | 173 passed, 2 xpassed |
| Build | PASS |
| Structural modules | All 3 BUILT in desktop2 |
| famililook-shared | SCAFFOLDED + AppErrorBus extracted (Phase 2 complete) |
| famililook-game-engine | SCAFFOLDED (empty) |
| desktop4/desktop6 wired to shared | NO |
| HIGH audit items open | 7 of 18 |
| AppLayout.jsx | 1,094 lines, 20 patches in 30 days — redesign candidate |
| ESLint Phase 4 rules | 1 of 3 active (AppStorage only) |
| Desktop6 E2E tests | NONE |
| Mobile/Capacitor | NOT STARTED |

---

## The Eight Objectives

| # | Objective | Shorthand |
|---|-----------|-----------|
| 1 | Complete famililook-shared — Phase 3 (AppStorage), Phase 4 (resultsContract), wire desktop4/6 | SHARED-PKG |
| 2 | Complete famililook-game-engine — extract rooms + protocol from desktop5/7 | GAME-ENGINE |
| 3 | iOS/Android readiness — Mobile Solutions Architect assessment, Capacitor, submission | MOBILE |
| 4 | Phase 2 audit fixes — 7 HIGH severity items still open | AUDIT-HIGH |
| 5 | Three ESLint Phase 4 rules — lock AppErrorBus, resultsContract, AppStorage gates | ESLINT-GATES |
| 6 | AppLayout.jsx decomposition — 1,094 lines, 20 patches, redesign candidate | APPLAYOUT |
| 7 | FamiliMatch buildout — desktop6 depth, E2E tests, viral solo hardening | MATCH-BUILD |
| 8 | Lift maintenance mode and relaunch | RELAUNCH |

---

## Q1: Which objectives are blocked by other objectives?

| Objective | Blocked by | Reason |
|-----------|-----------|--------|
| SHARED-PKG Phase 3 | Phase 2 ✅ DONE | AppStorage imports AppErrorBus — must be in shared package first |
| SHARED-PKG Phase 4 | Phase 3 | resultsContract consumers also import AppStorage — one migration pass |
| SHARED-PKG wire desktop4/6 | Phase 4 | All 3 modules must be in package before wiring other consumers |
| GAME-ENGINE | CEO backend permission | .py files require explicit per-session permission |
| MOBILE | SHARED-PKG + APPLAYOUT | Shared package must be stable before wrapping in Capacitor. AppLayout must be decomposed — 1,094 lines of monolithic shell cannot be the mobile entry point |
| ESLINT-GATES | SHARED-PKG Phase 4 | ESLint import paths change when modules move to shared package. Rules must target final paths |
| APPLAYOUT | SHARED-PKG Phase 3 | AppLayout imports AppStorage (12 calls) and AppErrorBus. Extract first, decompose second |
| MATCH-BUILD | SHARED-PKG wire desktop6 | Desktop6 should consume shared infrastructure before new feature work |
| RELAUNCH | ALL of the above | Cannot relaunch with 7 HIGH audit items, no E2E on desktop6, monolithic AppLayout, and incomplete shared infrastructure |

---

## Q2: Which objectives can run in parallel?

| Parallel pair | Why independent |
|---------------|----------------|
| GAME-ENGINE + SHARED-PKG | Backend (.py) vs frontend (.js) — different repos, different languages, zero overlap |
| AUDIT-HIGH (partial) + SHARED-PKG | Some HIGH fixes (UP-03 timeout, KS-04 checkout) touch files NOT involved in extraction |
| MATCH-BUILD (planning) + SHARED-PKG | Visual Director + Copywriter can spec FamiliMatch improvements while extraction runs |

**Cannot run in parallel:**
- SHARED-PKG phases are strictly sequential (2→3→4→wire)
- ESLINT-GATES must follow SHARED-PKG completion
- APPLAYOUT must follow SHARED-PKG Phase 3
- MOBILE must follow APPLAYOUT
- RELAUNCH is the terminal node

---

## Q3: Optimal Execution Sequence

Given constraints: max 2 phases per session, quality floor 1,444, CEO approves all diffs.

### Sprint A — Shared Package Completion (3 sessions)

| Session | Phases | Lead Agent | What |
|---------|--------|-----------|------|
| A1 | Phase 3 | Shared Infra Lead → FE Lead | AppStorage extraction (862 lines, 47 consumer imports). Delete AppErrorBus shim. |
| A2 | Phase 4 + wire desktop4 | Shared Infra Lead → FE Lead | resultsContract extraction (365 lines, 5 consumers). Wire desktop4 `file:` dependency. |
| A3 | Wire desktop6 + vitest config | FE Lead | Wire desktop6 `file:` dependency. Add vitest config to famililook-shared. Run shared package tests standalone. |

**Quality gates per session:** desktop2 ≥ 1,444 tests + build PASS. Shared package tests run in isolation.

### Sprint B — Audit Fixes + ESLint Gates (2 sessions)

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| B1 | 4 of 7 HIGH audit fixes | Platform Architect → FE Lead | KS-03 (BasketContext storage), UP-03 (quality timeout), KS-04 (checkout timeout), NV-02 (route error boundaries) |
| B2 | 3 of 7 HIGH fixes + 3 ESLint rules | Platform Architect → FE Lead | ST-02 (plan staleness), GM-01 (buildDeck failure), XD-01 (multi-tab sync). Then: `no-bare-catch`, `no-inline-results-logic`, `no-direct-localstorage` path updates |

**Why audit before AppLayout:** Several HIGH fixes touch files inside AppLayout's scope. Fix the bugs in the current structure, then decompose. Decomposing first moves bugs into new files — harder to track.

### Sprint C — AppLayout Decomposition (2 sessions)

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| C1 | Platform Architect redesign spec | Platform Architect | Read full 1,094-line file. Produce decomposition spec: which responsibilities extract to which new files. Identify state lifting requirements. |
| C2 | FE Lead implements decomposition | FE Lead | Execute spec. Target: AppLayout.jsx < 200 lines (shell + router only). Extract: BottomNav, SettingsTab, DrawerHost, ConsentLayer, AnalyticsInit |

**Gate:** Platform Architect spec must be CEO-approved before FE Lead touches AppLayout.

### Sprint D — FamiliMatch Buildout (2 sessions)

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| D1 | Playwright E2E setup + solo flow hardening | FE Lead + QA Lead | Install Playwright in desktop6. Write E2E tests for solo flow. Harden viral share UX. |
| D2 | Duo/Group depth + shared infra consumption | FE Lead | Wire desktop6 to consume shared AppErrorBus, AppStorage, resultsContract. Add depth to Duo/Group modes. |

### Sprint E — Game Engine Extraction (1-2 sessions)

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| E1 | Phase 5a-5f | Game Engine Architect → BE Lead | Extract shared rooms.py + protocol.py. Update desktop5. Requires CEO backend permission. |
| E2 | Phase 5g-5j | BE Lead | Update desktop7. Run all backend tests. |

**This sprint can run in parallel with Sprints B-D** if CEO grants backend permission.

### Sprint F — Mobile Readiness (2-3 sessions)

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| F1 | Mobile Solutions Architect assessment | Mobile Solutions Architect | TF.js WebGL, localStorage→AppStorage (done), WebSocket WSS, camera plugin, status bar. Produce readiness report. |
| F2 | Capacitor init + iOS build | Native App Lead | `npx cap init`, configure iOS, TestFlight internal build. |
| F3 | Android build + submission prep | Native App Lead | Configure Android, Google Play Internal Testing. |

**Gate:** Mobile Solutions Architect report must be CEO-approved before Capacitor init.
**Gate:** CEO device verification on physical phone before any store submission.

### Sprint G — Relaunch

| Session | Task | Lead Agent | What |
|---------|------|-----------|------|
| G1 | Pre-launch checklist + lift maintenance | COO + QA Lead | All HIGH fixes resolved. All ESLint gates active. AppLayout decomposed. E2E on desktop6. Shared infrastructure complete. CEO sign-off. |

---

## Q4: Critical Path to Lifting Maintenance Mode

```
Phase 2 ✅ DONE
    │
    ▼
Phase 3 (AppStorage extraction) ──── Session A1
    │
    ▼
Phase 4 + wire desktop4 ──────────── Session A2
    │
    ▼
Wire desktop6 ────────────────────── Session A3
    │
    ├──────────────────────┐
    ▼                      ▼
7 HIGH audit fixes    ESLint gates ── Sessions B1-B2
    │                      │
    ├──────────────────────┘
    ▼
AppLayout decomposition ──────────── Sessions C1-C2
    │
    ▼
FamiliMatch E2E + depth ──────────── Sessions D1-D2
    │
    ▼
Mobile readiness (if before relaunch) ── Sessions F1-F3
    │
    ▼
RELAUNCH ─────────────────────────── Session G1
```

**Critical path length:** 12-14 sessions minimum.

**Shortest path to web relaunch (no mobile):** A1 → A2 → A3 → B1 → B2 → C1 → C2 → D1 → G1 = **9 sessions**

Mobile (Sprint E + F) can follow relaunch if CEO prefers web-first.

---

## Q5: Which objectives require backend permission?

| Objective | Backend files | Permission needed |
|-----------|--------------|-------------------|
| GAME-ENGINE (Sprint E) | desktop5/*.py, desktop7/*.py, famililook-game-engine/*.py | YES — explicit CEO per-session |
| AUDIT-HIGH item NV-02 | May touch main.jsx routing (frontend only) | NO |
| AUDIT-HIGH item ST-02 | usePlanFeatures.js (frontend) | NO |
| All other objectives | Frontend only | NO |

**Only Sprint E requires backend permission.** All other sprints are frontend-only.

---

## Q6: Which objectives have protected files in scope?

| Objective | Protected files | Review needed |
|-----------|----------------|---------------|
| SHARED-PKG Phase 3 | AppStorage.js (structural module) | Platform Architect — converting to shim |
| SHARED-PKG Phase 4 | resultsContract.js (structural module) | Platform Architect — converting to shim |
| AUDIT-HIGH KS-03 | BasketContext.jsx (BLOCKED FILE) | Platform Architect + CEO |
| AUDIT-HIGH ST-02 | usePlanFeatures.js (BLOCKED FILE) | Platform Architect + CEO |
| AUDIT-HIGH XD-01 | Multi-tab sync touches AppStorage domain | Platform Architect |
| APPLAYOUT | AppLayout.jsx (20 patches — redesign, not patch) | Platform Architect full redesign spec |
| ESLINT-GATES | ESLint config (governance file) | Platform Architect |

**6 of 8 objectives touch at least one protected file.** Platform Architect is the most activated agent across this plan.

---

## Session Dependency Matrix (visual)

```
         A1   A2   A3   B1   B2   C1   C2   D1   D2   G1
A1 (P3)   ●
A2 (P4)   ←─   ●
A3 (wire)      ←─   ●
B1 (audit)          ←─   ●
B2 (audit+ESL)           ←─   ●
C1 (spec)                     ←─   ●
C2 (decomp)                        ←─   ●
D1 (match)          ←─                        ●
D2 (match)                                    ←─   ●
G1 (launch)                   ←────────────────────  ●

E1-E2 (game engine) — parallel track, independent of A-D
F1-F3 (mobile) — after C2, can be post-relaunch
```

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AppStorage 47-file migration introduces import typo | Low | High (app crash) | Mechanical find-replace + full test suite at each step |
| AppLayout decomposition breaks navigation | Medium | High | Platform Architect spec first. Every route tested. Back-button scenarios verified. |
| ESLint rule false positives block development | Medium | Medium | Rules target exact patterns. Exemption comments for known exceptions. |
| Desktop6 E2E setup takes longer than 1 session | Medium | Low | Solo flow E2E first (highest value). Duo/Group E2E in follow-up. |
| Game engine extraction breaks WebSocket protocol | Low | High | Standardise on desktop7 envelope (CEO Decision 2). All 148 backend tests must pass. |
| Mobile assessment reveals blocking WebGL issue | Medium | High | Assessment happens in Sprint F — before any Capacitor code. If blocked, defer mobile. |

---

## CEO Decision Points (upcoming)

| # | Decision | When | Options |
|---|----------|------|---------|
| 1 | Approve this execution plan | NOW | Approve / Redirect / Reprioritise |
| 2 | Web-first relaunch vs mobile-included? | Before Sprint F | A: Web relaunch first, mobile follows. B: Hold relaunch for mobile. |
| 3 | Backend permission for Sprint E | Start of E1 | Grant per-session |
| 4 | AppLayout decomposition spec approval | Gate at C1 | Approve Platform Architect spec |
| 5 | Lift maintenance mode | Gate at G1 | CEO sign-off |

---

## Recommendation

**Approve the plan as sequenced.** The critical path is clear: finish the shared package (3 sessions), fix the 7 HIGH audit items (2 sessions), decompose AppLayout (2 sessions), harden FamiliMatch (2 sessions), then relaunch. Game engine extraction runs as a parallel track whenever backend permission is granted. Mobile follows relaunch unless CEO wants to bundle it.

**First action after approval:** Begin Session A1 — Phase 3 AppStorage extraction per SHARED_INFRA_MIGRATION_2026_04_13.md Section 3.

---

_This execution plan is a GATE. No implementation work begins until the CEO approves, redirects, or reprioritises._
