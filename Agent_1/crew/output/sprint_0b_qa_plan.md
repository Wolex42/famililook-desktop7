# Sprint 0B QA Plan

**Date:** 2026-03-31
**Author:** QA Lead Agent
**Phase:** 3 (QA Planning)
**Products:** FamiliPoker (desktop4), FamiliLook (desktop2)
**Items:** 7

---

## PER-ITEM ASSESSMENT

---

### FP-003: FeaturePoker Back button loops to SETUP

**ROOT CAUSE:**
- File: `famililook-desktop4/src/layout/AppLayout.jsx` line 538
- Exact text: `{selectedGame === "poker" && <FeaturePoker onBack={() => setSelectedGame("poker")} />}`
- The `onBack` callback sets `selectedGame` to `"poker"` — the same value it already has. This means pressing Back in FeaturePoker re-renders FeaturePoker (its SETUP screen) instead of returning to the GameRooms lobby.
- Compare with line 539 (Feature21/Blackjack) which correctly uses `setSelectedGame(null)`.

**ACCEPTANCE CRITERIA:**
1. Pressing Back in FeaturePoker returns the user to the GameRooms lobby (selectedGame === null, no game component rendered).
2. Feature21/Blackjack Back button behaviour is unchanged (already correct).
3. Re-entering FeaturePoker after backing out shows the SETUP screen cleanly.

**TEST CASES:**
1. Navigate to Cards tab > select Poker > press Back button inside FeaturePoker > verify GameRooms lobby is displayed with both game tiles visible.
2. Navigate to Cards tab > select Blackjack > press Back > verify GameRooms lobby (regression).
3. Navigate to Poker > Back > re-enter Poker > verify SETUP screen loads fresh.

**REGRESSION RISKS:**
- If `null` causes the GameRooms component to not render, the lobby would be blank. Low risk — Feature21 already uses the same pattern on line 539.
- Tab switching between "cards" and "home" tabs while a game is selected.

**DFMEA:** Sev 8 | Occ 10 | Det 8 = RPN 640

---

### FP-001: Analysis errors not displayed in Poker

**ROOT CAUSE:**
- File: `famililook-desktop4/src/layout/AppLayout.jsx` lines 270-275
- The `useKinshipAnalysis` hook destructure only extracts `canAnalyze`, `isAnalyzing`, `runAnalysis`.
- The hook DOES export `error` (line 585) and `clearError` (line 586) in `useKinshipAnalysis.jsx`, but AppLayout never reads them.
- There is NO error rendering UI anywhere in desktop4's AppLayout — `grep` for "error", "Error", "alert" returned zero matches in the file.
- This means if an analysis fails (network error, backend down, invalid photo), the user sees nothing — the spinner just stops and the screen goes silent.

**ACCEPTANCE CRITERIA:**
1. `error` and `clearError` are destructured from `useKinshipAnalysis()`.
2. When `error` is truthy, a visible error banner/toast is rendered with the error message.
3. The error banner has a dismiss/clear action that calls `clearError`.
4. After clearing the error, the user can retry analysis.
5. Error state does not persist across tab switches.

**TEST CASES:**
1. Simulate network failure during analysis > verify error message is displayed.
2. Dismiss the error > verify error banner disappears and Analyze button is re-enabled.
3. Trigger error > switch tabs > return to home tab > verify error is cleared.
4. Successful analysis after previous error > verify results display normally.

**REGRESSION RISKS:**
- Adding error UI near the analysis section could shift layout and push content below the fold on small screens.
- Error state interaction with `isAnalyzing` — ensure mutual exclusivity (not showing spinner AND error simultaneously).

**DFMEA:** Sev 9 | Occ 4 | Det 10 = RPN 360

---

### FL-003: OrderSuccessPage dark theme broken

**ROOT CAUSE:**
- File: `famililook-desktop2/src/pages/OrderSuccessPage.jsx` line 75
- Exact text: `background: colors.bgPrimary,`
- `colors.bgPrimary` does NOT exist in `famililook-desktop2/src/theme/colors.js`. The correct token is `colors.bgMain` (line 7, value `"#0D0F1A"`).
- Since `bgPrimary` is undefined, `background` evaluates to `undefined`, which means the browser uses its default (white). On a dark-themed page, this produces a white flash / white background behind the order success card — breaking the dark theme entirely.

**ACCEPTANCE CRITERIA:**
1. `colors.bgPrimary` is replaced with `colors.bgMain` on OrderSuccessPage line 75.
2. The OrderSuccessPage renders with the `#0D0F1A` deep navy background.
3. All text on the page has adequate contrast against `bgMain` (already true — text tokens are light-on-dark).
4. No other file in desktop2 references `colors.bgPrimary` (verify no other instances of the same bug).

**TEST CASES:**
1. Complete a test order > land on OrderSuccessPage > verify background is dark navy (#0D0F1A), not white.
2. Inspect computed styles — `background` should resolve to `rgb(13, 15, 26)`.
3. Verify card content (bgCard `#161828`) is visible against bgMain.
4. Check mobile viewport (390px) — no white flashes or background bleed.

**REGRESSION RISKS:**
- Minimal. This is a direct token rename, not a logic change.
- Grep for `bgPrimary` across all desktop2 files to find any other broken references.

**DFMEA:** Sev 7 | Occ 10 | Det 8 = RPN 560

---

### FL-004: from=home back navigation wrong

**ROOT CAUSE:**
- File: `famililook-desktop2/src/layout/AppLayout.jsx` line 340
- Exact text: `to={new URLSearchParams(window.location.search).get('from') === 'trail' ? '/trail' : '/hub'}`
- This is a simple ternary that only checks for `from=trail`. ALL other `from` values (including `from=home`, `from=results`) fall through to `/hub`.
- Per CLAUDE.md cross-product navigation spec:
  - `from=results` should go to `/` (analysis results)
  - `from=home` should go to `/`
  - `from=hub` should go to `/hub`
  - `from=trail` should go to `/trail`
  - No param defaults to `/hub`
- Currently `from=home` and `from=results` both incorrectly route to `/hub`.

**ACCEPTANCE CRITERIA:**
1. `from=trail` navigates back to `/trail` (existing, must stay).
2. `from=results` navigates back to `/` (currently broken).
3. `from=home` navigates back to `/` (currently broken).
4. `from=hub` navigates back to `/hub` (currently works by accident via default).
5. No `from` param defaults to `/hub` (currently works).

**TEST CASES:**
1. Navigate to page with `?from=trail` > press back/logo > verify lands on `/trail`.
2. Navigate to page with `?from=results` > press back/logo > verify lands on `/`.
3. Navigate to page with `?from=home` > press back/logo > verify lands on `/`.
4. Navigate to page with `?from=hub` > press back/logo > verify lands on `/hub`.
5. Navigate to page with no `from` param > press back/logo > verify lands on `/hub`.
6. Navigate to page with `?from=bogus` > press back/logo > verify lands on `/hub` (unknown values default).

**REGRESSION RISKS:**
- If the replacement logic uses a switch/map incorrectly, `from=trail` (currently working) could break.
- Deep-links with `from` params from external sources (ads, emails) — verify they still resolve correctly.

**DFMEA:** Sev 6 | Occ 6 | Det 8 = RPN 288

---

### FL-006: Pet analysis in Coming Soon

**ROOT CAUSE:**
- File: `famililook-desktop2/src/layout/AppLayout.jsx` lines 808-814
- The Coming Soon section contains: `"Pet analysis"`, `"More games"`, `"Share & export"`
- Pet analysis IS a shipped feature (it exists in the platform), yet it is listed as "Coming Soon" — misleading users into thinking it is unavailable.
- There IS a "What's Included" section directly above (lines 781-793) that lists current features: Memory Match, Hungry Heads, Face Fusion, Group photo detection, 8 facial feature analysis. Pet analysis should be listed here if it is live.

**ACCEPTANCE CRITERIA:**
1. "Pet analysis" is removed from the Coming Soon array.
2. Pet analysis is added to the "What's Included" array (e.g., "Pet analysis" with appropriate emoji).
3. The Coming Soon section still renders with remaining items ("More games", "Share & export").
4. If Coming Soon has only 2 items, the section still renders correctly (no empty state, no layout break).

**TEST CASES:**
1. Open About/Settings tab > scroll to "What's Included" > verify "Pet analysis" is listed.
2. Scroll to "Coming Soon" > verify "Pet analysis" is NOT listed.
3. Verify Coming Soon section has "More games" and "Share & export" only.
4. Visual check: no layout shift, correct spacing with changed item counts.

**REGRESSION RISKS:**
- If pet analysis is only partially shipped (e.g., behind a plan gate), listing it in "What's Included" without qualification could confuse free-tier users. Verify pet analysis availability per plan.
- Item count changes may cause subtle layout shifts if the sections use fixed heights.

**DFMEA:** Sev 5 | Occ 10 | Det 8 = RPN 400

---

### FP-006: Analytics dev bypass missing

**ROOT CAUSE:**
- File: `famililook-desktop4/src/analytics.js` lines 1-12
- The `isConsentGiven()` function checks `localStorage.getItem('fl:consent')` and returns false if not found.
- There is NO `import.meta.env.DEV` bypass anywhere in the file.
- In dev mode, `ConsentBanner.jsx` returns `null` (never shown), so `fl:consent` is never set in localStorage, so `isConsentGiven()` returns `false`, so ALL analytics events are silently dropped.
- The `track()` method on line 96 gates on `isConsentGiven()` — every event is lost in dev.
- Compare with desktop2's pattern (`src/utils/analytics.js` line 170): `if (import.meta.env.DEV) return true;` inside `hasAnalyticsConsent()`.

**ACCEPTANCE CRITERIA:**
1. The analytics consent check includes a DEV bypass: when `import.meta.env.DEV` is true, consent is assumed.
2. The bypass is at the top of `isConsentGiven()` (or equivalent), before the localStorage check.
3. Production behaviour is unchanged — the bypass only fires in dev mode.
4. Analytics events are logged to console in dev mode (verify `logger.analytics` or equivalent is called).

**TEST CASES:**
1. In dev mode, trigger any analytics event > verify it is sent to backend (check Network tab or console log).
2. In dev mode, verify `fl:consent` is NOT in localStorage (consent banner hidden) > verify events still fire.
3. In production build, with no consent given > verify events are NOT sent (privacy preserved).
4. In production build, with consent given > verify events ARE sent.

**REGRESSION RISKS:**
- If the bypass is placed incorrectly (e.g., outside the consent function, or applied globally), it could leak analytics in production without consent — GDPR violation.
- Must be guarded by `import.meta.env.DEV` which is compile-time dead-code-eliminated in production builds.

**DFMEA:** Sev 3 | Occ 10 | Det 10 = RPN 300

---

### FP-007: Wrong client ID

**ROOT CAUSE:**
- File: `famililook-desktop4/src/hooks/useKinshipAnalysis.jsx` line 337
- Exact text: `client: "famililook-desktop2",`
- The meta payload sent to the backend identifies the client as `"famililook-desktop2"` (FamiliLook) instead of `"famililook-desktop4"` (FamiliPoker).
- This was likely a copy-paste error when the hook was ported from desktop2 to desktop4.
- Impact: backend analytics, rate limiting, and any client-specific logic will attribute Poker traffic to FamiliLook, corrupting analytics data and potentially applying wrong business rules.

**ACCEPTANCE CRITERIA:**
1. The `client` field in the meta payload is `"famililook-desktop4"`.
2. Backend receives the correct client ID for all Poker analyses.
3. No other hardcoded "desktop2" references exist in desktop4 (search the entire repo).

**TEST CASES:**
1. Run an analysis in FamiliPoker > inspect the request payload in Network tab > verify `client: "famililook-desktop4"`.
2. Grep desktop4 codebase for `"famililook-desktop2"` — should return zero results after fix.
3. Backend logs: verify new analyses from Poker show client=famililook-desktop4.

**REGRESSION RISKS:**
- If the backend has client-specific logic (e.g., different thresholds for desktop2 vs desktop4), changing the client ID could trigger different behaviour. Verify backend treats desktop4 identically or appropriately.
- If rate limiting is per-client, desktop4 users would get their own quota instead of sharing desktop2's — this is actually correct behaviour.

**DFMEA:** Sev 6 | Occ 10 | Det 10 = RPN 600

---

## CROSS-CUTTING TESTS

After ALL fixes are applied:

- `npm run test:run` (desktop2) — must pass
- `npm run build` (desktop2) — must succeed
- `npm run test:run` (desktop4) — must pass
- `npm run build` (desktop4) — must succeed
- Grep `bgPrimary` across desktop2 — zero results
- Grep `famililook-desktop2` across desktop4 — zero results
- Grep `DEV` in desktop4 analytics.js — must find the bypass

---

## PRIORITY ORDER (by RPN)

| Rank | ID     | Title                              | RPN | Product  |
|------|--------|------------------------------------|-----|----------|
| 1    | FP-003 | FeaturePoker Back button loops     | 640 | desktop4 |
| 2    | FP-007 | Wrong client ID                    | 600 | desktop4 |
| 3    | FL-003 | OrderSuccessPage dark theme broken | 560 | desktop2 |
| 4    | FL-006 | Pet analysis in Coming Soon        | 400 | desktop2 |
| 5    | FP-001 | Analysis errors not displayed      | 360 | desktop4 |
| 6    | FP-006 | Analytics dev bypass missing       | 300 | desktop4 |
| 7    | FL-004 | from=home back navigation wrong    | 288 | desktop2 |

---

## HANDOFF

**To:** FE Lead
**Task:** Implement all 7 fixes per the acceptance criteria above.
**Context:** All root causes confirmed by reading source files. Acceptance criteria defined. Regression risks identified.
**Artifacts:** This QA plan (`crew/output/sprint_0b_qa_plan.md`)
**Recommended implementation order:** By RPN (highest first), grouping by repo where possible (desktop4 items together, desktop2 items together) for batch efficiency.

---

*Sprint 0B QA Plan v1.0 — 2026-03-31 — QA Lead Agent*
