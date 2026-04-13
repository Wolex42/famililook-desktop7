# Change Request Package — Phase 1 Critical Fixes

```
===============================================
  CHANGE REQUEST — CR-PHASE1-CRITICAL
  Change Manager — 2026-04-07
===============================================

RISK TIER: P1 (production crash + trust failures)
CHANGE TYPE: Code — Bug Fixes (5 items)
SOURCE: Platform audit 2026-04-07, parallel FE agent sprint

-----------------------------------------------
CHANGES
-----------------------------------------------

  CR-KS01: Character Mug Missing Emotions
    7 character/emotion PNG imports + map entries added.
    African gran now has full 5-emotion parity.
    File: src/assets/characters/index.js
    Read-only verification: src/components/keepsakes/mobile/CharacterPicker.jsx
      (null guards already present — no edit needed)

  CR-KS02: Order Success Race Condition
    Single getOrderStatus call replaced with 5-attempt
    exponential backoff polling (1.5s base, ~46.5s max).
    Loading state shows "Payment received."
    Final failure says "Your payment was successful."
    File: src/pages/OrderSuccessPage.jsx

  CR-UP01: FacePicker Silent Crop Failure
    Silent catch replaced with inline error message.
    Modal stays open on crop failure so user can retry.
    Inline error used (not toast — z-index conflict).
    File: src/components/FacePicker.jsx

  CR-NV03: Chunk Reload Loop Guard
    Safe sessionStorage wrappers added to prevent
    SecurityError in private/incognito browsers.
    In-memory retry counter (max 1) prevents infinite loop.
    Raw error display gated behind DEV mode.
    Files: src/components/ui/ErrorBoundary.jsx
           src/utils/lazyWithReload.js

  CR-ST01: Analysis Abort Race Condition
    signal.aborted guards added after both async boundaries.
    Prevents cancelled analysis from overwriting fresh results.
    Zero logic changes — purely defensive guards.
    Platform Architect reviewed: YES.
    File: src/hooks/useKinshipAnalysis.jsx

-----------------------------------------------
FILES CHANGED (7 total, desktop2 only)
-----------------------------------------------

  1. src/assets/characters/index.js         (KS-01)
  2. src/components/keepsakes/mobile/CharacterPicker.jsx  (KS-01 read-only verify)
  3. src/pages/OrderSuccessPage.jsx          (KS-02)
  4. src/components/FacePicker.jsx           (UP-01)
  5. src/components/ui/ErrorBoundary.jsx     (NV-03)
  6. src/utils/lazyWithReload.js             (NV-03)
  7. src/hooks/useKinshipAnalysis.jsx        (ST-01)

-----------------------------------------------
VALIDATION
-----------------------------------------------

  PASSED  Traceability
          All 5 fixes map to platform audit findings:
          KS-01, KS-02, UP-01, NV-03, ST-01

  PASSED  Tests: 1,346 / 1,346 passing
          Evidence: npm run test:run — full suite green

  PASSED  Build: npm run build — PASS

  PASSED  Contract impact: NONE
          No changes to kinship_analyze.v1 or compare_faces.v1
          No changes to winner determination, feature votes,
          or percentage calculation

  PASSED  Blast radius: 7 files, desktop2 only
          No cross-repo impact (desktop3/4/5/6/7 untouched)

  PASSED  Rollback plan: git revert <commit range>
          All changes are additive guards — revert is safe
          and restores prior behaviour exactly

  PASSED  Patch count acceptable
          index.js: 4 (OVER LIMIT — but CEO-directed asset fix)
          All other files: first edit this sprint

  PASSED  No structural module bypass
          AppErrorBus: NOT YET BUILT — 3 new migration
            candidates flagged (FacePicker, ErrorBoundary,
            lazyWithReload)
          AppStorage: NOT YET BUILT — 2 new candidates
            flagged (ErrorBoundary, lazyWithReload)
          resultsContract.js: NOT YET BUILT — 1 candidate
            flagged (useKinshipAnalysis.jsx)

  PASSED  Documentation complete
          All 5 change_log entries verified with
          Description/Context/Action format
          Architecture migration candidates file created

-----------------------------------------------
QA SIGN-OFF
-----------------------------------------------

  QA Lead verdict: PASS (all 5 fixes validated)

  KS-01: PASS — All 7 emotions render, null guard works
  KS-02: PASS — Polling retries, loading state shows,
         failure message correct
  UP-01: PASS — Inline error displays, modal stays open,
         retry clears error
  NV-03: PASS — No SecurityError in simulated private mode,
         reload loop capped at 1, raw errors hidden in prod
  ST-01: PASS — Abort guards fire correctly, no state
         overwrite after cancellation

-----------------------------------------------
DEVICE VERIFICATION — PENDING CEO
-----------------------------------------------

  3 items require physical device confirmation:

  1. Character mug: gran_loving_african renders correctly
     on iOS Safari and Chrome Android
  2. FacePicker: inline error message visible and legible
     on physical device (not just desktop emulation)
  3. Private browser: reload behaviour in actual
     Safari Private / Chrome Incognito (not simulated)

-----------------------------------------------
CHANGE REGISTER ENTRIES
-----------------------------------------------

| Date | Repo | Type | Change | Source | Tier | Approval | Status |
|------|------|------|--------|--------|------|----------|--------|
| 2026-04-07 | desktop2 | Code | KS-01 Character Mug Crash | Audit KS-01 | P1 | CEO | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | KS-02 Order Success Race | Audit KS-02 | P1 | CEO | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | UP-01 FacePicker Catch | Audit UP-01 | P2 | CEO | DONE |
| 2026-04-07 | desktop2 | Code | NV-03 Chunk Reload Loop | Audit NV-03 | P2 | CEO | PENDING DEVICE |
| 2026-04-07 | desktop2 | Code | ST-01 Abort Race Guard | Audit ST-01 | P1 | CEO+Arch | DONE |

-----------------------------------------------
ARCHITECTURE HEALTH NOTES
-----------------------------------------------

  Files OVER 3-patch limit (require CEO sign-off for
  further edits):
    - GroupSnapshotSection.jsx: 11 patches (REDESIGN CANDIDATE)
    - AppLayout.jsx: 5-8 patches
    - 6 files at 4 patches
    - 6 files at 3 patches (AT limit)

  New migration candidates from this sprint:
    - AppErrorBus: +3 files (FacePicker, ErrorBoundary,
      lazyWithReload)
    - AppStorage: +2 files (ErrorBoundary, lazyWithReload)
    - resultsContract.js: +1 file (useKinshipAnalysis)

  Full migration queue: crew/output/ARCH_MIGRATION_CANDIDATES.md

-----------------------------------------------
RECOMMENDATION
-----------------------------------------------

  >>> APPROVE FOR MERGE TO MAIN <<<

  Deploy to production after CEO device verification
  of the 3 items listed above.

  Deployment process:
    git checkout production
    git merge main
    git push origin production
    git checkout main

  Post-deploy monitoring:
    - Watch Vercel build logs for successful deploy
    - Confirm no chunk errors in console
    - Verify gran_loving_african mug renders on prod

===============================================
  END OF CHANGE REQUEST — CR-PHASE1-CRITICAL
===============================================
```
