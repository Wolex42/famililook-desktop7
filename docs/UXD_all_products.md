# User Experience Definitions — FML Platform (All Products)

**Document:** UXD-001
**Date:** 2026-03-31
**Source:** Source code audit of famililook-desktop2 (FamiliLook + FamiliUno), famililook-desktop4 (FamiliPoker), famililook-desktop6 (FamiliMatch)
**Status:** Baseline — defines expected UX at each step. Deviations are failure modes catalogued in FMEA_comprehensive.md.

---

## Global Mobile Requirements (All Products)

All flows must satisfy these requirements on every smartphone released 2022 or later:

| Requirement | Specification |
|---|---|
| Touch targets | Minimum 44×44pt (iOS HIG / Material 48dp) for all interactive elements |
| Vertical scroll | Native smooth scrolling; no blocked scroll containers |
| Horizontal scroll | Permitted only inside explicitly scrollable carousels with visible affordance |
| Pinch-to-zoom | Must not be disabled on content pages; optional on interactive canvases |
| Cognitive overload | No more than 3 primary actions visible per screen state |
| Font size | Minimum 16px body text; 14px for secondary labels |
| Tap response | Visual feedback within 100ms of tap (active state) |
| Loading feedback | Any operation >300ms must show a loading indicator |
| Error states | Every error must display: what went wrong + at least one actionable next step |
| Empty states | Every empty list/result state must display: label + CTA to populate it |
| Back navigation | Every screen reachable by user action must have a clear way back |
| Orientation | Portrait-primary; landscape must not break layout |

---

## PRODUCT 1: FamiliLook

**URL:** famililook.com
**Repo:** famililook-desktop2
**Backend:** famililook-desktop3 (/kinship/analyze, /face/morph, /detect)
**Purpose:** AI-powered facial kinship analysis — who does your child take after?

---

### Flow FL-1: First Visit / Landing

**Entry point:** famililook.com (/)

#### Step FL-1.1 — Homepage Load

**What the user sees:**
- Branded hero with rotating tagline (one of 3 every 9 seconds):
  - "Who Do You Look Like Most — Mum or Dad?"
  - "Finally Settle the Family Debate"
  - "Turn your family photos into cards & keepsakes"
- Example result preview card
- Social proof counter ("12,800+ families")
- Event countdown badges (seasonal: Mother's Day, Easter)
- Portal button → /trail
- Fast-lane CTA button → /app?intent=child&from=home
- Product pills (FamiliUno, FamiliPoker, FamiliMatch)
- Email capture form
- Animated particle drift background (18 particles)

**Available actions:**
1. Click "See Results in 30 Seconds" / fast-lane CTA
2. Click portal button → Trail
3. Click product pills
4. Enter email → subscribe

**Expected behavior:**
1. CTA → navigate to /app?intent=child&from=home; URL carries intent and from params; AppLayout pre-sets intent to "child"
2. Portal → navigate to /trail
3. Product pill → navigate to respective product URL
4. Email submission → POST to email capture endpoint; show "Thanks!" confirmation inline; no page navigation

**Expected error handling:**
- Email submit with invalid format: inline validation message "Please enter a valid email"
- Email submit failure (network): "Something went wrong — please try again"

**Mobile requirements:**
- CTA button: minimum 44pt height, full-width on mobile
- Rotating taglines must not cause layout shift
- Particles must not block touch events (pointer-events: none)
- Social proof counter visible without scroll on any 375px+ screen

---

#### Step FL-1.2 — A/B Trail Redirect

**What the user sees:**
- If VITE_TRAIL_DEFAULT_LANDING=true and first visit: immediate redirect to /trail
- On return visits: stays on /

**Expected behavior:**
- First-time redirect: analytics.track('trail_ab_test_assigned') fires before redirect
- Subsequent visits: no redirect; user stays on /

**Mobile requirements:** Redirect must complete within 200ms; no flash of / before /trail

---

### Flow FL-2: Trail Navigation Hub

**Entry point:** famililook.com/trail

#### Step FL-2.1 — Trail Map Load

**What the user sees:**
- Board-game style interactive canvas with feature nodes
- Each node: icon, label, lock status (locked = greyed + lock icon)
- Tier badge (Free / Plus / Pro)
- Footer: Home, Plans, Privacy, Terms links

**Available actions:**
1. Tap any node
2. Tap locked node
3. Tap footer links

**Expected behavior:**
1. Unlocked node tap: TrailTooltip opens at tap position with description, CTA button, plan badge
2. Locked node tap: TrailTooltip opens with lock label + "Upgrade to [Tier]" CTA → /plans
3. Footer links navigate to respective pages

**Mobile requirements:**
- Nodes: minimum 44pt touch target each
- Canvas must support pinch-to-zoom if all nodes don't fit viewport
- TrailTooltip must not overflow screen edges; must auto-position

---

#### Step FL-2.2 — Trail Tooltip

**What the user sees:**
- Popup: feature name, one-line description, CTA button, lock status
- If feature visited: "Visited" badge

**Available actions:**
1. Tap CTA → navigate to feature
2. Tap outside tooltip → dismiss
3. If locked: tap "Upgrade" → /plans
4. If locked: tap "Peek" → PeekPreview shows locked feature preview

**Expected behavior:**
1. CTA navigation carries ?from=trail so back button returns to /trail
2. Dismiss closes tooltip, canvas returns to neutral
3. Upgrade navigates preserving current state
4. PeekPreview: modal overlay showing blurred/teaser content; dismiss closes it

**Expected error handling:** None — static UI, no network calls

---

#### Step FL-2.3 — Trail Completion

**What the user sees:**
- All accessible nodes visited: confetti animation plays
- "You've explored everything available on your plan!" message

**Expected behavior:**
- Confetti triggers automatically when all accessible node IDs are in localStorage.fl:trail_visited
- Message shown once per session; not re-triggered on return
- Does NOT auto-redirect; user can continue navigating

---

### Flow FL-3: Core Analysis — Individual / Child Mode

**Entry point:** famililook.com/app

#### Step FL-3.1 — App Shell Load

**What the user sees:**
- Bottom tab bar: Home (active), About
- Home tab content: UploadSection
- ConsentBanner (top of screen if !consent.acknowledged)
- AnalyzeButton (FAB, hidden until canAnalyze = true)

**Expected behavior:**
- On load: read ?intent= URL param; if present, pre-select corresponding intent radio
- Read ?tab= URL param; if "settings", switch to About tab
- Read ?section=: if "keepsakes" or "results" and hasResults=true, auto-scroll

**Mobile requirements:**
- ConsentBanner must not overlap the primary action area
- FAB must not obstruct content; must be reachable with thumb (bottom-right or bottom-center)

---

#### Step FL-3.2 — Biometric Consent Banner

**What the user sees:**
- Banner at top of screen: "FamiliLook uses AI to analyse facial features..."
- Two buttons: "Accept" and "Decline"

**Available actions:**
1. Accept → set consent.biometric=true, consent.acknowledged=true, store in fl:consent
2. Decline → set consent.acknowledged=true but biometric=false; banner dismissed; analysis blocked

**Expected behavior:**
1. Accept: banner dismisses; user can proceed to upload and analyze
2. Decline: banner dismisses; AnalyzeButton shows "Biometric consent required" if tapped

**Expected error handling:**
- If localStorage write fails: keep banner visible; show "Unable to save preference" toast

**Mobile requirements:**
- Banner: full-width; buttons must be 44pt minimum height
- Must not prevent scrolling of content beneath

---

#### Step FL-3.3 — Intent Selection

**What the user sees:**
- Intent selector (radio buttons / cards):
  - "Who does my child take after?" (child mode)
  - "Do I look like Mum or Dad?" (self mode)
  - "Whole family" (group mode)
  - "Family Pets" (pet mode)
- Selected intent highlighted

**Available actions:**
- Tap any intent card to select it

**Expected behavior:**
- Selection updates userIntent in context
- Upload slots below update to match intent (e.g., self mode shows 1 parent slot; child mode shows 2 parent + 1 child)
- COPPA gate fires on first upload attempt if child analysis selected (not on intent selection itself)

**Expected error handling:** None at this step

---

#### Step FL-3.4 — Photo Upload

**What the user sees:**
- Photo slot grid matching selected intent:
  - Child mode: [Parent A] [Parent B] + [Add Child] button
  - Self mode: [Parent] + [Me] slot
  - Group mode: [Group Photo] upload zone
- Each empty slot: dashed border, camera icon, "Upload Photo" label
- Filled slot: thumbnail, quality indicator (pending / good / advisory / warning)
- Face quality badge: green (good), yellow (advisory), red (warning)

**Available actions:**
1. Tap empty slot → file picker opens (camera + gallery options on mobile)
2. Tap filled slot → replacement picker opens
3. Tap remove (×) on filled slot → remove photo
4. Drag file onto slot → upload (desktop)
5. Add Child button → additional child slot added

**Expected behavior:**
1. File selected: validate size (<10MB) and type (JPEG/PNG/HEIC) client-side; if valid, compress via compressPhoto(); upload to /detect (background, non-blocking); show "pending" quality badge
2. Detection result returns: update quality badge to good/advisory/warning; if warning show tooltip ("No face detected — try a clearer photo")
3. Multiple faces in one photo: FacePicker modal opens; user selects which face to use; selected face stored
4. Remove: slot returns to empty state; quality cleared
5. Add Child: new child slot added (if plan allows); child name input appears

**Expected error handling:**
- File >10MB: show inline error "Photo is too large — please use a file under 10MB"
- Unsupported format: "This file type isn't supported — please use JPEG, PNG, or HEIC"
- Detection API error: quality shows "Could not verify photo — you can still proceed"
- Max children reached for plan: "Upgrade to add more children"
- Max parents reached for plan: "Upgrade to add another parent"

**Mobile requirements:**
- Slots: minimum 80×80pt tap area
- File picker must offer camera as first option on iOS/Android
- Quality badges must be readable at slot thumbnail size
- "Add Child" button: minimum 44pt height

---

#### Step FL-3.5 — COPPA Age Gate

**What the user sees:**
- Modal overlay: "Are you over 13, or do you have parental consent to upload photos of a child?"
- Confirm button: "Yes, I confirm"
- Cancel button: "Cancel"

**Available actions:**
1. Confirm → proceed with upload
2. Cancel → return to upload without proceeding

**Expected behavior:**
1. Confirm: consent flag set; pending photo upload resumes
2. Cancel: modal closes; photo not added to slot

**Mobile requirements:** Modal must cover full screen; buttons minimum 44pt height

---

#### Step FL-3.6 — Analyze

**What the user sees:**
- AnalyzeButton FAB: appears when canAnalyze=true AND no modal open
- Button label: "🔬 Who Do I Look Like?" (self mode) or "🔬 Analyze Family" (other modes)
- Plan usage counter (if free plan): "2 of 3 free analyses used"

**Available actions:**
1. Tap FAB → trigger analysis
2. If free plan exhausted → upgrade wall shown instead

**Expected behavior:**
1. Tap when biometric consent not yet given: consent modal shown first; after acceptance, analysis proceeds automatically
2. Tap when consent given and canAnalyze=true:
   - Check hasRemainingAttempts()
   - If exhausted: show UpgradeWall overlay
   - If OK: incrementAttempts() then runAnalysis()
3. runAnalysis(): validate photos → compress → POST FormData to /kinship/analyze with 3 retries, 60s timeout, exponential backoff
4. During analysis: isAnalyzing=true → FAB shows "⏳ Analyzing..." → skeleton result cards shown

**Expected error handling:**
- No remaining attempts: UpgradeWall shown with plan options
- Analysis API error: error card shown with "Try Again" button; clearError() resets
- Network failure (all retries exhausted): "Couldn't reach our server — check your connection and try again"
- Timeout: "Analysis is taking longer than expected — try again"
- Invalid response: "Something went wrong with the analysis"

**Mobile requirements:**
- FAB must be visible when scrolled to upload area
- Loading skeleton must fill the same space as results to prevent layout shift
- FAB must hide when any modal is open

---

#### Step FL-3.7 — Results Display

**What the user sees:**
- MobileResultsSection renders after isAnalyzing=false AND hasResults=true
- Per-child card (scrollable carousel if multiple children):
  - Child photo (thumbnail)
  - Winner verdict: "Leans [Parent Name]" with confidence percentage
  - Parent split bar (visual percentage)
  - 8-feature table with parent attribution icons
  - Narrative sentence ("Your eyes are your mum's, but that smile is all dad!")
  - Quality tip if unknownFeatureCount ≥ 2 ("Upload clearer photos for more accurate results")
- Feature sensitivity slider (expandable panel)
- Action buttons: "Play FamiliUno", "Keepsakes", "Share Result"
- "Analyze Another Child" button

**Available actions:**
1. Swipe left/right to navigate between child cards
2. Tap "Play FamiliUno" → navigate to /uno?from=results
3. Tap "Keepsakes" → open KeepsakesModal
4. Tap "Share Result" → native share sheet or clipboard copy
5. Drag sensitivity slider → re-render with new voteMargin
6. Tap "Analyze Another Child" → reset child photos; keep parent photos

**Expected behavior:**
1. Carousel: snap to one card at a time; position indicator shown (dots)
2. FamiliUno: navigate with from=results so back returns to /app
3. Keepsakes: modal opens pre-populated with this child's data
4. Share: navigator.share() with title, text, URL; fallback to clipboard copy with "Link copied!" toast
5. Sensitivity slider: lower value = more decisive; higher = more conservative; re-renders feature table; does NOT re-call API
6. Analyze Another Child: only child photos cleared; parent photos retained; scroll to upload section

**Rule: NO 50/50 displays. Winner must always lean at least 51/49.**
**Rule: Feature count invariant — mumFeatureCount + dadFeatureCount + unknownFeatureCount === 8 always.**
**Rule: Backend winner field is authoritative — frontend NEVER re-derives it.**

**Expected error handling:**
- calibrated_features null: "Face not detected clearly — try uploading a clearer photo" (not "Unknown" for all features)
- embedding_similarity = 0 AND calibrated_features empty: "Analysis incomplete — please retry with clearer photos"
- Zero children in results: show "No results — please add a child photo and try again"

**Mobile requirements:**
- Cards: must fit within viewport width without horizontal scroll
- Action buttons: minimum 44pt height
- Sensitivity slider: 48pt track height minimum for thumb
- Narrative text: 16px minimum
- Child photo: minimum 60×60pt thumbnail

---

### Flow FL-4: Group / Family Mode

**Entry point:** /app with intent="group" selected

#### Step FL-4.1 — Group Photo Upload

**What the user sees:**
- Single upload zone: "Upload a group photo"
- Or: multiple individual photo slots (parents + multiple children)
- GroupSnapshotSection after upload

**Expected behavior:**
- Upload: same validation as FL-3.4
- GroupSnapshotSection: detects all faces in group photo; shows bounding boxes with confidence
- Face quality assessment per detected face

---

#### Step FL-4.2 — Face Name Assignment

**What the user sees:**
- Group photo with bounding boxes overlaid on detected faces
- Inline name editor for each detected face
- Role dropdown per face: Parent, Child, Sibling, Other
- Face quality badge per face (poor / fair / good / excellent)

**Available actions:**
1. Edit name inline for each face
2. Select role from dropdown
3. Dismiss any face (exclude from analysis)

**Expected behavior:**
1. Name edit: updates face label; used in results display
2. Role assignment: parent-tagged faces are tracked in parentNameSet; their pairs filtered from results by default
3. Dismiss: excluded face not included in pairwise analysis

**Mobile requirements:**
- Name input fields: minimum 44pt height; auto-scroll to keep active input above keyboard

---

#### Step FL-4.3 — Group Analysis

**What the user sees:**
- "Analyze Group" button
- After tap: progress indicator with pairwise count ("3 of 15 comparisons complete")

**Expected behavior:**
- Trigger N×(N-1)/2 pairwise comparisons
- Parent-parent pairs: filtered from default results; opt-in toggle available ("Show partner comparison?")
- Results: pairwise kinship matrix rendered
- If ≥6 players: progress bar shown with "X of 15 complete" so user knows system is working

**Expected error handling:**
- Partial timeout (some pairs complete, some timeout): show partial results with "Some comparisons could not complete — try with fewer people"
- No faces detected: "No faces detected — please upload a clearer group photo"

---

### Flow FL-5: Keepsakes Flow

#### Step FL-5.1 — Keepsakes Modal Entry

**What the user sees:**
- Modal opens over results, filling available height (not a small centered box)
- **Pillbox step navigator** fixed at top of modal: four pill-shaped tabs [Category] [Product] [Style] [Preview]
  - Current step: filled/highlighted pill
  - Completed steps: tappable pills with checkmark — tap to navigate back
  - Future steps: dimmed pills — not tappable until reached
- Content area fills remaining height below pillbox navigator
- For FREE plan users: visible note "Preview available — upgrade to Plus to order" shown at step 1
- No vertical scrolling within a step — each step's content fits the viewport

**Expected behavior:**
- Free plan users see the paywall notice at step 1 (NOT after 4 steps)
- keepsakePreviewOnly flag checked on modal open; paywall shown early
- Completing a step auto-advances to the next pillbox with a smooth transition
- Tapping a completed pillbox navigates back to that step instantly
- Back gesture (swipe right or browser back) navigates to previous step, not closing modal
- Modal uses full available height (`100dvh - safe-area`) on mobile — templates fill the space lengthwise
- Each step's content is self-contained within the viewport — no scroll needed except for long product lists in Step 2

---

#### Step FL-5.2 — Category Selection

**What the user sees:**
- Grid of product categories: Cards, Mugs, T-shirts, Prints, Apparel, Home
- Each category: icon + label

**Available actions:** Tap any category

**Expected behavior:** Navigate to step 2 (Product) showing products in selected category

---

#### Step FL-5.3 — Product & Style Selection

**What the user sees:**
- Products in selected category (e.g., "Character Mug", "Trading Card", "Certificate")
- Each product: preview thumbnail, name, price (in user's detected currency), stock status

**Available actions:**
1. Tap product → select it
2. Select style variant (e.g., "Pokemon Style", "Classic", "Certificate")

**Expected behavior:**
1. Product selected: advance to step 3 (Style)
2. Style selected: advance to step 4 (Preview)

---

#### Step FL-5.4 — Preview

**What the user sees:**
- Live template render with actual child data (name, photo, features, winner)
- "Download PNG" button
- "Share" button

**Mobile preview requirements (375px / 360px baseline):**

**Layout hierarchy on mobile Preview step (top to bottom, NO SCROLLING needed):**
1. Pillbox navigator (fixed, ~50px)
2. Design style selector (compact horizontal carousel, ~60px) — NO age style cards on this screen
3. Template preview (fills remaining height, centered)
4. Action bar (sticky bottom): Download PNG | Share | Add to Basket | Buy Now

**Age style selection MUST happen at Step 3 (Style), NOT Step 4 (Preview).** The Preview step shows ONLY the rendered result + actions. Age style cards (Infant/Child/Teen) must NOT appear on the Preview screen — they consume 360px+ of vertical space and push the actual preview and purchase CTAs below the fold.

**Template preview sizing:**
- ALL template previews MUST be readable on mobile without horizontal scroll
- Templates wider than 340px MUST use a mobile-optimised preview layout (not just CSS scale)
- Mug wraps (830px native): Show the centre panel (character + headline + child info) at full mobile width, cropped to the main content area. The full wrap is available via horizontal scroll or "See full wrap" toggle.
- Mug 3D mockup: MUST be centred in the container with the mug handle visible. Current rendering shows mug at far-right edge with mostly empty space — MUST centre the mockup image.
- Print templates (480px+): Scale to fit with minimum 10px rendered text
- Cards (290-320px): Render at native size (fits mobile)
- The full print-resolution template is preserved for PNG export — mobile preview is display-only

**Action bar requirements:**
- Action buttons (Download, Share, Add to Basket, Buy Now) MUST be in a sticky bottom bar, always visible
- MUST NOT overlap with privacy text or other content
- MUST NOT be pushed below the fold by age cards or other UI
- Touch targets: 44px minimum height
- Grouped in a single row with wrapping only if 4 buttons don't fit

**Standard mug mockup rendering:**
- The 3D mug mockup MUST be centred horizontally in the preview container
- The mug MUST be visible at a reasonable size (minimum 60% of container width)
- The dark background area MUST NOT dominate — if the mug is small, reduce the container height to fit
- The mockup container height should match the mug's visible height, not stretch to fill available space with empty dark background

**Character mug role intelligence:**
- Character illustrations on mugs MUST match the actual family role assigned during upload
- All 17 upload roles (Mum, Dad, Grandma, Grandad, Brother, Sister, Son, Daughter, Aunt, Uncle, Cousin, Niece, Nephew, Friend, Partner, Colleague, In-Law) MUST map to appropriate character types
- Role → Character mapping: Grandma→gran, Grandad→gramps, Son/Brother/Nephew/Cousin→cub, Daughter/Sister/Niece→mini, Aunt→mama, Uncle→papa
- Multilingual aliases MUST be recognised (e.g., "Oma", "Nonna", "Abuela" → gran)
- For Plus+ users: "Add to Basket" and "Buy Now" buttons
- For Free users: "Upgrade to Plus to Order" link

**Available actions (Plus+):**
1. Download PNG
2. Share
3. Add to Basket → BasketContext.addItem(); toast "Added to basket!"; basket badge updates
4. Buy Now → OrderModal opens (single-item checkout)
5. Go back to change style

**Available actions (Free):**
1. Download PNG (allowed)
2. Share (allowed)
3. "Upgrade to Plus to Order" → navigate to /plans

**Expected behavior:**
- Template renders with live data; all fields populated
- Download: exports PNG at print resolution
- Add to Basket: item added; BasketDrawer becomes accessible; toast confirms

**Expected error handling:**
- Template render failure (null data): "Template preview unavailable — please try again"
- Download failure: "Could not export image — please try again"

---

### Flow FL-6: Basket & Checkout

#### Step FL-6.1 — Basket Drawer

**What the user sees:**
- BasketDrawer slides in from right/bottom
- List of items: product name, style, quantity selector, price, remove button
- Shipping form: name, address, postcode, country
- Total price (with currency)
- "Checkout" button

**Available actions:**
1. Adjust quantity (1–10 per item)
2. Remove item
3. Fill shipping fields
4. Tap Checkout

**Expected behavior:**
1. Quantity change: price updates; badge updates
2. Remove: item gone; if last item, drawer shows "Your basket is empty" + "Browse Products" CTA
3. Shipping: real-time validation on field blur
4. Checkout: validateShippingFields(); if valid → createBasketCheckout() → Stripe redirect URL returned → window.location.href = url

**Expected error handling:**
- Shipping validation: per-field inline errors (e.g., "Postcode is required")
- Checkout API error: "Checkout unavailable — please try again" toast
- Network error: same toast; basket retained

---

#### Step FL-6.2 — Stripe Checkout (External)

User is on Stripe-hosted checkout page. This is outside FML control.

**Expected behavior:**
- On payment success: Stripe redirects to /order-success?order_id=xxx
- On payment cancel: Stripe redirects to /app or /uno (configured in createBasketCheckout)

---

#### Step FL-6.3 — Order Success

**What the user sees:**
- Dark-themed confirmation page (background must match brand dark theme: #0D0F1A)
- Order confirmation: order ID, product list, estimated delivery
- "Return to FamiliLook" button → /app
- Basket cleared automatically

**Expected behavior:**
- On load: read ?order_id= or ?basket_id= from URL
- Fetch order status from backend
- Clear fl:pending-checkout and fl:basket from localStorage
- Track trackOrderCompleted event
- "Return to FamiliLook" → navigate to /app (not /hub)

**Expected error handling:**
- No order_id in URL: "Order not found — please check your email for confirmation"
- Order status fetch failure: "Could not retrieve your order details — please check your email"

**Mobile requirements:**
- Page background must be dark (#0D0F1A); no transparent/white fallback
- Return button: full-width, 44pt height

---

### Flow FL-7: Plan Upgrade

#### Step FL-7.1 — Upgrade Wall

**What the user sees:**
- Inline modal: "You've used all your free analyses"
- Plan comparison: Free / Plus / Pro feature lists
- "See Plans" → /plans button

**Expected behavior:**
- Modal only shows when hasRemainingAttempts() returns false
- "See Plans" preserves current photos in state (analysis not reset)

---

#### Step FL-7.2 — Plans Page

**What the user sees:**
- Three tiers: Free, Plus, Pro
- Monthly/Annual toggle (annual shows % saving)
- Feature comparison grid
- Email input + "Upgrade" button per paid tier
- Ambassador code input at bottom

**Available actions:**
1. Toggle monthly/annual
2. Enter email + select plan → checkout
3. Enter ambassador code → redeem

**Expected behavior:**
1. Toggle: prices update; annual shows discounted price
2. Plan select: validate email; if priceId set → createSubscriptionCheckout({ priceId, email }) → Stripe redirect; if priceId empty (env var missing) → show "This plan is not available right now — please contact support" with support email/link
3. Ambassador code: redeemAmbassadorCode({ code, email, name }) → if ok, store ambassador state; show confirmation

**On return from Stripe (session_id in URL):**
- Read fl:plan-email from localStorage
- If email found: getSubscriptionStatus(email) → setCurrentPlan(plan) → redirect to /app
- If email NOT found (localStorage cleared): show "Payment received — please enter your email to activate your plan" + email re-entry form

**Expected error handling:**
- Invalid email: inline "Please enter a valid email"
- Stripe unavailable: "Payment service temporarily unavailable — please try again"
- Plan not found (empty priceId): actionable error with support link (not just "not available")
- Ambassador code invalid: "This code is not valid or has expired"

---

### Flow FL-8: Settings / About Tab

#### Step FL-8.1 — About Tab

**What the user sees:**
- App version (should match package.json)
- Privacy section with consent management
- "Revoke biometric consent" button
- "Coming Soon" section (must NOT list features that are already live)
- "What's Included" feature list (must reflect current plan)
- Feedback button (shown if persistentAnalysisCount ≥ 2)
- "Clear All Photos & Data" button
- Legal links: Privacy, Terms

**Available actions:**
1. Revoke consent → clear consent.biometric; analysis blocked until re-consent
2. Feedback → feedback modal
3. Clear All Data → confirmation prompt → resetAll() + reload
4. Legal links → /privacy, /terms

**Expected behavior:**
1. Revoke: ConsentBanner re-shown on next app visit
2. Feedback: modal after 2+ analyses; sets fl:feedback-given after submit
3. Clear: confirmation dialog "Are you sure? This will remove all photos and results." → OK proceeds; Cancel does nothing
4. Legal: in-app navigation (not external)

**Note: "Coming Soon" section must be accurate — must NOT list pet analysis (already live), card games (already live), or any other live feature.**

---

### Flow FL-9: Demo Mode

#### Step FL-9.1 — Demo Activation

**Entry:** /app?demo=famili2026

**What the user sees:**
- "Conference Demo" badge in header
- All plan restrictions lifted
- All features accessible

**Expected behavior:**
- isDemoMode(): check localStorage for demo token; if not present or expired, check URL param
- If URL param matches: write demo token with 4h TTL to localStorage; activate all features
- After 4h: demo expires; restrictions restored; no visible badge

**Expected error handling:** Demo token expiry must not crash the app; graceful downgrade to free plan

---

## PRODUCT 2: FamiliUno

**URL:** famililook.com/uno
**Repo:** famililook-desktop2 (same codebase as FamiliLook)
**Purpose:** Physical and digital card game based on family kinship analysis results

---

### Flow FU-1: Entry — No Existing Analysis

**Entry point:** /uno (from trail, direct, or any source without ?from= carrying results)

#### Step FU-1.1 — FamiliUno Landing (No Cards)

**What the user sees:**
- FamiliUno hero section with logo and tagline
- "How It Works" steps: Upload → Analyze → Play & Order
- UploadSection (embedded, same as /app)
- Feature count selector: 2, 3, or 4 features per card
- Deep-link game prompt if ?game= param present: "Try [Game] — Try Demo | Use My Photos"

**Available actions:**
1. Use embedded UploadSection (same as FL-3.3–FL-3.4)
2. Select feature count: 2, 3, or 4
3. If ?game=memorymatch: "Try Demo" or "Use My Photos"
4. Analyze Family button

**Expected behavior:**
1. Upload: follows FL-3.4 behavior
2. Feature count: stored in fl:unoFeatureCount; persists across sessions
3. "Try Demo": inject demoResults into localStorage; reload page; card deck should appear
4. Analyze: calls runAnalysis() → on success, buildDeck() returns cards → hasCards=true → Phase 2 shown

**Expected error handling:**
- Analysis failure: same as FL-3.6 error handling
- Demo injection failure (checkHasCards() still false after demo data set): "Demo unavailable — please upload your own photos"
- Group mode analysis: buildDeck() must correctly read fl:groupSnapshot OR fl:analysisResults for group results; if neither produces cards, show "Please run an analysis first"

**Mobile requirements:**
- Feature count selector: buttons minimum 44pt; clear selected state
- "How It Works" steps: readable without scrolling on 375px screen

---

### Flow FU-2: Entry — With Existing Analysis

**Entry point:** /uno?from=results (navigating from /app after successful analysis)

#### Step FU-2.1 — FamiliUno Landing (Cards Available)

**What the user sees:**
- Card gallery header with family photo thumbnails
- Feature count selector (pre-set to saved preference)
- 5 game mode tiles: FaceMatch, MemoryMatch, FaceFusion (free); HungryHeads, FeatureCatch (Plus)
- "Love your deck? Order it" button
- Back navigation button (header)

**Available actions:**
1. Change feature count (2/3/4) → deck rebuilds immediately
2. Tap game tile → launch game
3. Plus-gated games: tap → UpgradeOverlay shown for Free users
4. "Order Deck" → checkout flow
5. Back button → reads ?from= param: trail→/trail, results→/app, home→/, else→/hub

**Expected behavior:**
1. Feature count change: fl:unoFeatureCount updated; buildDeck() re-runs; card gallery refreshes
2. Game launch: CardGame component renders with selected game
3. UpgradeOverlay: shows plan comparison; "Upgrade" → /plans
4. "Order Deck": check canOrderMerchandise(); if free→/plans; if Plus+→build manifest→basket.addItem()→dispatch "open-basket-drawer" event
5. Back: navigate based on ?from= param; if no param → /hub

**CRITICAL: The "open-basket-drawer" event can only be received by AppLayout's listener. FamiliUnoPage is NOT rendered inside AppLayout. The BasketDrawer must be rendered within FamiliUnoPage itself (or an alternative basket access mechanism must exist) for basket operations from /uno to work.**

**Expected error handling:**
- buildDeck() returns no cards: show "No cards available — please re-analyze your family" + "Analyze" CTA
- Order API error: "Could not start checkout — please try again"

---

### Flow FU-3: Games

#### Step FU-3.1 — Game Selection

**What the user sees:**
- 5 game tiles: FaceMatch, MemoryMatch, FaceFusion, HungryHeads (Plus), FeatureCatch (Plus)
- Free games: immediately accessible
- Plus games: lock icon badge; UpgradeOverlay on tap for Free users

**Expected behavior:**
- Game tile tap: renders selected game component below tile grid
- Game component mounts with data from localStorage (fl:analysisResults, fl:lastResults, fl:familyContext)

---

#### Step FU-3.2 — Individual Game Play

**What the user sees (varies by game):**
- FaceMatch: match face cards to names
- MemoryMatch: flip face cards to find pairs
- FaceFusion: swipe to blend parent features
- HungryHeads (Plus): face trivia challenge
- FeatureCatch (Plus): catch inherited features falling from top

**Universal game requirements:**
- Loading: if data preparation >300ms, show skeleton / loading animation
- Back button: must return to game selector (not restart same game)
- Win/Loss: CelebrationModal shown; "Play Again" or "Back to Games"
- Share: ShareResultModal allows sharing game outcome

**Expected error handling:**
- localStorage data corrupt/missing: "Game data unavailable — please run an analysis first" + "Analyze" CTA

---

### Flow FU-4: Physical Deck Order

#### Step FU-4.1 — Order Deck

**What the user sees (Plus+ users only):**
- "Love your deck? Order it as a physical card deck" section
- Price per deck, quantity selector (1–10)
- "Order" button

**Available actions:**
1. Adjust quantity
2. Tap Order

**Expected behavior:**
1. Quantity: price × quantity shown
2. Order: buildDeck() → validate manifest → basket.addItem({product_type:'deck', manifest, quantity}) → basket indicator shows → navigate to basket for checkout

**REQUIRED: Basket must be accessible from /uno. Current architecture requires BasketDrawer to be rendered within FamiliUnoPage, not just in AppLayout.**

---

### Flow FU-5: Back Navigation

**Rule:** Back button on /uno reads ?from= and navigates:
- ?from=results → /app
- ?from=trail → /trail
- ?from=home → /
- No param → /hub

This must be consistent with how /app handles ?from= (which currently has a bug for from=home → /hub instead of /).

---

## PRODUCT 3: FamiliPoker

**URL:** famililook-desktop4.vercel.app
**Repo:** famililook-desktop4
**Backend:** famililook-desktop3 (/kinship/analyze)
**Purpose:** Casino-style card games (Poker, Blackjack) powered by family facial feature analysis

---

### Flow FP-1: Age Gate

**Entry point:** Any URL on the domain

#### Step FP-1.1 — Age Confirmation

**What the user sees:**
- Full-screen AgeGateModal blocking all content
- "Are you 18 or older?" prompt
- "Yes, I'm 18+" button
- "No, take me back" button

**Available actions:**
1. Yes → set fl:age-confirmed-poker = 'true' in localStorage; render app
2. No → navigate to brand hub (BRAND_HUB_URL)

**Expected behavior:**
- Modal shown on EVERY visit until fl:age-confirmed-poker = 'true'
- If localStorage cleared: age gate re-appears
- App content completely blocked until confirmed

**Mobile requirements:**
- Full-screen overlay; no content visible behind it
- Both buttons: minimum 44pt height

---

### Flow FP-2: Upload & Analysis

**Entry point:** /app → Home tab (default loads on Games tab)

#### Step FP-2.1 — Initial App State

**What the user sees:**
- Games tab shown by default (default tab = "cards")
- If no analysis data: banner "Games unlock after analysis — go to Home tab to get started"
- Bottom nav: Home, Games, About

**Expected behavior:**
- Default tab = "cards" (via URL ?tab= or hardcoded default)
- If no analysis data AND on Games tab: banner shown with "Go to Home" CTA
- FeaturePoker renders immediately (selectedGame defaults to "poker") — this is incorrect; see FMEA

---

#### Step FP-2.2 — Photo Upload (Home Tab)

**What the user sees:**
- UploadSection with ModeSelector: Individual vs Group Photo
- Individual: Parent A + Parent B + Child slots
- Group Photo: single drop zone

**Expected behavior:**
- Same as FL-3.4 photo upload behavior
- PhotoPickerSheet: camera + gallery options on mobile

**Expected error handling:**
- Same as FL-3.4

---

#### Step FP-2.3 — Analysis

**What the user sees:**
- AnalyzeButton FAB
- On tap: AnalysisLoadingModal (full-screen overlay) with progress

**Expected behavior:**
- runAnalysis() → POST to /kinship/analyze
- On success: analysisResults stored; auto-navigate to Games tab
- On FAILURE: error state must be displayed. Currently error is silently swallowed. **Required behavior:** error card with retry option.

**Expected error handling:**
- ALL errors from useKinshipAnalysis must surface to the user with:
  - What went wrong (network, server, invalid photo, etc.)
  - A "Try Again" button
  - A "Get Help" link (email/support)

---

### Flow FP-3: Games Lobby

#### Step FP-3.1 — Game Selection

**What the user sees:**
- GameRooms lobby with game tiles: Poker, Blackjack (only 2 tiles)
- Game tiles: name, icon, short description
- Selected game renders below lobby

**Expected behavior:**
- Tap Poker: FeaturePoker component renders below lobby
- Tap Blackjack: Feature21 component renders below lobby
- No other games exist in gameRoomsConfig.js (memory, facematch, deck, feedfam, facefusion are NOT registered)

**Note: selectedGame initializes to "poker" on load — FeaturePoker auto-launches without user interaction. Expected behavior: no game auto-selected; user must actively choose.**

**Mobile requirements:**
- Game tiles: minimum 44pt height
- Lobby + game component must scroll together; no nested scroll

---

### Flow FP-4: Feature Poker (Texas Hold'em)

#### Step FP-4.1 — Age Selector & Tutorial

**What the user sees:**
- AgeSelector: Teens / Adults (card-style buttons)
- After selection: HowToPlay tutorial (5 animated slides)
- "Deal me in!" button

**Available actions:**
1. Select age group
2. Navigate tutorial slides
3. "Deal me in!" → start game

**Expected behavior:**
1. Age selection: sets content filter for feature labels (family-friendly vs adult themes)
2. Tutorial: 5 swipeable slides; skip option
3. "Deal me in!": dispatch SELECT_AGE → stage → ANTE

---

#### Step FP-4.2 — Poker Gameplay

**What the user sees:**
Stage machine: ANTE → DEAL → FLOP → TURN → RIVER → SHOWDOWN → RESULT

**ANTE/DEAL:** Automated with brief delay; cards dealt
**FLOP (Player's Turn):**
- Player's hole cards (2 face-up)
- Community cards (3 face-up)
- AI opponent's cards (face-down)
- Betting controls: Check | Bet [10] [25] [50] | Fold
- Chip count display
- Pot size display

**TURN:** Player acts again after 4th community card
**RIVER:** Player acts again after 5th community card
**SHOWDOWN:** All cards revealed; hand evaluations shown
**RESULT:**
- Winner announcement
- ResultOverlay: "Next Round" or "Quit"
- Back button

**Expected behavior (Back button):**
- Back must navigate to game lobby (selectedGame = null)
- NEVER restart the same game from SETUP
- Current bug: Back sets selectedGame = "poker" (restart) — must be fixed to setSelectedGame(null)

**Expected error handling:**
- localStorage data missing (no analysis): game should show placeholder features; banner "Analyze your family for personalized cards" must remain visible

**Mobile requirements:**
- Betting controls: each button minimum 44pt height
- Card display: readable at 375px width; no truncated text
- Chip count: always visible (sticky position or top of game area)

---

#### Step FP-4.3 — Poker Result

**What the user sees:**
- ResultOverlay: winner announcement, hand comparison
- "Next Round" button → NEW_ROUND dispatch; return to ANTE
- "Quit" → RESET dispatch → return to SETUP (age selector)

**Expected behavior:**
- "Next Round": same players, new hand; chip counts carry over
- "Quit": game resets fully; user must re-select age and go through tutorial

**Note: "Quit" should ideally return to game lobby, not require re-tutorial. Expected: "Quit" = return to lobby; "Reset" = re-do tutorial. This distinction should be made clear in UI.**

---

### Flow FP-5: Feature 21 (Blackjack)

#### Step FP-5.1 — Age Selector & Tutorial

Same pattern as FP-4.1.

---

#### Step FP-5.2 — Blackjack Gameplay

Stage machine: SETUP → BET → DEAL → PLAYER_TURN → DEALER_TURN → SETTLE → RESULT

**BET:**
- Chip selector: [10] [25] [50] [100] chip options
- "Deal!" button
- Chip count display
- Back button

**DEAL:** Cards dealt automatically; natural 21 → skip to DEALER_TURN
**PLAYER_TURN:**
- Player's hand (face-up)
- Dealer's hand (1 face-up, 1 face-down)
- Actions: Hit | Stand | Double (if first action and sufficient chips)
- Bust: automatic SETTLE

**DEALER_TURN:** Dealer auto-plays to 17+; animated card deals
**SETTLE → RESULT:**
- Win/Lose/Push outcome
- "Next Hand" or "Quit"

**Expected behavior (Back from BET stage):**
- Back: navigate to lobby (setSelectedGame(null))
- Confirmation dialog: "You'll lose your current bet — are you sure?"
- On confirm: navigate to lobby
- On cancel: return to BET

**Expected error handling:**
- Chip count reaches 0: "Game over — you're out of chips!" + "Start Over" (reset chips) + "Quit" (return to lobby)

**Mobile requirements:** Same as FP-4.2

---

### Flow FP-6: Plans Page

**URL:** /plans

**What the user sees:**
- Three plan tiers: Free ($0), Family ($29.99), Pro ($49.99)
- Feature comparison per tier
- "Select [Plan]" button per tier

**Expected behavior:**
- Plan selection must actually upgrade the plan
- Current bug: navigate(`/app?plan=${planKey}`) does nothing — context never reads ?plan=
- **Required:** implement plan upgrade flow (payment or ambassador code); currentPlan must update in context and persist

**Expected error handling:**
- Payment failure: "Payment could not be processed — please try again"
- Plan not available: actionable error with contact information

---

## PRODUCT 4: FamiliMatch

**URL:** famililook-desktop6.vercel.app
**Repo:** famililook-desktop6
**Backend:** famililook-desktop7 (WebSocket, Duo/Group) + famililook-desktop3 (/compare/faces, /face/morph)
**Purpose:** Face compatibility comparison — how well do two (or more) faces match?
**Audience:** Categorically different from FamiliLook — compatibility/matching (not kinship/parentage). NEVER consolidate into FamiliLook.

**IMPORTANT NOTE: The FamiliMatch source codebase is currently unrebuildable — 15+ source files are missing including index.html, vite.config.js, App.jsx, main.jsx, both context files, and 7 components. All flows below describe EXPECTED behavior derived from source analysis of existing files and compiled dist artifacts. The codebase must be restored before any changes can be made.**

---

### Flow FM-1: Landing / Mode Selection

**Entry point:** famililook-desktop6.vercel.app/

#### Step FM-1.1 — Landing Page Load

**What the user sees:**
- Brand hero with FamiliMatch logo and tagline
- Mode selection cards:
  - Solo: "Compare two faces" (always available)
  - Duo: "Compare face-to-face" [Plus badge if locked]
  - Group: "Group chemistry" [Plus badge if locked]
- Social proof counter (starts at 12,847, increments randomly — must be replaced with real data)
- Recent comparisons history (from localStorage, if any)
- Product identification: FamiliMatch (NOT FamiliLook)

**Available actions:**
1. Tap Solo card → consent check → navigate to /solo
2. Tap Duo card:
   - Free tier: UpgradeModal → link to FamiliLook hub settings?upgrade=plus
   - Plus tier: consent check → navigate to /room with mode=duo
3. Tap Group card: same as Duo
4. Tap history entry → view past result (if ResultsPage accessible)

**Expected behavior:**
- Tier determination: MUST come from a cryptographically signed session token from FamiliLook — NOT from a URL query parameter. Current ?tier= URL param approach is trivially bypassable.
- Mode unlock: Duo and Group require Plus or Pro tier
- Consent check: if !consent.bipaConsented → show ConsentModal; on accept → navigate to mode
- If ?mode= URL param present AND mode is unlocked: still require consent check before navigating

**Expected error handling:**
- Upgrade link failure: fallback to famililook.com/plans
- Consent rejection: return to landing with Solo as only visible option

**Mobile requirements:**
- Mode cards: minimum 80pt height; clearly differentiated Free vs Locked states
- Counter: must not distract from primary CTAs

---

#### Step FM-1.2 — Biometric Consent Modal (FamiliMatch)

**What the user sees:**
- Modal: FamiliMatch-specific BIPA/GDPR consent text
- "I Agree" button
- "No Thanks" button (returns to landing)

**Expected behavior:**
- Accept: consent.bipaConsented = true; stored in localStorage; modal dismissed; navigation proceeds
- Decline: modal dismissed; user stays on landing

---

### Flow FM-2: Solo Mode

**Entry point:** /solo

#### Step FM-2.1 — Onboarding (First Visit)

**What the user sees:**
- OnboardingScreen overlay: "What's your name?" input
- "Continue" button

**Expected behavior:**
- Name capture: stored in context as userName
- After name entry: overlay dismissed; upload phase shown

**Mobile requirements:**
- Name input: auto-focus on mount; keyboard appears immediately
- "Continue": minimum 44pt height; only enabled when name is non-empty

---

#### Step FM-2.2 — Photo Upload (Solo)

**What the user sees:**
- Two upload zones side by side (or stacked on narrow mobile):
  - Left/Top: "You" (userName from onboarding)
  - Right/Bottom: "Compare with..." (Person B)
- Each zone: dashed border, camera icon, "Tap to upload" label
- After upload: thumbnail shown; "Change" option

**Available actions:**
1. Tap upload zone → file picker (camera + gallery)
2. Tap thumbnail → replacement picker
3. "Compare Faces" button (enabled when both photos uploaded)

**Expected behavior:**
1. Photo selected: validate type and size; compress to 1024px JPEG; store as blob
2. Both uploaded: "Compare Faces" button enabled
3. "Compare Faces" tap: if !consent.bipaConsented → consent check; else → runComparison()

**Expected error handling:**
- File invalid: inline "This file type isn't supported"
- File too large: "Please use a photo under 10MB"

---

#### Step FM-2.3 — Analysis Loading

**What the user sees:**
- FeatureScanAnimation overlay (full screen or over upload area)
- Steps: "Detecting faces..." → "Extracting features..." → "Comparing..." → "Building result..."
- Progress bar
- Both names shown: [userName] vs [Person B name — NOT hardcoded "B"]

**Expected behavior:**
- compareSolo(photoA, photoB, progressCallback, nameA, nameB):
  - POST to /compare/faces with both photos and names
  - POST to /face/morph (non-blocking; failure silently ignored)
  - Minimum 8-second experience (setTimeout enforces this even if API responds faster)
  - progressCallback drives animation
- Names must be passed to both the API and displayed in the animation

**Expected error handling:**
- /compare/faces failure: "Comparison failed — please try again" with retry button
- Network error: "Check your connection and try again"

---

#### Step FM-2.4 — Results Story

**What the user sees:**
5-slide story (swipeable):
1. Percentage reveal: large number animating up to final % (e.g., "73%"); chemistry_label ("Magnetic Match"); chemistry_color as background accent
2. Strongest match: feature with match=true and highest similarity
3. Biggest contrast: feature with match=false
4. Feature breakdown: all 8 feature_comparisons as comparison table
5. Face fusion: morphed image (if morph succeeded); chemistry summary

**On each slide:**
- Swipe left/right or tap arrows to navigate
- Slide position indicator (dots)

**Available actions (slide 5):**
- "Share Result" → ShareCard
- "Try Again" → reset to upload phase
- "Go Back" → /

**Expected behavior:**
- All data from /compare/faces API response; NO frontend re-derivation of percentage, chemistry_label, or chemistry_color
- feature_comparisons: exactly 8 items always
- percentage: already rounded integer from backend
- If morph image unavailable: fusion slide shows "Face fusion unavailable — try with clearer photos"
- Results NOT persisted to localStorage on hard refresh; user sees "No results yet — start a comparison"

**API Contract compliance (NON-NEGOTIABLE):**
- Uses /compare/faces ONLY — never /kinship/analyze
- percentage = round(clamp(0.6 * embedding_sim + 0.4 * feature_sim, 0, 1) * 100) — backend authoritative
- shared_features exactly matches feature_comparisons where match=true
- Symmetry: swapping face_a/face_b produces identical percentage

**Mobile requirements:**
- Percentage: minimum 64px font size for impact
- Swipe gesture: 80%+ accuracy; no accidental horizontal scroll triggering
- Feature breakdown table: readable at 375px; no horizontal scroll on table itself

---

#### Step FM-2.5 — Share Card

**What the user sees:**
- Styled result card with: percentage, chemistry_label, both names, FamiliMatch branding
- "Share" button → Web Share API
- "Download" button → save as PNG

**Expected behavior:**
- html2canvas captures the card
- Web Share API: share with title, text, file (PNG)
- If Web Share not available: download PNG as fallback
- Share URL must use environment variable, not hardcoded production URL

**Expected error handling:**
- html2canvas failure: "Could not generate share image — download unavailable"
- Share cancelled: silent (user-initiated cancel)

---

### Flow FM-3: Duo / Group Room Mode (Plus+)

#### Step FM-3.1 — Room Lobby

**Entry point:** /room (after consent check on landing)

**What the user sees:**
- Room mode selection: Host or Join
- Host: "Create Room" button → room code displayed
- Guest: "Enter Room Code" input + "Join" button
- Player list: as players join, names/avatars appear
- "Ready to Start" (host only, when minimum players in room)

**Expected behavior:**
- WebSocket connects to wss://api.famililook.com/ws/match
- Host creates room: room code shown (e.g., "ABC123"); share link available
- Guest joins: enter 6-char code; on success, appears in host's player list
- Host starts: websocket broadcast triggers all clients to move to upload phase
- Phase: lobby → upload

**Expected error handling:**
- WebSocket connection failure: "Could not connect to the room — check your connection"
- Invalid room code: "Room not found — check the code and try again"
- Room full: "This room is full — please create a new one"

---

#### Step FM-3.2 — Upload Phase (Room)

**What the user sees:**
- Single PhotoUpload component
- "Upload your photo" instruction
- Upload zone (same as Solo upload, single photo)
- "I'm Ready" button (enabled after upload)

**Expected behavior:**
- Photo uploaded via WebSocket as base64 (connection.uploadPhoto(dataUrl))
- "I'm Ready": connection.markReady(); shows "Waiting for other players" state
- Phase: upload → waiting → analyzing (when all players ready)
- Auto-reconnect: if WebSocket drops during upload, reconnect and check if photo was received; if not, re-prompt upload

**Expected error handling:**
- Upload failure (WebSocket error): "Photo upload failed — please try again"
- Connection dropped during upload: auto-reconnect; if photo not confirmed received → re-prompt upload
- Timeout waiting for other players: "Waiting for [X] more players..." with player indicators

---

#### Step FM-3.3 — Analysis Phase (Room)

**What the user sees:**
- AnalysisProgress component: animated dots + progress bar
- Step labels: "Detecting faces" → "Extracting features" → "Comparing..." → "Building results..."

**Expected behavior:**
- Backend processes N×(N-1)/2 pairwise comparisons
- Progress messages updated via WebSocket
- Phase: analyzing → countdown → done

**Expected error handling:**
- Analysis timeout: "Analysis is taking longer than expected — please wait"
- Partial results: show available results; note "Some comparisons could not complete"

---

#### Step FM-3.4 — Countdown

**What the user sees:**
- CountdownOverlay: animated countdown (3... 2... 1... 🎉)
- Blocks all interaction

**Expected behavior:**
- On countdown complete: phase = transitioning (NOT done/blank)
- Navigation to /results happens when connection.results arrives (may be after countdown completes)
- During transition: "Loading results..." spinner — NOT blank card

---

#### Step FM-3.5 — Results (Duo/Group)

**Entry point:** /results (loaded after WebSocket 'reveal' message)

**Duo results:**
- Same 5-slide story as Solo (FM-2.4)
- But showing Player A vs Player B comparison

**Group results:**
- Chemistry matrix: grid of all pairwise chemistry scores
- Each cell: percentage + chemistry_label
- Click cell → expand to see feature breakdown for that pair
- Most compatible pair highlighted

**Expected behavior:**
- Results NOT persisted: hard refresh → "No results yet" with "Start a new comparison"
- Share: ShareCard for duo; screenshot/share for group matrix

**Expected error handling:**
- Results context lost (hard refresh): "No results yet — start a new comparison" + CTA
- Missing pair in matrix: cell shows "—" (comparison unavailable)

---

## UXD Gap Analysis — Missing Flows

The following flows are ABSENT from current implementations and represent gaps:

| Gap | Product | Missing Flow |
|---|---|---|
| UXD-GAP-01 | FamiliMatch | No error display in analysis (Solo mode) — results screen shows nothing on failure |
| UXD-GAP-02 | FamiliPoker | No error display for analysis failures — user sees loading overlay disappear with no explanation |
| UXD-GAP-03 | FamiliPoker | No plan upgrade flow — /plans is decorative |
| UXD-GAP-04 | FamiliUno | No basket access from /uno — event fires into void |
| UXD-GAP-05 | FamiliLook | No early paywall gate for free keepsake users — shown only at final step |
| UXD-GAP-06 | FamiliMatch | No session persistence for results — hard refresh loses all data |
| UXD-GAP-07 | FamiliMatch | Tier gating has no cryptographic validation |
| UXD-GAP-08 | FamiliPoker | No lobby on load — game auto-launches |
| UXD-GAP-09 | FamiliLook | from=home in /app navigates to /hub instead of / |
| UXD-GAP-10 | FamiliLook | Demo mode stale cache — may not activate or expire correctly |
| UXD-GAP-11 | FamiliLook/Uno | Group mode analysis may not produce cards in FamiliUno |
| UXD-GAP-12 | FamiliMatch | Room 'done' phase renders blank card before results navigate |
| UXD-GAP-13 | FamiliLook | OrderSuccessPage dark theme broken (colors.bgPrimary undefined) |
| UXD-GAP-14 | FamiliLook | Pet analysis listed as "Coming Soon" but is live |
| UXD-GAP-15 | FamiliPoker | FeaturePoker Back button loops to SETUP (cannot exit game) |

---

*End of User Experience Definitions v1.0 — 2026-03-31*
