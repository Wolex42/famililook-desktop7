# Change Log — famililook-desktop7 (FamiliMatch Backend)

All changes must be logged here with validation status.
Format: Description / Context / Action (D/C/A)

---

## 2026-04-13 — Phase A3: Challenge a Friend backend (CR-MATCH-A3)

**Risk Tier**: P1 (growth feature)
**Approved by**: CEO (backend permission for desktop7: POST /challenge/create, GET /challenge/{id}, POST /challenge/{id}/accept)
**Executed by**: BE Lead agent

| Date | Repo | Type | Description | Ref | Tier | Status |
|------|------|------|-------------|-----|------|--------|
| 2026-04-13 | desktop7 | Code | NEW app/challenges.py: create, get, accept endpoints. In-memory store, 7-day TTL, 10/IP rate limit | CR-MATCH-A3-01 | P1 | CLOSED |
| 2026-04-13 | desktop7 | Code | main.py: import + register challenges_router | CR-MATCH-A3-02 | P3 | CLOSED |
| 2026-04-13 | Hetzner | Config | Caddyfile: added /challenge/* → match-server:8030 route | CR-MATCH-A3-03 | P2 | CLOSED |

**Tests**: 111/120 passed (9 pre-existing protocol count failures from prior session). Quality floor maintained.

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
