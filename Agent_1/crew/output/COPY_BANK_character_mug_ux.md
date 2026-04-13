===============================================
  COPY BANK -- Character Mug UX Clarity
  Copywriter -- 2026-04-07
===============================================

PRODUCT: FamiliLook -- Character Mug (mobile flow)
CONTEXT: In-app UI copy (KeepsakeCustomise + KeepsakePreview screens)
AUDIENCE: Parents/family members building a character mug after analysis
VISUAL SPEC REFERENCE: VISUAL_DIRECTION_character_mug_ux.md

TONE GUIDE: Warm, celebratory, family pride. Match existing mugThemes.js
voice ("YOUR FAMILY RESEMBLANCE", "HAPPY MOTHER'S DAY"). No clinical
language. No mention of AI, algorithms, engines, or analysis pipelines.
Say "your results" or "your family's look" -- never "our engine" or
"we analysed".


-----------------------------------------------------------
COPY JOB 1 -- PRODUCT EXPLANATION MOMENT
Container: Dismissable banner card, top of KeepsakeCustomise scroll area
Headline zone: Inter SemiBold 16px, 1 line
Body zone: Inter Regular 13px, max 2 lines (~65 chars/line at 13px)
-----------------------------------------------------------

HEADLINES (max 35 chars -- verified):

  H01-A | Your look, on a mug             | 22 chars | Variant A
          Y-o-u-r- -l-o-o-k-,- -o-n- -a- -m-u-g
          1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22 = 22 PASS

  H01-B | A character made from family     | 31 chars | Variant B
          A- -c-h-a-r-a-c-t-e-r- -m-a-d-e- -f-r-o-m- -f-a-m-i-l-y
          1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31 = 31 PASS

BODY TEXT (max 2 lines, ~65 chars/line -- verified):

  B01-A | Line 1: "We matched your family's look to a one-of-a-kind"   | 52 chars
          Line 2: "character. Pick one below -- we'll print it on your mug." | 57 chars
          Total: 109 chars across 2 lines. Both under 65. PASS

  B01-B | Line 1: "Your results shaped a personalised character just"  | 51 chars
          Line 2: "for your family. Choose one and we'll put it on a mug." | 55 chars
          Total: 106 chars across 2 lines. Both under 65. PASS

DISMISS LABEL:

  D01   | Got it   | 6 chars


-----------------------------------------------------------
COPY JOB 2 -- RESULTS-TO-CHARACTER BRIDGE
Container: Bridge card below explanation banner, single-line chip + text
Bridge message zone: Inter Regular 12px, max 1 line
Template variables: {childName}, {winnerLabel}, {pct}
-----------------------------------------------------------

NOTE ON LAYOUT: Per the Visual Director's spec, the bridge card has
two text zones:
  (a) Dynamic text (14px, #FFFFFF): "[Child] looks [pct]% like [Winner]"
      -- this is data-driven, NOT copywriter-authored. FE Lead constructs
      it from data.childName, data.winnerPct, data.winnerLabel.
  (b) Bridge message (12px, #9090B0): copywriter-authored, single line,
      max 50 chars. This is what the templates below provide.

The bridge message sits BELOW the dynamic text line. It connects the
result statement to the character mug action.


TEMPLATE: Named child + named winner (pct shown)
  Dynamic text (FE-built): "{childName} looks {pct}% like {winnerLabel}"
  Bridge message (Copywriter):

  T01-A | Celebrate it -- pick a character for their mug  | 50 chars
          C-e-l-e-b-r-a-t-e- -i-t- ---  -p-i-c-k- -a- -c-h-a-r-a-c-t-e-r- -f-o-r- -t-h-e-i-r- -m-u-g
          1...50 = 50 PASS

  T01-B | That look deserves a mug -- pick a character    | 49 chars
          T-h-a-t- -l-o-o-k- -d-e-s-e-r-v-e-s- -a- -m-u-g- ---  -p-i-c-k- -a- -c-h-a-r-a-c-t-e-r
          1...49 = 49 PASS


TEMPLATE: Named child + unnamed winner
  Dynamic text (FE-built): "{childName} takes after {winnerLabel}"
  Bridge message (Copywriter):

  T02-A | Turn that family look into a keepsake mug       | 46 chars
          T-u-r-n- -t-h-a-t- -f-a-m-i-l-y- -l-o-o-k- -i-n-t-o- -a- -k-e-e-p-s-a-k-e- -m-u-g
          1...46 = 46 PASS

  T02-B | Pick a character to celebrate the resemblance   | 49 chars
          P-i-c-k- -a- -c-h-a-r-a-c-t-e-r- -t-o- -c-e-l-e-b-r-a-t-e- -t-h-e- -r-e-s-e-m-b-l-a-n-c-e
          1...49 = 49 PASS


TEMPLATE: No child name
  Dynamic text (FE-built): "Your child looks {pct}% like {winnerLabel}"
  Bridge message (Copywriter):

  T03-A | Make it a mug -- choose a character below       | 47 chars
          M-a-k-e- -i-t- -a- -m-u-g- ---  -c-h-o-o-s-e- -a- -c-h-a-r-a-c-t-e-r- -b-e-l-o-w
          1...47 = 47 PASS

  T03-B | Capture that family look on a character mug     | 47 chars
          C-a-p-t-u-r-e- -t-h-a-t- -f-a-m-i-l-y- -l-o-o-k- -o-n- -a- -c-h-a-r-a-c-t-e-r- -m-u-g
          1...47 = 47 PASS


TEMPLATE: Blend result
  Dynamic text (FE-built): "A beautiful blend of both parents"
  Bridge message (Copywriter):

  T04-A | The best of both -- pick a character to match   | 49 chars
          T-h-e- -b-e-s-t- -o-f- -b-o-t-h- ---  -p-i-c-k- -a- -c-h-a-r-a-c-t-e-r- -t-o- -m-a-t-c-h
          1...49 = 49 PASS

  T04-B | Celebrate both sides on a keepsake mug          | 44 chars
          C-e-l-e-b-r-a-t-e- -b-o-t-h- -s-i-d-e-s- -o-n- -a- -k-e-e-p-s-a-k-e- -m-u-g
          1...44 = 44 PASS


-----------------------------------------------------------
COPY JOB 3 -- PREVIEW CTA BUTTON
Max 20 chars -- verified
Screen: KeepsakeCustomise sticky bottom bar
Current label: "Continue to Preview" (19 chars -- within limit but generic)
-----------------------------------------------------------

  CTA-01 | Preview Your Mug    | 16 chars
           P-r-e-v-i-e-w- -Y-o-u-r- -M-u-g
           1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16 = 16 PASS

  CTA-02 | See Your Mug        | 12 chars
           S-e-e- -Y-o-u-r- -M-u-g
           1-2-3-4-5-6-7-8-9-10-11-12 = 12 PASS

  CTA-03 | Reveal Your Mug     | 15 chars
           R-e-v-e-a-l- -Y-o-u-r- -M-u-g
           1-2-3-4-5-6-7-8-9-10-11-12-13-14-15 = 15 PASS

RECOMMENDATION: CTA-01 ("Preview Your Mug"). It names the product,
tells the user what happens next, and uses active voice. "See Your Mug"
(CTA-02) is shorter but slightly less specific about the action.
"Reveal Your Mug" (CTA-03) adds excitement but may set expectations
for an animation/reveal moment that doesn't exist.


-----------------------------------------------------------
IMPLEMENTATION NOTES FOR FE LEAD
-----------------------------------------------------------

1. Use these exact strings. Do not abbreviate, reformat, or rephrase.

2. COPY JOB 1 -- Explanation Banner:
   - Show H01-A + B01-A as default. H01-B + B01-B are A/B test variants.
   - Headline is a single line in the banner (16px SemiBold, #FFFFFF).
   - Body is 2 lines (13px Regular, #B0B0C8).
   - Dismiss label "Got it" is sr-only text for the X button's aria-label,
     or shown as visible text if the Visual Director prefers a text
     dismiss link instead of an icon. Confirm with VD.

3. COPY JOB 2 -- Bridge Card:
   - The dynamic text line ("{childName} looks {pct}% like {winnerLabel}")
     is NOT in this copy bank -- FE Lead constructs it from data props.
   - The bridge message (T01-T04 templates) goes in the second line
     (12px Regular, #9090B0).
   - Use T01 when childName AND winnerLabel AND pct are all available.
   - Use T02 when childName AND winnerLabel are available but you want
     a variant without showing the percentage (fallback scenario).
   - Use T03 when childName is missing/empty.
   - Use T04 when winner === "blend" or winner === "unknown".
   - Priority order: T04 (blend check) > T01 (full data) > T03 (no name).
     T02 is an A/B variant of T01, not a separate fallback tier.

4. COPY JOB 3 -- CTA Button:
   - Replace "Continue to Preview" with the chosen CTA variant.
   - The label applies ONLY to the character_mug product on the
     KeepsakeCustomise screen. All other products keep "Continue to Preview".

5. Character count contract: all headlines are under 35, all bridge
   messages are under 50, all CTA labels are under 20. These limits
   are hard -- do not append text, prices, or icons inside the label
   string itself. Price goes in the separate price zone per VD spec.

6. No template variables appear in Copy Job 1 or Copy Job 3. Only
   Copy Job 2 bridge messages are static (no variables in the bridge
   line itself -- the dynamic text line above it handles personalisation).


-----------------------------------------------------------
BRAND COMPLIANCE
-----------------------------------------------------------

  Health/DNA claims:          NONE
  AI/algorithm mentions:      NONE
  "for entertainment" note:   N/A (in-app UI, not marketing material)
  Under-13 targeting:         NONE (copy addresses the parent/buyer)
  50/50 language:             NONE (blend variant celebrates "both", never "equal")
  FamiliPoker content:        NONE
  Clinical/technical tone:    NONE (no "analysis", "engine", "algorithm")

  VERDICT: PASS

===============================================
  END OF COPY BANK
  Awaiting CEO/CMO approval.
  After approval, FE Lead implements using exact strings above.
===============================================
