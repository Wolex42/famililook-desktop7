# Task: Upload Conversion Fixes — Show Value Before Asking for Photos

**Date**: 2026-03-28
**Priority**: P1 — Revenue-critical (0% upload conversion despite engaged traffic)
**Raised by**: CEO
**Source**: Combined findings from UX Researcher, Conversion Specialist, Copywriter (2026-03-28)
**Change Control**: CR-0006 — All edits require diff preview + CEO approval

---

## Problem Statement

15 daily users, 52 sessions, 14 "Try It Now" taps — but 0 uploads, 0 analyses. Users explore the Trail and tap CTAs but never upload photos because they don't know what they'll get. The entire funnel asks for commitment without showing the payoff.

---

## Fixes (5 items, ordered by impact)

### Fix 1: Example Result Preview on Homepage
**File**: `src/pages/HomePage.jsx`
**What**: Add a static "Here's what you'll discover" section above the portal CTA, showing a demo result card with:
- A mock winner display: "62% Mum" with feature icons
- 8-feature grid preview (eyes: Mum, nose: Dad, etc.)
- A keepsake card mockup thumbnail
- One-line: "Upload 3 photos. See which parent your child looks like — feature by feature."

**Approach**: Use inline styles (no Tailwind — matches codebase pattern). Static data, no API calls. Anonymised/illustrated — don't use real photos. Can use FeatureIcon components already in the codebase.

**Risk**: LOW — additive, doesn't change existing functionality
**Test**: Build passes, homepage renders without error, no layout shift on mobile

---

### Fix 2: Direct "Try It Free" CTA on Homepage
**File**: `src/pages/HomePage.jsx`
**What**: Add a prominent secondary button below the portal that links directly to `/app?intent=child&from=home`. Copy: "Try It Free — 30 Seconds" with the existing brand gradient.

Keep "Enter the Trail" as the primary exploration CTA. This adds a fast lane for motivated users.

**Approach**: Add a `<Link>` component below the portal button. Match existing button styling patterns.

**Risk**: LOW — additive
**Test**: Button renders, links to correct route, doesn't break portal animation

---

### Fix 3: Rewrite Biometric Consent Modal
**File**: `src/layout/UploadSection.jsx` (lines ~550-580, the biometric consent modal)
**What**: Replace legal-heavy copy with user-friendly version:

**Current title**: "Biometric Data Consent"
**New title**: "Your Privacy Matters"

**Current body**: "Your photos will be sent securely to our EU server for facial feature analysis. Facial embeddings (mathematical representations) are generated for comparison and deleted after your session. No biometric data is retained."
**New body**: "We'll compare your family's facial features — eyes, nose, smile, and more — to see who looks like who. Your photos are processed securely on EU servers and never stored. Analysis takes about 30 seconds, then your photos are deleted."

**Current legal**: "By proceeding, you consent to the processing of facial features under GDPR Art. 9 and applicable biometric privacy laws (including BIPA)."
**New legal** (smaller/secondary text): "We process facial features under GDPR Art. 9. You can revoke consent anytime from Settings."

**Current accept button**: "I Consent"
**New accept button**: "Let's Go" or "Start My Analysis"

**IMPORTANT**: Keep ALL legal compliance intact. The consent still captures `bipaConsented` in ConsentContext. Only the copy changes, not the mechanism.

**Risk**: MEDIUM — must verify consent still records correctly, GDPR/BIPA compliance maintained
**Test**: Consent flow works end-to-end, `bipaConsented` is set in state + localStorage after acceptance

---

### Fix 4: Social Proof Counter on Homepage
**File**: `src/pages/HomePage.jsx`
**What**: Add a visible counter near the CTAs: "X,XXX families have discovered their story"

**Approach**: Seed at a credible number (e.g. 12,800). Optionally increment slowly with a timer (like FamiliMatch's `useComparisonCount` pattern in desktop6). Place between the tagline and the portal button.

**Risk**: LOW — additive, cosmetic
**Test**: Counter renders, doesn't cause layout shift

---

### Fix 5: Homepage Copy Updates
**File**: `src/pages/HomePage.jsx` (TAGLINES array + portal section)
**What**: Replace rotating taglines with concrete value propositions:

| # | Current Main | Current Sub | New Main | New Sub |
|---|-------------|-------------|----------|---------|
| 1 | "Every family has a story" | "written in their faces" | "Who does your child look like more?" | "Mum or Dad? AI scans 8 facial features to settle it." |
| 2 | "Every family has a bond" | "written in their faces" | "Eyes like Mum, smile like Dad" | "Get a feature-by-feature breakdown for your family." |
| 3 | "Every family has a champion" | "challenge yours in bespoke games" | "Turn your family photos into cards & keepsakes" | "Winner cards, memory games, and prints — all from one upload." |

Update CTA sub-texts to match:
| # | Current CTA | New CTA |
|---|------------|---------|
| 1 | "Discover yours on FamiliTrail" | "See your results in 30 seconds" |
| 2 | "Capture the memory forever" | "Try it free — no sign-up" |
| 3 | "Play on FamiliTrail" | "Upload photos, get your family pack" |

**Risk**: LOW — copy-only change
**Test**: Taglines render and rotate correctly

---

## Agent Assignments

### FE Lead
Execute Fixes 1-5 in order. For EACH fix:
1. Show diff preview (old → new) with reasoning
2. Wait for CEO approval
3. Apply edit
4. Run `npm run test:run && npm run build`
5. Report result

ONE commit per fix. Do not bundle. Test between each.

### QA Lead
After ALL 5 fixes are applied:
1. Run full test suite
2. Verify consent flow still works (bipaConsented records correctly)
3. Verify homepage renders all new elements without layout issues
4. Verify the "Try It Free" CTA routes correctly
5. Ship/Fix/Block verdict

### Change Manager
Log each fix as a sub-entry under CR-0006 in `.claude/change_log.md`.

---

## Files in Scope

- `src/pages/HomePage.jsx` — Fixes 1, 2, 4, 5
- `src/layout/UploadSection.jsx` — Fix 3 (consent modal copy only)

NO other files should be modified. Update `.claude/working_set.txt` before starting.

---

## Rollback Plan

Each fix is a separate commit. If any fix causes regression:
```bash
git revert <sha> --no-commit && git commit -m "revert: Fix N caused regression"
```

No cascading reverts needed — fixes are independent.

---

## Success Criteria

Dashboard metrics to monitor over the next 7 days:
- **Uploads**: 0 → any (even 1 upload/day is success)
- **Analyses**: 0 → any
- **Try It Now → Upload conversion**: 0% → >10%
- **Consent acceptance rate**: track via analytics events
