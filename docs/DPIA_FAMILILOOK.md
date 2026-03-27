# Data Protection Impact Assessment (DPIA)
## FamiliLook Platform — JCMA Group Ltd

**Date**: 2026-03-27
**Data Controller**: JCMA Group Ltd
**DPO Contact**: privacy@famililook.com
**Products Covered**: FamiliLook, FamiliUno, FamiliPoker, FamiliMatch

---

## 1. Description of Processing

### What we process
- **Facial photographs**: Uploaded by users for resemblance analysis (FamiliLook/Uno/Poker) or compatibility comparison (FamiliMatch)
- **Facial embeddings**: 512-dimensional mathematical vectors generated from photos for comparison. Generated server-side, held in RAM only during processing.
- **8 facial feature labels**: Eyes, eyebrows, smile, nose, face shape, skin, hair, ears — calibrated against population data
- **Email addresses**: Voluntarily provided for newsletter subscription, ambassador programme, and order fulfilment
- **Shipping addresses**: For physical product orders (keepsakes, card decks)
- **Payment metadata**: Stripe session IDs (payment processing handled by Stripe)

### What we do NOT process
- We do not perform facial recognition (identifying who someone is)
- We do not match faces against databases
- We do not store face embeddings after the session
- We do not process data of children under 13 without the 13+ age gate confirmation

### Legal basis
- **Explicit consent** (GDPR Art. 9(2)(a)) for biometric processing — obtained via in-app consent gate before any photo upload
- **Legitimate interest** (GDPR Art. 6(1)(f)) for analytics (IP hashed, no PII)
- **Contract performance** (GDPR Art. 6(1)(b)) for order fulfilment

### Data subjects
- Parents and guardians (primary users)
- Children (photos uploaded by parents/guardians)
- Young adults (FamiliMatch users)
- All users must confirm they are 13+ before uploading photos

---

## 2. Necessity and Proportionality

### Why biometric processing is necessary
The core product (family resemblance analysis) requires comparing facial features between parents and children. This cannot be achieved without processing facial photographs.

### Proportionality measures
- **Minimum data**: Only 8 facial features are extracted — not full biometric templates
- **No storage**: Photos are processed in RAM and discarded immediately. No server-side persistence of photos or embeddings.
- **Thumbnails**: Low-resolution thumbnails stored client-side (localStorage) with 24h auto-expiry. User can clear instantly.
- **Purpose limitation**: Face data used only for resemblance/compatibility analysis, never for identification, surveillance, or third-party sharing.

---

## 3. Risk Assessment

| Risk | Likelihood | Severity | Mitigation | Residual Risk |
|---|---|---|---|---|
| Unauthorised access to photos in transit | Low | High | HTTPS/TLS enforced. HSTS header set. | Low |
| Server-side data breach | Low | High | Photos never stored. RAM-only processing. No database. | Low |
| Client-side thumbnail exposure | Medium | Low | 24h auto-expiry. One-tap clear. localStorage only. | Low |
| Re-identification from embeddings | Very Low | Medium | Embeddings are 512-dim vectors, not reversible to photos. Deleted after session. | Very Low |
| Child data processed without consent | Low | High | 13+ age gate before any upload. Biometric consent gate. | Low |
| Order PII breach | Low | Medium | Orders stored as flat JSON files on owned infrastructure (Hetzner EU). No cloud database. | Low-Medium |
| Third-party data sharing | Very Low | High | No cloud AI providers. All ML on owned infrastructure. Stripe handles payment PII under their own DPA. | Very Low |
| Marketing copy misrepresenting processing | Very Low | Medium | T-11 audit completed 2026-03-27 — all false "on-device" claims corrected. | Very Low |

---

## 4. Technical and Organisational Measures

### Technical
- **Encryption in transit**: TLS via Caddy reverse proxy (HTTPS enforced, HSTS)
- **No persistent storage**: Photos processed in RAM, never written to disk
- **Biometric consent middleware**: Rejects API calls without `X-Biometric-Consent: granted` header
- **API authentication**: `X-API-Key` header required on all non-public endpoints (timing-safe comparison)
- **Rate limiting**: 30 requests/minute per IP on heavy endpoints
- **CORS restriction**: Only whitelisted origins (famililook.com, Vercel deploy URLs)
- **Content Security Policy**: `default-src 'none'` on API responses
- **Server-side price validation**: Prevents frontend price tampering
- **GDPR deletion endpoint**: `POST /data/forget-me` covers all 6 data stores

### Organisational
- **Age gate**: 13+ confirmation required before any biometric processing
- **Biometric consent**: Explicit opt-in before photo upload, revocable from Settings
- **Privacy policy**: Published at famililook.com/privacy, covers all processing activities
- **Data deletion**: Users can request erasure via privacy@famililook.com (30-day response)
- **Incident response plan**: Documented in `docs/INCIDENT_RESPONSE_PLAN.md`
- **No third-party AI**: All ML models run on owned Hetzner infrastructure in EU

---

## 5. Data Flows

```
User Device
  → [HTTPS/TLS] →
Hetzner EU Server (desktop3)
  → MediaPipe face detection (RAM only)
  → ArcFace embedding generation (RAM only)
  → Feature calibration + comparison (RAM only)
  → Response returned to client
  → All face data discarded from RAM

Stripe (payment processing)
  → Handles card details under Stripe DPA
  → FamiliLook receives session ID only

Prodigi / QPMarkets (print fulfilment)
  → Receives keepsake/card images + shipping address
  → Under vendor DPA obligations
```

---

## 6. Data Retention

| Data Type | Retention | Deletion Method |
|---|---|---|
| Photos | Session only (RAM) | Automatic — never persisted |
| Face embeddings | Session only (RAM) | Automatic — never persisted |
| Client thumbnails | 24h (localStorage) | Auto-expiry + manual clear |
| Analytics events | 90 days | Automated cleanup (planned) |
| Order records | 6 years (UK HMRC) | Anonymised on GDPR request, retained for tax |
| Subscriber emails | Until unsubscribe | Deleted via forget-me endpoint |
| Ambassador grants | Until revoked | Deleted via forget-me endpoint |

---

## 7. Consultation

This DPIA was prepared by the development team with reference to:
- ICO DPIA guidance (https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/)
- GDPR Article 35 requirements
- Platform security assessment (docs/SECURITY_ASSESSMENT_2026-02-27.md)
- Full platform audit (docs/FULL_PLATFORM_AUDIT_2026-03-26.md)

**Review schedule**: This DPIA should be reviewed annually or when significant changes are made to data processing activities.

---

## 8. Approval

| Role | Name | Date | Signature |
|---|---|---|---|
| Data Controller | _________________ | ____/____/2026 | _________________ |
| Technical Lead | _________________ | ____/____/2026 | _________________ |

*This document satisfies the DPIA requirement under GDPR Article 35 for processing that is "likely to result in a high risk to the rights and freedoms of natural persons", including biometric data processing.*
