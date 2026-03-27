# TARA: Platform-Wide — Threat Analysis & Risk Assessment

**Document ID**: TARA-FM-003
**Feature**: Full platform (FamiliLook, FamiliUno, FamiliPoker, FamiliMatch) including commerce layer
**Date**: 2026-03-07 (updated from 2026-02-23)
**Author**: Claude Code (automated governance)
**Status**: CURRENT — Investor-ready audit (March 2026)

---

## 1. Scope

This TARA covers security and privacy threats across the entire FamiliLook platform, including the commerce layer (Stripe payments, Prodigi print fulfilment), keepsake template system, and all four products. Updated March 2026 to reflect live commerce, Family Mug Set product, and seasonal template capabilities.

### Components in Scope

| Component | Location | Role |
|-----------|----------|------|
| matchClient.js | desktop6/src/api/ | Solo mode API client — calls `POST /compare/faces` on desktop3 |
| useMatchConnection.js | desktop6/src/hooks/ | Duo/Group WebSocket client |
| ConsentContext.jsx | desktop6/src/contexts/ | BIPA consent gate |
| rooms.py | desktop7/app/ | Room lifecycle management (RAM dict) |
| comparison.py | desktop7/app/ | Pairwise comparison orchestration |
| desktop3_client.py | desktop7/app/ | HTTP client to desktop3 ML backend |
| /compare/faces | desktop3/app/main.py | Symmetric peer comparison endpoint. FROZEN: `contracts/compare_faces.v1.schema.json` |
| /face/morph | desktop3/app/main.py | Face morphing endpoint (shared with Gen 1) |
| KeepsakesModal.jsx | desktop2/src/components/keepsakes/ | Keepsake preview + ordering UI |
| BasketContext.jsx | desktop2/src/state/ | Multi-item shopping cart (localStorage) |
| CurrencyContext.jsx | desktop2/src/state/ | Multi-currency pricing (8 countries) |
| BasketDrawer.jsx | desktop2/src/components/keepsakes/ | Checkout drawer with Stripe integration |
| OrderModal.jsx | desktop2/src/components/keepsakes/ | Single-item Stripe checkout |
| payments.py | desktop3/app/ | Stripe checkout session creation + webhook handler |
| vendor_client.py | desktop3/app/ | Prodigi + QPMarkets API clients |
| /orders/keepsake | desktop3/app/main.py | Keepsake order routing to Prodigi |
| /orders/images/{id}.png | desktop3/app/main.py | Public image serving for Prodigi download |
| /payments/create-basket-checkout | desktop3/app/main.py | Multi-item Stripe checkout |
| /webhooks/print-status | desktop3/app/main.py | HMAC-verified Prodigi status callbacks |
| printProfiles.js | desktop2/src/components/keepsakes/utils/ | Product specs, dimensions, pricing |
| templateRegistry.js | desktop2/src/components/keepsakes/utils/ | Template component registry (lazy-loaded) |
| useFamilyKeepsakeData.js | desktop2/src/components/keepsakes/hooks/ | Aggregates ALL children's data for family products |
| printExport.js | desktop2/src/utils/ | HTML-to-PNG export for print fulfilment |

### Components Out of Scope

- Physical infrastructure (Hetzner VPS — covered in platform risk register)
- ML model internals (covered in DFMEA)

---

## 2. Threat Identification

### T-01: Photo interception during WebSocket transfer

**Threat**: An attacker intercepts photo data transmitted between a player's browser and desktop7 via WebSocket. Photos are base64-encoded but not encrypted at the application layer.

| Attribute | Value |
|-----------|-------|
| Likelihood | Medium (depends on deployment: `ws://` vs `wss://`) |
| Impact | High (intimate photos exposed, privacy violation, potential blackmail) |
| Risk Level | **HIGH** |

**Mitigation**:
- Production deployment MUST use `wss://` (TLS-encrypted WebSocket) via Caddy reverse proxy
- Caddy auto-provisions TLS certificates via Let's Encrypt
- No application-layer encryption needed if TLS is enforced

**Verification**: Caddy configuration file enforces HTTPS/WSS. Desktop7 should reject non-TLS connections in production.

**Residual Risk**: LOW — if TLS is properly configured. MEDIUM if someone deploys without Caddy/TLS.

---

### T-02: Unauthorized room join (room code guessing) — MITIGATED

**Threat**: An attacker guesses or brute-forces a room code to join an active room without invitation, gaining access to other players' photos and results.

| Attribute | Value |
|-----------|-------|
| Likelihood | **Very Low** (6-char alphanumeric = 2.18 billion possibilities) |
| Impact | High (non-consenting party sees another person's photo) |
| Risk Level | **LOW** (mitigated 2026-02-27) |

**Mitigations Implemented (2026-02-27)**:
- 6-character uppercase alphanumeric codes (36^6 = 2,176,782,336 combinations) — upgraded from 4-digit numeric (9,000)
- Cryptographic RNG via Python `secrets.choice()` — upgraded from predictable `random.randint()`
- Per-connection rate limiting: 5 failed join attempts per 60 seconds, then blocked
- Failed join attempts logged via `logging.warning()` for monitoring
- Rooms have a maximum player count — once full, no more joins
- Room codes are single-use (expire when room closes or after 30-min idle timeout)

**Verification**: `test_rooms.py` — `test_room_code_is_alphanumeric` (regex `[A-Z0-9]{6}`), `test_room_codes_are_unique`. Both desktop5 and desktop7 pass all tests.

**Residual Risk**: LOW — brute-force at 100 req/s would take ~250 days. Rate limiting blocks after 5 attempts per connection.

---

### T-03: Photo data persists in desktop7 memory after room close

**Threat**: Photo byte data remains in Python process memory after room close due to garbage collection delays, reference counting, or pending HTTP responses. A memory dump or server compromise exposes photos that should have been deleted.

| Attribute | Value |
|-----------|-------|
| Likelihood | Medium (Python GC is non-deterministic for large objects) |
| Impact | High (BIPA violation — photos retained beyond declared retention period) |
| Risk Level | **HIGH** |

**Mitigation**:
- Room close handler deletes room dict (removes primary reference)
- Python garbage collector eventually frees unreferenced memory

**Recommended Action**:
1. Explicitly `del` photo references and overwrite with zeros before deletion
2. Call `gc.collect()` after room cleanup
3. Add memory usage logging to detect photo data lingering
4. Consider `mmap` for photo storage with explicit `close()` + `unlink()`

**Residual Risk**: MEDIUM — even with explicit deletion, memory may contain residual data until OS reclaims pages.

---

### T-04: ~~Desktop3 retains embeddings from FamiliMatch requests~~ — CLOSED

**Threat**: ~~Desktop3's `/kinship/analyze` endpoint stores facial embeddings in its `GALLERY` dict (intended for Gen 1 family sessions). FamiliMatch requests may inadvertently persist embeddings in the GALLERY, violating the "RAM-only, no persistence" promise.~~

**Status: CLOSED — threat eliminated by architectural change (2026-02-26).**

FamiliMatch Solo and Duo modes now call `POST /compare/faces` exclusively — not `/kinship/analyze`. The `/compare/faces` endpoint has no GALLERY interaction; it is a stateless endpoint that processes the request in-memory and returns the result. The GALLERY persistence path (`gallery_persistence.json`) is only reachable via `/kinship/analyze` (Gen 1 / FamiliLook).

| Attribute | Value |
|-----------|-------|
| Likelihood | **None** — `/compare/faces` has no GALLERY |
| Impact | N/A |
| Risk Level | **CLOSED** |

**Evidence**: `matchClient.js` (desktop6) calls `POST /compare/faces`. Contract frozen at `contracts/compare_faces.v1.schema.json`. The contract's `must_not` list explicitly states: "Frontend must NOT call /kinship/analyze for FamiliMatch comparisons."

**Residual Risk**: NONE — architecture change eliminates the threat. Group mode calls `/detect` + `/embed` (no GALLERY) via desktop7.

---

### T-05: Consent bypass via direct API call — MITIGATED

**Threat**: A user bypasses the frontend BIPA consent modal by calling desktop3's `/kinship/analyze` or `/face/morph` endpoints directly (via curl, Postman, or browser dev tools). Photos are processed without consent.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low (requires technical knowledge) |
| Impact | High (BIPA violation — $5K/person statutory damages) |
| Risk Level | ~~MEDIUM~~ **MITIGATED** |

**Mitigations Implemented**:
- Frontend ConsentContext.jsx blocks all UI-driven API calls
- **Server-side**: `BiometricConsentMiddleware` (middleware.py:65-87) rejects any request missing the `X-Biometric-Consent` header — direct API calls without the header are blocked

**Recommended Action**: None — server-side enforcement is now active.

**Residual Risk**: LOW — server-side middleware enforces consent header. Direct API calls without the header are rejected.

---

### T-06: Player screenshots another player's photo during reveal

**Threat**: During Duo/Group reveal, one player takes a screenshot of the other player's photo using device-level screen capture. The captured photo exists outside the app's data lifecycle controls.

| Attribute | Value |
|-----------|-------|
| Likelihood | High (screenshots are trivial on all devices) |
| Impact | Low-Medium (single photo, no biometric data, similar to sharing a photo on any platform) |
| Risk Level | **LOW** |

**Mitigation**:
- Cannot prevent device-level screenshots (OS limitation)
- Terms of Service should disclose that participants may capture screenshots
- Consent modal should mention that photos will be visible to other room participants

**Recommended Action**: Add Terms of Service clause: "By participating in a FamiliMatch room, you acknowledge that other participants may capture screenshots of content displayed during the session."

**Residual Risk**: LOW — this is a social contract issue, not a technical one. Same risk exists in any video call or photo-sharing context.

---

### T-07: Room flooding / DoS (creating thousands of rooms)

**Threat**: An attacker creates thousands of rooms on desktop7, exhausting server memory and preventing legitimate users from creating rooms.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low-Medium (requires scripting, but WebSocket endpoint is public) |
| Impact | Medium (service unavailable for legitimate users) |
| Risk Level | **MEDIUM** |

**Mitigation**:
- Each room is a lightweight dict in RAM (~few KB without photos)
- Desktop7 has room inactivity timeout — empty rooms auto-close
- Caddy can rate-limit WebSocket connections per IP

**Recommended Action**:
1. Rate limit room creation: max 3 rooms per IP per hour
2. Max concurrent rooms globally (e.g., 500) — reject creation when full
3. Require room to have at least 1 player within 60 seconds or auto-close

**Residual Risk**: LOW — with rate limiting and auto-cleanup.

---

### T-08: Analytics tracking without explicit FamiliMatch consent — UPDATED

**Threat**: FamiliMatch sends analytics events (page views, button clicks) to desktop3's analytics backend without separate consent for FamiliMatch-specific tracking.

**Status: IMPLEMENTED WITH CONSENT GATE (2026-02-26).**

FamiliMatch (desktop6) now includes `analytics.js` tracking. The analytics module is gated on the BIPA consent flag (`fl:bipa-consent → { bipaConsented: true }`). Events are only fired after the user accepts the BIPA consent modal in `ConsentContext.jsx`. This is distinct from FamiliLook's consent key (`fl:consent`) — desktop6 specifically checks the BIPA consent field.

| Attribute | Value |
|-----------|-------|
| Likelihood | **Low** — analytics fire only after explicit BIPA consent |
| Impact | Low (if consent gate fails, analytics fire without consent) |
| Risk Level | **LOW** |

**Mitigation**:
- `analytics.js` checks `fl:bipa-consent → bipaConsented` before firing any event
- ConsentContext.jsx blocks all app functionality until consent is given
- Analytics product identifier set to `'familimatch'` — events attributed correctly in dashboard

**Recommended Action**:
1. Verify analytics consent gate unit tests cover the `bipaConsented=false` → no events path
2. Ensure privacy policy discloses analytics tracking alongside facial analysis consent
3. Confirm `analytics.js` in desktop6 does NOT collect any biometric or photo data — events only carry page/action labels and sessionId

**Residual Risk**: LOW — consent gate is implemented. Residual risk is if the gate has a bug; mitigated by unit tests.

---

### T-09: Stripe webhook forgery — attacker fakes payment confirmation

**Threat**: An attacker sends fake Stripe webhook events to `POST /webhooks/stripe` or `POST /webhooks/print-status`, triggering order fulfilment without payment.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low (requires knowledge of webhook URLs + payload format) |
| Impact | High (free merchandise, financial loss) |
| Risk Level | **MEDIUM** |

**Mitigation**:
- Stripe webhooks verified via `stripe.Webhook.construct_event()` using `STRIPE_WEBHOOK_SECRET`
- Prodigi webhooks verified via HMAC signature (`X-Prodigi-Signature` header)
- Both reject unsigned/invalid payloads with 400 status

**Residual Risk**: LOW — webhook verification is implemented. Risk only if secrets leak.

---

### T-10: Price tampering — frontend sends manipulated prices to backend

**Threat**: An attacker modifies the price sent from the frontend checkout to the Stripe session creation endpoint, paying less than the actual product price.

| Attribute | Value |
|-----------|-------|
| Likelihood | Medium (browser DevTools can modify any request) |
| Impact | High (products sold below cost) |
| Risk Level | **HIGH** |

**Mitigation**:
- Backend `payments.py` uses server-side `PRODUCT_PRICES_PENCE` dictionary — frontend price is **ignored**
- Stripe line items are built from server-side pricing only
- Personalised message surcharge (199p) is also server-side

**Verification**: Frontend sends `product_type`, backend looks up canonical price. No user-supplied price field in checkout request.

**Residual Risk**: LOW — price authority is server-side. Frontend price display is cosmetic only.

---

### T-11: Keepsake image URL enumeration — attacker accesses other users' print images

**Threat**: The `/orders/images/{order_id}.png` endpoint serves keepsake images publicly (no auth) for Prodigi to download. An attacker could enumerate order IDs to access other users' personalised keepsake images.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low (order IDs are UUIDs — 2^128 possibilities) |
| Impact | Medium (personalised images with family names/photos exposed) |
| Risk Level | **LOW** |

**Mitigation**:
- Order IDs are UUIDs (not sequential integers) — enumeration infeasible
- Images are generated on-demand and served ephemerally
- No directory listing endpoint

**Recommended Action**: Consider adding time-limited signed URLs (HMAC + expiry) for defense-in-depth.

**Residual Risk**: LOW — UUID randomness provides adequate protection for current scale.

---

### T-12: Family Mug Set exposes aggregated children's data in single template

**Threat**: The Family Mug Set template aggregates ALL children's analysis results (names, photos, feature breakdowns) into a single template. If the print image URL is accessed, it reveals more family data than a single-child keepsake.

| Attribute | Value |
|-----------|-------|
| Likelihood | Very Low (requires image URL access — see T-11) |
| Impact | Medium (multiple children's facial analysis in one image) |
| Risk Level | **LOW** |

**Mitigation**:
- Same UUID protection as T-11
- Data is what parents voluntarily chose to print — no additional data beyond what they uploaded
- No PII beyond first names and face crops (which parents provided)

**Residual Risk**: LOW — parents explicitly chose to create this product with their children's data.

---

### T-13: LLM-generated personalised messages contain inappropriate content

**Threat**: The `usePersonalizedMessage` hook calls an LLM to generate personalised messages for keepsake templates. The LLM could produce offensive, inaccurate, or legally problematic content that gets printed on physical products.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low (LLM is prompted for wholesome family content) |
| Impact | Medium (offensive content on physical product, customer complaint, brand damage) |
| Risk Level | **MEDIUM** |

**Mitigation**:
- LLM prompt constrains output to family-friendly, celebratory content
- User can preview the message before ordering (KeepsakesModal preview)
- Personalised message is optional (toggle on/off)

**Recommended Action**: Add content moderation check on LLM output before rendering. Consider a blocklist of terms that should never appear on keepsakes.

**Residual Risk**: LOW-MEDIUM — preview provides user gate, but automated moderation would be stronger.

---

### T-14: Basket/cart manipulation — adding items with tampered metadata

**Threat**: An attacker modifies BasketContext items in localStorage to change product types, quantities, or associated data before checkout.

| Attribute | Value |
|-----------|-------|
| Likelihood | Low (requires localStorage manipulation) |
| Impact | Medium (wrong products ordered, but server-side pricing limits financial impact) |
| Risk Level | **LOW** |

**Mitigation**:
- Server-side price validation (PRODUCT_PRICES_PENCE) prevents price tampering
- Stripe session built from server-side product catalogue
- MAX_ITEMS=20 prevents cart flooding
- Backend validates product_type exists in catalogue before creating order

**Residual Risk**: LOW — server-side validation limits attack surface.

---

### T-15: Unwanted interpersonal comparison — parents scored against each other

**Threat**: In family/group kinship analysis, the system generates pairwise comparison links for ALL detected faces including parent-parent pairs. This produces kinship scores between spouses, which users find socially inappropriate and distressing. User complaints received.

| Attribute | Value |
|-----------|-------|
| Likelihood | **Very High** (any family group with 2 parents triggers this — most common use case) |
| Impact | Medium (social discomfort, product trust erosion, user complaints) |
| Risk Level | **HIGH** (before mitigation) → **MITIGATED** |

**Mitigations Implemented (2026-03-08)**:
1. **PARENT_ROLES set** (`constants.js`): defines roles that should be excluded from pairwise comparison ("Mum", "Dad", "Partner")
2. **parentNameSet filter** (`GroupSnapshotSection.jsx`): builds a Set of face names assigned parent roles, filters pairwise_links to exclude pairs where both members are parents
3. **Label gate**: group results require parent tagging before displaying — amber prompt "Tag the parents first"
4. **Opt-in toggle**: green shield banner with Include/Exclude button. Default: excluded. Users can opt in to see parent-parent pairs.
5. **UploadSection couple nudge**: when exactly 2 parents and 0 children are uploaded, shows "Want to compare these two instead?" with redirect to FamiliMatch (`VITE_FAMILIMATCH_URL`)

**Verification**: Manual testing — label gate blocks results; toggle controls pair visibility; FamiliMatch redirect works.

**Residual Risk**: LOW — parents are excluded by default. Opt-in toggle is explicit and requires intentional action.

---

## 3. Risk Summary

| ID | Threat | Likelihood | Impact | Risk Level | Residual Risk |
|----|--------|-----------|--------|------------|---------------|
| T-01 | Photo interception (WebSocket) | Medium | High | ~~HIGH~~ **MITIGATED** | LOW — Caddy TLS + Vercel HTTPS live |
| T-02 | Room code guessing | Very Low | High | ~~MEDIUM~~ **MITIGATED** | LOW — 6-char alphanumeric + rate limit (2026-02-27) |
| T-03 | Photos persist in RAM after close | Medium | High | ~~HIGH~~ **MITIGATED** | LOW — zero-fill + gc.collect() on room close (2026-02-27) |
| T-04 | ~~Desktop3 retains embeddings~~ | None | N/A | **CLOSED** | NONE — `/compare/faces` has no GALLERY |
| T-05 | Consent bypass via direct API | Low | High | ~~MEDIUM~~ **MITIGATED** | LOW — BiometricConsentMiddleware enforces `X-Biometric-Consent` header server-side |
| T-06 | Player screenshots other's photo | High | Low-Medium | **LOW** | LOW |
| T-07 | Room flooding / DoS | Low-Medium | Medium | ~~MEDIUM~~ **MITIGATED** | LOW — join rate limit + creation rate limit + photo size limit + connection limit per IP (2026-02-27) |
| T-08 | Analytics without consent | Low | Low | ~~LOW~~ **MITIGATED** | LOW — consent gate implemented |
| T-09 | Stripe webhook forgery | Low | High | **MEDIUM** | LOW — webhook signature verification implemented |
| T-10 | Price tampering (FE → BE) | Medium | High | ~~HIGH~~ **MITIGATED** | LOW — server-side PRODUCT_PRICES_PENCE |
| T-11 | Keepsake image URL enumeration | Low | Medium | **LOW** | LOW — UUID order IDs |
| T-12 | Family Mug aggregated data exposure | Very Low | Medium | **LOW** | LOW — voluntary parent action |
| T-13 | LLM inappropriate content on keepsakes | Low | Medium | **MEDIUM** | LOW-MEDIUM — user preview gate |
| T-14 | Basket/cart manipulation | Low | Medium | **LOW** | LOW — server-side validation |
| T-15 | Unwanted parent-parent comparison | ~~Very High~~ Low | Medium | ~~HIGH~~ **MITIGATED** | LOW — couple gate + label gate + opt-in toggle (2026-03-08) |

---

## 4. Action Items

| Priority | Threat | Action | Owner | Status |
|----------|--------|--------|-------|--------|
| P0 | T-01 | Enforce `wss://` in production (Caddy TLS config) | DevOps | **DONE** — Caddy auto-TLS live on Hetzner; Vercel WSS by default |
| P0 | ~~T-04~~ | ~~Audit desktop3 GALLERY persistence for FamiliMatch requests~~ | Dev | **CLOSED** — FamiliMatch uses `/compare/faces`, not `/kinship/analyze`. GALLERY not reachable. |
| P0 | T-10 | Server-side price validation for all checkout flows | Dev | **DONE** — `PRODUCT_PRICES_PENCE` in payments.py, FE price ignored |
| P1 | T-02 | Rate limit room join attempts + upgrade room codes | Dev | **DONE (2026-02-27)** — 6-char alphanumeric codes, `secrets` RNG, 5/min rate limit |
| P1 | T-03 | Explicit photo deletion + gc.collect() on room close | Dev | **DONE (2026-02-27)** — zero-fill + gc.collect() |
| P1 | T-07 | Rate limit room creation (3/hour/IP) + max concurrent rooms | Dev | **DONE (2026-02-27)** — creation rate limit + connection limit per IP |
| P1 | T-09 | Webhook signature verification (Stripe + Prodigi) | Dev | **DONE** — construct_event() + HMAC verification |
| P2 | T-05 | Server-side consent token validation | Dev | **DONE** — `BiometricConsentMiddleware` (middleware.py:65-87) enforces `X-Biometric-Consent` header |
| P2 | T-06 | Terms of Service screenshot disclosure | Legal | NOT STARTED |
| P2 | T-13 | Content moderation for LLM-generated keepsake messages | Dev | NOT STARTED |
| P1 | T-15 | Exclude parent-parent pairwise comparisons in group mode | Dev | **DONE (2026-03-08)** — PARENT_ROLES filter, label gate, opt-in toggle, FamiliMatch redirect |
| P3 | T-11 | Consider signed/expiring image URLs for keepsake images | Dev | NOT STARTED (low priority — UUID protection adequate) |

---

## 5. Cross-References

| Document | Relevance |
|----------|-----------|
| [DFMEA_facematch.md](DFMEA_facematch.md) | Failure modes for same components |
| [SWOT_ANALYSIS.md](SWOT_ANALYSIS.md) | Strategic positioning and competitive analysis |
| [PLATFORM_STRATEGY_AND_RISK_REGISTER.md](PLATFORM_STRATEGY_AND_RISK_REGISTER.md) | Platform-wide risk register (R1-R23) |
| [SECURITY_ASSESSMENT_2026-02-27.md](SECURITY_ASSESSMENT_2026-02-27.md) | Consolidated security findings |
| [PLATFORM_ARCHITECTURE.md](PLATFORM_ARCHITECTURE.md) | Full technical architecture |

---

## 6. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Claude Code | 2026-02-23 | — |
| Updated | Claude Code | 2026-03-07 | — (commerce + keepsake threats added) |
| Updated | Claude Code | 2026-03-08 | — (T-15: parent-pair exclusion added) |
| Reviewer | — | — | — |
| Approver | — | — | — |
