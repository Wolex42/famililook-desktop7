# Product Backlog

> Last updated: 2026-03-21
> Sprint: 1 (post-integration)

## Format
```
- [STATUS] TASK-<id>: <title> | Product: <product> | Priority: <P0-P3> | Owner: <agent_id> | Effort: <S/M/L/XL>
```

STATUS: `TODO` | `IN_PROGRESS` | `BLOCKED` | `DONE`

---

## P0 — Critical (Blockers)

- [TODO] TASK-001: COPPA compliance — parental consent mechanism for children's biometric data | Product: FamiliLook | Priority: P0 | Owner: compliance + cto | Effort: XL
- [BLOCKED] TASK-002: QPMarkets API integration for FamiliUno card printing | Product: FamiliUno | Priority: P0 | Owner: be_lead | Effort: L | Blocker: Awaiting API key from QPMarkets
- [TODO] TASK-003: Server-side BIPA consent validation | Product: FamiliMatch | Priority: P0 | Owner: be_lead | Effort: M

## P1 — High (Revenue / Growth)

- [TODO] TASK-004: Live exchange rates API (replace hardcoded rates — FM-16 RPN 120) | Product: All | Priority: P1 | Owner: be_lead | Effort: M
- [TODO] TASK-005: Marketing claims audit — correct "never leaves your device" | Product: All | Priority: P1 | Owner: compliance + ad_crew | Effort: S
- [TODO] TASK-006: Formal DPIA document for all products | Product: All | Priority: P1 | Owner: compliance | Effort: L
- [TODO] TASK-007: Native mobile app (Capacitor) — at least FamiliLook | Product: FamiliLook | Priority: P1 | Owner: fe_lead + cto | Effort: XL
- [TODO] TASK-008: FamiliMatch viral sharing mechanics (TikTok-ready face fusion) | Product: FamiliMatch | Priority: P1 | Owner: fe_lead + cpo | Effort: L
- [TODO] TASK-016: FamiliTrail — analytics event tracking (trail_node_click, peek_viewed, tooltip_opened, upgrade_clicked) | Product: FamiliLook | Priority: P1 | Owner: fe_lead | Effort: S | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-017: FamiliTrail — progress persistence (fl:trail_visited in localStorage, visited node glow) | Product: FamiliLook | Priority: P1 | Owner: fe_lead | Effort: S | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-018: FamiliVault — consolidate two VaultCard components into unified component with mode prop | Product: FamiliLook | Priority: P1 | Owner: fe_lead + cto | Effort: M | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-019: FamiliVault — wire real calibrated percentiles from BE kinship response | Product: FamiliLook | Priority: P1 | Owner: fe_lead | Effort: S | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-020: FamiliVault — social sharing (screenshot export via html2canvas + Web Share API) | Product: FamiliLook | Priority: P1 | Owner: fe_lead | Effort: M | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-021: FamiliVault — physical card printing via Prodigi (standard card SKU, 300 DPI export) | Product: FamiliLook | Priority: P1 | Owner: fe_lead + commerce_lead | Effort: M | PRD: PRD_FAMILIVAULT.md

## P2 — Medium (Quality / UX)

- [TODO] TASK-009: Scaling plan — handle viral load beyond 50 concurrent analyses | Product: All | Priority: P2 | Owner: cto + devops | Effort: L
- [TODO] TASK-010: A/B test framework for conversion optimisation | Product: All | Priority: P2 | Owner: ux_researcher + fe_lead | Effort: M
- [TODO] TASK-011: EU AI Act transparency notices | Product: All | Priority: P2 | Owner: compliance | Effort: M
- [TODO] TASK-012: Cross-browser testing baseline (Chrome, Safari, Firefox) | Product: All | Priority: P2 | Owner: qa_lead | Effort: M
- [TODO] TASK-022: FamiliTrail — achievement badges (visit all free stops, visit 15+, toast notifications) | Product: FamiliLook | Priority: P2 | Owner: fe_lead + design_lead | Effort: M | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-023: FamiliTrail — A/B test trail as default landing page vs homepage | Product: FamiliLook | Priority: P2 | Owner: fe_lead + ux_researcher | Effort: S | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-024: FamiliVault — card collection / album page at /vault/collection | Product: FamiliLook | Priority: P2 | Owner: fe_lead + design_lead | Effort: M | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-025: FamiliVault — card back on keepsake version + flip interaction | Product: FamiliLook | Priority: P2 | Owner: fe_lead | Effort: S | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-026: FamiliVault — pack opening animation (gacha-style card reveal) | Product: FamiliLook | Priority: P2 | Owner: fe_lead + design_lead | Effort: M | PRD: PRD_FAMILIVAULT.md

## P3 — Low (Nice to Have)

- [TODO] TASK-013: Design system documentation | Product: All | Priority: P3 | Owner: design_lead | Effort: M
- [TODO] TASK-014: FamiliPoker multiplayer matchmaking improvements | Product: FamiliPoker | Priority: P3 | Owner: be_lead | Effort: M
- [TODO] TASK-015: Keepsake seasonal templates (Easter, Summer) | Product: FamiliLook | Priority: P3 | Owner: design_lead + fe_lead | Effort: S
- [TODO] TASK-027: FamiliTrail — seasonal zone theming (Easter eggs, Christmas snow, Valentine hearts) | Product: FamiliLook | Priority: P3 | Owner: design_lead + fe_lead | Effort: M | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-028: FamiliTrail — animated trail completion (confetti when all stops visited) | Product: FamiliLook | Priority: P3 | Owner: fe_lead | Effort: S | PRD: PRD_FAMILITRAIL.md
- [TODO] TASK-029: FamiliVault — FamiliClash battle cards (attack/defense, matchup system) | Product: FamiliLook | Priority: P3 | Owner: cpo + fe_lead | Effort: XL | PRD: PRD_FAMILIVAULT.md
- [TODO] TASK-030: FamiliVault — FamiliLegacy premium heirloom cards (radar chart, 19 sub-features) | Product: FamiliLook | Priority: P3 | Owner: cpo + fe_lead | Effort: XL | PRD: PRD_FAMILIVAULT.md

---

## Done (This Sprint)
_(none yet)_

---

## Task Dependency Graph

```
TASK-016 (Trail analytics) ─────────────────────────┐
TASK-017 (Trail persistence) ─► TASK-022 (Achievements) ─► TASK-023 (A/B test)
                                                      └─► TASK-028 (Completion confetti)
TASK-027 (Seasonal theming) ─ standalone ─

TASK-018 (Vault consolidate) ─┬─► TASK-019 (Wire percentiles)
                               ├─► TASK-020 (Social sharing)
                               ├─► TASK-021 (Physical printing)
                               ├─► TASK-024 (Collection page) ─► TASK-026 (Pack animation)
                               └─► TASK-025 (Card back + flip)
TASK-029 (FamiliClash) ─── requires TASK-018
TASK-030 (FamiliLegacy) ─── requires TASK-018
```
