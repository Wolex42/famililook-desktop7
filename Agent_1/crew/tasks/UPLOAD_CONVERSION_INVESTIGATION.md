# Task: Upload Conversion Drop-off Investigation

**Date**: 2026-03-28
**Priority**: P1 — Revenue-critical (zero analyses despite 15 daily users)
**Raised by**: CEO
**Trigger**: Dashboard shows 116 page views → 0 uploads → 0 analyses. Users explore Trail, tap games, browse — but nobody uploads photos.

---

## The Problem

Users don't understand WHY they should upload family photos. The value proposition isn't landing. They see a cool app, explore the Trail, peek at games — but never take the core action (upload photos → run analysis).

Dashboard evidence (2026-03-28):
- 15 unique users, 52 sessions (engaged, returning)
- 141 Trail peeks, 19 node clicks (exploring)
- 12 game launches (curious)
- 14 "Try It Now" taps (interested!)
- **0 uploads, 0 analyses** (but WHY would I?)
- 3 upgrade clicks (some monetisation intent)

The funnel is broken at the **motivation** step, not the mechanics.

---

## Hypothesis

Users land on the homepage or Trail and see:
1. "Every family has a story written in their faces" — poetic but vague
2. A Trail with locked nodes and game names — fun to explore but doesn't explain the payoff
3. "Try It Now" button — takes them to upload, but they don't know what they'll GET

What's missing: a clear, visual preview of what the RESULT looks like BEFORE they upload. They need to see "oh, THAT'S what I get" — the winner card, the feature breakdown, the keepsakes, the games populated with their faces.

---

## Agent Assignments

### UX Researcher
Investigate the current user journey from landing → upload:
1. Read the homepage (HomePage.jsx) — what does the user see first?
2. Read the upload flow (UploadSection.jsx) — what's the first thing asked of them?
3. Read the Trail landing (TrailHomePage.jsx) — does it explain why uploading matters?
4. Check: is there ANY preview of results shown BEFORE the user uploads?
5. Check: what does the "Try It Now" CTA actually link to? Where does the user land?
6. Map the full journey: homepage → CTA → upload → consent → analysis → results
7. Identify every friction point and motivation gap

### CPO (Product)
Based on UX Researcher findings:
1. What should the user understand BEFORE they upload?
2. What's the minimum viable "value preview" that would motivate upload?
3. Should the homepage show an example result (demo family, anonymised)?
4. Should the Trail explain "upload to unlock" more explicitly?
5. What's the 1-sentence value prop that makes someone think "I NEED to see this for my family"?

### Copywriter
Review all user-facing copy on the path to upload:
1. Homepage taglines (rotating CTAs we just added)
2. Trail node descriptions
3. Upload page prompts
4. Consent modal text
5. Identify where copy is vague/poetic vs concrete/compelling
6. Propose copy that answers "what will I get if I upload?"

### Conversion Specialist
Propose specific conversion improvements:
1. Social proof (the "12,847 comparisons made" counter — is it visible enough?)
2. Example results preview (before/after of what the analysis produces)
3. Urgency/scarcity (limited free analyses per day — is this communicated?)
4. Trust signals (GDPR, "never stored", EU servers — visible at decision point?)
5. Reduce steps between interest and upload (can we cut friction?)

---

## Deliverable

Each agent produces findings + recommendations in their output format.
CPO synthesises into a prioritised action list.
NO code changes — this is research and strategy only.
Code changes will be a separate task after CEO reviews recommendations.

---

## Context Files

- `src/pages/HomePage.jsx` — Landing page with rotating taglines
- `src/pages/TrailHomePage.jsx` — Trail with node exploration
- `src/layout/UploadSection.jsx` — Photo upload flow
- `src/components/ConsentBanner.jsx` — GDPR/biometric consent
- `src/pages/AnalyticsDashboard.jsx` — Dashboard data reference
- `docs/ADVERTISING_AND_CAMPAIGNS.md` — Marketing positioning
- `docs/PLATFORM_ARCHITECTURE.md` — Full system overview
