# CR-0012: Family Identity Profiles — Feature Summary

## What was built

Structured identity capture for family members during photo upload, feeding into keepsake personalisation. Three sub-phases:

1. **Composition Engine Wiring (A)** — Extended state normalisation with age/ethnicity/structuredRole defaults. Added 6 context helpers. Composition engine now prefers explicit winnerRole and respects winnerEthnicity for character selection.

2. **Identity Sheet UI (B)** — Bottom sheet component (`IdentitySheet.jsx`) for capturing role, name, age group, and ethnic variant per family member. Wired into UploadSection with role badges on PhotoSlot.

3. **Character Picker (C)** — Inline character + emotion picker (`CharacterPicker.jsx`) integrated into KeepsakeCustomise. Featured Card, Emotion Strip, and Role Chips. Auto-defaults from recipient identity data.

## How to activate

1. Set `VITE_FAMILY_PROFILES=true` in Vercel environment variables (desktop2 project)
2. Deploy: merge `main` into `production`, push
3. Feature is OFF by default — zero impact on production until flag is enabled

## How to test

1. With flag ON: upload photos, tap a PhotoSlot role badge to open IdentitySheet
2. Fill in role/name/age/variant, confirm
3. Run analysis, navigate to keepsakes
4. In KeepsakeCustomise for a character_mug, verify CharacterPicker shows with correct defaults
5. Automated: `npm run test:run` — 1,346 tests (32 new for this CR)

## How to rollback

Set `VITE_FAMILY_PROFILES=false` in Vercel and redeploy. All code paths fall back to existing behaviour. No database migrations, no backend changes.

## Backlog items (from QA review)

1. **Keyboard navigation** — CharacterPicker needs arrow-key support for accessibility
2. **Animation polish** — IdentitySheet spring transition for smoother open/close
3. **Analytics events** — identity_sheet_opened, identity_saved, character_selected funnel events

## Artifacts produced

| Artifact | Path |
|---|---|
| Change log entries | `.claude/change_log.md` (3 sub-phase entries + closure entry) |
| Sub-phase A output | `Agent_1/crew/output/family_identity_fe_subphase_a.md` |
| Sub-phase B output | `Agent_1/crew/output/family_identity_fe_subphase_b.md` |
| Sub-phase C output | `Agent_1/crew/output/family_identity_fe_subphase_c.md` |
| This summary | `Agent_1/crew/output/family_identity_summary.md` |
| Memory file | `~/.claude/projects/.../memory/project_family_identity_profiles.md` |
| PRD | `Agent_1/crew/tasks/PRD_FACE_ANCHORED_NAMING.md` |
| Composition study | `Agent_1/crew/tasks/CHARACTER_MUG_COMPOSITION_STUDY.md` |
