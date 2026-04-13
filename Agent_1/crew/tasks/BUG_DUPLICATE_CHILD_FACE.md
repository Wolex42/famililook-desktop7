# Bug: Same child face displayed for both children in results

> **Date**: 2026-04-04
> **Priority**: P0 — incorrect results shown to users
> **Status**: OPEN
> **Reporter**: CEO (live testing)

## Symptoms

1. User uploads 2 parents + 2 different children
2. Analysis completes successfully
3. Results show correct feature breakdown per child
4. BUT both result cards display the SAME child's face photo
5. "Your Child" and "Child 2" show identical thumbnail

## Investigation needed

### Frontend: Photo → FormData mapping
- In `useKinshipAnalysis.jsx`, how are child photos mapped to FormData fields?
- Are children sent as `children[0]`, `children[1]` or as named fields?
- Is the photo for Child 1 vs Child 2 correctly indexed?

### Backend: Photo → Result mapping
- In `main.py kinship_analyze()`, how does the backend associate results with specific children?
- Does the response preserve the child ordering from the request?
- Is the child's name/photo preserved in the result object?

### Frontend: Result → Display mapping
- In `MobileResultsCarousel.jsx`, how are child result cards matched to uploaded photos?
- Does it use child index, child name, or photo reference?
- Are thumbnails pulled from the result object or from the upload state?

## Key question
Is the issue in the UPLOAD (same file sent twice), the ANALYSIS (backend mixed them up), or the DISPLAY (frontend showing wrong photo)?

Check the downloaded JSON at `c:\Users\wole\Downloads\family-results-2026-04-04.json` for clues.
