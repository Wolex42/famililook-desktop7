# Workflow: Bug Fix
# Command: `/crew fix <bug>`
# Agents: change_manager, qa_lead, fe_lead (or be_lead)
# Execution: Sequential with CEO gates

---

## Prerequisites

Before this workflow can execute:
- Bug must be identified with a reference (FMEA ID, issue number, or description)
- The target repo must be known (desktop2, desktop4, desktop6, desktop3)
- If backend file: CEO must have granted explicit permission per CLAUDE.md

---

## Mandatory Standards (from Lessons Learnt)

These standards are NON-NEGOTIABLE for every bug fix. Violations will cause regression.

### Before Implementation (Change Manager verifies):
- [ ] If this is a VISUAL/UI fix: Visual Director must spec colours/dimensions BEFORE FE Lead implements (Lesson 7)
- [ ] If this is a TEXT/COPY fix: Copywriter must spec max lengths BEFORE FE Lead implements (Lesson 7)
- [ ] Blast radius scan: grep for all React hook usage vs imports in every modified file (Lesson 2)

### During Implementation (FE Lead must follow):
- [ ] NEVER use `display: none` for responsive hiding — use `{condition && (...)}` conditional rendering (Lesson 1)
- [ ] NEVER make ad-hoc design decisions — implement EXACTLY to Visual Director/Copywriter spec (Lesson 7)
- [ ] One agent owns a file — if another agent already edited it this session, coordinate or split (Lesson 5)
- [ ] After editing, READ BACK the changed lines to verify acceptance criteria (Lesson 6)

### After Implementation (QA Lead verifies):
- [ ] All React hooks in modified files are imported (Lesson 2)
- [ ] No `display: none` for responsive layout (Lesson 1)
- [ ] Mobile UI fixes: mark "UNVERIFIED on device" until CEO confirms (Lesson 6)
- [ ] If fix attempt > 2 for same issue: STOP, escalate to systemic review (Lesson 9)

### Before Commit (Change Manager verifies):
- [ ] FMEA status updated (Lesson 10)
- [ ] Change log appended (Lesson 10)
- [ ] Memory files updated if applicable (Lesson 10)

---

## Step 1: Change Manager — Scope & Risk Assessment

**Agent:** `change_manager`
**Input:** Bug reference, affected product, target files
**Action:**
1. Update `.claude/working_set.txt` with target files
2. Run `python .claude/validate_scope.py "<file_path>" --mode edit` for each file
3. Classify risk tier:
   - **P3**: Docs-only, test-only, cosmetic — Change Manager auto-approves
   - **P2**: Single-file, low blast radius, no contract impact — log and proceed
   - **P1**: Multi-file, cross-component, or contract-adjacent — CEO approval required
   - **P0**: Contract-breaking, security, compliance, data loss — CEO approval + rollback plan required
4. Check if fix touches backend files → if yes, STOP and flag for CEO permission
5. Write Change Request Package to `crew/output/<bug_id>_change_request.md`

**Output:** Change Request Package
```
═══════════════════════════════════════════════
  CHANGE REQUEST: <bug_id>
═══════════════════════════════════════════════
RISK TIER: P0|P1|P2|P3
CHANGE TYPE: Code|Config|Docs
PRODUCT: <product>
FILES:
  - <file_path> — <what changes>
BLAST RADIUS: <what could break>
CONTRACTS AFFECTED: None | kinship_analyze.v1 | compare_faces.v1
BACKEND CHANGES: Yes/No
ROLLBACK: <strategy>
WORKING SET: Updated ✓
SCOPE VALIDATION: All files ALLOWED ✓
═══════════════════════════════════════════════
```

**Gate (P1/P0 only):**
```
GATE: scope_approval
AGENT: change_manager
DECISION NEEDED: Approve scope for <bug_id>?
RISK TIER: <tier>
FILES: <list>
BLAST RADIUS: <assessment>
RECOMMENDATION: <approve/hold>
ARTIFACTS: crew/output/<bug_id>_change_request.md
```

### Handoff: change_manager -> qa_lead

**Task**: Reproduce and assess the bug
**Context**: Scope approved, working set updated, risk tier assigned
**Artifacts**:
- `crew/output/<bug_id>_change_request.md` — scope and risk assessment
**Decisions Made**: Risk tier, file scope, rollback strategy
**Open Questions**: Root cause confirmation, regression risk

---

## Step 2: QA Lead — Reproduce & Triage

**Agent:** `qa_lead`
**Input:** Change Request Package from Step 1
**Action:**
1. Read the relevant source files to understand current behaviour
2. Trace the data flow from entry point to render
3. Confirm the failure mode matches the FMEA description
4. Identify regression risks — what existing behaviour could break
5. Define acceptance criteria for the fix
6. Define test cases (what to verify after fix)
7. Write QA Assessment to `crew/output/<bug_id>_qa_assessment.md`

**Output:** QA Assessment
```
═══════════════════════════════════════════════
  QA ASSESSMENT: <bug_id>
═══════════════════════════════════════════════
BUG CONFIRMED: Yes/No
ROOT CAUSE: <technical root cause with file:line>
CURRENT BEHAVIOUR: <what happens now>
EXPECTED BEHAVIOUR: <what should happen>

ACCEPTANCE CRITERIA:
  1. <criterion>
  2. <criterion>

TEST CASES:
  1. <test description> — <expected result>
  2. <test description> — <expected result>

REGRESSION RISKS:
  - <risk> — <mitigation>

CONTRACTS IMPACT: None | <contract field affected>
═══════════════════════════════════════════════
```

### Handoff: qa_lead -> fe_lead

**Task**: Implement the fix
**Context**: Bug confirmed, root cause identified, acceptance criteria defined
**Artifacts**:
- `crew/output/<bug_id>_change_request.md` — scope and risk
- `crew/output/<bug_id>_qa_assessment.md` — root cause and test cases
**Decisions Made**: Root cause, acceptance criteria, regression risks
**Open Questions**: Implementation approach (if multiple options)

---

## Step 3: FE Lead — Implement Fix

**Agent:** `fe_lead`
**Input:** Change Request + QA Assessment
**Action:**
1. Read all affected files completely before making changes
2. For EACH file edit:
   a. Run `python .claude/validate_scope.py "<file_path>" --mode edit`
   b. Prepare exact diff (old_string -> new_string)
   c. Present diff preview to CEO with explanation
   d. **STOP and wait for CEO approval**
   e. Apply edit only after approval
3. After all edits applied:
   a. Run `npm run test:run` in the affected repo
   b. Run `npm run build` in the affected repo
   c. If tests fail: diagnose, fix, re-present diff, get approval
4. Update `.claude/change_log.md` with all changes made
5. Write implementation report to `crew/output/<bug_id>_fe_implementation.md`

**Output:** Implementation Report
```
═══════════════════════════════════════════════
  IMPLEMENTATION: <bug_id>
═══════════════════════════════════════════════
FILES CHANGED:
  - <file_path>:<line> — <description of change>

DIFFS APPLIED:
  [diff for each file]

TESTS: PASS (<count> tests) | FAIL (<details>)
BUILD: PASS | FAIL (<details>)
CHANGE LOG: Updated ✓
═══════════════════════════════════════════════
```

**Gate (every edit):**
```
GATE: edit_approval
AGENT: fe_lead
DECISION NEEDED: Approve this edit?
FILE: <file_path>
OLD: <old_string>
NEW: <new_string>
EXPLANATION: <what this changes and why>
RECOMMENDATION: approve
```

### Handoff: fe_lead -> qa_lead

**Task**: Verify the fix meets acceptance criteria
**Context**: Fix implemented, tests passing, build succeeding
**Artifacts**:
- `crew/output/<bug_id>_fe_implementation.md` — what was changed
- `crew/output/<bug_id>_qa_assessment.md` — acceptance criteria to verify against
**Decisions Made**: Implementation approach chosen and applied
**Open Questions**: Does the fix meet all acceptance criteria? Any regressions?

---

## Step 4: QA Lead — Verify Fix

**Agent:** `qa_lead`
**Input:** Implementation Report + original QA Assessment
**Action:**
1. Re-read all changed files to verify the diff was applied correctly
2. Verify each acceptance criterion is met
3. Check for regressions identified in Step 2
4. Verify tests pass and build succeeds
5. Verify change_log.md was updated
6. Write verification report to `crew/output/<bug_id>_qa_verification.md`

**Output:** Verification Report
```
═══════════════════════════════════════════════
  QA VERIFICATION: <bug_id>
═══════════════════════════════════════════════
ACCEPTANCE CRITERIA:
  1. <criterion> — PASS/FAIL
  2. <criterion> — PASS/FAIL

REGRESSION CHECK:
  - <risk checked> — PASS/FAIL

TESTS: <count> passing
BUILD: PASS
CHANGE LOG: Verified ✓

VERDICT: APPROVED / NEEDS REWORK
═══════════════════════════════════════════════
```

### Handoff: qa_lead -> change_manager

**Task**: Close the change request
**Context**: Fix verified, all criteria met
**Artifacts**:
- All prior artifacts
- `crew/output/<bug_id>_qa_verification.md` — verification result
**Decisions Made**: Fix verified as correct
**Open Questions**: None (if APPROVED)

---

## Step 5: Change Manager — Close Change Request

**Agent:** `change_manager`
**Input:** All artifacts from Steps 1-4
**Action:**
1. Verify all artifacts exist and are complete
2. Update `.claude/change_log.md` with final status
3. Update FMEA status if applicable (mark failure mode as FIXED)
4. Reset `.claude/working_set.txt` if no more fixes in this batch
5. Write Unified Change Register Entry

**Output:** Change Register Entry appended to change_log.md
```
| <timestamp> | <repo> | Code | <bug_id>: <description> | FMEA-<id> | <risk_tier> | CEO | — | CLOSED |
```

---

## Batch Mode

When fixing multiple bugs in one session (e.g., Sprint 0B with 7 fixes):

1. **Change Manager** runs Step 1 once for ALL bugs — single Change Request Package
2. **QA Lead** runs Step 2 for ALL bugs — single QA Assessment with per-bug sections
3. **FE Lead** runs Step 3 for ALL bugs — presents diffs grouped by file, one CEO gate per file
4. **QA Lead** runs Step 4 once — verifies all fixes
5. **Change Manager** runs Step 5 once — closes all change requests

This avoids 5-step overhead per individual bug when they are independent fixes.

---

## Error Handling

- **Scope validation fails (Exit 1):** Change Manager must update working_set.txt or escalate to CEO
- **Test failure after fix:** FE Lead diagnoses and retries once. If still failing, escalate to QA Lead
- **Build failure after fix:** FE Lead reverts the specific edit, investigates root cause, re-presents fix
- **CEO rejects diff:** FE Lead proposes alternative approach. If no alternative, escalate to QA Lead for reassessment
- **Backend file detected:** STOP entire workflow. Escalate to CEO for explicit backend permission

---

*Workflow: bug_fix.md v1.0 — 2026-03-31*
