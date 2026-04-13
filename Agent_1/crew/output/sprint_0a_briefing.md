# Sprint 0A Briefing — FamiliMatch Source Restoration

**Sprint ID:** 0A
**Date:** 2026-03-31
**Product:** FamiliMatch (famililook-desktop6)
**Sprint Type:** Source restoration (reverse-engineering from dist artifacts + surviving source)
**Risk Level:** Medium — production is LIVE from stale dist/, no source = no ability to patch

---

## SITUATION

FamiliMatch is live on Vercel (`famililook-desktop6.vercel.app`) but serving from a `dist/` folder with no corresponding source files for 17 of 26 expected source files. The app cannot be built, patched, or tested until source is restored. A `dist_backup_20260331` snapshot exists as rollback insurance.

### What EXISTS (9 files — the survivors)

| Path | Purpose |
|---|---|
| `src/pages/LandingPage.jsx` | Mode selection, email capture, upgrade prompts |
| `src/pages/SoloPage.jsx` | Solo comparison flow (upload, analyze, results) |
| `src/pages/RoomPage.jsx` | Duo/Group WebSocket room flow |
| `src/api/matchClient.js` | API client for `/compare/faces` + `/face/morph` |
| `src/utils/analytics.js` | Event tracking, consent-gated |
| `src/hooks/useMatchConnection.js` | WebSocket connection manager |
| `src/hooks/useMatchHistory.js` | localStorage history (max 20 entries) |
| `src/components/ChatPanel.jsx` | Real-time chat for rooms |
| `src/components/ShareCard.jsx` | Shareable result card with html2canvas |

### What is MISSING (17 files — must be restored)

| # | File | Sprint Item | Priority |
|---|---|---|---|
| 1 | `index.html` | FM-001 | P0 — build entry |
| 2 | `vite.config.js` | FM-001 | P0 — build entry |
| 3 | `src/main.jsx` | FM-001 | P0 — build entry |
| 4 | `src/App.jsx` | FM-001 | P0 — build entry |
| 5 | `src/state/ConsentContext.jsx` | FM-003 | P0 — all pages depend |
| 6 | `src/state/MatchContext.jsx` | FM-003 | P0 — all pages depend |
| 7 | `src/components/ConsentModal.jsx` | FM-004 | P0 — consent gate |
| 8 | `src/components/PhotoUpload.jsx` | FM-004 | P0 — solo + room upload |
| 9 | `src/components/OnboardingScreen.jsx` | FM-004 | P1 — solo onboarding |
| 10 | `src/components/FeatureScanAnimation.jsx` | FM-004 | P1 — analysis UX |
| 11 | `src/components/ResultsStory.jsx` | FM-004 | P0 — results display |
| 12 | `src/components/RoomLobby.jsx` | FM-004 | P1 — room lobby UI |
| 13 | `src/components/CountdownOverlay.jsx` | FM-004 | P1 — room countdown |
| 14 | `src/utils/config.js` | FM-005 | P0 — API_BASE, API_KEY, MATCH_SERVER_URL |
| 15 | `src/utils/constants.js` | FM-005 | P0 — COMPARE_FEATURES array |
| 16 | `src/pages/ResultsPage.jsx` | FM-001* | P1 — group results page |
| 17 | `src/pages/PrivacyPage.jsx` | FM-001* | P2 — static page |
| 18 | `src/pages/TermsPage.jsx` | FM-001* | P2 — static page |

*Items 16-18 discovered during investigation — they exist in dist as lazy-loaded chunks but are not in any surviving source. They are required for routing in App.jsx.

---

## REVERSE-ENGINEERING SOURCES

The following dist artifacts have been decoded and provide the authoritative specification for restoration:

### 1. `dist/assets/config-DgUokLBc.js` — DECODED

Exports confirmed:
```
API_BASE = "https://api.famililook.com"     (via VITE_API_BASE env var)
API_KEY_REF = (empty, set via VITE env var)
MATCH_SERVER_URL = "wss://api.famililook.com/ws/match"  (via VITE_MATCH_WS env var)
ConsentModal component (bundled here as side-effect)
Zap icon re-export
```

### 2. `dist/assets/index-BwvGOR5n.js` — DECODED

Contains the full React + ReactDOM + react-router-dom bundle plus:

**ConsentContext** (minified as `Sm`, `df`, `Mm`):
- localStorage key: `fl:bipa-consent`
- State shape: `{ bipaConsented: boolean, timestamp: number|null }`
- Methods: `grantConsent()`, `revokeConsent()`
- Hook: `useConsent()` — throws if outside provider

**MatchContext** (minified as `km`, `pf`, `Im`, `Em`):
- Initial state: `{ mode: null, roomCode: null, isHost: false, playerId: null, playerName: "", userName: sessionStorage.getItem("fm:username") || "", players: [], myPhoto: null, status: "idle", results: null, error: null }`
- Reducer actions: `SET_MODE, SET_PLAYER_NAME, SET_USERNAME, SET_ROOM, SET_STATUS, SET_PHOTO, UPDATE_PLAYERS, SET_RESULTS, SET_ERROR, RESET`
- `SET_USERNAME` persists to `sessionStorage` key `fm:username`
- Hook: `useMatch()` — throws if outside provider

**App structure** (minified as `Dm` wrapping `Sm` > `km` > `Om`):
```
BrowserRouter > ConsentProvider > MatchProvider > Suspense > Routes
```

**Routes:**
| Path | Component | Lazy chunk |
|---|---|---|
| `/` | LandingPage | LandingPage--VPLkchf.js |
| `/solo` | SoloPage | SoloPage-D0Y8ZcnU.js |
| `/room` | RoomPage | RoomPage-NnWGKN7V.js |
| `/results` | ResultsPage | ResultsPage-BeqOeRxe.js |
| `/privacy` | PrivacyPage | PrivacyPage-B6I-Do_9.js |
| `/terms` | TermsPage | TermsPage-uWERuUh2.js |

**Loading fallback:** Centered spinning circle with `border-primary` styling.

### 3. `dist/assets/PhotoUpload-BQEYefpI.js` — DECODED

- `usePhotoUpload()` custom hook: file validation (JPEG/PNG/WebP, max 10MB), resize to 1024px max, base64 conversion at 0.8 JPEG quality
- `PhotoUpload` component: drag-and-drop + click-to-upload, preview with X button, loading spinner
- 44px min touch targets on remove button

### 4. `dist/assets/ResultsStory-BiiQr7zi.js` — DECODED

- 5-slide story format (score, strongest match, biggest contrast, feature breakdown, fusion reveal)
- Exported constants: `COMPARE_FEATURES` (8 items), `FEATURE_EMOJI`, `FEATURE_LABELS`
- `getChemistryTier()` function with thresholds: 85/70/55/40/0
- `ResultsStory` component with animated percentage counter, gradient backgrounds, continue button
- `FusionReveal` sub-component with reveal button interaction

### 5. `dist/assets/SoloPage-D0Y8ZcnU.js` — DECODED

Contains inlined versions of: `OnboardingScreen` (name entry form), `FeatureScanAnimation` (3-phase progress), `ShareCard`, matchClient functions. These were tree-shaken into the solo chunk but the component APIs match what the surviving source files import.

### 6. `dist/assets/RoomPage-NnWGKN7V.js` — DECODED

Contains `RoomLobby` (create/join room UI, player list, host controls, room code display with copy) and `CountdownOverlay` (full-screen countdown 3-2-1).

### 7. `dist/assets/ResultsPage-BeqOeRxe.js` — DECODED

Group results page with `MatrixReveal` (pair-by-pair reveal animation) and `WinnerCard`. Duo mode uses `ResultsStory` directly.

### 8. `dist/assets/PrivacyPage-B6I-Do_9.js` + `TermsPage-uWERuUh2.js` — DECODED

Static content pages with branded header, back navigation.

---

## SPRINT ITEMS — DETAILED SPECIFICATIONS

### FM-001: Build Entry Points

**Owner:** FE Lead
**Files:** `index.html`, `vite.config.js`, `src/main.jsx`, `src/App.jsx`

`index.html`:
- Restore from `dist/index.html` — replace hashed asset references with `src/main.jsx` script tag
- Keep all meta tags, Open Graph, Twitter Card, structured data, favicon unchanged

`vite.config.js`:
- React plugin (`@vitejs/plugin-react`)
- Tailwind CSS via PostCSS
- Match existing `package.json` dependencies (Vite 5, React 18)

`src/main.jsx`:
- `createRoot(document.getElementById('root')).render(<App />)`
- Strict mode optional (dist does not use it)

`src/App.jsx`:
- `BrowserRouter > ConsentProvider > MatchProvider > Suspense > Routes`
- 6 routes: `/`, `/solo`, `/room`, `/results`, `/privacy`, `/terms`
- All page components lazy-loaded
- Loading fallback: centered spinner

**Acceptance:** `npm run build` succeeds. Dev server renders landing page.

---

### FM-003: Context Providers

**Owner:** FE Lead
**Files:** `src/state/ConsentContext.jsx`, `src/state/MatchContext.jsx`

`ConsentContext.jsx`:
- localStorage key: `fl:bipa-consent`
- State: `{ bipaConsented: boolean, timestamp: number|null }`
- Provider methods: `grantConsent()`, `revokeConsent()`
- Hook: `useConsent()` — error if outside provider
- Load from localStorage on init, persist on change

`MatchContext.jsx`:
- useReducer with initial state (11 fields — see decoded spec above)
- sessionStorage key for userName: `fm:username`
- 10 action types
- `SET_MODE` resets to initial state except mode
- Provider exposes: `setMode, setPlayerName, setUserName, setRoom, setStatus, setPhoto, updatePlayers, setResults, setError, reset`
- Hook: `useMatch()` — error if outside provider

**Acceptance:** Existing pages (LandingPage, SoloPage, RoomPage) import these successfully. `useConsent()` and `useMatch()` return expected shapes.

---

### FM-004: Missing Components (7 files)

**Owner:** FE Lead
**Files:** All in `src/components/`

#### ConsentModal.jsx
- Props: `{ onConsented }`
- BIPA consent text (exact string preserved from dist)
- Fixed overlay, z-50, max-w-md
- Decline button: `window.history.back()`
- Consent button: calls `grantConsent()` from ConsentContext, then `onConsented()`
- Revocation notice at bottom

#### PhotoUpload.jsx
- Props: `{ label, onPhotoReady, disabled }`
- Internal `usePhotoUpload()` hook (can be same-file or separate)
- File validation: JPEG/PNG/WebP only, max 10MB
- Resize: max 1024px, JPEG 0.8 quality
- Drag-and-drop zone (140x140px rounded)
- Preview with remove button (44px touch target)
- Loading spinner during processing

#### OnboardingScreen.jsx
- Props: `{ onComplete }`
- Full-screen overlay, z-40
- Name input form with "What should we call you?"
- Persists via `setUserName()` from MatchContext
- "Let's Go" submit button + "Skip for now" link
- Back button navigates to `famililook.com`
- Violet/pink gradient branding

#### FeatureScanAnimation.jsx
- Props: `{ progress: { step, pct }, nameA, nameB }`
- 3 phases based on progress percentage:
  - Phase 1 (0-59%): Feature-by-feature scan with check/spinner icons
  - Phase 2 (60-84%): Side-by-side comparison view
  - Phase 3 (85-100%): Fusion creation animation
- Uses `COMPARE_FEATURES`, `FEATURE_EMOJI`, `FEATURE_LABELS` from ResultsStory
- Gradient progress bar

#### ResultsStory.jsx
- Props: `{ results, nameA, nameB, onReset }`
- 5-slide carousel: Score, Strongest Match, Biggest Contrast, Feature Breakdown, Fusion Reveal
- Animated percentage counter (1.8s ease-out)
- Chemistry tier comments (2 per tier, 5 tiers)
- Feature emoji + labels for 8 features
- Dot indicators + Continue button
- `FusionReveal` sub-component with reveal interaction
- Exports: `ResultsStory` (default or named `R`), `COMPARE_FEATURES` (named `C`), `FEATURE_EMOJI` (named `F`), `FEATURE_LABELS` (named `a`), `getChemistryTier` (named `g`), `RotateCcw` icon (named `b`)

#### RoomLobby.jsx
- Props: `{ connection, onRoomReady }`
- Create Room / Join Room toggle
- Room code display with copy-to-clipboard
- Player list with crown icon for host
- "Start Game" button (host only, requires 2+ players)
- Name input for joining
- Connection status indicator

#### CountdownOverlay.jsx
- Props: `{ seconds, onComplete }`
- Full-screen overlay with large countdown number (3, 2, 1)
- Scale animation on each tick
- Calls `onComplete()` when countdown reaches 0

**Acceptance:** SoloPage full flow works (onboarding -> upload -> analyze -> results). RoomPage renders lobby.

---

### FM-005: Utility Files

**Owner:** FE Lead
**Files:** `src/utils/config.js`, `src/utils/constants.js`

`config.js`:
```js
export const API_BASE = import.meta.env.VITE_API_BASE || 'https://api.famililook.com';
export const API_KEY_REF = import.meta.env.VITE_API_KEY_REF || '';
export const MATCH_SERVER_URL = import.meta.env.VITE_MATCH_WS || 'wss://api.famililook.com/ws/match';
```

`constants.js`:
```js
export const COMPARE_FEATURES = [
  'eyes', 'eyebrows', 'smile', 'nose',
  'face_shape', 'skin', 'hair', 'ears'
];
```

**Acceptance:** `matchClient.js` import resolves. `analytics.js` import resolves. No build errors.

---

### FM-002: matchClient.js Broken Import (Auto-resolves)

**Owner:** FE Lead
**Files:** `src/api/matchClient.js` (NO CHANGES NEEDED)

The file currently imports:
```js
import { API_BASE, API_KEY } from '../utils/config';
import { COMPARE_FEATURES } from '../utils/constants';
```

Both imports break because neither file exists. Once FM-005 delivers `config.js` and `constants.js`, this resolves automatically. No code changes to `matchClient.js`.

**Acceptance:** `matchClient.js` compiles without errors.

---

### Additional Discovery: 3 Missing Pages

During investigation, 3 additional lazy-loaded pages were found in the dist bundle that are not in any surviving source:

| File | Content |
|---|---|
| `src/pages/ResultsPage.jsx` | Group/Duo results with MatrixReveal + WinnerCard |
| `src/pages/PrivacyPage.jsx` | Static privacy policy page |
| `src/pages/TermsPage.jsx` | Static terms of service page |

These are required by `App.jsx` routing. They must be included in FM-001 scope or the build will fail (lazy imports to nonexistent files).

---

## EXECUTION ORDER (dependency chain)

```
Phase 1 (no dependencies):
  FM-005 → config.js + constants.js

Phase 2 (depends on FM-005):
  FM-003 → ConsentContext.jsx + MatchContext.jsx
  FM-002 → auto-resolved

Phase 3 (depends on FM-003 + FM-005):
  FM-004 → 7 components (ConsentModal, PhotoUpload, OnboardingScreen,
           FeatureScanAnimation, ResultsStory, RoomLobby, CountdownOverlay)

Phase 4 (depends on all above):
  FM-001 → index.html, vite.config.js, main.jsx, App.jsx
           + ResultsPage.jsx, PrivacyPage.jsx, TermsPage.jsx

Phase 5 (verification):
  npm run build → must succeed
  npm run dev → landing page renders
  Solo flow → upload, analyze, results, share
  Room flow → lobby renders (no live backend test needed)
```

---

## ROLLBACK PLAN

If restoration introduces regressions:
1. Delete all new/modified source files
2. Restore `dist/` from `dist_backup_20260331/`
3. Vercel will continue serving the old dist

Production is never at risk — the dist backup is the safety net.

---

## PRE-SPRINT CHECKLIST (updated)

- [x] Dist backup created (`dist_backup_20260331/`)
- [x] Backend permission: NOT NEEDED (frontend only)
- [x] Rollback plan: revert to dist_backup
- [x] All dist chunks decoded and specifications extracted
- [x] Surviving source files audited (9 files, all healthy)
- [x] Sprint briefing written
- [ ] Working set: update `.claude/working_set.txt` before editing
- [ ] Change log: create in desktop6 before first edit
- [ ] FE Lead assigned and acknowledged

---

## TEAM ASSIGNMENTS

| Role | Agent | Responsibility |
|---|---|---|
| **COO** | (this briefing) | Sprint coordination, blockers, reporting |
| **FE Lead** | `Agent_1/crew/agents/fe_lead.md` | All file restoration, build verification |
| **QA Lead** | `Agent_1/crew/agents/qa_lead.md` | Acceptance testing per item |
| **Change Manager** | `Agent_1/crew/agents/change_manager.md` | Change log, working set governance |

---

## DECISIONS NEEDED: NONE

All scope is pre-approved. No backend changes. No CEO decisions required.

---

## ESTIMATED EFFORT

| Item | Files | Complexity | Est. time |
|---|---|---|---|
| FM-005 | 2 | Trivial | 5 min |
| FM-003 | 2 | Low | 15 min |
| FM-004 | 7 | Medium | 45 min |
| FM-001 | 4 + 3 pages | Medium | 30 min |
| FM-002 | 0 (auto) | None | 0 min |
| Verification | — | — | 15 min |
| **Total** | **18 files** | | **~2 hours** |

---

*Sprint briefing prepared by COO. Ready for Phase 2 execution on FE Lead acknowledgement.*
