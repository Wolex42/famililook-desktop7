# MODULE SPEC — AppStorage

**Platform Architect — 2026-04-09**
**Version:** 1.0
**Status:** SPEC COMPLETE — Awaiting CEO approval

---

## 1. PROBLEM CATEGORY

**Class of bugs eliminated:** Raw localStorage/sessionStorage access with no schema, no quota handling, no versioning, no multi-tab synchronisation, and silent failures when storage is full or unavailable.

**Current instance count:** 185 raw `localStorage` calls and 20 raw `sessionStorage` calls across 30 files. 42 unique storage keys identified. After code verification:

- **37 localStorage keys** actively used (5 are legacy/never-written)
- **5 sessionStorage keys** actively used
- **0 keys** have schema versioning
- **0 keys** have IndexedDB fallback
- **~8 locations** catch QuotaExceededError (most silently swallow it)
- **0 keys** use BroadcastChannel for multi-tab sync

**Existing partial solution:** `src/utils/storage.js` provides `safeJSON()`, `safeSetItem()`, a `STORAGE_KEYS` constant object (27 keys defined), and typed accessors for 8 keys. However:
- Only 3 of 30 files import from `storage.js` — the other 27 use raw `localStorage` directly
- `safeSetItem()` catches quota errors but only logs to console — no AppErrorBus integration
- No versioning, no migration, no BroadcastChannel, no IndexedDB fallback
- `STORAGE_KEYS` is incomplete (missing 15 keys used elsewhere in the codebase)

**Impact of the current pattern:**

1. **Quota failures are silent.** When localStorage fills (5-10MB depending on browser, 10MB hard limit on WKWebView), `setItem` throws `QuotaExceededError`. Most catch blocks swallow this. The user's basket, analysis results, or plan status silently fails to persist. On page refresh, data is gone.

2. **No versioning.** If the shape of `fl:groupSnapshot` changes between deploys, old data is parsed by new code. Result: crashes, wrong data displayed, or silent corruption. There is no way to detect stale schemas or migrate them.

3. **Multi-tab corruption.** Two tabs can write to the same key independently. `fl:basket` written in Tab A is overwritten by Tab B. The user loses basket items. `fl:plan` can diverge between tabs after an upgrade.

4. **No fallback for large values.** `fl:thumbnails` stores base64-encoded face thumbnails as a JSON object. A family of 5 with high-resolution crops can exceed 2MB in this single key. No IndexedDB fallback exists.

5. **Mobile WebView risk.** WKWebView has a 10MB hard limit with no warning. The current 37-key pattern with base64 thumbnails will hit this limit during normal use. AppStorage with IndexedDB fallback is a **prerequisite** for Capacitor wrapping (per Mobile Solutions Architect spec).

---

## 2. VERIFIED AUDIT — All 42 Storage Keys

### 2.1 localStorage Keys (37 active)

#### Analysis & Results (10 keys — HIGH priority, large data)

| # | Key | Type | Default | File(s) | Lines | Error Handling | Size Risk |
|---|-----|------|---------|---------|-------|----------------|-----------|
| 1 | `fl:analysisResults` | `Object\|null` | `null` | useKinshipAnalysis:434, FamiliUnoPage:337, storage.js | 434, 337 | None | HIGH — full engine result |
| 2 | `fl:lastResults` | `Array` | `[]` | useKinshipAnalysis:450, exportResults:63, PeekPreview:15, storage.js | 450, 63, 15 | None | MEDIUM |
| 3 | `fl:familyContext` | `Object\|null` | `null` | useKinshipAnalysis:472, PeekPreview:16, storage.js | 472, 16 | None | LOW |
| 4 | `fl:groupSnapshot` | `Object\|null` | `null` | useKinshipAnalysis:294,541,612, GroupSnapshotSection:2099,2115,2204,2245,2300,2398,2501, FamiliUnoPage:78,88, storage.js | 17 sites | AppErrorBus (low) on parse/persist | HIGH — full group data |
| 5 | `fl:faces` | `Array` | `[]` | GroupSnapshotSection:2300,2399, CardGame:648, storage.js | 4 sites | None | MEDIUM |
| 6 | `fl:pairwise` | `Object\|null` | `null` | GroupSnapshotSection:2412,2414,2516 | 3 sites | None | MEDIUM |
| 7 | `fl:thumbnails` | `Object` (name→dataURL) | `{}` | useKinshipAnalysis:595,633,675, GroupSnapshotSection:1288,2206,2210,2304,2313,2566,2857, deckBuilder:841,982,995, FaceFusion:54, usePetKeepsakeData:24, analytics:279, storage.js | 17 sites | None | **CRITICAL** — base64 images, can exceed 2MB |
| 8 | `fl:thumbnails:ts` | `string` (timestamp) | none | useKinshipAnalysis:596, GroupSnapshotSection:2211,2314,2567, analytics:280, storage.js | 6 sites | None | LOW |
| 9 | `fl:petResults` | `Array` | `[]` | useKinshipAnalysis:674, MobileResultsSection:216, faceFusionConfig:94, usePetKeepsakeData:15, storage.js | 5 sites | AppErrorBus (medium) | MEDIUM |
| 10 | `fl:gameDeck` | `Object` | none | GroupSnapshotSection:2138,2147 | 2 sites | None | MEDIUM |

#### Plan & Subscription (8 keys — HIGH priority, cross-tab sensitive)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 11 | `fl:plan` | `string` | `"free"` | usePlanFeatures:25,71, FamililookContext:112,124, kinshipClient:62, UploadSection:356 | 6 sites | AppErrorBus (medium) on read |
| 12 | `fl:plan-email` | `string` | `""` | usePlanFeatures:33,78, FamililookContext:115,125, kinshipClient:64, PlansPage:91,112,156 | 8 sites | AppErrorBus (low) on read |
| 13 | `fl:plan-verified-at` | `string` (timestamp) | none | usePlanFeatures:150,157,166 | 3 sites | None |
| 14 | `fl:analysisAttempts` | `Object\|null` | `null` | usePlanFeatures:55,85,88 | 3 sites | None |
| 15 | `fl:ambassador` | `Object\|null` (JSON) | `null` | usePlanFeatures:42,48,116,124, PlansPage:205 | 5 sites | AppErrorBus (medium) |
| 16 | `fl:ambassador-email` | `string` | `""` | usePlanFeatures:104, PlansPage:210 | 2 sites | AppErrorBus (medium) |
| 17 | `fl:ambassador-verified-at` | `string` (timestamp) | none | usePlanFeatures:107,117,125, PlansPage:211 | 4 sites | None |
| 18 | `fl:billing-cycle` | `string` | none | PlansPage:32,37 | 2 sites | None |

#### Commerce (3 keys — HIGH priority, data loss risk)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 19 | `fl:basket` | `Array` (JSON) | `[]` | BasketContext:13,31, OrderSuccessPage:28,40 | 4 sites | AppErrorBus (high) on save |
| 20 | `fl:pending-checkout` | `string` (`"true"`) | none | BasketDrawer:71, OrderSuccessPage:38,39, storage.js:128,130 | 5 sites | None |
| 21 | `fl:demo` | `string` (timestamp) | none | planConfig:145,148,154,158 | 4 sites | None |

#### Consent & Compliance (3 keys — CRITICAL, regulatory)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 22 | `fl:consent` | `Object` (JSON) | `{}` | ConsentContext:13,24, config:33, analytics:37,51,173 | 6 sites | None |
| 23 | `fl:age-confirmed-13` | `string` (`"true"`) | none | AgeGateModal:11,17,27 | 3 sites | AppErrorBus (medium) |
| 24 | `fl:age-confirmed-poker` | `string` (`"true"`) | none | AgeGateModal:116,124,134 | 3 sites | AppErrorBus (medium) |

#### Analytics & Session (6 keys — MEDIUM priority)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 25 | `fl:visitor-id` | `string` (UUID) | none | analytics:34,40 | 2 sites | None |
| 26 | `fl:visit-count` | `string` (int) | `"0"` | analytics:54,57,58 | 3 sites | None |
| 27 | `fl:country` | `string` (ISO code) | none | CurrencyContext:27,59, analytics:69 | 3 sites | None |
| 28 | `fl:tab-count` | `string` (int) | `"0"` | analytics:266,267,274,276,281 | 5 sites | AppErrorBus (low) |
| 29 | `fl:returning_user` | `string` (`"true"`) | none | AppRouter:58,60 | 2 sites | None |
| 30 | `fl:feedback-given` | `string` (`"true"`) | none | HomePage:103,769, AppLayout:149,957, FeedbackModal:200, EmotionalJourneyContext:320 | 6 sites | None |

#### Game State (5 keys — LOW priority)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 31 | `fl:game:ageGroup` | `string` | none | MemoryMatch:406,442, FaceFusion:112, HungryHeads:422 | 4 sites | Silent catch |
| 32 | `fl:cardCollection` | `Array` (JSON) | `[]` | CardGame:35,42 | 2 sites | Silent catch |
| 33 | `fl:unoFeatureCount` | `string` (int) | none | FamiliUnoPage:61,115, FaceMatchGame:135,141,902, deckBuilder:857 | 6 sites | None |
| 34 | `fl:game:fusion` | `Object` (JSON) | `{}` | faceFusionStorage:16,32 | 2 sites | None |
| 35 | `fl:achievements` | `Object` (JSON) | none | EmotionalJourneyContext:27,84, AchievementNotification:206,216,263 | 5 sites | None |

#### Trail & Discovery (3 keys — LOW priority)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 36 | `fl:trail_visited` | `Array` (JSON) | `[]` | TrailHomePage:57,78 | 2 sites | Silent catch |
| 37 | `fl:trail_badges` | `Array` (JSON) | `[]` | TrailBadges:65,73 | 2 sites | None |

#### Config & Misc (5 keys — LOW priority)

| # | Key | Type | Default | File(s) | Lines | Error Handling |
|---|-----|------|---------|---------|-------|----------------|
| 38 | `familook_detect_config` | `Object\|null` (JSON) | `null` | detectConfig:8,16,21 | 3 sites | AppErrorBus (low) |
| 39 | `familook_auto_detect` | `string` (`"1"/"0"`) | none | detectConfig:9,26,32 | 3 sites | Silent catch |
| 40 | `fl:settings` | `Object` (JSON) | `{}` | GroupSnapshotSection:2017,2033,2035 | 3 sites | None |
| 41 | `fl:qualityTipsSeen` | `string` (`"1"/"0"`) | none | GroupSnapshotSection:1921,1928 | 2 sites | Silent catch |
| 42 | `fl:analysis-count` | `string` (int) | `"0"` | EmotionalJourneyContext:183,194,195, HomePage:716, AppLayout:222 | 5 sites | None |

#### Additional keys (3 — maintenance, debug, kill switch)

| # | Key | Type | File(s) | Notes |
|---|-----|------|---------|-------|
| 43 | `fl:maintenance-feedback-given` | `string` (`"1"`) | MaintenancePage:162,252 | Maintenance mode only |
| 44 | `fl:disable-mobile-keepsakes` | `string` (`"1"`) | deviceDetection:21 | Kill switch |
| 45 | `fl:family-profiles` | `Object` (JSON, versioned) | familyProfiles:6,16,52,72 | Already has v1 schema |
| 46 | `fl:email-sub:*` | `Object` (JSON) | EmailCapture:15,39 | Dynamic key suffix |
| 47 | `DEBUG_KINSHIP` | `string` (`"1"`) | useKinshipAnalysis:219 | Dev-only flag, no `fl:` prefix |

### 2.2 sessionStorage Keys (5 active)

| # | Key | Type | File(s) | Notes |
|---|-----|------|---------|-------|
| S1 | `fl:analysis-cache` | `Object` (JSON) | FamililookContext:21,25,35,45 | Tab-scoped analysis cache |
| S2 | `fl:seen-instructions-memoryMatch` | `string` (`"1"`) | MemoryMatch:396,400 | Per-tab game instructions |
| S3 | `fl:seen-instructions-cardGame` | `string` (`"1"`) | CardGame:634,638 | Per-tab game instructions |
| S4 | `fl:seen-instructions-featureCatch` | `string` (`"1"`) | FeatureCatch:509,513 | Per-tab game instructions |
| S5 | `fl:seen-instructions-faceMatch` | `string` (`"1"`) | FaceMatchGame:132,140 | Per-tab game instructions |
| S6 | `fl:charMugExplainerDismissed` | `string` (`"1"`) | KeepsakeCustomise:87,95 | Per-tab explainer |
| S7 | `fl:chunk-reload` | `string` (`"1"`) | lazyWithReload:8,22,24,43, ErrorBoundary:55 | Chunk reload guard |

**Note:** sessionStorage keys are intentionally tab-scoped. AppStorage manages localStorage keys only. sessionStorage access stays raw (it is already safe — no quota risk at session scale, no cross-tab sync needed, data is discarded on tab close). The ErrorBoundary already wraps sessionStorage in `safeSessionGet/Set/Remove`. No migration needed.

### 2.3 Summary

| Category | Keys | localStorage Sites | Error Handling |
|----------|------|--------------------|----------------|
| Analysis & Results | 10 | 62 | 2 with AppErrorBus |
| Plan & Subscription | 8 | 34 | 4 with AppErrorBus |
| Commerce | 3 | 13 | 1 with AppErrorBus |
| Consent & Compliance | 3 | 12 | 2 with AppErrorBus |
| Analytics & Session | 6 | 21 | 1 with AppErrorBus |
| Game State | 5 | 19 | 3 silent catches |
| Trail & Discovery | 3 | 4 | 1 silent catch |
| Config & Misc | 8 | 16 | 2 with AppErrorBus, 2 silent |
| **Total** | **46** | **181** | **12 with AppErrorBus, ~8 silent** |

---

## 3. MODULE INTERFACE

### 3.1 Architecture Decision: Vanilla JS Module

**Same reasoning as AppErrorBus:**
- Zero-dependency (no Zustand, no new npm packages)
- Importable from non-React code (`kinshipClient.js`, `analytics.js`, `planConfig.js`, `storage.js`)
- Testable in isolation (no React context needed for unit tests)
- Extractable to `@famililook/shared/infrastructure/AppStorage` without code changes
- Tree-shakeable (plain named exports, no side effects at import time)
- Synchronous initialisation (no `async` constructor — IndexedDB operations are deferred)

**Relationship to existing `storage.js`:**
AppStorage replaces `storage.js` entirely. The existing `STORAGE_KEYS`, `safeJSON()`, `safeSetItem()`, `pruneStalePhotos()`, `pruneStaleCheckout()`, and typed accessors all migrate into AppStorage. After Phase 3, `storage.js` is deleted.

### 3.2 File Location

```
src/infrastructure/AppStorage.js     (new file — sits alongside AppErrorBus.js)
```

### 3.3 Key Schema

Every key is defined in a schema object with type, default value, version, namespace, and persistence tier:

```javascript
/**
 * @typedef {'string' | 'number' | 'boolean' | 'json'} KeyType
 * @typedef {'localStorage' | 'indexedDB'} StorageTier
 *
 * @typedef {Object} KeySchema
 * @property {string}      key         - The fl:* key name
 * @property {KeyType}     type        - How to serialize/deserialize
 * @property {*}           defaultVal  - Value returned when key is missing
 * @property {number}      version     - Schema version (starts at 1)
 * @property {string}      namespace   - Logical grouping: 'analysis', 'plan', 'commerce', 'consent', 'analytics', 'game', 'trail', 'config'
 * @property {boolean}     tabSync     - Whether to broadcast changes via BroadcastChannel
 * @property {StorageTier} tier        - 'localStorage' for all standard keys, 'indexedDB' for large values
 */

const KEY_SCHEMA = {
  // ─── Analysis & Results ──────────────────────────────────────
  'fl:analysisResults':      { type: 'json', defaultVal: null,  version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:lastResults':          { type: 'json', defaultVal: [],    version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:familyContext':        { type: 'json', defaultVal: null,  version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:groupSnapshot':        { type: 'json', defaultVal: null,  version: 1, namespace: 'analysis', tabSync: true,  tier: 'localStorage' },
  'fl:faces':                { type: 'json', defaultVal: [],    version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:pairwise':             { type: 'json', defaultVal: null,  version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:thumbnails':           { type: 'json', defaultVal: {},    version: 1, namespace: 'analysis', tabSync: false, tier: 'indexedDB' },
  'fl:thumbnails:ts':        { type: 'string', defaultVal: null, version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:petResults':           { type: 'json', defaultVal: [],    version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },
  'fl:gameDeck':             { type: 'json', defaultVal: null,  version: 1, namespace: 'analysis', tabSync: false, tier: 'localStorage' },

  // ─── Plan & Subscription ─────────────────────────────────────
  'fl:plan':                 { type: 'string', defaultVal: 'free', version: 1, namespace: 'plan', tabSync: true,  tier: 'localStorage' },
  'fl:plan-email':           { type: 'string', defaultVal: '',    version: 1, namespace: 'plan', tabSync: true,  tier: 'localStorage' },
  'fl:plan-verified-at':     { type: 'string', defaultVal: null,  version: 1, namespace: 'plan', tabSync: false, tier: 'localStorage' },
  'fl:analysisAttempts':     { type: 'json',   defaultVal: null,  version: 1, namespace: 'plan', tabSync: false, tier: 'localStorage' },
  'fl:ambassador':           { type: 'json',   defaultVal: null,  version: 1, namespace: 'plan', tabSync: true,  tier: 'localStorage' },
  'fl:ambassador-email':     { type: 'string', defaultVal: '',    version: 1, namespace: 'plan', tabSync: false, tier: 'localStorage' },
  'fl:ambassador-verified-at': { type: 'string', defaultVal: null, version: 1, namespace: 'plan', tabSync: false, tier: 'localStorage' },
  'fl:billing-cycle':        { type: 'string', defaultVal: null,  version: 1, namespace: 'plan', tabSync: false, tier: 'localStorage' },

  // ─── Commerce ────────────────────────────────────────────────
  'fl:basket':               { type: 'json',   defaultVal: [],    version: 1, namespace: 'commerce', tabSync: true,  tier: 'localStorage' },
  'fl:pending-checkout':     { type: 'string', defaultVal: null,  version: 1, namespace: 'commerce', tabSync: false, tier: 'localStorage' },
  'fl:demo':                 { type: 'string', defaultVal: null,  version: 1, namespace: 'commerce', tabSync: false, tier: 'localStorage' },

  // ─── Consent & Compliance ────────────────────────────────────
  'fl:consent':              { type: 'json',   defaultVal: {},    version: 1, namespace: 'consent', tabSync: true,  tier: 'localStorage' },
  'fl:age-confirmed-13':     { type: 'string', defaultVal: null,  version: 1, namespace: 'consent', tabSync: false, tier: 'localStorage' },
  'fl:age-confirmed-poker':  { type: 'string', defaultVal: null,  version: 1, namespace: 'consent', tabSync: false, tier: 'localStorage' },

  // ─── Analytics & Session ─────────────────────────────────────
  'fl:visitor-id':           { type: 'string', defaultVal: null,  version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:visit-count':          { type: 'number', defaultVal: 0,     version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:country':              { type: 'string', defaultVal: null,  version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:tab-count':            { type: 'number', defaultVal: 0,     version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:returning_user':       { type: 'string', defaultVal: null,  version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:feedback-given':       { type: 'string', defaultVal: null,  version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },
  'fl:analysis-count':       { type: 'number', defaultVal: 0,     version: 1, namespace: 'analytics', tabSync: false, tier: 'localStorage' },

  // ─── Game State ──────────────────────────────────────────────
  'fl:game:ageGroup':        { type: 'string', defaultVal: null,  version: 1, namespace: 'game', tabSync: false, tier: 'localStorage' },
  'fl:cardCollection':       { type: 'json',   defaultVal: [],    version: 1, namespace: 'game', tabSync: false, tier: 'localStorage' },
  'fl:unoFeatureCount':      { type: 'number', defaultVal: 3,     version: 1, namespace: 'game', tabSync: false, tier: 'localStorage' },
  'fl:game:fusion':          { type: 'json',   defaultVal: {},    version: 1, namespace: 'game', tabSync: false, tier: 'localStorage' },
  'fl:achievements':         { type: 'json',   defaultVal: null,  version: 1, namespace: 'game', tabSync: false, tier: 'localStorage' },

  // ─── Trail & Discovery ──────────────────────────────────────
  'fl:trail_visited':        { type: 'json',   defaultVal: [],    version: 1, namespace: 'trail', tabSync: false, tier: 'localStorage' },
  'fl:trail_badges':         { type: 'json',   defaultVal: [],    version: 1, namespace: 'trail', tabSync: false, tier: 'localStorage' },

  // ─── Config & Misc ──────────────────────────────────────────
  'familook_detect_config':  { type: 'json',   defaultVal: null,  version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'familook_auto_detect':    { type: 'string', defaultVal: null,  version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'fl:settings':             { type: 'json',   defaultVal: {},    version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'fl:qualityTipsSeen':      { type: 'string', defaultVal: null,  version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'fl:maintenance-feedback-given': { type: 'string', defaultVal: null, version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'fl:disable-mobile-keepsakes':   { type: 'string', defaultVal: null, version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
  'fl:family-profiles':      { type: 'json',   defaultVal: null,  version: 1, namespace: 'config', tabSync: false, tier: 'localStorage' },
};
```

### 3.4 Public API

```javascript
/**
 * @typedef {Object} AppStorageStats
 * @property {number} totalKeys       - Number of registered keys
 * @property {number} usedKeys        - Number of keys with non-null values
 * @property {number} estimatedBytes  - Approximate total storage usage
 * @property {Object} byNamespace     - Key counts per namespace
 */

// ─── Core CRUD ──────────────────────────────────────────────────

AppStorage.get(key: string): any
// Returns the typed, deserialized value for a registered key.
// If key has no value stored: returns the schema defaultVal.
// If key is not in KEY_SCHEMA: throws Error('Unknown storage key: <key>').
// If stored value fails to parse: returns defaultVal, reports to AppErrorBus
//   (severity: 'low', code: 'STORAGE_PARSE_FAIL').
// For 'indexedDB' tier keys: returns cached in-memory value synchronously.
//   IndexedDB is read on module init and kept in sync.
// Type coercion:
//   'string'  → returns as-is (or defaultVal if null)
//   'number'  → parseInt/parseFloat (or defaultVal if NaN)
//   'boolean' → value === 'true' (or defaultVal if null)
//   'json'    → JSON.parse (or defaultVal if parse fails)

AppStorage.set(key: string, value: any): boolean
// Serializes and stores the value. Returns true if successful.
// If key is not in KEY_SCHEMA: throws Error('Unknown storage key: <key>').
// For 'indexedDB' tier keys: writes to in-memory cache immediately (sync),
//   then persists to IndexedDB asynchronously. Returns true for the sync write.
// For 'localStorage' tier keys: writes to localStorage.
//   If QuotaExceededError:
//     1. Calls pruneStalePhotos(0) — attempt to free space
//     2. Retries once
//     3. If still fails: reports to AppErrorBus (severity: 'high',
//        code: 'STORAGE_QUOTA_EXCEEDED', meta: { key, valueSize })
//     4. Returns false
// If key.tabSync is true: broadcasts change via BroadcastChannel.
// Type serialization:
//   'string'  → stored as-is
//   'number'  → String(value)
//   'boolean' → String(value)
//   'json'    → JSON.stringify(value)

AppStorage.remove(key: string): void
// Removes the value for a registered key. Returns void.
// If key is not in KEY_SCHEMA: throws Error('Unknown storage key: <key>').
// For 'indexedDB' tier keys: removes from cache and IndexedDB.
// For 'localStorage' tier keys: calls localStorage.removeItem.
// If key.tabSync is true: broadcasts removal via BroadcastChannel.

AppStorage.clear(namespace?: string): void
// If namespace provided: removes all keys in that namespace.
// If no namespace: removes ALL registered keys. GDPR forget-me uses this.
// Does NOT remove unregistered keys (e.g. third-party cookie consent).
// Notifies BroadcastChannel for any tabSync keys removed.
// Reports to AppErrorBus (severity: 'low', code: 'STORAGE_CLEARED',
//   meta: { namespace, keysRemoved: count }).

// ─── Multi-tab Sync ─────────────────────────────────────────────

AppStorage.onExternalChange(key: string, callback: (newValue: any, oldValue: any) => void): () => void
// Subscribe to external changes (from other tabs) for a specific key.
// Returns an unsubscribe function.
// Only fires for keys with tabSync: true in the schema.
// Uses BroadcastChannel under the hood.
// If BroadcastChannel unavailable (Safari private mode): silently no-ops.
//   The callback is never called. The module still works for single-tab use.
// Callback receives the deserialized new and old values.

// ─── Schema Versioning ──────────────────────────────────────────

AppStorage.runMigrations(): void
// Called once on module initialisation (synchronous for localStorage keys).
// For each key in KEY_SCHEMA:
//   1. Read `fl:_schema_version` from localStorage (default: 0)
//   2. If stored version < current SCHEMA_VERSION: run registered
//      migration functions in order (v1→v2, v2→v3, etc.)
//   3. After all migrations: write current SCHEMA_VERSION to `fl:_schema_version`
// Migration functions are registered via AppStorage.registerMigration().
// If a migration fails: the key value is reset to defaultVal, and the failure
//   is reported to AppErrorBus (severity: 'high', code: 'STORAGE_MIGRATION_FAIL').

AppStorage.registerMigration(fromVersion: number, migrateFn: (storedData: Object) => Object): void
// Register a migration function that transforms stored data from one
// schema version to the next. Called during AppStorage.runMigrations().
// Example:
//   AppStorage.registerMigration(1, (data) => {
//     // v1 → v2: rename fl:cardDeck to fl:gameDeck
//     if (data['fl:cardDeck']) {
//       data['fl:gameDeck'] = data['fl:cardDeck'];
//       delete data['fl:cardDeck'];
//     }
//     return data;
//   });

// ─── Pruning ────────────────────────────────────────────────────

AppStorage.pruneStalePhotos(maxAgeMs?: number): number
// Replaces the existing pruneStalePhotos() from storage.js.
// Removes analysis-related keys if fl:thumbnails:ts is older than maxAgeMs
// (default: 25 hours). Returns count of keys removed.
// Keys pruned: fl:thumbnails, fl:thumbnails:ts, fl:analysisResults,
//   fl:lastResults, fl:groupSnapshot, fl:pairwise, fl:faces,
//   fl:petResults, fl:familyContext, fl:gameDeck.

AppStorage.pruneStaleCheckout(): void
// Replaces the existing pruneStaleCheckout() from storage.js.
// Removes fl:pending-checkout if it exists.

// ─── Dev Tools ──────────────────────────────────────────────────

AppStorage.getStats(): AppStorageStats
// Returns storage statistics. Only meaningful in DEV mode.
// In PROD: returns zeroed stats (tree-shaken).

AppStorage.dump(): Object
// Returns all registered key-value pairs as a plain object.
// DEV mode only. Useful for console inspection.

// ─── Constants ──────────────────────────────────────────────────

AppStorage.SCHEMA_VERSION: number
// Current schema version. Starts at 1. Incremented when key shapes change.

AppStorage.KEYS: Readonly<Record<string, string>>
// Frozen object mapping logical names to key strings.
// Replaces STORAGE_KEYS from storage.js.
// Example: AppStorage.KEYS.PLAN === 'fl:plan'
```

### 3.5 Quota Error Handling — Detailed Flow

```
1. AppStorage.set('fl:basket', items)
2.   → JSON.stringify(items)
3.   → localStorage.setItem('fl:basket', serialized)
4.   → QuotaExceededError thrown
5.   → Catch: call AppStorage.pruneStalePhotos(0)  // aggressive cleanup
6.   → Retry: localStorage.setItem('fl:basket', serialized)
7.   → Still fails?
8.     → AppErrorBus.report({
9.         message: 'Could not save — storage is full. Your data is still
10.                  in memory but may not survive a page refresh.',
11.        context: `AppStorage.set(${key})`,
12.        severity: 'high',
13.        code: 'STORAGE_QUOTA_EXCEEDED',
14.        meta: { key, valueSize: serialized.length, estimatedUsage }
15.      })
16.    → Return false (caller knows write failed)
```

### 3.6 IndexedDB Fallback — For Large Values Only

**Only `fl:thumbnails` uses IndexedDB tier** in v1. This single key stores base64-encoded face thumbnails that can exceed 2MB for a family of 5.

**How it works:**
1. On module init: read `fl:thumbnails` from IndexedDB into an in-memory cache
2. `AppStorage.get('fl:thumbnails')` → returns the in-memory cache (synchronous)
3. `AppStorage.set('fl:thumbnails', value)` → updates in-memory cache (synchronous), then `queueMicrotask(() => writeToIndexedDB(value))` (async)
4. If IndexedDB is unavailable (private browsing): falls back to localStorage with a console warning. The quota risk is acknowledged but the app still works.

**IndexedDB database:**
- Name: `famililook_storage`
- Version: 1
- Store: `kv` (key-value store, keyPath: `key`)

### 3.7 BroadcastChannel — Multi-tab Sync

**Channel name:** `famililook_storage_sync`

**Keys with tabSync enabled:**
- `fl:groupSnapshot` — prevents stale snapshot in second tab after new analysis
- `fl:plan` — plan upgrade in Tab A reflects immediately in Tab B
- `fl:plan-email` — same as above
- `fl:ambassador` — ambassador code applied in Tab A reflects in Tab B
- `fl:basket` — basket changes sync across tabs (prevent lost items)
- `fl:consent` — consent change in one tab applies everywhere

**Message format:**
```javascript
{
  type: 'set' | 'remove' | 'clear',
  key: 'fl:plan',          // for 'set'/'remove'
  value: 'plus',           // for 'set' only (already serialized)
  namespace: 'plan',       // for 'clear' only
  ts: Date.now()
}
```

**On receive:** Update the local in-memory state and fire any registered `onExternalChange` callbacks. Do NOT write back to localStorage (the sending tab already did that — writing again would loop).

**Fallback:** If `BroadcastChannel` is not available (Safari private mode, older browsers), the module works identically for single-tab use. The `onExternalChange` callback is never fired. The `storage` event on `window` is used as a secondary fallback (fires for cross-tab localStorage changes, not same-tab).

---

## 4. ADOPTION RULE

**Once AppStorage ships (Phase 1 complete), the following is FORBIDDEN:**

### Rule A: No direct localStorage access

```javascript
// FORBIDDEN after Phase 1:
localStorage.getItem('fl:plan')
localStorage.setItem('fl:basket', JSON.stringify(items))
localStorage.removeItem('fl:thumbnails')

// REQUIRED:
import { AppStorage } from '../infrastructure/AppStorage';
AppStorage.get('fl:plan')
AppStorage.set('fl:basket', items)
AppStorage.remove('fl:thumbnails')
```

### Rule B: No inline key strings

```javascript
// FORBIDDEN:
AppStorage.get('fl:plan')

// PREFERRED (after migration is complete):
AppStorage.get(AppStorage.KEYS.PLAN)
```

### Rule C: No new keys without schema registration

```javascript
// FORBIDDEN:
localStorage.setItem('fl:new-feature', 'value')

// REQUIRED:
// 1. Add key to KEY_SCHEMA in AppStorage.js
// 2. Use AppStorage.set('fl:new-feature', 'value')
```

### Enforcement

- **Change Manager** — reviews all PRs for raw `localStorage.getItem/setItem/removeItem` calls outside of `AppStorage.js` itself. Rejects any PR that introduces direct localStorage access.
- **Platform Architect** — blocks any PR that adds a new localStorage key without registering it in KEY_SCHEMA.
- **QA Lead** — verifies that migration phases are complete. Blocks release if raw localStorage calls remain in migrated files.
- **ESLint rule** (Phase 4) — `no-direct-localstorage` custom rule that flags any `localStorage.getItem`, `localStorage.setItem`, or `localStorage.removeItem` call outside of `AppStorage.js`. Severity: `error` (blocks CI).

---

## 5. MIGRATION PATH

### Phase 1: Build AppStorage.js + Tests (1 session)

**Deliverables:**
1. Create `src/infrastructure/AppStorage.js` — full module per Section 3 spec
2. Wire AppErrorBus integration for quota errors and parse failures
3. Implement IndexedDB fallback for `fl:thumbnails`
4. Implement BroadcastChannel sync for tabSync keys
5. Implement schema versioning with `runMigrations()` / `registerMigration()`
6. Migrate `pruneStalePhotos()` and `pruneStaleCheckout()` from storage.js
7. Unit tests (see Section 7)

**Zero migration in Phase 1.** No existing files are changed. The module is built and tested in isolation. `storage.js` remains untouched.

### Phase 2: Migrate Blocked Files — FamililookContext + BasketContext (1 session)

These are the highest-risk files. Both are on the FE Lead blocked files list. CEO waiver is required before FE Lead touches them.

**Phase 2 files:**

| File | localStorage Calls | What Changes |
|------|--------------------|--------------|
| `state/FamililookContext.jsx` | 4 (`fl:plan` ×2, `fl:plan-email` ×2) | Replace `localStorage.getItem("fl:plan")` with `AppStorage.get('fl:plan')`. Remove try/catch — AppStorage handles errors internally. |
| `state/BasketContext.jsx` | 2 (`fl:basket` load + save) | Replace `localStorage.getItem/setItem` with `AppStorage.get/set`. Remove try/catch + AppErrorBus.report — AppStorage handles quota + reporting internally. |

**Phase 2 also migrates:**
| File | localStorage Calls | What Changes |
|------|--------------------|--------------|
| `hooks/usePlanFeatures.js` | 18 (all plan + ambassador keys) | Replace all raw `localStorage` calls with `AppStorage.get/set/remove`. Remove per-call try/catch — AppStorage handles errors. Remove import of `STORAGE_KEYS` from storage.js — use `AppStorage.KEYS`. |
| `api/kinshipClient.js` | 2 (`fl:plan`, `fl:plan-email`) | Replace raw reads with AppStorage.get. Remove try/catch. |

**Total:** 4 files, 26 localStorage call sites migrated.

### Phase 3: Full Migration (1–2 sessions)

Migrate all remaining files. Files grouped by domain:

**Analysis & Results (4 files, ~45 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `hooks/useKinshipAnalysis.jsx` | 14 | groupSnapshot, analysisResults, lastResults, familyContext, thumbnails, thumbnails:ts, petResults |
| `layout/GroupSnapshotSection.jsx` | 28 | groupSnapshot, thumbnails, thumbnails:ts, faces, pairwise, gameDeck, settings, qualityTipsSeen |
| `layout/MobileResultsSection.jsx` | 1 | petResults |
| `utils/exportResults.js` | 4 | lastResults, faces, thumbnails, analysisCache |

**Commerce & Plans (3 files, ~8 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `pages/PlansPage.jsx` | 8 | billing-cycle, plan-email, plan-verified-at, ambassador, ambassador-email, ambassador-verified-at |
| `pages/OrderSuccessPage.jsx` | 4 | basket, pending-checkout |
| `components/keepsakes/BasketDrawer.jsx` | 1 | pending-checkout |

**Analytics & Session (3 files, ~14 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `utils/analytics.js` | 12 | visitor-id, visit-count, consent, country, tab-count, thumbnails, thumbnails:ts |
| `utils/config.js` | 1 | consent |
| `AppRouter.jsx` | 2 | returning_user |

**State & Context (4 files, ~10 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `state/ConsentContext.jsx` | 2 | consent |
| `state/CurrencyContext.jsx` | 2 | country |
| `state/EmotionalJourneyContext.jsx` | 5 | achievements, analysis-count, feedback-given |
| `state/detectConfig.js` | 4 | familook_detect_config, familook_auto_detect |

**Games (7 files, ~16 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `game/CardGame.jsx` | 3 | cardCollection, faces |
| `game/FaceMatchGame.jsx` | 3 | unoFeatureCount |
| `game/MemoryMatch.jsx` | 2 | game:ageGroup |
| `game/FaceFusion/FaceFusion.jsx` | 2 | thumbnails, game:ageGroup |
| `game/FaceFusion/faceFusionStorage.js` | 2 | game:fusion |
| `game/FaceFusion/faceFusionConfig.js` | 1 | petResults |
| `game/deckBuilder.js` | 4 | thumbnails, unoFeatureCount |
| `game/HungryHeads/HungryHeads.jsx` | 1 | game:ageGroup |

**Pages & Components (7 files, ~14 call sites):**

| File | Calls | Keys |
|------|-------|------|
| `pages/HomePage.jsx` | 3 | feedback-given, analysis-count |
| `pages/FamiliUnoPage.jsx` | 4 | unoFeatureCount, groupSnapshot, analysisResults |
| `pages/TrailHomePage.jsx` | 4 | trail_visited, trail completion keys |
| `pages/MaintenancePage.jsx` | 2 | maintenance-feedback-given |
| `layout/AppLayout.jsx` | 3 | feedback-given, analysis-count |
| `layout/UploadSection.jsx` | 1 | plan |
| `components/trail/TrailBadges.jsx` | 2 | trail_badges |
| `components/trail/PeekPreview.jsx` | 2 | lastResults, familyContext |
| `components/ui/AgeGateModal.jsx` | 5 | age-confirmed-13, age-confirmed-poker |
| `components/ui/EmailCapture.jsx` | 2 | email-sub:* dynamic key |
| `components/modals/AchievementNotification.jsx` | 3 | achievements |
| `components/keepsakes/hooks/usePetKeepsakeData.js` | 2 | petResults, thumbnails |

**Cleanup (1 file):**

| File | Action |
|------|--------|
| `utils/storage.js` | DELETE after all consumers migrated. All exports replaced by AppStorage. |
| `utils/familyProfiles.js` | Migrate 3 calls. |
| `utils/planConfig.js` | Migrate 4 calls (fl:demo). |
| `utils/deviceDetection.js` | Migrate 1 call (kill switch). |
| `utils/gameState.js` | Migrate 1 call (removeItem). |

### Phase 4: ESLint Rule (0.5 session)

1. Add ESLint rule to `eslint.config.js`:
   - Custom rule `no-direct-localstorage`
   - Flags any `localStorage.getItem`, `localStorage.setItem`, `localStorage.removeItem`, or `localStorage.clear` call
   - Exemption: `src/infrastructure/AppStorage.js` (the module itself)
   - Severity: `error` (blocks CI)
2. Optionally rename the two non-`fl:` keys (`familook_detect_config`, `familook_auto_detect`) to `fl:detect-config` and `fl:auto-detect` via a v1→v2 schema migration

---

## 6. FILES AFFECTED — Complete List

### New Files (Phase 1)

| File | Purpose |
|------|---------|
| `src/infrastructure/AppStorage.js` | Core storage module |
| `tests/infrastructure/AppStorage.test.js` | Unit tests |

### Modified Files (Phase 2) — 4 files

| File | Change |
|------|--------|
| `state/FamililookContext.jsx` | 4 localStorage calls → AppStorage |
| `state/BasketContext.jsx` | 2 localStorage calls → AppStorage |
| `hooks/usePlanFeatures.js` | 18 localStorage calls → AppStorage |
| `api/kinshipClient.js` | 2 localStorage calls → AppStorage |

### Modified Files (Phase 3) — ~30 files

See Phase 3 listing above for complete file list.

### Deleted Files (Phase 3)

| File | Reason |
|------|--------|
| `utils/storage.js` | All functionality absorbed into AppStorage |

### Modified Files (Phase 4)

| File | Change |
|------|--------|
| `eslint.config.js` | Add `no-direct-localstorage` rule |

---

## 7. TEST REQUIREMENTS

### 7.1 Unit Tests — AppStorage (`AppStorage.test.js`)

**Must test (minimum 15):**

1. **get() returns default for missing key** — call `get('fl:plan')` with no value stored, verify returns `'free'`
2. **set() and get() roundtrip (string)** — set a string key, get it back, verify exact match
3. **set() and get() roundtrip (json)** — set a JSON key (object), get it back, verify deep equality
4. **set() and get() roundtrip (number)** — set `'fl:visit-count'` to `5`, get it back, verify `5` (not `'5'`)
5. **get() returns default on corrupt JSON** — manually write invalid JSON to localStorage for a `json`-type key, verify `get()` returns `defaultVal`
6. **get() reports AppErrorBus on corrupt JSON** — same as above, verify `AppErrorBus.getActive()` has a `low` severity error with code `STORAGE_PARSE_FAIL`
7. **set() unknown key throws** — call `set('fl:nonexistent', 'value')`, verify throws `Error('Unknown storage key')`
8. **get() unknown key throws** — call `get('fl:nonexistent')`, verify throws
9. **remove() removes value** — set a key, remove it, verify `get()` returns default
10. **clear() with namespace** — set keys in `'plan'` and `'game'` namespaces, call `clear('plan')`, verify plan keys removed and game keys retained
11. **clear() without namespace** — set multiple keys, call `clear()`, verify all removed
12. **Quota exceeded triggers AppErrorBus** — mock `localStorage.setItem` to throw `QuotaExceededError`, call `set()`, verify `AppErrorBus.getActive()` has a `high` severity error with code `STORAGE_QUOTA_EXCEEDED`
13. **Quota exceeded returns false** — same mock, verify `set()` returns `false`
14. **Schema migration runs on stale version** — register a migration from v1→v2, set `fl:_schema_version` to `1`, add a key that needs migration, call `runMigrations()`, verify the key was migrated
15. **Schema migration failure resets to default** — register a migration that throws, verify the affected key is reset to `defaultVal` and AppErrorBus reports `STORAGE_MIGRATION_FAIL`
16. **KEYS constant is frozen** — verify `Object.isFrozen(AppStorage.KEYS)`
17. **getStats() returns correct counts** — set 3 keys, verify `usedKeys === 3`

### 7.2 Integration Tests — AppStorage + AppErrorBus (minimum 3)

1. **Quota path end-to-end** — mock `localStorage.setItem` to always throw, call `AppStorage.set('fl:basket', items)`, verify:
   - `AppStorage.set()` returns `false`
   - `AppErrorBus.getActive()` contains exactly 1 error
   - Error severity is `'high'`
   - Error code is `'STORAGE_QUOTA_EXCEEDED'`
   - Error message is human-readable
2. **Parse failure path** — write `'not json'` directly to localStorage for `fl:basket`, call `AppStorage.get('fl:basket')`, verify:
   - Returns `[]` (the default)
   - `AppErrorBus.getActive()` contains a `low` severity parse error
3. **Clear reports to AppErrorBus** — set 5 keys, call `AppStorage.clear()`, verify AppErrorBus received a `low` severity `STORAGE_CLEARED` report

### 7.3 BroadcastChannel Tests (minimum 2)

1. **onExternalChange fires on external set** — subscribe to `fl:plan`, simulate a BroadcastChannel message (or use the `storage` event fallback), verify callback fires with correct `newValue` and `oldValue`
2. **onExternalChange does NOT fire for non-tabSync keys** — subscribe to `fl:game:ageGroup` (tabSync: false), simulate external change, verify callback is NOT fired

### 7.4 IndexedDB Tests (minimum 2)

1. **IndexedDB tier set/get roundtrip** — call `AppStorage.set('fl:thumbnails', largeObject)`, verify `AppStorage.get('fl:thumbnails')` returns the object (from in-memory cache)
2. **IndexedDB fallback to localStorage** — mock `indexedDB` as unavailable, verify `fl:thumbnails` falls back to localStorage with a console warning

---

## 8. SECONDARY FAILURE RISKS

### Risk 1: BroadcastChannel Not Supported
**Scenario:** Safari private browsing mode does not support `BroadcastChannel`.
**Mitigation:** Feature-detect `typeof BroadcastChannel !== 'undefined'`. If unavailable, use the `window.addEventListener('storage', ...)` event as fallback (fires for cross-tab localStorage changes, not same-tab). If both unavailable: single-tab mode — `onExternalChange` callbacks are never fired. The module still works. No crash, no error.

### Risk 2: IndexedDB Blocked
**Scenario:** Private browsing on some browsers blocks IndexedDB entirely. Firefox private mode allows it but with 0 quota.
**Mitigation:** On module init, attempt to open the IndexedDB database. If it fails or times out (2-second timeout): fall back to localStorage for all keys including `fl:thumbnails`. Log a dev warning. The app works — the risk of quota exhaustion increases, but it's the same risk as the current pattern (which has no IndexedDB at all).

### Risk 3: Schema Migration Failure on Corrupt Data
**Scenario:** A migration function receives data that doesn't match the expected v1 shape (manually edited, browser extension interference, or silent corruption).
**Mitigation:** Each migration function runs inside a try/catch. On failure: the affected key is reset to its `defaultVal`. The failure is reported to AppErrorBus (`severity: 'high'`, `code: 'STORAGE_MIGRATION_FAIL'`). The user loses that key's data but the app continues working. This is better than crashing.

### Risk 4: Re-entrancy During AppErrorBus.report Inside Quota Catch
**Scenario:** `AppStorage.set()` fails with quota error → calls `AppErrorBus.report()` → AppErrorBus subscriber tries to persist the error → calls `AppStorage.set()` → infinite loop.
**Mitigation:** AppErrorBus does NOT persist errors to storage (by design — errors are in-memory only, per AppErrorBus spec Section 10 "Do Not"). Even if a future change violates this, AppStorage has a re-entrancy guard: a module-level `let _isReporting = false` flag. If `set()` is called while `_isReporting` is true, the quota error is logged to `console.error` instead of calling `AppErrorBus.report()`.

### Risk 5: `storage` Event Firing During Same-Tab Write
**Scenario:** The `storage` event fires in the same tab that wrote the value, causing `onExternalChange` to fire for the originating tab.
**Mitigation:** The `storage` event only fires in OTHER tabs, not the originating tab. This is spec-compliant browser behavior. BroadcastChannel messages do NOT echo back to the sender by default. Both paths are safe.

### Risk 6: Module Init Fails
**Scenario:** The module-level initialisation (reading IndexedDB, checking schema version) fails entirely.
**Mitigation:** All init code is wrapped in try/catch. On failure: the module operates in "degraded mode" — all operations use localStorage directly (no IndexedDB, no BroadcastChannel, no migration). A `console.error` is logged. The app continues working. This is equivalent to the current pattern.

### Risk 7: Email Capture Dynamic Keys
**Scenario:** `EmailCapture.jsx` uses dynamic keys (`fl:email-sub:${storageKey}`). These are not statically registered in KEY_SCHEMA.
**Mitigation:** `EmailCapture` uses a `storageKey` prop that generates keys like `fl:email-sub:maintenance`. These are registered with a wildcard pattern: `AppStorage.setDynamic('fl:email-sub', suffix, value)`. A separate API method handles dynamic-suffix keys while still enforcing the `fl:` prefix and providing quota error handling. Alternatively, EmailCapture can be migrated to use a single `fl:email-submissions` JSON key that stores all submissions as an object. Decision: FE Lead chooses during Phase 3. Both approaches are acceptable.

---

## 9. BUILD ESTIMATE

| Phase | Sessions | FE Lead Work |
|-------|----------|-------------|
| Phase 1: Build AppStorage.js + Tests | 1 | Build module, wire AppErrorBus, IndexedDB init, BroadcastChannel, schema versioning, 22+ tests |
| Phase 2: Migrate blocked files | 1 | 4 files (FamililookContext, BasketContext, usePlanFeatures, kinshipClient), 26 call sites. CEO waiver required. |
| Phase 3: Full migration | 1–2 | ~30 files, ~150 call sites. Mechanical replacement. Delete storage.js. |
| Phase 4: ESLint rule | 0.5 | Add `no-direct-localstorage` rule. Optional key rename migration. |
| **Total** | **3.5–4.5 sessions** | |

**Dependencies:**
- AppErrorBus must be built first (it is — Phases 1-3 complete)
- No new npm dependencies required
- IndexedDB and BroadcastChannel are browser APIs (no polyfills needed for our browser targets)

**Risk to existing tests:** LOW. Phases 2-3 replace `localStorage.getItem/setItem` calls with `AppStorage.get/set` calls. No logic changes. No return values modified. Existing tests should pass without modification if `AppStorage` is properly mocked in the test environment (the module must be mockable — no side effects at import time).

---

## 10. IMPLEMENTATION NOTES FOR FE LEAD

### Do:
- Keep the module as a plain ES module (no class, no React context for the module itself)
- Import `AppErrorBus` from `'../infrastructure/AppErrorBus'` (sibling import — both in infrastructure/)
- Use `Object.freeze()` on the `KEYS` constant to prevent mutation
- Use a module-level `Map` for in-memory IndexedDB cache (not an object — Map handles arbitrary key strings better)
- Initialise synchronously: read localStorage keys immediately, start IndexedDB read in background via `queueMicrotask`
- All fl:* key names must use the existing `fl:` prefix convention already established in the codebase
- Keep `pruneStalePhotos()` and `pruneStaleCheckout()` as methods on AppStorage (they are storage operations, not general utilities)
- Export `KEY_SCHEMA` as a frozen constant for test assertions

### Do Not:
- Do NOT use React context for the module. It must be importable from non-React code (`kinshipClient.js`, `analytics.js`)
- Do NOT use `async/await` in the module's top-level scope. The module must be importable without `await`. IndexedDB operations are deferred to microtasks.
- Do NOT add new npm dependencies (no `idb`, no `localforage`)
- Do NOT modify sessionStorage handling. sessionStorage keys stay raw (ErrorBoundary wraps them, they are tab-scoped, no cross-tab sync needed)
- Do NOT persist AppStorage metadata to IndexedDB (schema version stays in localStorage as `fl:_schema_version`)
- Do NOT make `AppStorage.get()` async — callers currently use synchronous `localStorage.getItem()` and cannot be changed to `await` without rewriting every consumer

### Key Naming Convention:
- All keys MUST use the `fl:` prefix
- The two legacy keys (`familook_detect_config`, `familook_auto_detect`) keep their names in v1. A v1→v2 migration renames them in Phase 4 (optional).
- New keys added by future features must be registered in `KEY_SCHEMA` before use

### Relationship to storage.js:
- Phase 1: AppStorage is created alongside storage.js. Both exist. No imports change.
- Phase 2-3: Files migrate from `import { STORAGE_KEYS, safeJSON } from '../utils/storage'` to `import { AppStorage } from '../infrastructure/AppStorage'`
- Phase 3 (end): `storage.js` is deleted. All its exports are absorbed into AppStorage.

---

## APPENDIX A: Example Migration — FamililookContext.jsx

**Before (current code, lines 112-115):**
```javascript
const initCurrentPlan = () => {
  try { return localStorage.getItem("fl:plan") || "free"; } catch (e) {
    reportError({ message: 'Could not read plan from localStorage — defaulting to free tier', context: 'FamililookContext.initCurrentPlan', severity: 'medium', code: 'PLAN_STATE_FAIL', cause: e });
    return "free";
  }
};
const initPlanEmail = () => {
  try { return localStorage.getItem("fl:plan-email") || ""; } catch (e) {
    reportError({ message: 'Could not read plan email from localStorage', context: 'FamililookContext.initPlanEmail', severity: 'low', code: 'PLAN_STATE_FAIL', cause: e });
    return "";
  }
};
```

**After (Phase 2 migration):**
```javascript
import { AppStorage } from '../infrastructure/AppStorage';

const initCurrentPlan = () => AppStorage.get('fl:plan');
const initPlanEmail = () => AppStorage.get('fl:plan-email');
```

**Key points:**
- The try/catch is removed — AppStorage handles parse errors internally and reports to AppErrorBus
- The `|| "free"` fallback is removed — AppStorage returns `defaultVal` (`'free'`) when the key is missing
- The `reportError` call is removed — AppStorage reports to AppErrorBus on its own for parse failures
- Two functions reduced to one line each. Total: -10 lines of code per function.

---

## APPENDIX B: Example Quota Path — BasketContext.jsx

**Before (current code, lines 13-33):**
```javascript
import { AppErrorBus } from '../infrastructure/AppErrorBus';

const STORAGE_KEY = "fl:basket";

function loadBasket() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    AppErrorBus.report({
      message: 'Could not load your basket from storage — starting with empty basket',
      context: 'BasketContext.loadBasket',
      severity: 'high',
      code: 'BASKET_LOAD_FAIL',
      cause: e,
    });
    return [];
  }
}

function saveBasket(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch (e) {
    AppErrorBus.report({
      message: 'Could not save your basket — storage may be full. Your items are still in memory but may not survive a page refresh.',
      context: 'BasketContext.saveBasket',
      severity: 'high',
      code: 'STORAGE_FULL',
      cause: e,
    });
  }
}
```

**After (Phase 2 migration):**
```javascript
import { AppStorage } from '../infrastructure/AppStorage';

function loadBasket() {
  return AppStorage.get('fl:basket');
}

function saveBasket(items) {
  const success = AppStorage.set('fl:basket', items);
  if (!success) {
    // AppStorage already reported to AppErrorBus with STORAGE_QUOTA_EXCEEDED.
    // Caller can optionally show inline UI — the toast from ErrorToast
    // will already be visible (high severity = 8s toast).
  }
}
```

**Key points:**
- `loadBasket` is reduced to one line. Parse errors, missing keys, and corrupt data are all handled by AppStorage internally.
- `saveBasket` now returns a boolean. The caller can optionally add inline UI, but the ErrorToast system (from AppErrorBus) already shows a user-visible toast for `high` severity errors.
- The manual `AppErrorBus.report()` calls in the catch blocks are removed — AppStorage reports with standardised codes (`STORAGE_QUOTA_EXCEEDED`, `STORAGE_PARSE_FAIL`).
- Total: -20 lines of code. Zero loss of error reporting coverage.

---

**END OF SPEC**

**Next step:** CEO approval required. Upon approval, FE Lead implements Phase 1. QA Lead reviews Phase 1 tests before Phase 2 begins.

**Prerequisites confirmed:**
- AppErrorBus: BUILT (Phases 1-3 complete, 2026-04-09)
- ErrorToast: BUILT and wired into AppLayout.jsx
- Both are in `src/infrastructure/` — AppStorage will sit alongside them
