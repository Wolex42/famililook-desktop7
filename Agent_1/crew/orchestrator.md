# Crew Orchestrator — Claude Code Native

## How To Use This File

When the user issues a crew command, Claude Code reads this file to determine:
1. Which workflow to execute
2. Which agents to activate
3. In what order (sequential or parallel)
4. What gates require CEO approval

---

## Command Routing

| Command | Workflow File | Agents Activated |
|---------|--------------|-----------------|
| `/crew status` | (inline) | coo, cto, cpo |
| `/crew sprint` | `workflows/sprint.md` | pm, cpo, cto, qa_lead |
| `/crew review` | (inline) | qa_lead, security, compliance |
| `/crew fix <bug>` | `workflows/bug_fix.md` | qa_lead, cto, fe_lead or be_lead |
| `/crew feature <spec>` | `workflows/feature_dev.md` | cpo, pm, design_lead, fe_lead/be_lead, qa_lead, devops |
| `/crew campaign <brief>` | (inline) | cmo → ad_crew pipeline |
| `/crew audit` | `workflows/audit.md` | compliance, security, change_manager |
| `/crew deploy <product>` | `workflows/deployment.md` | devops, qa_lead, cto, change_manager |
| `/crew briefing` | (inline) | coo |
| `/crew roadmap` | (inline) | cpo |
| `/crew revenue` | (inline) | commerce_lead |
| `/crew orders` | (inline) | fulfillment |
| `/crew changes` | (inline) | change_manager |
| `/crew marketing` | (inline) | cmo |
| `/crew release <product>` | (inline) | change_manager, qa_lead, devops |

---

## Execution Model

### Sequential Execution (default)
```
Agent A does work → saves output → Agent B reads output → does work → ...
```

Claude Code loads each agent persona, does the work, saves artifacts to `crew/output/`,
then loads the next agent persona and continues.

### Parallel Execution (when agents are independent)
```
┌─ Agent A (subagent) ──→ output_a
│
├─ Agent B (subagent) ──→ output_b    → Merge → Next step
│
└─ Agent C (subagent) ──→ output_c
```

Use Claude Code's `Agent` tool to launch parallel subagents. Each subagent
gets the agent persona prompt + task context. Results merge before the next step.

---

## Agent Loading Protocol

When activating an agent, Claude Code MUST:

1. Read the agent's persona file: `crew/agents/<agent_id>.md`
2. Adopt the agent's role, constraints, and output format
3. Use ONLY the tools allowed for that agent
4. Produce output in the agent's specified format
5. Save output to `crew/output/<task_id>_<agent_id>.md`
6. If the agent hits a blocker or needs CEO input, STOP and ask

### Agent Persona File Format
```markdown
# Agent: <role>
## Identity
## Scope (what files/tools this agent can use)
## Constraints (what this agent CANNOT do)
## Output Format
## Escalation Rules
```

---

## Gate Protocol

Some workflow steps require CEO approval before proceeding:

```
GATE: <gate_name>
AGENT: <who produced the output>
DECISION NEEDED: <what the CEO must decide>
OPTIONS:
  1. <option A> — <consequence>
  2. <option B> — <consequence>
RECOMMENDATION: <agent's recommendation>
ARTIFACTS: <files to review>
```

Claude Code MUST present this to the user and wait for a response
before proceeding to the next workflow step.

---

## Context Passing Between Agents

When one agent hands off to another:

```markdown
## Handoff: <from_agent> → <to_agent>

**Task**: <what needs to be done>
**Context**: <what was already done>
**Artifacts**:
- `crew/output/<file1>` — <description>
- `crew/output/<file2>` — <description>
**Decisions Made**: <any decisions locked in by previous agents>
**Open Questions**: <anything the next agent needs to resolve>
```

---

## Status Command (inline — no workflow file needed)

When user says `/crew status`:

1. **As CTO**: Scan all repos for test health, recent commits, open issues
   - `npm run test:run` in desktop2, desktop4, desktop6
   - Check git log for recent activity
   - Flag any failing builds

2. **As COO**: Compile cross-department status
   - Revenue status (if Stripe dashboard accessible)
   - Order pipeline status
   - Blocker summary

3. **As CPO**: Roadmap status
   - What's in progress
   - What's blocked
   - What's next

Present combined output in briefing format.

---

## Briefing Command (inline)

When user says `/crew briefing`:

As COO, generate:

```
═══════════════════════════════════════════════
  FAMILILOOK DAILY BRIEFING — <date>
═══════════════════════════════════════════════

PLATFORM STATUS: 🟢/🟡/🔴

TEST HEALTH:
  desktop2: <pass/fail> (<count> tests)
  desktop3: <pass/fail> (<count> tests)
  desktop4: <pass/fail> (<count> tests)
  desktop5: <pass/fail> (<count> tests)
  desktop6: <pass/fail> (<count> tests)
  desktop7: <pass/fail> (<count> tests)

RECENT COMMITS (last 7 days):
  <commit summaries>

ACTIVE WORK:
  <what's in progress based on git activity>

BLOCKERS:
  <anything requiring CEO input>

PRIORITIES:
  1. <next priority>
  2. <next priority>
  3. <next priority>
═══════════════════════════════════════════════
```

---

## Review Command (inline)

When user says `/crew review`:

Run four agents in parallel (as Claude Code subagents):

1. **QA Lead**: Run test suites, report results
2. **Security**: Run `npm audit` / dependency checks
3. **Compliance**: Check consent flows, data handling
4. **Change Manager**: Scan for untracked changes, orphaned runs, stale state

Merge results into a single review report.

---

## Changes Command (inline)

When user says `/crew changes`:

As Change Manager, run a Change Health Report:

1. **Scan all 7 repos** for commits since last audit
2. **Cross-reference** each commit against change_log entries
3. **Check ops_reports** for completeness (no orphaned runs)
4. **Check ad_crew output** for unregistered campaigns
5. **Verify** working_set.txt is current, hooks installed
6. **Report** in Change Health Report format

---

## Marketing Command (inline)

When user says `/crew marketing`:

As CMO:

1. **Read seasonal calendar** — identify next event within 30 days
2. **Check ads_live_by deadline** — how urgent?
3. **Review existing campaign output** — has ad_crew already run for this event?
4. **Report readiness** in Campaign Readiness format
5. If campaign needed and deadline urgent: recommend dispatching ad_crew

---

## Release Command (inline)

When user says `/crew release <product>`:

Sequential workflow with Change Manager as coordinator:

1. **Change Manager**: Assemble Change Request Package
   - Gather all changes since last release for this product
   - Classify risk tier (P0-P3)
   - Run validation checklist (traceability, tests, contracts, blast radius)

2. **QA Lead**: Validate test health
   - Run test suite for the target repo
   - Report pass/fail with evidence

3. **DevOps**: Prepare deployment
   - Verify Vercel/Hetzner target is ready
   - Confirm rollback plan
   - Check infra health

4. **GATE: Release Approval**
   ```
   GATE: release_approval
   AGENT: change_manager (assembled), qa_lead (validated), devops (ready)
   DECISION NEEDED: Approve release of <product>?
   RISK TIER: <P0-P3>
   VALIDATION: <checklist results>
   TEST HEALTH: <pass/fail counts>
   ROLLBACK: <strategy>
   RECOMMENDATION: <approve/hold>
   ```

5. If approved → DevOps deploys → Change Manager logs release

---

## Campaign Command (updated)

When user says `/crew campaign <brief>`:

1. **As CMO**: Assess the campaign brief against seasonal calendar and brand context
2. **CMO dispatches ad_crew**: Sets phase, event, budget, channels
3. **Ad crew runs**: Generates content → publish queue
4. **CMO reviews**: Brand compliance check on all output
5. **Change Manager**: Registers campaign output in change system

**GATE: Campaign Approval** (before publishing)
```
GATE: campaign_approval
AGENT: cmo (reviewed)
DECISION NEEDED: Approve campaign for <event>?
CONTENT: <N posts in publish queue>
BUDGET: £<total>
BRAND CHECK: ✅/⚠️/🔴
RECOMMENDATION: <approve/revise>
```

---

## Change Manager Integration Points

The Change Manager participates in these existing workflows:

| Workflow | When CM is involved | What CM does |
|----------|-------------------|-------------|
| `/crew feature` | After QA passes, before ship gate | Assembles Change Request Package for CEO |
| `/crew fix` | After fix applied | Verifies ops_report created, change_log updated |
| `/crew deploy` | Before deploy approval | Validates all changes tracked, risk tier assigned |
| `/crew campaign` | After ad_crew output | Registers campaign in change system |
| `/crew audit` | During audit | Reports change health alongside compliance + security |
| `/crew review` | Added as 4th parallel check | Scans for untracked changes |
| `/crew status` | Included in briefing | Reports change health summary to COO |

---

## Error Handling

If an agent step fails:
1. Log the failure with context
2. Attempt one retry with adjusted approach
3. If still failing, escalate to the agent's manager
4. If manager can't resolve, escalate to CEO with:
   - What was attempted
   - Why it failed
   - Suggested alternatives
