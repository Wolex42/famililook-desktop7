# Claude Code Project Instructions - FML (Famililook)

## Response Quality Rules (NON-NEGOTIABLE)

### Never Declare Absence Without Exhaustive Search
Before saying something "doesn't exist" or "wasn't found":
1. Search `C:\Users\wole\Documents\FML\` (authoritative working copy)
2. Search ALL file types: `.py`, `.md`, `.yaml`, `.json`, `.jsx`, `.js`
3. Check git history (`git log -S`, `git log --grep`)
4. Check memory files in `.claude/projects/`
5. Use parallel search agents for thoroughness
6. If still not found, say "I haven't found it yet" — NOT "it doesn't exist"

### Never State Status Without Reading Memory (NON-NEGOTIABLE)

Before listing blockers, open issues, or project status in ANY summary:
1. READ the relevant memory files (commerce_status.md, vendor_integrations.md, security_status.md, etc.)
2. Do NOT generate status from conversational recall or stale context
3. If you cannot read the file first, say "let me check" — NEVER guess
4. This applies to: "where to next" lists, priority summaries, blocker lists, status updates

**Violation of this rule wastes user time, erodes trust, and burns tokens on corrections.**

### Verify Before Escalating (NON-NEGOTIABLE)

Before flagging ANYTHING as a problem, broken, or needing attention:
1. CHECK PRODUCTION FIRST — curl the URL, test the endpoint, verify the service
2. If production works, local state issues are informational only — mention briefly, do not investigate unless asked
3. READ memory files for context — the issue may already be known, resolved, or intentional
4. Do NOT ask the user to explain something you can verify yourself
5. Do NOT raise alarms then investigate — investigate FIRST, report findings AFTER

**Pattern to avoid:** "I found X missing/broken!" → user spends time → "actually it's fine." This wastes time and erodes trust.

### Store Outcomes to Memory (NON-NEGOTIABLE)

After completing ANY task that changes the state of the system:
1. UPDATE the relevant memory file immediately (security_status.md, commerce_status.md, etc.)
2. Record WHAT was done, WHEN, and the RESULT
3. If a blocker was resolved, mark it as resolved IN MEMORY — not just in conversation
4. Future conversations MUST be able to find the current state by reading memory alone

### Agent System — 15 Native Personas (v3.0)
All agents are Claude Code native personas in `Agent_1/crew/agents/*.md` — zero API cost.
Orchestrator: `Agent_1/crew/orchestrator.md`
CrewAI agents (ad_crew, ops_agents) are SUPERSEDED — do not reference them.

**15 agents across 5 levels:**

| Level | Agent | File |
|-------|-------|------|
| System | Platform Architect | `agents/platform_architect.md` |
| System | Mobile Solutions Architect | `agents/mobile_solutions_architect.md` |
| System | Game Engine Architect | `agents/game_engine_architect.md` |
| Lead | FE Lead | `agents/fe_lead.md` |
| Lead | BE Lead | `agents/be_lead.md` |
| Lead | Native App Lead | `agents/native_app_lead.md` |
| Solutions | Data Solutions Architect | `agents/data_solutions_architect.md` |
| Solutions | Shared Infrastructure Lead | `agents/shared_infrastructure_lead.md` |
| Quality | QA Lead | `agents/qa_lead.md` |
| Governance | Change Manager | `agents/change_manager.md` |
| Operations | COO | `agents/coo.md` |
| Marketing | CMO | `agents/cmo.md` |
| Marketing | Copywriter | `agents/copywriter.md` |
| Marketing | Visual Director | `agents/visual_director.md` |
| Marketing | Growth Monitor | `agents/growth_monitor.md` |

**Crew commands:**
`/crew fix`, `/crew redesign`, `/crew feature`, `/crew sprint`, `/crew review`,
`/crew audit`, `/crew deploy`, `/crew release`, `/crew briefing`, `/crew status`,
`/crew mobile` (NEW), `/crew multiplayer` (NEW), `/crew migrate` (NEW),
`/crew analytics` (NEW), `/crew campaign`, `/crew marketing`, `/crew changes`, `/crew roadmap`

### Thoroughness Over Speed
- When asked about what exists in the codebase: search deeply, not quickly
- When asked to build something: check if it already exists first
- When uncertain: say so and search more, don't guess
- Use the Agent tool with parallel searches when the question spans multiple directories

---

## Repository & Deployment Rules (NON-NEGOTIABLE)

### Single Working Copy
- **`C:\Users\wole\Documents\FML`** is the ONLY repo for git operations (commit, push, deploy)
- **`C:\Users\wole\OneDrive\FML`** is read-only reference — NO git operations
- Violating this causes production branch divergence (incident 2026-03-27)

### Deployment Process
All products deploy via merging `main` into `production` branch. Vercel auto-builds on push.
```bash
# From Documents working copy ONLY:
git checkout production
git merge main
git push origin production
git checkout main
```

### Product Repos

| Product | FE Repo | BE | Prod Domain | Port |
|---|---|---|---|---|
| **FamiliLook** | desktop2 | desktop3 | famililook.com | 8008 |
| **FamiliUno** | desktop2 (/uno route) | desktop3 | famililook.com/uno | 8008 |
| **FamiliPoker** | desktop4 | desktop5 | famililook-desktop4.vercel.app | 8008 |
| **FamiliMatch** | desktop6 | desktop7 | famililook-desktop6.vercel.app | 8008 |

**Shared packages (NEW):**

| Package | Repo | Type | Consumed by |
|---------|------|------|------------|
| famililook-shared | `famililook-shared/` | npm | desktop2, desktop4, desktop6 |
| famililook-game-engine | `famililook-game-engine/` | pip | desktop5, desktop7 |

- desktop2/3/4/5/6/7 are independent repos (NOT submodules)
- desktop3 is the shared ML backend for all products
- desktop5 is the game server for FamiliPoker + FamiliUno (WebSocket)
- desktop7 is the game server for FamiliMatch (WebSocket, proxies ML to desktop3)
- FamiliMatch has a categorically different audience — NEVER consolidate into FamiliLook

### Umbrella App Strategy
All four products ship as a single Capacitor app with four tabs:
- Tab 1: FamiliLook (entry point)
- Tab 2: FamiliMatch
- Tab 3: FamiliUno (unlocks after first analysis)
- Tab 4: FamiliPoker (Plus tier only)

### Cross-Product Navigation
All navigation TO `/uno` must include a `?from=` param so the back button returns users correctly:
- `?from=results` → back to `/` (analysis results)
- `?from=trail` → back to `/trail`
- `?from=hub` → back to `/hub`
- `?from=home` → back to `/`
- No param → defaults to `/hub`

Apply the same pattern when adding navigation to `/poker` or `/match` (future).

---

## Critical Guardrails

### Backend File Protection (NON-NEGOTIABLE)

**DO NOT modify any backend files without explicit user permission.**

Backend files requiring explicit CEO permission per session:
- `famililook-desktop3/` — shared ML backend (all .py files)
- `famililook-desktop5/` — FamiliPoker/Uno game server (all .py files)
- `famililook-desktop7/` — FamiliMatch game server (all .py files)
- `famililook-game-engine/` — shared game engine package (all .py files)
- Any `*.py` file anywhere in the repo tree
- Any files in `/api/`, `/backend/`, `/server/` directories

**Permission rules:**
1. STOP and ASK: "This file appears to be a backend file. Do I have permission to modify it?"
2. Wait for explicit "yes" or permission before proceeding
3. Permission granted in a previous session does NOT carry over to a new session
4. When granting permission, CEO states: "Backend permission granted for [specific task] in [specific repo] in this session only"
5. If in doubt, ASK — do not assume permission

**Additional rules for shared packages:**
- Changes to `famililook-game-engine/` require CEO permission AND Game Engine Architect review
- Changes to `famililook-desktop3/routes/` that touch frozen contract schemas require CEO + CTO sign-off (P0)

---

## Shared Package Rules (NON-NEGOTIABLE)

### famililook-shared (npm package)
Location: `C:\Users\wole\Documents\FML\famililook-shared\`
Consumed by: desktop2, desktop4, desktop6

Any change to famililook-shared is **P1 minimum** — it affects ALL consuming repos simultaneously.

Before editing any file in famililook-shared:
1. Platform Architect or Shared Infrastructure Lead must assess cross-repo impact
2. Show diff preview to CEO and wait for approval
3. After applying: QA Lead must run regression tests in ALL consuming repos (desktop2, desktop4, desktop6) — not just one
4. Change Manager must log the change against ALL affected repos

**Never remove or rename an exported function or component without a migration plan** — this breaks all consumers simultaneously. Adding new exports is safe. Changing or removing existing ones is P1.

### famililook-game-engine (pip package)
Location: `C:\Users\wole\Documents\FML\famililook-game-engine\`
Consumed by: desktop5, desktop7

Same P1 rules as famililook-shared.
Additionally: Game Engine Architect must review any change to rooms, protocol, or reconnection modules before BE Lead implements.

### Structural Modules (cross-cutting — owned by Platform Architect)
These modules, once built, make entire categories of bugs impossible. No agent may bypass them:

| Module | Location | Status | Bypass = |
|--------|----------|--------|---------|
| AppErrorBus | famililook-shared/infrastructure/ | NOT BUILT | Silent catch block → P1 violation |
| AppStorage | famililook-shared/infrastructure/ | NOT BUILT | Direct localStorage call → P1 violation |
| resultsContract.js | famililook-shared/infrastructure/ | NOT BUILT | Winner logic outside this file → P1 violation |

Once built: any new `catch {}`, direct `localStorage.getItem/setItem`, or winner derivation outside resultsContract.js is a governance violation that Change Manager must flag and block.

---

## Cross-Repo Change Logging (NON-NEGOTIABLE)

When a change in one repo affects another repo's behaviour:

1. Log the change in the repo where the edit was made (normal process)
2. Add a cross-reference entry in every affected repo's change_log.md:
   ```
   ### [date] — Cross-repo impact from [source repo] change [CR-NNNN]
   Description: No local files changed. Behaviour affected: [what changed and why]
   Action: [what consuming repos must do — e.g. update dependency, run tests]
   ```
3. Change Manager identifies and logs ALL cross-repo impacts — not just the agent who made the edit
4. QA Lead runs tests in ALL affected repos even if no files were edited in that repo

**change_log.md must exist in every active repo.** Current status:

| Repo | change_log exists? | Action required |
|------|--------------------|----------------|
| famililook-desktop2 | YES | — |
| famililook-desktop3 | NO | Create `.claude/change_log.md` |
| famililook-desktop4 | YES | — |
| famililook-desktop5 | NO | Create `.claude/change_log.md` |
| famililook-desktop6 | NO | Create `.claude/change_log.md` |
| famililook-desktop7 | NO | Create `.claude/change_log.md` |
| famililook-shared | NOT YET CREATED | Create with package |
| famililook-game-engine | NOT YET CREATED | Create with package |
| FML (parent) | YES | — |

Creating missing change_logs is a Change Manager task. Do it before any work begins in those repos.

---

## Native App File Governance (NON-NEGOTIABLE)

Once Capacitor is initialised, these files require Native App Lead review before any edit:

| File | Risk | Rule |
|------|------|------|
| `capacitor.config.ts` | Any change affects both iOS and Android | Native App Lead reviews + CEO approval |
| `ios/App/App/Info.plist` | Wrong entries cause App Store rejection | Native App Lead reviews + CEO approval |
| `android/app/src/main/AndroidManifest.xml` | Wrong entries cause Play Store rejection | Native App Lead reviews + CEO approval |

Before modifying any native config file:
1. Read the current Mobile Solutions Architect spec (`crew/output/MOBILE_SOLUTIONS_ARCH_*.md`)
2. Confirm the change matches the spec exactly
3. Show diff preview to CEO
4. Wait for explicit approval

**Never add `UIBackgroundModes` to Info.plist without Mobile Solutions Architect explicit approval.** Background mode declarations are scrutinised by App Store reviewers. Declaring modes not in use causes rejection.

**Never add permissions not required by active features.** Both platforms flag unused permission declarations.

---

## Platform Submission Gate (NON-NEGOTIABLE)

No App Store or Google Play submission without ALL of the following:

1. QA Lead sign-off on the specific build being submitted
2. Native App Lead submission readiness report (all checklist items GREEN)
3. CEO explicit approval: `"Approved for [App Store | Google Play] submission — version [X.Y.Z] build [N]"`
4. Change Manager logs the submission as a P1 change

**Submission is irreversible.** Once submitted, do not submit an update until either:
- The submission is approved (then submit next version normally through this gate)
- The submission is rejected (fix the rejection reason, resubmit through this gate)

Never submit two versions simultaneously to the same platform.

**Physical products (keepsakes, card decks) are exempt from platform billing rules.** Only digital subscriptions (Plus/Pro) must use Apple IAP and Google Play Billing when purchased inside the app. Stripe stays for all physical product orders.

---

## Dependency Version Governance (NON-NEGOTIABLE)

desktop2 is the canonical version reference for all shared frontend dependencies. All consuming repos must stay aligned.

| Package | Canonical version | Current desktop4 | Current desktop6 | Action |
|---------|------------------|-----------------|-----------------|--------|
| react | ^18.3.1 | ^18.3.1 ✅ | ^18.3.1 ✅ | — |
| react-dom | ^18.3.1 | ^18.3.1 ✅ | ^18.3.1 ✅ | — |
| react-router-dom | ^7.9.5 | ^7.9.5 ✅ | **^7.1.1 ❌** | Align desktop6 |
| framer-motion | ^12.34.3 | **^11.0.0 ❌** | **^11.0.0 ❌** | Align desktop4+6 |

**Rules:**
1. When desktop2 upgrades a shared dependency: Platform Architect assesses cross-repo impact, all other repos align in the same sprint
2. Never upgrade a dependency in one repo without a plan to align all others
3. Divergence is flagged by Change Manager in every COO briefing until resolved
4. Once famililook-shared is active, shared dependencies are declared as peerDependencies in the package — consuming repos must use the same version

---

## BE/FE Contract Stability Rules

These contracts are STABLE and must NOT be broken:

### 1. Winner Determination (5-3 Rule)
- Backend determines winner based on feature votes
- 5+ features for a parent = that parent wins
- Frontend TRUSTS backend's `winner` field - NEVER re-derive it

### 2. Order Invariance
- If Parent A becomes Parent B, the winner LABEL changes but the REAL winner stays the same
- Swapping parent order must NOT change who actually won
- Backend handles this - frontend just displays what backend says

### 3. 8-Feature Requirement
- ALL analyses must have 8 features: eyes, eyebrows, smile, nose, face_shape, skin, hair, ears
- Every feature has a parent winner (no ties at feature level)
- Unknown features are tracked separately, not assigned to either parent

### 4. Cardinal Rule: No 50/50
- NEVER display 50/50 percentages
- Always nudge to show winner's margin (minimum 51/49)
- Backend winner is authoritative for which side gets the nudge

### 5. Feature Count Invariant
- `mumFeatureCount + dadFeatureCount + unknownFeatureCount === 8` (always)
- Unknown features don't count toward either parent's total

### 6. Compatibility Mode — No Kinship Framing (compare_faces.v1)
- FamiliMatch (Solo/Duo/Group) MUST use `/compare/faces` — NEVER `/kinship/analyze`
- All scoring is backend-authoritative: `0.6 * embedding_sim + 0.4 * feature_sim`
- Frontend MUST NOT re-derive `percentage`, `chemistry_label`, or `feature_comparisons`
- All inputs are real face metrics — no synthetic, fabricated, or placeholder values
- Response always has exactly 8 `feature_comparisons` entries
- `embedding_similarity` and `feature_similarity` are both floats in [0.0, 1.0]
- Symmetry invariant: swapping `face_a`/`face_b` produces the same `percentage`

### 7. WebSocket Protocol (compare_faces.v1 extension — multiplayer)
- All WebSocket messages use the canonical envelope from famililook-game-engine
- Game servers NEVER re-derive analysis results — they proxy to desktop3
- All WebSocket connections use WSS (wss://) in production — never plain WS
- Room state is server-authoritative — clients are displays, not state owners

---

## API Contract (kinship_analyze.v1) — FamiliLook

Response schema: `contracts/kinship_analyze.v1.schema.json`

Key fields:
```json
{
  "ok": boolean,
  "schema_version": "kinship_analyze.v1",
  "engineResult": {
    "mode": string,
    "parents": { "parent1": {...}, "parent2": {...} },
    "children": [{
      "name": string,
      "inheritance": {
        "winner": "parent1" | "parent2" | "blend" | "unknown",
        "winner_reason": string
      },
      "feature_votes": {
        "eyes": "parent1" | "parent2",
        "eyebrows": "parent1" | "parent2",
        // ... 8 features total
      }
    }]
  }
}
```

---

## API Contract (compare_faces.v1) — FamiliMatch ONLY ⚡ FROZEN

Response schema: `contracts/compare_faces.v1.schema.json`

Key fields:
```json
{
  "ok": true,
  "percentage": integer,            // [0, 100]
  "chemistry_label": string,        // "Feature Twins" | "Magnetic Match" | "Complementary Pair" | "Interesting Contrast" | "Opposites Attract"
  "chemistry_color": string,        // hex: #FFD700 | #8B5CF6 | #3B82F6 | #14B8A6 | #F97316
  "embedding_similarity": number,   // [0.0, 1.0] — symmetric cosine
  "feature_similarity": number,     // [0.0, 1.0] — fraction of 8 label matches
  "feature_comparisons": [          // ALWAYS exactly 8 items
    { "feature": string, "label_a": string, "label_b": string, "match": boolean }
  ],
  "shared_features": [string],      // subset of 8 feature keys where match=true
  "calibrated_a": object,           // full calibrate_all_features() output for face_a
  "calibrated_b": object,           // full calibrate_all_features() output for face_b
  "name_a": string,
  "name_b": string
}
```

**Hard invariants (enforced by tests):**
- `feature_comparisons.length === 8` always
- `percentage === round(clamp(0.6 * embedding_sim + 0.4 * feature_sim, 0, 1) * 100)`
- `shared_features` exactly matches `feature_comparisons.filter(c => c.match).map(c => c.feature)`
- `chemistry_label` and `chemistry_color` are consistent with `percentage` thresholds

---

## Frontend Architecture

### Critical Files (desktop2)
- `src/layout/MobileResultsSection.jsx` - Winner display logic
- `src/components/results/MobileResultsCarousel.jsx` - Feature display + FamiliUno deck button
- `src/state/FamililookContext.jsx` - App state (PROTECTED — Platform Architect review required)
- `src/state/EmotionalJourneyContext.jsx` - Celebration system
- `src/pages/FamiliUnoPage.jsx` - Card deck with back navigation (`?from=` aware)
- `src/layout/AppLayout.jsx` - Main layout, settings, navigation
- `src/hooks/usePlanFeatures.js` - Authoritative plan source (not FamililookContext.currentPlan)

### Protected Files (require Platform Architect review before FE Lead edits)
- `src/state/FamililookContext.jsx`
- `src/state/BasketContext.jsx`
- `src/hooks/useKinshipAnalysis.jsx`
- `src/utils/analytics.js`
- Any file with direct `localStorage.getItem` / `localStorage.setItem` calls (once AppStorage is built)
- Any file with bare `catch {}` blocks (once AppErrorBus is built)

### famililook-shared Components (once built — import from package, never reimplement)
- `@famililook/shared/infrastructure/AppErrorBus`
- `@famililook/shared/infrastructure/AppStorage`
- `@famililook/shared/infrastructure/resultsContract`
- `@famililook/shared/components/ErrorBoundary`
- `@famililook/shared/components/ConsentGate`
- `@famililook/shared/components/PlanGate`
- `@famililook/shared/hooks/usePlanFeatures`
- `@famililook/shared/hooks/useAnalytics`
- `@famililook/shared/hooks/useFromParam`
- `@famililook/shared/hooks/useWebSocket`
- `@famililook/shared/theme/colors`

### UI Guidelines
- iOS Human Interface Guidelines compliance
- 44pt minimum touch targets
- Native scrolling behavior
- No horizontal scroll on cards
- Brand: violet #7C3AED / #4F46E5 (FamiliLook), green-blue #30d158 (FamiliUno)
- Safe area insets required on all sticky/fixed elements: `env(safe-area-inset-bottom)`

---

## Testing Requirements

### Frontend (per repo)
Before any PR:
1. `npm run test:run` — unit tests pass
2. `npm run build` — build succeeds
3. `npx playwright test` — E2E tests pass (desktop2 and desktop4 only — desktop6 needs E2E added)
4. Manual verification of:
   - 8 features display correctly
   - Winner matches feature majority
   - No 50/50 displays
   - Order invariance maintained

### Shared Package Testing (famililook-shared)
When any change is made to famililook-shared:
1. Run tests within the package itself
2. Run `npm run test:run` in ALL consuming repos (desktop2, desktop4, desktop6)
3. All three must pass before the shared package change is considered done
4. QA Lead signs off on cross-repo regression — not just the repo where the edit was made

### Backend (per repo)
1. `pytest tests/ -v` — all tests pass
2. No new silent exception handlers (`catch: pass` or equivalent)
3. All new endpoints Pydantic-validated

### Mobile (before any Capacitor submission)
1. TestFlight internal testing: minimum 5 sessions, zero crashes (iOS)
2. Google Play Internal Testing: minimum 3 sessions (Android)
3. Device verification by CEO on physical phone
4. Native App Lead submission readiness report: all items GREEN

---

## Enforcement Layer (Governance)

### Files
- `.claude/guardrails.json` — Rules and invariants
- `.claude/validate_scope.py` — File access validator (must be updated for new repos)
- `.claude/patch_validator.py` — Edit validation
- `.claude/working_set.txt` — Allowed files for current task (must include new repos when relevant)
- `.claude/pre-commit-hook.sh` — Regression gate (must be installed in ALL repos)
- `.claude/change_log.md` — Quick reference audit trail (must exist in ALL repos)

### Pre-commit Hook Status
| Repo | Hook installed? | Action |
|------|----------------|--------|
| desktop2 | YES | — |
| desktop3 | UNKNOWN | Verify + install |
| desktop4 | YES | — |
| desktop5 | NO | Install |
| desktop6 | YES | — |
| desktop7 | NO | Install |
| famililook-shared | NOT YET | Install when created |
| famililook-game-engine | NOT YET | Install when created |

---

## MANDATORY PRE-EDIT CHECKLIST (NON-NEGOTIABLE)

**Claude MUST complete this checklist BEFORE using the Edit tool.**
**Failure to follow this process is a governance violation.**

### Step 1: Validate Scope (MUST RUN FIRST)
```bash
python .claude/validate_scope.py "<file_path>" --mode edit
```
- Exit 0 = ALLOWED — proceed to Step 2
- Exit 1 = BLOCKED — STOP, do not edit
- Exit 2 = REQUIRES_APPROVAL — ASK user before proceeding

**Additional checks before Step 2:**
- Is this a backend (.py) file? → Confirm explicit CEO backend permission for this session
- Is this a shared package file (famililook-shared/ or famililook-game-engine/)? → Platform Architect or Game Engine Architect must have reviewed
- Is this a native app config file (Info.plist, AndroidManifest.xml, capacitor.config.ts)? → Native App Lead must have reviewed
- Has this file been patched 2+ times in 30 days? → QA Lead triage required
- Has this file been patched 3+ times? → HALT, route to /crew redesign

### Step 2: Show Diff Preview
Before applying any edit, Claude MUST:
1. Show the user the exact `old_string` to be replaced
2. Show the user the exact `new_string` replacement
3. Explain what the change does in one sentence

### Step 3: Wait for Approval
- Do NOT apply the edit until user confirms
- User must explicitly approve with "yes", "approved", "proceed", or similar
- Silence or ambiguity = DO NOT PROCEED

### Step 4: Apply Edit
Only after Steps 1-3 are complete, use the Edit tool.

### Step 5: Log the Change
Update `.claude/change_log.md` in the same session — not later.
If change_log.md doesn't exist in this repo: CREATE it first.
For shared package changes: log in ALL affected repos.

### Step 6: Run Tests
```bash
npm run test:run  # Frontend
npm run build     # Build check
pytest tests/ -v  # Backend (if applicable)
```
For shared package changes: run tests in ALL consuming repos.

---

### Dev Analytics Bypass (NON-NEGOTIABLE)

**DO NOT remove or modify the `if (import.meta.env.DEV) return true` line in `analytics.js → hasAnalyticsConsent()`.**

Why: In dev mode, `ConsentBanner.jsx` returns `null` (line 13), so `fl:consent` is never set in localStorage. Without the dev bypass, `hasAnalyticsConsent()` returns `false` and **silently drops ALL analytics events**, causing the dashboard to show zeros. This has been a recurring breakage — the bypass is the structural fix.

- Production GDPR consent is unaffected (bypass only fires when `import.meta.env.DEV` is true)
- If the consent banner behavior changes to show in dev, this bypass is still harmless

---

### Key Principles

1. **USER is main focus** — E2E tests after every update
2. **BE provides all data** — FE never invents results
3. **Developer sign-off** — No auto-commits, no auto-edits
4. **Backend permission** — Explicit CEO permission per session for any .py file
5. **Documents only** — All git operations from `C:\Users\wole\Documents\FML`
6. **Verify before stating** — Read memory files before citing status
7. **No regression** — No change may break existing navigation, touch targets, consent flows, or any fixed functionality. Only the CEO can authorise breaking changes. After ANY edit, verify existing behaviour still works.
8. **Shared packages are P1** — Any change to famililook-shared or famililook-game-engine affects all products simultaneously. Treat with the same care as a production deployment.
9. **Platform submissions are irreversible** — CEO approval required before any App Store or Google Play submission.
10. **Dependency alignment** — desktop2 is the canonical version reference. Divergence must be resolved in the same sprint it is identified.

---

### Working Set (Current Task)

Update `.claude/working_set.txt` when starting a new task.
Only files listed there can be modified.

**Working set entries for new repos (add when task requires):**

```
# Shared package work
famililook-shared/src/

# Game engine work
famililook-game-engine/

# Native app work (after Capacitor init)
famililook-desktop2/capacitor.config.ts
famililook-desktop2/ios/App/App/Info.plist
famililook-desktop2/android/app/src/main/AndroidManifest.xml

# FamiliPoker game server
famililook-desktop5/app/

# FamiliMatch game server
famililook-desktop7/app/
```
