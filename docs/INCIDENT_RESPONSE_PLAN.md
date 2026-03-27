# Incident Response Plan
## FamiliLook Platform — JCMA Group Ltd

**Date**: 2026-03-27
**Owner**: JCMA Group Ltd
**Contact**: privacy@famililook.com

---

## 1. Scope

This plan covers security incidents affecting the FamiliLook platform:
- FamiliLook (famililook.com)
- FamiliUno (famililook.com/uno)
- FamiliPoker (famililook-desktop4.vercel.app)
- FamiliMatch (famililook-desktop6.vercel.app)
- Backend ML engine (Hetzner EU — desktop3)
- Vendor integrations (Stripe, Prodigi, QPMarkets)

---

## 2. Incident Classification

| Severity | Definition | Examples | Response Time |
|---|---|---|---|
| **P1 — Critical** | Active data breach, PII exposed | Server compromised, order data leaked, photos stored when shouldn't be | Immediate (within 1 hour) |
| **P2 — High** | Security vulnerability exploitable | API key leaked, auth bypass discovered, XSS in production | Within 4 hours |
| **P3 — Medium** | Potential vulnerability, no active exploit | Dependency CVE, misconfiguration found in audit | Within 24 hours |
| **P4 — Low** | Minor security improvement | Missing header, non-critical hardening | Within 1 week |

---

## 3. Response Procedure

### Step 1: Detect and Assess (0-1 hour)
- Identify what happened: what data, what systems, what timeframe
- Classify severity (P1-P4)
- Preserve evidence: do NOT delete logs, do NOT redeploy until assessed

### Step 2: Contain (1-4 hours)
- **P1**: Take affected service offline immediately
  - Hetzner: `docker compose down` on desktop3
  - Vercel: Disable deployment in dashboard
- **P2**: Rotate compromised credentials immediately
  - API keys: Update `FAMILILOOK_API_KEY` in Hetzner `.env` + rebuild
  - Stripe keys: Rotate in Stripe dashboard
  - QPMN token: Contact QPMarkets support
- **P3/P4**: Schedule fix, no immediate containment needed

### Step 3: Notify (within 72 hours for P1/P2)

**GDPR Article 33 — ICO notification required if:**
- Personal data breach occurred
- Risk to rights and freedoms of individuals
- Must notify within 72 hours of becoming aware

**ICO Breach Reporting**: https://ico.org.uk/make-a-complaint/data-protection-complaints/data-protection-complaints/
**ICO Phone**: 0303 123 1113

**Notification must include:**
1. Nature of the breach (what data, how many people affected)
2. Contact details of DPO (privacy@famililook.com)
3. Likely consequences
4. Measures taken to address and mitigate

**User notification required if:**
- High risk to individuals (e.g., financial data, biometric data exposed)
- Notify affected users directly via email if available

### Step 4: Remediate
- Fix the root cause
- Deploy fix through normal pipeline (Documents repo → main → production)
- Verify fix with build + tests
- Update security status in memory files

### Step 5: Post-Incident Review (within 7 days)
- Document: what happened, timeline, root cause, what was done
- Update this plan if gaps found
- Update DPIA if processing changed
- File incident report in `docs/incidents/YYYY-MM-DD_description.md`

---

## 4. Key Contacts

| Role | Contact | Responsibility |
|---|---|---|
| Data Controller / CEO | [TO BE FILLED] | Final authority, ICO notification |
| Technical Lead | [TO BE FILLED] | Containment, remediation |
| Privacy Contact | privacy@famililook.com | User communications, DSAR handling |
| Stripe Support | https://support.stripe.com | Payment data incidents |
| Hetzner Support | https://accounts.hetzner.com | Server infrastructure |
| ICO | 0303 123 1113 | Regulatory notification |

---

## 5. Key Credentials to Rotate in a Breach

| Credential | Location | How to Rotate |
|---|---|---|
| `FAMILILOOK_API_KEY` | Hetzner `.env` | Generate new key, update `.env`, rebuild Docker |
| `SECRET_KEY` | Hetzner `.env` | Generate new key, update `.env`, rebuild Docker |
| `STRIPE_SECRET_KEY` | Hetzner `.env` + Stripe dashboard | Roll key in Stripe, update `.env` |
| `STRIPE_WEBHOOK_SECRET` | Hetzner `.env` + Stripe dashboard | Delete + recreate webhook endpoint |
| `QPMARKETS_STORE_TOKEN` | Hetzner `.env` | Contact QPMarkets to regenerate |
| `INTERNAL_API_TOKEN` | Hetzner `.env` | Generate new token, update `.env` |
| Vercel deploy tokens | Vercel dashboard | Regenerate in project settings |

---

## 6. What Data Could Be Exposed

| Data Store | Contains PII? | Encrypted at Rest? | Breach Impact |
|---|---|---|---|
| Gallery (RAM) | Yes (embeddings) | N/A (RAM only) | Low — lost on restart |
| Orders (JSON files) | Yes (names, addresses, emails) | No (flat files on disk) | **High** — shipping PII |
| Analytics (JSONL) | Minimal (hashed IPs) | No | Low — pseudonymised |
| Subscribers (JSONL) | Yes (emails) | No | Medium — email list |
| Ambassador Grants (JSON) | Yes (emails, names) | No | Medium — email + plan data |
| Stripe | Yes (payment details) | Yes (Stripe-managed) | High — but Stripe's responsibility |

**Priority in a breach**: Rotate credentials first, then assess if order files were accessed.

---

## 7. Prevention Measures (Already In Place)

- HTTPS/TLS enforced (Caddy + HSTS)
- API key authentication on all non-public endpoints
- Biometric consent middleware
- Rate limiting (30 req/min per IP)
- CORS origin restriction
- No cloud AI providers (all processing on owned infrastructure)
- Photos never stored server-side
- Server-side price validation

---

## 8. Review Schedule

This plan must be reviewed:
- Annually (next review: 2027-03-27)
- After any P1 or P2 incident
- When new data processing activities are added
- When infrastructure changes (new hosting, new vendors)

*This document satisfies the incident response requirement implied by GDPR Articles 33-34.*
