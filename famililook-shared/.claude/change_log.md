# Change Log — famililook-shared

## 2026-04-14 — Standalone vitest config + consumer wiring (CR-SHARED-04)

### CR-SHARED-04 — vitest.config.js + test scripts + desktop4/desktop6 wired
**Description:** Added vitest.config.js (jsdom environment, tests/**/*.test.js include pattern) and "test"/"test:run" scripts to package.json. Desktop4 and desktop6 now have `@famililook/shared: file:../famililook-shared` in dependencies with verified symlinks.
**Context:** Session A2. All 3 consumers (desktop2, desktop4, desktop6) now wired to the shared package. 88 tests pass standalone.
**Cross-repo impact:** desktop4 (commit f9eed1a) and desktop6 (commit 49e78f6) — package.json + package-lock.json updated. All tests + builds pass in both repos.
**Risk Tier:** P3 (Routine — no source code changes, dependency wiring only)
**Status:** COMPLETE

---

## 2026-04-14 — resultsContract extraction (CR-SHARED-03)

### CR-SHARED-03 — resultsContract extraction to famililook-shared
**Description:** resultsContract.js (365 lines) and resultsContract.test.js (45 tests, 401 lines) copied verbatim from desktop2. Zero internal dependencies — pure functions module, no AppErrorBus or AppStorage imports.
**Context:** famililook-shared Phase 4. Third structural module. All three infrastructure modules now in shared package.
**Cross-repo impact:** desktop2 — re-export shim installed (named + default exports), 1,444 tests passing, build PASS.
**Risk Tier:** P2
**Status:** COMPLETE

---

## 2026-04-14 — AppStorage extraction (CR-SHARED-02)

### CR-SHARED-02 — AppStorage extraction to famililook-shared
**Description:** AppStorage.js (861 lines) and AppStorage.test.js (31 tests, 394 lines) copied verbatim from desktop2. Internal `./AppErrorBus` import resolves to sibling in shared package — zero source changes.
**Context:** famililook-shared Phase 3. Second structural module. Desktop2 consumes via re-export shim.
**Cross-repo impact:** desktop2 — re-export shim installed, test fix for module identity (4 dynamic imports), 1,444 tests passing, build PASS.
**Risk Tier:** P2
**Status:** COMPLETE

---

## 2026-04-14 — AppErrorBus extraction (CR-SHARED-01)

### CR-SHARED-01 — AppErrorBus extraction to famililook-shared
**Description:** AppErrorBus.js (273 lines) and AppErrorBus.test.js (12 tests) copied verbatim from famililook-desktop2/src/infrastructure/. No source changes. Package exports map already covered this path from Phase 1 scaffolding.
**Context:** famililook-shared Phase 2. First structural module extracted. Desktop2 consumes via re-export shim. Desktop4 and desktop6 not yet wired.
**Cross-repo impact:** desktop2 — re-export shim installed, 1,444 tests passing, build PASS. No impact on desktop4/desktop6 (not yet consuming the package).
**Risk Tier:** P2
**Status:** COMPLETE
