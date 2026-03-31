## Design Lead: Trail-to-Destination Colour Handoff Spec

**Agent**: Design Lead
**Task**: Option B — keep trail zone colours, add product-colour transition handoff
**Date**: 2026-03-23

---

### Principle

Trail board = colourful game map (zone colours for visual variety).
Destinations = brand-consistent product colours.
The **tooltip CTA** is the bridge — it previews the destination's brand colour before navigation.

---

### Change 1: Tooltip CTA uses product gradient (not tier colour)

**Current**: CTA button gradient uses tier badge colour (`#22d3ee` cyan for free, `#a855f7` purple for plus, `#f59e0b` amber for pro).

**Proposed**: CTA button gradient uses the **destination product gradient**:

| Destination | CTA Gradient | Nodes |
|-------------|-------------|-------|
| FamiliLook (`/app`) | `#f5a623→#ff6b6b` (amber→coral) | 1,2,3,4,5,6,8,9 |
| FamiliUno (`/uno`) | `#30d158→#0a84ff` (green→blue) | 7,11,12,13,14 |
| FamiliPoker (external) | `#bf5af2→#ff375f` (purple→magenta) | 15,16 |
| FamiliMatch (external) | `#0a84ff→#5e5ce6` (blue→indigo) | 18 |
| Vault (`/vault`) | `#f59e0b→#fbbf24` (amber→gold) | 10 |
| Upgrade (`/plans`) | Keep existing purple→pink gradient | locked nodes |
| Coming Soon | `#64748b` (slate) — muted, no action | 17,19,20,21,22 |

**How it works**: Add a `productGradient` field to each trail node in `trailData.js`. The tooltip reads it for the CTA button background.

**Tailwind equivalent**: `bg-gradient-to-r from-[#f5a623] to-[#ff6b6b]`

---

### Change 2: Unify dark backgrounds

**Current**: Three different darks — `#000000` (app), `#020617` (trail), `#0a0f1e` (tooltip).

**Proposed**: Use `#000000` everywhere. It's the app standard, the deepest black, and matches iOS dark mode conventions. The trail board already renders zone background bands over the page background — those create the visual richness, not the base colour.

| Component | Current bg | Proposed bg |
|-----------|-----------|-------------|
| AppLayout | `#000000` | `#000000` (no change) |
| TrailHomePage | `#020617` | `#000000` |
| TrailTooltip | `#0a0f1e` | `#000000` with `border-top: 2px solid {zone.color}` |

The tooltip gets a **zone-coloured top border** — this preserves the zone identity while the CTA shows the product identity. Zone badge stays zone-coloured. CTA button is product-coloured.

---

### Change 3: Zone colour accent in tooltip header

**Current**: Tooltip shows node icon + label + description. No zone colour reference.

**Proposed**: Add a subtle zone tint to the tooltip header area:
- `background: linear-gradient(180deg, rgba({zone.color}, 0.08) 0%, transparent 100%)`
- This creates a gentle wash of the zone colour at the top that fades to black
- Combined with the product-coloured CTA at the bottom, the tooltip bridges zone→product

---

### What stays the same

- Trail board zone colours — unchanged (teal, amber, purple, green, pink, slate)
- Trail board zone background gradient bands — unchanged
- Zone node circle colours — unchanged
- Tier lock badges — unchanged (cyan/purple/amber/slate)
- Badge bar — unchanged (amber gold for earned)

---

### Visual Flow (user perspective)

```
TRAIL BOARD                    TOOLTIP                       DESTINATION
(zone colours)                 (bridge)                      (product colours)

 [Teal node] ──tap──→  ┌─ Zone tint (teal wash) ─┐  ──→  FamiliLook
                        │  Node: Upload Photos    │       (amber/coral)
                        │  Description text       │
                        │                         │
                        │  [Try It Now ▸]         │
                        │  (amber→coral gradient) │
                        └─────────────────────────┘
```

The user sees: teal zone → teal-tinted tooltip → amber CTA button → amber app. The CTA colour prepares their eye for the destination.

---

### Accessibility

- CTA button text remains white (#fff) on all gradients — contrast ratio ≥ 4.5:1 verified for all product gradients against white text
- Zone tint at 8% opacity does not affect text readability
- No colour-only information — icons and text labels always present

---

**Handoff: Design Lead → FE Lead**
