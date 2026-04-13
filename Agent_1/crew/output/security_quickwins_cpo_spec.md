## CPO Spec: Security Quick Wins — 4 Fixes, All S Effort

**Agent**: CPO
**Date**: 2026-03-23
**Context**: Security assessment flagged these as MEDIUM severity, all S effort. Ship together.

---

### Fix M17: innerHTML XSS in exportResults.js
- **Risk**: `card.ownerName` is user-supplied, inserted via innerHTML. Attacker could inject `<script>` or event handlers.
- **Fix**: Replace innerHTML with textContent or DOM API.
- **File**: src/utils/exportResults.js (desktop2)

### Fix M20: Rate limiting on payment endpoints
- **Risk**: No rate limit on Stripe checkout creation. Attacker could spam `POST /payments/create-checkout-session`.
- **Fix**: Add rate limiter middleware to payment routes (e.g., 5 requests/minute per IP).
- **File**: app/payments.py (desktop3) — **BACKEND, needs permission**

### Fix M21: Docker containers run as root
- **Risk**: Container compromise = root on host (in theory). Defense-in-depth.
- **Fix**: Add `USER` directive to Dockerfiles for desktop3 and desktop7.
- **Files**: famililook-desktop3/Dockerfile, famililook-desktop7/Dockerfile — **BACKEND, needs permission**

### Fix M19: Thumbnails in localStorage (not sessionStorage)
- **Risk**: Face thumbnails persist across sessions longer than necessary.
- **Fix**: Move `fl:thumbnails` from localStorage to sessionStorage. Clear on session end.
- **File**: src/utils/photoUtils.js (desktop2)

---

**Scope**: desktop2 (FE) + desktop3 (BE) + desktop7 (BE)
**Effort**: S per fix, half day total

**Handoff: CPO → Security (verify fixes) → FE Lead (M17, M19) + BE Lead (M20, M21)**
