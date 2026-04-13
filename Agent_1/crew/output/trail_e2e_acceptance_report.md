# FamiliTrail — 22 Node E2E Customer Acceptance Report

> **Date**: 2026-03-23
> **Audited by**: QA Lead (nodes 1-14, 21-22) + CTO (nodes 15-20)
> **Scoring**: 5 dimensions × 0-2 each = max 10 per node, max 220 total

---

## Overall Score: 88 / 220 (40%)

| Rating | Threshold | Nodes |
|--------|-----------|-------|
| **SHIP** (8-10) | Customer-ready | 3 nodes |
| **FIX REQUIRED** (5-7) | Usable but gaps | 4 nodes |
| **BLOCKED** (0-4) | Cannot release | 15 nodes |

---

## Full Scorecard

| # | Node | Zone | Tier | Reach | Func | Data | UX | Money | Total | Rating |
|---|------|------|------|-------|------|------|-----|-------|-------|--------|
| 1 | Upload Photos | Discovery | free | 2 | 2 | 2 | 2 | 1 | **9** | SHIP |
| 2 | 8 Feature Scan | Discovery | free | 1 | 1 | 0 | 1 | 1 | **4** | BLOCKED |
| 3 | Parent vs Child | Discovery | free | 1 | 1 | 0 | 1 | 1 | **4** | BLOCKED |
| 4 | Group Photo | Discovery | plus | 2 | 2 | 1 | 1 | 1 | **7** | FIX REQUIRED |
| 5 | Pet Compare | Discovery | free | 2 | 1 | 1 | 1 | 0 | **5** | FIX REQUIRED |
| 6 | Keepsake Cards | Keepsakes | free | 0 | 1 | 0 | 0 | 1 | **2** | BLOCKED |
| 7 | Full Card Deck | Keepsakes | plus | 0 | 1 | 0 | 0 | 1 | **2** | BLOCKED |
| 8 | Digital Downloads | Keepsakes | free | 0 | 1 | 0 | 0 | 0 | **1** | BLOCKED |
| 9 | Print & Order | Keepsakes | plus | 0 | 1 | 0 | 0 | 2 | **3** | BLOCKED |
| 10 | FamiliVault Cards | Keepsakes | pro | 2 | 2 | 2 | 2 | 1 | **9** | SHIP |
| 11 | Memory Match | Arcade | free | 2 | 1 | 0 | 1 | 0 | **4** | BLOCKED |
| 12 | Face Fusion | Arcade | free | 2 | 1 | 0 | 1 | 0 | **4** | BLOCKED |
| 13 | Hungry Heads | Arcade | plus | 2 | 1 | 0 | 1 | 0 | **4** | BLOCKED |
| 14 | Feature Catch | Arcade | plus | 2 | 1 | 0 | 1 | 0 | **4** | BLOCKED |
| 15 | Feature Poker | Casino | pro | 1 | 2 | 0 | 1 | 1 | **5** | FIX REQUIRED |
| 16 | Feature 21 | Casino | pro | 1 | 2 | 0 | 1 | 1 | **5** | FIX REQUIRED |
| 17 | Multiplayer Battle | Casino | pro | 1 | 0 | 0 | 0 | 0 | **1** | BLOCKED |
| 18 | Solo Compare | Chemistry | free | 2 | 2 | 2 | 2 | 0 | **8** | SHIP |
| 19 | Duo Room | Chemistry | plus | 1 | 1 | 0 | 1 | 0 | **3** | BLOCKED |
| 20 | Group Party | Chemistry | pro | 1 | 1 | 0 | 1 | 0 | **3** | BLOCKED |
| 21 | FamiliUno Cards | Coming Soon | — | 1 | 0 | 0 | 1 | 0 | **2** | BLOCKED |
| 22 | Uno Multiplayer | Coming Soon | — | 1 | 0 | 0 | 1 | 0 | **2** | BLOCKED |

---

## Score by Zone

| Zone | Nodes | Avg Score | Best | Worst |
|------|-------|-----------|------|-------|
| Discovery | 5 | 5.8 | 9 (Upload) | 4 (Feature Scan, Parent Compare) |
| Keepsakes | 5 | 3.4 | 9 (Vault) | 1 (Digital Downloads) |
| Arcade | 4 | 4.0 | 4 (all equal) | 4 (all equal) |
| Casino | 3 | 3.7 | 5 (Poker, 21) | 1 (MP Battle) |
| Chemistry | 3 | 4.7 | 8 (Solo) | 3 (Duo, Group) |
| Coming Soon | 2 | 2.0 | 2 | 2 |

## Score by Dimension

| Dimension | Total (max 44) | % | Weakest zone |
|-----------|---------------|---|-------------|
| Reachable | 26 | 59% | Keepsakes (0/8) |
| Functional | 22 | 50% | Coming Soon (0/4) |
| Data-Ready | 8 | 18% | **Everywhere except Upload, Vault, Solo** |
| UX Quality | 18 | 41% | Keepsakes (2/10) |
| Monetisation | 10 | 23% | Arcade + Chemistry (0/14) |

---

## Critical Issues (ranked by impact)

### P0 — Blocks Customer Release

| Issue | Nodes Affected | Root Cause | Fix |
|-------|---------------|------------|-----|
| **Keepsakes are unreachable** | 6, 7, 8, 9 | Route `/app` with no section anchor. User lands on IntentSelector, not keepsakes | Node 7→`/uno`. Nodes 6,8,9 need post-analysis state check + conditional routing |
| **Multiplayer Battle doesn't exist** | 17 | Listed as "Coming Soon" in desktop4. WebSocket not implemented | Move to `coming_soon` tier |
| **Games need data with no fallback** | 11, 12, 13, 14 | `buildDeck()` returns empty without prior analysis | Add "Try with demo family" option or route to upload-first flow |
| **Data-Ready is 18% overall** | 13 of 22 nodes | Features require prior analysis data in localStorage | Design cold-start paths for every data-dependent feature |

### P1 — Significantly Degrades Experience

| Issue | Nodes Affected | Root Cause | Fix |
|-------|---------------|------------|-----|
| **3 Discovery nodes are identical** | 2, 3 | All route to `/app?intent=child` | Collapse into 1 node OR add `#results`/`#features` section anchors |
| **No deep-linking in external apps** | 15, 16, 19, 20 | External URLs go to app root, not specific feature | Add `?game=poker` to desktop4, `?mode=duo` to desktop6 |
| **Duo/Group need WebSocket** | 19, 20 | `wss://api.famililook.com/ws/match` — status unknown | Verify WS endpoint is live. If not, move to `coming_soon` |
| **No data portability cross-app** | 15, 16 | Desktop4 needs fresh analysis — can't reuse desktop2 data | Explore shared session or URL-passed embeddings |

### P2 — Lost Revenue / Missed Opportunity

| Issue | Nodes Affected | Fix |
|-------|---------------|-----|
| **Zero monetisation in Arcade zone** | 11-14 | Add "Order physical cards" CTA post-game |
| **Zero monetisation in Chemistry zone** | 18-20 | Add keepsake cross-sell after match result |
| **"Get Notified" button is a no-op** | 21, 22 | Wire to EmailCapture component (already exists in BrandHub) |
| **Pet mode has no revenue path** | 5 | Add pet keepsake templates or remove pet from trail |

---

## Recommendations to CEO

### Immediate (before any marketing push)

1. **Move Node 17 (Multiplayer Battle) to `coming_soon`** — it promises a feature that doesn't exist. Misleading.
2. **Fix Keepsake Kingdom routing** — 4 nodes are dead ends. This is the revenue zone.
3. **Add demo mode for games** — so cold users can try games without prior analysis.

### Short-term (before Capacitor)

4. **Collapse or differentiate Discovery nodes 2+3** — 3 nodes to the same page is confusing.
5. **Verify WebSocket endpoints** — if `ws/match` and `ws/game` are not live, move Duo/Group/MP to `coming_soon`.
6. **Wire "Get Notified" to email capture** — convert interest into leads.

### Medium-term (with Capacitor work)

7. **Cross-app deep-linking** — `?game=poker` param in desktop4, `?mode=solo` in desktop6.
8. **Data portability** — shared face data between desktop2/4/6.
9. **Monetisation CTAs in games and match results** — every feature should have a path to revenue.

---

## Crew Sign-Off

| Agent | Verdict |
|-------|---------|
| QA Lead | 40% acceptance rate. 15 of 22 nodes BLOCKED. Cannot recommend customer release of trail as primary navigation without fixing P0 issues. |
| CTO | Cross-app nodes 15-16 are functional but friction-heavy. Nodes 17, 19, 20 depend on unverified infrastructure. Recommend moving to `coming_soon` until WS endpoints confirmed. |
| CPO | Trail as front door needs 70%+ acceptance rate minimum. Current 40% means trail should remain a secondary discovery path (not default landing) until P0/P1 issues resolved. **A/B test should stay OFF (`VITE_TRAIL_DEFAULT_LANDING=false`).** |
