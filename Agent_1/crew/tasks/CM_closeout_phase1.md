# Change Manager Close-Out Brief — Phase 1 Critical Fixes
**Agent:** Change Manager
**Date:** 2026-04-07
**Activates:** After QA Lead issues sign-off

---

## Mission

Close out all 5 Phase 1 critical fixes in the change register. Verify documentation is complete. Assemble the release package for CEO approval. Track the architectural notes raised by QA Lead.

---

## Step 1: Documentation Audit

For each fix, verify the change_log entry exists and is complete:

```bash
grep -A5 "KS-01\|KS-02\|UP-01\|NV-03\|ST-01" .claude/change_log.md
```

Required format for each:
```
### <CR-NNNN> — <Fix Name>
**Description:** <what changed>
**Context:** <why — audit finding reference>
**Action:** <what was done — files, approach>
**Risk Tier:** P1 | P2
**Test evidence:** npm run test:run — <N>/<total> passing
**Build:** PASS
**Approved by:** CEO
**Date:** 2026-04-07
```

If any entry is missing or incomplete → do NOT proceed to release package. Return to the responsible FE agent to complete documentation first.

---

## Step 2: Architecture Health Update

Update the architecture health record:

**New AppErrorBus migration candidates identified:**
- `FacePicker.jsx:83` — catch block now uses toast, pending AppErrorBus migration
- Add to tracking: `crew/output/ARCH_MIGRATION_CANDIDATES.md` (create if doesn't exist)

**New resultsContract.js migration candidates identified:**
- `useKinshipAnalysis.jsx` — flagged by Platform Architect during ST-01 review
- Add to tracking in same file

**Patch count update:**
Run patch frequency check and update architecture health:
```bash
grep -E "src/.*\.(jsx|js)" .claude/change_log.md | grep -oE "src/[^ ]+" | sort | uniq -c | sort -rn | head -20
```

Report any files now at 2+ patches (approaching the 3-patch limit).

---

## Step 3: Release Package Assembly

Assemble the Change Request Package for CEO:

```
═══════════════════════════════════════════════
  CHANGE REQUEST — CR-PHASE1-CRITICAL
  Change Manager — 2026-04-07
═══════════════════════════════════════════════

RISK TIER: P1 (production crash + trust failures)
CHANGE TYPE: Code — Bug Fixes (5 items)
SOURCE: Platform audit 2026-04-07, parallel FE agent sprint

CHANGES:
  CR-KS01: Character Mug Crash — assets/characters/index.js + CharacterPicker.jsx
  CR-KS02: Order Success Race — OrderSuccessPage.jsx
  CR-UP01: FacePicker Silent Catch — FacePicker.jsx
  CR-NV03: Chunk Reload Loop — ErrorBoundary.jsx
  CR-ST01: Abort Race Condition — useKinshipAnalysis.jsx (Platform Architect reviewed)

FILES CHANGED (total: 6):
  src/assets/characters/index.js
  src/components/keepsakes/mobile/CharacterPicker.jsx
  src/pages/OrderSuccessPage.jsx
  src/components/FacePicker.jsx
  src/components/ui/ErrorBoundary.jsx
  src/hooks/useKinshipAnalysis.jsx

VALIDATION:
  ✅ Traceability: Platform audit 2026-04-07 findings KS-01, KS-02, UP-01, NV-03, ST-01
  ✅/❌ Tests: <N> / <total> — Evidence: npm run test:run output
  ✅ Contract impact: None — no changes to kinship_analyze.v1 or compare_faces.v1
  ✅/❌ ops_report: <path>
  ✅ Blast radius: 6 files, desktop2 only, no cross-repo impact
  ✅ Rollback plan: git revert <commit range> — all changes are additive guards
  ✅ Patch count: all files first-time edits in this sprint (or within limit)
  ✅ No structural module bypass: AppErrorBus/AppStorage not yet built — violations flagged for migration
  ✅/❌ Documentation: change_log complete for all 5 fixes

QA SIGN-OFF: <QA Lead verdict>
DEVICE VERIFICATION: PENDING CEO (3 items)

RECOMMENDATION: APPROVE FOR MERGE TO MAIN
  Deploy to production after CEO device verification of:
  1. Character mug gran_loving_african on physical device
  2. FacePicker toast on physical device
  3. Private browser reload behaviour

ARCHITECTURAL NOTES (no action needed now):
  - AppErrorBus: 1 new migration candidate added (FacePicker.jsx)
  - resultsContract.js: useKinshipAnalysis.jsx flagged for future migration
  - Platform Architect should prioritise AppErrorBus build next sprint
═══════════════════════════════════════════════
```

---

## Step 4: Unified Change Register Entry

Add to the unified change register (`crew/output/CHANGE_REGISTER.md`):

```
| 2026-04-07 | desktop2 | Code | KS-01 Character Mug Crash | Audit KS-01 | P1 | CEO | <ops_report> | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | KS-02 Order Success Race | Audit KS-02 | P1 | CEO | <ops_report> | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | UP-01 FacePicker Catch | Audit UP-01 | P2 | CEO | <ops_report> | DONE |
| 2026-04-07 | desktop2 | Code | NV-03 Chunk Reload Loop | Audit NV-03 | P2 | CEO | <ops_report> | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | ST-01 Abort Race Guard | Audit ST-01 | P1 | CEO+ArchReview | <ops_report> | DONE |
```

---

## Step 5: Architecture Migration Candidates File

Create or update `crew/output/ARCH_MIGRATION_CANDIDATES.md`:

```markdown
# Architecture Migration Candidates
**Maintained by:** Change Manager + Platform Architect
**Last updated:** 2026-04-07

## AppErrorBus Migration Queue
(Files with catch blocks to migrate once AppErrorBus is built)

| File | Line | Current pattern | Added | Priority |
|------|------|----------------|-------|----------|
| FacePicker.jsx | 83 | toast workaround | 2026-04-07 | HIGH |
| BasketContext.jsx | 25 | catch {} empty | (pre-audit) | CRITICAL |
| orderApi.js | 22-31 | timeout not surfaced | (pre-audit) | HIGH |
| FamililookContext.jsx | 154-157 | sessionStorage catch-all | (pre-audit) | MEDIUM |
| CardGame.jsx | 32-37 | buildDeck fail = blank | (pre-audit) | HIGH |
| [+ 18 others from audit Appendix A] | | | | |

## AppStorage Migration Queue
(Files with raw localStorage to migrate once AppStorage is built)

| File | Pattern | Added | Priority |
|------|---------|-------|----------|
| useKinshipAnalysis.jsx | localStorage.setItem catch ignored (lines 297, 539) | (pre-audit) | HIGH |
| kinshipClient.js | localStorage.getItem catch ignored (line 65) | (pre-audit) | MEDIUM |
| [+ 30+ others from 35 key audit] | | | | |

## resultsContract.js Migration Queue

| File | What to migrate | Added | Priority |
|------|----------------|-------|----------|
| useKinshipAnalysis.jsx | Winner determination (lines 443-457) | 2026-04-07 | HIGH |
| MobileResultsSection.jsx | Winner re-derivation (lines 350-416) | (pre-audit) | HIGH |
| useKinshipAnalysis.jsx | Feature vote extraction (lines 291-295) | (pre-audit) | HIGH |
| MobileResultsSection.jsx | Feature vote extraction (lines 270-322) | (pre-audit) | HIGH |
```

---

## Stop Conditions

You are DONE when:
- [ ] Documentation audit complete — all 5 change_log entries verified
- [ ] Architecture migration candidates file updated
- [ ] Release package assembled and ready for CEO
- [ ] Unified change register updated
- [ ] Architecture health metrics updated (patch counts)
- [ ] No "documentation to follow" items remaining

Do NOT mark any fix as DONE if its change_log entry is missing or incomplete. Return to the responsible agent first.
