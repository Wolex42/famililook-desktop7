# Platform Security Assessment — Consolidated

**Document ID**: SA-004
**Date**: 2026-03-07 (updated from 2026-02-27)
**Scope**: Full platform (desktop2-desktop7, all 4 products) + commerce layer (Stripe, Prodigi)
**TARA Alignment**: TARA-FM-003 (T-01 to T-14), Risk Register R1-R28
**Status**: CURRENT — Investor-ready audit

---

## Executive Summary

The famili platform has a **strong privacy-by-design architecture** (no cloud AI, no third-party data sharing, in-memory-only photo processing) protected by **good perimeter defenses** (security headers, source map stripping, robots.txt, TLS via Caddy). The February 2026 sprint closed **12 critical/high findings**. The March 2026 update adds the commerce layer (Stripe payments, Prodigi fulfilment) which introduces **4 new findings** (N-12 to N-15), all LOW-MEDIUM severity.

**Current posture**: T-11 marketing claims FIXED (2026-03-27). T-16 GDPR deletion FIXED (2026-03-27). COPPA age gate deployed (2026-03-27). DPIA written. Incident Response Plan written. 1 high-severity open item (T-05: server-side consent), 6 medium items. Commerce layer is well-secured with server-side price validation and webhook signature verification.

---

## TARA Alignment — Status Update

### TARA-FM-002 (FamiliMatch Gen 3) — Last reviewed: 2026-02-23

| ID | Threat | Original Status | Current Status | Notes |
|----|--------|----------------|----------------|-------|
| T-01 | Photo interception (WebSocket) | DESIGNED | **MITIGATED** | Caddy TLS live on Hetzner; Vercel WSS by default |
| T-02 | Room code guessing | NOT STARTED | **MITIGATED** | 6-char alphanumeric codes (2.18B combinations) + `secrets` RNG + 5/min rate limit. Implemented 2026-02-27 |
| T-03 | Photos persist in RAM after close | NOT STARTED | **OPEN** | `clear_data()` exists but no `gc.collect()` or zero-fill |
| T-04 | Desktop3 retains embeddings | CLOSED | CLOSED | `/compare/faces` has no GALLERY |
| T-05 | Consent bypass via direct API | NOT STARTED | **OPEN** | No server-side consent validation |
| T-06 | Player screenshots photo | NOT STARTED | **ACCEPTED** | Social contract; ToS clause needed |
| T-07 | Room flooding / DoS | NOT STARTED | **PARTIAL** | Join rate limit added; creation rate limit still missing |
| T-08 | Analytics without consent | IMPLEMENTED | IMPLEMENTED | Consent-gated analytics live |

### TARA-FP-002 (Gen 1 Privacy & Security) — Last reviewed: 2026-02-13

| ID | Threat | Original Status | Current Status | Notes |
|----|--------|----------------|----------------|-------|
| T-09 | Unencrypted transmission | CRITICAL | **MITIGATED** | Caddy auto-TLS on Hetzner; all FEs on Vercel HTTPS |
| T-10 | No API authentication | HIGH | **PARTIAL** | API key middleware exists in desktop3, but **disabled if env var empty** |
| T-11 | "Never leaves device" claim | CRITICAL | **FIXED** | All claims corrected across 3 repos (2026-03-27). Now reads "processed securely on EU servers — never stored" |
| T-12 | CORS wildcard | HIGH | **MITIGATED** | CORS restricted to specific origins (localhost + production domains) |
| T-13 | No CSRF protection | MEDIUM | **CLOSED** | Mitigated by architecture (stateless API, no cookies, allow_credentials=False) |
| T-14 | Thumbnails in localStorage | MEDIUM | **OPEN** | Still uses localStorage, not sessionStorage |
| T-15 | Analytics leaks patterns | LOW | **MITIGATED** | HTTPS enforced, IP anonymized |
| T-16 | No data deletion (GDPR) | HIGH | **FIXED** | POST /data/forget-me covers 6 data stores (2026-03-27) |

---

## New Findings (Not in Existing TARAs)

### N-01: API auth disabled by default on Desktop3

**Severity**: CRITICAL

Desktop3's API key middleware skips authentication when `FAMILILOOK_API_KEY` env var is empty:
```python
# app/main.py
API_KEY = os.getenv("FAMILILOOK_API_KEY", "")
# middleware: if not API_KEY: return await call_next(request)  # BYPASSES AUTH
```

If the env var is not set in production Docker config, **all endpoints are fully open** including `/kinship/analyze`, `/detect`, `/embed`, `/orders/*`.

**TARA Cross-ref**: Elevates TARA-FP-002 T-10 from PARTIAL to CRITICAL.

**Fix**: Fail startup if API key not set in production:
```python
if os.getenv("ENVIRONMENT") == "production" and not API_KEY:
    raise RuntimeError("FAMILILOOK_API_KEY required in production")
```

---

### N-02: Photo upload has no size limit (DoS)

**Severity**: CRITICAL

Desktop7 accepts base64 photo data via WebSocket with **no size validation before decoding**:
```python
photo_b64 = data.get("photo", "")
photo_bytes = base64.b64decode(photo_b64)  # no size check
```

An attacker can send a 1GB base64 string, causing the server to allocate ~750MB of RAM per decode. With 6 players in a group room, this becomes ~4.5GB.

Desktop3 has a `MAX_UPLOAD_MB = 10` check in its middleware, but this only applies to HTTP requests — not to the Desktop7 WebSocket pipeline.

**TARA Cross-ref**: New finding. Extends TARA-FM-002 T-07 (DoS).

**Fix**: Validate base64 length before decoding:
```python
MAX_PHOTO_B64_LEN = 10 * 1024 * 1024 * 4 // 3  # ~10MB decoded
if len(photo_b64) > MAX_PHOTO_B64_LEN:
    await send(error_msg("Photo too large (max 10MB)"))
    continue
```

---

### N-03: No WebSocket connection limit per IP

**Severity**: HIGH

Desktop5 and Desktop7 accept unlimited WebSocket connections per IP address. An attacker can open thousands of concurrent connections, exhausting server memory and file descriptors.

**TARA Cross-ref**: Extends TARA-FM-002 T-07 (DoS).

**Fix**: Track connections per IP in a global dict; reject connections beyond threshold (e.g., 10 per IP).

---

### N-04: Deck size unbounded in Desktop5

**Severity**: HIGH

Desktop5 validates minimum deck size (`len(deck) < 4`) but **no maximum**. An attacker can send a deck with millions of cards, causing OOM:
```python
deck = msg.get("deck", [])
if not deck or len(deck) < 4:  # no upper bound
```

**Fix**: `if len(deck) > 52: return error_msg("Deck too large (max 52 cards)")`

---

### N-05: Player names have no length limit

**Severity**: MEDIUM

Both desktop5 and desktop7 accept player names without length validation. A 1MB player name would be broadcast to all room participants, consuming bandwidth and potentially crashing clients.

**Fix**: `name = data.get("name", "Player")[:30]`

---

### N-06: No Content Security Policy on Vercel deployments

**Severity**: MEDIUM

All three Vercel deployments have X-Frame-Options, X-XSS-Protection, etc., but **no CSP header**. This allows injected scripts to execute if an XSS vector is found.

**Fix**: Add CSP to all vercel.json headers:
```
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; connect-src 'self' https://<backend-domain>
```

---

### N-07: innerHTML with user data in exportResults.js

**Severity**: MEDIUM

`famililook-desktop2/src/utils/exportResults.js` uses `innerHTML` with `card.ownerName` (from localStorage):
```javascript
cardEl.innerHTML = `... <div class="card-name">${card.ownerName || "Family Member"}</div> ...`;
```

If `ownerName` contains HTML, this is an XSS vector.

**TARA Cross-ref**: Extends TARA-FP-002 T-07 (XSS via names). React JSX escapes, but this is raw DOM manipulation outside React.

**Fix**: Use `textContent` or `createElement` instead of `innerHTML`.

---

### N-08: VITE_ADMIN_KEY exposed in frontend bundle

**Severity**: MEDIUM

The admin dashboard gate (`/dashboard?key=fl-admin-2026`) uses a key embedded in the Vite define block. Anyone reading the JS bundle can extract it.

**Fix**: Move admin auth to backend (JWT or session-based).

---

### N-09: Error messages echo user input

**Severity**: LOW

Both WebSocket servers echo user-supplied values in error messages:
```python
await ws.send_json(error_msg(f"Room {code} not found"))
await ws.send_json(error_msg(f"Unknown message type: {msg_type}"))
```

If a client renders these without escaping, it could be an XSS vector.

**Fix**: Use generic error messages without echoing input.

---

### N-10: No room creation rate limit

**Severity**: MEDIUM

Join attempts are now rate-limited (5/min), but room **creation** has no limit. An attacker can create thousands of empty rooms, exhausting the room pool.

**TARA Cross-ref**: TARA-FM-002 T-07 recommended "max 3 rooms per IP per hour" — not yet implemented.

**Fix**: Track room creation per connection; limit to 3 per hour.

---

### N-11: Docker containers run as root

**Severity**: LOW

No explicit `USER` directive in Dockerfiles. Containers inherit the default user (typically root).

**Fix**: Add `RUN useradd -r app && USER app` to Dockerfiles.

---

### N-12: Keepsake image endpoint has no authentication

**Severity**: LOW

`GET /orders/images/{order_id}.png` serves keepsake print images without authentication — by design, for Prodigi to download. Order IDs are UUIDs (2^128 possibilities), making enumeration infeasible. However, if an order ID leaks (e.g., in logs or URLs), the image is accessible to anyone.

**TARA Cross-ref**: TARA T-11.

**Fix**: Consider time-limited signed URLs (HMAC + expiry) for defense-in-depth. Not urgent — UUID randomness is sufficient for current scale.

---

### N-13: Stripe secret key in Docker environment

**Severity**: LOW

The Stripe secret key (`sk_live_*`) is passed as an environment variable to the Docker container. If the container is compromised, the attacker has full Stripe API access.

**Fix**: Use Docker secrets or a vault (e.g., HashiCorp Vault) for production keys. For current scale, env vars are acceptable with container hardening (N-11 non-root user).

---

### N-14: No rate limiting on payment endpoints

**Severity**: MEDIUM

`POST /payments/create-checkout-session` and `POST /payments/create-basket-checkout` have no rate limiting. An attacker could create thousands of Stripe checkout sessions, potentially triggering Stripe rate limits or incurring Stripe fees.

**Fix**: Rate limit payment endpoints to 10/minute per IP. Add CAPTCHA or challenge for high-volume checkout attempts.

---

### N-15: Personalised message content not sanitised before print

**Severity**: LOW

LLM-generated personalised messages are rendered directly in keepsake templates. While XSS is not a concern (templates are server-rendered to PNG), inappropriate content could be printed on physical products.

**TARA Cross-ref**: TARA T-13.

**Fix**: Add content moderation (keyword blocklist or LLM classification) before allowing message onto keepsake template.

---

## Consolidated Risk Matrix

### Critical (Must fix before public launch)

| ID | Finding | Component | TARA Ref | Status |
|----|---------|-----------|----------|--------|
| N-01 | API auth disabled by default | Desktop3 | T-10 | **MITIGATED** (startup guard, 2026-02-27) |
| N-02 | Photo upload no size limit | Desktop7 | T-07 ext | **MITIGATED** (10MB limit, 2026-02-27) |
| T-11 | "Never leaves device" marketing claim | All | T-11 | **FIXED** (2026-03-27) |

### High (Fix within 2 weeks)

| ID | Finding | Component | TARA Ref | Status |
|----|---------|-----------|----------|--------|
| N-03 | No WebSocket connection limit | Desktop5, 7 | T-07 ext | **MITIGATED** (10/IP, 2026-02-27) |
| N-04 | Deck size unbounded | Desktop5 | New | **MITIGATED** (max 52 cards, 2026-02-27) |
| T-03 | Photos persist in RAM | Desktop7 | T-03 | **MITIGATED** (gc.collect + zero-fill, 2026-02-27) |
| T-16 | No GDPR data deletion | Desktop3 | T-16 | **FIXED** — POST /data/forget-me covers 6 data stores (2026-03-27) |
| N-10 | No room creation rate limit | Desktop5, 7 | T-07 | **MITIGATED** (3/hour/conn, 2026-02-27) |
| T-05 | Consent bypass via direct API | Desktop3 | T-05 | **OPEN** |

### Medium (Fix within 1 month)

| ID | Finding | Component | TARA Ref | Status |
|----|---------|-----------|----------|--------|
| N-05 | Player names no length limit | Desktop5, 7 | New | **MITIGATED** (30 char cap, 2026-02-27) |
| N-06 | No CSP on Vercel | Desktop2, 4, 6 | New | **MITIGATED** (CSP added, 2026-02-27) |
| N-07 | innerHTML with user data | Desktop2 | T-07 ext | **OPEN** |
| N-08 | Admin key in FE bundle | Desktop2 | New | **FIXED** — SHA-256 hash verification, raw key removed from bundle (2026-03-26) |
| T-13 | No CSRF protection | Desktop3 | T-13 | **CLOSED** — mitigated by architecture (stateless API, no cookies, allow_credentials=False) |
| T-14 | Thumbnails in localStorage | Desktop2 | T-14 | **OPEN** |
| N-09 | Error messages echo input | Desktop5, 7 | New | **OPEN** |
| N-11 | Docker runs as root | Desktop3, 5, 7 | New | **OPEN** |
| N-14 | No rate limit on payment endpoints | Desktop3 | New | **OPEN** |

### Low (Monitor / best-practice)

| ID | Finding | Component | TARA Ref | Status |
|----|---------|-----------|----------|--------|
| N-12 | Keepsake image endpoint unauthenticated | Desktop3 | T-11 | **ACCEPTED** (UUID protection) |
| N-13 | Stripe key in Docker env var | Desktop3 | New | **ACCEPTED** (standard for current scale) |
| N-15 | LLM content not moderated before print | Desktop2 | T-13 | **OPEN** |

### Mitigated (Verified closed)

| ID | Finding | Component | Closed Date |
|----|---------|-----------|-------------|
| T-01 | Photo interception (TLS) | Desktop7 | 2026-02-26 (Caddy TLS + Vercel HTTPS) |
| T-02 | Room code guessing | Desktop5, 7 | 2026-02-27 (6-char + rate limit) |
| T-04 | Desktop3 GALLERY persistence | Desktop3 | 2026-02-26 (architecture change) |
| T-08 | Analytics without consent | Desktop6 | 2026-02-26 (consent gate) |
| T-09 | Unencrypted transmission | All | 2026-02-26 (Caddy + Vercel) |
| T-12 | CORS wildcard | Desktop3 | 2026-02-27 (restricted origins) |
| T-15 | Analytics leaks patterns | Desktop3 | 2026-02-26 (HTTPS + IP hash) |
| — | Source maps exposed | All FEs | 2026-02-27 (sourcemap: false) |
| — | Console logs in production | All FEs | 2026-02-27 (esbuild drop) |
| — | No security headers | All FEs | 2026-02-27 (Vercel headers) |
| — | No robots.txt | All FEs | 2026-02-27 (crawler control) |
| — | No LICENSE files | All repos | 2026-02-27 (JCMA Group Ltd) |
| N-02 | Photo upload size limit | Desktop7 | 2026-02-27 (10MB max base64 check) |
| N-04 | Deck size cap | Desktop5 | 2026-02-27 (max 52 cards) |
| N-05 | Player name length cap | Desktop5, 7 | 2026-02-27 (30 char truncation) |
| N-10 | Room creation rate limit | Desktop5, 7 | 2026-02-27 (3/hour/connection) |
| N-01 | API key enforced in production | Desktop3 | 2026-02-27 (startup guard raises RuntimeError) |
| N-03 | WebSocket connection limit per IP | Desktop5, 7 | 2026-02-27 (10 connections/IP) |
| T-03 | Photo memory cleanup | Desktop7 | 2026-02-27 (zero-fill + gc.collect on room close) |
| N-06 | Content Security Policy | Desktop2, 4, 6 | 2026-02-27 (CSP headers in vercel.json) |
| N-16 | Parent-parent comparison in group results | Desktop2 | 2026-03-08 (couple gate: PARENT_ROLES filter + label gate + opt-in toggle) |

---

## What's Working Well

1. **Privacy-by-design**: No cloud AI, no third-party sharing, in-memory photo processing
2. **TLS everywhere**: Caddy auto-TLS on backend, Vercel HTTPS on frontends
3. **Strong room codes**: 2.18B combinations with cryptographic RNG
4. **Security headers**: X-Frame-Options, X-Content-Type-Options, Referrer-Policy, CSP on all deployments
5. **Source protection**: Source maps disabled, console stripped, robots.txt blocks scrapers
6. **CI/CD security**: GitHub Actions run npm audit, pip-audit, TruffleHog, Bandit
7. **Consent model**: BIPA consent gate on all products, analytics opt-in, GDPR banner
8. **Minimal dependencies**: Game servers have tiny dependency surfaces
9. **Test coverage**: 2,100+ automated tests across all repos (836 FE + 166 BE + 932 d4 + 98 d6 + 111 d7)
10. **Governance framework**: CLAUDE.md guardrails, pre-commit hooks, ops reports, TARA, DFMEA, SWOT
11. **Commerce security**: Server-side price validation (PRODUCT_PRICES_PENCE), Stripe webhook signature verification, Prodigi HMAC callbacks
12. **Payment isolation**: All pricing authority server-side — FE cannot tamper with prices
13. **Social safety controls**: Parent-pair exclusion (couple gate) prevents socially inappropriate comparisons between spouses. Label gate requires parent tagging before group results. FamiliMatch redirect for peer-to-peer use case.

---

## Recommended Fix Priority

### Sprint 1 (This week) — Critical + Quick wins

| # | Fix | Effort | Impact |
|---|-----|--------|--------|
| 1 | Enforce API key in production (N-01) | 30 min | Closes biggest auth gap |
| 2 | Photo upload size limit (N-02) | 30 min | Prevents DoS |
| 3 | Deck size cap at 52 (N-04) | 10 min | Prevents OOM |
| 4 | Player name length cap (N-05) | 10 min | Prevents broadcast abuse |
| 5 | Room creation rate limit (N-10) | 1 hr | Completes DoS protection |

### Sprint 2 (Next week) — High severity

| # | Fix | Effort | Impact |
|---|-----|--------|--------|
| 6 | WebSocket connection limit per IP (N-03) | 2 hrs | Resource exhaustion protection |
| 7 | gc.collect() on room close (T-03) | 1 hr | BIPA compliance for RAM |
| 8 | Revise marketing claims (T-11) | 1 day | Legal compliance |
| 9 | CSP headers on Vercel (N-06) | 1 hr | XSS defense-in-depth |

### Sprint 3 (Month 1) — Medium severity

| # | Fix | Effort | Impact |
|---|-----|--------|--------|
| 10 | GDPR delete endpoints (T-16) | 3 days | Regulatory compliance |
| 11 | Server-side consent validation (T-05) | 2 days | BIPA defense-in-depth |
| 12 | Replace innerHTML in exportResults (N-07) | 1 hr | Closes XSS vector |
| 13 | Move admin auth to backend (N-08) | 1 day | Proper access control |
| 14 | Switch thumbnails to sessionStorage (T-14) | 30 min | Reduces data persistence |
| 15 | Docker non-root user (N-11) | 30 min | Container hardening |

---

## Cross-References

| Document | Relevance |
|----------|-----------|
| [TARA_facematch.md](TARA_facematch.md) | FamiliMatch threat model (T-01 to T-08) |
| [TARA_family_personalization.md](../famililook-desktop2/download/ops_reports/TARA_family_personalization.md) | Gen 1 privacy threats (T-01 to T-16) |
| [DFMEA_facematch.md](DFMEA_facematch.md) | FamiliMatch failure modes |
| [PLATFORM_STRATEGY_AND_RISK_REGISTER.md](PLATFORM_STRATEGY_AND_RISK_REGISTER.md) | Platform risk register (R1-R23) |
| [SECURITY_HARDENING_PLAN.md](../famililook-desktop2/download/ops_reports/SECURITY_HARDENING_PLAN.md) | Implementation roadmap |
| [SECURITY.md](../famililook-desktop2/docs/SECURITY.md) | Architecture and principles |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Claude Code | 2026-02-27 | — |
| Updated | Claude Code | 2026-03-07 | — (commerce layer findings N-12 to N-15 added) |
| Reviewer | — | — | — |
| Approver | — | — | — |
