# Crew Orchestrator — Claude Code Native
**Version:** 3.0 — 2026-04-09
**Changes:** Added 6 new agents, 3 new workflows, activation model, umbrella app strategy, shared package routing

---

## Agent Roster (15 agents, 5 levels)

### System Level — owns the platform, no feature work
| Agent | File | Domain |
|-------|------|--------|
| Platform Architect | `agents/platform_architect.md` | AppErrorBus, AppStorage, resultsContract, shared infrastructure, protected files |
| Mobile Solutions Architect | `agents/mobile_solutions_architect.md` | iOS/Android technical assessment, Capacitor readiness, TF.js compatibility |
| Game Engine Architect | `agents/game_engine_architect.md` | WebSocket protocol, room management, famililook-game-engine package |

### Lead Level — owns a product or platform layer
| Agent | File | Domain |
|-------|------|--------|
| FE Lead | `agents/fe_lead.md` | All frontend repos (desktop2, desktop4, desktop6) |
| BE Lead | `agents/be_lead.md` | All backend repos (desktop3, desktop5, desktop7) |
| Native App Lead | `agents/native_app_lead.md` | Capacitor config, iOS/Android submission, IAP |

### Solutions Level — owns a domain across all products
| Agent | File | Domain |
|-------|------|--------|
| Data Solutions Architect | `agents/data_solutions_architect.md` | Analytics pipeline, geo enrichment, growth metrics |
| Shared Infrastructure Lead | `agents/shared_infrastructure_lead.md` | famililook-shared npm package, famililook-game-engine pip package migration |

### Quality and Governance
| Agent | File | Domain |
|-------|------|--------|
| QA Lead | `agents/qa_lead.md` | DFMEA, halt authority, cross-product regression |
| Change Manager | `agents/change_manager.md` | Audit trail, architecture health, all repos |
| COO | `agents/coo.md` | Daily briefing, KPIs, architecture health |

### Marketing and Growth
| Agent | File | Domain |
|-------|------|--------|
| CMO | `agents/cmo.md` | Four-product campaign strategy |
| Copywriter | `agents/copywriter.md` | Four product voices |
| Visual Director | `agents/visual_director.md` | Four brand identities, shared UI kit |
| Growth Monitor | `agents/growth_monitor.md` | Four product funnels |

---

## Command Routing

| Command | Workflow | Agents |
|---------|----------|--------|
| `/crew status` | inline | coo, platform_architect (architecture health) |
| `/crew briefing` | inline | coo |
| `/crew fix <bug>` | **PRE-FIX TRIAGE GATE → then** bug_fix | change_manager → qa_lead → [visual_director + copywriter if visual] → fe_lead or be_lead → qa_lead → change_manager |
| `/crew redesign <component>` | redesign workflow | platform_architect → qa_lead → GATE → fe_lead/be_lead → qa_lead → change_manager |
| `/crew feature <spec>` | feature_dev | cpo, qa_lead, fe_lead/be_lead, qa_lead, change_manager |
| `/crew mobile` | **NEW** mobile workflow | mobile_solutions_architect → GATE → native_app_lead → qa_lead → change_manager |
| `/crew multiplayer` | **NEW** multiplayer workflow | game_engine_architect → GATE → be_lead → qa_lead → change_manager |
| `/crew migrate` | **NEW** migration workflow | shared_infrastructure_lead → GATE → fe_lead/be_lead → qa_lead → change_manager |
| `/crew analytics` | **NEW** analytics workflow | data_solutions_architect → GATE → fe_lead + be_lead → qa_lead → change_manager |
| `/crew sprint` | sprint workflow | coo, qa_lead, fe_lead, be_lead, change_manager |
| `/crew review` | inline | qa_lead, change_manager (parallel) |
| `/crew audit` | audit workflow | qa_lead, change_manager, platform_architect |
| `/crew deploy <product>` | deployment workflow | qa_lead, native_app_lead (if mobile), change_manager |
| `/crew release <product>` | inline | change_manager, qa_lead |
| `/crew campaign <brief>` | inline | cmo → ad_crew |
| `/crew marketing` | inline | cmo |
| `/crew changes` | inline | change_manager |
| `/crew roadmap` | inline | coo |

---

## Activation Model — Who Runs When

**Always available (every task):**
FE Lead, QA Lead, Change Manager, COO

**Activated by task type:**

| Trigger | Activate first | Then |
|---------|---------------|------|
| Fix touches protected file | Platform Architect | CEO gate → FE/BE Lead |
| Any multiplayer/WebSocket work | Game Engine Architect | CEO gate → BE Lead |
| Any Capacitor/mobile work | Mobile Solutions Architect | CEO gate → Native App Lead |
| Any analytics work | Data Solutions Architect | CEO gate → FE + BE Lead |
| Any shared package work | Shared Infrastructure Lead | CEO gate → FE/BE Lead |
| Any backend Python work | BE Lead | (requires explicit CEO backend permission) |
| Any native plugin work | Native App Lead | — |
| Any visual fix | Visual Director spec first | FE Lead implements after |
| Any copy change | Copywriter spec first | FE Lead implements after |
| Fix attempted 3+ times | Platform Architect HALT | /crew redesign |
| Fix attempted 2 times | QA Lead triage | HALT or proceed |

---

## PRE-FIX TRIAGE GATE (mandatory before every /crew fix)

Before routing ANY fix to FE Lead or BE Lead:

**Q1 — Patch count**
```bash
grep -c "<file/component>" .claude/change_log.md
```
- 0-1: PROCEED
- 2: QA Lead recommendation required
- 3+: HALT → route to /crew redesign

**Q2 — Root cause classification**
QA Lead classifies: SYMPTOM | ROOT_CAUSE
If SYMPTOM and patch count ≥ 2: HALT

**Q3 — Protected file check**
Does fix touch: FamililookContext.jsx, BasketContext.jsx, useKinshipAnalysis.jsx, analytics.js, any direct localStorage call, any WebSocket endpoint?
If YES: Platform Architect (frontend) or Game Engine Architect (WebSocket) reviews first.

**Q4 — Backend permission check**
Does fix touch any .py file?
If YES: confirm explicit CEO backend permission before proceeding.

Present triage result to CEO before routing.

---

## New Workflow: /crew mobile

Use when: any Capacitor work, App Store preparation, native plugin integration, mobile performance assessment.

```
Step 1 — Mobile Solutions Architect
  Reads: capacitor.config.ts (if exists), AppRouter.jsx, main.jsx, TF.js init code
  Produces: MOBILE_SOLUTIONS_ARCH_<date>.md
  Assesses: WebGL, localStorage, model loading, WebSocket, plugins needed

GATE: mobile_scope_approval
  CEO approves: which products to wrap, which plugins to add, iOS-first or both

Step 2 — Native App Lead (iOS)
  Implements: capacitor.config.ts, Info.plist
  Integrates: approved plugins
  Prepares: App Store Connect listing

Step 3 — QA Lead
  Validates: TestFlight internal testing results
  Checks: entertainment disclaimer visible, COPPA gate first, WSS verified
  Mobile items: UNVERIFIED until CEO device verification

Step 4 — Native App Lead (Android) — after iOS stable
  Implements: AndroidManifest.xml
  Prepares: Google Play Console listing

Step 5 — Change Manager
  Logs: release package for both platforms
  Tracks: submission status
```

---

## New Workflow: /crew multiplayer

Use when: any WebSocket server work, room management, P2P game features, reconnection logic.

```
Step 1 — Game Engine Architect
  Reads: desktop5/app/, desktop7/app/ in full
  Produces: GAME_ENGINE_ARCH_<date>.md
  Assesses: current room management, protocol, what extracts to shared engine

GATE: multiplayer_scope_approval
  CEO approves: shared engine scope, FamiliUno server placement (desktop5 vs new repo)

Step 2 — BE Lead (with explicit CEO backend permission)
  Implements: famililook-game-engine package
  Migrates: desktop5 and desktop7 to consume shared engine
  Adds: reconnection, friendly room codes, heartbeat

Step 3 — FE Lead
  Implements: useWebSocket hook from famililook-shared
  Updates: game UI to handle reconnection states

Step 4 — QA Lead
  Validates: room creation, joining, disconnection, reconnection
  Tests: background/foreground cycle on device
  Mobile items: UNVERIFIED until CEO device test

Step 5 — Change Manager: close out
```

---

## New Workflow: /crew migrate

Use when: moving code into famililook-shared or famililook-game-engine.

```
Step 1 — Shared Infrastructure Lead
  Reads: source files in all product repos
  Classifies: IDENTICAL/NEAR-IDENTICAL/SIMILAR/UNIQUE
  Produces: SHARED_INFRA_MIGRATION_<date>.md
  Specifies: migration order (max 3 components per sprint)

GATE: migration_scope_approval
  CEO approves: which components migrate this sprint

Step 2 — FE Lead (frontend) + BE Lead (backend) in parallel
  Each migrates approved components
  Strangler fig: one product at a time, tests pass at each step
  Never leaves a product half-migrated

Step 3 — QA Lead
  Cross-product regression: tests pass in ALL consuming repos
  Not just the first product migrated

Step 4 — Change Manager: update architecture health metrics
  Track: which shared modules are built and consumed
```

---

## Architecture Health Tracking (in every /crew briefing)

COO briefing includes:

```
ARCHITECTURE HEALTH — <date>
Structural modules:
  AppErrorBus:          NOT BUILT | BUILT (<date>) | CONSUMED BY: <repos>
  AppStorage:           NOT BUILT | BUILT (<date>) | CONSUMED BY: <repos>
  resultsContract:      NOT BUILT | BUILT (<date>) | CONSUMED BY: <repos>
  famililook-shared:    NOT BUILT | SCAFFOLDED | ACTIVE (<components>)
  famililook-game-engine: NOT BUILT | SCAFFOLDED | ACTIVE (<modules>)

Files patched 3+ times (30 days): <list or NONE>
Silent catches outstanding: <count>
Dependency divergences: <list or NONE>

Mobile readiness:
  AppStorage (WebView safe): NOT BUILT | BUILT
  TF.js WebGL assessment: PENDING | DONE
  Capacitor init: NOT STARTED | IN PROGRESS | DONE

Multiplayer readiness:
  famililook-game-engine: NOT BUILT | BUILT
  WSS on all endpoints: NO (<list plain WS>) | YES
  Graceful reconnection: NOT BUILT | BUILT
```

---

## Protected Structural Modules

Once built, no agent may bypass these:

| Module | Status | Bypass = |
|--------|--------|---------|
| AppErrorBus | NOT BUILT | Silent catch block → P1 violation |
| AppStorage | NOT BUILT | Direct localStorage call → P1 violation |
| resultsContract.js | NOT BUILT | Winner logic outside this file → P1 violation |
| famililook-shared | SCAFFOLDED | Reimplementing shared component in product → P2 |
| famililook-game-engine | NOT BUILT | Separate room management in game server → P2 |

---

## Umbrella App Tab Structure

```
FamiliLook App (Capacitor)
├── Tab 1: FamiliLook  — analysis, keepsakes, trail (entry point)
├── Tab 2: FamiliMatch — comparison, chemistry, social
├── Tab 3: FamiliUno   — card games (unlocks after first analysis)
└── Tab 4: FamiliPoker — multiplayer poker (Plus tier only)

All tabs share:
  @capacitor/camera      — face upload
  @capacitor/status-bar  — status bar styling
  @capacitor/app         — lifecycle events
  famililook-shared      — UI kit, hooks, infrastructure
```

---

## Execution Model

### Sequential (default)
Agent A completes → saves output → Agent B reads output → continues

### Parallel (independent agents)
```
┌─ Agent A → output_a
├─ Agent B → output_b  → Merge → Next step
└─ Agent C → output_c
```

Use parallel execution for: Visual Director + Copywriter, FE Lead + BE Lead on different files, iOS + Android submission prep.

---

## Gate Protocol

```
GATE: <gate_name>
AGENT: <who produced>
DECISION NEEDED: <what CEO decides>
OPTIONS:
  A. <option> — <consequence>
  B. <option> — <consequence>
RECOMMENDATION: <agent recommendation>
ARTIFACTS: <files to review>
```

Always wait for explicit CEO decision before proceeding past a gate.

---

## Error Handling

If an agent step fails:
1. Log failure with full context
2. One retry with adjusted approach
3. If still failing → escalate to agent's manager
4. If manager can't resolve → CEO escalation with: what was attempted, why it failed, alternatives
