# Workflow: Sprint Planning & Execution
# Command: `/crew sprint`
# Agents: coo, change_manager, qa_lead, fe_lead
# Execution: Sequential with CEO gates

---

## Prerequisites

Before a sprint can start:
- Sprint plan must exist (e.g., `SPRINT_PLAN_CONSOLIDATED.md` or equivalent)
- Previous sprint's items must be verified as complete or carried over
- Pre-sprint checklist must be satisfied (backups, working set, hooks)

---

## Phase 1: Sprint Setup — COO

**Agent:** `coo`
**Action:**
1. Read the sprint plan and identify the current sprint
2. Verify pre-sprint checklist items are complete:
   - [ ] Dist backup (if applicable)
   - [ ] Backend permission (if sprint touches backend)
   - [ ] Change log exists in target repos
   - [ ] Pre-commit hooks installed in target repos
   - [ ] Rollback strategy documented
   - [ ] Working set cleared from prior sprint
3. Compile sprint scope: items, products, estimated effort, dependencies
4. Identify any items requiring CEO decisions before work begins
5. Write Sprint Briefing to `crew/output/sprint_<N>_briefing.md`

**Output:** Sprint Briefing
```
═══════════════════════════════════════════════
  SPRINT <N> BRIEFING — <date>
═══════════════════════════════════════════════

SPRINT GOAL: <1-sentence goal>
DURATION: <dates>
PRODUCTS: <desktop2, desktop4, desktop6>

ITEMS:
  1. <ID> — <title> — <effort> — <product>
  2. ...

PRE-SPRINT CHECKLIST:
  [x] <item> — DONE
  [ ] <item> — BLOCKED: <reason>

DEPENDENCIES:
  - <item X> must complete before <item Y>

CEO DECISIONS NEEDED:
  - <decision>

RISKS:
  - <risk> — <mitigation>
═══════════════════════════════════════════════
```

**Gate (if CEO decisions needed):**
```
GATE: sprint_approval
AGENT: coo
DECISION NEEDED: Approve Sprint <N> scope and resolve open decisions?
ITEMS: <count> items across <count> products
EFFORT: <total estimate>
DECISIONS:
  1. <decision needed> — Options: A|B — Recommended: <X>
RECOMMENDATION: approve
ARTIFACTS: crew/output/sprint_<N>_briefing.md
```

### Handoff: coo -> change_manager

**Task**: Set up governance for the sprint
**Context**: Sprint scope approved, checklist verified
**Artifacts**: `crew/output/sprint_<N>_briefing.md`
**Decisions Made**: Sprint items, scope, CEO decisions
**Open Questions**: None

---

## Phase 2: Governance Setup — Change Manager

**Agent:** `change_manager`
**Action:**
1. Update `.claude/working_set.txt` with ALL files in sprint scope
2. Run `python .claude/validate_scope.py` for each target file
3. Classify risk tier for the overall sprint
4. Create sprint Change Request Package covering all items
5. Verify change_log.md exists in each target repo
6. Write to `crew/output/sprint_<N>_change_request.md`

**Output:** Sprint Change Request Package (same format as bug_fix, but covering all items)

### Handoff: change_manager -> qa_lead

**Task**: Assess all sprint items for testability and regression risk
**Context**: Working set updated, scope validated, risk classified
**Artifacts**: Sprint briefing + change request
**Decisions Made**: File scope, risk tiers
**Open Questions**: Test strategy, acceptance criteria per item

---

## Phase 3: QA Planning — QA Lead

**Agent:** `qa_lead`
**Action:**
1. For each sprint item:
   a. Read affected source files
   b. Confirm the failure mode / expected behaviour
   c. Define acceptance criteria
   d. Identify regression risks
   e. Define test cases
2. Write Sprint QA Plan to `crew/output/sprint_<N>_qa_plan.md`

**Output:** Sprint QA Plan
```
═══════════════════════════════════════════════
  SPRINT <N> QA PLAN
═══════════════════════════════════════════════

PER-ITEM ASSESSMENT:

## <bug_id>: <title>
ROOT CAUSE: <file:line>
ACCEPTANCE CRITERIA:
  1. <criterion>
TEST CASES:
  1. <test>
REGRESSION RISKS:
  - <risk>

[repeat for each item]

CROSS-CUTTING TESTS:
  - npm run test:run (desktop2) — must pass
  - npm run build (desktop2) — must succeed
  - [per-repo as applicable]
═══════════════════════════════════════════════
```

### Handoff: qa_lead -> fe_lead

**Task**: Implement all sprint fixes
**Context**: Scope validated, acceptance criteria defined, regression risks identified
**Artifacts**: Sprint briefing + change request + QA plan
**Decisions Made**: Root causes, acceptance criteria, test strategy
**Open Questions**: Implementation approach per item

---

## Phase 4: Implementation — FE Lead

**Agent:** `fe_lead`
**Action:**

For each sprint item (ordered by dependency graph):
1. Read all affected files
2. Prepare exact diffs
3. Present each diff to CEO for approval (per CLAUDE.md mandatory pre-edit checklist)
4. Apply approved edits
5. Run tests + build after each logical group of changes

After ALL items implemented:
1. Run full test suite: `npm run test:run` per affected repo
2. Run full build: `npm run build` per affected repo
3. Update `.claude/change_log.md` with all changes
4. Write implementation report to `crew/output/sprint_<N>_fe_implementation.md`

**Gate (per edit):**
```
GATE: edit_approval
AGENT: fe_lead
FILE: <file_path>
OLD: <old_string>
NEW: <new_string>
EXPLANATION: <what and why>
```

**Output:** Sprint Implementation Report (all items, all diffs, test results, build results)

### Handoff: fe_lead -> qa_lead

**Task**: Verify all sprint items meet acceptance criteria
**Context**: All fixes implemented, tests passing, builds succeeding
**Artifacts**: Sprint implementation report + QA plan (criteria to verify against)
**Decisions Made**: All implementations applied
**Open Questions**: Do all fixes meet criteria? Any regressions?

---

## Phase 5: Verification — QA Lead

**Agent:** `qa_lead`
**Action:**
1. Re-read all changed files
2. Verify each item's acceptance criteria
3. Check all regression risks
4. Verify tests and build status
5. Write Sprint Verification Report to `crew/output/sprint_<N>_qa_verification.md`

**Output:** Sprint Verification Report
```
═══════════════════════════════════════════════
  SPRINT <N> VERIFICATION
═══════════════════════════════════════════════

PER-ITEM RESULTS:

## <bug_id>: <title>
  1. <criterion> — PASS/FAIL
  2. <criterion> — PASS/FAIL
  REGRESSION: CLEAR / <issue found>

CROSS-CUTTING:
  Tests (desktop2): <count> passing
  Build (desktop2): PASS
  Tests (desktop4): <count> passing
  Build (desktop4): PASS

VERDICT: ALL PASS / <N> ITEMS NEED REWORK
═══════════════════════════════════════════════
```

If any items FAIL: handoff back to fe_lead for rework (loop Phase 4-5).

### Handoff: qa_lead -> change_manager

**Task**: Close the sprint
**Context**: All items verified
**Artifacts**: All prior artifacts + verification report
**Decisions Made**: All fixes verified
**Open Questions**: None

---

## Phase 6: Sprint Close — Change Manager

**Agent:** `change_manager`
**Action:**
1. Verify all artifacts exist and are complete
2. Update `.claude/change_log.md` with all sprint items (CLOSED status)
3. Update FMEA statuses for all fixed items
4. Reset `.claude/working_set.txt`
5. Write Sprint Summary to `crew/output/sprint_<N>_summary.md`
6. Compile Unified Change Register entries for all items

**Output:** Sprint Summary
```
═══════════════════════════════════════════════
  SPRINT <N> SUMMARY — <date>
═══════════════════════════════════════════════

ITEMS COMPLETED: <N> of <N>
ITEMS DEFERRED: <N> (with reasons)

CHANGE REGISTER:
| Timestamp | Repo | Type | Description | Ref | Tier | Approved | Status |
|-----------|------|------|-------------|-----|------|----------|--------|
| ... | ... | ... | ... | ... | ... | CEO | CLOSED |

FMEA UPDATES:
  - <FMEA-ID>: Open -> FIXED
  - <FMEA-ID>: Open -> FIXED

NEXT: Sprint <N+1> ready to begin
═══════════════════════════════════════════════
```

---

## Sprint Execution Rules

1. **No skipping phases.** Every sprint runs all 6 phases even for XS items.
2. **CEO gates every edit.** Per CLAUDE.md, no auto-edits. FE Lead presents diffs, CEO approves.
3. **Tests must pass.** If tests fail after implementation, FE Lead fixes before QA verification.
4. **No regression.** QA Lead checks all identified regression risks. Any regression = rework.
5. **Change log is append-only.** Change Manager never overwrites prior entries.
6. **Backend requires permission.** Any backend-touching item triggers a CEO gate at Phase 1.
7. **Batch efficiency.** When multiple items share a file, FE Lead groups diffs per file, one gate per file.

---

*Workflow: sprint.md v1.0 — 2026-03-31*
