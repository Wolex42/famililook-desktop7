# PRD: Face-Anchored Naming — Tap-to-Name on Group Photo

> **Author**: CPO Agent
> **Date**: 2026-04-02
> **Product**: FamiliLook (desktop2 FE)
> **Priority**: P1
> **Status**: SPEC_READY

---

## 1. Problem Statement

When a group photo detects 12+ faces, users must mentally map numbered badges on the photo (#1, #2... #13) to a separate naming grid on Card 2 of the carousel. With 13 faces this is a cognitive nightmare — users can't tell which "Person 7" in the grid corresponds to which face in the photo. They either guess wrong (producing wrong keepsake names) or abandon the flow entirely.

**Evidence:**
- Your own test with 13 faces showed the disconnect clearly
- The current flow requires a horizontal swipe to move from photo → naming, losing visual context
- No interactive link exists between photo badges and naming fields
- `FaceDetectionPreview` already has `onFaceClick` and `highlightedIndex` props — implemented but never wired up

## 2. Goal

Eliminate the mental mapping burden by letting users tap a face on the photo to name it directly, with a bottom sheet anchored to the selected face. Each tap shows the face crop so the user has visual certainty they're naming the right person.

## 3. Solution: Tap-to-Name Bottom Sheet

### Flow

```
1. Group photo displayed with numbered face badges (existing)
2. User taps face badge #6
3. Badge #6 highlights pink (existing highlightedIndex behaviour)
4. All other badges dim slightly
5. Bottom sheet slides up from bottom of screen:
   ┌─────────────────────────────────────┐
   │  ┌──────┐                           │
   │  │ crop │  Name: [_____________]    │
   │  │  #6  │  Role: [Select role   ▼] │
   │  └──────┘                           │
   │   ● Good quality                    │
   │                                     │
   │     ◀ Prev (#5)    Next (#7) ▶     │
   │          [Exclude from analysis]     │
   └─────────────────────────────────────┘
6. User types name, selects role
7. Taps "Next ▶" — sheet updates to show face #7, badge #7 highlights
8. After naming all faces, user taps outside sheet or "Done" button
9. Sheet closes, all names are saved
```

### Why This Works
- **Visual certainty**: Thumbnail crop shows the exact face being named
- **No mental mapping**: Tap face → name appears right there
- **Progressive flow**: Prev/Next lets user walk through all faces sequentially
- **No carousel swipe**: Photo stays visible above the bottom sheet
- **Zero data model change**: Uses same `faceNames[idx]` and `faceRelationships[idx]` state

---

## 4. Technical Design

### 4.1 What Already Exists (no changes needed)

| Component | Existing Feature | Status |
|-----------|-----------------|--------|
| `FaceDetectionPreview.jsx:97-110` | `onFaceClick(face, index)` prop | **Implemented, not wired** |
| `FaceDetectionPreview.jsx:197-218` | `highlightedIndex` — pink border + glow + z-index boost | **Implemented, not wired** |
| `GroupSnapshotSection.jsx:2174` | `handleFaceNameChange(faceIndex, newName)` | **Working** — syncs pairwise_links, thumbnails, context |
| `GroupSnapshotSection.jsx:2228` | `handleFaceRelationshipChange(faceIndex, newRole)` | **Working** — syncs context |
| `GroupSnapshotSection.jsx:2314` | `toggleExcludeFace(faceId, label)` | **Working** — manages exclusion state |
| `fl:thumbnails` in localStorage | Cropped face images keyed by name | **Working** — used by keepsakes + card game |

### 4.2 New Component: `FaceNamingSheet.jsx`

A bottom sheet overlay that appears when a face is tapped.

**Props:**
```javascript
{
  face: Object,              // Face object from result.faces[idx]
  faceIndex: number,         // Array index (0-based)
  totalFaces: number,        // Total visible face count
  currentName: string,       // faceNames[idx] || face.name || "Person N"
  currentRole: string,       // faceRelationships[idx] || ""
  thumbnailUrl: string,      // From fl:thumbnails[name] or cropped from photo
  qualityLevel: string,      // "good" | "advisory" | "warning"
  onNameChange: function,    // → handleFaceNameChange(idx, name)
  onRoleChange: function,    // → handleFaceRelationshipChange(idx, role)
  onExclude: function,       // → toggleExcludeFace(faceId, label)
  onPrev: function,          // Navigate to previous face
  onNext: function,          // Navigate to next face
  onClose: function,         // Close the sheet
  isExcluded: boolean,       // Whether this face is currently excluded
}
```

**Rendering:**
- Fixed to bottom of viewport (`position: fixed; bottom: 0`)
- z-index: 1100 (below COPPA 2000, above content)
- Backdrop dimmer (rgba(0,0,0,0.3)) — tapping backdrop closes sheet
- 44px minimum touch targets on all buttons
- Smooth slide-up animation (transform: translateY)
- Face thumbnail: 64x64px, cropped from `fl:thumbnails[name]`
- Name input: auto-focused when sheet opens
- Role dropdown: reuses existing `RELATIONSHIP_OPTIONS` array

### 4.3 State Changes in GroupSnapshotSection

**New state (2 fields):**
```javascript
const [selectedFaceIdx, setSelectedFaceIdx] = useState(null);  // null = sheet closed
const [sheetVisible, setSheetVisible] = useState(false);
```

**New handler:**
```javascript
const handleFaceClick = useCallback((face, idx) => {
  setSelectedFaceIdx(idx);
  setSheetVisible(true);
}, []);

const handleSheetClose = useCallback(() => {
  setSheetVisible(false);
  setSelectedFaceIdx(null);
}, []);

const handleSheetPrev = useCallback(() => {
  setSelectedFaceIdx(prev => {
    // Find previous non-excluded face
    let target = prev - 1;
    while (target >= 0 && excludedSet.has(getFaceKey(faces[target], target))) target--;
    return target >= 0 ? target : prev;
  });
}, [faces, excludedSet]);

const handleSheetNext = useCallback(() => {
  setSelectedFaceIdx(prev => {
    // Find next non-excluded face
    let target = prev + 1;
    while (target < faces.length && excludedSet.has(getFaceKey(faces[target], target))) target++;
    return target < faces.length ? target : prev;
  });
}, [faces, excludedSet]);
```

### 4.4 Wiring Changes in DetectionCarousel

Pass `onFaceClick` and `highlightedIndex` to `FaceDetectionPreview`:

```javascript
<FaceDetectionPreview
  imageUrl={previewUrl}
  faces={visibleFaces}
  onFaceClick={handleFaceClick}               // NEW — was undefined
  highlightedIndex={selectedFaceIdx}           // NEW — was null
/>
```

### 4.5 What Happens to Card 2 (Naming Grid)

**Keep it.** The grid becomes a secondary/review view:
- Still accessible via carousel swipe
- Shows all names at a glance after user has named faces via tapping
- Acts as a "review all" before "Update Names & Continue"
- No code changes to Card 2 — it reads the same `faceNames` and `faceRelationships` state

This means **zero removal of existing UI** — the bottom sheet is purely additive.

---

## 5. Blast Radius Analysis

### Zone 1: Direct Changes (3 files)

| File | Change | Risk |
|------|--------|------|
| `src/layout/GroupSnapshotSection.jsx` | Add `selectedFaceIdx`/`sheetVisible` state + handlers. Wire `onFaceClick`/`highlightedIndex` to FaceDetectionPreview. Render FaceNamingSheet when `sheetVisible`. | **MEDIUM** — GroupSnapshotSection is 4000+ lines. Changes are additive (new state, new render). |
| `src/components/detection/FaceNamingSheet.jsx` | **NEW FILE** — bottom sheet component | **LOW** — no existing code affected |
| `src/components/detection/FaceDetectionPreview.jsx` | **NO CHANGES** — `onFaceClick` and `highlightedIndex` already implemented | **NONE** |

### Zone 2: State & Data Flow (7 downstream consumers)

The bottom sheet calls the **same handlers** that the Card 2 grid calls today. The data flow is identical:

```
Bottom Sheet name edit
    ↓ handleFaceNameChange(idx, name)     ← SAME function
    ↓ Updates faceNames[idx]               ← SAME state
    ↓ Updates result.faces[idx].name       ← SAME mutation
    ↓ Updates pairwise_links.pair names    ← SAME sync
    ↓ Re-keys fl:thumbnails                ← SAME logic
    ↓ setGroupAnalysis(updated)            ← SAME context sync
    ↓ persistAnalysisToSession()           ← SAME persistence
```

| Consumer | Reads | Affected? | Why |
|----------|-------|-----------|-----|
| PairwiseCarousel | `faceRelationships[idx]`, `result.faces[idx].name` | **NO** — reads same state | Same handlers update it |
| AnalysisSection | `groupAnalysis` from context | **NO** — same context sync | `setGroupAnalysis()` still called |
| Keepsakes (useGroupPairwiseKeepsakeData) | `pairwiseLink.pair[0/1]` | **NO** — pairwise_links updated by same handler | `handleFaceNameChange` line 2191 |
| Card Game (deckBuilder.js) | `fl:groupSnapshot.faces[].name/.relationship` | **NO** — same localStorage writes | Written by same handler |
| Thumbnails | `fl:thumbnails[name]` | **NO** — re-keyed by same handler | `handleFaceNameChange` line 2213-2217 |
| Card 2 naming grid | `faceNames[idx]`, `faceRelationships[idx]` | **NO** — reads same state | Updated by same handler |
| Exclusion system | `excludedFaceIds` | **NO** — same `toggleExcludeFace()` called | Sheet has "Exclude" button |

**ZERO downstream changes needed.** The bottom sheet is a new INPUT mechanism using the SAME state management.

### Zone 3: localStorage & Session

| Key | Written By | Affected? | Why |
|-----|-----------|-----------|-----|
| `fl:groupSnapshot` | handleFaceNameChange | **NO** — same write | Same handler |
| `fl:thumbnails` | handleFaceNameChange | **NO** — same re-key | Same handler |
| `fl:faces` | handleFaceNameChange | **NO** — same write | Same handler |
| `fl:pairwise` | buildFilteredResult | **NO** — not changed | |
| `fl:analysis-cache` (session) | setGroupAnalysis | **NO** — same path | Same handler |

### Zone 4: CSS & Layout

| Concern | Risk | Mitigation |
|---------|------|-----------|
| Bottom sheet overlaps navigation bar | **LOW** | z-index 1100, bottom padding for nav |
| Sheet covers photo on small screens | **MEDIUM** | Max height 40vh, photo stays visible above |
| Keyboard opens on name input → pushes sheet | **MEDIUM** | Use `visualViewport` API to adjust sheet position on keyboard open |
| Sheet animation jank on low-end devices | **LOW** | Use `transform: translateY()` (GPU-accelerated), not `bottom` |

### Zone 5: Cross-Product

| Product | Affected? | Why |
|---------|-----------|-----|
| FamiliUno | **NO** | FamiliUno doesn't use group photo mode |
| FamiliPoker | **NO** | Independent codebase |
| FamiliMatch | **NO** | Independent codebase |
| Backend (desktop3) | **NO** | All changes are frontend-only |

---

## 6. Feature Flag

Gate behind `VITE_FACE_NAMING_SHEET === "true"`.

When flag OFF:
- `onFaceClick` not passed to FaceDetectionPreview (stays `undefined`)
- `highlightedIndex` stays `null`
- FaceNamingSheet never renders
- Card 2 naming grid is the only way to name faces (existing behaviour)

When flag ON:
- Tapping face opens bottom sheet
- Card 2 grid still works as review/fallback
- Both use identical state + handlers

---

## 7. Acceptance Criteria

- [ ] Tapping a face badge opens bottom sheet with that face's thumbnail, name, and role
- [ ] Selected face badge highlights pink with glow (existing FaceDetectionPreview behaviour)
- [ ] Non-selected badges dim (reduce opacity)
- [ ] Name input auto-focuses on sheet open
- [ ] Typing name and blurring/pressing Enter saves via `handleFaceNameChange`
- [ ] Selecting role saves via `handleFaceRelationshipChange`
- [ ] Prev/Next buttons navigate to adjacent non-excluded faces
- [ ] "Exclude from analysis" calls `toggleExcludeFace`, closes sheet, removes badge
- [ ] Tapping backdrop or "Done" closes sheet
- [ ] Card 2 naming grid reflects names entered via bottom sheet (same state)
- [ ] Pairwise carousel shows correct names after bottom sheet edits
- [ ] Keepsakes show correct names after bottom sheet edits
- [ ] Card game deck uses correct names after bottom sheet edits
- [ ] Thumbnails re-keyed correctly when names changed via bottom sheet
- [ ] 44px minimum touch targets on all interactive elements
- [ ] Sheet height max 40vh — photo stays visible above
- [ ] Works on iOS Safari, Android Chrome, desktop Chrome
- [ ] Flag OFF = zero change to existing behaviour

---

## 8. Agent Assignments

| Step | Agent | Task | Depends On | Gate |
|------|-------|------|-----------|------|
| 0 | qa_lead | Write baseline tests for group naming flow (Card 2 grid, handleFaceNameChange, handleFaceRelationshipChange, pairwise sync) | — | BLOCKS feature work |
| 1 | fe_lead | Create `FaceNamingSheet.jsx` component (bottom sheet with name/role/prev/next/exclude) | — | — |
| 2 | fe_lead | Add `selectedFaceIdx`/`sheetVisible` state + handlers to GroupSnapshotSection | — | — |
| 3 | fe_lead | Wire `onFaceClick` and `highlightedIndex` to FaceDetectionPreview in DetectionCarousel | Step 2 | — |
| 4 | fe_lead | Render FaceNamingSheet in GroupSnapshotSection (behind flag) | Steps 1-3 | — |
| 5 | qa_lead | Write tests: sheet open/close, name saves, role saves, prev/next navigation, exclusion, flag isolation | Steps 1-4 | — |
| 6 | visual_director | Review sheet design: thumbnail size, spacing, animation, keyboard handling | Step 1 | — |
| 7 | copywriter | Review label text: button labels, placeholder text, exclude confirmation | Step 1 | — |
| V-T1 | qa_lead | Post-deploy Tier 1: automated tests + build | Steps 1-5 merged | BLOCKS V-T2 |
| V-T2 | qa_lead + fe_lead | Post-deploy Tier 2: manual device testing (3 devices, 13-face photo) | V-T1 pass | BLOCKS V-T3 |
| V-T3 | growth_monitor | Post-deploy Tier 3: analytics validation (48h) | V-T2 pass | BLOCKS flag cleanup |

---

## 9. Effort Estimate

| Component | Size | Days |
|-----------|------|------|
| FaceNamingSheet.jsx (new) | S | 1 |
| GroupSnapshotSection wiring | S | 0.5 |
| Baseline + feature tests | M | 1 |
| Manual testing + polish | S | 0.5 |
| **Total** | **M** | **3 days** |

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Keyboard pushes sheet off screen on mobile | Medium | High | Use `visualViewport.height` to cap sheet position; test on iOS + Android |
| Thumbnail crop quality poor for small faces | Medium | Low | Show face number as fallback if thumbnail unavailable |
| User doesn't discover tap-to-name (just swipes to Card 2) | Medium | Low | Add pulsing "Tap a face to name" prompt below photo; Card 2 still works |
| Name change in sheet not reflected in Card 2 grid | Low | Medium | Both read same `faceNames` state — React re-render guarantees sync |
| 13 faces on small screen → hard to tap precise badge | Medium | Medium | Increase badge touch target to 44px; use expanded hit area beyond visible badge |
| Sheet animation janky on low-end | Low | Low | GPU-accelerated `transform: translateY()`, no reflows |

---

## 11. Regression Matrix Additions

| ID | Component | Invariant | Test Coverage | Phase |
|----|-----------|-----------|--------------|-------|
| FAN-01 | FaceDetectionPreview | `onFaceClick` fires with correct (face, index) on badge tap | Unit test | 0 |
| FAN-02 | FaceDetectionPreview | `highlightedIndex` renders pink border + glow on correct face | Unit test | 0 |
| FAN-03 | FaceNamingSheet | Name change calls `onNameChange` with correct (index, name) | Unit test | 5 |
| FAN-04 | FaceNamingSheet | Role change calls `onRoleChange` with correct (index, role) | Unit test | 5 |
| FAN-05 | FaceNamingSheet | Prev/Next skips excluded faces | Unit test | 5 |
| FAN-06 | GroupSnapshotSection | Bottom sheet name edit → pairwise_links updated | Integration test | 5 |
| FAN-07 | GroupSnapshotSection | Bottom sheet name edit → fl:thumbnails re-keyed | Integration test | 5 |
| FAN-08 | GroupSnapshotSection | Bottom sheet name edit → groupAnalysis in context updated | Integration test | 5 |
| FAN-09 | GroupSnapshotSection | Flag OFF = no sheet, no highlight, Card 2 grid only | Unit test | 5 |
| FAN-10 | FaceNamingSheet | Sheet closes on backdrop tap and "Done" button | Unit test | 5 |
