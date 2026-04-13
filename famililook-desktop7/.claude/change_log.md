# Change Log — famililook-desktop7 (FamiliMatch Backend)

All changes must be logged here with validation status.
Format: Description / Context / Action (D/C/A)

---

## 2026-04-13 — Cross-repo impact from desktop6 Phase A1 (CR-MATCH-A1-04)

**Description:** Added `https://familimatch.com`, `https://www.familimatch.com`, and `https://famililook-desktop6.vercel.app` to CORS `ALLOWED_ORIGINS` default in `app/main.py`. FamiliMatch is moving to its own domain — without this, WebSocket and API calls from familimatch.com would be blocked.
**Risk Tier**: P1
**Approved by**: CEO (backend permission granted for CORS task)
**Status**: CLOSED

---

## 2026-03-31 | Sprint 2: DFMEA + Gap Analysis Fixes (CR-0009)

**Risk Tier**: P2
**Approved by**: CEO
**Executed by**: FE Lead agent | **Verified by**: QA Lead agent

| Date | Repo | Type | Description | Ref | Tier | Approver | Status |
|------|------|------|-------------|-----|------|----------|--------|
| 2026-03-31 | desktop7 | Code | FM-009: Added verify_tier_token() to main.py, gates CREATE_ROOM for duo/group on Plus tier | FM-009 | P2 | CEO | CLOSED |
| 2026-03-31 | desktop7 | Code | DFMEA-FM-05: Added REJOIN_ROOM protocol to protocol.py, disconnect_player/rejoin_player to rooms.py, rejoin handler to main.py | DFMEA-FM-05 | P2 | CEO | CLOSED |

---
