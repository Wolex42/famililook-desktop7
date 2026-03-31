## CPO Spec: BIPA Server-Side Consent Validation (B2)

**Agent**: CPO
**Date**: 2026-03-24
**Severity**: BLOCKER — frontend-only consent means a direct API caller bypasses all consent.

---

### Problem

Biometric consent is checked client-side only. The backend (`/detect`, `/embed`, `/kinship/analyze`, `/compare/faces`) processes photos from any source without verifying consent. A curl command can bypass all consent UX.

### Solution

Add a consent verification header to all biometric endpoints. Frontend sends `X-Biometric-Consent: granted` header. Backend rejects requests without it.

### Acceptance Criteria

- [ ] Backend checks `X-Biometric-Consent` header on: `/detect`, `/embed`, `/kinship/analyze`, `/compare/faces`, `/face/morph`
- [ ] Missing header → 403 with body: `{"error": "biometric_consent_required", "message": "Biometric consent must be granted before processing"}`
- [ ] Header value must be "granted" (case-insensitive)
- [ ] Desktop2 FE: all API calls include `X-Biometric-Consent: granted` header when `consent.biometric === true`
- [ ] Desktop6 FE: matchClient.js includes header when `consent.bipaConsented === true`
- [ ] CORS: `X-Biometric-Consent` added to `Access-Control-Allow-Headers` in Caddyfile
- [ ] Existing tests still pass

### Scope

- desktop3: middleware + Caddyfile CORS header
- desktop2: API call headers (config.js or fetch wrapper)
- desktop6: matchClient.js headers

**Effort**: M
**Handoff: CPO → BE Lead (middleware) + FE Lead (headers)**
