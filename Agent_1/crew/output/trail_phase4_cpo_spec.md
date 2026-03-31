## CPO Spec: FamiliTrail Enhancements — Badges + A/B Test

**Agent**: CPO
**Task**: Phase 4 enhancements for FamiliTrail
**Date**: 2026-03-23
**ICE Score**: Impact 7 × Confidence 8 × Ease 6 = 336

---

### Context

Trail foundation is solid: 16/20 active nodes work, 44 tests pass, docs are current. Now we add the engagement and conversion layers.

### Priority Assessment

| Enhancement | Priority | Revenue signal | Effort | Build now? |
|-------------|----------|---------------|--------|------------|
| Achievement badges + toast | P2 | Drives engagement → feature adoption → upgrades | S | **Yes** |
| A/B test: trail as default landing | P2 | Data-driven — could increase conversion if trail > homepage | S | **Yes** |
| Dynamic unlock animation | P3 | Polish — nice but no revenue signal | S | **Defer** |
| Seasonal zone theming | P3 | Seasonal relevance — Easter is April 3 (11 days) | M | **Defer** (too close) |
| Trail completion confetti | P3 | Polish — celebration drives sharing | S | **Defer** |

**Decision: Build badges + A/B test. Defer P3 items to post-Capacitor.**

---

### Enhancement 1: Achievement Badges

**What**: Unlockable badges that appear as toast notifications when milestones are reached, displayed on trail header.

**Badges:**
| Badge | Name | Criteria | Icon |
|-------|------|----------|------|
| 1 | Discovery Explorer | Visit all 5 Discovery Zone nodes | compass |
| 2 | Keepsake Collector | Visit all 5 Keepsake Kingdom nodes | trophy |
| 3 | Arcade Champion | Visit all 4 Game Arcade nodes | gamepad |
| 4 | Trail Blazer | Visit 15+ total nodes | fire |
| 5 | Completionist | Visit all accessible nodes (tier-dependent) | star |

**Acceptance Criteria:**
- [ ] Badge state persisted in `localStorage fl:trail_badges`
- [ ] Toast notification fires when badge earned (first time only)
- [ ] Badge icons displayed in trail page header
- [ ] Badge count shown ("3/5 badges earned")
- [ ] Earned badges show gold, unearned show grey with lock
- [ ] Badge check runs on every node visit (computed from `fl:trail_visited`)
- [ ] No badge re-triggers on page reload (idempotent)

**Scope**: New file `TrailBadges.jsx` + updates to `TrailHomePage.jsx`. No backend. No existing file modifications beyond TrailHomePage.

---

### Enhancement 2: A/B Test — Trail as Default Landing

**What**: Feature flag to test whether routing new users to `/trail` instead of `/` increases feature adoption and upgrade rate.

**Acceptance Criteria:**
- [ ] `VITE_TRAIL_DEFAULT_LANDING` env var (boolean string: "true"/"false")
- [ ] Added to vite.config.mjs define block
- [ ] When "true": AppRouter redirects `/` to `/trail` for users without `fl:returning_user` in localStorage
- [ ] When "false" or unset: normal homepage behaviour (default)
- [ ] First visit to trail sets `fl:returning_user = true` (so they get homepage on return)
- [ ] Analytics event: `trail_ab_test_assigned` with variant "trail" or "homepage"
- [ ] No change for returning users — they always get homepage

**Scope**: Small changes to `AppRouter.jsx` + `.env.local`. No backend. Feature flag defaults to "false" (safe).

---

**Handoff: CPO → Design Lead (badges UI) + FE Lead (A/B test implementation)**

**Parallel work:**
- Design Lead specs the badge UI (icons, toast, header layout)
- FE Lead implements A/B test (pure routing logic, no UI design needed)

**Artifacts**: This spec
**Decisions Made**: P3 items deferred. Only badges + A/B test in this phase.
**Open Questions**: None
