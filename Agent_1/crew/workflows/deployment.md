# Workflow: Deployment
# Command: `/crew deploy <product>`
# Agents: change_manager, qa_lead, coo (sequential with CEO gate)
# Execution: Sequential — validate, test, approve, deploy, verify

---

## Prerequisites

- All changes committed to `main` branch
- Working copy is `C:\Users\wole\Documents\FML` (ONLY repo for git ops)
- Target product identified: desktop2, desktop4, desktop6
- No active sprint edits in progress for the target product

---

## Phase 1: Pre-Deploy Validation — Change Manager

**Agent:** `change_manager`
**Action:**
1. Run `git status` — verify clean working tree for target repo
2. Run `git log main..production` — identify what will be deployed
3. Cross-reference all commits against change_log entries
4. Verify all changes have been through a `/crew fix` or `/crew sprint` workflow
5. Classify overall deployment risk tier
6. Document rollback strategy:
   - Git SHA to revert to
   - Steps to rollback on Vercel
7. Write to `crew/output/deploy_<product>_<date>_validation.md`

**Output:** Deployment Validation Report
```
═══════════════════════════════════════════════
  DEPLOY VALIDATION: <product> — <date>
═══════════════════════════════════════════════
COMMITS TO DEPLOY: <count>
  - <sha> <message>
  - <sha> <message>

CHANGE LOG COVERAGE: <N>/<N> commits tracked
UNTRACKED CHANGES: None / <list>

RISK TIER: P0|P1|P2|P3
CONTRACTS AFFECTED: None | <contract>
BACKEND CHANGES: None | <list>

ROLLBACK STRATEGY:
  Revert to: <git SHA>
  Vercel: Redeploy previous production commit
  Time to rollback: <estimate>
═══════════════════════════════════════════════
```

### Handoff: change_manager -> qa_lead

**Task**: Run full test suite and build validation
**Context**: All commits tracked, risk classified, rollback planned
**Artifacts**: `crew/output/deploy_<product>_<date>_validation.md`

---

## Phase 2: Test Validation — QA Lead

**Agent:** `qa_lead`
**Action:**
1. Run full test suite: `npm run test:run` in target repo
2. Run production build: `npm run build` in target repo
3. Run `npm audit` for security vulnerabilities
4. If E2E tests exist: `npx playwright test`
5. Verify all FMEA items marked FIXED in this release are actually fixed
6. Write to `crew/output/deploy_<product>_<date>_qa.md`

**Output:** Deploy QA Report
```
═══════════════════════════════════════════════
  DEPLOY QA: <product> — <date>
═══════════════════════════════════════════════
UNIT TESTS: <count> passing / <count> failing
BUILD: PASS / FAIL
SECURITY AUDIT: <vulnerabilities count>
E2E TESTS: <count> passing / N/A

FMEA ITEMS IN THIS RELEASE:
  - <FMEA-ID>: VERIFIED FIXED / NOT VERIFIED

VERDICT: READY / NOT READY (<reason>)
═══════════════════════════════════════════════
```

---

## Phase 3: Deploy Gate — CEO

```
GATE: deploy_approval
AGENT: change_manager (validated), qa_lead (tested)
DECISION NEEDED: Deploy <product> to production?
COMMITS: <count> changes
RISK TIER: <tier>
TESTS: <count> passing, 0 failing
BUILD: PASS
ROLLBACK: <strategy>
RECOMMENDATION: deploy / hold
ARTIFACTS:
  - crew/output/deploy_<product>_<date>_validation.md
  - crew/output/deploy_<product>_<date>_qa.md
```

---

## Phase 4: Deploy — Execution

**Action (executed by FE Lead or COO with CEO present):**

```bash
# From C:\Users\wole\Documents\FML ONLY
cd famililook-<product>
git checkout production
git merge main
git push origin production
git checkout main
```

For desktop6 (FamiliMatch): Also push main (both branches trigger deploy per memory).

---

## Phase 5: Post-Deploy Verification — QA Lead

**Agent:** `qa_lead`
**Action:**
1. Wait 2-3 minutes for Vercel build to complete
2. Verify production URL loads correctly
3. Smoke test critical paths:
   - Landing page renders
   - Core flow completes (upload/analysis/results or compare/results)
   - No console errors
4. Write to `crew/output/deploy_<product>_<date>_smoke.md`

**Output:** Smoke Test Report
```
SMOKE TEST: <product> — <date>
  Landing page: PASS/FAIL
  Core flow: PASS/FAIL
  Console errors: None / <list>
  VERDICT: LIVE / ROLLBACK NEEDED
```

If ROLLBACK NEEDED:
```bash
git checkout production
git revert HEAD
git push origin production
git checkout main
```

---

## Phase 6: Close — Change Manager

**Agent:** `change_manager`
**Action:**
1. Log deployment in change_log.md
2. Update memory files if deployment changes operational status
3. Mark all deployed FMEA items as DEPLOYED
4. Write deployment summary

---

*Workflow: deployment.md v1.0 — 2026-03-31*
