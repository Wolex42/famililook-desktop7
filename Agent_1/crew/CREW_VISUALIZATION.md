# FamiliLook Crew — Visual Workflows

> Open this file in VS Code (built-in Mermaid preview) or paste into https://mermaid.live
> Zero cost, zero plugins needed in VS Code 2026+

---

## 1. Organisation Chart

```mermaid
graph TD
    CEO["👔 CEO (Wole)<br/>Final sign-off"]

    CEO --> CPO["🎯 CPO<br/>Product Dept"]
    CEO --> CTO["⚙️ CTO<br/>Engineering Dept"]
    CEO --> COO["📊 COO<br/>Operations Dept"]

    CPO --> PM["📋 Product Manager"]
    CPO --> DL["🎨 Design Lead"]
    CPO --> UXR["🔬 UX Researcher"]

    CTO --> FE["💻 FE Lead"]
    CTO --> BE["🐍 BE Lead"]
    CTO --> QA["✅ QA Lead"]
    CTO --> DO["🚀 DevOps"]
    CTO --> SEC["🔒 Security"]

    COO --> AD["📣 Ad Crew (9 agents)"]
    COO --> COM["💳 Commerce Lead"]
    COO --> FUL["📦 Fulfillment"]
    COO --> CMP["⚖️ Compliance"]

    style CEO fill:#FFD700,stroke:#333,stroke-width:3px,color:#000
    style CPO fill:#8B5CF6,stroke:#333,stroke-width:2px,color:#fff
    style CTO fill:#3B82F6,stroke:#333,stroke-width:2px,color:#fff
    style COO fill:#14B8A6,stroke:#333,stroke-width:2px,color:#fff
```

---

## 2. Task Flow: How Work Gets Assigned

```mermaid
flowchart TD
    subgraph INPUT["📥 TASK INPUT"]
        DC["Direct Command<br/>@agent_id task"]
        BL["Backlog Task<br/>Pick up TASK-008"]
        PRD["PRD Document<br/>run PRD path/to/prd.md"]
    end

    subgraph ORCHESTRATOR["🎛️ ORCHESTRATOR"]
        ROUTE["Route to Department"]
        LOAD["Load Agent Persona (.md)"]
        INJECT["Inject Task into ## 2. TASK"]
    end

    subgraph EXECUTE["⚡ EXECUTION"]
        SEQ["Sequential<br/>(agent → agent → agent)"]
        PAR["Parallel<br/>(Agent tool subagents)"]
    end

    subgraph OUTPUT["📤 OUTPUT"]
        RESULT["crew/output/<br/>task_id_agent.md"]
        VIZ["Mermaid Workflow<br/>Diagram"]
        GATE["CEO GATE<br/>(approve/reject)"]
    end

    DC --> ROUTE
    BL --> ROUTE
    PRD --> ROUTE
    ROUTE --> LOAD
    LOAD --> INJECT
    INJECT --> SEQ
    INJECT --> PAR
    SEQ --> RESULT
    PAR --> RESULT
    RESULT --> GATE
    RESULT --> VIZ

    style INPUT fill:#F3F4F6,stroke:#333
    style ORCHESTRATOR fill:#EEF2FF,stroke:#333
    style EXECUTE fill:#F0FDF4,stroke:#333
    style OUTPUT fill:#FEF3C7,stroke:#333
    style GATE fill:#FFD700,stroke:#333,stroke-width:2px
```

---

## 3. Feature Development Workflow (11 Steps)

```mermaid
sequenceDiagram
    actor CEO as CEO (Wole)
    participant ORC as Orchestrator
    participant CPO as CPO
    participant CMP as Compliance
    participant PM as PM
    participant DL as Design Lead
    participant CTO as CTO
    participant DEV as FE/BE Lead
    participant QA as QA Lead
    participant SEC as Security
    participant DO as DevOps

    CEO->>ORC: /crew feature "add X"
    ORC->>CPO: Step 1: Spec & Prioritise

    par Parallel Steps 2+3
        ORC->>CMP: Step 2: Compliance Check
        ORC->>PM: Step 3: User Stories
    end

    CMP-->>CEO: Compliance verdict
    PM-->>CEO: User stories ready

    Note over CEO: 🚦 GATE: Approve scope

    par Parallel Steps 5+6
        ORC->>DL: Step 5: UI Spec
        ORC->>CTO: Step 6: Architecture Review
    end

    DL-->>DEV: Design spec
    CTO-->>DEV: Tech approach

    DEV->>CEO: Step 7: Show diff preview
    Note over CEO: 🚦 GATE: Approve each edit
    CEO-->>DEV: Approved

    par Parallel Steps 8+9
        ORC->>QA: Step 8: Run tests
        ORC->>SEC: Step 9: Security review
    end

    QA-->>CEO: Test report
    SEC-->>CEO: Security clear

    Note over CEO: 🚦 GATE: Ship approval

    ORC->>DO: Step 11: Deploy
    DO-->>CEO: Live ✅
```

---

## 4. Bug Fix Workflow

```mermaid
flowchart LR
    BUG["🐛 Bug Report"] --> QA["QA Lead<br/>Reproduce & Triage"]
    QA --> CTO["CTO<br/>Assess Impact"]
    CTO --> |"FE bug"| FE["FE Lead<br/>Fix + Test"]
    CTO --> |"BE bug"| BE["BE Lead<br/>Fix + Test"]
    FE --> GATE["CEO GATE<br/>Approve Diff"]
    BE --> GATE
    GATE --> QA2["QA Lead<br/>Verify Fix"]
    QA2 --> DO["DevOps<br/>Deploy"]

    style BUG fill:#FEE2E2,stroke:#EF4444
    style GATE fill:#FFD700,stroke:#333,stroke-width:2px
    style DO fill:#22C55E,color:#fff
```

---

## 5. Sprint Planning Workflow

```mermaid
flowchart TD
    START["Sprint Start"] --> CPO["CPO<br/>Review Backlog<br/>Set Priorities"]
    CPO --> PM["PM<br/>Break into Stories<br/>Estimate Effort"]
    PM --> CTO["CTO<br/>Tech Feasibility<br/>Flag Risks"]
    CTO --> GATE["CEO GATE<br/>Approve Sprint"]
    GATE --> PAR{Parallel Execution}
    PAR --> FE["FE Lead"]
    PAR --> BE["BE Lead"]
    PAR --> DL["Design Lead"]
    PAR --> CMP["Compliance"]
    FE --> QA["QA<br/>Sprint Review"]
    BE --> QA
    DL --> QA
    CMP --> QA
    QA --> RETRO["Sprint Retro<br/>(COO Report)"]

    style START fill:#8B5CF6,color:#fff
    style GATE fill:#FFD700,stroke:#333,stroke-width:2px
    style RETRO fill:#14B8A6,color:#fff
```

---

## 6. Deployment Workflow

```mermaid
flowchart LR
    REQ["Deploy Request"] --> QA["QA Lead<br/>Full test suite"]
    QA --> |"PASS"| SEC["Security<br/>npm audit"]
    QA --> |"FAIL"| BLOCK["❌ BLOCKED<br/>Fix First"]
    SEC --> |"CLEAR"| CTO["CTO<br/>Approve Release"]
    SEC --> |"VULN"| BLOCK
    CTO --> GATE["CEO GATE"]
    GATE --> DO["DevOps<br/>Deploy + Smoke Test"]
    DO --> MON["Monitor 30min"]
    MON --> |"OK"| DONE["✅ LIVE"]
    MON --> |"Issues"| ROLL["🔄 Rollback"]

    style BLOCK fill:#FEE2E2,stroke:#EF4444
    style DONE fill:#22C55E,color:#fff
    style GATE fill:#FFD700,stroke:#333
    style ROLL fill:#F97316,color:#fff
```

---

## 7. Incident Response Workflow

```mermaid
flowchart TD
    INC["🚨 Incident Detected"] --> COO["COO<br/>Coordinate Response"]
    COO --> PAR{Parallel}
    PAR --> CTO["CTO<br/>Root Cause"]
    PAR --> DO["DevOps<br/>Mitigate"]
    PAR --> COM["Commerce<br/>Revenue Impact"]
    CTO --> FIX["Fix Team<br/>(FE/BE Lead)"]
    FIX --> QA["QA<br/>Verify"]
    QA --> DEPLOY["Emergency Deploy"]
    DEPLOY --> COO2["COO<br/>Post-Mortem"]
    COO2 --> CEO["CEO Briefing"]

    style INC fill:#FEE2E2,stroke:#EF4444,stroke-width:2px
    style CEO fill:#FFD700,stroke:#333
```

---

## 8. Marketing Campaign Workflow

```mermaid
flowchart TD
    BRIEF["Campaign Brief"] --> COO["COO<br/>Approve Brief"]
    COO --> BS["Brand Strategist<br/>Brand Brief"]
    BS --> PAR{Parallel}
    PAR --> CW["Copywriter<br/>Ad Copy"]
    PAR --> VD["Visual Director<br/>Creative Specs"]
    PAR --> SM["Social Media Mgr<br/>Platform Strategy"]
    CW --> CS["Conversion Specialist<br/>CTA Optimization"]
    VD --> CS
    SM --> CS
    CS --> GATE["CEO GATE<br/>Approve Campaign"]
    GATE --> LAUNCH["🚀 Launch"]

    style BRIEF fill:#8B5CF6,color:#fff
    style GATE fill:#FFD700,stroke:#333
    style LAUNCH fill:#22C55E,color:#fff
```

---

## 9. Product Backlog Status

```mermaid
gantt
    title Product Backlog — Priority View
    dateFormat YYYY-MM-DD
    axisFormat %b

    section P0 Critical
    COPPA Compliance (TASK-001)       :crit, t001, 2026-03-15, 30d
    QPMarkets API (TASK-002)          :crit, t002, 2026-03-15, 21d
    BIPA Consent (TASK-003)           :crit, t003, 2026-03-15, 14d

    section P1 High
    Live Exchange Rates (TASK-004)    :t004, after t003, 10d
    Marketing Claims Audit (TASK-005) :t005, 2026-03-20, 5d
    DPIA Document (TASK-006)          :t006, after t001, 14d
    Capacitor Mobile (TASK-007)       :t007, after t003, 45d
    FamiliMatch Viral (TASK-008)      :t008, after t004, 21d

    section P2 Medium
    Scaling Plan (TASK-009)           :t009, after t007, 14d
    A/B Test Framework (TASK-010)     :t010, after t008, 10d
    EU AI Act Notices (TASK-011)      :t011, after t006, 10d
    Cross-Browser Testing (TASK-012)  :t012, after t010, 7d
```

---

## 10. Agent Interaction Matrix — Who Talks To Whom

```mermaid
graph LR
    subgraph PRODUCT["Product Dept"]
        CPO["CPO"]
        PM["PM"]
        DL["Design Lead"]
        UXR["UX Researcher"]
    end

    subgraph ENGINEERING["Engineering Dept"]
        CTO["CTO"]
        FE["FE Lead"]
        BE["BE Lead"]
        QA["QA Lead"]
        SEC["Security"]
        DO["DevOps"]
    end

    subgraph OPERATIONS["Operations Dept"]
        COO["COO"]
        COM["Commerce"]
        FUL["Fulfillment"]
        CMP["Compliance"]
    end

    CEO["CEO (Wole)"]

    %% Cross-department collaboration lines
    CPO <--> CTO
    CPO --> PM
    CPO --> DL
    DL --> FE
    PM --> FE
    PM --> BE
    CTO --> FE
    CTO --> BE
    CTO --> QA
    FE --> QA
    BE --> QA
    QA --> DO
    SEC --> DO
    CMP --> CPO
    CMP --> SEC
    COM --> BE
    COM --> FUL
    FUL --> BE
    UXR --> DL
    UXR --> FE

    %% CEO gates
    CEO -.->|"gates"| CPO
    CEO -.->|"gates"| CTO
    CEO -.->|"gates"| COO

    style CEO fill:#FFD700,stroke:#333,stroke-width:3px,color:#000
    style PRODUCT fill:#f3e8ff,stroke:#8B5CF6
    style ENGINEERING fill:#dbeafe,stroke:#3B82F6
    style OPERATIONS fill:#ccfbf1,stroke:#14B8A6
```

---

## 11. Sprint 1 — FamiliTrail Agent Collaboration

Shows which agents collaborate on each FamiliTrail task and handoff points.

```mermaid
sequenceDiagram
    actor CEO as CEO (Wole)
    participant FE as FE Lead
    participant QA as QA Lead
    participant DL as Design Lead
    participant UXR as UX Researcher

    Note over CEO,UXR: TASK-016: Trail Analytics (P1, Effort: S)
    FE->>FE: Add trackAction() to TrailTooltip,<br/>PeekPreview, FamilyTrailCanvas
    FE->>QA: Handoff: verify events fire correctly

    Note over CEO,UXR: TASK-017: Trail Persistence (P1, Effort: S)
    FE->>FE: fl:trail_visited localStorage +<br/>visited node glow on TrailNode
    FE->>QA: Handoff: verify persistence + visual

    Note over CEO,UXR: TASK-022: Achievement Badges (P2, depends 017)
    DL->>FE: Badge designs (3 tiers)
    FE->>FE: Toast notifications +<br/>badge on trail header
    FE->>QA: Handoff: verify badge logic

    Note over CEO,UXR: TASK-023: A/B Test (P2, depends 022)
    UXR->>FE: Test hypothesis + metrics
    FE->>FE: VITE_TRAIL_DEFAULT_LANDING flag
    FE->>UXR: Results after 2 weeks
```

---

## 12. Sprint 1 — FamiliVault Agent Collaboration

Shows the multi-agent workflow for VaultCard consolidation and downstream tasks.

```mermaid
sequenceDiagram
    actor CEO as CEO (Wole)
    participant CTO as CTO
    participant FE as FE Lead
    participant QA as QA Lead
    participant DL as Design Lead
    participant COM as Commerce Lead

    Note over CEO,COM: TASK-018: Vault Consolidation (P1, Effort: M) — UNLOCKS 4 TASKS
    CTO->>FE: Architecture: unified VaultCard with mode prop<br/>(interactive vs print)
    FE->>FE: Merge standalone + keepsake VaultCard<br/>Unified rarity (6 tiers)
    FE->>FE: Update templateRegistry + printProfiles
    FE->>QA: Handoff: all modes, all rarities

    par Parallel after TASK-018
        Note over FE: TASK-019: Wire Percentiles (P1)
        FE->>FE: Map calibrated_features →<br/>featureStars (percentile→star)

        Note over FE,COM: TASK-021: Physical Printing (P1)
        FE->>COM: Print-ready at 300 DPI?
        COM->>FE: Prodigi SKU CLASSIC-POST-GLOS-6X4
        FE->>FE: Register in Prodigi flow
    end

    Note over FE: TASK-020: Social Sharing (P1)
    FE->>FE: html2canvas → PNG → Web Share API

    QA->>QA: Write tests for unified VaultCard
    QA->>CEO: Test report (all modes, all rarities)

    Note over CEO: GATE: Ship approval
```

---

## 13. Task Dependency Graph — Agent Ownership

Visual map of task dependencies colour-coded by owning agent.

```mermaid
flowchart TD
    subgraph TRAIL["FamiliTrail Tasks"]
        T16["TASK-016<br/>Analytics<br/>🟢 fe_lead"]
        T17["TASK-017<br/>Persistence<br/>🟢 fe_lead"]
        T22["TASK-022<br/>Achievements<br/>🟡 fe + design"]
        T23["TASK-023<br/>A/B Test<br/>🟡 fe + ux"]
        T27["TASK-027<br/>Seasonal<br/>🔵 design + fe"]
        T28["TASK-028<br/>Confetti<br/>🔵 fe_lead"]
    end

    subgraph VAULT["FamiliVault Tasks"]
        T18["TASK-018<br/>Consolidate<br/>🟢 fe + cto"]
        T19["TASK-019<br/>Percentiles<br/>🟢 fe_lead"]
        T20["TASK-020<br/>Sharing<br/>🟢 fe_lead"]
        T21["TASK-021<br/>Printing<br/>🟢 fe + commerce"]
        T24["TASK-024<br/>Collection<br/>🟡 fe + design"]
        T25["TASK-025<br/>Card Back<br/>🟡 fe_lead"]
        T26["TASK-026<br/>Pack Anim<br/>🟡 fe + design"]
        T29["TASK-029<br/>FamiliClash<br/>🔵 cpo + fe"]
        T30["TASK-030<br/>FamiliLegacy<br/>🔵 cpo + fe"]
    end

    T17 --> T22
    T22 --> T23
    T22 --> T28

    T18 --> T19
    T18 --> T20
    T18 --> T21
    T18 --> T24
    T18 --> T25
    T24 --> T26
    T18 --> T29
    T18 --> T30

    style T16 fill:#22C55E,color:#fff
    style T17 fill:#22C55E,color:#fff
    style T18 fill:#22C55E,color:#fff
    style T19 fill:#22C55E,color:#fff
    style T20 fill:#22C55E,color:#fff
    style T21 fill:#22C55E,color:#fff
    style T22 fill:#EAB308,color:#000
    style T23 fill:#EAB308,color:#000
    style T24 fill:#EAB308,color:#000
    style T25 fill:#EAB308,color:#000
    style T26 fill:#EAB308,color:#000
    style T27 fill:#3B82F6,color:#fff
    style T28 fill:#3B82F6,color:#fff
    style T29 fill:#3B82F6,color:#fff
    style T30 fill:#3B82F6,color:#fff
```

Legend: Green = P1 (this sprint), Yellow = P2 (next sprint), Blue = P3 (future)

---

## 14. Agent Communication Patterns

How artifacts flow between agents during execution.

```mermaid
flowchart TD
    subgraph SPEC["Spec Phase"]
        CPO_W["CPO<br/>PRD + acceptance criteria"]
        PM_W["PM<br/>User stories + effort"]
        CMP_W["Compliance<br/>Regulatory check"]
    end

    subgraph DESIGN["Design Phase"]
        CTO_W["CTO<br/>Architecture doc"]
        DL_W["Design Lead<br/>UI mockup / motion spec"]
    end

    subgraph BUILD["Build Phase"]
        FE_W["FE Lead<br/>React components + tests"]
        BE_W["BE Lead<br/>API endpoints + tests"]
    end

    subgraph VERIFY["Verify Phase"]
        QA_W["QA Lead<br/>Test report"]
        SEC_W["Security<br/>Audit report"]
    end

    subgraph SHIP["Ship Phase"]
        DO_W["DevOps<br/>Deploy + smoke test"]
        COO_W["COO<br/>Status report"]
    end

    CPO_W -->|"PRD"| PM_W
    CPO_W -->|"PRD"| CMP_W
    PM_W -->|"stories"| CTO_W
    CMP_W -->|"verdict"| CTO_W
    CTO_W -->|"arch doc"| FE_W
    CTO_W -->|"arch doc"| BE_W
    DL_W -->|"UI spec"| FE_W
    FE_W -->|"code"| QA_W
    BE_W -->|"code"| QA_W
    FE_W -->|"code"| SEC_W
    BE_W -->|"code"| SEC_W
    QA_W -->|"pass"| DO_W
    SEC_W -->|"clear"| DO_W
    DO_W -->|"live"| COO_W

    GATE1{{"CEO GATE 1<br/>Approve Scope"}}
    GATE2{{"CEO GATE 2<br/>Approve Ship"}}

    PM_W --> GATE1
    CMP_W --> GATE1
    GATE1 --> CTO_W
    GATE1 --> DL_W
    QA_W --> GATE2
    SEC_W --> GATE2
    GATE2 --> DO_W

    style GATE1 fill:#FFD700,stroke:#333,stroke-width:2px
    style GATE2 fill:#FFD700,stroke:#333,stroke-width:2px
    style SPEC fill:#f3e8ff,stroke:#8B5CF6
    style DESIGN fill:#dbeafe,stroke:#3B82F6
    style BUILD fill:#dcfce7,stroke:#22C55E
    style VERIFY fill:#fef3c7,stroke:#EAB308
    style SHIP fill:#d1fae5,stroke:#10B981
```

---

## 15. Three Crew Systems — How They Interoperate

```mermaid
flowchart LR
    subgraph MAIN["Crew System (Claude Code Native)"]
        direction TB
        ORC["Orchestrator"]
        A14["14 Business Agents"]
        ORC --> A14
    end

    subgraph AD["Ad Crew (CrewAI)"]
        direction TB
        BS["Brand Strategist"]
        CW["Copywriter"]
        VD["Visual Director"]
        SM["Social Media Mgr"]
        CS["Conversion Specialist"]
        IS["Influencer Scout"]
        PR["PR Agent"]
        SEO["SEO Specialist"]
    end

    subgraph OPS["Ops Agents (CrewAI)"]
        direction TB
        SPEC["Spec Agent"]
        DEV["Developer Agent"]
        GK["Gatekeeper Agent"]
        CG["Contract Guardian"]
        CC["Commit Controller"]
        SPEC --> DEV --> GK --> CG --> CC
    end

    CEO["CEO (Wole)"]

    CEO --> MAIN
    MAIN -->|"/crew campaign"| AD
    MAIN -->|"code patches"| OPS
    OPS -->|"validated diffs"| MAIN
    AD -->|"campaign assets"| MAIN

    style CEO fill:#FFD700,stroke:#333,stroke-width:3px,color:#000
    style MAIN fill:#dbeafe,stroke:#3B82F6
    style AD fill:#fce7f3,stroke:#EC4899
    style OPS fill:#d1fae5,stroke:#10B981
```

---

## 16. Current Sprint Gantt — Agent Assignments

```mermaid
gantt
    title Sprint 1 — FamiliTrail + FamiliVault Hardening
    dateFormat YYYY-MM-DD
    axisFormat %d %b

    section FamiliTrail
    TASK-016 Analytics (fe_lead)        :t16, 2026-03-21, 1d
    TASK-017 Persistence (fe_lead)      :t17, after t16, 1d

    section FamiliVault
    TASK-018 Consolidate (cto + fe)     :t18, 2026-03-21, 3d
    TASK-019 Percentiles (fe_lead)      :t19, after t18, 1d
    TASK-020 Sharing (fe_lead)          :t20, after t18, 1d
    TASK-021 Printing (fe + commerce)   :t21, after t18, 1d

    section QA
    Trail tests (qa_lead)              :qt, after t17, 1d
    Vault tests (qa_lead)              :qv, after t21, 2d
```

---

## How to View These Diagrams

1. **VS Code** (recommended): Open this file — Mermaid renders in the built-in markdown preview (Ctrl+Shift+V)
2. **Mermaid Live**: Copy any `mermaid` block to https://mermaid.live
3. **GitHub**: Push this file — GitHub renders Mermaid natively in markdown
4. **Export**: Use Mermaid CLI (`mmdc`) to export as PNG/SVG/PDF
