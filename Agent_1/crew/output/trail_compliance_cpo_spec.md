## CPO Spec: Pre-Production Compliance Fixes (Option B)

**Agent**: CPO
**Task**: 8 compliance fixes before trail goes to production
**Date**: 2026-03-23
**Approved**: CEO selected Option B (minimum + Privacy/Terms expansion)

---

### Group 1: Minimum Viable (S effort each)

**Fix 1**: Move biometric consent BEFORE /detect call
- Currently: photo uploads → /detect fires → biometric consent only before Analyze
- Required: consent gate must fire BEFORE first /detect call
- File: UploadSection.jsx — wrap detectPhoto() with consent check

**Fix 2**: Fix BrandHub misleading privacy claims
- FamiliLook tile: "Everything happens on your phone" → "Processed securely on our EU servers. Photos are never stored."
- FamiliUno tile: keep as-is (card deck is client-side)
- FamiliPoker tile: keep as-is (accurate)
- FamiliMatch tile: keep as-is (accurate)
- Trust badges: "Works on your device" → "Works in your browser"
- File: BrandHubPage.jsx

**Fix 3**: Make footer disclaimer readable
- Current: 11px, rgba(255,255,255,0.2) — functionally invisible
- Required: 12px, rgba(255,255,255,0.4), add line about data processing
- File: BrandHubPage.jsx

**Fix 4**: Add age confirmation for FamiliPoker
- When user taps FamiliPoker tile OR trail Casino node → modal: "This section contains simulated gambling content for users aged 18+. Are you 18 or over?"
- Yes → proceed (store in localStorage fl:age-confirmed-poker)
- No → close, don't navigate
- Files: BrandHubPage.jsx, TrailTooltip.jsx (or shared AgeGateModal component)

### Group 2: Expand Legal Pages (M effort)

**Fix 5**: Expand Privacy Policy
- Add: GDPR lawful basis (Art. 6(1)(a) consent, Art. 9(2)(a) explicit consent for biometric)
- Add: BIPA disclosure (Illinois biometric information privacy act)
- Add: Data retention periods (photos: session only, embeddings: deleted after analysis, analytics: 90 days, order data: 7 years per tax law)
- Add: Third-party data sharing (Stripe for payments, Prodigi for printing, Cloudflare for CDN)
- Add: International data transfers (EU server for analysis, Stripe US, Prodigi UK)
- Add: Special category data notice (biometric data is GDPR Art. 9 special category)
- Add: Children's data section (acknowledge platform may process children's photos with parental authority)
- Add: Data subject rights (access, rectification, erasure, portability, objection)
- Add: DPO/contact that is monitored
- Remove: "beta testing phase" language
- File: PrivacyPolicy.jsx

**Fix 6**: Expand Terms of Service
- Add: Age restriction (13+ to use, 18+ for FamiliPoker)
- Add: Limitation of liability
- Add: Intellectual property (user retains photo rights, we retain analysis output rights)
- Add: Prohibited uses (deepfakes, harassment, surveillance, identity verification)
- Add: Refund/cancellation policy (keepsakes: Prodigi handles, subscriptions: cancel anytime)
- Add: Dispute resolution / governing law (England and Wales)
- Add: Acceptable use of AI features
- Remove: "BETA" language
- File: TermsOfService.jsx

**Fix 7**: Add consent revocation button
- Settings/About tab or Privacy page: "Revoke Biometric Consent" button
- Clears fl:consent.biometric from localStorage
- Next analysis will re-trigger consent modal
- File: AppLayout.jsx (settings tab) or PrivacyPolicy.jsx

**Fix 8**: Delay visitor ID until consent
- Move `fl:visitor-id` and `fl:visit-count` creation from analytics constructor to after consent check
- If no consent: generate ephemeral session ID (not persisted)
- File: analytics.js

---

### Scope
- FE only — desktop2
- No backend changes
- No frozen contract impact

**Handoff: CPO → FE Lead (all 8 fixes) → QA Lead (verify) → Change Manager (CR-0005)**
