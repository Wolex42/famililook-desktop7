# Change Request Package — Keepsake Product Fixes (Batch)

```
═══════════════════════════════════════════════════════════════
  CHANGE REQUEST — CR-0007 (Batch: 4 items)
  Date: 2026-04-01
  Author: Change Manager
═══════════════════════════════════════════════════════════════

RISK TIER: P2 — Standard
CHANGE TYPE: Code (Frontend only)
PRODUCT: FamiliLook — Keepsakes Module
SOURCE: QA Lead investigation + Visual Director audit (keepsake_issues_plan_of_attack.md)

═══════════════════════════════════════════════════════════════
  ITEM 1: FMEA-KSK-01 — Card Products in Keepsake Catalogue
═══════════════════════════════════════════════════════════════

DESCRIPTION:
  standard_card and card_deck entries appear in the keepsake catalogue
  but are FamiliUno products. card_deck has useLegacyTemplates: true
  with empty components — preview cannot render.

CONTEXT:
  FMEA-KSK-01 | S:4 O:10 D:2 | RPN: 80
  User confusion — cards appear where they shouldn't

ACTION REQUIRED:
  - Add hideFromCatalogue: true to standard_card and card_deck in productCatalog.js
  - KeepsakeCatalogue.jsx: filter out products with hideFromCatalogue flag
  - DO NOT delete the entries — FamiliUno deck ordering pipeline depends on them

FILES:
  1. famililook-desktop2/src/components/keepsakes/utils/productCatalog.js
     — Add hideFromCatalogue: true to standard_card and card_deck entries
  2. famililook-desktop2/src/components/keepsakes/mobile/KeepsakeCatalogue.jsx
     — Filter products where hideFromCatalogue === true

BLAST RADIUS: Low — catalogue display only, no order pipeline impact
EFFORT: XS (30 minutes)

═══════════════════════════════════════════════════════════════
  ITEM 2: FMEA-KSK-02 — Mug Text Overflow
═══════════════════════════════════════════════════════════════

DESCRIPTION:
  Text spills outside containers on mug graphics. Long child names
  overflow the 170px SVG rect in MugCeramicPreview. Headlines in
  CharacterMugTemplate truncated at 35 chars but rendered at 36-42px
  uppercase — overflows 341px panel.

CONTEXT:
  FMEA-KSK-02 | S:7 O:6 D:3 | RPN: 126
  Broken visual layout visible to users at purchase decision point

ACTION REQUIRED:
  1. MugCeramicPreview.jsx — Add SVG <clipPath> to hero text area
  2. CharacterMugTemplate.jsx — Reduce headline max chars OR reduce font size
     on narrow panels, add overflow: hidden + textOverflow: ellipsis
  3. characterHeadlines.js — Verify/adjust max character limits for headlines

FILES:
  1. famililook-desktop2/src/components/keepsakes/MugCeramicPreview.jsx
     — Add SVG clipPath to contain hero text
  2. famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx
     — Fix headline overflow (reduce max chars or font size)
  3. famililook-desktop2/src/components/keepsakes/utils/characterHeadlines.js
     — Adjust character limits if needed

BLAST RADIUS: Medium — affects mug preview and print output for all mug orders.
  Must verify all 4 layout variants (Celebration, Heritage, Carnival, Ubuntu).
EFFORT: M (2-3 hours)

═══════════════════════════════════════════════════════════════
  ITEM 3: FMEA-KSK-03 Phase 1 — AI Message Toggle Ungated
═══════════════════════════════════════════════════════════════

DESCRIPTION:
  The personalised message toggle appears in the mobile flow for ALL
  products, even those that do NOT support custom messages. Users can
  toggle it ON and pay the £1.99 surcharge for a feature that renders
  nothing on their product.

CONTEXT:
  FMEA-KSK-03 | S:9 O:6 D:2 | RPN: 108
  Revenue risk — charging for invisible feature. Trust risk.
  Phase 1 only: gate the toggle. Phase 2 (rendering) deferred pending
  Visual Director spec.

ACTION REQUIRED:
  - KeepsakeCustomise.jsx: Only show personalised message toggle when
    the selected template has supportsCustomMessage: true in templateRegistry
  - Desktop modal (KeepsakesModal.jsx) already gates correctly — no change needed

FILES:
  1. famililook-desktop2/src/components/keepsakes/mobile/KeepsakeCustomise.jsx
     — Gate toggle on supportsCustomMessage from templateRegistry

BLAST RADIUS: Low — toggle visibility only, no template rendering changes
EFFORT: XS (30 minutes)

═══════════════════════════════════════════════════════════════
  ITEM 4: FMEA-KSK-04 — Transparent Preview Backing
═══════════════════════════════════════════════════════════════

DESCRIPTION:
  Templates with transparent backgrounds (especially CushionTemplate)
  are hard to see on the dark preview screen. CushionTemplate uses
  light gray text for feature badges — invisible on dark background.

CONTEXT:
  FMEA-KSK-04 | S:5 O:8 D:3 | RPN: 120
  Users cannot see what they're buying on preview screen

ACTION REQUIRED:
  1. KeepsakePreview.jsx — Add subtle light backing behind templates
     with transparent backgrounds (preview-only, not in export)
  2. CushionTemplate.jsx — Use darker text colour for feature badges

FILES:
  1. famililook-desktop2/src/components/keepsakes/mobile/KeepsakePreview.jsx
     — Add preview-only light backing for transparent templates
  2. famililook-desktop2/src/components/keepsakes/templates/Products/Home/CushionTemplate.jsx
     — Fix badge text colour to be visible on any background

BLAST RADIUS: Low — preview display only, export pipeline unchanged
EFFORT: S (1 hour)

═══════════════════════════════════════════════════════════════
  BATCH VALIDATION SUMMARY
═══════════════════════════════════════════════════════════════

TOTAL FILES IN SCOPE: 8
TOTAL ITEMS: 4 (KSK-01 through KSK-04, with KSK-03 Phase 1 only)

VALIDATION:
  [PASS] Traceability: All items map to FMEA IDs (KSK-01 through KSK-04)
  [PASS] Scope validation: All 8 files returned Exit 0 (ALLOWED)
  [PASS] Working set: Updated with all 8 target files
  [PASS] Contract impact: NONE — no kinship_analyze.v1 or compare_faces.v1 contact
  [PASS] Backend changes: NONE — all files are frontend (desktop2 .jsx/.js only)
  [PASS] Blast radius: 8 files, single repo (desktop2), no cross-repo impact
  [N/A]  ops_report: Will be generated after implementation
  [N/A]  Tests: Will run after implementation (Step 3)

CONTRACTS AFFECTED: None
BACKEND CHANGES: No
ROLLBACK: git revert on the single commit (all 4 fixes in one atomic commit)

RISK ASSESSMENT:
  - All changes are P2 (Standard): within existing patterns, no new
    dependencies, no contract impact, frontend-only
  - No P1/P0 items — CEO gate not required for scope approval
  - Change Manager pre-validates and presents with APPROVE recommendation

RECOMMENDATION: APPROVE
  All 4 items are well-scoped frontend fixes with clear root causes
  documented in the plan of attack. No backend files touched, no
  frozen contracts affected. Combined effort ~4-5 hours.

CONDITIONS:
  - All 4 layout variants (Celebration, Heritage, Carnival, Ubuntu) must
    be visually verified for KSK-02 mug text overflow fix
  - KSK-03 Phase 2 (message rendering) is explicitly OUT OF SCOPE —
    deferred pending Visual Director specification
  - Export pipeline must remain unchanged for KSK-04 (backing is preview-only)

═══════════════════════════════════════════════════════════════
  HANDOFF: change_manager -> qa_lead
═══════════════════════════════════════════════════════════════

TASK: Reproduce and assess all 4 bugs (batch mode Step 2)
CONTEXT: Scope approved, working set updated, risk tier P2 assigned
ARTIFACTS:
  - Agent_1/crew/output/keepsake_fixes_change_request.md (this document)
  - Agent_1/crew/output/keepsake_issues_plan_of_attack.md (root cause analysis)
DECISIONS MADE: Risk tier P2, file scope (8 files), rollback = git revert
OPEN QUESTIONS: Root cause confirmation, regression risk per item

═══════════════════════════════════════════════════════════════
```
