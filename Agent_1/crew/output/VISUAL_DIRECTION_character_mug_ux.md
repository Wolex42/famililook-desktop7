# VISUAL DIRECTION -- Character Mug UX Clarity

```
===============================================
  VISUAL DIRECTION -- Character Mug UX Clarity
  Visual Director -- 2026-04-07 (v2 -- revised)
===============================================

PRODUCT: FamiliLook -- Character Mug (mobile flow)
SCREENS AFFECTED: KeepsakeCustomise (character_mug), KeepsakePreview (character_mug)
MOBILE TARGET: 375px viewport minimum, component type: PRODUCT MOCKUP (UI elements, not print)

CRITICAL DISTINCTION:
  This spec is for: MOBILE UI ELEMENTS.
  These are NOT print templates. They are contextual UI components
  that appear in the KeepsakeCustomise and KeepsakePreview screens
  to explain the product intelligence to the user.

  The print template (MugWrapTemplate / CharacterMugTemplate) is
  UNAFFECTED by this spec. That pipeline uses inline styles and
  exports at 830px for Prodigi. Do not conflate the two.

CEO PAIN POINTS ADDRESSED:
  1. "Not clear how characters render on mugs" -- no product explanation
  2. "How it would merge with results" -- no bridge from analysis to character
  3. Preview CTA buried -- too much scroll before the user can act

KEY DATA FLOW CONTEXT:
  The character mug has TWO selection modes:
  - AUTO-SELECTION: engine reads winnerRole -> character type,
    winnerPct -> emotion bracket, winnerEthnicity -> variant.
    Occasion and recipient can override further.
  - USER OVERRIDE: CharacterPicker lets user pick manually.
    Their choice overrides the illustration ONLY.
  In BOTH cases, the mug headline (e.g., "MUMMY'S MINI ME"),
  score line (e.g., "65% Mum"), and dominant feature text
  ALWAYS come from analysis results.

  The user currently sees NONE of this intelligence. These specs
  make it visible.


-------------------------------------------------------
SPEC 1 -- PRODUCT EXPLANATION MOMENT
-------------------------------------------------------

ASSESSMENT OF OPTIONS:

  Option A (Dismissable inline card at top of KeepsakeCustomise):
    + Visible immediately on entry -- proactive, not hidden
    + Does not interrupt flow (no extra modal/screen to dismiss)
    + Can be dismissed; won't nag users who already understand
    + Natural reading position: user reads explanation, then sees preview
    - Takes vertical space above the already-tall preview zone

  Option B (Intro modal before CharacterPicker):
    + Dedicated attention -- user must read before proceeding
    - Adds friction to an already 3-screen flow
    - Character mug has the most customisation of any product;
      another step is unwelcome
    - Modals on mobile feel like roadblocks, not education

  Option C (Tooltip/info icon in catalogue):
    + Zero friction for users who don't need it
    - Easy to miss entirely -- CEO said it was "not clear",
      meaning explanation must be proactive
    - Mobile tooltips are awkward (no hover; requires tap to open)
    - Catalogue shows all products; tooltip can't convey
      the personalised nature specific to character_mug

  >>> RECOMMENDATION: Option A -- Dismissable inline card

  RATIONALE: The explanation must be proactive (users are confused
  NOW) but must not add a full extra screen. An inline card at
  the top of the Customise screen is seen immediately, sits above
  the mug preview, and can be dismissed once understood. It
  specifically reveals the INTELLIGENCE behind the mug -- not a
  generic product description, but "your results shaped this mug."


PLACEMENT:
  Screen: KeepsakeCustomise
  Condition: productId === "character_mug"
  Position: First element inside the scrollable content area,
  ABOVE the live preview zone. In code: first child of the
  scrollable <div> at line 226, before the preview container.

TRIGGER:
  Shown on every entry to KeepsakeCustomise when product is
  character_mug UNLESS sessionStorage key
  "fl:charMugExplainerDismissed" is set.
  Once per session -- not permanent. Returning users in a new
  session see it again until the product is well-understood.

DISMISS:
  User taps the X button (top-right of card).
  On dismiss: set sessionStorage "fl:charMugExplainerDismissed" = "1".
  Also implicitly dismissed when user taps "Continue to Preview"
  (advancing past Customise means they've engaged with the product).

LAYOUT:
  |<-16px->|<------------ calc(100% - 32px) ----------->|<-16px->|
           +----------------------------------------------+
           |  16px padding-top                             |
           |  +------+  +-----------------------------+   |
           |  | ICON |  | HEADLINE ZONE               |   |  [X] 44x44
           |  | 40x40|  | Inter SemiBold 15px #FFFFFF  |   |  top-right
           |  |  px  |  +-----------------------------+   |
           |  |      |  | BODY ZONE -- 2 lines max    |   |
           |  |      |  | Inter Regular 13px #B0B0C8  |   |
           |  +------+  +-----------------------------+   |
           |  16px padding-bottom                          |
           +----------------------------------------------+
           |<-16px->|<-12px gap->|<---- flex 1 ---->|<-44->|
           marginBottom: 0 (preview area below has 16px padding)

DIMENSIONS:
  Card width: calc(100% - 32px) -- 16px margin each side
  Card min-height: 88px (content-driven, not fixed)
  Card border-radius: 12px
  Card padding: 16px all sides
  Icon container: 40px x 40px, border-radius: 10px
  Gap between icon and text: 12px
  Dismiss button: 44px x 44px touch target (icon itself 20px)

COLOURS:
  Background:   #1E1040 (deep violet tint -- distinct from the
                neutral #1a1a2e used by customisation chips below,
                signalling "this is explanatory, not a control")
  Border:       1px solid rgba(124, 58, 237, 0.3)
  Icon bg:      rgba(124, 58, 237, 0.2)
  Icon colour:  #7C3AED (use Sparkles from lucide-react, 20px)
  Headline:     #FFFFFF
  Body text:    #B0B0C8
  Dismiss icon: #6a6a8e (subtle, not prominent)

TYPOGRAPHY:
  Headline: Inter, SemiBold (600), 15px, sentence case, line-height 20px
  Body:     Inter, Regular (400), 13px, line-height 18px

ANIMATION:
  Entry: fade in, opacity 0 -> 1, 200ms ease-out on mount
  Dismiss: fade out, opacity 1 -> 0, 150ms ease-in, then remove from DOM
  No slide -- keeps the element grounded and lightweight.

VISUAL HIERARCHY:
  1. Icon (sparkle/wand -- draws eye to card as distinct from preview)
  2. Headline (one sentence: what the product IS, personalised)
  3. Body (how the user's results shaped this mug)
  4. Dismiss (secondary, corner)

COPY BRIEF FOR COPYWRITER:
  Headline: Communicate that this mug is personalised to THEIR results.
  NOT "here's what a character mug is" -- instead: "your analysis
  results have shaped every part of this mug." The user should
  understand: "my results drove this product."
  Example direction: "Your results, on a real mug"

  Body: Explain in warm, celebratory language that:
  - The character was auto-chosen based on who the child looks like
  - The headline text on the mug (e.g., "MUMMY'S MINI ME") comes
    from their winner
  - The percentage and dominant feature are printed from real results
  Example direction: "We've chosen a celebrating Mama character
  because [child] looks 65% like Mum. The score and feature text
  on the mug are yours too."
  2 lines maximum. Warm, not technical. "We've chosen" not "the
  algorithm selected." Do NOT use the word "render."


-------------------------------------------------------
SPEC 2 -- RESULTS-TO-CHARACTER BRIDGE
-------------------------------------------------------

PLACEMENT:
  Screen: KeepsakeCustomise
  Position: BETWEEN the live preview area and the first customisation
  chips section ("Design Style"). This is the natural reading
  position: user sees the mug preview, then immediately below sees
  WHY this character was chosen, then scrolls to options.

  In code: insert after the preview container div (ends ~line 305)
  and before the customisation chips div (starts ~line 308, the
  <div style={{ padding: "0 16px 16px" }}> block).

  Stacking order in scroll area when all elements are visible:
    1. Spec 1 -- Explanation card (conditional on dismiss state)
    2. Live mug preview (36vh -- see Spec 3 Fix A)
    3. >>> Spec 2 -- Results bridge card (HERE) <<<
    4. Customisation chips (style, age, recipient, character, etc.)

SHOWN WHEN:
  data.winnerLabel is truthy AND data.winnerPct is a number > 0
  (i.e., analysis results exist with a determined winner).

HIDDEN WHEN:
  No analysis results, or winnerLabel/winnerPct are missing.
  Graceful omission -- element does not render. No placeholder,
  no fallback. Customisation chips move up naturally.

LAYOUT:
  |<-16px->|<------------ calc(100% - 32px) ----------->|<-16px->|
           +----------------------------------------------+
           |  12px padding-top                             |
           |                                               |
           |  [WINNER CHIP]  [SCORE CHIP]                  |
           |   pill 28px h    pill 28px h                   |
           |                                               |
           |  [BRIDGE MESSAGE -- 1-2 lines]    mt: 8px     |
           |                                               |
           |  [DOMINANT FEATURE LINE -- 1 line] mt: 4px    |
           |   (only if data.dominantFeatureLabel exists)   |
           |                                               |
           |  12px padding-bottom                          |
           +----------------------------------------------+
           marginTop: 0 (preview area above has 16px padding)
           marginBottom: 16px (before customisation chips)

WINNER CHIP:
  Shape: pill, border-radius: 14px
  Height: 28px
  Padding: 0 12px
  Background: rgba(124, 58, 237, 0.15)
  Border: 1px solid rgba(124, 58, 237, 0.25)
  Dot: 8px circle, filled #7C3AED, margin-right 6px
  Text: data.winnerLabel (e.g., "Mum")
  Font: Inter, Medium (500), 13px, #FFFFFF

SCORE CHIP:
  Shape: pill, border-radius: 14px
  Height: 28px
  Padding: 0 12px
  Background: rgba(124, 58, 237, 0.08)
  Border: 1px solid rgba(124, 58, 237, 0.15)
  Text: `${data.winnerPct}%` (e.g., "65%")
  Font: Inter, Bold (700), 13px, #7C3AED

  Gap between chips: 8px
  Chips are flex, left-aligned

BRIDGE MESSAGE:
  Font: Inter, Regular (400), 13px, line-height 18px
  Colour: #B0B0C8
  Max: 2 lines (wraps naturally, no truncation)
  Margin-top: 8px from chip row

DOMINANT FEATURE LINE (optional):
  Shown only if data.dominantFeatureLabel is truthy
  Font: Inter, Regular (400), 12px, line-height 16px, italic
  Colour: #9090B0
  Margin-top: 4px from bridge message
  Example rendered: "Got Mum's Eyes"

DIMENSIONS:
  Card width: calc(100% - 32px) -- 16px margin each side
  Card min-height: 72px (content-driven)
  Card border-radius: 12px
  Card padding: 12px 16px

COLOURS:
  Background:     #14122A (slightly different from #1a1a2e to
                  create visual layering -- "context card" vs
                  "control card")
  Border:         1px solid rgba(124, 58, 237, 0.2)
  Winner chip bg: rgba(124, 58, 237, 0.15)
  Winner dot:     #7C3AED
  Score chip bg:  rgba(124, 58, 237, 0.08)
  Score text:     #7C3AED
  Bridge text:    #B0B0C8
  Feature text:   #9090B0

ANIMATION:
  Entry: fade in 200ms ease-out (matching Spec 1 timing)

VISUAL HIERARCHY:
  1. Winner chip + dot (colour draws eye, matches results page)
  2. Score chip (percentage -- the key number)
  3. Bridge message (explains connection in words)
  4. Dominant feature (optional reinforcing detail)

COPY BRIEF FOR COPYWRITER:
  Bridge message: Connect the analysis result to the character on
  the mug. The user should read this and think "ah, THAT'S why the
  mug looks like that." Template concept: "[Child] looks [pct]%
  like [Winner] -- so we've picked a [emotion] [character] to
  celebrate that!"
  Tone: warm, not technical. "We've chosen" not "the algorithm
  selected." Brief -- 1-2 lines max.

  Dominant feature line: A secondary detail that adds specificity.
  Template concept: "Got [Winner]'s [dominant feature]."
  Uses data.dominantFeatureLabel. Only render if truthy.

DATA MAPPING (for FE Lead):
  Winner chip label: data.winnerLabel
  Score chip label:  `${data.winnerPct}%`
  Bridge message:    Copywriter template, interpolated with
                     data.childName, data.winnerLabel, data.winnerPct
  Dominant feature:  data.dominantFeatureLabel (conditional)
  Child name:        data.childName (fallback: "Your child")


-------------------------------------------------------
SPEC 3 -- PREVIEW CTA POSITION FIX
-------------------------------------------------------

ASSESSMENT OF OPTIONS:

  Option A (Sticky bottom bar -- fixed at viewport bottom):
    + Always visible regardless of scroll position
    + Proven mobile commerce pattern (Shopify, Amazon, Apple Store)
    + ALREADY IMPLEMENTED on both KeepsakeCustomise (line 746) and
      KeepsakePreview (via MobileActionBar.jsx at z-index 9990)
    + User never has to hunt for the purchase action
    - Content behind bar needs bottom padding

  Option B (Move preview section higher):
    + No fixed positioning needed
    - User can scroll past and lose it
    - Breaks natural hierarchy (preview should be after decisions)
    - Inconsistent with existing fixed-bar pattern

  >>> RECOMMENDATION: Option A -- Sticky bottom bar
  (ALREADY IMPLEMENTED -- the fix is refinement, not replacement)

  RATIONALE: Both screens ALREADY use fixed bottom bars. The
  CEO's complaint is NOT about the bar type but about:
  (a) The mug preview taking 50vh, pushing options far below fold
  (b) Character mug having 5+ customisation sections after preview
  (c) The "Continue to Preview" label not communicating purchase intent

  The fix has THREE parts:


FIX A -- REDUCE PREVIEW ZONE HEIGHT (character_mug only):

  Current: minHeight: "50vh" on the preview container (line 237)
  Proposed: minHeight: "36vh" when productId === "character_mug"
  All other products: unchanged at 50vh

  RATIONALE: Character mug has the most customisation options.
  Reducing preview by 14vh (~100px on a 712px viewport) brings
  the first customisation section closer to the visible fold.
  The MugCeramicPreview renders at 300px width with its own
  aspect ratio -- at 36vh (~256px), the mug still fits with
  16px padding on all sides.


FIX B -- ENHANCE STICKY BAR WITH PRICE CONTEXT (character_mug only):

  Current bar layout:
  +----------------------------------------------------------+
  |  [         Continue to Preview         ]                  |
  +----------------------------------------------------------+

  Proposed bar layout:
  +----------------------------------------------------------+
  |  [PRICE]    [    Preview Your Mug  ->   ]                 |
  +----------------------------------------------------------+

  Full ASCII with dimensions:
  +--------------------------------------------------------------+
  |  borderTop: 1px solid #2a2a4e                                |
  |  10px padding-top                                            |
  |  +----------+                                                |
  |  | PRICE    |  +---------------------------------------+     |
  |  | "14.99"  |  |         CTA BUTTON                    |     |
  |  | Inter    |  |    52px height, 12px border-radius     |     |
  |  | Bold 14  |  |    violet gradient                    |     |
  |  | #FFFFFF  |  |    Inter SemiBold 15px #FFFFFF        |     |
  |  +----------+  +---------------------------------------+     |
  |  paddingBottom: calc(10px + env(safe-area-inset-bottom))      |
  +--------------------------------------------------------------+
  |<-16px->|<60px>|<-12px gap->|<------ flex 1 ------->|<-16px->|

POSITION:
  position: fixed
  bottom: 0
  left: 0, right: 0
  z-index: 100 (matches current, consistent with flow z-index)
  background: #0D0F1A
  borderTop: 1px solid #2a2a4e

HEIGHT:
  Content: 52px (button) + 10px top + 10px bottom = 72px before safe area
  With safe area: ~106px on notched iPhones, ~72px on others

SAFE AREA:
  paddingBottom: calc(10px + env(safe-area-inset-bottom, 0px))
  (Already correct in existing code)

CONTENT PADDING on scroll container:
  Current paddingBottom: 80px (line 232)
  Proposed paddingBottom: 108px (character_mug only)
  Other products: keep 80px

PRICE ZONE (new, left side):
  Width: auto (content-driven)
  Min-width: 60px
  Display: flex, alignItems: center
  Font: Inter, Bold (700), 16px, #FFFFFF
  Content: pound sign + spec.price (e.g., "14.99")
  Sub-line: Inter, Regular (400), 11px, #9090B0, "Free delivery"
  Vertical stack, gap: 2px
  Shown only when price available; if no price, CTA takes full width

CTA BUTTON (existing, minor enhancement):
  Width: flex: 1
  Height: 52px
  Border-radius: 12px
  Background: linear-gradient(135deg, #7C3AED, #6D28D9)
  Font: Inter, SemiBold (600), 15px, #FFFFFF
  Touch target: 52px height x full remaining width (well above 44pt)


FIX C -- SCROLL PADDING ON CONTENT (no visual change):

  Increase paddingBottom on the scrollable content <div> from 80px
  to 108px specifically for character_mug. This ensures the last
  customisation section (personalised message toggle) is fully
  visible above the enhanced sticky bar.

  For non-character_mug products: keep 80px (bar is simpler, 68px).

KEYBOARD INTERACTION:
  When text inputs gain focus (personalised message fields), the
  iOS keyboard pushes fixed elements up naturally. No special
  handling needed -- the bar sits above the keyboard.

COLOURS:
  Bar background:  #0D0F1A (unchanged, matches page bg)
  Border-top:      1px solid #2a2a4e (unchanged)
  Price text:      #FFFFFF
  Sub-price text:  #9090B0
  CTA background:  linear-gradient(135deg, #7C3AED, #6D28D9)
  CTA text:        #FFFFFF

VISUAL HIERARCHY:
  1. CTA button (violet gradient, dominant visual weight)
  2. Price (white bold text, always visible without scrolling)
  3. Sub-price line (muted, supplementary)

COPY BRIEF FOR COPYWRITER:
  CTA label on Customise screen: Consider "Preview Your Mug" or
  "See Your Mug" instead of "Continue to Preview." The label should
  remind the user what they're building. Max ~20 characters to fit
  one line at 15px on a 375px screen with the price zone beside it.

  Price sub-line: "Free delivery" or "Incl. delivery" -- short,
  one line, reinforces value.


-------------------------------------------------------
PLAN GATE NOTE (KS-07 -- OUT OF SCOPE)
-------------------------------------------------------

  The KeepsakePreview screen handles the plan gate:
  - canOrderMerchandise() === true:  "Add to Basket -- [price]"
  - canOrderMerchandise() === false: "Upgrade to Plus to Order"
    with onClick -> /plans

  KS-07 reports the modal closes silently for free users. This
  suggests /plans may not exist or navigation fails silently.

  OUT OF SCOPE for this document. Flag for separate task:
  "Free tier plan gate feedback on character mug order CTA."


-------------------------------------------------------
IMPLEMENTATION NOTES FOR FE LEAD
-------------------------------------------------------

  1. ALL new elements use INLINE STYLES (consistent with existing
     KeepsakeCustomise.jsx which uses inline styles throughout).
     Do NOT introduce Tailwind classes into this file -- it would
     create a mixed pattern.

  2. Touch targets: all interactive elements >= 44px in smallest
     dimension. Verified in this spec:
     - Spec 1 dismiss: 44x44px
     - Spec 3 CTA: 52px height x full width
     - All existing buttons already meet 44pt (verified in source)

  3. Safe area: already handled correctly on the existing sticky
     bar. No changes to the approach.

  4. SessionStorage key for Spec 1: "fl:charMugExplainerDismissed"
     Use sessionStorage (not localStorage) so banner reappears
     in new sessions.

  5. Data access for Spec 2:
     - data.winnerLabel  (string, e.g., "Mum")
     - data.winnerPct    (number, e.g., 65)
     - data.childName    (string, e.g., "Emma")
     - data.dominantFeatureLabel (string, e.g., "Eyes") -- optional
     All already available as the `data` prop.

  6. Spec 3 preview zone: only reduce to 36vh when
     productId === "character_mug". All other products keep 50vh.

  7. Spec 3 paddingBottom: increase from 80px to 108px for
     character_mug only.

  8. Render order in scroll container (character_mug):
       a. Spec 1 -- Explanation card (conditional on dismiss)
       b. Live mug preview (36vh for character_mug)
       c. Spec 2 -- Results bridge (conditional on data)
       d. Customisation chips (style, age, recipient, character, etc.)

  9. Animations: reuse existing charPickerFadeIn keyframe pattern
     from CharacterPicker.jsx (200ms ease-out fade). Add any new
     keyframes to the existing <style> block.

  10. Gate all three specs with: productId === "character_mug".
      Do NOT show for mug_wrap, family_mug_set, or other products.


-------------------------------------------------------
ASSETS REQUIRED
-------------------------------------------------------

  1. SPARKLE ICON (Spec 1 -- explanation card)
     Source: lucide-react Sparkles icon (already in dependencies)
     Size: 20px x 20px, rendered inside 40x40px container
     Colour: #7C3AED
     No new asset file needed.

  No other new assets required. All character images, brand
  colours, and UI patterns already exist in the codebase.

===============================================
  END OF VISUAL DIRECTION
  Awaiting CEO/CMO approval before FE Lead proceeds.
===============================================
```
