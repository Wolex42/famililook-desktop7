# Spec: Complete Tiering Enforcement — Every Feature Gated

> **Author**: CEO + CPO
> **Date**: 2026-04-02
> **Priority**: P0 — Revenue-critical. Ungated features = lost subscription revenue.
> **Status**: SPEC_READY
> **Scope**: desktop2 (FE), desktop4 (FamiliPoker), desktop6 (FamiliMatch)

---

## 1. Problem

Multiple features have no tier enforcement. Users access Plus/Pro content for free because the gates were never built. This directly undermines subscription revenue — why pay £3.99/mo when everything is already accessible?

### Ungated features (confirmed)

| Feature | Where | Should be | Currently |
|---------|-------|-----------|-----------|
| FamiliPoker (all games) | desktop4 | **Plus** | Completely free, no gate |
| Face Match | desktop2 CardGame.jsx | **Plus** | No plan check |
| Face Fusion | desktop2 CardGame.jsx | **Plus** | No plan check |
| Memory Match (adult) | desktop2 CardGame.jsx | **Plus** | No kids/adult split |
| Hungry Heads | desktop2 CardGame.jsx | **Plus** | Unclear enforcement |
| Feature Catch | desktop2 CardGame.jsx | **Plus** | Unclear enforcement |
| FamiliMatch Duo | desktop6 | **Plus** | May have gating, needs verification |
| FamiliMatch Group | desktop6 | **Plus** | May have gating, needs verification |

---

## 2. Approved Tiering Matrix (CEO-approved)

### FREE (no sign-up, no payment)

| Feature | Rationale |
|---------|-----------|
| Individual analysis (5 per 14 days) | Core product, drives uploads |
| Group photo analysis (5 per 14 days, shared count) | Needed for occasion card funnels |
| FamiliUno digital (real cards, no placeholders) | Core game, drives physical deck orders |
| Memory Match — kids level only | Low-friction family fun, viral with parents |
| FamiliMatch Solo | Onboarding for comparison features, 2 photos = lowest friction |
| Treasure ordering at full price (no discount) | Homepage fast-track needs ordering |
| Digital download (PNG) | Free shareability, viral acquisition |
| Share results | Viral loop |

### PLUS (£3.99/mo or £29.99/yr)

| Feature | Rationale |
|---------|-----------|
| Unlimited analyses | Upgrade incentive |
| Face Match | Intermediate game — requires analysis data |
| Face Fusion | Premium visual feature |
| Memory Match — adult levels | Kids free, adults gated |
| Hungry Heads | Premium game |
| Feature Catch | Premium game |
| **FamiliPoker (all modes)** | Premium game, 18+ content, subscription feature |
| FamiliMatch Duo | Premium social comparison |
| FamiliMatch Group | Premium social comparison |
| 10% treasure discount | Reward for subscribing |
| Saved sessions | Convenience feature |
| Unlimited pets with full analysis | Extended feature |
| Pet cards in deck | Extended feature |

### PRO (£7.99/mo or £49.99/yr)

| Feature | Rationale |
|---------|-----------|
| Everything in Plus | |
| FamiliUno Lobby (P2P multiplayer) | Premium social |
| Explain-why scoring | Advanced detail |
| 15% treasure discount | Best rate |
| Priority support | Premium perk |
| Early access | Premium perk |
| Pet merchandise | Extended feature |

---

## 3. Implementation — Desktop2 (FamiliLook FE)

### 3.1 Add tier flags to planConfig.js

Add these fields to each tier's `limits` object:

```javascript
// FREE tier limits — add:
faceMatch: false,
faceFusion: false,
memoryMatchAdult: false,
hungryHeads: false,
featureCatch: false,
pokerAccess: false,

// PLUS tier limits — add:
faceMatch: true,
faceFusion: true,
memoryMatchAdult: true,
hungryHeads: true,
featureCatch: true,
pokerAccess: true,

// PRO tier limits — add (same as Plus):
faceMatch: true,
faceFusion: true,
memoryMatchAdult: true,
hungryHeads: true,
featureCatch: true,
pokerAccess: true,
```

### 3.2 Add helper functions to usePlanFeatures.js

```javascript
const canPlayFaceMatch = () => isUnlocked() || planLimits.faceMatch === true;
const canPlayFaceFusion = () => isUnlocked() || planLimits.faceFusion === true;
const canPlayMemoryMatchAdult = () => isUnlocked() || planLimits.memoryMatchAdult === true;
const canPlayHungryHeads = () => isUnlocked() || planLimits.hungryHeads === true;
const canPlayFeatureCatch = () => isUnlocked() || planLimits.featureCatch === true;
const canPlayPoker = () => isUnlocked() || planLimits.pokerAccess === true;
```

Export all of these from the hook.

### 3.3 Gate games in CardGame.jsx

Find where each game mode is launched/selected. Before allowing play, check the plan:

```jsx
const { canPlayFaceMatch, canPlayFaceFusion, canPlayMemoryMatchAdult,
        canPlayHungryHeads, canPlayFeatureCatch } = usePlanFeatures();

// When user selects a game:
if (selectedGame === 'face_match' && !canPlayFaceMatch()) {
  showUpgradePrompt('Face Match', 'Plus');
  return;
}
```

#### Upgrade prompt component

Create a reusable `GameUpgradePrompt`:

```jsx
function GameUpgradePrompt({ gameName, requiredTier, onClose }) {
  return (
    <div style={{ /* modal overlay */ }}>
      <div style={{ /* card */ }}>
        <h3>🔒 {gameName} requires {requiredTier}</h3>
        <p>Upgrade to {requiredTier} to unlock {gameName} and more games.</p>
        <Link to="/plans" style={{ /* violet CTA */ }}>
          Upgrade to {requiredTier} — £3.99/mo →
        </Link>
        <button onClick={onClose}>Maybe later</button>
      </div>
    </div>
  );
}
```

#### Memory Match kids/adult split

Memory Match currently has no age level concept. Two approaches:

**Option A (simple):** Memory Match is entirely free. Skip the adult gating.
**Option B (proper):** Add a difficulty selector (Easy/Medium/Hard). Easy = free. Medium/Hard = Plus.

Recommend **Option A** for now — Memory Match is a simple card-flip game that doesn't benefit from age gating. Revisit if it becomes a conversion issue.

### 3.4 Gate FamiliPoker link on homepage

The homepage pillbox links to FamiliPoker (desktop4). Gate the link:

```jsx
// In HomePage.jsx pillbox:
{
  name: 'FamiliPoker',
  icon: '🎰',
  href: canPlayPoker() ? (import.meta.env.VITE_FAMILIPOKER_URL || '...') : '/plans',
  gradient: '#bf5af2',
  badge: canPlayPoker() ? null : 'Plus',
}
```

If Free user taps FamiliPoker → routes to `/plans` instead of the poker app. Shows a "Plus" badge on the pillbox.

Also gate in the Game Night occasion card:

```jsx
// Card 3 (Game night) CTA:
cta: canPlayPoker() ? 'Start game night →' : 'Upgrade to play →',
link: canPlayPoker() ? '/app?intent=self&product=card_deck' : '/plans',
```

### 3.5 Gate in OccasionShelf games strip

The games strip in OccasionShelf already shows "Plus →" for Plus games. Verify this works correctly with the new plan flags. The free games row should only show games the user can actually play.

---

## 4. Implementation — Desktop4 (FamiliPoker)

FamiliPoker is a separate app. It needs its own gate.

### 4.1 Session token approach

When a Plus/Pro user navigates to FamiliPoker from FamiliLook:
1. FamiliLook generates a short-lived session token (stored in localStorage)
2. FamiliPoker URL includes the token: `?session=abc123`
3. FamiliPoker validates the token against the backend
4. If invalid/missing → shows upgrade prompt with link back to FamiliLook `/plans`

### 4.2 Simpler approach (recommended for now)

FamiliPoker checks `localStorage` for `fl:plan`. Since both apps share the same domain origin (`famililook.com` subdirectories or same-origin), they can read the same localStorage.

**If different origins** (Vercel deploys to different subdomains):
- Pass plan via URL param: `?plan=plus`
- FamiliPoker reads param, shows game if plus/pro, shows upgrade if free/missing
- This is bypassable but acceptable for MVP — proper token auth comes later

### 4.3 FamiliPoker gate component

In desktop4, create a gate wrapper:

```jsx
function PlanGate({ children }) {
  const plan = new URLSearchParams(window.location.search).get('plan')
    || localStorage.getItem('fl:plan')
    || 'free';

  if (plan === 'free' || !plan) {
    return (
      <div>
        <h2>🎰 FamiliPoker requires Plus</h2>
        <p>Upgrade to Plus (£3.99/mo) to unlock FamiliPoker and 5 more games.</p>
        <a href="https://famililook.com/plans">Upgrade now →</a>
      </div>
    );
  }

  return children;
}
```

### 4.4 Update FamiliPoker link in desktop2

When navigating to FamiliPoker, pass the plan:

```javascript
const pokerUrl = `${import.meta.env.VITE_FAMILIPOKER_URL}?plan=${currentPlan}`;
```

---

## 5. Implementation — Desktop6 (FamiliMatch)

### 5.1 Verify existing gating

FamiliMatch may already gate Duo/Group. Check:
- Does desktop6 read `fl:plan` from localStorage?
- Does it check plan before allowing Duo/Group modes?
- If not, apply same approach as desktop4.

### 5.2 FamiliMatch Solo must remain free

Solo mode is a free acquisition tool. Only Duo and Group are gated.

---

## 6. Plans Page Update

The Plans page comparison table needs updating to reflect the complete tiering:

```javascript
// PlansPage.jsx comparison table rows:
{ name: 'Analyses', free: '5 per 2 weeks', plus: 'Unlimited', pro: 'Unlimited' },
{ name: 'Group Photos', free: '✓', plus: '✓', pro: '✓' },
{ name: 'Memory Match', free: '✓', plus: '✓', pro: '✓' },
{ name: 'FamiliUno (digital)', free: '✓', plus: '✓', pro: '✓' },
{ name: 'FamiliMatch Solo', free: '✓', plus: '✓', pro: '✓' },
{ name: 'Face Match', free: '—', plus: '✓', pro: '✓' },
{ name: 'Face Fusion', free: '—', plus: '✓', pro: '✓' },
{ name: 'Hungry Heads', free: '—', plus: '✓', pro: '✓' },
{ name: 'Feature Catch', free: '—', plus: '✓', pro: '✓' },
{ name: 'FamiliPoker', free: '—', plus: '✓', pro: '✓' },
{ name: 'FamiliMatch Duo', free: '—', plus: '✓', pro: '✓' },
{ name: 'FamiliMatch Group', free: '—', plus: '✓', pro: '✓' },
{ name: 'FamiliUno Lobby (P2P)', free: '—', plus: '—', pro: '✓' },
{ name: 'Treasure Ordering', free: 'Full price', plus: '10% off', pro: '15% off' },
{ name: 'Treasure Discount', free: '—', plus: '10%', pro: '15%' },
{ name: 'Uno Deck Order', free: 'Full price', plus: '10% off', pro: '15% off' },
{ name: 'Saved Sessions', free: '—', plus: '✓', pro: '✓' },
{ name: 'Explain-Why Scoring', free: '—', plus: '—', pro: '✓' },
{ name: 'Priority Support', free: '—', plus: '—', pro: '✓' },
```

---

## 7. File Changes

### Desktop2 (FamiliLook FE)

| File | Change | Effort |
|------|--------|--------|
| `src/utils/planConfig.js` | Add 6 game tier flags to each plan | S |
| `src/hooks/usePlanFeatures.js` | Add 6 canPlay helper functions | S |
| `src/game/CardGame.jsx` | Gate Face Match, Face Fusion, Hungry Heads, Feature Catch | M |
| `src/components/cardgame/GameSimulation.jsx` | Gate poker-betting mode | S |
| `src/pages/HomePage.jsx` | Gate FamiliPoker pillbox link + Game Night occasion card | S |
| `src/pages/PlansPage.jsx` | Update comparison table with full feature list | S |
| `src/components/results/OccasionShelf.jsx` | Verify games strip gating works | S |
| `src/components/ui/GameUpgradePrompt.jsx` | **NEW** — reusable upgrade prompt modal | S |
| Tests for all above | Unit tests for each gate | M |

### Desktop4 (FamiliPoker FE)

| File | Change | Effort |
|------|--------|--------|
| Gate wrapper component | **NEW** — PlanGate checks plan param/localStorage | S |
| Main entry point | Wrap app in PlanGate | S |

### Desktop6 (FamiliMatch FE)

| File | Change | Effort |
|------|--------|--------|
| Verify existing Duo/Group gating | Read code, confirm enforcement | S |
| Add gate if missing | Similar to desktop4 PlanGate | S |

---

## 8. Agent Assignments

| Step | Agent | Task | Repo |
|------|-------|------|------|
| 1 | qa_lead | Audit current game gating — verify which games check plans | desktop2 |
| 2 | fe_lead | Add tier flags to planConfig.js + helpers to usePlanFeatures.js | desktop2 |
| 3 | fe_lead | Create GameUpgradePrompt component | desktop2 |
| 4 | fe_lead | Gate CardGame.jsx — Face Match, Face Fusion, Hungry Heads, Feature Catch | desktop2 |
| 5 | fe_lead | Gate FamiliPoker link + Game Night card on homepage | desktop2 |
| 6 | fe_lead | Update PlansPage comparison table | desktop2 |
| 7 | qa_lead | Tests for all gates — free blocked, plus allowed, upgrade prompt shown | desktop2 |
| 8 | fe_lead | Create PlanGate for FamiliPoker | desktop4 |
| 9 | fe_lead | Verify/add Duo+Group gate for FamiliMatch | desktop6 |
| 10 | qa_lead | E2E: free user → blocked game → upgrade prompt → plans page | desktop2 |

---

## 9. Acceptance Criteria

### Desktop2 games
- [ ] Free user selecting Face Match → sees upgrade prompt, not game
- [ ] Free user selecting Face Fusion → sees upgrade prompt
- [ ] Free user selecting Hungry Heads → sees upgrade prompt
- [ ] Free user selecting Feature Catch → sees upgrade prompt
- [ ] Plus user can play all 4 gated games
- [ ] Memory Match works for all tiers (keeping it free per Option A)
- [ ] FamiliUno digital works for all tiers
- [ ] FamiliMatch Solo works for all tiers

### FamiliPoker
- [ ] Free user tapping FamiliPoker pillbox → goes to /plans (not poker app)
- [ ] Plus user tapping FamiliPoker → goes to poker app with plan param
- [ ] FamiliPoker app shows upgrade prompt if plan=free or missing
- [ ] FamiliPoker app allows play if plan=plus or plan=pro

### FamiliMatch
- [ ] Solo mode works for free users
- [ ] Duo mode blocked for free users (upgrade prompt)
- [ ] Group mode blocked for free users (upgrade prompt)

### Plans page
- [ ] Comparison table shows ALL features with correct tier marks
- [ ] Free column shows what's included and what's locked
- [ ] Plus column shows all unlocked features
- [ ] Pro column shows Plus + extras

### Homepage
- [ ] FamiliPoker pillbox shows "Plus" badge for free users
- [ ] Game Night occasion card shows "Upgrade to play →" for free users
- [ ] All other occasion cards work for free users

---

## 10. Revenue Impact

At current traffic (7 users/day), even 1 conversion to Plus per week = £17/month recurring.

The games are the primary upgrade hook — users discover them for free (Memory Match, Uno, Solo), get hooked, then hit the gate on the premium games (Face Match, Poker, Duo). The gate must feel like an invitation ("unlock 6 more games for £3.99/mo") not a wall.

The upgrade prompt copy should emphasise what they GET, not what they're blocked from:
- "Unlock Face Match, Face Fusion, FamiliPoker, and 3 more games"
- "Plus members get 10% off all treasures too"
- "£3.99/mo · Cancel anytime"
