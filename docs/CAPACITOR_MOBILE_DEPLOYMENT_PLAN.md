# Capacitor Mobile Deployment Plan — FamiliLook Platform

## Context

FamiliLook is a 3-app React/Vite platform (desktop2, desktop4, desktop6) currently deployed as web SPAs on Vercel. The goal is to wrap all three apps with Capacitor to ship native iOS (App Store) and Android (Google Play) apps — keeping the existing web deployment intact. This is the fastest path to mobile store presence, reusing ~95% of existing code.

After Capacitor is validated and shipped, the next phase will be React Native (option 2) once marketing strategy is aligned.

> **Update (2026-03-27 — Option C decision):** FamiliPoker will be merged into desktop2 as a `/poker` route, reducing Capacitor from 3 apps to 2: desktop2 (FamiliLook + FamiliUno + FamiliPoker) and desktop6 (FamiliMatch). This affects Phase 3 and store listing count below.

**Decisions confirmed:**
- Both Apple Developer + Google Play accounts are set up
- Backend-only ML detection on mobile (no TF.js/ONNX in native builds)
- ~~3 separate store listings (not a unified app)~~ → **2 store listings** after Poker merge into desktop2
- Bundle IDs: `io.famililook.app`, ~~`io.famililook.poker`~~, `io.famililook.match`

---

## Agent Crew (6 Specialized Workstreams)

| Agent | Role | Scope |
|-------|------|-------|
| **PLATFORM-CORE** | Foundation | Capacitor init, `src/platform/` abstraction layer, Vite config, npm scripts |
| **IOS-SPECIALIST** | Apple | Xcode project, Info.plist, icons, splash, signing, TestFlight, App Store Connect |
| **ANDROID-SPECIALIST** | Google | Android Studio project, manifest, adaptive icons, keystore, Play Console |
| **TFJS-MIGRATION** | ML Strategy | Remove client-side TF.js on mobile, route detection to backend API, exclude 151MB models |
| **STORE-ASSETS** | Creative/Legal | App icons, screenshots, descriptions, privacy declarations, age ratings |
| **QA-VERIFICATION** | Testing | Device matrix testing, regression, performance benchmarks |

---

## Phase 1: desktop6 (FamiliMatch) — Pilot

**Why first:** No TensorFlow.js, smallest build (~456KB), simplest architecture (1 context provider), purely API-driven. Fastest path to a working native build.

### Step 1.1: Capacitor Scaffolding

**Files created/modified:**
- `famililook-desktop6/capacitor.config.ts` (new)
- `famililook-desktop6/package.json` (add deps)

```bash
cd famililook-desktop6
npm install @capacitor/core @capacitor/cli
npx cap init "FamiliMatch" "io.famililook.match" --web-dir dist
npm install @capacitor/camera @capacitor/browser @capacitor/share \
  @capacitor/haptics @capacitor/preferences @capacitor/status-bar \
  @capacitor/splash-screen @capacitor/app @capacitor/keyboard @capacitor/network
npm install @capacitor/ios @capacitor/android
npx cap add ios
npx cap add android
```

`capacitor.config.ts`:
```ts
const config: CapacitorConfig = {
  appId: 'io.famililook.match',
  appName: 'FamiliMatch',
  webDir: 'dist',
  server: { androidScheme: 'https' },
  plugins: {
    SplashScreen: { launchAutoHide: true, backgroundColor: '#0a0a0a' },
    StatusBar: { style: 'Dark', backgroundColor: '#0a0a0a' },
  },
};
```

### Step 1.2: Vite Config for Capacitor

**File:** `famililook-desktop6/vite.config.mjs`

Add conditional `base: './'` for Capacitor builds so asset paths are relative (not absolute `/`):
```js
const isCapacitor = process.env.CAPACITOR_BUILD === 'true';
// In build config:
base: isCapacitor ? './' : '/',
```

### Step 1.3: Platform Abstraction Layer

**New directory:** `famililook-desktop6/src/platform/`

| File | Purpose |
|------|---------|
| `index.js` | `isNative()`, `isIOS()`, `isAndroid()`, `isWeb()` via `Capacitor.isNativePlatform()` |
| `camera.js` | `pickPhoto()` → Capacitor Camera on native, null on web (falls through to HTML input) |
| `browser.js` | `openExternal(url)` → Capacitor Browser on native, `window.open` on web |
| `share.js` | `shareContent({title, text, url})` → Capacitor Share on native, Web Share API / clipboard on web |
| `statusBar.js` | Configure status bar color/style on native, no-op on web |

### Step 1.4: Adapt Photo Upload

**File:** `famililook-desktop6/src/hooks/usePhotoCapture.js`

Wrap `openFilePicker` to check `isNative()` — on native call `pickPhoto()` from platform layer, on web keep existing `<input type="file">` behavior unchanged.

### Step 1.5: Fix index.html

**File:** `famililook-desktop6/index.html`

Add `viewport-fit=cover` to viewport meta tag (currently missing on desktop6).

### Step 1.6: Add Build Scripts

**File:** `famililook-desktop6/package.json`

```json
"build:cap": "cross-env CAPACITOR_BUILD=true vite build",
"cap:sync": "npm run build:cap && npx cap sync",
"cap:ios": "npm run cap:sync && npx cap open ios",
"cap:android": "npm run cap:sync && npx cap open android"
```

### Step 1.7: CORS Backend Update (Requires Permission)

**File:** `famililook-desktop3` CORS config

Add allowed origins: `capacitor://localhost` (iOS), `https://localhost` (Android with `androidScheme: 'https'`).

### Step 1.8: iOS + Android Config

**iOS (`ios/App/App/Info.plist`):**
- `NSCameraUsageDescription`: "FamiliMatch uses the camera to capture photos for face comparison"
- `NSPhotoLibraryUsageDescription`: "FamiliMatch accesses your photo library to select photos for comparison"

**Android (`android/app/src/main/AndroidManifest.xml`):**
- `android.permission.CAMERA`
- `android.permission.READ_MEDIA_IMAGES` (API 33+)
- `android.permission.INTERNET`

### Step 1.9: Test on Simulators, Submit to TestFlight + Internal Testing

---

## Phase 2: desktop2 (FamiliLook + FamiliUno) — Core Product

### Step 2.1: Capacitor Scaffolding

Same pattern as Phase 1 with `appId: 'io.famililook.app'`, `appName: 'FamiliLook'`.

### Step 2.2: TF.js/ONNX Mobile Strategy (CRITICAL)

**Problem:** 151MB of ML models in `public/models/`. WebGL/WASM unreliable in iOS WebView.

**Solution — Backend-only detection on mobile:**

a) **Exclude models from Capacitor build:**
- `famililook-desktop2/vite.config.mjs` — when `CAPACITOR_BUILD=true`, set `build.copyPublicDir: false` and selectively copy only non-model public assets (robots.txt, og images, config JSONs)

b) **Modify `famililook-desktop2/src/utils/detectFaces.js`:**
- Add `isNative()` check at top of `detectFaces()`
- On native → call `detectFacesViaBackend(img)` which POSTs to `/detect/faces`
- On web → existing client-side TF.js path unchanged

c) **Modify `famililook-desktop2/src/arcface.js`:**
- On native → call backend `/embed` endpoint
- On web → existing ONNX path unchanged

d) **Handle `<script src="/models/ort/ort.min.js">` in `index.html`:**
- Switch to dynamic import that catches errors, or remove the script tag and load ORT via JS only when `!isNative()`

### Step 2.3: Photo Upload Adaptation

**20+ file inputs** across 6+ components. Strategy: create a `<NativeFileInput>` wrapper component in `src/components/upload/` that:
- On web: renders standard `<input type="file">` (zero change)
- On native: renders a button calling `@capacitor/camera`
- Returns File/Blob compatible with existing handlers

Then progressively replace `<input>` elements in:
- `PhotoSlot.jsx`, `DropLane.jsx`, `ChildDrop.jsx`, `PremiumUploadLayout.jsx`, `UploadSection.jsx`, `GroupSnapshotSection.jsx`

### Step 2.4: Stripe Checkout on Native

**File:** `famililook-desktop2/src/components/keepsakes/OrderModal.jsx`

Replace `window.location.href = checkoutUrl` with `openExternal(checkoutUrl)` from platform layer. Configure deep links so `famililook.com/order-success` returns to the app:
- iOS: `apple-app-site-association` file on famililook.com
- Android: `assetlinks.json` on famililook.com

### Step 2.5: Cross-App Navigation

**File:** `famililook-desktop2/src/pages/BrandHubPage.jsx`

FamiliPoker/FamiliMatch links use `window.location.href`. On native, open via `openExternal()` (system browser or deep link to sister app if installed).

### Step 2.6: Sharing, Haptics, Analytics Adaptation

- `ShareModal.jsx` → use `shareContent()` from platform layer
- `haptics.js` → use Capacitor Haptics on native
- `analytics.js` → normalize `window.location.pathname` for Capacitor origin. **DO NOT touch the dev bypass.**

### Step 2.7: OffscreenCanvas Fallback

**File:** `famililook-desktop2/src/utils/compressPhoto.js`

Add feature detection: if `OffscreenCanvas` unavailable (some iOS WebViews), fall back to regular `document.createElement('canvas')`.

---

## Phase 3: desktop4 (FamiliPoker) — LIKELY OBSOLETE

> **Note (2026-03-27):** Per the Option C decision, FamiliPoker is being merged into desktop2 as a `/poker` route. If that merge completes before Capacitor work begins, this phase is unnecessary — Poker will ship as part of the desktop2 Capacitor app (Phase 2). The store compliance notes below still apply to the combined app.

Same pattern as Phase 2 with `appId: 'io.famililook.poker'`, `appName: 'FamiliPoker'`.

- Reuse platform abstraction layer from Phase 2
- Apply same TF.js backend-only strategy
- **Note:** FamiliPoker has "casino" theming → Google Play requires "Simulated Gambling" category, no real money. Apple may require 17+ age rating. Store descriptions must clearly state "no real money wagering."

---

## App Store Submission Checklist

### Apple App Store (per app)
- [ ] Xcode 15+ project builds clean
- [ ] Deployment target: iOS 16.0+
- [ ] iPhone-only initially (iPad optional later)
- [ ] Camera + Photo Library permission strings in Info.plist
- [ ] Privacy manifest (`PrivacyInfo.xcprivacy`)
- [ ] App icons: 1024x1024 + all size variants
- [ ] Screenshots: iPhone 6.7", 6.5", 5.5" (min 3 each)
- [ ] Age rating: 4+ (Match/Look), 17+ (Poker)
- [ ] Privacy policy: `https://famililook.com/privacy`
- [ ] Binary size < 200MB (guaranteed — models excluded)
- [ ] TestFlight internal testing pass

### Google Play (per app)
- [ ] Target API 34+, min SDK 24
- [ ] AAB format (not APK)
- [ ] Adaptive icons: 512x512 foreground + background
- [ ] Feature graphic: 1024x500
- [ ] Screenshots: min 2 phone
- [ ] IARC content rating
- [ ] Data safety section filled
- [ ] Privacy policy URL
- [ ] Simulated Gambling declaration (Poker only)
- [ ] Internal testing track pass

---

## Verification Strategy

### Existing tests must still pass (web not broken)
```bash
# Per app:
npm run test:run    # Unit tests
npm run build       # Web build
npx playwright test # E2E (web)
```

### Native-specific manual testing
| Test | iOS | Android |
|------|-----|---------|
| App launches without crash | Simulator + device | Emulator + device |
| Photo from camera | Real device only | Real device only |
| Photo from gallery | Simulator | Emulator |
| API calls work (CORS) | Both | Both |
| Safe area insets | iPhone 15 Pro (Dynamic Island) | N/A |
| Status bar styling | Both | Both |
| External links open | Both | Both |
| Share sheet works | Both | Both |
| Android back button | N/A | Emulator |
| App background/resume | Both | Both |
| localStorage persists | Both | Both |

### Performance targets
- Cold start < 3s (iOS) / < 4s (Android)
- Photo pick to preview < 1s
- API round-trip < 5s
- App binary < 30MB (models excluded)

---

## Capacitor Dependencies (all 3 apps)

```
@capacitor/core, @capacitor/cli
@capacitor/ios, @capacitor/android
@capacitor/camera, @capacitor/browser, @capacitor/share
@capacitor/haptics, @capacitor/preferences
@capacitor/status-bar, @capacitor/splash-screen
@capacitor/app, @capacitor/keyboard, @capacitor/network
```

---

## Risk Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| TF.js fails in iOS WebView | CRITICAL | Backend-only detection on mobile (confirmed) |
| 151MB models bloat native app | CRITICAL | Exclude `public/models/` from Capacitor builds |
| Stripe checkout breaks in WebView | HIGH | Use `@capacitor/browser` for checkout redirect + deep links for return |
| CORS rejects Capacitor origin | HIGH | Add `capacitor://localhost` + `https://localhost` to backend CORS |
| OffscreenCanvas unavailable | MEDIUM | Feature-detect + fallback to regular Canvas |
| FamiliPoker rejected for gambling | MEDIUM | "Simulated Gambling" category, no real money, clear disclaimers |
| Cross-app nav breaks on native | MEDIUM | Use `openExternal()` for sister app links |

---

## Execution Order

1. **Phase 1 (desktop6)** — Pilot. Creates the platform abstraction pattern, validates Capacitor on simplest app.
2. **Phase 2 (desktop2)** — Core product. Heaviest lift (TF.js migration, 20+ upload points, Stripe).
3. **Phase 3 (desktop4)** — Likely obsolete if Poker merges into desktop2 (Option C). Store compliance notes still apply.

Each phase: scaffold → platform layer → adapt native-sensitive code → test → submit to store.

---

## Prerequisites

- **Backend session token:** `POST /session/create` → `GET /session/{token}` should be implemented before Capacitor work begins, as `localStorage` is not available in native mobile apps. See `navigation_strategy.md`.
