# COO Feasibility Note: Family Identity Profiles

**Author:** COO (Agent)  
**Date:** 2026-04-05  
**Inputs:** PRD_FAMILY_IDENTITY_PROFILES.md, TECH_FAMILY_IDENTITY_FEASIBILITY.md

---

## 1. Operational Impact

- **Vendors (Prodigi, QPMarkets):** NONE. Feature is entirely FE-side. Character illustration selection changes which PNG is composited onto the mug/card, but the Prodigi SKU, artwork upload API, and QPMarkets manifest format are all unchanged. No vendor coordination required.
- **Payment flow:** NONE. No new products, no price changes, no Stripe schema changes.
- **Backend:** NONE. Phase 1 explicitly avoids backend changes. The `kinship_analyze.v1` and `compare_faces.v1` contracts are untouched. Role/age/ethnicity are FE-only metadata for keepsake rendering.
- **localStorage:** New key `fl:family-profiles` added. Cookie policy (`public/cookie-policy.html`) documents 35+ keys — this needs a one-line addition. Low effort.

**Verdict:** Operationally clean. No vendor, payment, or backend risk.

## 2. Conflicts with Active Work

Active priorities from `project_next_session_priorities.md`:
- **Phase C activation** (flag ON + deploy + manual test) — no file overlap with Identity Profiles.
- **Smart Photo Selection Phase 3** (5-7 days, next build) — touches upload flow and PhotoSlot. Identity Profiles also touch UploadSection and PhotoSlot. **CONFLICT: concurrent changes to upload UX would create merge risk and QA complexity.**
- **Phase C error polish** (1 day) — touches creation flow, not upload. No conflict.

**Verdict:** DEFER until Smart Photo Phase 3 is merged or sequence them explicitly. Running both in parallel on the upload flow invites regressions.

## 3. Revenue Impact

- **Positive:** Structured profiles improve character accuracy (60% to 90%+ per PRD). Accurate mugs = fewer "that doesn't look like us" abandonments. Returning user flow ("Welcome back") increases repeat purchases — target 1.0 to 1.3 products/session.
- **Positive:** "Add another family member" prompt is a natural upsell hook aligned with the product-led pivot (sell the mug, not the engine).
- **Neutral:** No new SKUs or pricing changes. Revenue uplift comes from conversion, not catalogue expansion.
- **Risk:** If the Identity Sheet adds perceived friction (even though optional), upload-to-analyse conversion could dip. The 0% upload conversion baseline (per `project_upload_conversion.md`) means we cannot afford ANY friction increase.

**Verdict:** Net positive for revenue, but only if the sheet is genuinely zero-friction. Must be invisible to users who don't want it.

## 4. Timeline Risk

FE Lead estimates 10h across ~10 files changed and ~3 new files (~500 lines + ~200 lines tests).

- **Realistic?** The estimate is credible for a senior dev in isolation. However:
  - Blast radius spans 6 core modules (UploadSection, FamililookContext, stateNormalization, KeepsakeCustomise, compositionEngine, characters/index).
  - Per lessons learnt (Sprint 0A-4D), any edit touching FamililookContext has historically caused cascade regressions (3 incidents).
  - Mobile viewport testing on KeepsakeCustomise (scroll overflow risk at 375px) adds 1-2h not accounted for.
  - The "Welcome back" banner UX needs design review — not costed.
- **Adjusted estimate:** 12-14h with mobile QA and banner design. 10h is optimistic.

## 5. Recommendation: SPLIT

| Phase | Scope | Effort | Ship when |
|-------|-------|--------|-----------|
| **1A** | Context schema + composition engine structured input + tests | 3h | After Phase C activation |
| **1B** | Identity Sheet UI + role/age/ethnicity capture + upload integration | 5h | After Smart Photo Phase 3 |
| **1C** | Character picker in KeepsakeCustomise + localStorage profiles + welcome banner | 4h | After 1B validated |

**Rationale:**
- 1A is invisible to users but unlocks structured data in the composition engine. Zero UX risk. Can ship immediately after Phase C goes live.
- 1B is the user-facing feature. Must NOT overlap with Smart Photo Phase 3 on the upload flow.
- 1C is the retention play. Only worth building after 1B proves adoption (target: 40% of sessions use structured profiles within 30 days).

**Gate:** Do not proceed to 1C unless 1B achieves >20% structured profile usage in first 14 days.
