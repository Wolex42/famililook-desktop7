# Bug: Children photos skipped despite green badge at upload

> **Date**: 2026-04-04
> **Priority**: P0 — blocks core product flow
> **Status**: OPEN — needs orchestrated agent investigation
> **Reporter**: CEO (live testing)

---

## Symptoms

1. User uploads 2 parent photos + 2 child photos
2. All 4 photos show GREEN badge (✓) at upload time — faces detected, embedding_ok
3. User taps "Analyze Family"
4. Analysis returns: "2 photo(s) skipped: face not clearly detected. Try a clearer, front-facing photo."
5. The 2 CHILDREN were skipped — parents worked fine

## What we already fixed (2026-04-02)

- `/detect` endpoint aligned with `/kinship/analyze` — both now use `engine.get_faces()`
- `load_bgr()` has `seek(0)` safety net
- Distinct skip reasons: "Face detected but couldn't be analysed" vs "No face detected"

## But the problem persists

The green badge at upload means `/detect` returned `embedding_ok: true`. But `/kinship/analyze` still skips the same photos. This means either:
1. The compression/resize between upload and analysis degrades the photo further
2. The engine pool round-robin hits different engines with different states
3. The children's photos are marginal quality — passing `/detect` threshold but failing the full kinship pipeline
4. Race condition: engine state changes between detect and analyze calls

## Evidence needed

- Backend logs during the failed analysis — which engine handled it? Did InsightFace or MediaPipe process the children?
- The exact `det_score` and `embedding` status for each child photo at `/detect` time vs `/kinship/analyze` time
- Whether `compressPhoto()` is degrading the children's photos more than the parents'

## Agent assignments

| Agent | Task |
|-------|------|
| qa_lead | Reproduce the issue with test photos. Trace the full pipeline: upload → detect → compress → analyze. Log every step. |
| fe_lead (BE) | Add detailed logging to `_face_from_upload()` in main.py — log det_score, embedding size, engine index for each photo |
| fe_lead (FE) | Check if children photos go through additional processing (crop from FacePicker?) that parents don't |
| qa_lead | Compare the exact bytes sent to `/detect` vs `/kinship/analyze` — are they the same file? |

## Key question

Are the children's photos being sent to `/kinship/analyze` as the FacePicker-cropped version (800x800 JPEG) or the original compressed version? If FacePicker cropped them, the crop may have lost quality.
