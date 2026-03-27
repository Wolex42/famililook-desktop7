# FamiliLook Platform Architecture

**Version:** 4.0
**Date:** 2026-03-21 (updated from 2026-03-07)
**Author:** Francis Aroyehun

---

## 1. Platform Overview

Four products built on a shared face analysis engine. All ML inference runs through desktop3. The key architectural split is not between products — it is between the **two analysis modes** the engine can operate in. Each product also connects to external supplier APIs for its physical product layer.

### Brand Hub Layout (famililook.com homepage)

```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│    FAMILILOOK       │    FAMILIUNO        │
│   (top-left)        │   (top-right)       │
│                     │                     │
│  Family analysis    │  Physical Uno-      │
│  6 card games       │  style card packs   │
│  Keepsake prints    │  from your family   │
│                     │  face analysis      │
├─────────────────────┼─────────────────────┤
│                     │                     │
│    FAMILIPOKER      │    FAMILIMATCH      │
│   (bottom-left)     │   (bottom-right)    │
│                     │                     │
│  Casino card games  │  Face compatibility │
│  Feature Poker      │  Solo / Duo / Group │
│  Feature 21         │  + face fusion      │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

The brand hub lives at **famililook.com** (desktop2 root route). Each tile navigates to the relevant product — FamiliLook and FamiliUno are within desktop2; FamiliPoker and FamiliMatch link to their own deployments.

### Engine and Product Map

```
                      SHARED ENGINE (desktop3)
              Face detection · Embeddings · Feature extraction
              Calibration · Kinship analysis · Face morphing
                               │
       ┌───────────┬───────────┼───────────┬───────────┐
       │           │           │           │           │
  FAMILILOOK  FAMILIUNO   FAMILIPOKER  FAMILIMATCH
  (Family     (Physical   (Casino      (Compat-
   Analysis)   Cards)      Games)       ibility)
  d2 + d3      d2 + d3      d4 + d5      d6 + d7
               (same FE)
  Families     Families     Adults       Anyone
  Free/Prem    Freemium     In-app       Freemium

  KINSHIP      KINSHIP     KINSHIP     COMPAT.
  MODE         MODE        MODE        MODE
  (always)   (deck gen)  (deck gen)  (always)

  Analysis     Card deck   Casino      Compat.
  6 games      preview     card games  reveal
  Keepsakes    Uno-pack    —           + fusion
  → Prodigi    → Card API
```

**External API dependencies:**

| Product | External API | Purpose | Status |
|---------|-------------|---------|--------|
| FamiliLook | Prodigi Print API | Physical keepsake prints (mugs, framed cards, cushions, puzzles, T-shirts, etc.) | **LIVE** |
| FamiliLook | Stripe Checkout | Payment processing (single + basket checkout, subscriptions) | **LIVE** |
| FamiliUno | QPMarkets Card API | Physical Uno-style family card packs | **LIVE** (2026-03-26) |
| FamiliPoker | TBD card provider | Physical card decks (premium upsell, future) | Planned |
| All products | Analytics (internal) | Event tracking → desktop3 `/analytics/track` | LIVE |

---

## 2. The Two Analysis Modes

This is the most important architectural concept in the platform. Every call to desktop3 falls into one of two modes, and they use different endpoints, different scoring logic, and serve different product purposes.

### 2.1 Kinship Mode — "Does this child look like these parents?"

**When to use:** There is an expected family relationship. You are looking for inherited traits.

**Inputs:** At least one parent + one child photo (can be a single group photo or individual uploads).

**Desktop3 endpoints activated:**
- `POST /kinship/analyze` — individual upload: parent A + parent B + child(ren)
- `POST /kinship/group-snapshot` — single group photo: detects all faces, runs pairwise kinship

**What the engine does:**
1. Detects faces and extracts 512-dim AdaFace embeddings for all subjects
2. Runs MediaPipe landmark extraction → 8 feature attributes per face
3. Calibrates features against population percentiles (654-face dataset)
4. Runs feature voting: each of 8 features votes for whichever parent it resembles more
5. Applies 5-3 rule: 5+ features → that parent wins; 3-5 range is contested
6. Returns: per-feature winner + inheritance percentages + calibrated labels

**Key invariants (hard-coded, non-negotiable):**
- 8 features always (eyes, eyebrows, smile, nose, face_shape, skin, hair, ears)
- No 50/50 — minimum 51/49 nudge, winner determined by backend
- Order-invariant — swapping parent A and B gives same real winner, different label
- `parent1_count + parent2_count + unknown_count = 8` always

**Outputs feed:**
- FamiliLook results carousel (inheritance breakdown)
- Card deck generation (`/cards/generate-deck`) → all 6 games + physical keepsakes
- Group family photo snapshot with pairwise kinship links between all family members

**Products:** FamiliLook (primary), FamiliPoker (deck generation only)

---

### 2.2 Compatibility Mode — "How similar are these two faces as peers?"

**When to use:** There is NO expected family relationship. You are measuring facial similarity between any two people — romantic partners, friends, strangers, anyone.

**Inputs:** Two or more individual photos, one per person. Each photo is processed independently.

**Desktop3 endpoints activated:**
- `POST /compare/faces` — single-call symmetric peer comparison (Solo + Duo)
- `POST /face/morph` — face blend for the pair (optional, aesthetic reveal)

> **Group mode** (desktop7 orchestrates): still uses `POST /detect` + `POST /embed` per person for the full N×(N-1)/2 pairwise matrix; scoring aggregated in desktop7.

**What the engine does (`/compare/faces`):**
1. Detects faces and extracts 512-dim AdaFace embeddings for both inputs
2. Runs `calibrate_all_features()` on each face → 8 calibrated feature labels per face
3. Computes symmetric cosine similarity: `(1 + cosine(emb_A, emb_B)) / 2` → `[0..1]`
4. Computes feature match fraction across the 8 calibrated labels
5. Blends: `0.6 · embedding_sim + 0.4 · feature_sim` → percentage `[0, 100]`
6. Returns: `percentage`, `chemistry_label`, `chemistry_color`, `feature_comparisons[8]`, `shared_features`, `calibrated_a`, `calibrated_b`

**Contract:** `contracts/compare_faces.v1.schema.json` — FROZEN. Frontend must not re-derive percentage, chemistry_label, or feature_comparisons.

For group (N people): all N×(N-1)/2 pairs are scored by desktop7, highest = winner pair

**Why this is the right model:**
- Symmetric: score(A, B) === score(B, A) — order does not matter
- No kinship assumptions — cosine similarity between peers is semantically correct
- Normalized: `(1 + cosine) / 2` maps the full [-1, 1] range to [0, 1], spreading scores naturally
- Feature matching tests shared traits (same eye shape, same face shape, etc.) not inheritance

**Outputs:**
- Compatibility percentage + chemistry label
- Per-feature side-by-side breakdown
- Face fusion image (morph of the pair)
- For group: full pairwise matrix + winner pair announcement

**Products:** FamiliMatch (all modes — Solo, Duo, Group)

---

### 2.3 Mode Comparison

| Aspect | Kinship Mode | Compatibility Mode |
|--------|-------------|-------------------|
| **Question asked** | Who does this child look like? | How similar are these two people? |
| **Relationship assumed** | Family (parent + child) | None |
| **Upload type** | Individual or group photo | Individual photos per person |
| **Primary endpoint** | `/kinship/analyze` or `/kinship/group-snapshot` | `/compare/faces` (Solo/Duo); `/detect` + `/embed` per person (Group via desktop7) |
| **Scoring runs in** | desktop3 (ML pipeline) | desktop3 (via `/compare/faces`); Group: desktop7 orchestrates |
| **Symmetric?** | No — child/parent roles fixed | Yes — score(A,B) === score(B,A) by construction |
| **Feature comparison** | Calibrated percentile voting (8 features) | Calibrated label matching (8 features, same dataset) |
| **Outputs feed** | Games, keepsakes, cards | Compatibility reveal, face fusion |
| **Products** | FamiliLook, FamiliPoker (deck gen) | FamiliMatch |

---

## 3. Product Definitions

### 3.1 FamiliLook (LIVE)

| Attribute | Value |
|-----------|-------|
| **Repos** | desktop2 (FE), desktop3 (BE) |
| **Audience** | Families with children |
| **Analysis mode** | Kinship only |
| **Core feature** | "Who does your child look like?" — upload parent + child photos, get 8-feature inheritance analysis |
| **Upload types** | Individual (parent A + parent B + child), or single group photo |
| **Digital products** | 6 card games using family face data (MemoryMatch, FeatureMatch, CardGame, FaceFusion, HungryHeads, FeatureCatch) |
| **Physical products** | Keepsake prints via Prodigi (certificates, framed cards, mugs) — NOT card game packs (that is FamiliUno) |
| **Status** | Production (Vercel + Hetzner). 1,022+ FE tests, 166+ BE tests. Commerce LIVE. |
| **Revenue** | Free tier + Premium plans + Prodigi keepsake orders |

### 3.2 FamiliPoker (IN DEVELOPMENT)

| Attribute | Value |
|-----------|-------|
| **Repos** | desktop4 (FE), desktop5 (BE game server) |
| **Audience** | Adults (18+) |
| **Analysis mode** | Kinship (deck generation only — host runs analysis before entering the casino) |
| **Core feature** | Casino-style card games using family face data — Feature Poker, Feature 21 (Blackjack) |
| **Secondary** | Multiplayer rooms, chip economy, tournament mode |
| **Status** | desktop4: 463 unit tests, 42 e2e. desktop5: WebSocket server complete, 37 tests |
| **Revenue** | In-app purchases (chip packs, card cosmetics, tournament entry) |

**DECISION (2026-03-27):** FamiliPoker will be merged into desktop2 as `/poker` route. FamiliMatch stays independent at `match.famililook.com`. Session token pattern (`POST /session/create`) deferred to mobile app phase.

### 3.3 FamiliMatch (IN DEVELOPMENT)

| Attribute | Value |
|-----------|-------|
| **Repos** | desktop6 (FE), desktop7 (BE room server) |
| **Audience** | Singles, couples, friend groups — no family relationship assumed |
| **Analysis mode** | Compatibility only |
| **Core feature** | Facial compatibility — upload selfie(s), get chemistry score + face fusion + feature breakdown |
| **Modes** | Solo (1 person, 2 photos), Duo (2 people, room + simultaneous reveal), Group (3–6 people, pairwise matrix) |
| **Status** | desktop6: Solo/Duo/Group FE complete, 98 tests, build clean. desktop7: WebSocket server complete, 111 tests |
| **Revenue** | Freemium (free comparisons, premium: unlimited + HD fusion + save/share) |

### 3.4 FamiliUno (LIVE)

| Attribute | Value |
|-----------|-------|
| **Repos** | desktop2 (FE — within same app as FamiliLook), desktop3 (BE — shared engine for deck gen) |
| **Audience** | Families who want a physical card game from their face data |
| **Analysis mode** | Kinship (card deck generation only — borrows generated deck from FamiliLook session) |
| **Core feature** | "Turn your family face analysis into a real Uno-style card game you can order and play" |
| **Flow** | 1. Run FamiliLook analysis → 2. Generate card deck (`/cards/generate-deck`) → 3. Preview card designs (virtual card simulation) → 4. Order physical Uno-style card pack via card supplier API |
| **Key distinction from FamiliLook** | FamiliLook keepsakes = individual prints (Prodigi — certificates, mugs, framed photos). FamiliUno = full physical Uno card game set with your family faces printed as the card artwork |
| **Card supplier API** | QPMarkets — LIVE since 2026-03-26. Full pipeline: Stripe → webhook → CardPrintClient → QPMarkets API |
| **Status** | **LIVE** (2026-03-26) — FE complete, BE ordering pipeline complete, QPMarkets integration live |
| **Revenue** | Per-order revenue (one-time purchase per card pack); potential subscription for ongoing reprints |

**FaceMatch onboarding wizard:** FamiliUno includes a 5-step interactive onboarding wizard (`FaceMatchOnboarding`) teaching physical card deck rules: card anatomy, matching mechanics, feature modes (2/3/4 features per card), special cards, and winning conditions. Free tier: 3 cards, 10 turns, no specials. Plus tier: full 7-card hands, all specials, unlimited turns. The upgrade CTA connects to the Plus subscription and deck ordering flow.

### 3.5 FamiliTrail (BUILT — desktop2)

| Attribute | Value |
|-----------|-------|
| **Repo** | desktop2 (FE — within same app as FamiliLook) |
| **Route** | `/trail` |
| **Audience** | All users — discovery + upgrade funnel |
| **Purpose** | Board-game style product map showing all FamiliLook features as stops on a winding trail |
| **Status** | **Built and live** — routed, linked from homepage (3 entry points), build-bundled as `TrailHomePage-*.js` |

**What it is:** A gamified feature discovery page. Users see a snaking SVG board-game path with 22 stops across 6 themed zones. Each stop represents a product feature. Tapping a stop opens a bottom-sheet with description, CTA, zone cross-sell, and upgrade nudge. Locked stops show a 2-second "peek preview" teaser with personalised data from localStorage.

**Architecture:**

```
TrailHomePage.jsx (page)
    ├── FamilyTrailCanvas.jsx (SVG board — snaking path, zone bands, particles, "YOU" token)
    ├── TrailTooltip.jsx (bottom-sheet detail overlay for each node)
    ├── PeekPreview.jsx (2-second timed teaser for locked/coming-soon nodes)
    └── trailData.js (22 nodes, 6 zones, tier config, layout math)
```

**6 Zones:**

| Zone | Theme | Colour | Stops |
|------|-------|--------|-------|
| Discovery Zone | Core analysis | Teal | Upload, 8-Feature Scan, Parent vs Child, Group Photo, Pet Compare |
| Keepsake Kingdom | Physical products | Amber | Cards, Deck, Downloads, Print & Order, FamiliVault |
| Game Arcade | Digital games | Purple | Memory Match, Face Fusion, Hungry Heads, Feature Catch |
| Casino Floor | FamiliPoker | Green | Feature Poker, Feature 21, Multiplayer Battle |
| Chemistry Lab | FamiliMatch | Pink | Solo Compare, Duo Room, Group Party |
| Coming Soon Island | Planned features | Grey | Uno Multiplayer |

**Tier gating (22 stops):**
- **Free:** 8 stops (core analysis, basic games, downloads)
- **Plus:** 6 stops (group photo, full deck, print ordering, arcade, duo room)
- **Pro:** 5 stops (FamiliVault, poker, blackjack, multiplayer, group party)
- **Coming Soon:** 2 stops (FamiliUno)
- **"YOU ARE HERE" token** — bouncing arrow indicates last accessible stop for current plan

**Campaign windows:** Mother's Day UK (2026-03-22), Easter (2026-04-05), Mother's Day US (2026-05-10) — campaign badges shown in header when within window.

**Remaining work:**

| Task | Status | Priority |
|------|--------|----------|
| Core trail board (SVG, zones, nodes, path) | **Done** | — |
| Tier gating + "YOU" token | **Done** | — |
| Bottom-sheet tooltip (per-node detail) | **Done** | — |
| Peek preview (2s teaser for locked nodes) | **Done** | — |
| Homepage links (3 entry points) | **Done** | — |
| Campaign window badges | **Done** | — |
| Trail progress persistence (remember visited stops) | **Done** (2026-03-13, tested 2026-03-23) | — |
| Analytics tracking (trail_node_click events) | **Done** (2026-03-13, tested 2026-03-23) | — |
| Route fix: 17 broken/weak nodes fixed (deep-links, external URLs, BrandHub 4-tile) | **Done** (2026-03-23, CR-0001) | — |
| Test coverage: 44 test cases across 6 files | **Done** (2026-03-23, CR-0001) | — |
| Achievement badges (complete all free stops) | Not started | P2 |
| A/B test: trail as default landing vs current homepage | Not started | P2 |
| Animated trail completion (confetti/celebration) | Not started | P3 |
| Dynamic node unlock animation | Not started | P3 |
| Seasonal zone theming (Easter eggs, Christmas snow) | Not started | P3 |

---

### 3.6 FamiliVault (BUILT — desktop2)

| Attribute | Value |
|-----------|-------|
| **Repo** | desktop2 (FE — two components: standalone preview + keepsake template) |
| **Routes** | `/vault` (preview gallery), keepsake modal (print ordering) |
| **Audience** | Premium users (Pro tier) — collectors, gifters |
| **Purpose** | Heritage trading cards with real biometric data — collector-grade with rarity tiers, holographic effects, and power stats |
| **Status** | **Built** — both components working, registered in keepsake system, trail-linked |

**What it is:** Premium collectible trading cards generated from real face analysis data. Each card has a deterministic rarity tier (based on biometric distinctiveness), power stats (PWR/DEF/CHM derived from feature similarities), a DNA genome strip, holographic foil effects, and a unique serial number.

**Architecture — Two Components:**

```
1. STANDALONE PREVIEW (interactive gallery)
   src/components/vault/VaultCard.jsx      — Full card: 3D tilt, flip, card back, holo stamp
   src/components/vault/vaultCardData.js   — Schema: rarity, heritage types, builders
   src/pages/VaultPreview.jsx              — Gallery at /vault with all rarity tiers

2. KEEPSAKE TEMPLATE (print-ready for Prodigi)
   src/components/keepsakes/templates/ChildCards/VaultCard.jsx — Print version: foil shimmer, stat bars, QR, barcode
   Registered in: templateRegistry.js, printProfiles.js, messageGenerator.js, KeepsakesModal.jsx
```

**Rarity System (data-driven, not random):**

| Tier | Standalone | Keepsake | Trigger |
|------|-----------|----------|---------|
| Common | ✓ | ✓ | Low avg feature scores |
| Uncommon | ✓ | ✓ | 1+ features ≥80th percentile |
| Rare | ✓ | ✓ | 2+ features ≥80th |
| Epic | ✓ | — | 3.5+ distinctiveness score |
| Ultra Rare | — | ✓ | 4+ features ≥80th |
| Legendary | ✓ | ✓ | 6+ features ≥80th |
| Mythic | ✓ | — | 4.5+ distinctiveness score |

**Heritage Types (standalone version):**
- **Guardian** — structural features dominate (face shape, nose, ears)
- **Luminary** — expressive features dominate (eyes, smile, brows)
- **Artisan** — fine detail features (skin, hair, ear shape)
- **Sovereign** — balanced across all 8 features
- **Maverick** — high variance, unique from both parents

**Power Stats (keepsake version):**
- **PWR** (eyes + smile + hair) — striking features
- **DEF** (face_shape + ears + nose) — structural solidity
- **CHM** (skin + eyebrows + smile) — warmth & expressiveness

**Remaining work:**

| Task | Status | Priority |
|------|--------|----------|
| Standalone VaultCard (3D tilt, flip, foil, genome strip) | **Done** | — |
| Keepsake VaultCard (print-ready, stat bars, QR, barcode) | **Done** | — |
| Preview gallery at /vault | **Done** | — |
| Registration in keepsake system | **Done** | — |
| Trail integration (vault_cards node) | **Done** | — |
| Consolidate two VaultCard versions into one unified component | Not started | P1 |
| Wire real calibrated percentiles from BE (currently uses similarity as proxy) | Not started | P1 |
| Card back on keepsake version (standalone has it, keepsake doesn't) | Not started | P2 |
| Flip interaction on keepsake version | Not started | P2 |
| FamiliClash (battle cards — planned concept) | Not started | P3 |
| FamiliLegacy (premium heirloom cards — planned concept) | Not started | P3 |
| Pack opening animation (gacha-style reveal) | Not started | P2 |
| Card collection / album page | Not started | P2 |
| Share card to social media (screenshot export) | Not started | P1 |
| Physical VaultCard printing (Prodigi standard card SKU) | Not started | P1 |

---

## 4. Shared Engine (desktop3)

The analysis backend runs on Hetzner CPX22 (2 vCPU, 4 GB RAM, Helsinki). All three products call it; none of them duplicate ML logic.

```
                    desktop3 (Python FastAPI) — Port 8008
                    ┌─────────────────────────────────────────┐
                    │  ML Models (loaded at startup, ~2 GB)   │
                    │  ├── InsightFace buffalo_l (detection)  │
                    │  ├── AdaFace IR50 (512-dim embeddings)  │
                    │  ├── ArcFace (fallback)                 │
                    │  └── MediaPipe Face Mesh (468 landmarks)│
                    │                                         │
                    │  KINSHIP ENDPOINTS                      │
                    │  ├── POST /kinship/analyze              │
                    │  │   parent A + parent B + child(ren)  │
                    │  │   → 8-feature inheritance + winner  │
                    │  └── POST /kinship/group-snapshot       │
                    │       single group photo                │
                    │       → all faces detected + pairwise  │
                    │         kinship links                   │
                    │                                         │
                    │  COMPATIBILITY ENDPOINT                 │
                    │  ├── POST /compare/faces               │
                    │  │   → symmetric peer comparison      │
                    │  │   → %, chemistry, 8-feat breakdown │
                    │  │   (FROZEN contract v1)             │
                    │  └── POST /face/morph                  │
                    │       → blended face image            │
                    │                                        │
                    │  ANALYSIS PRIMITIVES                   │
                    │  ├── POST /detect                      │
                    │  │   → face validation + attributes   │
                    │  └── POST /embed                       │
                    │       → 512-dim embedding vector      │
                    │                                         │
                    │  SHARED UTILITIES                       │
                    │  ├── POST /attributes                   │
                    │  ├── POST /cards/generate-deck          │
                    │  ├── POST /kinship/card-features        │
                    │  └── GET  /analytics/*, /health         │
                    └─────────────────────────────────────────┘
```

**Endpoint usage by product:**

| Endpoint | FamiliLook | FamiliPoker | FamiliMatch |
|----------|:----------:|:-----------:|:-----------:|
| `/kinship/analyze` | Yes | No | **No** |
| `/kinship/group-snapshot` | Yes | No | **No** |
| `/compare/faces` | No | No | **Yes** (Solo + Duo) |
| `/detect` | Yes | Yes (deck gen) | Yes (Group via desktop7) |
| `/embed` | Yes | Yes (deck gen) | Yes (Group via desktop7) |
| `/attributes` | Yes | Yes (deck gen) | Via /detect |
| `/face/morph` | Yes (FaceFusion game) | No | Yes (fusion reveal) |
| `/cards/generate-deck` | Yes | Yes | No |
| `/kinship/card-features` | Yes | Yes | No |
| `/analytics/track` | Yes | Yes | Yes |
| `/orders/keepsake` | Yes | No | No |
| `/orders/images/{id}.png` | Yes | No | No |
| `/payments/create-checkout-session` | Yes | No | No |
| `/payments/create-basket-checkout` | Yes | No | No |
| `/webhooks/stripe` | Yes | No | No |
| `/webhooks/print-status` | Yes | No | No |

> **FamiliMatch uses `POST /compare/faces` for Solo and Duo mode.** The endpoint runs all ML inference inside desktop3: AdaFace embeddings, `calibrate_all_features()` for 8 calibrated feature labels per face, symmetric cosine similarity `(1 + cosine) / 2`, and blended scoring `0.6 · emb + 0.4 · feat`. An earlier design considered per-person `/detect` + `/embed` with client-side scoring — this was superseded by the dedicated endpoint, which is symmetric by construction and governed by a frozen contract (`contracts/compare_faces.v1.schema.json`). Group mode still uses per-person primitives orchestrated by desktop7 for the full N×(N-1)/2 pairwise matrix.

---

## 5. Product Architectures

### 5.1 FamiliLook (desktop2 + desktop3)

```
Browser (desktop2 / React + Vite / Vercel)
    │
    │  INDIVIDUAL UPLOAD
    │  POST /kinship/analyze
    │  parent_a, parent_b, children[]
    │
    │  GROUP PHOTO
    │  POST /kinship/group-snapshot
    │  group_photo (single image, N faces)
    │
    ▼
Caddy (api.famililook.com → :8008)
    ▼
desktop3 → kinship pipeline → 8-feature result + calibrated labels
    │
    ▼
Browser stores in localStorage:
    fl:familyData     → inheritance results
    fl:thumbnails     → face crops (base64)
    fl:deck           → card deck for games
    │
    ▼
6 Games: MemoryMatch, FeatureMatch, CardGame, FaceFusion, HungryHeads, FeatureCatch

FamiliLook keepsakes (Prodigi): certificates, framed photos, mugs
    │
    ▼ (separate product — FamiliUno)
FamiliUno card ordering (Card Supplier API): full Uno-style physical card game set
```

**Key invariants enforced here:** 8 features, 5-3 winner rule, no 50/50, order-invariant.

**FamiliUno deck button in results carousel:** Each child result card in `MobileResultsCarousel` includes a "Play FamiliUno" button that navigates to `/uno?from=results` with all family data loaded. This is the primary cross-sell entry point from kinship results into the card ordering flow.

**Cross-product back navigation (`?from=` pattern):** All navigation to `/uno` includes a `?from=` query parameter (`results`, `trail`, `hub`, `home`) so the back button returns users to their origin. The same pattern applies to the future `/poker` route. This ensures deep-linked product transitions always have a coherent return path.

#### 5.1.1 Parent-Pair Exclusion (Couple Gate)

Parents (Mum, Dad, Partner) are **excluded from pairwise comparison with each other** by default. This prevents the socially unwanted scenario of husbands/wives being "scored" against each other in family or group contexts.

**How it works:**

```
GroupSnapshotSection.jsx
    │
    ├── faceRelationships[] state — user labels each face (Mum, Dad, Child, etc.)
    │
    ├── PARENT_ROLES set (constants.js) — { "Mum", "Dad", "Partner" }
    │
    ├── parentNameSet (useMemo) — builds Set of face names with parent roles
    │
    ├── Label Gate — if group mode has faces but no parent labels assigned:
    │       shows amber prompt "Tag the parents first"
    │       blocks pairwise results until parents are labelled
    │
    ├── Pairwise filter — excludes pairs where BOTH members are in parentNameSet
    │       unless includeParentComparison toggle is ON
    │
    └── includeParentComparison toggle — green shield banner with Include/Exclude button
            defaults to OFF (parents excluded)
            user can opt in to see parent-parent pairs
```

**UploadSection couple nudge:** When exactly 2 parents are uploaded with no children, a "Want to compare these two instead?" prompt appears with a "Try FamiliMatch" redirect button (uses `VITE_FAMILIMATCH_URL` env var).

**Design rationale:** Family kinship analysis answers "who does the child look like?" — comparing spouses against each other is not the product's intent. Users who want peer-to-peer comparison are redirected to FamiliMatch, which uses `/compare/faces` (symmetric compatibility mode).

---

### 5.2 FamiliPoker (desktop4 + desktop5)

```
Host phone (desktop4)
    │
    │  1. Run kinship analysis (calls desktop3 — same as FamiliLook)
    │     → gets deck in localStorage
    │
    │  2. Open Poker Lobby → create room → share 4-digit code
    │
    ▼
desktop5 Game Server (WebSocket, Port 8020)
    │  Host sends deck data on start
    │  Server shuffles, deals hands, manages game state (RAM only)
    │  No photos ever sent to desktop5
    │
    ▼
Guest phones (desktop4) — join via room code, receive cards from server
```

desktop5 is a pure relay — it never calls desktop3. All ML work happens in the host's browser before the room opens.

---

### 5.3 FamiliMatch (desktop6 + desktop7)

```
                    SOLO MODE
                    (1 person, 2 photos — no room needed)

    Browser (desktop6)
        │
        │  Photo A + Photo B uploaded
        │
        ├── POST /compare/faces (A + B)
        │       → percentage, chemistry_label, chemistry_color
        │       → feature_comparisons[8], shared_features
        │       → calibrated_a, calibrated_b
        │       (Backend does ALL scoring — no client-side computation)
        │
        ├── POST /face/morph (A + B) → fusion image (optional reveal)
        │
        ▼
    ResultsStory (5-card reveal in browser)
    Card 1: Score + chemistry label
    Card 2: Strongest matching feature
    Card 3: Biggest contrast feature
    Card 4: Full 8-feature breakdown
    Card 5: Face fusion reveal


                    DUO MODE
                    (2 people, simultaneous reveal)

    Player A (desktop6) ←─── WebSocket ──→ desktop7 ←─── WebSocket ──→ Player B (desktop6)
                                               │
                               ┌───────────────┼───────────────┐
                               │ POST /detect (A)              │
                               │ POST /detect (B)              │
                               │ POST /embed (A)               │
                               │ POST /embed (B)               │
                               │ Pairwise compatibility scored │
                               │ POST /face/morph (A + B)      │
                               └───────────────────────────────┘
                                               │
                               3...2...1 countdown → simultaneous reveal


                    GROUP MODE
                    (3–6 people, pairwise matrix)

    All players upload → desktop7 collects all photos
        │
        ├── POST /detect (each person)
        ├── POST /embed (each person)
        │
        │  All N×(N-1)/2 pairs scored:
        │  e.g. 4 people → 6 pairs (A-B, A-C, A-D, B-C, B-D, C-D)
        │
        ├── Highest-scoring pair = winner
        ├── POST /face/morph (winner pair only)
        │
        ▼
    GroupMatrix (progressive reveal: lowest → highest → winner)
```

**desktop7 WebSocket protocol:**

| Client → Server | Payload | Effect |
|-----------------|---------|--------|
| `create_room` | `{ player_name, room_type }` | Room created, code issued |
| `join_room` | `{ room_code, player_name }` | Player added to room |
| `upload_photo` | `{ photo: base64 }` | Photo held in RAM |
| `ready` | `{}` | When all ready → analysis starts |
| `leave` | `{}` | Player removed |

| Server → Client | Payload | Purpose |
|-----------------|---------|---------|
| `room_created` | `{ room_code }` | Room ready |
| `player_joined` | `{ player_name, count }` | Lobby update |
| `all_photos_in` | `{}` | Analysis starting |
| `analyzing` | `{ step, total_steps }` | Progress |
| `countdown` | `{ seconds }` | Reveal countdown |
| `reveal` | `{ compatibility, features, fusion_image }` | Duo results |
| `group_reveal` | `{ pairs, winner_pair, winner_score }` | Group results |

---

## 6. Scoring Systems

### 6.1 Kinship Scoring (FamiliLook / FamiliPoker deck gen)

**Goal:** Determine which parent a child resembles more, feature by feature.

```
For each of 8 features:
  similarity_to_parent1 = compare(child_feature, parent1_feature)
  similarity_to_parent2 = compare(child_feature, parent2_feature)

  if |sim_p1 - sim_p2| < VOTE_MARGIN:
      vote = "unknown"
  elif sim_p1 > sim_p2:
      vote = "parent1"
  else:
      vote = "parent2"

Winner = parent with ≥5 feature votes (5-3 rule)
Display percentage = feature_vote_count / 8, nudged to avoid 50/50
```

Calibrated percentile labels (e.g. "Almond", "Round", "Broad") come from the 654-face population dataset. These labels are designed for inheritance detection — not peer comparison.

### 6.2 Compatibility Scoring (FamiliMatch)

**Goal:** Measure similarity between any two peers symmetrically.

```
# All runs inside desktop3 — POST /compare/faces
# Backend computes atomically and returns the result:

embedding_A = AdaFace(photo_A)           # 512-dim IR50 vector
embedding_B = AdaFace(photo_B)

embedding_similarity = (1 + cosine(emb_A, emb_B)) / 2    # [0..1, symmetric]

calibrated_A = calibrate_all_features(photo_A)  # 8 feature labels
calibrated_B = calibrate_all_features(photo_B)
feature_similarity = matched_labels / 8          # [0..1]

compatibility_score  = 0.6 · embedding_similarity
                     + 0.4 · feature_similarity

percentage           = round(compatibility_score × 100)   # integer [0, 100]
```

Feature labels use the same `calibrate_all_features()` pipeline as kinship mode — population-percentile calibrated labels (e.g. "Round Eyes", "Arched Brows", "Oval Face"). Matching is exact label equality (case-insensitive). The frontend receives the blended `percentage` directly and must not re-derive it. Contract: `contracts/compare_faces.v1.schema.json`.

### 6.3 Chemistry Labels (shared across all compatibility displays)

| Score | Label | Color |
|-------|-------|-------|
| 85–100% | Feature Twins | Gold `#FFD700` |
| 70–84% | Magnetic Match | Purple `#8B5CF6` |
| 55–69% | Complementary Pair | Blue `#3B82F6` |
| 40–54% | Interesting Contrast | Teal `#14B8A6` |
| 0–39% | Opposites Attract | Orange `#F97316` |

---

## 7. Server Infrastructure

### 7.1 Hetzner CPX22 — Current Layout

```
89.167.113.178 (Helsinki, EU)
2 vCPU · 4 GB RAM · 80 GB SSD

Caddy (Port 443 / 80)
├── api.famililook.com/*         → desktop3 :8008
├── api.famililook.com/ws/game/* → desktop5 :8020
└── api.famililook.com/ws/match/*→ desktop7 :8030

desktop3 (Analysis Engine)    ~2.0 GB RAM  (ML models loaded at startup)
desktop5 (FamiliPoker WS)     ~0.2 GB RAM  (pure relay, rooms in RAM)
desktop7 (FamiliMatch WS)     ~0.2 GB RAM  (photo buffers + analysis orchestration)
OS + Caddy                    ~0.4 GB RAM
Headroom                      ~1.2 GB RAM
```

### 7.2 Frontend Hosting

| Product | Host | Branch | Domain |
|---------|------|--------|--------|
| FamiliLook (desktop2) | Vercel | `production` | famililook.com |
| FamiliPoker (desktop4) | Vercel | `production` | famililook-desktop4.vercel.app |
| FamiliMatch (desktop6) | Vercel | `production` | famililook-desktop6.vercel.app |

### 7.3 Scaling Path

1. **Vertical first**: CPX32 (4 vCPU, 8 GB) doubles desktop3 throughput
2. **Split**: dedicated ML VPS for desktop3, lightweight relay VPS for desktop5 + desktop7
3. **Horizontal**: multiple desktop3 instances behind load balancer; sticky sessions for WS servers

---

## 8. Data Flow & Privacy

### 8.1 Photo Lifecycle

```
FamiliLook (Kinship):
  Browser uploads → desktop3 processes → result returned → server forgets
  Browser stores: calibrated labels + thumbnail crops in localStorage (fl:*)
  Card deck built from labels (no raw embeddings stored anywhere)

FamiliPoker:
  Host runs kinship analysis (same as above, data in localStorage)
  Host sends card metadata (not photos) to desktop5
  desktop5 holds deck in RAM during game → room closes → gone

FamiliMatch (Compatibility):
  Solo/Duo: browser → POST /compare/faces → desktop3 does all ML → result returned → photos never leave request
  Group: players upload selfies → desktop7 holds in RAM → calls desktop3 (/detect, /embed per person)
         desktop3 extracts embeddings → returned to desktop7 → photos discarded
         desktop7 runs pairwise matrix → results broadcast → room closes → everything gone
  No photos, no embeddings, no scores stored anywhere after room close
```

### 8.2 What's Stored Where

| Data | Browser localStorage | Server RAM (transient) | Server Disk |
|------|:-------------------:|:---------------------:|:-----------:|
| Raw photos | No | During analysis only | Never |
| Thumbnails (base64) | FamiliLook only | During game room | Never |
| Feature labels | FamiliLook (fl:familyData) | During room | Never |
| Embeddings | Never | During analysis only | Never |
| Card deck | FamiliLook (fl:deck) | During game room | Never |
| Fusion image | Shown in UI only | Generated on request | Never |
| Compatibility score | FamiliMatch: UI only | During room | Never |
| Analytics events | No | No | JSONL (anonymised) |

**COPPA 13+ age gate:** A `CoppaAgeGate` component (in `AgeGateModal.jsx`) fires before the first photo upload across all products. Confirmation is stored in localStorage (`fl:age-confirmed-13`). This gates all biometric processing — no face analysis endpoints are called until the user confirms they are 13 or older.

**GDPR forget-me endpoint:** `POST /data/forget-me` covers 6 data stores: gallery (cleared), analytics (IP hash purge), feedback (IP + email purge), subscribers (email purge), orders (anonymised for UK tax retention), and ambassador grants (email purge). This is the single endpoint for full GDPR right-to-erasure compliance.

---

## 9. Commerce Layer (LIVE — March 2026)

### 9.1 Architecture Overview

```
Browser (desktop2)
    |
    |-- KeepsakesModal.jsx -----> Template Preview (live render)
    |       |                      |-- useKeepsakeData() (single child)
    |       |                      |-- useFamilyKeepsakeData() (all children)
    |       |                      |-- usePersonalizedMessage() (LLM)
    |       |
    |-- BasketContext.jsx -------> Multi-item cart (localStorage fl:basket)
    |-- CurrencyContext.jsx -----> 8 countries, formatPrice()
    |-- BasketDrawer.jsx --------> Checkout UI (shipping + Stripe)
    |-- OrderModal.jsx ----------> Single-item Stripe checkout
    |
    v
POST /payments/create-basket-checkout (desktop3)
    |-- Validates product_type against PRODUCT_PRICES_PENCE
    |-- Creates per-item order records
    |-- Creates Stripe Checkout Session (line_items[])
    |-- Returns session URL → redirect to Stripe
    |
    v
Stripe Checkout (hosted page)
    |-- Customer pays
    |-- Webhook → POST /webhooks/stripe
    |       |-- Verifies signature (construct_event)
    |       |-- Marks orders as paid
    |       |-- Triggers Prodigi order creation
    |
    v
POST /orders/keepsake (desktop3 → Prodigi)
    |-- route_order_to_vendor() → ProdigiClient
    |-- Uploads image URL: GET /orders/images/{id}.png
    |-- Prodigi prints + ships to customer address
    |
    v
POST /webhooks/print-status (Prodigi → desktop3)
    |-- HMAC signature verification
    |-- Updates order status in DB
```

### 9.2 Keepsake Template System

```
templateRegistry.js ─── Product → Template Component mapping
    |
    |-- PRODUCT_TEMPLATE_REGISTRY: { product_type → { component, styles[], requiresFamilyData } }
    |-- TEMPLATE_STYLES: { style_id → { label, variant, thumbnail } }
    |
    |-- Lazy-loaded components (React.lazy):
    |       KeepsakeCertificate, TradingCardTemplate, VaultCard,
    |       MugTimelineTemplate, FamilyMugTemplate, StandardCardTemplate,
    |       PostcardTemplate, etc.
    |
    |-- requiresFamilyData flag → switches data source to useFamilyKeepsakeData()
    |
printProfiles.js ─── Product specs for print production
    |-- PRODUCT_TYPES enum (14 product types)
    |-- PRODUCT_SPECS: { dimensions, dpi, price, vendors[], fileFormat }
    |
printExport.js ─── HTML-to-PNG export pipeline
    |-- html2canvas renders template → canvas → PNG blob
    |-- PNG uploaded to backend → served at /orders/images/{id}.png
```

### 9.3 Product Catalogue

| Product | Price (GBP) | Prodigi SKU | Template | Family Data? |
|---------|-------------|-------------|----------|:------------:|
| Fine Art Print (8x10) | 9.99 | GLOBAL-FAP-8X10 | KeepsakeCertificate | No |
| Fine Art Print (16x20) | 19.99 | GLOBAL-FAP-16x20 | KeepsakeCertificate | No |
| Framed Canvas (12x16) | 34.99 | GLOBAL-FRA-SLIMCAN-12x16 | KeepsakeCertificate | No |
| Ceramic Mug | 14.99 | GLOBAL-MUG-W | MugTimelineTemplate | No |
| Family Mug Set | 27.99 | GLOBAL-MUG-W (x2) | FamilyMugTemplate | **Yes** |
| T-Shirt | 19.99 | GLOBAL-TEE-GIL-5000 | — | No |
| ~~Baby Bodysuit~~ | ~~14.99~~ | ~~GLOBAL-TEE-GIL-5000~~ | — | **Removed** |
| Cushion | 24.99 | GLOBAL-CUSH-16X16-CAN-DUAL | — | No |
| Jigsaw Puzzle (252pc) | 24.99 | JIGSAW-PUZZLE-252 | — | No |
| Greeting Card | 7.99 | CLASSIC-GRE-FEDR-7X5-BLA | StandardCardTemplate | No |
| Postcard | 4.99 | CLASSIC-POST-GLOS-6X4 | PostcardTemplate | No |
| Standard Card | 9.99 | — | TradingCardTemplate | No |
| FamiliVault Card | 9.99 | — | VaultCard | No |
| Card Deck | 24.99 | — | — | No |

### 9.4 Multi-Currency Support

8 countries supported via `CurrencyContext.jsx`:

| Country | Currency | Approx Rate (from GBP) |
|---------|----------|----------------------|
| GB | GBP | 1.00 |
| US | USD | 1.27 |
| CA | CAD | 1.72 |
| AU | AUD | 1.93 |
| DE | EUR | 1.17 |
| FR | EUR | 1.17 |
| IE | EUR | 1.17 |
| NL | EUR | 1.17 |

Rates are hardcoded approximations. Stripe Adaptive Pricing handles actual conversion at checkout.

---

## 10. Technology Stack

| Repo | Language | Framework | Key Deps | Tests |
|------|----------|-----------|----------|-------|
| desktop2 | JavaScript | React 18 + Vite | face-api.js, TF.js, framer-motion, Stripe | Vitest 1,022+ + Playwright |
| desktop3 | Python 3.10 | FastAPI + Uvicorn | InsightFace, AdaFace ONNX, MediaPipe, OpenCV, Stripe, Prodigi | pytest 166+ |
| desktop4 | JavaScript | React 18 + Vite + Tailwind | face-api.js, TF.js, framer-motion | Vitest 932 + Playwright 42 |
| desktop5 | Python 3.10 | FastAPI + Uvicorn | pydantic | pytest 37 |
| desktop6 | JavaScript | React 18 + Vite + Tailwind | react-router-dom, framer-motion, lucide-react | Vitest 98 |
| desktop7 | Python 3.10 | FastAPI + Uvicorn | pydantic, httpx | pytest 111 |

### Shared FE utilities (desktop2 / desktop4 / desktop6)

| Module | d2 | d4 | d6 |
|--------|----|----|----|
| `deckBuilder.js` | Yes | Yes | No — no card concept |
| `useGameFamilyData.js` | Yes | Yes | No |
| `Card.jsx` components | Yes | Yes | No |
| `photoUtils.js` | Yes | Yes | Yes |
| `analytics.js` | Yes | Yes | Yes |
| Chemistry label logic | No | No | Yes (`constants.js`) |
| Room / WebSocket client | No | Yes | Yes |

---

## 11. Implementation Status

### FamiliLook (desktop2 + desktop3) — LIVE WITH COMMERCE

- [x] 8-feature kinship analysis with calibrated labels
- [x] 6 games (MemoryMatch, FeatureMatch, CardGame, FaceFusion, HungryHeads, FeatureCatch)
- [x] Group photo snapshot (`/kinship/group-snapshot`)
- [x] Analytics dashboard (`/dashboard?key=fl-admin-2026`)
- [x] **Brand hub homepage** (famililook.com root → 4-tile product grid) — **LIVE** (2026-02-26)
- [x] **Commerce layer** — Stripe checkout (single + basket), multi-currency (8 countries), personalised message surcharge
- [x] **Prodigi integration** — keepsake ordering live, verified SKUs, webhook status tracking
- [x] **Keepsake template system** — lazy-loaded templates, print profiles, preview rendering
- [x] **Family Mug Set** — Mum/Dad pair product, FamilyMugTemplate, useFamilyKeepsakeData hook
- [x] **LLM personalisation** — AI-generated messages on keepsake templates (optional toggle)
- [x] **Custom SVG feature icons** — 8 icons built, preview page at /icon-preview
- [x] **GDPR consent banner** — analytics gated on consent
- [x] **FamiliVault heritage card** — premium trading card template with rarity tiers, power stats, barcode, QR zone, holographic effects (see §3.6)
- [x] **FamiliTrail board** — gamified feature discovery page at `/trail`, 22 stops across 6 zones, tier gating, peek previews, campaign badges (see §3.5)
- [x] **Parent-pair exclusion (couple gate)** — parents excluded from pairwise comparison by default; label gate requires parent tagging in group mode; opt-in toggle; FamiliMatch redirect for couples
- [ ] Analytics dashboard bugs (feedback endpoint, session count, double-count) — deferred
- [ ] 3D keepsake mockups — planned (Blender templates + browser compositing)
- [ ] Wire SVG icons into all templates (currently still using emoji)
- [ ] FamiliTrail: analytics tracking, progress persistence, achievement badges (see §3.5)
- [ ] FamiliVault: consolidate two components, wire real percentiles, card collection page (see §3.6)

### FamiliUno (desktop2 FE + desktop3 BE) — LIVE

| Task | Status |
|------|--------|
| Product definition | Complete (this document) |
| Card supplier API selection | QPMarkets selected, `card_deck_order.v1` contract finalized |
| FamiliUno section in desktop2 FE | **Complete** — `FamiliUnoPage.jsx` with upload, analysis, and card deck generation |
| Card deck preview / virtual simulation | Complete (reuses CardGame component) |
| Physical card pack order flow | Backend ordering endpoints complete (`POST /orders/card-deck`) |
| Card supplier API integration | `CardPrintClient` in `vendor_client.py` — manifest validation + QPMarkets API. **LIVE** (2026-03-26). |

### FamiliPoker (desktop4 + desktop5) — IN DEVELOPMENT

| Task | Status |
|------|--------|
| Feature Poker (single-player) | Design complete |
| Feature 21 (single-player) | Design complete |
| Casino lobby + room system | Design complete |
| desktop5 game server | Complete (37 tests) |
| desktop4 FE multiplayer client | Not started |
| Chip economy + cosmetics | Not started |

### FamiliMatch (desktop6 + desktop7) — IN DEVELOPMENT

| Task | Status |
|------|--------|
| desktop7 WebSocket room server | Complete (111 tests) |
| Solo mode FE (upload → compatibility reveal) | Complete |
| Duo mode FE (room → countdown → reveal) | Complete |
| Group mode FE (room → individual selfies → pairwise matrix) | Complete |
| ResultsStory 5-card progressive reveal | Complete |
| GroupMatrix progressive reveal | Complete |
| OnboardingScreen + sessionStorage name | Complete |
| FeatureScanAnimation (3-phase analysis display) | Complete |
| Face fusion integration | Complete (via /face/morph) |
| Desktop6 FE tests | 98 passing |
| **Wire Solo to `/compare/faces`** (symmetric peer comparison, all scoring in backend) | **Done** — `matchClient.js` uses `POST /compare/faces`; contract frozen at `contracts/compare_faces.v1.schema.json` |
| **Group photo scan mode** (upload one photo → detect all faces → pairwise compat) | **Planned** — distinct from /kinship/group-snapshot which is FamiliLook-only |
| Sharing / screenshot of results | Not started |
| Blind matching mode | Not started |
| Match history (localStorage) | Not started |

---

## 12. Repo Map

```
FML/                              (parent repo — main branch)
├── famililook-desktop2/          LIVE — FamiliLook FE (independent repo, NOT submodule)
├── famililook-desktop3/          LIVE — Shared Analysis Engine (independent repo, NOT submodule)
├── famililook-desktop4/          DEV  — FamiliPoker FE
├── famililook-desktop5/          DEV  — FamiliPoker Game Server
├── famililook-desktop6/          DEV  — FamiliMatch FE
├── famililook-desktop7/          DEV  — FamiliMatch Room Server
├── docs/
│   ├── PLATFORM_ARCHITECTURE.md (this document)
│   └── FAMILIMATCH_DESIGN_REQUIREMENTS.md
├── legal/                        Privacy policies, terms
└── CLAUDE.md                     Dev governance
```
