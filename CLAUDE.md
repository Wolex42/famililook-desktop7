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

### Agent System — 30 Native Personas
All agents are Claude Code native personas in `Agent_1/crew/agents/*.md` — zero API cost.
- 5 teams: product (4), engineering (6), operations (5), marketing (9), patch_cycle (6)
- Orchestrator: `Agent_1/orchestrator/orchestrator.py`
- CrewAI agents (ad_crew, ops_agents) are SUPERSEDED — do not reference them

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
| **FamiliPoker** | desktop4 | desktop3 | famililook-desktop4.vercel.app | 8008 |
| **FamiliMatch** | desktop6 | desktop3 | famililook-desktop6.vercel.app | 8008 |

- desktop2/3/4/5/6 are independent repos (NOT submodules)
- All share desktop3 as ML backend
- FamiliMatch has a categorically different audience — NEVER consolidate into FamiliLook

### Cross-Product Navigation
All navigation TO `/uno` must include a `?from=` param so the back button returns users correctly:
- `?from=results` → back to `/` (analysis results)
- `?from=trail` → back to `/trail`
- `?from=hub` → back to `/hub`
- `?from=home` → back to `/`
- No param → defaults to `/hub`

Apply the same pattern when adding navigation to `/poker` (future).

---

## Critical Guardrails

### Backend File Protection (NON-NEGOTIABLE)

**DO NOT modify any backend files without explicit user permission.**

Backend directories that require explicit permission:
- `famililook-desktop3/` (Python backend)
- Any `*.py` files
- Any files in `/api/`, `/backend/`, `/server/` directories

Before modifying any backend file:
1. STOP and ASK the user: "This file appears to be a backend file. Do I have permission to modify it?"
2. Wait for explicit "yes" or permission before proceeding
3. If in doubt, ASK - do not assume permission

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
- `src/state/FamililookContext.jsx` - App state
- `src/state/EmotionalJourneyContext.jsx` - Celebration system
- `src/pages/FamiliUnoPage.jsx` - Card deck with back navigation (`?from=` aware)
- `src/layout/AppLayout.jsx` - Main layout, settings, navigation
- `src/hooks/usePlanFeatures.js` - Authoritative plan source (not FamililookContext.currentPlan)

### UI Guidelines
- iOS Human Interface Guidelines compliance
- 44pt minimum touch targets
- Native scrolling behavior
- No horizontal scroll on cards
- Brand: violet #7C3AED / #4F46E5 (FamiliLook), green-blue #30d158 (FamiliUno)

---

## Testing Requirements

Before any PR:
1. `npm run test:run` - Unit tests pass
2. `npm run build` - Build succeeds
3. `npx playwright test` - E2E tests pass
4. Manual verification of:
   - 8 features display correctly
   - Winner matches feature majority
   - No 50/50 displays
   - Order invariance maintained

---

## Enforcement Layer (Governance)

### Files
- `.claude/guardrails.json` - Rules and invariants
- `.claude/validate_scope.py` - File access validator
- `.claude/patch_validator.py` - Edit validation
- `.claude/working_set.txt` - Allowed files for current task
- `.claude/pre-commit-hook.sh` - Regression gate
- `.claude/change_log.md` - Quick reference audit trail

---

## MANDATORY PRE-EDIT CHECKLIST (NON-NEGOTIABLE)

**Claude MUST complete this checklist BEFORE using the Edit tool.**
**Failure to follow this process is a governance violation.**

### Step 1: Validate Scope (MUST RUN FIRST)
```bash
python .claude/validate_scope.py "<file_path>" --mode edit
```
- Exit 0 = ALLOWED - proceed to Step 2
- Exit 1 = BLOCKED - STOP, do not edit
- Exit 2 = REQUIRES_APPROVAL - ASK user before proceeding

### Step 2: Show Diff Preview
Before applying any edit, Claude MUST:
1. Show the user the exact `old_string` to be replaced
2. Show the user the exact `new_string` replacement
3. Explain what the change does

### Step 3: Wait for Approval
- Do NOT apply the edit until user confirms
- User must explicitly approve with "yes", "approved", "proceed", or similar
- Silence or ambiguity = DO NOT PROCEED

### Step 4: Apply Edit
Only after Steps 1-3 are complete, use the Edit tool.

### Step 5: Log the Change
Update `.claude/change_log.md` for quick reference.

### Step 6: Run Tests
```bash
npm run test:run  # Frontend
npm run build     # Build check
```

---

### Dev Analytics Bypass (NON-NEGOTIABLE)

**DO NOT remove or modify the `if (import.meta.env.DEV) return true` line in `analytics.js → hasAnalyticsConsent()`.**

Why: In dev mode, `ConsentBanner.jsx` returns `null` (line 13), so `fl:consent` is never set in localStorage. Without the dev bypass, `hasAnalyticsConsent()` returns `false` and **silently drops ALL analytics events**, causing the dashboard to show zeros. This has been a recurring breakage — the bypass is the structural fix.

- Production GDPR consent is unaffected (bypass only fires when `import.meta.env.DEV` is true)
- If the consent banner behavior changes to show in dev, this bypass is still harmless

---

### Key Principles

1. **USER is main focus** - E2E tests after every update
2. **BE provides all data** - FE never invents results
3. **Developer sign-off** - No auto-commits, no auto-edits
4. **Backend permission** - Ask before .py files
5. **Documents only** - All git operations from `C:\Users\wole\Documents\FML`
6. **Verify before stating** - Read memory files before citing status
7. **No regression** - No change may break existing navigation, touch targets, consent flows, or any fixed functionality. Only the CEO can authorise breaking changes. After ANY edit, verify existing behaviour still works.

---

### Working Set (Current Task)

Update `.claude/working_set.txt` when starting a new task.
Only files listed there can be modified.
