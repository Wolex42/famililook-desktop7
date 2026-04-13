# Shared Infrastructure Migration Assessment
**Author:** Shared Infrastructure Lead (Claude Code native persona)
**Date:** 2026-04-13
**Status:** ASSESSMENT COMPLETE — 5 CEO architectural decisions CONFIRMED (2026-04-13). Pre-implementation checklist items 4-8 pending.

---

## SECTION 1 — famililook-shared Package Specification

### 1.1 Package Location

```
C:\Users\wole\Documents\FML\famililook-shared\
```

Sibling to desktop2/3/4/5/6/7 under the FML parent. Does NOT exist yet.

### 1.2 Package.json Structure

```json
{
  "name": "@famililook/shared",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "exports": {
    "./infrastructure/AppErrorBus": "./src/infrastructure/AppErrorBus.js",
    "./infrastructure/AppStorage": "./src/infrastructure/AppStorage.js",
    "./infrastructure/resultsContract": "./src/infrastructure/resultsContract.js"
  },
  "peerDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "vitest": "^2.1.9",
    "jsdom": "^25.0.1"
  }
}
```

**Notes on exports:**
- Phase 1 scaffolding creates the package with empty `src/infrastructure/` directory only
- Exports map uses **explicit file paths** (not wildcards) for maximum bundler compatibility with Vite 5
- No React components in Phase 1 — peerDependencies declared now for forward compatibility
- `private: true` — this is a local file: dependency, not published to npm

### 1.3 Which Infrastructure Modules Move in Phase 1

**None.** Phase 1 is scaffolding only (empty package structure + dependency wiring).

Modules move in this order across subsequent phases:

| Phase | Module | Lines | Dependencies | Risk |
|-------|--------|-------|-------------|------|
| 2 | AppErrorBus | 273 | None (vanilla JS, zero imports) | **LOWEST** |
| 3 | AppStorage | 862 | Imports `AppErrorBus.report()` | Medium — depends on Phase 2 |
| 4 | resultsContract | 365 | None (pure functions, zero imports) | Low — but consumers import from AppStorage |

**Rationale for AppErrorBus first:**
- Zero internal dependencies (no imports from other infrastructure modules)
- Zero external dependencies (no React, no npm packages)
- Vanilla JS event emitter — works identically in any consuming repo
- Smallest consumer surface: 9 files import it in desktop2 (vs 47 for AppStorage)
- If the `file:` dependency wiring breaks, the failure is isolated and easy to diagnose

**Rationale for AppStorage second:**
- AppStorage imports `{ report as reportError }` from `./AppErrorBus` (line 21)
- After Phase 2, this import path changes to a sibling import within the shared package
- 47 files in desktop2 import from AppStorage — highest consumer count, mechanical migration

**Rationale for resultsContract third:**
- resultsContract itself has zero imports (pure functions)
- But its 7 consumer files also import AppStorage — they are already migrated in Phase 3
- Moving resultsContract last means consumers only change import paths once, not twice

### 1.4 Import Path Changes

#### AppErrorBus (Phase 2)

| Consuming repo | Current import | New import |
|---------------|---------------|-----------|
| desktop2 | `from '../infrastructure/AppErrorBus'` | `from '@famililook/shared/infrastructure/AppErrorBus'` |
| desktop2 | `from '../../infrastructure/AppErrorBus'` | `from '@famililook/shared/infrastructure/AppErrorBus'` |
| desktop4 | Does not yet consume AppErrorBus | `from '@famililook/shared/infrastructure/AppErrorBus'` (future) |
| desktop6 | Does not yet consume AppErrorBus | `from '@famililook/shared/infrastructure/AppErrorBus'` (future) |

**desktop2 consumer files (9):**
- `hooks/useKinshipAnalysis.jsx`
- `state/FamililookContext.jsx`
- `layout/MobileResultsSection.jsx`
- `layout/UploadSection.jsx`
- `game/FaceFusion/FaceFusion.jsx`
- `game/CardGame.jsx`
- `utils/imageProcessing.js`
- `components/ui/ErrorToast.jsx` (uses `import * as AppErrorBus`)
- `infrastructure/AppStorage.js` (internal cross-reference — stays as relative import inside shared package)

#### AppStorage (Phase 3)

| Consuming repo | Current import | New import |
|---------------|---------------|-----------|
| desktop2 (47 files) | `from '../infrastructure/AppStorage'` (and deeper) | `from '@famililook/shared/infrastructure/AppStorage'` |
| desktop4 | Does not yet consume AppStorage | Future |
| desktop6 | Does not yet consume AppStorage | Future |

The 47 desktop2 consumer files span: state contexts (5), hooks (3), game modules (7), layout sections (6), pages (7), utils (9), components (10).

#### resultsContract (Phase 4)

| Consuming repo | Current import | New import |
|---------------|---------------|-----------|
| desktop2 (5 direct importers) | `from '../infrastructure/resultsContract'` (and deeper) | `from '@famililook/shared/infrastructure/resultsContract'` |
| desktop4 | Does not yet consume resultsContract | Future |
| desktop6 | Does not yet consume resultsContract | Future |

**desktop2 direct importers (5):**
- `hooks/useKinshipAnalysis.jsx`
- `layout/MobileResultsSection.jsx`
- `layout/AnalysisSection.jsx`
- `components/keepsakes/hooks/useKeepsakeData.js`
- `components/keepsakes/hooks/useFamilyKeepsakeData.js`

### 1.5 How `file:` Dependency Works

Each consuming repo adds to its `package.json` dependencies:

```json
"dependencies": {
  "@famililook/shared": "file:../famililook-shared"
}
```

Then runs `npm install`. npm creates a symlink from `node_modules/@famililook/shared` → `../famililook-shared`.

**How this works across the repo structure:**
```
FML/
├── famililook-shared/          ← the package
│   ├── package.json
│   └── src/infrastructure/
│       ├── AppErrorBus.js
│       ├── AppStorage.js
│       └── resultsContract.js
├── famililook-desktop2/        ← consumer
│   ├── package.json            ← "file:../famililook-shared"
│   └── node_modules/
│       └── @famililook/shared/ ← symlink → ../../famililook-shared
├── famililook-desktop4/        ← consumer
│   ├── package.json            ← "file:../famililook-shared"
│   └── node_modules/
│       └── @famililook/shared/ ← symlink
└── famililook-desktop6/        ← consumer
    ├── package.json            ← "file:../famililook-shared"
    └── node_modules/
        └── @famililook/shared/ ← symlink
```

**Vite resolves symlinks by default** (`resolve.preserveSymlinks` is false). The shared package source is processed by Vite's transform pipeline as if it were local code. No separate build step needed for the shared package.

**Gotcha — `import.meta.env.DEV`:** Both AppErrorBus (line 58) and AppStorage (line 33) use `import.meta.env?.DEV`. This works correctly because Vite injects `import.meta.env` at transform time for all files in the dependency graph, including symlinked packages. The `?.` optional chaining is already present as a safety guard.

### 1.6 Peer Dependency Versions

Pulled from desktop2 `package.json` (canonical reference):

| Package | Version | desktop4 | desktop6 | Aligned? |
|---------|---------|----------|----------|----------|
| react | ^18.3.1 | ^18.3.1 | ^18.3.1 | Yes |
| react-dom | ^18.3.1 | ^18.3.1 | ^18.3.1 | Yes |

The shared package declares `"react": "^18.3.0"` and `"react-dom": "^18.3.0"` as peerDependencies (allowing ^18.3.x from any consumer). Phase 1 infrastructure modules don't use React, but future component migrations will.

**Known divergence (not blocking Phase 1):**
- framer-motion: desktop2 `^12.34.3`, desktop4 `^11.0.0`, desktop6 `^12.34.3`
- This divergence must be resolved before any framer-motion-dependent component migrates to the shared package

---

## SECTION 2 — famililook-game-engine Package Specification

### 2.1 Package Location

```
C:\Users\wole\Documents\FML\famililook-game-engine\
```

Sibling to desktop5/desktop7 under the FML parent. Does NOT exist yet.

### 2.2 pyproject.toml Structure

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "famililook-game-engine"
version = "0.1.0"
description = "Shared room management and WebSocket protocol for FamiliLook game servers"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
test = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23.0",
]
```

### 2.3 Package Structure

```
famililook-game-engine/
├── pyproject.toml
├── src/
│   └── famililook_game_engine/
│       ├── __init__.py
│       ├── rooms.py          ← shared Player, BaseRoom, RoomManager
│       ├── protocol.py       ← shared message types, envelope builder
│       ���── codes.py          ← room code generation (extracted)
│       └── heartbeat.py      ← future: connection keepalive
└── tests/
    ├── test_rooms.py
    └── test_protocol.py
```

### 2.4 What Extracts from desktop5 vs desktop7

#### Assessment: rooms.py Comparison

| Element | desktop5 (162 lines) | desktop7 (300 lines) | Classification |
|---------|---------------------|---------------------|---------------|
| **Player class** | 4 slots (id, name, ws, connected_at) | 6 slots (+connection_id, disconnected_at) | NEAR-IDENTICAL — desktop7 is superset |
| **Room.broadcast()** | Identical pattern | Identical pattern | IDENTICAL |
| **Room.send_to()** | Identical pattern | Identical pattern | IDENTICAL |
| **Room.add_player()** | Returns Optional[str] | Raises ValueError | SIMILAR — different error style |
| **Room.remove_player()** | Basic removal | Full cleanup (photos, consent, ready) | SIMILAR — desktop7 has more state |
| **RoomManager._generate_code()** | 36^6, secrets, 100 retries | Identical | IDENTICAL |
| **RoomManager._cleanup_loop()** | 60s interval, idle check | 60s interval + disconnected player cleanup | NEAR-IDENTICAL |
| **RoomManager.create_room()** | (host_id, max_players) | (room_type, host_player) | SIMILAR — different signatures |
| **Reconnection support** | Not present | disconnect_player(), rejoin_player(), cleanup_disconnected() | UNIQUE to desktop7 |
| **Photo/consent management** | Not present | photos dict, consents dict, ready_players set, clear_data() | UNIQUE to desktop7 |
| **Memory management** | Not present | Secure zeroing, gc.collect() in clear_data() | UNIQUE to desktop7 |

#### Assessment: protocol.py Comparison

| Element | desktop5 (53 lines) | desktop7 (75 lines) | Classification |
|---------|---------------------|---------------------|---------------|
| **Core client messages** | CREATE_ROOM, JOIN_ROOM, LEAVE | Same 3 + REJOIN_ROOM, GRANT_CONSENT, UPLOAD_PHOTO, READY, SEND_CHAT | NEAR-IDENTICAL core |
| **Core server messages** | ROOM_CREATED, PLAYER_JOINED, PLAYER_LEFT, ERROR | Same 4 + 13 match-specific messages | NEAR-IDENTICAL core |
| **server_msg() builder** | `{"type": ..., **kwargs}` (flat) | `{"type": ..., "data": {...}}` (envelope) | SIMILAR — different envelope |
| **error_msg() builder** | Flat structure | Nested data structure | SIMILAR |
| **Data models** | Card (game-specific) | FeatureComparison, CompatibilityResult (match-specific) | UNIQUE per product |
| **RoomType enum** | Not present | DUO, GROUP | UNIQUE to desktop7 |

#### What Goes Into the Shared Engine

**EXTRACT (genuinely shared):**

1. **Base Player class** — desktop7 superset (6 slots). desktop5's 4-slot Player is a strict subset.
2. **Room code generation** — identical algorithm in both. Extract as standalone `generate_room_code()`.
3. **broadcast() + send_to()** — identical WebSocket message dispatch. Extract as mixin or base class methods.
4. **Cleanup loop skeleton** — identical 60-second interval pattern. Extract with hook for product-specific cleanup.
5. **Core message type enums** — 3 shared client types, 4 shared server types. Extract as base enums.
6. **Message envelope builder** — standardise on desktop7's `{"type", "data"}` envelope (cleaner, more extensible).

**DO NOT EXTRACT (product-specific):**

1. **desktop5 `GameState` integration** — `Room.game` attribute, deck management, turn-based logic
2. **desktop7 photo/consent management** — `photos`, `consents`, `ready_players`, `clear_data()`
3. **desktop5 `Card` model** — game-specific data structure
4. **desktop7 `FeatureComparison` + `CompatibilityResult` models** — match-specific
5. **desktop7 `RoomType` enum** — match-specific (DUO/GROUP), though the pattern of having room types is extractable

### 2.5 How pip Local Path Dependency Works

Each consuming repo adds to its `requirements.txt`:

```
famililook-game-engine @ file:../famililook-game-engine
```

Then runs `pip install -r requirements.txt`. pip installs the local package in editable/development mode.

**Repo structure:**
```
FML/
├── famililook-game-engine/     ← the package
│   ├── pyproject.toml
│   └── src/famililook_game_engine/
��       ├── __init__.py
│       ├── rooms.py
│       └── protocol.py
├── famililook-desktop5/        ← consumer
��   ├── requirements.txt        ← "famililook-game-engine @ file:../famililook-game-engine"
│   └── app/
│       ├── rooms.py            ← imports from famililook_game_engine.rooms
��       └── protocol.py         ��� imports from famililook_game_engine.protocol
└── famililook-desktop7/        ← consumer
    ├── requirements.txt
    └─��� app/
        ├── rooms.py            ← imports from famililook_game_engine.rooms
        └── protocol.py
```

**Import changes:**
```python
# desktop5 current:
from .game_state import GameState

# desktop5 after migration:
from famililook_game_engine.rooms import Player, RoomManager
from famililook_game_engine.protocol import server_msg, error_msg
from .game_state import GameState  # stays local — game-specific
```

---

## SECTION 3 — Migration Sequence

### Phase 1: Package Scaffolding (this session, after CEO approval)

**Goal:** Create empty package structures. Wire `file:` dependencies. Verify builds pass with zero functional changes.

**famililook-shared:**

| Step | Action | Verification |
|------|--------|-------------|
| 1a | Create `famililook-shared/package.json` | `cat package.json` — valid JSON |
| 1b | Create `famililook-shared/src/infrastructure/` directory | `ls -la` confirms |
| 1c | Create empty `famililook-shared/src/infrastructure/.gitkeep` | Directory tracked by git |
| 1d | Add `"@famililook/shared": "file:../famililook-shared"` to desktop2 `package.json` dependencies | `npm install` succeeds in desktop2 |
| 1e | Run `npm run test:run` in desktop2 | 1,444 tests pass (quality floor held) |
| 1f | Run `npm run build` in desktop2 | Build succeeds |

**Do NOT wire desktop4 or desktop6 yet.** They have no consumers of the shared package. Wire them when they first need a shared module.

**famililook-game-engine:**

| Step | Action | Verification |
|------|--------|-------------|
| 1g | Create `famililook-game-engine/pyproject.toml` | Valid TOML |
| 1h | Create `famililook-game-engine/src/famililook_game_engine/__init__.py` | Package importable |
| 1i | Add `famililook-game-engine @ file:../famililook-game-engine` to desktop5 `requirements.txt` | `pip install -r requirements.txt` succeeds |
| 1j | Add same to desktop7 `requirements.txt` | `pip install -r requirements.txt` succeeds |
| 1k | Run desktop5 tests | 37 tests pass |
| 1l | Run desktop7 tests | 111 tests pass |

**Files created in Phase 1:**
- `famililook-shared/package.json`
- `famililook-shared/src/infrastructure/.gitkeep`
- `famililook-game-engine/pyproject.toml`
- `famililook-game-engine/src/famililook_game_engine/__init__.py`

**Files modified in Phase 1:**
- `famililook-desktop2/package.json` (add dependency)
- `famililook-desktop2/package-lock.json` (auto-generated)
- `famililook-desktop5/requirements.txt` (add dependency)
- `famililook-desktop7/requirements.txt` (add dependency)

### Phase 2: Extract AppErrorBus (next session)

**Goal:** Move `AppErrorBus.js` from desktop2 into famililook-shared. Update desktop2 imports. Tests remain at 1,444.

| Step | Action | Files changed |
|------|--------|--------------|
| 2a | Copy `desktop2/src/infrastructure/AppErrorBus.js` → `famililook-shared/src/infrastructure/AppErrorBus.js` | 1 new file |
| 2b | Copy `desktop2/tests/infrastructure/AppErrorBus.test.js` → `famililook-shared/tests/infrastructure/AppErrorBus.test.js` | 1 new file |
| 2c | Add vitest config to famililook-shared | 1 new file |
| 2d | Run tests in famililook-shared | 22 tests pass in isolation |
| 2e | Update 8 desktop2 consumer files: change import path from `../infrastructure/AppErrorBus` → `@famililook/shared/infrastructure/AppErrorBus` | 8 files |
| 2f | Update AppStorage.js import: `./AppErrorBus` stays as-is (internal cross-reference moves together in Phase 3) | 0 files — IMPORTANT: AppStorage still lives in desktop2, still imports from `./AppErrorBus`. Create a re-export shim: `desktop2/src/infrastructure/AppErrorBus.js` becomes `export * from '@famililook/shared/infrastructure/AppErrorBus'` | 1 file (replace contents) |
| 2g | Run `npm run test:run` in desktop2 | 1,444 tests pass |
| 2h | Run `npm run build` in desktop2 | Build succeeds |

**Critical detail — Phase 2f:** AppStorage (still in desktop2) imports from `./AppErrorBus`. We have two options:
- **Option A (shim):** Replace desktop2's `AppErrorBus.js` with a re-export: `export * from '@famililook/shared/infrastructure/AppErrorBus'`. AppStorage's `./AppErrorBus` import keeps working. Clean, no consumer changes needed for AppStorage.
- **Option B (update AppStorage import):** Change AppStorage's import to `@famililook/shared/infrastructure/AppErrorBus`. This touches a blocked file (AppStorage.js) and is a pre-requisite change before AppStorage itself moves.

**Recommendation:** Option A (shim). Keeps AppStorage untouched. The shim is deleted when AppStorage moves in Phase 3.

### Phase 3: Extract AppStorage (depends on Phase 2)

**Goal:** Move `AppStorage.js` from desktop2 into famililook-shared. Update 47 desktop2 imports.

| Step | Action | Files changed |
|------|--------|--------------|
| 3a | Copy `desktop2/src/infrastructure/AppStorage.js` → `famililook-shared/src/infrastructure/AppStorage.js` | 1 new file |
| 3b | Update AppStorage's internal import: `./AppErrorBus` → `./AppErrorBus` (same — both now in shared package) | 0 changes — import is already correct |
| 3c | Copy AppStorage tests → famililook-shared | 1 new file |
| 3d | Run tests in famililook-shared | 22 (AppErrorBus) + 31 (AppStorage) = 53 tests |
| 3e | Update 47 desktop2 consumer files: change import paths | 47 files (mechanical find-replace) |
| 3f | Replace desktop2's `AppStorage.js` with re-export shim | 1 file |
| 3g | Delete desktop2's `AppErrorBus.js` shim (no longer needed — AppStorage moved) | 1 file deleted |
| 3h | Run `npm run test:run` in desktop2 | 1,444 tests pass |
| 3i | Run `npm run build` in desktop2 | Build succeeds |
| 3j | Verify ESLint `no-direct-localstorage` rule still works (paths may need updating) | 1 file checked |

### Phase 4: Extract resultsContract (depends on Phase 3)

**Goal:** Move `resultsContract.js` from desktop2 into famililook-shared. Update 5 desktop2 imports.

| Step | Action | Files changed |
|------|--------|--------------|
| 4a | Copy `desktop2/src/infrastructure/resultsContract.js` → `famililook-shared/src/infrastructure/resultsContract.js` | 1 new file |
| 4b | Copy resultsContract tests → famililook-shared | 1 new file |
| 4c | Run tests in famililook-shared | 53 + 37 = 90 tests |
| 4d | Update 5 desktop2 consumer files: change import paths | 5 files |
| 4e | Replace desktop2's `resultsContract.js` with re-export shim | 1 file |
| 4f | Run `npm run test:run` in desktop2 | 1,444 tests pass |
| 4g | Run `npm run build` in desktop2 | Build succeeds |

After Phase 4, desktop2's `src/infrastructure/` directory contains only re-export shims. These can be deleted once all consuming imports point directly to `@famililook/shared/...`.

### Phase 5: Extract Game Engine (independent of Phases 2-4)

**Goal:** Extract shared room management from desktop5/desktop7 into famililook-game-engine. Requires CEO backend permission.

| Step | Action | Files changed |
|------|--------|--------------|
| 5a | Build `rooms.py` in shared engine: base Player (6 slots), generate_code(), broadcast(), send_to(), base RoomManager skeleton | 1 new file |
| 5b | Build `protocol.py` in shared engine: 3 core client types, 4 core server types, standardised envelope builder | 1 new file |
| 5c | Build `codes.py`: extract `_generate_code()` as standalone function | 1 new file |
| 5d | Write tests for shared engine | ~30 tests |
| 5e | Update desktop5 `rooms.py`: import base classes, extend with game-specific logic (GameState, deck) | 1 file |
| 5f | Update desktop5 `protocol.py`: import base enums, extend with game-specific messages | 1 file |
| 5g | Run desktop5 tests | 37 tests pass |
| 5h | Update desktop7 `rooms.py`: import base classes, extend with match-specific logic (photos, consent, reconnection) | 1 file |
| 5i | Update desktop7 `protocol.py`: import base enums, extend with match-specific messages | 1 file |
| 5j | Run desktop7 tests | 111 tests pass |

**Phase 5 can run in parallel with Phases 2-4** — it touches different repos (backend vs frontend).

---

## SECTION 4 — Risk Assessment

### 4.1 What Breaks if the Package Import Fails

| Scenario | Impact | Blast radius |
|----------|--------|-------------|
| `file:../famililook-shared` path wrong | `npm install` fails — no code change, no breakage | Build-time only |
| Vite can't resolve `@famililook/shared` | Build fails — no deployment | Build-time only |
| AppErrorBus export mismatch | Import error at runtime — ErrorToast stops showing, catch blocks silent again | desktop2 only (desktop4/6 not wired yet) |
| AppStorage export mismatch | Import error at runtime — ALL localStorage access fails, app likely non-functional | desktop2 only |
| resultsContract export mismatch | Import error at runtime — results page shows no winner/percentages | desktop2 only |
| Game engine import fails | `pip install` fails — server won't start | desktop5 or desktop7 (independent) |

**Key observation:** Because we wire desktop2 first (and only desktop2), the blast radius of any Phase 2-4 failure is limited to desktop2. desktop4 and desktop6 are unaffected until they explicitly opt in.

### 4.2 Rollback Plan per Phase

| Phase | Rollback action | Time to rollback |
|-------|----------------|-----------------|
| Phase 1 (scaffolding) | Remove `@famililook/shared` from desktop2 package.json, `npm install`. Delete empty package directories. | < 5 minutes |
| Phase 2 (AppErrorBus) | Restore desktop2's `AppErrorBus.js` from git (`git checkout -- src/infrastructure/AppErrorBus.js`). Revert 8 import changes. `npm run test:run`. | < 15 minutes |
| Phase 3 (AppStorage) | Same — `git checkout` restores AppStorage.js + revert 47 import changes. Or: `git revert` the entire Phase 3 commit. | < 15 minutes (single git revert) |
| Phase 4 (resultsContract) | Same — `git revert` the Phase 4 commit. | < 5 minutes |
| Phase 5 (game engine) | Restore desktop5/desktop7 `rooms.py` and `protocol.py` from git. Remove game engine from requirements.txt. | < 10 minutes |

**Each phase is a single atomic commit.** `git revert <hash>` undoes everything cleanly. This is by design — the strangler fig pattern ensures each phase is independently reversible.

### 4.3 Test Verification at Each Phase

| Phase | Test command | Quality floor | Must pass |
|-------|-------------|--------------|-----------|
| 1 | `cd famililook-desktop2 && npm run test:run && npm run build` | 1,444 | Yes |
| 2 | `cd famililook-shared && npx vitest run` + `cd famililook-desktop2 && npm run test:run && npm run build` | 1,444 (desktop2) + 22 (shared) | Yes |
| 3 | Same + verify 53 tests in shared package | 1,444 + 53 | Yes |
| 4 | Same + verify 90 tests in shared package | 1,444 + 90 | Yes |
| 5 | `cd famililook-desktop5 && pytest tests/ -v` + `cd famililook-desktop7 && pytest tests/ -v` | 37 (d5) + 111 (d7) | Yes |

**Quality floor is NON-NEGOTIABLE:** desktop2 must never drop below 1,444 tests at any phase. If a phase causes test failures, it is rolled back before the next phase begins.

### 4.4 Specific Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Vite symlink resolution fails** | Low | High (build breaks) | Test in Phase 1 with empty package before any code moves. Vite 5 resolves symlinks by default. |
| **`import.meta.env.DEV` undefined in shared package** | Low | Medium (dev console logs stop) | Already guarded with `?.` optional chaining in both modules. Test confirms. |
| **Circular dependency: AppStorage ↔ AppErrorBus** | None | N/A | AppStorage imports AppErrorBus. AppErrorBus does NOT import AppStorage. One-directional. Verified by reading both files. |
| **ESLint paths break after move** | Medium | Low (lint warnings, not runtime) | Update glob patterns in ESLint config same phase as the move. |
| **IndexedDB/BroadcastChannel in test environment** | Medium | Medium (AppStorage tests fail) | jsdom supports neither. AppStorage tests must mock these. Existing tests already handle this. |
| **desktop5/desktop7 message envelope divergence** | High | Medium (protocol mismatch) | Standardise on desktop7's `{"type", "data"}` envelope in shared engine. desktop5 must be updated to match. This is a **CEO decision** (Section 5). |
| **47-file import change introduces typo** | Low | High (single broken import = app crash) | Mechanical find-replace with exact string match. Each file verified by test suite. |

---

## SECTION 5 — CEO Gate Items

### 5.1 Architectural Decisions Required Before Implementation

#### Decision 1: Package disk location

**Question:** Where do the packages live on disk?

**Recommendation:** Sibling to the desktop repos, inside FML parent:
```
FML/
├── famililook-shared/
├── famililook-game-engine/
├── famililook-desktop2/
├── famililook-desktop4/
├── famililook-desktop6/
...
```

**Why:** `file:../famililook-shared` is the simplest relative path. It matches how desktop repos already reference each other. Both npm and pip support `file:` local paths natively. No package registry, no publish step, no version coordination. Changes to the shared package are immediately visible to consumers.

**Alternative considered:** Nested inside a `packages/` subdirectory (monorepo style). Rejected — adds path complexity (`file:../packages/famililook-shared`) and doesn't match the existing flat repo structure.

**CEO DECISION: CONFIRMED (2026-04-13).** Sibling flat structure approved.

#### Decision 2: Message envelope standardisation

**Question:** desktop5 uses flat messages `{"type": "...", ...kwargs}`. desktop7 uses enveloped messages `{"type": "...", "data": {...}}`. The shared game engine must pick one.

**Recommendation:** Standardise on desktop7's envelope pattern `{"type", "data"}`.

**Why:**
- Cleaner separation of routing (type) from payload (data)
- Easier to validate — `data` can be typed per message type
- desktop7 has 111 tests vs desktop5's 37 — more mature protocol
- desktop5 must be updated to match (desktop5 client code in desktop4 also changes)

**Impact:** desktop5 `protocol.py` and desktop4 WebSocket client code must be updated. This is a breaking change to the desktop5 protocol, but desktop5 is not yet in production with real multiplayer users.

**CEO DECISION: CONFIRMED (2026-04-13).** Standardise on desktop7's nested `{"type", "data"}` envelope.

#### Decision 3: FamiliUno P2P scope

**Question:** Should `famililook-game-engine` absorb FamiliUno P2P multiplayer, or is that a separate decision?

**Recommendation:** Separate decision. Do not include FamiliUno P2P in the game engine extraction scope.

**Why:**
- FamiliUno multiplayer does not exist yet (status: "Coming Soon" on trail)
- The game engine extraction (Phase 5) should cover what EXISTS today (desktop5 + desktop7 room management)
- FamiliUno P2P will be designed by Game Engine Architect when that feature is prioritised
- Adding speculative requirements to Phase 5 increases risk and delays the extraction

**CEO DECISION: CONFIRMED (2026-04-13).** FamiliUno P2P out of scope for Phase 5. Separate decision when that feature is prioritised.

#### Decision 4: Phase 5 backend permission

**Question:** Phase 5 modifies `.py` files in desktop5 and desktop7. Per CLAUDE.md, this requires explicit CEO backend permission per session.

**CEO DECISION: CONFIRMED (2026-04-13).** Backend permission granted per-session when Phase 5 begins. Not granted now.

#### Decision 5: Phase execution pace

**Question:** How many phases per session?

**Recommendation:** Maximum 2 phases per session. Phase 1 (scaffolding) is low-risk and can pair with Phase 2 (AppErrorBus extraction) in one session. Phases 3-5 should each be their own session.

**CEO DECISION: CONFIRMED (2026-04-13).** Max 2 phases per session. Phase 1 + Phase 2 can pair. Phases 3-5 each their own session.

### 5.2 Pre-Implementation Checklist (must all be GREEN before Phase 1 begins)

| # | Item | Status | Action |
|---|------|--------|--------|
| 1 | CEO approves sibling disk location | **CONFIRMED** | Sibling flat structure (2026-04-13) |
| 2 | CEO approves envelope standardisation | **CONFIRMED** | desktop7 nested envelope (2026-04-13) |
| 3 | CEO confirms FamiliUno P2P out of scope | **CONFIRMED** | Separate decision (2026-04-13) |
| 4 | Governance baseline commit pushed (SESSION_F_START Task 1) | PENDING | From Session F handoff — .claude/ files, SESSION_PROTOCOL.md |
| 5 | CLAUDE.md stale rows fixed (structural modules table) | PENDING | From Session F handoff — "NOT BUILT" → "BUILT" |
| 6 | change_log.md exists in desktop5, desktop6, desktop7 | PENDING | Change Manager task — required before any work in those repos |
| 7 | famililook-shared added to `.claude/validate_scope.py` | PENDING | Governance layer must know about new package |
| 8 | famililook-game-engine added to `.claude/validate_scope.py` | PENDING | Same |

---

## Summary

This migration is **mechanical, not architectural**. The hard work — building the three structural modules, migrating all consumers, adding ESLint enforcement — is already done (Sessions A-F). What remains is moving files from `desktop2/src/infrastructure/` into a shared package and updating import paths.

**Total phases:** 5
**Total files created:** ~12 (package configs, copied modules, tests)
**Total files modified:** ~65 (import path changes across desktop2, desktop5, desktop7)
**Lines of new code written:** 0 (all code already exists — this is a move, not a rewrite)
**Risk:** Low per phase (each independently reversible)
**Quality floor:** 1,444 desktop2 tests must pass at every phase boundary

---

_All 5 architectural decisions CONFIRMED by CEO (2026-04-13). Pre-implementation checklist items 4-8 must be GREEN before Phase 1 scaffolding begins._
