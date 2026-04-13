# Phase 1 Critical Fixes — Execution Master Plan
**Date:** 2026-04-07
**Orchestrator:** This document

---

## Execution Map

```
STEP 1 — PARALLEL (launch all 4 simultaneously)
├── FE Lead Alpha    → tasks/KS01_fe_alpha.md    → CharacterPicker + characters/index.js
├── FE Lead Beta     → tasks/KS02_fe_beta.md     → OrderSuccessPage.jsx
├── FE Lead Gamma    → tasks/UP01_fe_gamma.md    → FacePicker.jsx
└── FE Lead Delta    → tasks/NV03_fe_delta.md    → ErrorBoundary.jsx

STEP 2 — SEQUENTIAL (while parallel runs, or after)
└── Platform Architect → tasks/ST01_arch_fe_epsilon.md (Step 1: assessment)
        ↓
    CEO GATE (approve scope)
        ↓
    FE Lead Epsilon → tasks/ST01_arch_fe_epsilon.md (Step 3: implement)

STEP 3 — AFTER ALL ABOVE COMPLETE
└── QA Lead → tasks/QA_validation_phase1.md

STEP 4 — AFTER QA SIGNS OFF
└── Change Manager → tasks/CM_closeout_phase1.md

STEP 5 — CEO
└── Device verification (3 items) → mark as VERIFIED → approve release
```

---

## How to Launch Each Agent in Claude Code

For each parallel agent, inject the task briefing as the agent's TASK section:

```
Load persona: crew/agents/fe_lead.md
Inject task: crew/tasks/KS01_fe_alpha.md [for Alpha]
             crew/tasks/KS02_fe_beta.md  [for Beta]
             crew/tasks/UP01_fe_gamma.md [for Gamma]
             crew/tasks/NV03_fe_delta.md [for Delta]
Working directory: C:\Users\wole\Documents\FML\famililook-desktop2
```

For the sequential track:
```
Load persona: crew/agents/platform_architect.md
Inject task: crew/tasks/ST01_arch_fe_epsilon.md (Step 1 only)
```

---

## File Boundary Enforcement

Each agent may ONLY edit files in their working set. Zero overlap:

| Agent | Allowed files |
|-------|--------------|
| Alpha | assets/characters/index.js, CharacterPicker.jsx |
| Beta | OrderSuccessPage.jsx |
| Gamma | FacePicker.jsx |
| Delta | ErrorBoundary.jsx |
| Epsilon | useKinshipAnalysis.jsx (after gate) |

If any agent needs a file outside their set → STOP and escalate. Do not proceed.

---

## CEO Checkpoints

| Checkpoint | When | What you decide |
|-----------|------|----------------|
| Per-edit approvals (×N) | During each agent's work | Approve each diff preview |
| ST-01 gate | After Platform Architect assessment | Approve scope (A/B/C) |
| QA sign-off review | After QA validates | Review verdict, note any conditionals |
| Device verification | After QA sign-off | Test 3 items on physical device |
| Release approval | After device verification | Merge to main → production |

---

## What Success Looks Like

All 5 critical findings from the audit eliminated:
- KS-01: Character mug no longer crashes on gran_loving_african
- KS-02: Order success page no longer shows "Something went wrong" when payment succeeded
- UP-01: FacePicker crop failure shows error toast, modal stays open
- NV-03: Private browser no longer loops infinitely on chunk error
- ST-01: Cancelled analysis no longer overwrites fresh analysis result

Full test suite passing. Clean build. 6 files changed. Architecture migration candidates logged for next sprint.
