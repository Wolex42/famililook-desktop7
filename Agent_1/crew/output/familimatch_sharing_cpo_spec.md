## CPO Spec: FamiliMatch Sharing + Match History (H10, H12)

**Agent**: CPO
**Date**: 2026-03-23
**Product**: FamiliMatch (desktop6)
**Why now**: Best unit economics ($2.50 CPI, 3-month payback) but zero viral loop.

---

### Feature H10: Result Screenshot Sharing

**What**: After Solo/Duo comparison, user can share their result as an image.
**Why**: Every share = free acquisition. Face comparison results are inherently shareable content.

**What to build**:
- Share card component: percentage, chemistry label, feature breakdown (no real faces — privacy)
- "Share" button on results screen
- html2canvas captures the share card as PNG
- Web Share API (mobile native share sheet) with fallback to download
- Pre-filled share text: "We're X% alike! Try FamiliMatch → [link]"
- Analytics: `match_result_shared` event

**Acceptance Criteria**:
- [ ] Share card renders without actual face photos (privacy — use silhouettes or initials)
- [ ] Share card includes: percentage, chemistry label + colour, names, feature matches count
- [ ] Web Share API works on mobile Safari + Chrome
- [ ] Fallback: download PNG if share API unavailable
- [ ] Share text includes famililook-desktop6.vercel.app link
- [ ] Analytics event fires on share

**Files**: desktop6 — new ShareCard.jsx component, update SoloPage.jsx + ResultsPage.jsx
**Effort**: M

---

### Feature H12: Match History

**What**: Users can see their past comparisons (stored in localStorage).
**Why**: Repeat engagement. Users come back to compare with new people.

**What to build**:
- After each comparison, save result to `fl:match_history` in localStorage
- History entry: `{ name_a, name_b, percentage, chemistry_label, timestamp }`
- Max 20 entries (FIFO)
- History section on landing page: "Recent Matches" list
- Tap to view details (no photos stored — just scores)

**Acceptance Criteria**:
- [ ] Results saved after Solo and Duo completions
- [ ] Max 20 entries, oldest removed first
- [ ] "Recent Matches" section on LandingPage
- [ ] Each entry shows: names, percentage, chemistry label, date
- [ ] "Clear History" button
- [ ] No photos or biometric data stored in history (just scores + names)

**Files**: desktop6 — new useMatchHistory.js hook, update LandingPage.jsx, SoloPage.jsx
**Effort**: S

---

**Handoff: CPO → FE Lead (desktop6)**
