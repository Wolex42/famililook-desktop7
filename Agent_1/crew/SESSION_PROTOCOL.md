# Session Opening Protocol — FML Platform
**Version:** 1.0 — 2026-04-10
**Status:** MANDATORY — every new Claude Code session must follow this before any work

---

## Why This Exists

New chat sessions start without memory of previous sessions. Without a
structured opening, agents drift — making assumptions, skipping governance
steps, working on the wrong priority, or editing files without the correct
process. This protocol eliminates that drift by ensuring every session
starts from the same known state.

---

## Step 1 — Read These Five Files (in order, completely)

Do not skim. Do not begin work until all five are read.

1. `C:\Users\wole\Documents\FML\CLAUDE.md`
   — The law. Every rule, every constraint, every non-negotiable.

2. `Agent_1/crew/orchestrator.md`
   — The 15 agents, their roles, the workflows, the triage gates.

3. Most recent `Agent_1/crew/output/SESSION_HANDOFF_*.md`
   — What was completed, what is in progress, what comes next.

4. Most recent `Agent_1/crew/output/SESSION_*_START.md` (if exists)
   — Specific instructions for this session's first tasks.

5. `C:\Users\wole\.claude\projects\c--Users-wole-Documents-FML\memory\MEMORY.md`
   — Current platform state, structural modules, test counts.

---

## Step 2 — Answer These Five Questions Before Any Work

Answer from the files you just read. No guessing. If you cannot answer
without guessing, say so and re-read the relevant file.

**Q1:** What is the current test quality floor for desktop2?
*(Expected: a specific number — e.g. 1,444)*

**Q2:** Which structural modules are BUILT vs NOT BUILT?
*(AppErrorBus, AppStorage, resultsContract — each with phase status)*

**Q3:** What is the single highest priority task this session?
*(From the most recent SESSION_HANDOFF Section 5 or SESSION_*_START)*

**Q4:** Which files are on the BLOCKED FILES list?
*(From fe_lead.md Section 4 — list all 6)*

**Q5:** What is the mandatory pre-edit checklist?
*(From CLAUDE.md — list all 6 steps)*

Present answers to CEO. Wait for confirmation before proceeding to Step 3.

---

## Step 3 — Load The Correct Agent Persona

Based on the session's first task, identify which agent persona to load:

| Task type | Lead agent | Support agents |
|-----------|-----------|---------------|
| Code fix or feature | FE Lead | QA Lead, Change Manager |
| Backend work | BE Lead | QA Lead, Change Manager |
| Architecture/structural | Platform Architect | QA Lead |
| Multiplayer/WebSocket | Game Engine Architect | BE Lead |
| Mobile/Capacitor | Mobile Solutions Architect | Native App Lead |
| Analytics | Data Solutions Architect | FE Lead, BE Lead |
| Shared package migration | Shared Infrastructure Lead | FE Lead, BE Lead |
| Governance/documentation | Change Manager | COO |
| Campaign/marketing | CMO | Copywriter, Visual Director |

Read the lead agent's persona file completely before beginning work.
State which persona you have loaded and which workflow applies.

---

## Step 4 — State Session Scope Explicitly

Before the first edit, state:

```
SESSION SCOPE DECLARATION
Agent: <persona loaded>
Task: <exact task from handoff>
Working set: <files that may be edited this session>
Quality floor: <test count — must not drop>
Blocked files in scope: <YES (list) | NONE>
Backend permission needed: <YES (explicit CEO statement required) | NO>
CEO approval required for: <every diff preview — no exceptions>
```

Get explicit CEO confirmation of the scope before proceeding.

---

## Step 5 — Patch Count Check

For every file in the working set, check patch frequency:
```bash
cd C:\Users\wole\Documents\FML\famililook-desktop2
git log --since="30 days ago" --format="%H" -- <file_path> | wc -l
```

- 0-1 patches: proceed normally
- 2 patches: note it, QA Lead triage recommended
- 3+ patches: HALT — route to /crew redesign, do not proceed

Report patch counts to CEO before any edit.

---

## Step 6 — Begin Work

Only after Steps 1-5 are complete:
- Every edit gets a diff preview shown to CEO
- Every edit waits for explicit approval
- Every session ends with change_log updated and commits pushed
- Every session produces a SESSION_HANDOFF document before closing

---

## Common Failure Modes — What To Watch For

These are the patterns that have caused session drift in the past:

| Failure mode | Warning sign | Correct action |
|-------------|-------------|----------------|
| Starting work without reading governance files | Agent makes assumptions about rules | Stop. Read the five files. |
| Working set not updated | validate_scope.py blocks change_log.md | Update working_set.txt first |
| Editing blocked files without waiver | Direct edit of FamililookContext etc | Stop. Request Platform Architect review |
| Bundling multiple session tasks | "Let me also fix..." | One task at a time. Complete and commit before next task |
| Self-certifying mobile fixes | "This should work on device" | Mark UNVERIFIED. CEO confirms on physical phone |
| Documentation after the fact | "I'll update change_log later" | Update in same session. Not later. |
| Session pressure causing shortcuts | Fast edits without diff preview | Slow down. Every edit gets a preview |
| Wrong working directory in git commands | git restore in wrong repo | Always prefix: cd <repo> && git <command> |

---

## Session Close Protocol

Before ending any session:

- [ ] All edits committed and pushed to origin/main
- [ ] change_log.md updated in same session
- [ ] Tests passing at or above quality floor
- [ ] SESSION_HANDOFF document written to `Agent_1/crew/output/`
- [ ] Memory files updated if architecture health changed
- [ ] No uncommitted work left in working tree (or explicitly noted as intentional)

---

## The One-Line Test

Before starting any work, ask:
**"If the CEO asked me right now what I am doing and why, could I answer
with a specific task name, a specific file, and a specific reason from
the handoff document?"**

If yes: proceed.
If no: go back to Step 1.

---

*This protocol exists because sessions without it drift. Sessions with it
deliver. Follow it every time.*
