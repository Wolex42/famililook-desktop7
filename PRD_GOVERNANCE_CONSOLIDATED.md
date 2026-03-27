# FamiliLook — Consolidated PRD & Governance Document

**Version:** 3.5
**Date:** 2026-02-24
**Product Owner:** Francis Aroyehun
**Status:** Active Development (Beta — Phase 0)
**PRD Base:** v1.2.1 (January 20, 2026)

> This document consolidates ALL product requirements, user experience requests,
> fixes applied, and outstanding to-dos into one governance reference.

---

## Table of Contents

1. [Vision & Pillars](#1-vision--pillars)
2. [Platform & Beta Strategy](#2-platform--beta-strategy)
3. [Architecture](#3-architecture)
4. [BE/FE Contract & Stability Rules](#4-befe-contract--stability-rules)
5. [User Journeys](#5-user-journeys)
6. [Card System](#6-card-system)
7. [Game Modes](#7-game-modes)
8. [Emotional Journey & UX](#8-emotional-journey--ux)
9. [Security & Privacy](#9-security--privacy)
10. [Implementation Status](#10-implementation-status)
11. [UX Fixes Applied (Full History)](#11-ux-fixes-applied-full-history)
12. [Outstanding To-Dos](#12-outstanding-to-dos)
13. [Roadmap](#13-roadmap)
14. [QA & Acceptance Criteria](#14-qa--acceptance-criteria)
15. [Monetization](#15-monetization)
16. [Document Index](#16-document-index)
17. [PRD Version History](#17-prd-version-history)

---

## 1. Vision & Pillars

### Vision Statement
> "Turn facial resemblance into joyful family moments — private, premium, and playable."

### Core Pillars (Non-Negotiable)

| # | Pillar | Description |
|---|--------|-------------|
| 1 | **Privacy-First** | 100% local processing; no cloud uploads; no accounts required |
| 2 | **Scientific-Grade** | 8-feature analysis with deterministic winner selection |
| 3 | **Cards-First UX** | Primary outputs are visual cards, not raw data. Analytics behind "Explore details" |
| 4 | **Decisive Outcomes** | Always Parent A or Parent B; never "balanced" or 50/50 |
| 5 | **Playable + Collectible** | Card games for family engagement (ages 4 to adult) |
| 6 | **No Silent Degradation** | Individual: exactly 1 face or hard-fail. Group: face-selection panel |
| 7 | **Blended Family Support** | Parent A/B with user-defined naming (Mum/Dad/Guardian) |
| 8 | **Premium Warm Aesthetic** | Warm amber/gold accents, calm spacing, subtle motion |

### Target Users

| Segment | Use Case | Primary Output |
|---------|----------|----------------|
| Families | "Who does the baby look like?" | Keepsake Cards |
| Parents | Daily resemblance discovery | Mobile carousel |
| Extended Family | Group reunions | Group Family Card |
| Game Nights | Family bonding activity | Playing Cards Deck |
| Blended/Adoptive | Neutral labels (Parent A/B) | Inclusive results |
| Family Photographers | Add-on service | Premium exports |
| Genealogy Enthusiasts | Family tree visualization | Group analysis |

---

## 2. Platform & Beta Strategy

**Shipped product target:** iOS + Android (on-device analysis, no server).

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 (now) | Desktop harness — React UI + localhost FastAPI (port 8008). Photos stay on test machine. | ACTIVE |
| Phase 1 (next) | Mobile-only beta — same analysis engine runs in-app on iOS/Android. No cloud. | PLANNED |

> "Local-only" = no cloud upload. A localhost companion service is still local-only.

---

## 3. Architecture

### Technology Stack

| Layer | Technology | Repository |
|-------|------------|------------|
| Frontend | React 18 + Vite + Tailwind CSS | `famililook-desktop2` (branch: `rebuild/mission-lock`) |
| Backend | Python + FastAPI + Uvicorn | `famililook-desktop3` |
| Face Detection | InsightFace RetinaFace (buffalo_l) + MediaPipe fallback | Backend |
| Face Recognition | **AdaFace IR50** (CVPR 2022, ONNX) with ArcFace fallback | Backend |
| Facial Analysis | MediaPipe FaceMesh (468 landmarks), calibrated percentile labels | Backend |
| State | React Context (`FamililookContext`) | Frontend |
| FamiliMatch FE | React 18 + Vite + Tailwind + framer-motion | `famililook-desktop6` |
| FamiliMatch BE | Python + FastAPI + WebSocket rooms | `famililook-desktop7` |
| Testing | Vitest (723 d2 + 100 d6) + Pytest (98 d3 + 111 d7) + Playwright | All repos |
| Testing (Gen 2) | Vitest (932 d4) + Pytest (37 d5) | desktop4/5 |
| Ops/CI | Pre-commit hook (FE tests + build + BE tests) | `.claude/pre-commit-hook.sh` |

> **Total platform tests: 1,964** (d2: 723, d3: 98, d4: 932, d5: 37, d6: 100, d7: 111)

### Product Feature Boundaries

| Feature / Game | FamiliLook | FamiliPoker | FamiliMatch | Notes |
|----------------|:----------:|:-----------:|:-----------:|-------|
| 8-feature analysis | Yes | Inherited | Yes | Shared desktop3 endpoint |
| Winner determination (5-3 rule) | Yes | No | No | Family context only |
| Feature Match (card-matching) | Yes | No | No | Renamed from FaceMatch UNO |
| Memory Match | Yes | No | No | 3 age groups |
| Card Gallery / Print | Yes | No | No | 52-card deck |
| Face Fusion (gacha) | Yes | No | No | Family composite faces |
| Hungry Heads | Yes | No | No | Motion-controlled |
| Feature Catch | Yes | No | No | Arcade bubble-catching |
| Keepsakes (6 templates) | Yes | No | No | PNG export |
| Group Photo snapshot | Yes | No | No | Pairwise family analysis |
| Pet comparison | Yes | No | No | Embedding similarity |
| Feature Poker | No | Yes | No | Texas Hold'em with face cards |
| Feature 21 (Blackjack) | No | Yes | No | Star values (1-5) |
| Multiplayer Battle | No | Yes | No | Top Trumps via desktop5 |
| Casino aesthetics (3D cards, felt) | No | Yes | No | GameCard3D, FeltTable, ChipStack |
| Solo Compare (instant) | No | No | Yes | Direct API call |
| Duo Room (synchronized) | No | No | Yes | WebSocket countdown reveal |
| Group Room (party matrix) | No | No | Yes | Pairwise N×N matrix |
| Chemistry labels | No | No | Yes | 5 tiers |
| Face Fusion 50/50 blend | No | No | Yes | Compatibility context |
| BIPA consent modal | No | No | Yes | Required before any analysis |

> **Separation principle:** Each product owns distinct features. FamiliPoker requires FamiliLook's analysis output (family face cards) as input. FamiliMatch is fully standalone.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Server health check |
| `/faces/validate` | POST | Validate single-face uploads |
| `/faces/detect` | POST | Detect faces in group photos |
| `/kinship/enroll` | POST | Cache face descriptors for session |
| `/kinship/analyze` | POST | Full resemblance analysis (individual) |
| `/kinship/group-snapshot` | POST | Group photo pairwise analysis |
| `/cards/generate-deck` | POST | Generate playing card deck |
| `/face/morph` | POST | Delaunay triangulation face morphing |
| `/feedback` | POST | Structured survey feedback collection |
| `/data/forget-me` | POST | GDPR — delete all stored data |
| `DELETE /kinship/gallery/{id}` | DELETE | GDPR — delete specific person |
| `DELETE /kinship/gallery` | DELETE | GDPR — delete all gallery data |

### Key Directories

```
famililook-desktop2/
├── src/
│   ├── components/       # UI components (results, cards, keepsakes, upload)
│   ├── game/             # Game logic (deckBuilder, FeatureMatch, MemoryMatch, FaceFusion, etc.)
│   ├── layout/           # Page layouts (AppLayout, UploadSection, GroupSnapshot)
│   ├── state/            # React context providers
│   ├── lib/              # API services
│   └── utils/            # Constants, helpers
├── docs/                 # Documentation
├── tests/                # Unit tests (Vitest)
└── e2e/                  # End-to-end tests (Playwright)
```

---

## 4. BE/FE Contract & Stability Rules

### The 8-Feature System

Backend outputs exactly 8 features: `eyes`, `eyebrows`, `smile`, `nose`, `face_shape`, `skin`, `hair`, `ears`.

### Stability Rules (NON-NEGOTIABLE)

| Rule | Description |
|------|-------------|
| **Winner Trust** | FE trusts BE `winner` field — NEVER re-derives it |
| **Order Invariance** | Swapping parent order doesn't change who won |
| **8-Feature Count** | `mumCount + dadCount + unknownCount === 8` always |
| **No 50/50** | Display always nudged to show winner's margin (min 51/49) |
| **Unknown Respected** | FE displays "?" for unknown features, never invents a parent |
| **No Rewrites** | Architectural changes require PRD version bump |
| **BE Provides All Data** | FE renders BE data; FE NEVER computes winner, percentages, or features |
| **On BE Failure** | Show error to user, never fabricate results |

### Winner Determination (5-3 Rule)

```
1. Count feature votes → parent with more votes wins
2. If tied → use weighted similarity scores (NOT embedding similarity)
3. If still tied → deterministic SHA tiebreak (symmetric, order-invariant)
4. NEVER "balanced" — winner MUST be declared
```

### API Response Shape (kinship_analyze.v1)

```json
{
  "ok": true,
  "schema_version": "kinship_analyze.v1",
  "engineResult": {
    "mode": "individual",
    "children": [{
      "name": "Emma",
      "inheritance": {
        "winner": "parent1",
        "winner_reason": "votes_parent1"
      },
      "feature_votes": {
        "eyes": "parent1", "eyebrows": "parent2",
        "smile": "parent1", "nose": "parent1",
        "face_shape": "parent2", "skin": "parent1",
        "hair": "parent1", "ears": "unknown"
      }
    }]
  }
}
```

### Immutable Contract Fields
- `ok` — boolean success indicator
- `schema_version` — MUST NOT change without explicit human approval
- `engineResult` — shape MUST remain backward compatible; field removal forbidden; new fields MUST be optional

### Protected Files (require explicit approval to modify)
- Backend: `main.py`
- Frontend: `useKinshipService.js`, `analysisService.js`

---

## 5. User Journeys

### Journey A: Individual Analysis — COMPLETE
Upload 2 parents + 1-N children. Full 8-feature analysis per child.
1. Choose Individual Mode
2. Upload Child photo (must be 1 face)
3. Upload Parent A photo (must be 1 face)
4. Upload Parent B photo (must be 1 face)
5. Tap Analyze
6. Premium anticipation animation plays
7. Results render: Verdict, Keepsake Family Card, Narrative, Explore details (collapsed)

### Journey B: Single Parent Mode — PARTIAL
Upload 1 parent + children. Uses same analysis pipeline.
- Schema supports it
- Dedicated UI flow: partial (uses same UI as dual-parent)
- Single parent messaging: NOT STARTED

### Journey C: Group Photo Mode — COMPLETE
Upload group photo. Pairwise analysis between all detected faces.
1. Upload group photo
2. Face detection → detection carousel (swipe between photo preview and name grid)
3. Name faces (optional)
4. Analyze → pairwise 8-feature comparison
5. Results: Combined similarity (60% embedding + 40% feature), vertical feature tables
6. "Play Card Game" button → transitions to card games

### Journey D: Card Games — COMPLETE (4 game types)
Analysis results become playable card decks.
- Feature Match (card-matching)
- Memory Match (3 age groups)
- Card Gallery / Print
- Face Fusion (gacha spinner + feature compositing)

### Journey E: Keepsakes — COMPLETE
Export analysis as premium visual cards.
- 6 age-themed templates
- Family Card, Certificate, Pokemon-style variants
- Group Family Card collage
- PNG export (1200x1600px)
- Mirror Image card (Person B photo rendering)

### Journey F: Pet Comparison — PARTIAL
Entertainment feature — "which parent does the pet look like?"
- Uses embedding similarity (not scientifically accurate)
- Context supports it, UI minimal

### Journey G: Solo Compare (Gen 3 — FamiliMatch) — FUNCTIONAL
Two adults upload photos for instant compatibility comparison.
1. User opens desktop6, navigates to `/solo`
2. Uploads two photos (drag/drop or camera capture)
3. BIPA consent modal shown before first comparison
4. Frontend calls desktop3 `/kinship/analyze` directly (adults as parent1/parent2, one reused as child)
5. Backend returns: `engineResult.parents.parent1/parent2.calibrated_features` + `children[0].embedding_similarity_parent2`
6. Frontend displays: compatibility % + chemistry label + 8-feature comparison + face morph (50/50 blend via `/face/morph`)
7. Chemistry labels: Feature Twins (85%+), Magnetic Match (70-84%), Complementary Pair (55-69%), Interesting Contrast (40-54%), Opposites Attract (0-39%)

### Journey H: Duo Room (Gen 3 — FamiliMatch) — BUILT, NOT DEPLOYED
Two people compare faces in a synchronized room.
1. Player A creates room → gets 4-digit code
2. Player B joins with code
3. Both grant BIPA consent + upload selfie
4. desktop7 holds photos in RAM, calls desktop3 for ML analysis
5. Countdown 3..2..1 → simultaneous reveal of score + fusion + features
6. Room closes → all data deleted from RAM

### Journey I: Group Room (Gen 3 — FamiliMatch) — BUILT, NOT DEPLOYED
3-6 people compare pairwise in a party setting.
1. Host creates room → shares code
2. Players join + upload selfies
3. desktop7 computes NxN pairwise compatibility matrix
4. Reveal: grid of all pairs + "most compatible pair" winner highlight

### Journey J: Family Trail (Gen 4 — FamiliTrail) — BUILT
Gamified feature discovery — users explore all platform features on a board-game trail.
1. User lands on homepage → sees "Enter the Trail" portal (or taps `/trail` link)
2. SVG board-game canvas renders 22 nodes across 6 themed zones
3. "YOU ARE HERE" bouncing token shows last accessible stop for current plan
4. Tap free node → bottom-sheet with description + "Try It Now" → navigates to feature
5. Hover/tap locked node → 2-second peek preview with personalised data from localStorage
6. Locked node CTA → "Upgrade to Plus/Pro" → navigates to `/plans`
7. Coming Soon nodes → "Get Notified When Ready" → teaser with 3-step ordering journey
8. Campaign badges (Mother's Day, Easter) shown when within seasonal window

### Journey K: FamiliVault Cards (Gen 4 — FamiliVault) — BUILT
Premium collector trading cards generated from real biometric analysis data.
1. User completes kinship analysis (Journey A or C)
2. Navigate to `/vault` preview gallery OR open Keepsakes modal → select FamiliVault Card
3. Card generated with: real feature similarities as star ratings, deterministic rarity tier, heritage type, power stats (PWR/DEF/CHM), unique serial number
4. Standalone: hover for holographic foil effect, click to flip and see card back with DNA ring + barcode
5. Keepsake: preview print-ready version with QR placeholder + stat bars → order via Prodigi
6. Rarity ranges from Common (low scores) to Legendary/Mythic (6+ features at 80th+ percentile)
5. Room closes → all data deleted from RAM

---

## 6. Card System

### 6.1 Keepsake Cards — Save & Share

| Attribute | Value |
|-----------|-------|
| Purpose | Export / Print / Share as family memento |
| Data Source | Real 8-feature analysis results |
| Features Shown | All 8 with parent attribution |
| Export | PNG (high-res), PDF (planned) |
| Variants | Family Card, Certificate, Pokemon-style, Group Collage, Mirror Image |

### 6.2 Playing Cards — Game & Collect

| Attribute | Value |
|-----------|-------|
| Purpose | Playable card game |
| Data Source | Backend features + seed-based fallback |
| Features Shown | 4 random (from 8), two-line badges (category + trait) |
| Deck Size | 15–72 cards (scales with family size) |
| Rarity | 1–5 stars based on feature uniqueness |

### Card Anatomy (Playing Card)

```
┌──────────────────────┐
│ Eyes          Face    │ ← corner badges (emoji + category + trait)
│ "Almond"    "Oval"   │    two-line: white category, gold ONE-WORD trait
│                      │
│    ┌──────────┐      │
│    │  PHOTO   │      │ ← family member face photo
│    │          │      │
│    └──────────┘      │
│    ★★★★☆             │ ← rarity stars (top-left, above badges)
│                      │
│ Nose          Hair   │ ← bottom corner badges
│ "Broad"    "Forward" │
│                      │
│       "Sarah"        │ ← person name
└──────────────────────┘
```

### Feature Icons & Labels (Centralized in `src/utils/constants.js`)

| Feature | Icon | Short Label |
|---------|------|-------------|
| eyes | `\u{1F440}` | Eyes |
| eyebrows | `\u{1F928}` | Brows |
| smile | `\u{1F60A}` | Smile |
| nose | `\u{1F443}` | Nose |
| face_shape | `\u{1F4A0}` | Face |
| skin | `\u{2728}` | Skin |
| hair | `\u{1F487}` | Hair |
| ears | `\u{1F442}` | Ears |

### Deck Building Pipeline

```
buildDeck({ plan, maxCards })
  → Load family data from localStorage
  → Priority: fl:groupSnapshot first, then buildDeck() fallback
  → Extract features per person (calibrated → raw → embedding → hash fallback)
  → Generate face cards (4 display features + all 8 stored)
  → Generate special cards (Mirror, Swap, Family Bond, Wild)
  → Assign rarity stars (1–5)
  → Return { cards[], meta }
```

### Calibrated Feature Labels (One-Word, 8×5 Percentile Grid)

All 8 primary features use **one-word** labels derived from percentile-based calibration. Labels are identical across BE → FE → card corner badges.

| Feature | 0–20 | 20–40 | 40–60 | 60–80 | 80–100 | Metric |
|---------|------|-------|-------|-------|--------|--------|
| **Eyes** | Narrow | Almond | Balanced | Round | Wide | `aspect_ratio` (avg L+R) |
| **Brows** | Straight | Soft | Arched | High | Dramatic | `curvature` (avg L+R) |
| **Smile** | Thin | Subtle | Balanced | Full | Broad | `mar` |
| **Nose** | Narrow | Slim | Medium | Broad | Wide | `nostril_width` |
| **Face** | Square | Round | Balanced | Oval | Long | `face_ratio` (L/W) |
| **Skin** | Deep | Tan | Medium | Light | Fair | `luminance` |
| **Hair** | Low | Forward | Balanced | High | Receded | `forehead_ratio` |
| **Ears** | Flat | Subtle | Balanced | Visible | Prominent | `protrusion` (avg L+R) |

**Occlusion rule**: If ears `visibility_left < 0.5` AND `visibility_right < 0.5` → label = `"Occluded"`, description = `"Not clearly visible at this angle"`.

**Left/right averaging**: Eyes, Brows, and Ears metrics use `_left/_right` suffix keys from extraction. `calibrate_feature()` averages both sides when the bare metric key is not found.

Sub-features (eye_spacing, brow_thickness, lip_fullness, etc.) retain multi-word titles — they are secondary and only appear in card game detail views.

### Group Snapshot Similarity Formula

```
combined_sim = 0.6 × embedding_similarity + 0.4 × avg_measured_feature_similarity
```

- **Embedding similarity** (60%): 512-dim AdaFace cosine similarity, normalized to 0–1
- **Feature similarity** (40%): Average of per-feature scores, **only for measured features**
- Features where either face lacks measurements are flagged `measured: false` and excluded from the average
- FE shows collapsible "How we calculated this" breakdown with per-feature % and unmeasured exclusion count

### Data Source Priority (Phantom Member Prevention)
When both individual and group data exist in localStorage:
1. Group snapshot names take priority (named faces from group photo)
2. Pairwise pool names included
3. Individual analysis names (Parent 1/2, file-name children) excluded when group data exists

---

## 7. Game Modes

### 7.1 Feature Match (Card-Matching) — IMPLEMENTED
**File:** `src/game/FaceMatchGame.jsx` (nested inside CardGame via Browse/Play toggle)

| Aspect | Value |
|--------|-------|
| Access | Card Deck → "Play" toggle (no separate game entry) |
| Players | Auto-populated from analysis |
| Matching | Play card that shares a feature with top of discard pile |
| Special cards | Mirror Match, Feature Swap, Family Bond, Wild Card |
| Win condition | First to empty hand |
| Card display | Two-line corner badges (category + trait value) |
| Stars | Rarity display above feature badges |
| Responsive | Dynamic hand columns (tablet:6, phone:4) |
| Landscape | Two-column layout (deck+controls left, players right) |
| iOS fullscreen | CSS pseudo-fullscreen (`fixed inset-0 z-[9999]`) for Safari |
| Auto-play | useRef-based timer for stable closures across re-renders |
| Game log | 15-entry limit, turn-prefixed `[N]`, positioned below deck |
| Rotation prompt | Mobile portrait: dismissible "Rotate for Best Experience" |

### 7.2 Memory Match — IMPLEMENTED
**Files:** `src/game/MemoryMatch.jsx`, `MemoryMatchCard.jsx`, `memoryMatchConfig.js`

| Age Group | Cards | Timer | Hints | Penalties | Flip Time |
|-----------|-------|-------|-------|-----------|-----------|
| Kids (3–9) | 4/6/8 | None | Unlimited | None | 3s |
| Teens (10–17) | 8/12/16/20 | Optional | 3 per game | -25 wrong, -5/10s | 1.5s |
| Adults (18+) | 12/16/24/30 | Always on | None | -25 wrong, -10/10s | 1s |

**Feature reveal:** Dramatic 3-phase anticipation overlay at round start:
"Next match" → "Match by..." → sparkle reveal (72px icon + 42px glowing gold label).
Persistent glowing feature banner visible during gameplay.

Matching by shared trait value. +100 base per match, +50 per streak.
Trait description pill shown between photo and name.
Percentage-based photo sizing (scales with grid cell on tablets).
Cross-person pairing: each pair requires two different family members sharing a trait (Fisher-Yates shuffle).
Fallback: same-person pairs only when <3 family members (prevents empty board).

### 7.3 Card Gallery / Print — IMPLEMENTED
**File:** `src/game/CardGame.jsx`

Browse/Play toggle: "Browse" shows gallery view + print layout; "Play" launches FaceMatchGame inline.
Two-line corner badges with trait descriptions, rarity stars.

### 7.4 Face Fusion (Gacha) — IMPLEMENTED
**Files:** `src/game/FaceFusion/FaceFusion.jsx`, `SpinPhase.jsx`, `PickPhase.jsx`, `FusePhase.jsx`

| Phase | Description |
|-------|-------------|
| Spin | 3-reel gacha spinner determines which family members contribute |
| Pick | 8-slot feature builder — assign eyes/nose/smile etc. from different people |
| Fuse | Transformation animation, fusion card reveal, save to collection |

Config: `faceFusionConfig.js` (rarity, combos, age settings)
Storage: `faceFusionStorage.js` (localStorage CRUD for collection)

### 7.5 Feature Catch — DESIGNED (not implemented)
**File:** `docs/FEATURE_CATCH.md`
Arcade game: control family head with tilt/swipe, catch falling features.

### 7.6 Hungry Heads — DESIGNED (partially implemented)
**File:** `docs/HUNGRY_HEADS_DESIGN.md`, `src/game/HungryHeads/`
Three-phase loop: Hunt → Feast → Pop. Tilt/touch control, physics-based.
HuntPhase tilt/touch rewrite completed (touch-primary, tilt-optional).
Fisher-Yates shuffle of person order on mount + reset (prevents same-first-person repetition).

### 7.7 Future Game Modes (from PRD)

| Mode | Target Age | Mechanic | Status |
|------|-----------|----------|--------|
| Race to Empty | Kids (4–8) | First to play all cards | Designed |
| Points Battle | Teens (9–15) | Combo scoring, P values | Designed, values in Card.jsx |
| Feature Poker | Adults (16+) | Bluffing + betting, B values | Designed, awaiting game modes |
| Family Slingshot | All | Physics/Angry Birds style | Concept only |
| Bounce & Match | All | Bubble matching | Concept only |

---

## 8. Emotional Journey & UX

### The 8-Stage Journey

```
DISCOVERY → ANTICIPATION → WOW MOMENT → SHARE/SAVE
    ↓            ↓              ↓            ↓
Upload with   Loading modal   Animated     Keepsake
instant       + suspense      results      cards +
feedback      building        reveal       sharing
    ↓            ↓              ↓            ↓
MONETIZE  → GAMIFICATION → ENGAGEMENT → RETENTION
Premium      Card game      Demo → Play   Analyze
upsells      celebration    conversion    more kids
```

### Home Screen
The home screen is the **front page** where users are introduced to the beta test, given instructions on what to expect, and asked for feedback. It is NOT the upload page.

### Age-Appropriate Tone

| Context | Kids | Teens | Adults |
|---------|------|-------|--------|
| Match found | "AMAZING!" | "Nice!" | "+100" |
| Wrong match | "Oops, try again!" | "Were you even looking?" | "-25" |
| Streak | "UNSTOPPABLE!" | "On fire!" | "x3 Multiplier" |
| Victory | "YOU DID IT!" | "Not bad." | "Score: 1250" |

### Celebration Scale

| Age | Confetti | Trophy | Sound | Replay Label |
|-----|----------|--------|-------|-------------|
| Kids | 150 particles | Yes, big | On | "Play Again!" |
| Teens | 80 particles | Yes | On | "Beat That Score" |
| Adults | 30 particles | No | Off | "New Game" |

### Mobile UX Requirements
- iOS Human Interface Guidelines compliance
- 44pt minimum touch targets
- Native scroll snap for carousels
- `viewport-fit=cover`, CSS custom properties for nav height
- Portrait + landscape support (landscape: compact 52px nav)
- Max width: 480px phone, 768px tablet
- Fullscreen hook for all games (`useFullscreen.js`)
- Dismissible "HOW TO PLAY" instruction banners
- Device-responsive via `useDeviceClass.js` hook

---

## 9. Security & Privacy

### Provable Privacy Claims

| Claim | Evidence | Status |
|-------|----------|--------|
| "No cloud AI processes your photos" | Zero cloud SDKs in requirements.txt; zero external HTTP calls | PROVABLE |
| "Photos are never stored — only measurements" | No `cv2.imwrite()` in backend; gallery stores 512D vectors only | PROVABLE |
| "Photos never shared with third parties" | Zero webhooks, S3 uploads, or external telemetry | PROVABLE |
| "All face analysis runs on local AI models" | MediaPipe (WASM), InsightFace (ONNX), no API keys | PROVABLE |

### NOT Provable Yet

| Claim | Issue | Fix |
|-------|-------|-----|
| "Photos never leave your device" | Images sent to backend over HTTP | Revise marketing language |
| "Data encrypted in transit" | HTTPS not configured in production | Enforce HTTPS (H-02) |

### Security Hardening Plan (8 Items)

| ID | Item | Priority | Status |
|----|------|----------|--------|
| H-01 | Revise marketing claims to match provable facts | P0 | Code done, copy TBD |
| H-02 | Enforce HTTPS in production | P0 | Config placeholder set |
| H-03 | Add API authentication (`X-API-Key` header) | P0 | IMPLEMENTED |
| H-04 | Restrict CORS (explicit origins, not wildcard) | P1 | IMPLEMENTED |
| H-05 | Add GDPR data deletion endpoints | P1 | IMPLEMENTED |
| H-06 | Add CSRF protection | P2 | NOT STARTED |
| H-07 | Switch thumbnails to sessionStorage | P1 | REVERTED — using localStorage + 24h TTL instead |
| H-08 | Add rate limiting (30 req/min on heavy endpoints) | P2 | IMPLEMENTED |

### TARA Threats (16 Identified)

**Part A — Data Bridge (T-01 to T-08)**

| ID | Threat | Risk | Mitigation | Status |
|----|--------|------|------------|--------|
| T-01 | Stale data leakage (wrong family names in games) | HIGH | `clearStaleGameData()` at analysis start | MITIGATED |
| T-02 | localStorage write failure | MEDIUM | try/catch + multi-level fallback | MITIGATED |
| T-03 | Data shape mismatch writer/reader | HIGH | Cross-layer shape contract tests | MITIGATED |
| T-04 | Missing familyRole on cards | MEDIUM | deckBuilder stamps role from familyContext | MITIGATED |
| T-05 | Player name resolution failure | MEDIUM | Priority chain (familyContext → lastResults → groupSnapshot → defaults) | MITIGATED |
| T-06 | Corrupted JSON in localStorage | LOW | try/catch + graceful degradation | MITIGATED |
| T-07 | Feature data loss between analysis and games | MEDIUM | Calibrated → raw → embedding → hash fallback chain | MITIGATED |
| T-08 | Stale thumbnails (blob URLs die on reload) | HIGH | Base64 data URLs in localStorage + 24h TTL | MITIGATED |

**Part B — Privacy & Security (T-09 to T-16)**

| ID | Threat | Risk | Mitigation | Status |
|----|--------|------|------------|--------|
| T-09 | Unencrypted transmission (HTTP) | CRITICAL | HTTPS enforcement in production | PENDING (config only) |
| T-10 | No API authentication | HIGH | `X-API-Key` middleware | IMPLEMENTED |
| T-11 | Invalid marketing claims ("never leaves device") | CRITICAL | Revised provable language | PENDING (copy) |
| T-12 | CORS wildcard (`allow_origins=["*"]`) | HIGH | Explicit origin list | IMPLEMENTED |
| T-13 | No HSTS header | MEDIUM | `Strict-Transport-Security` header | IMPLEMENTED |
| T-14 | Thumbnails persist in localStorage indefinitely | MEDIUM | 24h TTL cleanup | IMPLEMENTED |
| T-15 | No rate limiting on heavy endpoints | MEDIUM | 30 req/min on analyze/enroll/group-snapshot | IMPLEMENTED |
| T-16 | No GDPR data deletion | HIGH | Three deletion endpoints | IMPLEMENTED |

---

## 10. Implementation Status

**Last verified:** 2026-03-21 | **Tests:** 923 FE d2, 932 FE d4, 98 FE d6, 166 BE d3 pass

### Core Features

| Feature | Status |
|---------|--------|
| Photo upload (parents + children) | COMPLETE |
| Face detection + validation (InsightFace + MediaPipe fallback) | COMPLETE |
| 8-feature extraction | COMPLETE |
| Winner determination (5-3 rule) | COMPLETE |
| Order invariance | COMPLETE |
| Results carousel | COMPLETE |
| Keepsake cards (6 templates + Mirror Image) | COMPLETE |
| Group photo analysis | COMPLETE |
| Pairwise 8-feature comparison | COMPLETE |
| Calibrated one-word feature labels (8×5 percentile grid, BE→FE→cards) | COMPLETE |
| Ear occlusion detection (visibility threshold) | COMPLETE |
| Explainable % breakdown (per-feature similarity, measured flag) | COMPLETE |
| Face naming (detection carousel with swipe) | COMPLETE |
| Face thumbnail cropping (canvas → base64) | COMPLETE |
| Individual analysis → game data bridge | COMPLETE |
| Family personalization (familyRole, names in games) | COMPLETE |

### Card Games

| Feature | Status |
|---------|--------|
| Deck builder (calibrated features, phantom member prevention) | COMPLETE |
| Feature Match (card-matching, nested in Card Deck) | COMPLETE |
| Memory Match (3 age groups + feature reveal) | COMPLETE |
| Card Gallery / Print view | COMPLETE |
| Face Fusion (gacha spin + pick + fuse) | COMPLETE |
| Two-line badges (category + trait) across all games | COMPLETE |
| Centralized icons + labels | COMPLETE |
| Stars above badges (not overlapping) | COMPLETE |
| Feature Catch (arcade) | DESIGNED, NOT BUILT |
| Hungry Heads (physics) | PARTIALLY IMPLEMENTED |
| Points Battle / Feature Poker | DESIGNED, NOT BUILT |

### Infrastructure

| Feature | Status |
|---------|--------|
| Pre-commit hook (FE tests + build + BE tests) | COMPLETE |
| API contract schema (kinship_analyze.v1) | COMPLETE |
| Regression tests (14 scenarios, 723 FE tests) | COMPLETE |
| AdaFace IR50 face recognition (CVPR 2022) | COMPLETE |
| Structured feedback survey + gate | COMPLETE |
| Security hardening (auth, CORS, rate limiting, GDPR) | MOSTLY COMPLETE |
| Deployment config (Docker + Caddy + Cloudflare) | COMPLETE |
| Analytics dashboard (`/dashboard?key=` admin-gated, lazy-loaded) | COMPLETE |
| Analytics pipeline (BE JSONL storage, `/analytics/track`, `/analytics/summary`, `/analytics/range`) | COMPLETE |
| E2E tests (Playwright) | PARTIAL (2 specs) |
| Device-responsive layout (phone + tablet + landscape) | COMPLETE |
| Fullscreen hook for all games (iOS pseudo-fullscreen fallback) | COMPLETE |
| Bottom nav: Home + About (Games tab removed — access via results page) | COMPLETE |
| Clear All button (top + bottom of results, clears 20+ localStorage keys) | COMPLETE |

### FamiliTrail — Feature Discovery Board

| Feature | Status |
|---------|--------|
| Board-game SVG canvas (snaking path, 22 nodes, 6 zones) | COMPLETE |
| Tier gating (Free/Plus/Pro/Coming Soon) | COMPLETE |
| "YOU ARE HERE" token with breathing animation | COMPLETE |
| Bottom-sheet tooltip per node (description, CTA, zone cross-sell) | COMPLETE |
| Peek preview (2s timed teaser for locked nodes with personalised data) | COMPLETE |
| Campaign window badges (Mother's Day, Easter) | COMPLETE |
| Homepage links (3 entry points from HomePage.jsx) | COMPLETE |
| Trail progress persistence (remember visited stops) | NOT STARTED |
| Achievement badges (complete all free stops) | NOT STARTED |
| Analytics tracking (trail_node_click events) | NOT STARTED |
| Seasonal zone theming | NOT STARTED |

### FamiliVault — Heritage Trading Cards

| Feature | Status |
|---------|--------|
| Standalone VaultCard (3D tilt, flip, card back, foil, genome strip, holo stamp) | COMPLETE |
| Keepsake VaultCard (print-ready, stat bars, QR placeholder, barcode) | COMPLETE |
| Preview gallery at `/vault` (all rarity tiers, full-size showcase) | COMPLETE |
| Registration in keepsake system (templateRegistry, printProfiles, messageGenerator) | COMPLETE |
| Trail integration (vault_cards node in Keepsake Kingdom zone) | COMPLETE |
| Rarity system (6 tiers, data-driven from biometric distinctiveness) | COMPLETE |
| Heritage type classification (Guardian/Luminary/Artisan/Sovereign/Maverick) | COMPLETE |
| Power stats (PWR/DEF/CHM derived from feature similarities) | COMPLETE |
| Consolidate standalone + keepsake into unified component | NOT STARTED |
| Wire real calibrated percentiles from BE | NOT STARTED |
| Card collection / album page | NOT STARTED |
| Pack opening animation (gacha reveal) | NOT STARTED |
| Share card to social media | NOT STARTED |
| Physical VaultCard printing via Prodigi | NOT STARTED |

---

## 11. UX Fixes Applied (Full History)

### 2026-02-23

| Fix | Files | Trigger |
|-----|-------|---------|
| Fix _left/_right key mismatch in `calibrate_feature()` — eyes, brows, ears now resolve correctly via L+R averaging | calibrated_features.py | Group snapshot showed "Measurement not available" for eyes, brows, ears despite features being visible |
| One-word calibrated labels for all 8 primary features (Narrow/Almond/Balanced/Round/Wide etc.) — BE, FE, cards all aligned | calibrated_features.py, deckBuilder.js, GroupSnapshotSection.jsx, MobileResultsCarousel.jsx | Multi-word labels inconsistent across pipeline; users couldn't verify descriptions against photos |
| Ear occlusion detection — reports "Occluded" when both ears visibility < 0.5 | calibrated_features.py | Ears behind hair/angle should say so, not show fake measurement |
| `measured` flag on feature_similarities + recompute % from measured features only | main.py | Unmeasured features defaulted to 0.5 similarity, inflating percentage with fake data |
| Collapsible "How we calculated this" explainable % breakdown | GroupSnapshotSection.jsx | "The percentage resemblance has to be explainable and adds up in the context of the analysis" |
| Per-feature similarity % shown next to description in feature table (e.g., "Almond 82%") | GroupSnapshotSection.jsx | Feature table lacked quantitative context for each comparison |
| Graceful handling of "Occluded" / "Measurement not available" in FE (shows "—" or "Not visible at this angle") | GroupSnapshotSection.jsx | Broken labels when features couldn't be measured |

### 2026-02-22

| Fix | Files | Trigger |
|-----|-------|---------|
| Clear All button at top + bottom of results; clears 20+ localStorage keys including game/photo data | useKinshipAnalysis.jsx, MobileResultsCarousel.jsx, MobileResultsSection.jsx | "Clear All not visible; stale photos remain after wipe" |
| Memory Match cross-person pairing + Fisher-Yates shuffle; fallback for small families | MemoryMatch.jsx | "Same pictures repeat; matching feels illogical" |
| Feature Match nested inside CardGame via Browse/Play toggle; removed separate game entry | CardGame.jsx, FaceMatchGame.jsx, AppLayout.jsx | "Confusing having Card Deck AND Feature Match as separate games" |
| Feature Match landscape two-column layout + rotation prompt + iOS pseudo-fullscreen | FaceMatchGame.jsx, useOrientation.js (NEW) | "No landscape; iPhone fullscreen button missing; buttons overflow on iPhone 15 Pro" |
| Feature Match game log reorder (below deck), 15-entry limit, turn-prefixed `[N]` messages | FaceMatchGame.jsx | "Game log hard to find; no turn context" |
| Feature Match instructions rewrite (removed UNO references, focus on feature-matching mechanics) | FaceMatchGame.jsx | "Instructions reference UNO which is confusing" |
| Feature Match auto-play fix — useRef for playTurn to avoid stale closures when nested in CardGame | FaceMatchGame.jsx | "Auto simulation button frozen, players not rotating" |
| Games icon removed from bottom nav (Home + About only); games accessed via results page | AppLayout.jsx | "Photos still visible via Games tab after Clear All — users lose confidence in wipe" |
| Hungry Heads Fisher-Yates shuffle of person order on mount + reset | HungryHeads.jsx | "Same person keeps coming up to be fed" |
| Analytics dashboard (`/dashboard?key=fl-admin-2026`), lazy-loaded, admin-gated | AnalyticsDashboard.jsx (NEW), AppLayout.jsx | Internal analytics visibility for beta |
| Free-form comments box added to feedback survey | FeedbackModal.jsx | "There is no free form in the feedback loop" |

### 2026-02-21

| Fix | Files | Trigger |
|-----|-------|---------|
| Memory Match feature reveal (3-phase anticipation overlay with sparkles) | MemoryMatch.jsx | "Make the feature to match very prominent in large fonts sparkles" |
| Persistent glowing feature banner replaces tiny 12px subtitle | MemoryMatch.jsx | Feature prompt too small to notice |

### 2026-02-20

| Fix | Files | Trigger |
|-----|-------|---------|
| AdaFace IR50 model upgrade (ArcFace 2019 → AdaFace CVPR 2022) | adaface_onnx.py (NEW), main.py, docker-compose.yml, Dockerfile | "I need to be able to say the most up to date facial recognition math" |
| Structured feedback survey (12 questions) | FeedbackModal.jsx (NEW) | Need to collect user feedback for beta |
| Feedback gate (require survey before re-access) | AppLayout.jsx, FeedbackModal.jsx | "I want to make giving feedback a provisor for reaccessing the app" |
| Free-form comments in survey | FeedbackModal.jsx, main.py | "There is no free form in the feedback loop" |

### 2026-02-17–18

| Fix | Files | Trigger |
|-----|-------|---------|
| Face Fusion backend morph (Delaunay triangulation + affine warp) | face_morph.py (NEW), main.py, faceCompositor.js | Canvas band-slicing produces Frankenstein faces |
| Photo quality gates (threshold-based assessment + consent gate) | faceQualityAdvice.js (NEW), GroupSnapshotSection.jsx, CardGame.jsx | FE ignores backend quality signals |
| Max 52-card deck + fixed specials + real print size | deckBuilder.js, CardGame.jsx, planConfig.js | Deck sizing inconsistent |
| Smart role suggestions (age/gender detection) | core.py, main.py, GroupSnapshotSection.jsx | Flat dropdown slow to navigate |
| DFMEA bug fixes FM-24 to FM-32 (9 tickets) | 8 files | User-reported bugs rewritten as DFMEA |
| DFMEA robustness FM-11 to FM-23 (13 failure modes) | 6 files + 42 tests | Beta hardening |
| FE resilience — timeout + retry for beta load | kinshipClient.js | No timeout, retry, or abort |
| Deployment config (Docker + Caddy + Cloudflare) | 5 files | No deployment files existed |
| Game instruction banners (HOW TO PLAY) | FaceMatchGame, FeatureCatch, HungryHeads, CardGame | Games lacked instructions |
| Photo upload tips | UploadSection.jsx | No guidance for best photo quality |
| Entertainment-only legal disclaimer | HomePage.jsx | No legal protection from genetic proof claims |

### 2026-02-14

| Fix | Files | Trigger |
|-----|-------|---------|
| Face Fusion MVP (5 batches: spin, pick, fuse, config, storage) | FaceFusion.jsx, SpinPhase.jsx, PickPhase.jsx, FusePhase.jsx, faceFusionConfig.js, faceFusionStorage.js | Game design existed, no code |
| Sticky header + remove navigate(-1) fallback + persist selectedGame to URL | AppLayout.jsx | Navigation broken on all devices |
| Phantom member fix (9 members showing instead of 5) | FaceFusion.jsx, deckBuilder.js | Stale individual data mixing with group data |
| 3 phantom member regression tests | regressionFlows.test.jsx | Prevent recurrence |

### 2026-02-13

| Fix | Files | Trigger |
|-----|-------|---------|
| Device-responsive layout (4 batches) | useDeviceClass.js (NEW), AppLayout.jsx, mobile.css, MemoryMatchCard.jsx, FaceMatchGame.jsx, memoryMatchConfig.js | S22 Ultra tilt broken; 480px cap wastes tablet space; back button broken |
| User testing fixes (5 batches, 8 issues) | hungreyHeadsConfig.js, HuntPhase.jsx, memoryMatchConfig.js, MemoryMatch.jsx, FaceMatchGame.jsx, useFullscreen.js (NEW), KeepsakesModal.jsx, mobile.css | Real-device testing S22 Ultra + iPad |
| Food-obstacle collision + config-driven tilt sensitivity | hungreyHeadsConfig.js, HuntPhase.jsx | P0: Hungry Heads collision broken |
| Viewport-aware card sizing + grid columns | memoryMatchConfig.js, MemoryMatch.jsx, FaceMatchGame.jsx | P1: Cards too large on phone |
| Dismissible "HOW TO PLAY" instruction banners | MemoryMatch.jsx, FaceMatchGame.jsx | P1: No gameplay instructions |
| Shared fullscreen hook for all games | useFullscreen.js, 4 game files | P2: No fullscreen support |
| Responsive keepsakes layout + iPad CSS breakpoint | KeepsakesModal.jsx, mobile.css | P2: Keepsakes broken on iPad |
| Thumbnail persistence revert (sessionStorage → localStorage + 24h TTL) | ThumbnailService.js, FamililookContext.jsx | Blank thumbnails after page reload |
| E2E test overhaul — real contract fixtures | 15 e2e test files | Tests using stale fixture data |
| Security hardening (H-01 to H-08) | config.js, kinshipApi.js, analytics.js, main.py, 10 files for thumbnail migration | TARA T-09 to T-16 |
| Privacy & security audit (TARA v2) | TARA doc, Security Hardening Plan | "Can we claim privacy-first?" |
| Gap closure tests (35 new) + TARA/DFMEA docs | individualModeBridge.test.js, TARA, DFMEA | 4 critical test gaps identified |
| Individual analysis → games bridge (7 files) | useKinshipAnalysis.jsx, deckBuilder.js, FaceMatchGame.jsx, MemoryMatch.jsx, memoryMatchConfig.js, FeatureCatch.jsx, HungryHeads.jsx | Game data never reached from individual analysis |

### 2026-02-12

| Fix | Files | Trigger |
|-----|-------|---------|
| Card feature legibility (two-line badges: category + trait) | FaceMatchGame.jsx, CardGame.jsx, MemoryMatchCard.jsx | "Can't make out what characteristics of features there are" |
| Stars relocated above feature badges | FaceMatchGame.jsx, CardGame.jsx | Stars overlapping corner badges |
| Centralized FEATURE_ICONS + FEATURE_SHORT_LABELS | constants.js, 3 game files | 3 duplicate emoji maps; emoji 8px too small; labels 6px truncated |
| Layout/viewport fixes for phones (portrait + landscape) | index.html, mobile.css, AppLayout.jsx | Beta testers: bottom buttons not visible, landscape broken |
| Header back arrow uses history instead of hard link | AppLayout.jsx | Always navigated to `/` instead of going back |
| Back navigation + preserve state across tab switches | AppLayout.jsx | Data lost on tab switch; replace:true killed history |
| Mirror Image card shows Person B photo | MiniMeCard.jsx | Left-side person showed letter avatar instead of face |
| Fix black card images (bbox normalization + CORS) | GroupSnapshotSection.jsx | Game cards showed black rectangles |
| Crop individual face thumbnails from group photo | GroupSnapshotSection.jsx | No face photos on any card |
| Fix name-picture-feature correspondence on rename | GroupSnapshotSection.jsx | Photos broke when faces renamed |
| Game mode transition race condition | GroupSnapshotSection.jsx, AppLayout.jsx | App glitchy after face exclusion |
| Analysis → CardGame flow connection | MobileResultsCarousel.jsx, MobileResultsSection.jsx, GroupSnapshotSection.jsx, UploadSection.jsx, AppLayout.jsx | No path from analysis results to card game |

### 2026-02-08

| Fix | Files | Trigger |
|-----|-------|---------|
| Centralized feature icons with Unicode escapes | constants.js, FaceMatchGame.jsx, deckBuilder.js | Broken UTF-8 emoji encoding (mojibake) |

### 2026-02-07

| Fix | Files | Trigger |
|-----|-------|---------|
| Detection carousel for group photos (swipe UX) | GroupSnapshotSection.jsx | Name entry hidden at bottom; needed intuitive swipe-to-name |
| MediaPipe same-face bug (all faces returning identical attributes) | attributes_dense.py | max_num_faces=5 too low for 17-face groups |
| Vertical 8-feature cards for group pairwise | GroupSnapshotSection.jsx | Compact 4x2 grid insufficient for feature detail |
| Feature similarities added to group-snapshot pairwise links | main.py | FE checks `has_feature_analysis` but BE wasn't returning it |
| FE unknown feature fix (stop converting "unknown" to "mum") | MobileResultsCarousel.jsx | `getParent()` was inventing parent assignments for unknown features |
| Fix "unknown" to "mum" conversion in data transform | MobileResultsSection.jsx | Data layer `getParent()` defaulted to "mum" |
| Unknown feature handling tests (34 tests) | unknownFeatureHandling.test.js | E2E validation with real BE response data |
| Mock BE response fixtures for FE testing | analysisResults.json, MobileResultsCarousel.test.jsx | Automated testing without user input |
| Restore /kinship/group-snapshot endpoint + 8-feature computation | main.py | 404 on group-snapshot; endpoint missing from main.py |
| InsightFace/MediaPipe fallback detector | main.py | Face detection failed without InsightFace |
| Governance enforcement (mandatory pre-edit checklist) | CLAUDE.md | Previous edit violated governance process |

---

## 12. Outstanding To-Dos

### CRITICAL

| Item | Context | Status |
|------|---------|--------|
| Home button blocked from reaching correct page | Home button at bottom-left doesn't navigate to front page (beta intro/instructions/feedback) | NOT INVESTIGATED |
| Regression test 1 validates wrong assumption | Test assumes `activeTab === "home"` is the upload page; real home is beta intro page | NEEDS REWRITE |
| HTTPS enforcement in production (H-02) | `.env.production` has placeholder URL; no actual HTTPS config | CONFIG ONLY |
| Marketing claims revision (H-01/T-11) | Cannot claim "photos never leave device"; need provable language in app copy | PENDING |

### HIGH

| Item | Context | Status |
|------|---------|--------|
| ~~Face Fusion: canvas-based face compositing~~ | ~~Replaced with backend Delaunay + affine warp~~ | ✅ COMPLETE (2026-02-17) |
| Expand E2E tests for all journeys | Only 2 Playwright specs exist | PARTIAL |
| Verify Electron security settings | contextIsolation, nodeIntegration settings unverified | NOT STARTED |
| CSRF protection (H-06) | No CSRF tokens on mutation endpoints | NOT STARTED |

### MEDIUM

| Item | Context | Status |
|------|---------|--------|
| Single parent UI messaging | Schema supports it, UI uses dual-parent flow | NOT STARTED |
| Sound effect library | No audio in any game | NOT STARTED |
| Score sharing (teens celebration) | No sharing mechanism | NOT STARTED |
| OpenAPI documentation | No API discoverability | NOT STARTED |
| Performance baselines | No profiling | NOT STARTED |

### LOW (FUTURE)

| Item | Context | Status |
|------|---------|--------|
| Feature Catch game (arcade) | Full design doc exists | DESIGNED |
| Points Battle mode (teens) | P values already in Card.jsx | DESIGNED |
| Feature Poker mode (adults) | B values already in Card.jsx | DESIGNED |
| Hungry Heads completion | Hunt + Feast + Pop implemented; person shuffle added; needs polish | PARTIAL |
| Pet comparison full UI | Context ready, UI minimal | PARTIAL |
| Mobile-only beta (Phase 1) | On-device analysis | PLANNED |
| Premium merchandise | Commerce integration | PLANNED |
| Family profiles / session history | Requires persistence layer | PLANNED |
| Leaderboards | Requires persistence | PLANNED |
| PDF export (multi-page family report) | Single-card PNG only today | PLANNED |
| Physical deck printing | Print-on-demand integration | PLANNED |

### GOVERNANCE TO-DOS

| Item | Status |
|------|--------|
| Update `.claude/working_set.txt` for current task | STALE (frozen on security hardening) |
| ~~Log phantom member fix + regression tests~~ | ✅ LOGGED (parent change_log.md) |
| ~~Log Face Fusion MVP~~ | ✅ LOGGED (both change_logs) |
| ~~Log AdaFace upgrade + feedback features~~ | ✅ LOGGED (2026-02-21) |

---

## 13. Roadmap

### NOW — Stability & Polish

- [x] Card feature legibility (two-line badges, trait descriptions)
- [x] Stars relocated above feature badges
- [x] Memory Match gameplay bug fixes
- [x] Memory Match feature reveal (sparkle anticipation overlay)
- [x] Layout/viewport fixes for phones + tablets
- [x] Device-responsive layout (useDeviceClass hook)
- [x] Face Fusion MVP (gacha spin + pick + fuse)
- [x] Face Fusion backend morph (Delaunay + affine warp)
- [x] Phantom member prevention
- [x] Security hardening (auth, CORS, rate limiting, GDPR)
- [x] AdaFace IR50 face recognition upgrade
- [x] Structured feedback survey + gate
- [x] Photo quality gates
- [x] One-word calibrated feature labels (8×5 grid, consistent BE→FE→cards)
- [x] Ear occlusion detection + graceful "Not visible" messaging
- [x] Explainable % breakdown (per-feature similarity, exclude unmeasured)
- [x] Fix _left/_right key mismatch for eyes/brows/ears calibration
- [x] DFMEA robustness (FM-11 to FM-32)
- [x] Deployment config (Docker + Caddy + Cloudflare)
- [ ] Fix home button navigation
- [ ] Fix regression test 1
- [ ] Verify Electron security settings
- [ ] Expand E2E tests

### NEXT — Game Depth (FamiliLook) + FamiliPoker Foundation
- [ ] Feature Catch (arcade game) — FamiliLook
- [ ] Points Battle mode (teens) — FamiliLook
- [ ] Feature Poker mode (adults) — FamiliPoker
- [ ] Feature 21 / Blackjack — FamiliPoker
- [ ] Multiplayer Battle (Top Trumps) — FamiliPoker
- [ ] Sound effect library
- [ ] Score sharing

### GEN 3 — FamiliMatch (Compatibility Product)
- [x] desktop6 (React FE) — Solo Compare, Room UI, Results, 100 tests
- [x] desktop7 (Python BE) — WebSocket rooms, desktop3 integration, 111 tests
- [x] Solo mode functional (reuses /kinship/analyze + /face/morph from desktop3)
- [x] BIPA consent modal + RAM-only photo processing
- [x] Chemistry labels (5 tiers from Feature Twins to Opposites Attract)
- [x] Face morph 50/50 blend for compatibility reveal
- [ ] Duo/Group room E2E testing with real desktop3
- [ ] Production deployment (desktop7 on Hetzner, desktop6 on Vercel)
- [ ] Brand name decision + domain setup

### GEN 4 — FamiliTrail + FamiliVault Hardening

- [x] FamiliTrail: 22-node board, 6 zones, tier gating, peek previews
- [x] FamiliVault: standalone + keepsake card, rarity system, power stats
- [ ] Trail: analytics event tracking (trail_node_click, peek_viewed, tooltip_opened)
- [ ] Trail: progress persistence (mark stops as visited in localStorage)
- [ ] Trail: achievement badges (complete all free stops → congratulation)
- [ ] Trail: A/B test as default landing page vs homepage
- [ ] Vault: consolidate two VaultCard components into one
- [ ] Vault: wire real calibrated percentiles from backend
- [ ] Vault: card collection / album page
- [ ] Vault: pack opening animation (gacha-style)
- [ ] Vault: share card to social media (screenshot export)
- [ ] Vault: physical printing via Prodigi (standard card SKU)
- [ ] Vault: card back on keepsake version

### LATER — Mobile & Commerce

- [ ] Phase 1: Mobile-only beta (on-device analysis)
- [ ] Premium merchandise
- [ ] Family profiles / session history
- [ ] Leaderboards
- [ ] PDF export
- [ ] Physical deck printing

### FUTURE — Expansion

- [ ] Hungry Heads full game
- [ ] Pet comparison full UI
- [ ] Multi-generational family trees
- [ ] Social sharing / viral features
- [ ] FamiliClash: battle cards with attack/defense mechanics
- [ ] FamiliLegacy: premium heirloom cards (radar chart, full 19 sub-features)

---

## 14. QA & Acceptance Criteria

### Smoke Tests
1. Individual: child + parentA + parentB → analyze → winner always A or B (never balanced)
2. Order invariance: swapping parents yields same real winner
3. Individual: multi-face upload → blocked with guidance
4. Group: group photo → face thumbnails → Group Family Card generated
5. Explore details collapsed by default; core results visible
6. Reset clears session fully
7. Card games playable from both individual and group analysis
8. Face Fusion: spin → pick → fuse → card saved

### Regression Guards
- `mumCount + dadCount + unknownCount === 8` always
- FE never invents parent assignments for "unknown" features
- No slot-defaulting: equal similarities → "unknown" vote (not parent A by default)
- Order invariance unit test (backend)
- Phantom member prevention: group data excludes stale individual names
- Thumbnails use base64 data URLs, not blob URLs
- Face names persist across re-analysis (when face count matches)

### Testing Requirements
- `npm run test:run` — 723+ FE unit tests pass
- `npm run build` — Build succeeds
- `npx playwright test` — E2E tests pass
- `python -m pytest tests/` — 100 BE tests pass
- Manual: 8 features display, winner matches majority, no 50/50, order invariance

---

## 15. Monetization

### Tiers

| Tier | Features |
|------|----------|
| Free | Limited analyses, demo deck styles, watermark exports |
| Family | Unlimited analyses + full deck generation + group mode |
| Pro | Advanced insights, premium frames, merchandise, photographer tools |

### FamiliPoker Tiers (Gen 2)

| Tier | Features |
|------|----------|
| Free | Feature Poker (single-player vs AI), demo chip stack |
| Premium | Feature 21, multiplayer rooms, custom card backs, tournament mode |
| VIP | All games, unlimited chip refills, exclusive card cosmetics |

### FamiliMatch Tiers (Gen 3)

| Tier | Features |
|------|----------|
| Free | 3 solo comparisons/day, standard fusion, chemistry label |
| Premium | Unlimited comparisons, HD fusion, save/share, duo rooms |
| Party | Group rooms (3-6 players), pairwise matrix, winner highlight |

### Revenue Streams
- Subscriptions (Family/Pro for FamiliLook, Premium/VIP for FamiliPoker, Premium/Party for FamiliMatch)
- Digital packs (frames/foils/seasonal)
- Print-on-demand decks and framed keepsakes
- B2B licensing for photographers/studios
- Event kiosk mode (later)

---

## 16. Document Index

### Active Documents

| Document | Location | Purpose |
|----------|----------|---------|
| **This file** | `PRD_GOVERNANCE_CONSOLIDATED.md` | Single source of truth |
| GUARDRAILS_CONSOLIDATED.md | Root | All 70 guardrails from both repos |
| CLAUDE.md | Root | Project instructions + pre-edit checklist |
| FAMILILOOK_PRD_CONSOLIDATED.md | `famililook-desktop2/docs/` | Previous consolidated PRD (v2.0) |
| FamiliLook_PRD_v1.2.1 | `layby/docs/` | Original PRD |
| SECURITY.md | `famililook-desktop2/docs/` | Security architecture |
| ENGINEERING_GUARDRAILS.md | `famililook-desktop2/docs/` | No-rewrite rules |
| TARA | `famililook-desktop2/download/ops_reports/` | 16 threats assessed |
| DFMEA | `famililook-desktop2/download/ops_reports/` | 10 failure modes |
| Security Hardening Plan | `famililook-desktop2/download/ops_reports/` | 8 hardening items |

### API Contracts

| Schema | Location |
|--------|----------|
| kinship_analyze.v1 | `contracts/kinship_analyze.v1.schema.json` (3 copies: Agent_1, desktop2, desktop3) |
| faces_detect.v1 | `famililook-desktop3/contracts/` |
| faces_validate.v1 | `famililook-desktop3/contracts/` |
| kinship_enroll.v1 | `famililook-desktop3/contracts/` |
| cards_generate_deck.v1 | `famililook-desktop3/contracts/` |
| group_snapshot.v1 | `famililook-desktop2/src/contracts/` |

### Change Logs

| Log | Location | Scope |
|-----|----------|-------|
| Parent change log | `.claude/change_log.md` | All changes (gitignored, local only) |
| Desktop2 change log | `famililook-desktop2/.claude/change_log.md` | FE implementation batches |
| Ops reports (90+) | `famililook-desktop2/download/ops_reports/` | Timestamped implementation reports |

### Game Design Docs

| Doc | Location | Status |
|-----|----------|--------|
| Memory Match mechanics | `src/game/memorygame.md` | Active |
| Feature Catch design | `docs/FEATURE_CATCH.md` | Ready to build |
| Hungry Heads design | `docs/HUNGRY_HEADS_DESIGN.md` | Partially built |
| Feed the Fam prototypes | `docs/FEED_THE_FAM_PROTOTYPES.md` | Reference |
| Game Ideas | `docs/GAME_IDEAS.md` | Reference |

---

## 17. PRD Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v1.0 | TBD | Baseline PRD |
| v1.1 | 2026-01-06 | Order-invariance requirement + deterministic tie-break |
| v1.2 | 2026-01-15 | Locked deterministic winner rules; embeddings not used for winner; vote aliases |
| v1.2.1 | 2026-01-20 | Clarified platforms (iOS/Android only); defined beta phases; desktop is harness only |
| v2.0 | 2026-02-13 | Consolidated PRD + tech spec + game designs + implementation status + roadmap |
| v3.0 | 2026-02-14 | Consolidated PRD + all UX fixes + all to-dos + security/privacy + governance |
| v3.1 | 2026-02-21 | AdaFace IR50 upgrade; feedback survey + gate; Memory Match feature reveal; Face Fusion backend morph; DFMEA FM-11–FM-32; deployment config; 723 FE + 100 BE tests |
| v3.2 | 2026-02-22 | User feedback fixes: Clear All (20+ keys), Memory Match cross-person pairing, Feature Match nested in CardGame (Browse/Play toggle) + landscape + iOS fullscreen + auto-play fix, Games nav removed, Hungry Heads person shuffle, analytics dashboard |
| v3.3 | 2026-02-23 | One-word calibrated feature labels (8×5 percentile grid) across full pipeline BE→FE→cards; fix _left/_right key mismatch for eyes/brows/ears; ear occlusion detection; explainable % breakdown (per-feature similarity, measured flag, exclude unmeasured); graceful "Not visible" messaging |
| **v3.4** | **2026-02-23** | **Gen 3 FamiliMatch built: desktop6 (36 src files, 100 tests) + desktop7 (7 app files, 111 tests). Solo Compare functional against desktop3. Duo/Group rooms built. BIPA consent, RAM-only photos, chemistry labels, face morph 50/50 blend. Total platform tests: 1,964. DFMEA + TARA created for Gen 3.** |
| **v3.5** | **2026-02-24** | **Product separation & rebranding: FaceCasino → FamiliPoker, FaceMatch (product) → FamiliMatch, FaceMatch (UNO game) → Feature Match. Product feature boundaries table added. Each product now owns distinct features with no overlaps. FamiliPoker monetization tiers added.** |

---

*Document maintained by FamiliLook Engineering Team. Updated 2026-02-24.*
