# PRD: FamiliVault — Heritage Trading Cards

> **Author**: CPO Agent
> **Date**: 2026-03-21
> **Product**: FamiliLook (desktop2)
> **Priority**: P1
> **Status**: IN_PROGRESS (core built, consolidation + enhancements needed)

---

## 1. Problem Statement

Two separate VaultCard components exist — a standalone interactive version (3D tilt, flip, card back) and a keepsake print version (stat bars, QR, barcode). They share the concept but diverge in data schema, rarity tiers, and visual treatment. This creates maintenance overhead and prevents a unified "collect → print → share" user journey. Additionally, the cards use similarity scores as percentile proxies instead of real calibrated percentiles from the backend.

## 2. Goal

One unified VaultCard component that works for both interactive preview and print export, powered by real calibrated biometric data, with a collection/album system and social sharing capability.

## 3. Context

- **Current state**: Two working VaultCard components in desktop2. Both render correctly. Keepsake version registered in templateRegistry, printProfiles, messageGenerator, KeepsakesModal. Standalone has richer interaction (3D tilt, flip, card back). Trail links to `/vault`.
- **Evidence**: Build output shows both bundled. 923 tests pass. `/vault` route works.
- **Technical debt**: Standalone uses `featureStars` (1-5), keepsake uses `featureDetails[].similarity`. Different rarity tier systems. Duplicate Barcode components.

### Current File Map

```
STANDALONE (interactive)
├── src/components/vault/VaultCard.jsx       — 622 lines, 3D tilt, flip, genome strip, holo stamp
├── src/components/vault/vaultCardData.js    — 184 lines, schema + builders + demo cards
└── src/pages/VaultPreview.jsx               — 195 lines, gallery at /vault

KEEPSAKE (print-ready)
└── src/components/keepsakes/templates/ChildCards/VaultCard.jsx — 541 lines, stat bars, QR, barcode
```

## 4. User Stories

- As a parent, I want one VaultCard that I can interact with (flip, tilt) AND order as a physical print.
- As a collector, I want to see all my family's VaultCards in an album, so I can compare rarity and stats.
- As a user, I want to share my child's Legendary VaultCard on social media with one tap.
- As a parent, I want the card's rarity to reflect real calibrated biometric data, not approximations.

## 5. Acceptance Criteria

### Already Done
- [x] Standalone VaultCard with 3D tilt, flip interaction, holographic foil, genome strip, holo stamp
- [x] Keepsake VaultCard with foil shimmer, stat bars (PWR/DEF/CHM), QR placeholder, barcode
- [x] Card back design (hexagonal grid, DNA ring, FV emblem, barcode)
- [x] Preview gallery at `/vault` with all rarity tiers + full-size showcase
- [x] Registration in keepsake system (templateRegistry, printProfiles, messageGenerator, KeepsakesModal)
- [x] Trail integration (vault_cards node in Keepsake Kingdom, Pro tier)
- [x] Deterministic rarity system (6-tier standalone, 5-tier keepsake)
- [x] Heritage type classification (Guardian/Luminary/Artisan/Sovereign/Maverick)
- [x] Power stats (PWR/DEF/CHM) derived from feature similarity groups
- [x] Deterministic serial numbers + barcode from name hash
- [x] Demo cards for all rarity tiers

### To Build (Priority Order)

#### P1 — Consolidation + Data Integrity
- [ ] **Unify VaultCard**: merge standalone + keepsake into single component with `mode` prop (`interactive` vs `print`)
  - Interactive mode: 3D tilt, flip, foil overlay, holo stamp, genome strip
  - Print mode: static layout optimized for html2canvas export (no animations, no hover effects)
  - Shared: rarity system, serial generation, barcode, power stats, feature display
- [ ] **Unified rarity system**: consolidate 6-tier (standalone) and 5-tier (keepsake) into one 6-tier system (Common → Uncommon → Rare → Epic → Legendary → Mythic)
- [ ] **Wire real calibrated percentiles**: consume `calibrated_features` from backend kinship response instead of using `similarity` as proxy. Map percentile ranges to star ratings (0-20th=1★, 20-40th=2★, 40-60th=3★, 60-80th=4★, 80-100th=5★)
- [ ] **Unified data builder**: single `buildVaultCard()` function that accepts either `featureStars` (manual) or `featureDetails` (from analysis) and produces consistent card object

#### P1 — Revenue + Social
- [ ] **Physical printing**: register unified VaultCard in Prodigi print flow (standard card SKU: `CLASSIC-POST-GLOS-6X4` or custom size)
- [ ] **Share to social**: screenshot export of card face (html2canvas → PNG → Web Share API / download)
- [ ] **Print-ready export**: ensure html2canvas renders correctly at 300 DPI for standard trading card dimensions (63mm × 88mm = 744 × 1039px at 300 DPI)

#### P2 — Collection + Engagement
- [ ] **Card collection page**: `/vault/collection` route — grid of all generated VaultCards for current family, stored in `localStorage fl:vault_collection`
- [ ] **Card back on keepsake**: port card back design from standalone to unified component
- [ ] **Flip interaction everywhere**: tap/click to flip in both collection view and keepsake preview
- [ ] **Pack opening animation**: gacha-style card reveal (wrapper tears open → card spins in → rarity announcement)

#### P3 — Future Products
- [ ] **FamiliClash**: battle card variant — attack/defense stats, matchup system, head-to-head gameplay
- [ ] **FamiliLegacy**: premium heirloom variant — radar chart with all 19 sub-features, gold leaf border, certificate number
- [ ] **Card trading**: share card codes between families (deterministic serial enables verification)

## 6. Scope

### In Scope
- Component consolidation (FE refactor)
- Wire backend calibrated data (FE data mapping)
- Collection page (new FE route)
- Social sharing (FE Web Share API)
- Print export optimization (FE html2canvas)
- Tests for unified component

### Out of Scope
- Backend changes (calibrated_features already returned in kinship response)
- New backend endpoints
- Payment changes (uses existing Prodigi + Stripe flow)
- Card trading system (future phase)

## 7. Agent Assignments

| Step | Agent | Task | Depends On |
|------|-------|------|-----------|
| 1 | cto | Architecture review — unified component design | — |
| 2 | fe_lead | Merge VaultCard components with `mode` prop | Step 1 |
| 3 | fe_lead | Unify rarity system (6 tiers) | Step 2 |
| 4 | fe_lead | Wire calibrated percentiles from BE response | Step 2 |
| 5 | fe_lead | Update templateRegistry + printProfiles for unified component | Step 2 |
| 6 | qa_lead | Write tests for unified VaultCard (all modes, all rarities) | Steps 2-5 |
| 7 | design_lead | Pack opening animation design + motion spec | — |
| 8 | fe_lead | Implement collection page at `/vault/collection` | Step 2 |
| 9 | fe_lead | Social sharing (screenshot export) | Step 2 |
| 10 | fe_lead | Pack opening animation | Steps 7, 8 |
| 11 | fe_lead | Print-ready export at 300 DPI | Step 5 |
| 12 | qa_lead | E2E test: analysis → vault card → print order | Steps 6, 11 |

## 8. Dependencies & Blockers

- Dependency: `calibrated_features` in kinship response (already available — verified in desktop3 engine.py)
- Dependency: `html2canvas` for print export (already installed in desktop2)
- Dependency: Prodigi SKU for standard card (CLASSIC-POST-GLOS-6X4 verified)
- No blockers

## 9. Success Metrics

| Metric | Baseline | Target | Measured By |
|--------|----------|--------|-------------|
| VaultCard generation rate | Unknown | 30% of analyses generate a vault card | analytics.trackAction('vault_card_generated') |
| Card orders (physical) | 0 | 5% of vault card views → order | Stripe checkout events |
| Social shares | 0 | 10% of vault card views → share | Web Share API usage tracking |
| Collection page visits | 0 | 20% of vault card generators visit collection | page_view /vault/collection |

## 10. Effort Estimate

- **Size**: L (consolidation = 3 days; data wiring = 1 day; collection page = 2 days; social sharing = 1 day; print optimization = 1 day; pack animation = 2 days)
- **ICE Score**: Impact(9) × Confidence(8) × Ease(5) = 360

## Files to Modify

| File | Changes |
|------|---------|
| `src/components/vault/VaultCard.jsx` | Become the unified component (add `mode` prop) |
| `src/components/vault/vaultCardData.js` | Unified rarity tiers + data builder |
| `src/components/keepsakes/templates/ChildCards/VaultCard.jsx` | Replace with import from unified component |
| `src/pages/VaultPreview.jsx` | Use unified component |
| `src/pages/VaultCollection.jsx` | **NEW** — collection/album page |
| `src/AppRouter.jsx` | Add `/vault/collection` route |
| `src/components/keepsakes/utils/templateRegistry.js` | Update VaultCard import |
| `src/components/keepsakes/utils/printProfiles.js` | Update print specs for standard card |
| `src/hooks/useKeepsakeData.js` | Map calibrated_features to featureStars |
| `tests/vault/*.test.jsx` | **NEW** — unified VaultCard tests |
