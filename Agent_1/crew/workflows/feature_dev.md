# Workflow: Feature Development
# Command: `/crew feature <spec>`
# Agents: coo, change_manager, qa_lead, fe_lead, copywriter, visual_director
# Execution: Sequential with parallel sub-steps and 3 CEO gates

---

## Prerequisites

- Feature spec or PRD must exist (in `crew/tasks/` or provided inline)
- Product target must be known
- No P0 blockers open for the target product

---

## Phase 1: Scope & Feasibility — COO + Change Manager (parallel)

### COO:
1. Assess operational impact (vendor dependencies, revenue impact, timeline)
2. Check for conflicts with active sprints or campaigns
3. Write feasibility note to `crew/output/<feature_id>_coo_feasibility.md`

### Change Manager:
1. Classify risk tier for the feature
2. Identify all files likely to be modified
3. Check for contract impacts (kinship_analyze.v1, compare_faces.v1)
4. Check if backend changes are required
5. Write Change Request Package to `crew/output/<feature_id>_change_request.md`

**Gate 1: Scope Approval**
```
GATE: feature_scope_approval
AGENT: coo + change_manager
DECISION NEEDED: Approve feature scope?
FEATURE: <feature name>
RISK TIER: <tier>
BACKEND CHANGES: Yes/No
CONTRACT IMPACT: None/<contract>
ESTIMATED EFFORT: <XS/S/M/L/XL>
OPERATIONAL IMPACT: <assessment>
RECOMMENDATION: approve/defer/split
ARTIFACTS:
  - crew/output/<feature_id>_coo_feasibility.md
  - crew/output/<feature_id>_change_request.md
```

---

## Phase 2: Design — Visual Director + Copywriter (parallel)

### Visual Director:
1. Read feature spec and existing UI patterns
2. Produce Visual Direction Document
3. Write to `crew/output/<feature_id>_visual_direction.md`

### Copywriter:
1. Read feature spec and brand context
2. Produce Copy Bank for all user-facing text
3. Write to `crew/output/<feature_id>_copy_bank.md`

### Handoff: visual_director + copywriter -> fe_lead

**Task**: Implement the feature
**Context**: Scope approved, visual direction defined, copy written
**Artifacts**: Change request + visual direction + copy bank
**Decisions Made**: Scope, risk tier, design direction, all user-facing copy
**Open Questions**: Technical implementation approach

---

## Phase 3: Implementation — FE Lead

**Agent:** `fe_lead`
**Action:**
1. Read all artifacts from Phase 1-2
2. Read existing code in target files
3. Plan implementation approach
4. For EACH file edit:
   a. Validate scope
   b. Present diff to CEO
   c. Wait for approval
   d. Apply edit
5. Integrate copy from Copy Bank (exact strings, not paraphrased)
6. Follow Visual Direction for layout and styling
7. Run tests + build
8. Update change_log.md
9. Write to `crew/output/<feature_id>_fe_implementation.md`

**Gate 2: Per-edit approval (same as bug_fix workflow)**

---

## Phase 4: Verification — QA Lead

**Agent:** `qa_lead`
**Action:**
1. Read feature spec and all acceptance criteria
2. Verify implementation against spec
3. Check for regressions
4. Verify copy matches Copy Bank exactly
5. Verify visual direction compliance
6. Run tests + build
7. Write verification report to `crew/output/<feature_id>_qa_verification.md`

If FAIL: handoff back to fe_lead for rework.

---

## Phase 5: Ship Gate — Change Manager + QA Lead

**Gate 3: Ship Approval**
```
GATE: feature_ship_approval
AGENT: change_manager (change package), qa_lead (verification)
DECISION NEEDED: Ship feature <name>?
TESTS: <count> passing
BUILD: PASS
QA VERDICT: APPROVED
RISK TIER: <tier>
ROLLBACK: <strategy>
RECOMMENDATION: ship
ARTIFACTS:
  - crew/output/<feature_id>_qa_verification.md
  - crew/output/<feature_id>_fe_implementation.md
```

---

## Phase 6: Close — Change Manager

1. Update change_log.md with SHIPPED status
2. Update any relevant memory files
3. Reset working_set.txt
4. Write feature summary to `crew/output/<feature_id>_summary.md`

---

*Workflow: feature_dev.md v1.0 — 2026-03-31*
