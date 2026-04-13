# PRD: Smart Photo Selection — Intelligent Upload Assistant

> **Author**: CPO Agent
> **Date**: 2026-04-01
> **Product**: FamiliLook (desktop2 FE + desktop3 BE)
> **Priority**: P1
> **Status**: SPEC_READY

---

## 1. Problem Statement

Users struggle to find good photos from their camera roll that meet the requirements for kinship analysis. The current flow asks them to upload Parent A, Parent B, and Child photos — but gives no guidance on *which* photo will produce the best results until *after* detection runs. Users pick distant group shots for parent slots, blurry selfies, or photos with sunglasses. Bad input produces bad results, the user blames the product, and churn follows.

**Evidence:**
- Upload conversion is low (9 visitors, 14 CTAs, 0 uploads — tracked in Growth Monitor)
- Backend quality thresholds exist (yaw <25°, pitch <20°, det_score >0.85, face >80px) but are only surfaced *after* the user has already picked a photo
- FacePicker handles multi-face crops reactively — but users still have to find the right photo first
- No client-side pre-screening exists — all quality checks require a round-trip to `/detect`

## 2. Goal

Reduce photo selection friction by using on-device intelligence to help users find the best photos *before* they upload. Each slot selection progressively narrows candidates for the next slot using face embeddings — the user identifies who is who by picking, not by the system guessing.

**Success target:** 3x increase in upload-to-analysis completion rate within 30 days of launch.

## 3. Solution Overview — Progressive Slot-Aware Selection

### Core Insight
The system doesn't need to know who anyone is in advance. Each time the user picks a photo for a slot, the system learns that person's face embedding and uses it to filter candidates for subsequent slots.

### Flow

```
1. User taps "Upload Mum" (Parent A slot)
2. System requests photo library access (with explicit consent)
3. Client-side face detector scans recent N photos (on-device, nothing uploaded)
4. System ranks photos by: face detected, single face, face size, sharpness, head pose
5. Presents top 8 candidates as "Best photos for this slot"
6. User picks one → system captures Mum's face embedding (client-side)
7. User taps "Upload Dad" (Parent B slot)
8. System re-ranks candidates, EXCLUDING photos where the primary face matches Mum's embedding
9. Presents top 8 candidates (now biased toward a different person)
10. User picks one → system captures Dad's embedding
11. User taps "Upload Child"
12. System re-ranks candidates, EXCLUDING both Mum and Dad lookalikes
13. Remaining candidates are likely children, siblings, others
14. User picks → analysis proceeds with high-quality, correctly-slotted photos
```

### Why This Works
- **No pre-labelling needed** — each selection teaches the system about the next slot
- **No privacy risk** — embeddings computed on-device, discarded after the session
- **Handles the "child looks like parent" edge case** — exclusion threshold is tuned looser than kinship detection threshold (we exclude near-identical faces, not family resemblance)
- **All on-device** — no photos leave the phone until the user explicitly confirms

---

## 4. Phased Delivery

### Phase 1: Pre-Upload Quality Gate (Sprint-ready)
**Effort: S (1-2 days) | Impact: High**

Enhance the existing `faceQualityAdvice.js` flow to give *specific, actionable* feedback before the user commits to a photo.

| Signal | Current State | Target State |
|--------|--------------|--------------|
| No face detected | Red badge, generic message | "No face found — try a closer photo where we can see the face clearly" |
| Face too small | Not surfaced until backend | "Face is too small — try a photo from shoulders up" + visual overlay showing ideal framing |
| Bad head pose | Not surfaced until backend | "Head is turned too far — try a front-facing photo" |
| Multiple faces | Scissors icon, FacePicker | Keep FacePicker + add: "Multiple faces detected — tap the face you want to use" |
| Sunglasses/occlusion | Not detected client-side | "Eyes may be hidden — try a photo without sunglasses for best results" |

**Implementation:**
- Extend `faceQualityAdvice.js` to surface all quality signals from the `/detect` response that currently go unused
- Add slot-aware tips: parent slots show "one clear adult face", child slots show "one clear face", group slots show "everyone visible"
- Add visual framing guide: silhouette overlay showing ideal crop zone inside PhotoSlot

**Files to modify:**
| File | Changes |
|------|---------|
| `src/utils/faceQualityAdvice.js` | Add pose/size/occlusion advice from backend response |
| `src/components/upload/PhotoSlot.jsx` | Slot-aware tip text, framing guide overlay |
| `src/components/upload/DropLane.jsx` | Slot-aware validation messages |
| `tests/faceQualityAdvice.test.js` | New tests for expanded advice |

### Phase 2: Smart Crop for Wrong-Slot Photos (Sprint-ready)
**Effort: S (1 day) | Impact: Medium**

When a user uploads a group photo to a single-person slot, instead of just showing the scissors icon, proactively present the FacePicker with a clear prompt: "We found 3 faces — tap the one you want for this slot."

**Implementation:**
- Auto-open FacePicker when `faceCount > 1` on a parent/child slot (instead of waiting for user to notice the scissors icon)
- Add face-size ranking to FacePicker: largest/clearest face shown first with "Recommended" badge
- After crop, re-run quality check on the cropped region

**Files to modify:**
| File | Changes |
|------|---------|
| `src/components/upload/FacePicker.jsx` | Auto-open logic, "Recommended" badge on best face |
| `src/components/upload/PhotoSlot.jsx` | Trigger FacePicker auto-open on multi-face detect |
| `src/layout/UploadSection.jsx` | Wire auto-open into detection callback |

### Phase 3: Client-Side Photo Ranker with Progressive Exclusion (Key differentiator)
**Effort: L (5-7 days) | Impact: Transformative**

This is the headline feature — scanning the user's camera roll on-device to suggest the best photos per slot, with progressive embedding-based exclusion.

#### 3a. On-Device Face Detection
- Use **MediaPipe Face Detection** (already a project dependency for backend fallback) compiled to WASM/WebGL for browser
- Alternatively, leverage existing `@vladmandic/face-api` (already in desktop2 dependencies) with TinyFaceDetector
- Scan last 100-200 photos from camera roll (user grants access via File System Access API or `<input webkitdirectory>` on mobile)
- Per-photo: detect face count, face bounding box, detection confidence
- Filter: single face, confidence > 0.7, face width > 15% of image width

#### 3b. Quality Ranking (On-Device)
For each candidate photo, compute a composite quality score:

```javascript
quality_score = (
    0.35 * face_size_ratio +          // face area / image area (bigger = better)
    0.25 * detection_confidence +      // det_score from face-api
    0.20 * frontal_score +             // 1.0 - normalized yaw/pitch deviation
    0.10 * sharpness_estimate +        // Laplacian variance on face region
    0.10 * lighting_uniformity         // luminance std dev on face region (lower = better)
)
```

#### 3c. Progressive Embedding Exclusion
After the user picks a photo for Slot N:
1. Extract 128-dim embedding using `face-api` FaceRecognitionNet (already available client-side)
2. Store embedding transiently in session state (never persisted, never uploaded)
3. For Slot N+1, compute cosine similarity between each candidate and all previously-selected embeddings
4. **Exclude** candidates where `cosine_similarity > 0.65` (same person threshold)
5. **Soft-demote** candidates where `cosine_similarity > 0.45` (possibly same person — show but rank lower)

Note: The exclusion threshold (0.65) must be *higher* than the kinship similarity range (~0.2-0.5) so children who resemble parents are NOT excluded.

#### 3d. Consent UX
- **Trigger:** When user taps a photo slot, before opening the picker, show a one-time consent sheet:
  > "**Find your best photos**
  > FamiliLook can scan your recent photos to suggest the clearest face shots for this analysis. All scanning happens on your device — no photos are uploaded until you choose one.
  > [Allow] [No thanks, I'll pick manually]"
- Consent stored in `localStorage` as `fl:photoScanConsent` with timestamp
- Revocable from Settings page at any time
- If declined, fall back to standard file picker (no degradation)

#### 3e. UI: Suggested Photos Grid

```
┌──────────────────────────────────────────┐
│  Best photos for "Mum"                   │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ ★    │ │      │ │      │ │      │   │
│  │ img1 │ │ img2 │ │ img3 │ │ img4 │   │
│  │ 94%  │ │ 87%  │ │ 82%  │ │ 79%  │   │
│  └──────┘ └──────┘ └──────┘ └──────┘   │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │      │ │      │ │      │ │      │   │
│  │ img5 │ │ img6 │ │ img7 │ │ img8 │   │
│  │ 75%  │ │ 71%  │ │ 68%  │ │ 63%  │   │
│  └──────┘ └──────┘ └──────┘ └──────┘   │
│                                          │
│  [Browse all photos instead]             │
└──────────────────────────────────────────┘
```

- 2x4 grid, sorted by quality score descending
- ★ badge on top-ranked photo
- Score shown as percentage (normalised quality_score * 100)
- "Browse all photos instead" falls back to native picker
- After selecting for Parent A, the grid for Parent B auto-refreshes with exclusions applied
- Smooth transition: selected photo slides into the slot with a confirmation animation

**Files to create/modify:**
| File | Changes |
|------|---------|
| `src/components/upload/SmartPhotoScanner.jsx` | **NEW** — Camera roll scanner + ranker component |
| `src/components/upload/SuggestedPhotosGrid.jsx` | **NEW** — 2x4 grid UI with quality scores |
| `src/components/upload/PhotoScanConsent.jsx` | **NEW** — One-time consent sheet |
| `src/hooks/usePhotoScanner.js` | **NEW** — Hook: scan, rank, exclude, cache results |
| `src/utils/clientFaceQuality.js` | **NEW** — On-device quality scoring (face size, sharpness, pose) |
| `src/components/upload/PhotoSlot.jsx` | Integrate SmartPhotoScanner as alternative to native picker |
| `src/layout/UploadSection.jsx` | Pass slot context + prior embeddings to scanner |
| `src/state/FamililookContext.jsx` | Add transient embedding state (session-only) |
| `tests/usePhotoScanner.test.js` | **NEW** — Unit tests for ranking + exclusion logic |
| `tests/clientFaceQuality.test.js` | **NEW** — Unit tests for quality scoring |

### Phase 4: Photo Pair Quality Scorer (Post-MVP)
**Effort: M (2-3 days) | Impact: Medium**

After both parents are uploaded, run a quick cross-check:
- Compute embedding similarity between Parent A and Parent B
- If similarity > 0.8: warn "These photos may be the same person — double-check your selection"
- If both photos have same quality issue (e.g., both wearing sunglasses): warn "Both parent photos have hidden eyes — results will be less accurate for eye features"
- Show a "pair quality" indicator: "Great pair" / "Could be better" / "Consider re-selecting"

### Phase 5: Camera Coaching Mode (Future)
**Effort: L (5+ days) | Impact: High (marketing moment)**

Real-time camera overlay that guides users to take the ideal photo:
- Live face detection with bounding box overlay
- Green zone indicator when face is properly positioned, sized, and lit
- "Hold still..." → capture when quality score exceeds threshold
- Great for users who don't have suitable existing photos

---

## 5. Technical Constraints & Decisions

### Client-Side ML Stack
- **Already available in desktop2:** `@vladmandic/face-api` (v1.7.15), TensorFlow.js (v4.22.0)
- **No new dependencies needed for Phase 1-3** — face-api provides detection, landmarks, and 128-dim recognition embeddings
- **Model loading:** ~2-5MB for TinyFaceDetector + FaceRecognitionNet. Load on-demand when user grants photo scan consent (not on page load)
- **Performance target:** Scan 100 photos in <10 seconds on mid-range mobile (using WebGL backend, batched inference)

### Privacy Architecture
- ALL photo scanning happens on-device via client-side ML
- Face embeddings are **transient** — stored in React state only, never in localStorage, never uploaded
- Photos are NOT uploaded to any server until the user explicitly selects one for a slot
- Consent is explicit, granular, and revocable
- No face database is built — embeddings discarded when the user leaves the upload flow
- Compliant with GDPR Article 9 (biometric data) because:
  - Processing happens entirely on user's device
  - User gives explicit consent before scanning
  - No data transmitted to any server
  - User can revoke consent and all client-side data is discarded

### Camera Roll Access
- **Mobile (iOS/Android):** `<input type="file" accept="image/*" multiple webkitdirectory>` or File System Access API where available
- **Desktop:** Standard file picker with folder selection
- **Fallback:** If camera roll access is denied or unavailable, the standard single-file picker works as before (zero degradation)

### Embedding Threshold Tuning
- **Same-person exclusion:** cosine_similarity > 0.65 (face-api 128-dim space)
- **Soft demotion:** cosine_similarity > 0.45
- **Family resemblance range:** typically 0.2-0.5 (must NOT trigger exclusion)
- These thresholds need A/B testing in production — expose as feature flags:
  - `VITE_PHOTO_SCAN_EXCLUDE_THRESHOLD` (default: 0.65)
  - `VITE_PHOTO_SCAN_DEMOTE_THRESHOLD` (default: 0.45)

---

## 6. User Stories

| # | As a... | I want to... | So that... |
|---|---------|-------------|-----------|
| 1 | New user | See which of my photos will work best before I upload | I don't waste time on photos that produce bad results |
| 2 | Mobile user | Get specific feedback on why my photo isn't ideal | I know exactly what to fix (closer, less turned, remove sunglasses) |
| 3 | Parent uploading family photos | Have the system filter out photos of the wrong person for each slot | I don't accidentally upload Mum's photo in the Dad slot |
| 4 | User with many photos | See a curated shortlist instead of scrolling through thousands | The process feels fast and guided, not overwhelming |
| 5 | Privacy-conscious user | Know that my photos are scanned on my phone, not uploaded | I trust the app with my family's biometric data |
| 6 | User who declines scanning | Still upload photos manually with no loss of functionality | I'm never forced into a feature I don't want |

---

## 7. Acceptance Criteria

### Phase 1 (Quality Gate)
- [ ] Quality messages are specific and actionable (not generic "low quality")
- [ ] Slot-aware tips appear inside each upload slot before photo is selected
- [ ] Backend quality signals (pose, face size, occlusion) are surfaced in advice text
- [ ] All existing quality badge behaviour preserved (no regression)

### Phase 2 (Smart Crop)
- [ ] FacePicker auto-opens when multi-face detected on single-person slot
- [ ] Largest/clearest face has "Recommended" badge
- [ ] Post-crop quality re-check runs automatically
- [ ] User can still dismiss FacePicker and use full image

### Phase 3 (Photo Ranker)
- [ ] Consent sheet shown before any camera roll scanning
- [ ] Scanning runs entirely on-device (verified: no network calls during scan)
- [ ] Top 8 photos shown in grid, ranked by composite quality score
- [ ] Progressive exclusion works: Parent B grid excludes Parent A's face
- [ ] Child grid excludes both parent faces
- [ ] "Browse all photos instead" falls back to native picker
- [ ] Embeddings discarded when user leaves upload flow
- [ ] Consent revocable from Settings
- [ ] Feature degrades gracefully: no consent = standard picker, no face-api = standard picker

---

## 8. Agent Assignments

| Step | Agent | Task | Depends On |
|------|-------|------|-----------|
| 1 | fe_lead | Expand `faceQualityAdvice.js` with actionable, slot-aware messages | — |
| 2 | fe_lead | Add framing guide overlay to PhotoSlot | — |
| 3 | qa_lead | Write tests for expanded quality advice | Steps 1-2 |
| 4 | fe_lead | Auto-open FacePicker on multi-face + "Recommended" badge | — |
| 5 | qa_lead | Write tests for auto-open FacePicker behaviour | Step 4 |
| 6 | fe_lead | Build `usePhotoScanner` hook (scan, rank, exclude) | — |
| 7 | fe_lead | Build `clientFaceQuality.js` (on-device quality scoring) | — |
| 8 | fe_lead | Build `SmartPhotoScanner.jsx` + `SuggestedPhotosGrid.jsx` | Steps 6-7 |
| 9 | fe_lead | Build `PhotoScanConsent.jsx` (consent UX) | — |
| 10 | fe_lead | Integrate scanner into PhotoSlot + UploadSection | Steps 8-9 |
| 11 | visual_director | Design consent sheet, suggested grid, quality overlays | — |
| 12 | qa_lead | Write tests for scanner, ranker, exclusion, consent | Steps 6-10 |
| 13 | copywriter | Write consent copy, quality tip copy, slot guidance copy | — |
| 14 | coo | Privacy review: verify on-device only, GDPR compliance | Steps 8-9 |

---

## 9. Dependencies & Blockers

| Dependency | Status | Notes |
|-----------|--------|-------|
| `@vladmandic/face-api` in desktop2 | AVAILABLE | v1.7.15 already in package.json |
| TensorFlow.js WebGL backend | AVAILABLE | v4.22.0 already in package.json |
| File System Access API | PARTIAL | Available in Chrome/Edge, fallback needed for Safari/Firefox |
| Backend `/detect` endpoint | AVAILABLE | Used by Phase 1-2, not needed for Phase 3 on-device scanning |

**No blockers.** All ML dependencies are already in the project.

---

## 10. Success Metrics

| Metric | Baseline | Target | Measured By |
|--------|----------|--------|-------------|
| Upload-to-analysis completion | ~0% (0 uploads) | 15%+ of visitors complete analysis | `analysis_complete` events / `page_view` events |
| Photo quality warnings per session | Unknown | <1 warning per session (down from est. 2-3) | `photo_quality_failed` events |
| Time from first slot tap to analysis start | Unknown | <90 seconds | Timestamp analytics |
| Smart scan opt-in rate | N/A | >60% of users who see consent | `photo_scan_consent_granted` events |
| Photos re-selected after quality warning | Unknown | <20% (most picks are good first time) | `photo_replaced` events |

---

## 11. Effort Estimate

| Phase | Size | Days | ICE Score |
|-------|------|------|-----------|
| Phase 1: Quality Gate | S | 1-2 | I(8) × C(9) × E(9) = 648 |
| Phase 2: Smart Crop | S | 1 | I(6) × C(9) × E(9) = 486 |
| Phase 3: Photo Ranker | L | 5-7 | I(10) × C(7) × E(5) = 350 |
| Phase 4: Pair Scorer | M | 2-3 | I(5) × C(8) × E(7) = 280 |
| Phase 5: Camera Coach | L | 5+ | I(7) × C(5) × E(4) = 140 |

**Recommended sprint order:** Phase 1 → Phase 2 → Phase 3 (ship incrementally, each phase is independently valuable)

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Camera roll scanning too slow on low-end devices | Medium | High | Limit scan to 50 photos on slow devices, show progress bar, scan in Web Worker |
| face-api models too large for mobile | Low | Medium | TinyFaceDetector is 190KB, FaceRecognitionNet is 6.2MB — lazy-load only on consent |
| Exclusion threshold too aggressive (excludes children who look like parents) | Medium | High | Start conservative (0.65), A/B test, expose as feature flag |
| File System Access API not available on Safari | High | Medium | Fallback to `<input multiple>` — works everywhere, just less elegant |
| Users decline photo scanning consent | Medium | Low | Zero degradation — standard picker works as before |

---

## 13. Regression Protection Plan (NON-NEGOTIABLE)

### 13.1 Current State — Test Gaps in Upload Flow

An audit of the upload flow reveals significant test coverage gaps in the very components this feature modifies. These gaps **must be closed BEFORE any feature code ships**, not after.

| Component | Current Test Coverage | Risk if Modified Without Tests |
|-----------|----------------------|-------------------------------|
| `faceQualityAdvice.js` | 32 unit tests | LOW — well covered |
| `faceDetectionPreview` | 24 unit tests | LOW — box formats covered |
| `upload-quality-gate.spec.js` | 5 E2E scenarios | LOW — critical path covered |
| `smoke-upload-analyze.spec.js` | 1 E2E flow | LOW — happy path covered |
| **`PhotoSlot.jsx`** | **ZERO tests** | **HIGH — Phase 1+2+3 modify this** |
| **`FacePicker.jsx`** | **ZERO tests** | **HIGH — Phase 2 modifies this** |
| **`UploadSection.jsx`** | **1 smoke test only** | **HIGH — Phase 3 modifies this** |
| **`compressPhoto.js`** | **ZERO tests** | **MEDIUM — compression could break embeddings** |
| **`imageProcessing.js`** | **ZERO tests** | **MEDIUM — face detection API integration** |
| **`DropLane.jsx`** | **ZERO tests** | **MEDIUM — drag-drop file handling** |
| **`IntentSelector.jsx`** | **ZERO tests** | **LOW — not directly modified, but coupled** |
| **`ConsentContext.jsx`** | **ZERO tests** | **HIGH — Phase 3 adds new consent type** |

### 13.2 Full Blast Radius Map — Four Zones of Impact

This section traces **every downstream consumer** of every file we modify. A change to file X doesn't just risk X — it risks everything that imports X. This is the full dependency tree, audited from the codebase.

#### ZONE 1: Component Dependency Chain (What imports what we change)

```
                         ┌─────────────────────────────────────────┐
                         │         FILES WE MODIFY (DIRECT)         │
                         └────────────────┬────────────────────────┘
                                          │
    ┌─────────────────────────────────────┼──────────────────────────────────┐
    │                                     │                                  │
    ▼                                     ▼                                  ▼
faceQualityAdvice.js              PhotoSlot.jsx                    FamililookContext.jsx
    │                              FacePicker.jsx                         │
    │                              UploadSection.jsx                      │
    │                                     │                               │
    ▼ CONSUMERS                           ▼ CONSUMERS                     ▼ CONSUMERS (16 FILES)
┌──────────────────┐          ┌────────────────────┐          ┌────────────────────────────┐
│ GroupSnapshot     │          │ AppLayout.jsx      │          │ AppLayout.jsx              │
│   Section.jsx    │          │   (main entry)     │          │ MobileResultsSection.jsx   │
│ PhotoSlot.jsx    │          │ FamiliUnoPage.jsx   │          │ GroupSnapshotSection.jsx    │
│ CardGame.jsx ⚡  │          │   (Uno game entry) │          │ FamiliUnoPage.jsx           │
│ tests (32)       │          │ tests (1 smoke)    │          │ UploadSection.jsx           │
└──────────────────┘          └────────────────────┘          │ AnalysisSection.jsx         │
                                                              │ useKinshipAnalysis.jsx      │
                                                              │ useKeepsakeData.js          │
                                                              │ useFamilyKeepsakeData.js    │
                                                              │ PremiumUploadLayout.jsx     │
                                                              │ StateInspector.jsx          │
                                                              │ + 5 test files              │
                                                              └────────────────────────────┘
```

**Key finding:** `faceQualityAdvice.js` is consumed by `CardGame.jsx` — a completely separate flow from upload. If we change the return shape of `assessFaceQuality()` or `assessAllFaces()`, the card game breaks silently.

**Key finding:** `FamililookContext.jsx` has **16 consumers**. Any state shape change (adding new fields, changing reset behaviour) cascades across the ENTIRE app — results display, keepsakes, analysis, games, everything.

**Key finding:** `PhotoSlot.jsx` and `FacePicker.jsx` are currently **not imported by any file** (they exist as standalone components). But `UploadSection.jsx` uses them internally. The real entry points are `AppLayout.jsx` and `FamiliUnoPage.jsx`.

#### Per-File Blast Radius Detail

| File We Modify | Direct Consumers | Indirect Consumers | Blast if Broken |
|---------------|-----------------|-------------------|-----------------|
| `faceQualityAdvice.js` | GroupSnapshotSection, PhotoSlot, **CardGame.jsx** | AppLayout → entire app | **CardGame.jsx** stops rendering quality indicators. GroupSnapshot shows wrong advice. |
| `PhotoSlot.jsx` | (internal to UploadSection) | UploadSection → AppLayout, FamiliUnoPage | Upload slots render incorrectly or don't respond to input. |
| `FacePicker.jsx` | (internal to UploadSection) | UploadSection → AppLayout, FamiliUnoPage | Multi-face selection breaks. Users can't crop faces from group photos. |
| `UploadSection.jsx` | AppLayout, FamiliUnoPage, 1 test | Entire app (it's the upload entry point) | **ALL upload flows dead.** No analysis possible. |
| `FamililookContext.jsx` | **16 files** | Every page, every hook, every game | **Entire app breaks.** State undefined errors cascade everywhere. |
| `compressPhoto.js` | UploadSection | AppLayout | Photos sent to backend uncompressed (>10MB), API rejects, silent failure. |
| `imageProcessing.js` | DropLane, ChildrenPanel | IndividualUploadPanel, PetsPanel | Face detection for individual/pet uploads breaks. |

#### ZONE 2: State & Storage Collisions

| Storage Layer | Existing Keys | New Keys (Smart Photo) | Collision Risk |
|--------------|--------------|----------------------|----------------|
| **FamililookContext state** | `parents`, `children`, `pets`, `groupPhoto`, `analysisResults`, `featureBreakdown`, `groupAnalysis`, `isAnalyzing`, `currentPlan`, `planEmail`, `userIntent`, `confidenceThreshold`, `voteMargin` | `photoScannerState` (new), `photoEmbeddings` (new) | **MEDIUM** — new fields are additive but `resetAll()` MUST clear them. If not, stale embeddings persist across analyses. |
| **localStorage** | 36 `fl:` keys including `fl:consent` `{ analytics, biometric, acknowledged }` | `fl:photoScanConsent` (new) | **NONE** — separate key, no collision. But MUST be documented in cookie-policy.html. |
| **sessionStorage** | `fl:analysis-cache` `{ analysisResults, featureBreakdown, groupAnalysis }` | No changes needed | **NONE** — scanner state is transient (React state only). |
| **Consent ordering** | COPPA (z:2000) → Analytics banner (z:700) → Biometric (inline gate) | Photo scan consent (z:1900) | **LOW** — fires only when user taps slot with scanner enabled. Does NOT interrupt existing COPPA or biometric gates. But: if user sees 3 consent prompts in sequence (COPPA → biometric → scan), it feels hostile. |

**Critical invariant:** `resetAll()` in FamililookContext currently clears `parents`, `children`, `analysisResults`, etc. Any new state fields MUST be added to `resetAll()` or they leak across sessions. This must be a unit test (SPS-09).

**Critical invariant:** `fl:consent` is the single source of truth for ConsentContext. Photo scan consent MUST NOT be stored inside `fl:consent` — it would change the object shape that 8+ files read.

#### ZONE 3: Performance & Bundle Impact

| Concern | Current State | After Phase 3 | Risk |
|---------|-------------|--------------|------|
| **Main bundle** | 931KB (index-CcL-jiiQ.js) | 931KB (no change — face-api already bundled) | **NONE** |
| **Model files** | 22MB in `/public/models/faceapi/` (loaded on-demand) | Same files, loaded earlier (when consent granted) | **MEDIUM** — model download starts during upload flow, not after. Could cause 8s delay on first use. |
| **Main thread blocking** | face-api runs on main thread (no Web Worker) | Scanning 100-200 photos on main thread | **HIGH** — UI freezes during scan. Must use Web Worker. |
| **Memory** | TF.js tensors for single-photo detection | TF.js tensors for 100-200 photos + 128-dim embeddings × N | **HIGH** — if tensors aren't disposed, memory leak. Each embedding is ~512 bytes, but TF intermediate tensors are much larger. |
| **Code splitting** | No manual chunks for ML deps. face-api + TF.js in main bundle. | Same (already bundled) | **MEDIUM** — should split into separate chunk so non-upload pages don't pay the cost. |
| **Lazy loading** | Routes lazy-loaded via `React.lazy()`. ML libs are eager. | ML models should lazy-load on consent | **Requires change** — add `React.lazy` for scanner components. |

**Critical requirement:** Phase 3 MUST use a **Web Worker** for face detection across multiple photos. Without it, scanning 100 photos on the main thread blocks the UI for 10-30 seconds. This is a P0 implementation requirement, not a nice-to-have.

**Critical requirement:** Every TF.js tensor created during scanning MUST be explicitly disposed via `tf.dispose()` or wrapped in `tf.tidy()`. Leaking tensors during a 200-photo scan will consume hundreds of MB of GPU memory and crash the tab.

#### ZONE 4: Cross-Product and Shared Flow Impact

| Question | Answer | Implication |
|----------|--------|------------|
| Does desktop4 (FamiliPoker) share upload components? | **NO** — independent codebase, copy-paste pattern | No cross-product blast |
| Does desktop6 (FamiliMatch) share upload components? | **NO** — no `/src/components/upload/` directory | No cross-product blast |
| Does desktop3 (backend) need changes? | **NO for Phase 1-3** — all on-device. Backend API unchanged | No backend blast |
| Does FamiliUno (`FamiliUnoPage.jsx`) use UploadSection? | **YES** — imports it directly | Changes to UploadSection affect Uno's upload path too |
| Does CardGame use faceQualityAdvice? | **YES** — imports `assessAllFaces`, `getQualityColor`, `getQualityLabel` | Quality advice changes must preserve existing function signatures |
| Does the keepsake flow depend on FamililookContext state? | **YES** — `useKeepsakeData.js` and `useFamilyKeepsakeData.js` both consume it | Context state shape changes could break keepsake rendering |

#### ZONE 4 Summary: What Else Breaks If We Get This Wrong

```
If faceQualityAdvice.js return shape changes:
  → CardGame.jsx quality indicators break
  → GroupSnapshotSection advice text wrong
  → 32 existing unit tests fail (good — we catch it)

If FamililookContext state shape changes unexpectedly:
  → MobileResultsSection can't read results
  → AnalysisSection shows stale/undefined data
  → useKeepsakeData hook returns bad keepsake content
  → useKinshipAnalysis sends wrong FormData
  → FamiliUnoPage can't access parent/child data
  → resetAll() leaves orphaned state

If UploadSection.jsx has a render error:
  → AppLayout shows blank upload area (the entire homepage is dead)
  → FamiliUnoPage can't start a new game (needs upload first)
  → No analysis possible anywhere in the app

If compressPhoto.js changes behavior:
  → Photos sent to backend uncompressed → 413 Payload Too Large
  → OR compression corrupts image → backend face detection fails
  → Silent failure: user sees "analysis failed" with no explanation

If PhotoSlot.jsx breaks:
  → Upload slots don't accept files
  → Quality badges don't render
  → Camera/gallery toggle doesn't work
  → Labels can't be edited
```

### 13.2a Protection Rules Derived from Blast Radius

Based on the above analysis, these rules are **mandatory** for all phases:

| Rule | Rationale | Enforcement |
|------|-----------|-------------|
| **R1:** `faceQualityAdvice.js` — preserve ALL existing function signatures. New advice MUST be additive (new fields/messages), never change existing return shapes. | CardGame.jsx depends on `assessAllFaces()`, `getQualityColor()`, `getQualityLabel()` | Unit test: existing 32 tests pass without modification |
| **R2:** `FamililookContext.jsx` — new state fields are additive only. NEVER rename or remove existing fields. `resetAll()` MUST clear new fields. | 16 consumers read context state. Any shape change cascades app-wide. | Unit test: `resetAll()` test updated to verify new fields cleared |
| **R3:** Phase 3 scanner MUST run in a **Web Worker**. Main-thread scanning is BLOCKED. | Scanning 100+ photos on main thread freezes UI for 10-30s | Code review gate: PR rejected if `detectAllFaces()` called outside worker |
| **R4:** All TF.js tensors MUST be wrapped in `tf.tidy()` or explicitly `tf.dispose()`d. | Memory leak during multi-photo scan crashes the browser tab | Unit test: mock `tf.memory()` before/after scan, assert tensor count returns to baseline |
| **R5:** Photo scan consent uses key `fl:photoScanConsent` — NEVER modify `fl:consent` object shape. | 8+ files read `fl:consent`. Changing its shape breaks analytics consent, biometric gates, and GDPR compliance. | Unit test: `fl:consent` shape unchanged after scanner flow |
| **R6:** Scanner components MUST lazy-load via `React.lazy()` or dynamic `import()`. | Scanner adds ~6MB of model dependencies. Eager loading penalises every non-upload page. | Build check: scanner chunk is separate from main bundle |
| **R7:** New consent prompt MUST NOT appear if user has NOT yet completed COPPA + biometric consent. | Three sequential consent prompts (COPPA → biometric → scan) feels hostile and may cause abandonment. | E2E test: photo scan consent only appears after COPPA and biometric are resolved |
| **R8:** `UploadSection.jsx` changes must be tested against BOTH entry points: `AppLayout.jsx` (main) AND `FamiliUnoPage.jsx` (Uno). | FamiliUnoPage imports UploadSection directly. A change that works on the homepage but breaks Uno is a regression. | E2E test: upload flow works from both `/` and `/uno` routes |
| **R9:** `compressPhoto.js` — if modified, verify output is valid JPEG that backend `/detect` accepts. | Compression corruption = silent backend failure = user sees "analysis failed" with no explanation. | Integration test: compress → upload → detect returns faces |
| **R10:** Cookie policy (`public/cookie-policy.html`) MUST be updated to document `fl:photoScanConsent` before Phase 3 ships. | GDPR requires all storage keys to be documented. Undocumented biometric-adjacent consent is a compliance risk. | Manual checklist item in ship gate |

### 13.3 Mandatory Pre-Work: Baseline Test Suite (Phase 0)

**BEFORE any feature code is written, the qa_lead agent MUST deliver the following baseline tests.** These tests lock in the current working behaviour so that any regression from feature development is immediately caught.

#### Phase 0a — Unit Tests for Existing Components (MUST ship before Phase 1)

| Test File to Create | What It Covers | Min Test Count |
|---------------------|---------------|----------------|
| `tests/upload/PhotoSlot.test.jsx` | Renders with/without photo, quality badge displays correctly, file input triggers, camera/gallery toggle, label editing (Enter/ESC/blur), remove button clears slot, change button re-opens picker | 12 |
| `tests/upload/FacePicker.test.jsx` | Renders face bounding boxes, confidence color coding (red/yellow/green), face selection fires callback with correct crop data, modal close, handles 1/2/5 faces, recommended face ranking by det_score | 10 |
| `tests/upload/DropLane.test.jsx` | File type validation (rejects non-image), file size validation (rejects >10MB), max file count enforcement, drag-drop event handling, detection status badges render, batch upload state | 8 |
| `tests/upload/compressPhoto.test.js` | Skips files <300KB, respects max dimension 1200px, outputs JPEG, preserves image orientation, handles HEIC gracefully (no crash), returns original on failure | 6 |
| `tests/upload/IntentSelector.test.jsx` | All 3+ intents render, selection fires correct callback, visual highlight on selected intent | 4 |
| `tests/consent/ConsentContext.test.jsx` | Initial state from localStorage, consent granted persists, consent revoked clears, biometric consent gate blocks detection | 6 |

**Total: ~46 baseline tests locking in current behaviour.**

#### Phase 0b — E2E Regression Scenarios (MUST ship before Phase 2)

| E2E Test File | What It Covers | Scenarios |
|---------------|---------------|-----------|
| `e2e/upload-photo-slot.spec.js` | Single photo upload → quality badge → remove → re-upload. Verifies slot lifecycle works end-to-end | 3 |
| `e2e/upload-multi-face.spec.js` | Upload photo with 2+ faces → FacePicker appears → select face → slot shows cropped photo. Verifies multi-face flow is intact | 2 |
| `e2e/upload-error-recovery.spec.js` | Upload bad photo (no face) → warning → replace with good photo → proceed to analysis. Verifies recovery path | 2 |
| `e2e/consent-gate.spec.js` | Attempt upload without biometric consent → blocked → grant consent → upload proceeds | 2 |

**Total: ~9 E2E scenarios protecting the upload critical path.**

### 13.4 Feature Flag Isolation

Every phase of Smart Photo Selection MUST be gated behind a feature flag so it can be **instantly disabled without a deploy** if any regression is detected.

```javascript
// .env / Vercel env vars
VITE_SMART_PHOTO_PHASE1 = "true"   // Quality gate enhancements
VITE_SMART_PHOTO_PHASE2 = "true"   // Auto-open FacePicker
VITE_SMART_PHOTO_PHASE3 = "true"   // Camera roll scanner
```

**Implementation rules:**
- Each phase wraps its changes in `if (import.meta.env.VITE_SMART_PHOTO_PHASEN === 'true')` guards
- When flag is `false` or absent, behaviour is **identical to current production** — zero change
- Flags are enabled per-environment: `false` in production initially, `true` in preview/dev
- After post-deploy verification protocol passes (see 13.6), flag guard can be removed in a cleanup PR

### 13.5 Integration Point Protection

Each phase touches existing components. Here's how each integration point is protected:

#### Phase 1 — `faceQualityAdvice.js` Changes
| Risk | Protection |
|------|-----------|
| New advice messages break existing badge rendering | Existing 32 unit tests + 5 E2E tests still pass. New messages tested in Phase 0a |
| Slot-aware tips interfere with PhotoSlot layout | Phase 0a PhotoSlot tests lock in current layout. New tip renders inside feature flag |
| Backend response fields missing (pose, size data) | Advice function returns existing message when new fields absent (graceful degradation) |

#### Phase 2 — `FacePicker.jsx` + `PhotoSlot.jsx` Changes
| Risk | Protection |
|------|-----------|
| Auto-open breaks manual scissors button | Phase 0a FacePicker tests verify scissors still works. Auto-open gated behind flag |
| "Recommended" badge obscures small face thumbnails | Visual regression E2E test captures before/after screenshots |
| Post-crop quality re-check creates infinite loop | Unit test: verify re-check runs once, not recursively |

#### Phase 3 — New Components + `UploadSection.jsx` + `FamililookContext.jsx` Changes
| Risk | Protection |
|------|-----------|
| SmartPhotoScanner blocks standard file picker | Feature flag: when off, standard picker is used. E2E test verifies both paths |
| Transient embeddings leak into persistent state | Unit test: verify embeddings absent from localStorage after flow completion |
| face-api model loading slows page load | Models loaded **only after consent granted**, behind `React.lazy()`. Bundle size measured in CI |
| New consent flow conflicts with existing COPPA/biometric consent | Phase 0b consent E2E tests verify existing consent still works. New consent is additive (separate `fl:photoScanConsent` key), does NOT modify existing consent gates |
| Context state changes break other consumers | FamililookContext changes are additive (new fields only). Existing resetAll() test updated to verify new fields are also cleared |
| Camera roll access prompt scares users | Consent copy reviewed by copywriter agent. Decline = zero degradation (tested) |

### 13.6 Staged Delivery with Hard Gates & Post-Deploy Verification

**No phase starts until the previous phase's gates are ALL green.** Not "mostly green" — all green. A single gate failure means stop, diagnose, and fix before moving forward.

#### Pre-Merge Gate (before code reaches main)

```
PHASE N — PRE-MERGE CHECKLIST
──────────────────────────────
[ ] Phase 0 baseline tests all pass (npm run test:run)
[ ] Phase N feature tests all pass
[ ] Feature flag OFF: all E2E tests pass (existing behaviour unchanged)
[ ] Feature flag ON: all E2E tests pass (new + existing)
[ ] npm run build succeeds (no bundle size increase > 50KB ungzipped)
[ ] Lighthouse performance audit: no regression > 5% on upload page
[ ] No new console errors or warnings
```

#### Post-Deploy Verification Protocol (after merge to production)

Each phase goes through **three verification tiers** after deploy. All three must pass before the next phase is authorised.

**TIER 1 — Automated Verification (immediate, <10 minutes)**

```
[ ] E2E suite runs against production URL — all green
[ ] Lighthouse audit on production upload page — no regression
[ ] Console error scan — no new errors or warnings
[ ] Bundle size check — within 50KB of baseline
```

**Owner:** qa_lead agent
**Trigger:** Automated on deploy via CI or manual trigger
**Fail action:** Flag OFF immediately, diagnose

**TIER 2 — Manual Validation (same day, <2 hours after deploy)**

```
[ ] Real device test — iOS Safari (latest)
[ ] Real device test — Android Chrome (latest)
[ ] Real device test — Desktop Chrome
[ ] Full flow with flag OFF: upload → analyse → results → keepsake
[ ] Full flow with flag ON: upload → analyse → results → keepsake
[ ] Edge case: bad photo (no face) → warning → replace → proceed
[ ] Edge case: group photo in parent slot → FacePicker → crop → proceed
[ ] Edge case: decline consent (Phase 3) → standard picker works
[ ] FamiliUno path: /uno upload → analyse → card game works
[ ] Consent gates: COPPA → biometric → (scan consent if Phase 3) — correct order, no doubling
```

**Owner:** qa_lead agent + fe_lead agent
**Fail action:** Flag OFF immediately, open bug ticket, block next phase

**TIER 3 — Analytics Validation (24-48 hours after deploy)**

```
[ ] Growth Monitor agent confirms: new analytics events are firing
[ ] No spike in photo_quality_failed events vs pre-deploy baseline
[ ] No drop in analysis_complete events vs pre-deploy baseline  
[ ] Upload conversion rate not regressed (compare 48h pre vs 48h post)
[ ] No increase in bounce rate on upload page
[ ] If Phase 3: photo_scan_consent_granted events appearing
```

**Owner:** growth_monitor agent
**Fail action:** Flag OFF, investigate root cause, report findings

#### Phase Progression Timeline

```
Phase 0a (baseline unit tests)
    │ GATE: 46 tests green, no existing tests broken
    ▼
Phase 0b (baseline E2E tests)
    │ GATE: 9 scenarios green, existing E2E still passes
    ▼
Phase 1 deploy → Tier 1 (10 min) → Tier 2 (same day) → Tier 3 (48h)
    │ GATE: All 3 tiers pass
    ▼
Phase 2 deploy → Tier 1 (10 min) → Tier 2 (same day) → Tier 3 (48h)
    │ GATE: All 3 tiers pass
    ▼
Phase 3 deploy → Tier 1 (10 min) → Tier 2 (same day) → Tier 3 (48h)
    │ GATE: All 3 tiers pass
    ▼
Flag guards removed in cleanup PR
```

**Total timeline: Phase 0 through Phase 3 fully verified in under 3 weeks.**

Each 48h analytics window is not passive soaking — the Growth Monitor agent actively reviews real traffic data and reports. If traffic is too low for statistical significance in 48h, extend to 72h but no further — at that point the risk shifts from "not enough data" to "stalling momentum."

### 13.7 Rollback Plan

If a regression is detected post-deploy:

1. **Immediate (< 5 min):** Set `VITE_SMART_PHOTO_PHASEN = "false"` in Vercel env vars → triggers redeploy → feature disabled, existing flow restored
2. **If flag doesn't resolve:** Revert the merge commit on `production` branch → redeploy
3. **Post-mortem:** Root-cause the regression, add it to the regression matrix, write a test that would have caught it, re-enable flag only after fix is verified

### 13.8 Updated Agent Assignments (with Phase 0 + Verification Owners)

| Step | Agent | Task | Depends On | Gate |
|------|-------|------|-----------|------|
| **0a** | **qa_lead** | **Write baseline unit tests for PhotoSlot, FacePicker, DropLane, compressPhoto, IntentSelector, ConsentContext (46 tests)** | — | **BLOCKS all feature work** |
| **0b** | **qa_lead** | **Write baseline E2E tests for upload slot lifecycle, multi-face flow, error recovery, consent gate (9 scenarios)** | — | **BLOCKS Phase 2+** |
| 1 | fe_lead | Expand `faceQualityAdvice.js` with actionable, slot-aware messages (behind VITE_SMART_PHOTO_PHASE1 flag) | **Step 0a** | Phase 0a tests pass |
| 2 | fe_lead | Add framing guide overlay to PhotoSlot (behind flag) | **Step 0a** | Phase 0a tests pass |
| 3 | qa_lead | Write tests for expanded quality advice + framing guide | Steps 1-2 | — |
| **V1-T1** | **qa_lead** | **Phase 1 post-deploy: Tier 1 automated verification (E2E on prod, Lighthouse, console errors)** | Steps 1-3 merged | **BLOCKS Phase 2 start** |
| **V1-T2** | **qa_lead + fe_lead** | **Phase 1 post-deploy: Tier 2 manual validation (3 devices, flag ON/OFF, edge cases)** | V1-T1 pass | **BLOCKS Phase 2 start** |
| **V1-T3** | **growth_monitor** | **Phase 1 post-deploy: Tier 3 analytics validation (48h — event firing, no conversion drop)** | V1-T2 pass | **BLOCKS Phase 2 start** |
| 4 | fe_lead | Auto-open FacePicker on multi-face + "Recommended" badge (behind VITE_SMART_PHOTO_PHASE2 flag) | **V1-T3 pass** | All Phase 1 verification tiers pass |
| 5 | qa_lead | Write tests for auto-open FacePicker behaviour | Step 4 | — |
| **V2-T1** | **qa_lead** | **Phase 2 post-deploy: Tier 1 automated verification** | Steps 4-5 merged | **BLOCKS Phase 3 start** |
| **V2-T2** | **qa_lead + fe_lead** | **Phase 2 post-deploy: Tier 2 manual validation (incl. FamiliUno path)** | V2-T1 pass | **BLOCKS Phase 3 start** |
| **V2-T3** | **growth_monitor** | **Phase 2 post-deploy: Tier 3 analytics validation (48h)** | V2-T2 pass | **BLOCKS Phase 3 start** |
| 6 | fe_lead | Build `usePhotoScanner` hook (scan, rank, exclude) | **V2-T3 pass** | All Phase 2 verification tiers pass |
| 7 | fe_lead | Build `clientFaceQuality.js` (on-device quality scoring) | **V2-T3 pass** | — |
| 8 | fe_lead | Build `SmartPhotoScanner.jsx` + `SuggestedPhotosGrid.jsx` | Steps 6-7 | — |
| 9 | fe_lead | Build `PhotoScanConsent.jsx` (consent UX) | — | — |
| 10 | fe_lead | Integrate scanner into PhotoSlot + UploadSection (behind VITE_SMART_PHOTO_PHASE3 flag) | Steps 8-9 | Pre-merge checklist pass |
| 11 | visual_director | Design consent sheet, suggested grid, quality overlays | — | — |
| 12 | qa_lead | Write tests for scanner, ranker, exclusion, consent | Steps 6-10 | — |
| 13 | copywriter | Write consent copy, quality tip copy, slot guidance copy | — | — |
| 14 | coo | Privacy review: verify on-device only, GDPR compliance. Update cookie-policy.html. | Steps 8-9 | — |
| **V3-T1** | **qa_lead** | **Phase 3 post-deploy: Tier 1 automated verification** | Steps 6-14 merged | **BLOCKS flag cleanup** |
| **V3-T2** | **qa_lead + fe_lead** | **Phase 3 post-deploy: Tier 2 manual validation (consent flow, scanner, decline path)** | V3-T1 pass | **BLOCKS flag cleanup** |
| **V3-T3** | **growth_monitor** | **Phase 3 post-deploy: Tier 3 analytics validation (48h — scan consent rate, conversion)** | V3-T2 pass | **BLOCKS flag cleanup** |
| 15 | fe_lead | Remove feature flag guards (cleanup PR) | **V3-T3 pass** | All Phase 3 verification tiers pass |

### 13.9 Regression Matrix Additions

The following entries MUST be added to `docs/MASTER_REGRESSION_MATRIX.md` as each phase ships:

| ID | Component | Invariant | Test Coverage | Phase |
|----|-----------|-----------|--------------|-------|
| SPS-01 | PhotoSlot | Slot renders photo preview, quality badge, and controls in all states (empty/loaded/pending/error) | `PhotoSlot.test.jsx` | 0a |
| SPS-02 | FacePicker | Multi-face selection returns correct crop coordinates and File object | `FacePicker.test.jsx` | 0a |
| SPS-03 | DropLane | File validation rejects oversized/wrong-type files, respects max count | `DropLane.test.jsx` | 0a |
| SPS-04 | compressPhoto | Compression preserves image integrity, skips small files, handles HEIC | `compressPhoto.test.js` | 0a |
| SPS-05 | ConsentContext | Existing COPPA + biometric consent gates unaffected by new photo scan consent | `ConsentContext.test.jsx` + `consent-gate.spec.js` | 0a/0b |
| SPS-06 | faceQualityAdvice | Slot-aware messages only appear when flag ON; existing messages unchanged when flag OFF | `faceQualityAdvice.test.js` (updated) | 1 |
| SPS-07 | FacePicker | Auto-open only triggers when flag ON; scissors button still works in both states | `FacePicker.test.jsx` (updated) | 2 |
| SPS-08 | SmartPhotoScanner | Camera roll scanning never fires without explicit consent | `usePhotoScanner.test.js` | 3 |
| SPS-09 | SmartPhotoScanner | Transient embeddings are NOT persisted to localStorage or uploaded | `usePhotoScanner.test.js` | 3 |
| SPS-10 | SmartPhotoScanner | Flag OFF = standard file picker, zero code path change | `upload-photo-slot.spec.js` | 3 |
| SPS-11 | PhotoScanConsent | Decline = standard picker, no degradation, no retry prompts | `PhotoScanConsent.test.jsx` | 3 |
| SPS-12 | UploadSection | Analysis completes successfully with photos selected via scanner (same backend contract) | `smoke-upload-analyze.spec.js` (updated) | 3 |
