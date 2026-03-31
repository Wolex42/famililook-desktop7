## Design Lead: FamiliTrail Badge UI Spec

**Agent**: Design Lead
**Input**: CPO spec (trail_phase4_cpo_spec.md) — approved
**Date**: 2026-03-23

---

### Badge Bar (Trail Page Header)

**Position**: Below page title, above canvas. Horizontal scrollable row.
**Height**: 48px
**Background**: `rgba(255,255,255,0.04)` with `border: 1px solid rgba(255,255,255,0.08)`, `border-radius: 12px`

**Layout**: `display: flex; gap: 8px; padding: 8px 12px; overflow-x: auto;`

**Badge Pill** (each badge):
- Size: `36px × 36px` circle
- Earned: `background: linear-gradient(145deg, #f59e0b, #fbbf24)`, icon white, subtle glow `box-shadow: 0 0 12px rgba(251,191,36,0.3)`
- Unearned: `background: rgba(255,255,255,0.06)`, icon `rgba(255,255,255,0.2)`, lock overlay
- Icon: Lucide icons at 18px — `Compass`, `Trophy`, `Gamepad2`, `Flame`, `Star`
- Touch target: 44px minimum (iOS HIG compliant)

**Counter**: Right-aligned after badges — `"3/5"` in `fontSize: 13px, color: rgba(255,255,255,0.4)`

---

### Toast Notification (on badge earn)

**Position**: Top of screen, below safe area inset
**Animation**: Slide down from -60px → 0, hold 3 seconds, slide up and fade
**Style**:
- `background: rgba(0,0,0,0.85)`, `backdrop-filter: blur(12px)`
- `border: 1px solid rgba(251,191,36,0.3)`, `border-radius: 16px`
- `padding: 12px 16px`, `max-width: 320px`, centered
- Badge icon (28px, gold) + text: "🏆 Badge Earned!" (14px bold) + badge name (12px, muted)
- `z-index: 200` (above canvas, below modals)

**Tailwind equivalents**:
```
bg-black/85 backdrop-blur-md border border-amber-400/30 rounded-2xl px-4 py-3
text-sm font-bold text-white
```

---

### Badge Detail (tap on earned badge)

**Not in scope for Phase 4** — future enhancement. Tapping earned badge does nothing for now. Tapping unearned badge shows "Visit X more nodes to earn this badge" tooltip.

---

### Responsive

- **Mobile** (< 480px): Badge bar fills width, horizontal scroll if needed
- **Tablet/Desktop** (> 480px): Badge bar centered, no scroll needed for 5 badges

### Accessibility

- `role="list"` on badge bar, `role="listitem"` on each badge
- `aria-label="Discovery Explorer badge — earned"` or `"— locked, visit 3 more nodes"`
- Toast has `role="status"` and `aria-live="polite"`
- Contrast: Gold on dark background ≥ 4.5:1

---

**Handoff: Design Lead → FE Lead**

**Task**: Implement badge bar + toast per this spec
**Artifacts**: This spec (`trail_phase4_design_spec.md`)
