## CPO Spec: Trail P3 Polish — Unlock Animation + Seasonal Theming + Confetti

**Agent**: CPO
**Date**: 2026-03-23
**Context**: Easter is April 3 (11 days). Ship seasonal theming NOW or miss the window.

---

### Feature 1: Dynamic Unlock Animation (S)

**When**: User upgrades from Free→Plus or Plus→Pro (detected via currentPlan change)
**What**: New nodes that become accessible glow + pulse + particle burst
**How**:
- TrailHomePage watches `currentPlan` state
- On change: compute newly-accessible nodes (compare old tier vs new)
- For each newly-accessible node: trigger CSS animation
  - Scale 1→1.3→1 over 0.6s
  - Radial gradient burst (node colour, 0→100% opacity→0 over 0.8s)
  - Gold sparkle particles (4-6 small circles flying outward, fade)
- Play once, then node settles to normal accessible state
- Analytics: `trail_unlock_animation` with count of newly unlocked nodes

**Files**: FamilyTrailCanvas.jsx (add animation class), TrailHomePage.jsx (detect plan change)

---

### Feature 2: Seasonal Zone Theming (M)

**Easter 2026 (April 3-6) — ship NOW:**

| Zone | Easter Theme |
|------|-------------|
| Discovery | Floating pastel eggs (3-4 small egg emojis drifting slowly) |
| Keepsake Kingdom | Golden egg glow on zone header |
| Game Arcade | Bunny ears on the zone icon |
| Casino Floor | No change (not Easter-appropriate) |
| Chemistry Lab | Heart-shaped particles (pastel pink) |
| Coming Soon | Subtle spring green tint |

**Implementation**:
- `SEASONAL_THEMES` config in trailData.js with date ranges + zone overrides
- FamilyTrailCanvas reads current date, applies themed particles/effects
- Particles are CSS-only (no canvas/WebGL) — small absolutely-positioned divs with float animation
- Each seasonal config: `{ id, startDate, endDate, zones: { discovery: { particles: [...] } } }`

**Future seasons** (just config, same engine):
- Christmas: snowflakes, red/green tints, star on Coming Soon
- Valentine's: hearts in Chemistry Lab, pink tints
- Halloween: spooky purple, bat particles in Casino
- Summer: sunshine particles in Discovery, wave effect

**Files**: trailData.js (SEASONAL_THEMES config), FamilyTrailCanvas.jsx (render particles), new SeasonalParticles.jsx component

---

### Feature 3: Trail Completion Confetti (S)

**When**: User visits all nodes accessible at their tier level
**What**: Confetti burst + toast "You've explored everything! 🎉"
**How**:
- TrailHomePage: after each node visit, check if visitedNodes includes ALL accessible nodes
- Accessible = nodes where TIER_ORDER[node.tier] <= TIER_ORDER[currentPlan]
- When complete: trigger CSS confetti (30-40 coloured squares/circles falling from top)
- Show toast: "Trail Complete! You've explored every stop available to you."
- If user is Free: add "Upgrade to unlock X more stops →"
- Fire once per tier completion (store `fl:trail_completed_{tier}` in localStorage)
- Analytics: `trail_completion` with tier and total visited

**Files**: TrailHomePage.jsx (completion check + toast), new TrailConfetti.jsx component

---

### Priority: Ship in this order
1. **Seasonal theming** — Easter is 11 days. Must ship today.
2. **Confetti** — quick win, drives engagement
3. **Unlock animation** — requires plan change to trigger (less immediate)

**Handoff: CPO → FE Lead**
