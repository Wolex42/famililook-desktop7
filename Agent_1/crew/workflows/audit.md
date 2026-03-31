# Workflow: Platform Audit
# Command: `/crew audit`
# Agents: qa_lead, change_manager (parallel) -> coo (merge)
# Execution: Parallel audit, then merged report

---

## Prerequisites

- All repos accessible in `C:\Users\wole\Documents\FML`
- No active deploys in progress

---

## Phase 1: Parallel Audit (3 agents)

### QA Lead — Quality Audit
**Action:**
1. Run test suites across all repos:
   - `npm run test:run` in desktop2, desktop4, desktop6
   - `npm run build` in desktop2, desktop4, desktop6
2. Check test coverage gaps
3. Review FMEA for items still marked Open
4. Identify untested paths
5. Write to `crew/output/audit_qa.md`

**Output:** Quality Audit Report
```
═══════════════════════════════════════════════
  QUALITY AUDIT — <date>
═══════════════════════════════════════════════
TEST HEALTH:
  desktop2: <pass/fail> (<count> tests)
  desktop4: <pass/fail> (<count> tests)
  desktop6: <pass/fail> (<count> tests)

BUILD HEALTH:
  desktop2: PASS/FAIL
  desktop4: PASS/FAIL
  desktop6: PASS/FAIL

OPEN FMEA ITEMS: <count>
  P0: <count> (<IDs>)
  P1: <count> (<IDs>)

UNTESTED PATHS:
  - <path description>

RECOMMENDATIONS:
  1. <recommendation>
═══════════════════════════════════════════════
```

### Change Manager — Change Health Audit
**Action:**
1. Scan all repos for commits since last audit
2. Cross-reference commits against change_log entries
3. Check for untracked changes (files modified but not logged)
4. Verify working_set.txt is current
5. Verify pre-commit hooks are installed
6. Check for orphaned ops_reports
7. Write to `crew/output/audit_changes.md`

**Output:** Change Health Report (per Change Manager output format)

### Security Audit (inline — no dedicated agent)
**Action:**
1. Run `npm audit` in desktop2, desktop4, desktop6
2. Check for exposed secrets (grep for API keys, tokens in source)
3. Check consent flows are enforced (biometric consent middleware, COPPA gates)
4. Check for publicly accessible internal routes
5. Write to `crew/output/audit_security.md`

---

## Phase 2: Merge — COO

**Agent:** `coo`
**Action:**
1. Read all 3 audit reports
2. Compile into unified Platform Audit Report
3. Identify CEO decisions needed
4. Prioritise findings
5. Write to `crew/output/audit_platform_<date>.md`

**Output:** Platform Audit Report
```
═══════════════════════════════════════════════
  PLATFORM AUDIT — <date>
═══════════════════════════════════════════════

OVERALL STATUS: GREEN/YELLOW/RED

QUALITY: <summary>
CHANGE HEALTH: <summary>
SECURITY: <summary>

TOP FINDINGS:
  1. <finding> — <severity> — <owner>
  2. ...

CEO DECISIONS NEEDED:
  - <decision>

RECOMMENDED ACTIONS:
  1. <action> — <agent> — <priority>
═══════════════════════════════════════════════
```

---

*Workflow: audit.md v1.0 — 2026-03-31*
