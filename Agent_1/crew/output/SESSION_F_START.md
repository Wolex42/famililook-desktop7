# Session F — Start Here

**Date:** Next session after 2026-04-10
**First action:** Read CLAUDE.md + orchestrator.md + SESSION_HANDOFF_2026_04_10.md

## Immediate first task (before any development):
Add governance layer to git tracking.
```bash
cd C:\Users\wole\Documents\FML
git add .claude/guardrails.json .claude/validate_scope.py .claude/working_set.txt .claude/pre-commit-hook.sh .claude/patch_validator.py .claude/scan-secrets.sh .claude/session-start.sh .claude/settings.json
git add docs/
git commit -m "chore: add governance layer and docs to git tracking (baseline — post-repair state)"
git push origin main
```
Do NOT add .claude/settings.local.json — this is local-only.

## Second task (main development work):
resultsContract Phase 3 — migrate 6 consumers.
Spec: MODULE_SPEC_resultsContract.md Section 4.
Files: MobileResultsSection.jsx, AnalysisSection.jsx, useKeepsakeData.js,
       useFamilyKeepsakeData.js, childSummaryGenerator.js, narrativeGenerator.js.
Quality floor: 1,444 tests.

## DO NOT start Task 3 (AppErrorBus Phase 4 ESLint) this session.
## resultsContract Phase 3 is the priority — it unblocks the relaunch.
