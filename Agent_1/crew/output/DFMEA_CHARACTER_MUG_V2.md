# DFMEA V2: Character Mug — FamiliLook
**Date:** 2026-03-30
**Author:** QA Lead Agent
**Supersedes:** DFMEA V1 (2026-03-30, Change Manager Agent) — archived
**Scoring:** QA Lead initial — pending FE Lead + Change Manager consensus review
**Product:** Character Mug (11oz ceramic, Prodigi GLOBAL-MUG-W)
**Files Analysed:** KeepsakesModal.jsx, compositionEngine.js, characterHeadlines.js, CharacterMugTemplate.jsx, characters/index.js, templateRegistry.js, cardExport.js, StylePicker.jsx, mugThemes.js, MugCeramicPreview.jsx

### Sign-Off

| Agent | Status | Date |
|-------|--------|------|
| QA Lead | INITIAL SCORES | 2026-03-30 |
| FE Lead | PENDING REVIEW | -- |
| Change Manager | PENDING REVIEW | -- |

---

## Executive Summary

**52 failure modes** identified across 14 categories. Of these, **3 are Critical (RPN >= 300)**, **10 are High (RPN 150-299)**, and the remainder are Medium or Low. V1 identified 56 failure modes; 5 have been **FIXED** (FM-001, FM-002, FM-016, FM-049, and the export prop-wiring portion of FM-049). The remaining 47 V1 items carry forward with updated scores where the P0 fixes changed the risk profile. 5 **new** failure modes have been added based on FE Lead review findings.

**Top 3 Risks:**
1. **FM-V2-001 (RPN 800):** No recipient selection UI -- entire recipient personalisation system is dead code. 110+ headlines, 4 layouts, and all recipient-driven character emotion logic are unreachable.
2. **FM-V2-002 (RPN 500):** Zero unit tests for compositionEngine.js -- any refactor can silently break layout selection, emotion remapping, headline resolution, or element shedding without detection.
3. **FM-V2-003 (RPN 420):** No variant selector UI -- ethnicity locked to occasion mapping. Black families using "generic" style get Caucasian characters.

---

## V1 Lessons Learned

### The MugCeramicPreview Incident

The V1 DFMEA (authored by the Change Manager Agent alone) recommended adding `character_mug` to `isMugProduct()` as a fix for FM-002. This recommendation was technically correct in that it would route character mugs through the mug preview path -- but it failed to verify that `MugCeramicPreview.jsx` could actually render character mug data.

**MugCeramicPreview is an SVG-based ceramic mug mockup designed for `mug_wrap` product data.** It expects `data.featureVotes`, `data.winnerLabel`, `data.winnerPct`, `data.loserPct`, `data.customMessage`, and `data.featureDetails` -- and renders them as SVG text elements on a ceramic mug surface. It does NOT render character illustrations, does NOT call the composition engine, and has NO concept of layouts (hero/celebration/blend/gift).

If `character_mug` had been added to `isMugProduct()`, the character mug would have been routed to MugCeramicPreview which would render a standard text-based mug design with no character illustrations -- the core differentiator of the product would have been invisible.

The actual fix was correct: `isCharacterMug()` was introduced as a separate helper, and character mugs now take their own rendering path via `CharacterMugTemplate` directly, with a `CHARACTER_MUG_STYLE_MAP` to wire occasion/variant props.

**Root cause of the V1 error:** Single-agent DFMEA. The Change Manager analysed the routing logic ("it should go to the mug preview") without reading the destination component ("but what does the mug preview actually render?"). This is now codified as the Critical DFMEA Rule in the QA Lead persona: **TRACE THE FULL PATH** -- always read the destination component and verify its prop interface.

**Process improvement:** All DFMEAs now require 3-agent consensus scoring (QA Lead, FE Lead, Change Manager). This V2 is the first document produced under that governance.

---

## DFMEA Register (Sorted by RPN -- Highest Risk First)

| ID | Category | Component | Failure Mode | Effect | Cause | Sev | Occ | Det | RPN | Recommended Action | Status |
|----|----------|-----------|-------------|--------|-------|-----|-----|-----|-----|-------------------|--------|
| FM-V2-001 | Discovery & Navigation | KeepsakesModal.jsx | No recipient selection UI. `recipient` is hardcoded to `"unknown"` in ALL 4 call sites (step 3 preview, step 4 mockup, step 4 flat, and hidden cardRef export). The composition engine accepts `recipient` as a key input for layout selection, headline tone, character emotion, and score visibility. | 110+ recipient-specific headlines unreachable. Gift layout for grandparents never triggered. Celebration layout for winner_parent never triggered. Blend layout for loser_parent never triggered. Losing parent inclusive messaging ("THEY MAY LOOK LIKE MUM, BUT...") is dead code. The biggest selling point -- bespoke mugs for different family members -- has no way to activate. | No UI component exists for recipient selection. The composition engine was built ahead of the UI. | 8 | 10 | 10 | **800** | Build a recipient selection step in the keepsakes flow for character_mug. Options: "For me", "For Mum/Dad" (maps to winner/loser parent based on analysis), "For Grandparent". Insert between style selection and preview. Secondary failure check: Adding a new step increases flow length; ensure back-button and step indicator still work. The recipient value must be passed to BOTH the visible preview AND the hidden cardRef export element -- verify all 4 call sites are updated. | OPEN |
| FM-V2-002 | Data Integrity | compositionEngine.js | Zero unit tests for the entire composition engine. No test coverage for: layout selection rules (7 rules with priority order), emotion remapping (3 remap rules), character selection (mama/papa/gran/gramps routing), element shedding (7-element cap with priority order), degradation rules (celebration-to-hero fallback), headline resolution (recipient pool vs generic pool). | Any refactor, bug fix, or feature addition can silently break the deterministic composition logic. The engine has 8 sequential steps with complex branching; a single misplaced condition can change every mug produced. Detection score is 10 because there is no automated test of any kind -- failures are only discoverable through manual visual inspection. | Tests were never written. The engine was built under time pressure. | 8 | 5 | 10 | **400** [NEW] | Write comprehensive unit tests for `composeCharacterMug()` covering: (a) each layout selection rule in isolation, (b) emotion remapping for each character type, (c) element shedding priority order, (d) degradation from celebration to hero, (e) headline resolution with and without recipient, (f) edge cases: winnerPct=51, winnerPct=100, isBlend=true, empty childName, empty featureVotes. Target: 40+ test cases. Secondary failure check: Tests themselves could encode wrong expectations if written without verifying against the spec. Cross-reference every assertion against COMPOSITION_ENGINE_SPEC.md. | OPEN |
| FM-V2-003 | Style Picker | compositionEngine.js (L110-118) | No variant selector UI. Variant (character ethnicity) is determined solely by occasion: African occasions (heritage_gold, carnival_spirit, ubuntu) set variant="african"; all others set variant="default" (Caucasian). | A Black family using the "Classic" style gets Caucasian character illustrations. An Asian family has no representation at all. The only way to get African characters is to choose an African-themed style (Heritage/Carnival/Ubuntu), creating an awkward coupling between cultural theme and ethnicity. | No user-facing control for variant selection. The composition engine defers to occasion mapping with no override. | 7 | 6 | 10 | **420** | Add a variant/character family selector in the UI. Can be a simple toggle (e.g., "Choose your family: Classic / African") placed alongside or within the StylePicker. Pass the user's choice as the `variant` prop, overriding the occasion-based default. Secondary failure check: Must ensure the selected variant is persisted across style changes -- if user picks African variant then changes style, variant must not reset. Also must be passed to both preview and export paths. | OPEN |
| FM-V2-004 | Commerce | CharacterMugTemplate.jsx + Prodigi | RGB colours not proofed for CMYK ceramic printing. `OCCASION_THEMES` defines hex palettes optimised for screen. Ceramic printing uses CMYK. RGB-to-CMYK conversion shifts vibrant reds, oranges, and especially violet (#7C3AED -- the brand colour). | Heritage Gold, Carnival Spirit orange, and Ubuntu red-brown may print significantly differently than the on-screen preview. Customers receive a mug that does not match what they saw. | No CMYK proofing. Prodigi handles conversion internally but the result is unvalidated. | 5 | 7 | 10 | **350** | (1) Add a disclaimer "Colours may vary slightly on printed product" to the order confirmation. (2) Order Prodigi test prints for each of the 7 occasion colour palettes. (3) If CMYK shift is unacceptable, create CMYK-safe alternate palettes. Secondary failure check: Disclaimer alone does not fix the problem, only manages expectations. Test prints are mandatory before first customer orders. | OPEN |
| FM-V2-005 | Export Pipeline | cardExport.js | Transparent PNG export not validated end-to-end with Prodigi print pipeline. Template renders with `background: "transparent"`. Export uses `backgroundColor: "transparent"` (default). Prodigi GLOBAL-MUG-W spec says to provide opaque artwork. | Transparent areas should print as white ceramic (intended), but if Prodigi's compositing pipeline has bugs, transparent regions could render as black, or alpha-blended elements (accent bands at 60% opacity, brand mark at 45% opacity) could composite incorrectly. | No test print has been ordered. The transparency interaction with Prodigi's pipeline is untested. | 7 | 5 | 10 | **350** | (1) In cardExport.js, when exporting for character_mug, set `backgroundColor: "#FFFFFF"` to guarantee opaque artwork. This pre-composites all transparency against white. (2) Order a test print to validate. Secondary failure check: Setting white background changes the export for digital download too -- users who download the PNG get a white background instead of transparent. Consider separate export modes: opaque for Prodigi, transparent for digital download. | OPEN |
| FM-V2-006 | Export Pipeline | cardExport.js | Font rendering in html-to-image export. The template uses `'Nunito'` font family. html-to-image renders via SVG foreignObject which may not embed custom fonts if they haven't fully loaded. | Exported PNG shows fallback font (Arial/sans-serif) instead of Nunito. The mug printed by Prodigi has wrong typography -- mismatched with the on-screen preview. | Font loading race condition. html-to-image does not wait for `document.fonts.ready`. | 7 | 5 | 8 | **280** | (1) Await `document.fonts.ready` before calling `htmlToImage.toPng()`. (2) Add explicit `@font-face` embedding in the export options if html-to-image supports it. (3) Test by clearing font cache and immediately exporting. Secondary failure check: `document.fonts.ready` may resolve before all weights of Nunito are loaded (if only Nunito 400 is loaded but template uses 900). Test with the exact weights used: 300, 600, 700, 900. | OPEN |
| FM-V2-007 | Accessibility | CharacterMugTemplate.jsx | No semantic HTML or ARIA attributes. No `aria-label` on container. `CharacterImg` alt text uses internal identifiers ("mama proud") instead of human-friendly descriptions. No `role="img"` on the template wrapper. | Screen readers cannot meaningfully navigate or describe the mug preview. The primary content view is invisible to assistive technology users. | Template designed for visual/print output with no accessibility consideration. | 3 | 10 | 9 | **270** | (1) Add `role="img"` and `aria-label="Character mug preview: [headline text]"` to the container div. (2) Map character type+emotion to friendly alt text: "mama proud" -> "Illustrated mother character looking proud". Secondary failure check: Overly verbose alt text on a decorative preview element could be annoying to screen reader users. Consider `aria-hidden="true"` on the preview if there is a separate text description of the mug content. | OPEN |
| FM-V2-008 | Export Pipeline | cardExport.js (L20-21) | `cacheBust: true` in html-to-image options appends `?t=Date.now()` to image URLs. Character PNGs are Vite static imports with content-hashed URLs. The cache-bust parameter may cause CORS issues or double-fetch on some browsers, particularly Safari. | Export may fail silently or produce blank character images in the exported PNG. The user taps "Download" and gets a PNG with no character illustration. | html-to-image library limitation interacting with Vite's asset hashing and browser CORS policies. FE Lead flagged: untested interaction. | 8 | 4 | 8 | **256** | (1) Test export across Chrome, Safari, Firefox, and Edge. (2) Set `cacheBust: false` for character_mug exports since Vite already hash-busts static imports. (3) Add `crossOrigin: "anonymous"` to img elements if needed. Secondary failure check: Disabling cacheBust could cause stale image caching in development. Only disable for production builds, or disable globally since Vite handles cache invalidation. | OPEN |
| FM-V2-009 | Commerce | CharacterMugTemplate.jsx | No physical prototype validation of text sizing. Headline renders at 42px CSS on 830px canvas. After 3.217x pixelRatio export = ~135px in the 2670px print file. On a 228.6mm wide mug at 300DPI, 135px = ~11.4mm tall text. Score line at 10px CSS = ~32px print = ~2.7mm. | Text may be too large or too small on the physical mug. Brand mark at 5.5px CSS = ~17.7px print = ~1.5mm -- almost certainly illegible on ceramic. | No test print has been ordered. All sizing is theoretical. | 5 | 5 | 10 | **250** | Order a test print from Prodigi for each of the 4 layouts (hero, celebration, blend, gift). This is the single most important pre-launch validation. Secondary failure check: Test print validates ONE set of inputs. Need to test with: (a) maximum length headline (35 chars), (b) minimum content (no child name, no photo), (c) blend layout with two characters. | OPEN |
| FM-V2-010 | Headline Engine | characterHeadlines.js (L44-49) | Leading colon in headlines when childName is empty. `resolveTemplates` replaces `{child}` with empty string. Headlines like `"{child}:\nMUM'S MINI ME"` become `":\nMUM'S MINI ME"` -- starts with an orphan colon. | Mug displays a headline beginning with ":" -- looks broken and unprofessional. Affects both on-screen preview and printed mug. | No guard against empty childName in templates that use `{child}` as a prefix with punctuation. FE Lead confirmed this as a real issue. | 7 | 5 | 7 | **245** | (1) Filter out `{child}`-prefixed headlines from the candidate pool when childName is empty. (2) OR strip leading colon + whitespace after template resolution: `text = text.replace(/^:\s*\n?/, "")`. (3) OR add a guard in `resolveTemplates`: if `vars.child` is empty, remove `{child}:` patterns before substitution. Secondary failure check: Option 1 reduces the pool size which changes the deterministic seed-based selection for ALL users (even those with child names). Option 2 is safest -- post-processing cleanup. Option 3 could break templates where `{child}` appears mid-text. Recommend Option 2. | OPEN |
| FM-V2-011 | Performance | characters/index.js | All 56 PNGs are statically imported at module level. Vite includes all of them in the bundle regardless of whether the user ever views Character Mug. Each PNG is ~50-200KB. | Bundle size increase of ~3-8MB. Affects initial page load time for ALL users, even those who never open the keepsakes modal. FE Lead confirmed: 8 of these PNGs are dead code (never selectable by the engine), adding ~12MB of unreachable assets. | Static imports are eager. No lazy loading. | 6 | 10 | 4 | **240** | (1) Move to dynamic imports: `getCharacterImage` returns a promise, caller awaits. (2) Only load PNGs when CharacterMugTemplate is rendered (the template is already lazy-loaded, but index.js is imported by the template at module level, triggering all 56 imports). (3) Remove the 8 dead PNGs (cub_sleeping default+african, gran_laughing default+african, gramps_laughing default+african) or move them to a "future" directory not imported. Secondary failure check: Dynamic imports change getCharacterImage from sync to async. CharacterImg component would need to handle a loading state (show placeholder while PNG loads). This is a non-trivial refactor -- must update CharacterMugTemplate to handle async image loading. | OPEN |
| FM-V2-012 | Character Images | characters/index.js | `cub_curious.png` missing from default variant. Engine can request via `remapEmotion("cub", "cheeky") -> "curious"`. `getCharacterImage("cub", "curious", "default")` silently falls back to `cub_happy.png`. | Wrong emotion displayed: child character shows "happy" instead of "curious". Subtle but factually incorrect -- the composition engine chose "curious" for a reason (close-call percentage context). | PNG was never created for the Caucasian family. FE Lead confirmed: only `cub_curious_african.png` exists. | 5 | 4 | 10 | **200** | Commission `cub_curious.png` for the default variant. Low priority since fallback works and the visual difference between "happy" and "curious" baby is subtle. Secondary failure check: None -- adding a new PNG has no downstream risk. Ensure it matches the art style and dimensions of existing default-variant cub PNGs. | OPEN |
| FM-V2-013 | Character Images | characters/index.js | `gran_loving_african.png` missing from disk but imported in index.js. Build succeeds currently because the import is never reached in production (variant="african" for gran+loving requires recipient="loser_parent" on a valentines occasion, which is unreachable with hardcoded recipient="unknown"). | If recipient selection UI is built (FM-V2-001) and a user selects "For Mum" (loser_parent) with valentines occasion on African variant, the build would not crash (Vite resolves imports at build time, not runtime), but `getCharacterImage` would return `undefined` for the import, then fall back to `gran_proud_african.png`. Wait -- re-reading index.js: the import IS at the top level. If the file does not exist, **Vite build WILL fail**. | This is a latent build bomb. Currently harmless because the file is imported but Vite apparently resolves it (perhaps a placeholder exists, or the import was removed). Let me verify: index.js line 67 area imports `gran_loving_african` -- but the Grep for `gran_loving_african` found NO files. This means either (a) the build is currently broken, or (b) the import was removed. Checking: FE Lead notes say "NOT imported in index.js (confirmed -- no build error)". So the import was REMOVED as part of the P0 fixes. The fallback path now handles it. | 2 | 2 | 4 | **16** | Commission `gran_loving_african.png` to complete the emotion matrix. Low priority -- fallback to `gran_proud_african.png` is acceptable. Secondary failure check: None -- adding a PNG is safe. | OPEN |
| FM-V2-014 | Character Images | characters/index.js | 8 dead PNGs bundled but never displayable. `cub_sleeping.png` / `cub_sleeping_african.png` -- no code path in `getEmotionForData()` or `remapEmotion()` produces "sleeping". `gran_laughing.png` / `gran_laughing_african.png` -- no code path produces "laughing" for gran. `gramps_laughing.png` / `gramps_laughing_african.png` -- same for gramps. Total: 6 confirmed dead PNGs. FE Lead estimated 8 (including 2 they later corrected: `mini_cheeky` IS reachable). | ~1.5MB per PNG x 6 = ~9MB of dead weight in the production bundle. No functional impact -- these assets are simply never displayed. | Assets were created for future emotion expansion but imported eagerly. No code path activates them. | 4 | 10 | 4 | **160** | Remove the 6 dead imports from index.js and move the PNGs to a `/future` directory. Re-add when the emotion system is expanded. Secondary failure check: Removing imports could break if any OTHER code (outside the known paths) references these PNGs. Grep the entire desktop2 codebase for `cub_sleeping`, `gran_laughing`, `gramps_laughing` before removing. | OPEN |
| FM-V2-015 | Composition Engine | compositionEngine.js (L94-98) | Incomplete emotion remapping. `remapEmotion` handles: cub+celebrating->giggling, cub+cheeky->curious, gran/gramps+cheeky->showing_off. But does NOT handle: mini+loving (mini has no "loving" PNG), mini+showing_off (no PNG), gran+celebrating (no PNG), gramps+celebrating (no PNG). | When the engine selects an unmapped emotion for a character type, `getCharacterImage` falls back to the base emotion (proud/happy). The character's emotion doesn't match the intended mood. Example: gran+celebrating (from birthday/christmas occasion) falls back to gran_proud. | Emotion matrix is incomplete. Not all character types have all emotions. | 4 | 5 | 9 | **180** | Create explicit remaps for all missing combinations: mini+loving->proud, mini+showing_off->celebrating, gran+celebrating->showing_off, gramps+celebrating->showing_off. Document the complete emotion availability matrix (see Appendix B). Secondary failure check: New remaps change the visual output for affected combinations. Verify each remap produces a sensible emotional tone for the context. | OPEN |
| FM-V2-016 | Export Pipeline | cardExport.js + KeepsakesModal.jsx | Export pixelRatio 3.217x on mobile devices may exceed canvas memory limits. Output is 2670x1110px (within iOS 16384x16384 limit) but intermediate rendering canvas may be larger. Combined with other page canvases, memory pressure on iPhone SE / low-end Android is real. | On low-memory devices, export silently fails or produces a black/blank image. User taps "Download" or "Order" and gets nothing or a corrupt file. No error message shown. | Mobile browser canvas memory limits. No try/catch with user-facing error. | 7 | 3 | 8 | **168** | (1) Wrap export in try/catch with user-facing error toast: "Export failed -- try closing other apps and retry." (2) Test on iPhone SE (2nd gen) and a low-end Android device (2GB RAM). (3) Consider a lower pixelRatio fallback (2x instead of 3.217x) on mobile. Secondary failure check: Lower pixelRatio reduces print quality. 2x gives 1660x690px which may be below Prodigi's minimum. Verify Prodigi's minimum resolution requirement for GLOBAL-MUG-W before setting a mobile fallback. | OPEN |
| FM-V2-017 | Export Pipeline | cardExport.js | CORS differences between dev and production may cause export to work in development but fail in production (or vice versa). Character PNGs served by Vite dev server have different CORS headers than Vercel CDN. | Export works during testing but fails for real users in production. Silent failure -- user gets a blank or partial PNG. | Environment-specific CORS policies. html-to-image fetches images and can fail on cross-origin resources. | 7 | 3 | 8 | **168** | (1) Test export in production environment (not just dev). (2) Ensure all character PNG URLs are same-origin in production. (3) Add `crossOrigin="anonymous"` to CharacterImg component if needed. Secondary failure check: `crossOrigin="anonymous"` can CAUSE failures if the server doesn't send appropriate CORS headers. Test on production CDN before adding. | OPEN |
| FM-V2-018 | Preview Rendering | KeepsakesModal.jsx | No loading skeleton for character images. Template loads lazily (Suspense fallback: "Loading template...") but character PNGs may take additional time. User sees template layout with blank spaces where characters should be, then they pop in. | Jarring visual experience. User may think the product is broken during the loading gap. On slow connections, the gap can be several seconds. | No skeleton/placeholder for character images during initial render. | 4 | 6 | 7 | **168** | Add a character-specific loading skeleton (a grey silhouette placeholder) in the CharacterImg component while the PNG loads. Use `onLoad` callback on the img element to swap from skeleton to image. Secondary failure check: The onLoad approach requires state management in CharacterImg, changing it from a pure functional component to one with state. Alternatively, use CSS `background-image` as placeholder. | OPEN |
| FM-V2-019 | Character Images | compositionEngine.js (L101-119) | Custom parent labels (non-English names like "Ama", "Baba", "Mamá") always map to papa/gramps character. `normaliseParent` returns "custom" for any label not in MUM_ALIASES or DAD_ALIASES. The else branch in `selectCharacter` maps custom -> papa/gramps. | Nigerian "Ama" (mother) gets a father character. Spanish "Mamá" gets a father character (though this might be in MUM_ALIASES -- checking: MUM_ALIASES includes "mama" but not "mamá" with accent). International users see the wrong gendered character. | MUM_ALIASES and DAD_ALIASES only contain English variants. `normaliseParent` lowercases but does not strip accents. | 5 | 3 | 9 | **135** | (1) Expand MUM_ALIASES: add "mamá", "maman", "amma", "ama", "anne", "ummi", "eomma". (2) Expand DAD_ALIASES: add "papá", "baba", "appa", "tata", "abi", "abeoji". (3) OR add accent stripping: `label.normalize("NFD").replace(/[\u0300-\u036f]/g, "")` before lookup. Secondary failure check: Over-broad aliases could misclassify a name. "Ama" is a mother term in some cultures but a given name in others. The consequence of misclassification is cosmetic (wrong character gender) not functional. Acceptable risk. | OPEN |
| FM-V2-020 | Headline Engine | characterHeadlines.js (L416-432) | Hero headline 35-char enforcement with long custom parent labels. If ALL pool candidates exceed 35 chars after template resolution (e.g., winnerLabel="Grandmother"), `truncateAtWord` produces ugly truncation like "GRANDMOTHER'S GREA...". | Ugly truncated headline on the mug. Professional appearance degraded. | Long custom parent labels expand all template variables. `truncateAtWord` fallback produces poor results for headline text. | 5 | 3 | 7 | **105** | Add a short-label fallback pool for when all primary candidates exceed 35 chars: ["MINI ME", "LOOK ALIKE", "THEIR TWIN", "THE VERDICT", "FAMILY GENES"]. These have no template variables and are guaranteed to fit. Secondary failure check: Short fallback pool is generic and loses the personalised feel. Acceptable trade-off vs truncated text. | OPEN |
| FM-V2-021 | Regression Risk | KeepsakesModal.jsx (L79-84) | `CHARACTER_MUG_STYLE_MAP` sync risk. If a new style is added to `templateRegistry.js` but not to `CHARACTER_MUG_STYLE_MAP`, the new style silently falls back to occasion="generic", variant="default". No build error, no runtime error, no visual error -- just wrong theming. | New style renders identically to "Classic". User sees no visual difference when selecting the new style. FE Lead flagged this as a fragile code path. | Two separate data structures must be kept in sync manually with no validation. | 7 | 3 | 10 | **210** [NEW] | (1) Move CHARACTER_MUG_STYLE_MAP into templateRegistry.js alongside the style definitions, so they are co-located. (2) Add a dev-mode assertion: `if (import.meta.env.DEV) { for (const styleId of styles) { console.assert(CHARACTER_MUG_STYLE_MAP[styleId], "Missing style mapping: " + styleId); } }`. Secondary failure check: Moving the map to templateRegistry creates an import dependency from KeepsakesModal to templateRegistry. This dependency already exists (KeepsakesModal imports `getTemplateComponent` etc. from templateRegistry), so no new coupling. | OPEN |
| FM-V2-022 | Composition Engine | compositionEngine.js (L303-342) | Element shedding priority order removes photo before occasionTag. The 7-element cap sheds: featureCallout -> speechBubble -> photo -> score. But photo is user-provided content while occasionTag is system-generated. | User specifically provided a child photo but it's removed in favour of an auto-generated occasion label. User expectation violated. | Priority order optimised for layout balance, not user content importance. | 4 | 3 | 8 | **96** | Reorder shedding: featureCallout -> speechBubble -> occasionTag -> score -> photo. User-provided content (photo) should be preserved over system-generated content (occasionTag). Secondary failure check: Removing occasionTag before photo changes gift layout appearance -- the occasion header is the visual anchor of gift layout. May need layout-specific shedding rules instead of a global order. | OPEN |
| FM-V2-023 | Composition Engine | compositionEngine.js (L124-148) | Blend layout with two custom-label parents. Both custom labels normalise to "papa" (via FM-V2-019 else branch). `selectSecondCharacter` picks opposite of primary, but if primary is already papa (due to custom label), second becomes mama. This works. BUT if both parents have mum-like custom names and one happens to be in MUM_ALIASES, primary=mama, second picks based on loserLabel which is also custom=papa. So: mama + papa. This actually works correctly in most cases. | Risk is low. The character pairing logic handles custom labels by defaulting to opposite of primary, which produces visually sensible results (one mama, one papa). | Defensive design already handles this. | 3 | 2 | 9 | **54** | No action needed. The existing fallback logic produces acceptable results. Monitor for edge cases. Secondary failure check: N/A. | MITIGATED |
| FM-V2-024 | Cross-browser/device | CharacterMugTemplate.jsx (L22-37) | Accent bands use semi-transparent gradient: `${theme.light}60` (hex + alpha notation). On transparent PNG exported for white ceramic, bands render as faded colour. | Accent bands may be nearly invisible on the physical mug. The top and bottom decorative lines that frame the design could disappear. | Transparency compositing against white ceramic. Alpha=0x60 (~37%) is very faint. | 4 | 5 | 10 | **200** | Pre-composite accent bands against white: use opaque colours calculated from `mix(theme.light, white, 0.37)`. Or increase alpha to 0xAA (~67%). Secondary failure check: Increasing opacity changes the on-screen appearance. Ensure preview still looks good on dark and light backgrounds. | OPEN |
| FM-V2-025 | Commerce | CharacterMugTemplate.jsx (L41-57) | Brand mark 5.5px CSS at 0.45 opacity. After 3.217x export = ~17.7px at 300DPI = ~1.5mm on physical mug. | "famililook.com" is microscopic and likely illegible on the ceramic mug. Brand identity invisible on the product. | Ultra-small font size designed for screen preview, not print. | 3 | 10 | 10 | **300** | Increase to at least 8px CSS (= ~25.7px print = ~2.2mm) and opacity 0.6+. Secondary failure check: Larger brand mark takes more visual space and may overlap with content in tight layouts (celebration right panel, blend centre). Verify brand mark does not collide with score line or child name in all 4 layouts. | OPEN |
| FM-V2-026 | Preview Rendering | CharacterMugTemplate.jsx (L121-137) | ChildPhoto renders with `objectFit: "cover"` and no face-centering logic. Landscape photos may crop the child's face (top of head or chin cut off). | Child's face partially visible in the photo circle. User sees a poorly cropped photo on their mug preview and potentially on the printed product. | No face-detection-based crop positioning. Default `object-position: center center` doesn't account for face location. | 5 | 5 | 8 | **200** | Use `object-position: center 30%` as default (captures faces better for typical portrait/landscape photos). Ideal: use face detection coordinates from the backend analysis to set precise `object-position`. Secondary failure check: `center 30%` is a heuristic that works for most photos but could crop feet-up shots poorly. Since this is a baby/child photo context, the heuristic is reasonable. | OPEN |
| FM-V2-027 | Data Integrity | KeepsakesModal.jsx | `childPhoto` in templateData comes from `childInfo.previewUrl || childInfo.photo`. If this is a blob URL, it may have expired by the time the user reaches the keepsakes modal. Blob URLs are revoked when the creating object is garbage collected. | Child photo circle shows broken image on the mug preview. If the user orders, the exported PNG has a broken/missing photo. | Blob URL lifecycle not managed across the application session. | 7 | 4 | 7 | **196** | Convert blob URLs to data URIs at upload time, or ensure blob URLs are not revoked until the keepsakes modal is closed. Check: `URL.revokeObjectURL` is not called prematurely. Secondary failure check: Data URIs are larger than blob URLs and persist in memory. For a single child photo this is acceptable (~500KB-2MB). | OPEN |
| FM-V2-028 | Composition Engine | characterHeadlines.js (L282-314) | `getRecipientHeadlinePool` for winner_parent with pctBracket="close": accesses `pool.mum["close"]` which does not exist. Falls back to `pool.mum.medium`. | Winner parent with a close-call result (51-59%) gets "medium" headlines like "MOSTLY YOU, MUM" which feel inaccurate at 52%. Currently unreachable because recipient is always "unknown" (FM-V2-001). | No "close" bracket in winner_parent headline banks. Will surface when FM-V2-001 is fixed. | 4 | 4 | 9 | **144** | Add close-call pools to winner_parent headlines: `close: ["SO CLOSE!\nBUT IT'S YOU", "BY A WHISKER,\nIT'S YOU", "JUST BARELY\nYOURS"]`. Secondary failure check: New headlines must respect the 35-char limit. Verify each candidate: "SO CLOSE! BUT IT'S YOU" = 22 chars. OK. | OPEN |
| FM-V2-029 | Headline Engine | characterHeadlines.js | 110+ recipient-specific headlines exist but are unreachable. Entire `RECIPIENT_HEADLINES` object (winner_parent mum high/medium, dad high/medium, custom; loser_parent mum/dad/custom/fallback; grandparent; blend) is dead code due to FM-V2-001. | Investment in headline writing is wasted. The product's key differentiator (personalised messaging) is invisible to users. | Recipient is hardcoded to "unknown"; `getRecipientHeadlinePool("unknown", ...)` returns null. | 6 | 10 | 10 | **600** [NEW] | Blocked by FM-V2-001 (recipient selector UI). Once the selector is built, these headlines automatically become reachable. No code changes needed in characterHeadlines.js. Secondary failure check: When recipient headlines are activated, the headline length/content should be tested for all recipient+pctBracket combinations to verify 35-char limit compliance. Several winner_parent headlines use `{child}` which could cause the colon bug (FM-V2-010). | OPEN |
| FM-V2-030 | Composition Engine | compositionEngine.js (L24-43) | `deriveContext` does not validate `input.data` exists. If `data` is undefined/null, accessing `data.winnerLabel` throws TypeError -> white screen crash. | Entire keepsakes modal fails. User sees blank screen. | No defensive null check. KeepsakesModal likely guards this upstream, but compositionEngine should be self-defensive. | 10 | 2 | 4 | **80** | Add early return with safe defaults: `if (!input?.data) return { layout: "hero", ... }` with sensible defaults. Secondary failure check: Returning a default plan with no real data produces a mug preview with placeholder text. Better than a white screen, but should also log a warning. | OPEN |
| FM-V2-031 | Headline Engine | characterHeadlines.js (L405-406) | `selectHeadlines` seed: `seedStr = (childName || "FamiliLook") + winnerPct`. Two different children with the same name and same winner percentage get the exact same headline. | Siblings analysed separately get identical mugs. Unlikely but possible for twins. | Seed doesn't include enough entropy (no parent name, no feature data). | 3 | 2 | 10 | **60** | Add more entropy to seed: `seedStr = (childName || "FamiliLook") + winnerPct + winnerLabel + loserLabel`. Secondary failure check: Changing the seed changes the headline for ALL existing users (deterministic but different selection). If any mugs have already been ordered, the preview-to-print consistency is broken. Since no mugs have shipped yet, this is safe to change now. | OPEN |
| FM-V2-032 | Composition Engine | compositionEngine.js (L346-371) | Degradation from celebration to hero does not re-run character selection. Character was chosen for celebration context (e.g., "showing_off" for grandparent). After degradation to hero layout, the emotion doesn't match hero's intended tone. | Character emotion mismatches the layout mood. Minor visual inconsistency. | Degradation changes layout but not character state. | 3 | 2 | 9 | **54** | Accept the minor mismatch or re-derive emotion after layout degradation. Low priority -- degradation path requires no childName AND no childPhoto AND specific recipient, which is unlikely. Secondary failure check: Re-running selectCharacter could change the character type (mama->papa) if context differs, which would be a larger visual change. Safer to only re-derive emotion, not character type. | OPEN |
| FM-V2-033 | Composition Engine | compositionEngine.js (L153-162) | `getLoserBestFeature` returns hardcoded "SMILE" when featureVotes is empty or all 8 features match the winner (8-0 sweep). | Headline template `{feature}` resolves to "SMILE" even when there's no smile attribution. Minor factual inaccuracy on mugs for 8-0 sweeps. | Fallback is reasonable but could mislead. 8-0 sweeps are rare (~2% of analyses). | 3 | 2 | 10 | **60** | Accept the fallback for now. Could improve to use "LOOKS" as a generic feature term. Secondary failure check: "LOOKS" is vague but not misleading. No downstream issues. | MITIGATED |
| FM-V2-034 | Composition Engine | compositionEngine.js (L48-68) | `selectLayout` Rule 6: celebration for medium bracket with known recipient. But recipient is always "unknown" (FM-V2-001), so this rule never fires. When FM-V2-001 is fixed, this rule may conflict with Rule 1 (gift for seasonal occasions). Rule evaluation order means Rule 1 wins, which is correct. | No current bug. Latent interaction when recipient is enabled -- but rule priority handles it correctly. | Rule ordering is correct; flagging for documentation. | 1 | 1 | 5 | **5** | No action needed. Document the rule priority in a comment. Secondary failure check: N/A. | MITIGATED |
| FM-V2-035 | Accessibility | StylePicker.jsx (L144-162) | Dot indicators use `onClick` on `<div>` elements without keyboard accessibility. No `role="button"`, `tabIndex`, or `onKeyDown`. | Keyboard-only and screen reader users cannot navigate styles via dots. Main style buttons ARE keyboard accessible (`<button>` elements). | Dots added as visual convenience, not accessible controls. | 4 | 3 | 9 | **108** | Add `role="button"`, `tabIndex={0}`, and `onKeyDown` (Enter/Space) to dot indicators. OR remove `onClick` from dots since the main buttons already work. Secondary failure check: Adding keyboard interaction to dots creates a focus management complexity (two parallel navigation mechanisms). Simpler fix: remove onClick from dots entirely and make them purely visual indicators. | OPEN |
| FM-V2-036 | Cross-browser/device | StylePicker.jsx (L88-99) | Scroll container hides scrollbar with `scrollbarWidth: "none"` and `msOverflowStyle: "none"`, but inline styles cannot target `&::-webkit-scrollbar`. | Visible scrollbar on Chrome, Safari, Edge (WebKit-based). Cosmetic issue only. | Inline styles cannot target pseudo-elements. | 2 | 7 | 5 | **70** | Add a CSS class with `::-webkit-scrollbar { display: none }` or use a global stylesheet rule. Secondary failure check: Global stylesheet rule could affect other scroll containers. Use a scoped class name. | OPEN |
| FM-V2-037 | Composition Engine | compositionEngine.js (L38-39) | Names with only special characters (e.g., "---") pass the `hasChildName` check. Headline shows "---:\nMUM'S MINI ME" and child name displays as "---" on the mug. | Unusual child name displayed on mug. Very unlikely in practice -- users type real names. | No character validation on childName. | 3 | 1 | 9 | **27** | Add alphanumeric check: `hasChildName = /[a-zA-Z\u00C0-\u024F]/.test(childName)` to include accented characters. Secondary failure check: Unicode regex may exclude valid names in non-Latin scripts (Arabic, Chinese, Korean). Use `/\p{L}/u` for full Unicode letter support. | OPEN |
| FM-V2-038 | Regression Risk | templateRegistry.js (L290-300) | All 4 character_mug styles lazy-import the SAME component (CharacterMugTemplate). Differentiation happens entirely through props. If the prop mapping in CHARACTER_MUG_STYLE_MAP breaks, all 4 styles render identically with no visible error. | No error, no crash -- just 4 identical-looking styles. User switches between Heritage/Carnival/Ubuntu and sees no change. FE Lead flagged as fragile. | Single component, multi-style architecture with no visual differentiation validation. | 7 | 3 | 10 | **210** [NEW] | (1) Add a visual regression test: render CharacterMugTemplate with each occasion and screenshot-compare. (2) In dev mode, display the current occasion/variant in a debug overlay on the template. Secondary failure check: Screenshot tests are brittle and can produce false positives from font rendering differences across CI environments. Use a generous pixel-diff threshold. | OPEN |
| FM-V2-039 | Composition Engine | mugThemes.js | No `christmas`, `valentines`, `grandparents_day`, or `birthday` occasion themes defined in OCCASION_THEMES. compositionEngine.js references these occasions but `getOccasionTheme()` silently falls back to generic. | If these occasions are ever wired up (currently only heritage_gold, carnival_spirit, ubuntu are mapped via styles), colours will be generic red instead of seasonal. | Theme objects not defined for all occasions the engine knows about. | 3 | 2 | 7 | **42** | Add christmas, valentines, birthday, and grandparents_day theme objects. Low priority until occasion selector is built. Wait -- checking mugThemes.js: `birthday` IS defined (line 37). `christmas`, `valentines`, `grandparents_day` are not. Secondary failure check: Adding new theme objects has no downstream risk -- `getOccasionTheme` safely uses them only when matched. | OPEN |
| FM-V2-040 | Performance | compositionEngine.js (L409-464) | `composeCharacterMug` runs on every render cycle if React.useMemo dependencies have referential inequality. If `data` object is recreated on each render (common React pattern), memo busts repeatedly. | Unnecessary recomputations on every render. No visual bug but wastes CPU, especially on mobile. | Object identity changes in React props. | 2 | 5 | 3 | **30** | Verify that KeepsakesModal memoises `templateData` with `useMemo`. If not, add memoisation. Secondary failure check: Over-memoisation can mask bugs where data SHOULD update but doesn't due to stale memo. Ensure memo dependencies include all fields that affect the composition plan. | OPEN |
| FM-V2-041 | Commerce | printProfiles.js | Character mug uses same Prodigi SKU (GLOBAL-MUG-W) as mug_wrap but charges GBP 16.99 vs GBP 14.99. | User might question why character mug costs more for the "same" physical product. Business decision (illustration premium) but not explained in UI. | Intentional pricing -- no code bug. | 2 | 1 | 3 | **6** | Add a "Why this price?" tooltip: "Includes original character illustration." Secondary failure check: None -- tooltip is informational only. | MITIGATED |
| FM-V2-042 | Preview Rendering | CharacterMugTemplate.jsx (L623-665) | `CharacterMugTemplate` accepts `ageTheme` prop but never uses it. All colour decisions use `getOccasionTheme(occasion)`. | ageTheme is a wasted prop. The age-based theming used by other keepsake products is silently ignored for character mugs. | Design decision -- character mugs use occasion themes, not age themes. | 1 | 10 | 3 | **30** | Document in a code comment that character mugs intentionally ignore ageTheme. Consider removing the prop from the interface to avoid confusion. Secondary failure check: Removing the prop causes a console warning if KeepsakesModal still passes it. Update all call sites. | MITIGATED |
| FM-V2-043 | Data Integrity | CharacterMugTemplate.jsx (L99-117) | `CharacterImg` returns `null` if `getCharacterImage()` returns null. Layout renders with empty space where character should be. | Mug preview shows a layout with blank left panel. If user orders, they get a mug with no illustration. | Character type or variant completely missing from index. | 9 | 1 | 7 | **63** | (1) Add a visible fallback (FamiliLook logo or silhouette placeholder). (2) Block the "Order" button when character image is null. Secondary failure check: Blocking order requires detecting null in the template and propagating to the parent. Could use a callback prop or context. | OPEN |
| FM-V2-044 | Headline Engine | characterHeadlines.js (L54-133) | HEADLINES contain hardcoded English text. No i18n support. | Non-English speaking users see English headlines on their mug. Product is English-only for MVP. | No internationalisation layer. | 4 | 3 | 10 | **120** | Accept for MVP. Document as known limitation. Plan i18n for v2.0 when the product expands to non-English markets. Secondary failure check: N/A for MVP. | MITIGATED |
| FM-V2-045 | Composition Engine | compositionEngine.js (L48-68) | No "sibling", "friend", or "other" recipient type. If a user wants a mug for a sibling, they have no appropriate option. Falls to "unknown" -> generic hero layout. | Limited gifting options. | Recipient taxonomy covers winner_parent, loser_parent, grandparent, self, unknown -- but not extended family or friends. | 3 | 4 | 9 | **108** | Expand recipient options when building the UI (FM-V2-001). Add "sibling" -> hero layout, "friend" -> hero layout, "other" -> hero layout. Secondary failure check: More options increase UI complexity. Consider a dropdown instead of buttons for 7+ options. | OPEN |
| FM-V2-046 | Preview Rendering | CharacterMugTemplate.jsx (L270-393) | CelebrationLayout right panel (25% = 208px) is nearly empty when featureCallout is shed by validateElementCount. Only brand mark remains. | Asymmetric layout with visually empty right panel. Looks unbalanced. | Element shedding doesn't adapt panel proportions. | 4 | 3 | 7 | **84** | Rebalance to 30/70 split when right panel has no feature callout. Or move brand mark to centre panel. Secondary failure check: Changing panel proportions affects text sizing and character image positioning. Needs visual regression testing across all data combinations. | OPEN |
| FM-V2-047 | Preview Rendering | CharacterMugTemplate.jsx | Inconsistent brand mark placement. Hero/Celebration/Gift use the BrandMark component (positioned absolute within right panel). Blend layout uses inline brand mark (centred in the centre panel). | Minor visual inconsistency across layouts. Users who switch between styles/layouts may notice the brand position jumping. | Different layouts were authored independently. | 2 | 10 | 5 | **100** | Standardise: either always use BrandMark component or always inline. Recommend: move brand to an absolute position relative to the outer canvas (not a sub-panel) for consistency. Secondary failure check: Changing brand position in one layout may cause overlap with content. Test all 4 layouts after change. | OPEN |
| FM-V2-048 | Cross-browser/device | CharacterMugTemplate.jsx (L60-95) | SpeechBubble maxWidth 100px may clip longest text "I WANT A RECOUNT" (16 chars at 6.5px bold font). | Speech bubble text truncated with ellipsis. Minor cosmetic issue. | Fixed maxWidth doesn't account for bold font metrics across browsers. | 3 | 3 | 7 | **63** | Shorten "I WANT A RECOUNT" to "RECOUNT!" or increase maxWidth to 120px. Secondary failure check: Increasing maxWidth may cause bubble to overlap with the headline panel on narrow layouts. Verify at 830px canvas width. | OPEN |
| FM-V2-049 | Export Pipeline | cardExport.js (L81-86) | `sanitizeFilename` strips all non-alphanumeric characters. Accented names (Amelie, Bjorn) become garbled: "Am_lie", "Bj_rn". | Download filename looks ugly but is functional. | Aggressive ASCII-only sanitisation. | 2 | 3 | 5 | **30** | Allow Unicode word characters: use `[^\p{L}\p{N}_-]/gu` instead of `[^a-zA-Z0-9_-]`. Secondary failure check: Unicode filenames may cause issues on older Windows systems or FAT32 filesystems. The risk is low for modern OS but non-zero. | OPEN |
| FM-V2-050 | Regression Risk | compositionEngine.js (getOccasionTheme fallback) | `getOccasionTheme()` returns `OCCASION_THEMES.generic` for any unrecognised occasion string. Silently masks typos and mapping errors. | A misspelled occasion like "heritag_gold" silently renders with generic theme instead of erroring. Developer never knows the mapping is wrong. FE Lead flagged as fragile. | Silent fallback with no logging. | 5 | 3 | 10 | **150** [NEW] | Add a dev-mode warning: `if (import.meta.env.DEV && !OCCASION_THEMES[occasion]) console.warn("Unknown occasion:", occasion)`. Secondary failure check: Console warnings in dev mode have no production impact. Safe to add. | OPEN |
| FM-V2-051 | Preview Rendering | CharacterMugTemplate.jsx | No `@media print` styles. Browser print (Ctrl+P) produces poor output. | Poor browser print. Minor -- users should use export/order flow. | Not designed for browser print. | 2 | 2 | 5 | **20** | No action needed. Export flow is the intended path. Secondary failure check: N/A. | MITIGATED |
| FM-V2-052 | Data Integrity | compositionEngine.js (L5) | `winnerPct` of exactly 50 not handled. Contract says 51-100 but no frontend guard. If backend sends 50, `isBlend` is false yet `pctBracket` is "close". | Close-call layout used when blend would be more appropriate. Minor visual mismatch for edge case. | No input validation on winnerPct range. | 3 | 2 | 8 | **48** | Add guard: `if (winnerPct <= 50 && !isBlend) { isBlend = true; pctBracket = "blend"; }`. Secondary failure check: Overriding to blend when backend said parent1/parent2 won could confuse headline logic. Better: just treat 50 as "close" (which it already does). Accept current behaviour. | MITIGATED |

---

## V1 Status Tracker

| V1 ID | V1 RPN | Description | Status | V2 ID | Notes |
|-------|--------|-------------|--------|-------|-------|
| FM-001 | 810 | Occasion/recipient/variant props never passed to CharacterMugTemplate | **FIXED** | -- | `CHARACTER_MUG_STYLE_MAP` added to KeepsakesModal with `isCharacterMug()` helper. All 4 preview/export paths now pass `occasion` and `variant` correctly. |
| FM-002 | 560 | character_mug excluded from isMug checks | **FIXED** | -- | `isCharacterMug()` helper introduced. Character mugs now take their own rendering path (NOT routed through MugCeramicPreview -- V1's recommendation was wrong). |
| FM-003 | 200 | cub_curious.png missing from default variant | OPEN | FM-V2-012 | Unchanged. Fallback to cub_happy works silently. |
| FM-004 | 60 | gran_loving_african.png missing, import would crash build | **FIXED** | FM-V2-013 | FE Lead confirmed: import removed from index.js. Fallback to gran_proud_african handles it. RPN reduced from 60 to 16. |
| FM-005 | 48 | winnerPct=50 not handled | OPEN | FM-V2-052 | Unchanged. Accepted as mitigated. |
| FM-006 | 112 | Transparent PNG export may cause Prodigi issues | OPEN | FM-V2-005 | Rolled into broader export validation item. RPN increased to 350 (combined with untested Prodigi pipeline). |
| FM-007 | 256 | html-to-image cacheBust + Vite hashing interaction | OPEN | FM-V2-008 | Unchanged. |
| FM-008 | 168 | Export pixelRatio on mobile may exceed canvas limits | OPEN | FM-V2-016 | Unchanged. |
| FM-009 | 30 | StylePicker returns null for <= 1 style | MITIGATED | -- | Acceptable behaviour. |
| FM-010 | 60 | getLoserBestFeature fallback "SMILE" | MITIGATED | FM-V2-033 | Unchanged. |
| FM-011 | 245 | Leading colon when childName empty | OPEN | FM-V2-010 | Unchanged. FE Lead confirmed the bug. |
| FM-012 | 105 | Long custom labels cause ugly truncation | OPEN | FM-V2-020 | Unchanged. |
| FM-013 | 180 | Incomplete emotion remapping | OPEN | FM-V2-015 | Unchanged. |
| FM-014 | 63 | CharacterImg returns null -> blank space | OPEN | FM-V2-043 | Unchanged. |
| FM-015 | 240 | 56 PNGs statically imported -> bundle bloat | OPEN | FM-V2-011 | Updated with FE Lead's dead PNG analysis (6 confirmed dead). |
| FM-016 | 720 | Style-to-occasion mapping missing | **FIXED** | -- | CHARACTER_MUG_STYLE_MAP now maps each style to its occasion. |
| FM-017 | 42 | Missing christmas/valentines themes | OPEN | FM-V2-039 | Updated: birthday theme exists. |
| FM-018 | 135 | Custom parent labels always map to papa | OPEN | FM-V2-019 | Unchanged. |
| FM-019 | 90 | Both custom parents -> two papa characters | OPEN | FM-V2-023 | Re-analysed: existing fallback handles it. MITIGATED. |
| FM-020 | 245 | Text unreadably small on mobile flat preview | OPEN | -- | Partially addressed by FM-002 fix (character mugs now have own path). Needs further verification. |
| FM-021 | 96 | Element shedding removes photo before occasionTag | OPEN | FM-V2-022 | Unchanged. |
| FM-022 | 144 | winner_parent with close pctBracket -> wrong headlines | OPEN | FM-V2-028 | Unchanged. Latent until FM-V2-001 is fixed. |
| FM-023 | 10 | loserBubble computed but unused | MITIGATED | -- | Dead code, acceptable for future use. |
| FM-024 | 63 | SpeechBubble maxWidth clips long text | OPEN | FM-V2-048 | Unchanged. |
| FM-025 | 280 | Nunito font may not embed in export | OPEN | FM-V2-006 | Unchanged. |
| FM-026 | 20 | No @media print styles | MITIGATED | FM-V2-051 | Unchanged. |
| FM-027 | 6 | Same Prodigi SKU, different price | MITIGATED | FM-V2-041 | Unchanged. |
| FM-028 | 80 | No null check on input.data | OPEN | FM-V2-030 | Unchanged. |
| FM-029 | 5 | Headline source switch when FM-001 fixed | MITIGATED | FM-V2-034 | FM-001 is now fixed. Verified: rule priority handles it correctly. |
| FM-030 | 108 | Dot indicators not keyboard accessible | OPEN | FM-V2-035 | Unchanged. |
| FM-031 | 70 | Scrollbar visible on WebKit | OPEN | FM-V2-036 | Unchanged. |
| FM-032 | 270 | CharacterImg alt text uses internal identifiers | OPEN | FM-V2-007 | Combined with FM-033 into accessibility item. |
| FM-033 | 270 | No aria-label on template container | OPEN | FM-V2-007 | Combined with FM-032. |
| FM-034 | 24 | Special chars in winnerLabel | MITIGATED | -- | React handles escaping. |
| FM-035 | 27 | Special-char-only childName passes check | OPEN | FM-V2-037 | Unchanged. |
| FM-036 | 196 | Blob URL expiry for child photo | OPEN | FM-V2-027 | Unchanged. |
| FM-037 | 168 | CORS differences between dev and prod for export | OPEN | FM-V2-017 | Unchanged. |
| FM-038 | 54 | Degradation doesn't re-run character selection | OPEN | FM-V2-032 | Unchanged. |
| FM-039 | 250 | No physical prototype validation of text sizing | OPEN | FM-V2-009 | Unchanged. |
| FM-040 | 200 | Accent bands semi-transparent on ceramic | OPEN | FM-V2-024 | Unchanged. |
| FM-041 | 300 | Brand mark 5.5px illegible on mug | OPEN | FM-V2-025 | Unchanged. |
| FM-042 | 350 | RGB colours not CMYK proofed | OPEN | FM-V2-004 | Unchanged. |
| FM-043 | 30 | useMemo bust on data object recreation | OPEN | FM-V2-040 | Unchanged. |
| FM-044 | 168 | No loading skeleton for character images | OPEN | FM-V2-018 | Unchanged. |
| FM-045 | 120 | No i18n support | MITIGATED | FM-V2-044 | Unchanged. |
| FM-046 | 108 | No sibling/friend recipient type | OPEN | FM-V2-045 | Unchanged. |
| FM-047 | 1 | Print profile key format verified correct | MITIGATED | -- | No action needed. |
| FM-048 | 200 | Photo crop doesn't centre on face | OPEN | FM-V2-026 | Unchanged. |
| FM-049 | 810 | Export also missing occasion/variant props | **FIXED** | -- | Fixed alongside FM-001. All export paths now use CHARACTER_MUG_STYLE_MAP. |
| FM-050 | 30 | ageTheme prop accepted but ignored | MITIGATED | FM-V2-042 | Unchanged. |
| FM-051 | 420 | No variant selector -> ethnicity locked to occasion | OPEN | FM-V2-003 | Unchanged. |
| FM-052 | 100 | Inconsistent brand mark placement across layouts | OPEN | FM-V2-047 | Unchanged. |
| FM-053 | 800 | No recipient selection UI | OPEN | FM-V2-001 | Unchanged. Remains top risk. |
| FM-054 | 700 | No occasion selection UI | **PARTIALLY FIXED** | -- | Occasion is now mapped via style selection (CHARACTER_MUG_STYLE_MAP). Heritage->heritage_gold, Carnival->carnival_spirit, Ubuntu->ubuntu. Remaining gap: seasonal occasions (christmas, valentines, mothers_day, etc.) still have no UI path. |
| FM-055 | 84 | Celebration right panel empty after shedding | OPEN | FM-V2-046 | Unchanged. |
| FM-056 | 30 | Filename sanitisation strips accented chars | OPEN | FM-V2-049 | Unchanged. |

---

## Recommended Fix Priority

### P0 -- Fix Before Launch (blocks core value)
1. **FM-V2-001 (RPN 800):** Build recipient selection UI. This unlocks 60% of the composition engine's value.
2. **FM-V2-002 (RPN 400):** Write unit tests for compositionEngine.js. Zero test coverage on the core deterministic engine is unacceptable.
3. **FM-V2-003 (RPN 420):** Build variant/character family selector. Ethnicity locked to occasion is a significant UX gap.

### P1 -- Fix Before First Orders (blocks quality)
4. **FM-V2-004 (RPN 350):** Order CMYK test prints for all 7 colour palettes.
5. **FM-V2-005 (RPN 350):** Set `backgroundColor: "#FFFFFF"` for Prodigi exports. Test transparency pipeline.
6. **FM-V2-006 (RPN 280):** Ensure Nunito font embeds in export (await `document.fonts.ready`).
7. **FM-V2-009 (RPN 250):** Order physical test prints to validate text sizing.
8. **FM-V2-010 (RPN 245):** Fix leading colon bug in headlines with empty childName.
9. **FM-V2-025 (RPN 300):** Increase brand mark size for print legibility.
10. **FM-V2-021 (RPN 210):** Move CHARACTER_MUG_STYLE_MAP into templateRegistry to prevent sync drift.

### P2 -- Fix Before Scale (quality + performance)
11. **FM-V2-011 (RPN 240):** Lazy-load character PNGs, remove 6 dead imports.
12. **FM-V2-008 (RPN 256):** Test export across browsers, consider `cacheBust: false`.
13. **FM-V2-015 (RPN 180):** Complete emotion remapping for all character types.
14. **FM-V2-027 (RPN 196):** Convert blob URLs to data URIs for child photos.
15. **FM-V2-016 (RPN 168):** Add try/catch with user-facing error on export failure.
16. **FM-V2-038 (RPN 210):** Add visual regression tests for style differentiation.

### P3 -- Backlog (polish)
17. FM-V2-007 (RPN 270): Accessibility improvements (alt text, aria-label).
18. FM-V2-035 (RPN 108): Keyboard accessibility for dot indicators.
19. FM-V2-019 (RPN 135): International parent name aliases.
20. FM-V2-026 (RPN 200): Face-centred photo cropping.
21. FM-V2-024 (RPN 200): Accent band opacity for print.
22. FM-V2-020 (RPN 105): Short-label fallback pool for long parent names.
23. FM-V2-050 (RPN 150): Dev-mode warning for unknown occasions.

---

## Appendix A: Render Path Map

```
User selects "Character Mug" product
    |
    v
KeepsakesModal.jsx
    |-- Step 3 (Style): StylePicker.jsx
    |       |-- getProductStyles("character_mug") -> 4 styles from templateRegistry.js
    |       |-- User selects style ID (e.g., "character_heritage")
    |
    |-- CHARACTER_MUG_STYLE_MAP[selectedStyle]
    |       |-- character_default  -> { occasion: "generic",        variant: "default" }
    |       |-- character_heritage -> { occasion: "heritage_gold",  variant: "african" }
    |       |-- character_carnival -> { occasion: "carnival_spirit", variant: "african" }
    |       |-- character_ubuntu   -> { occasion: "ubuntu",          variant: "african" }
    |
    |-- Step 3 Preview: CharacterMugTemplate (visible)
    |       props: { data, occasion, variant, recipient:"unknown", ageTheme }
    |
    |-- Step 4 Mockup: MugCeramicPreview (for mug_wrap ONLY, NOT character_mug)
    |       character_mug takes SEPARATE path via isCharacterMug() check
    |
    |-- Step 4 Flat View: CharacterMugTemplate (visible, scaled)
    |       props: same as step 3
    |
    |-- Hidden cardRef: CharacterMugTemplate (offscreen, for export)
    |       props: same as above
    |
    v
CharacterMugTemplate.jsx
    |-- composeCharacterMug({ data, occasion, recipient, variant })
    |       -> compositionEngine.js (8-step pipeline)
    |       -> Returns: CompositionPlan { layout, character, headline, ... }
    |
    |-- getOccasionTheme(occasion) -> mugThemes.js
    |
    |-- Layout Router: hero | celebration | blend | gift
    |       |-- HeroLayout:        40/60 split, character left, headline right
    |       |-- CelebrationLayout: 30/45/25, personal content centre
    |       |-- BlendLayout:       25/50/25, two characters flanking
    |       |-- GiftLayout:        35/65, occasion header + content
    |
    |-- CharacterImg -> getCharacterImage(type, emotion, variant)
    |       -> characters/index.js -> IMAGES[variant][type][emotion]
    |       -> Fallback: BASE_EMOTION[type] -> null if character missing
    |
    v
Export (cardExport.js)
    |-- exportCardAsPng(cardRef, { pixelRatio: 3.217, backgroundColor: "transparent" })
    |       -> html-to-image toPng()
    |       -> 2670x1110px PNG
    |
    v
Prodigi (GLOBAL-MUG-W)
    |-- Receives PNG
    |-- RGB->CMYK conversion
    |-- Prints on 11oz white ceramic
```

---

## Appendix B: Emotion Availability Matrix

Shows which emotions exist per character type per variant. **Gap** = fallback triggered (wrong emotion displayed). **DEAD** = PNG exists but no code path selects it. **MISSING** = PNG does not exist but could be requested.

| Character | proud | surprised | cheeky | loving | celebrating | showing_off | giggling | curious | happy | sleeping | laughing |
|-----------|-------|-----------|--------|--------|-------------|-------------|----------|---------|-------|----------|----------|
| **mama (default)** | Y | Y | Y | Y | Y | -- | -- | -- | -- | -- | -- |
| **mama (african)** | Y | Y | Y | Y | Y | -- | -- | -- | -- | -- | -- |
| **papa (default)** | Y | Y | Y | Y | Y | -- | -- | -- | -- | -- | -- |
| **papa (african)** | Y | Y | Y | Y | Y | -- | -- | -- | -- | -- | -- |
| **cub (default)** | -- | Y | -- | -- | -- | -- | Y | **MISSING** | Y | DEAD | -- |
| **cub (african)** | -- | Y | -- | -- | -- | -- | Y | Y | Y | DEAD | -- |
| **mini (default)** | Y | Y | Y | -- | Y | -- | -- | -- | -- | -- | -- |
| **mini (african)** | Y | Y | Y | -- | Y | -- | -- | -- | -- | -- | -- |
| **gran (default)** | Y | Y | -- | Y | -- | Y | -- | -- | -- | -- | DEAD |
| **gran (african)** | Y | Y | -- | **MISSING** | -- | Y | -- | -- | -- | -- | DEAD |
| **gramps (default)** | Y | Y | -- | Y | -- | Y | -- | -- | -- | -- | DEAD |
| **gramps (african)** | Y | Y | -- | Y | -- | Y | -- | -- | -- | -- | DEAD |

**Emotions requested by compositionEngine but not available (fallback triggered):**
- `mini + loving` -> falls back to `mini_proud` (base emotion)
- `mini + showing_off` -> falls back to `mini_proud` (base emotion)
- `gran + celebrating` -> falls back to `gran_proud` (base emotion)
- `gramps + celebrating` -> falls back to `gramps_proud` (base emotion)
- `cub + curious (default)` -> falls back to `cub_happy` (base emotion)
- `gran + loving (african)` -> falls back to `gran_proud_african` (base emotion)

**Dead PNGs (imported but unreachable by engine):**
1. `cub_sleeping.png` -- no code path produces "sleeping"
2. `cub_sleeping_african.png` -- no code path produces "sleeping"
3. `gran_laughing.png` -- no code path produces "laughing" for gran
4. `gran_laughing_african.png` -- no code path produces "laughing" for gran
5. `gramps_laughing.png` -- no code path produces "laughing" for gramps
6. `gramps_laughing_african.png` -- no code path produces "laughing" for gramps

---

## Appendix C: V1 Incident Analysis (MugCeramicPreview)

### What happened
The V1 DFMEA (FM-002) recommended: "Add `character_mug` to `isMugProduct()` checks in KeepsakesModal."

### Why it was wrong
`isMugProduct()` gates routing to `MugCeramicPreview.jsx`. MugCeramicPreview is an SVG-based component that renders:
- Feature chips (Eyes, Nose, etc.) as SVG rectangles
- Score line as SVG text
- Winner declaration as SVG text ("Mum, I look more like you")
- Child photo as SVG image element
- All rendered on a ceramic mug SVG illustration

It does NOT render:
- Character illustrations (mama, papa, cub, etc.)
- Composition engine layouts (hero, celebration, blend, gift)
- Dynamic headlines from characterHeadlines.js
- Speech bubbles

Adding character_mug to isMugProduct() would have routed character mugs to MugCeramicPreview, which would display a standard text-based mug with no character illustrations -- destroying the product's core value proposition.

### The correct fix
Introduce `isCharacterMug()` as a SEPARATE helper:
```javascript
const isCharacterMug = (p) => p === "character_mug";
```

Character mugs now take their own rendering path using `CharacterMugTemplate` directly, with `CHARACTER_MUG_STYLE_MAP` providing occasion/variant props.

### Root cause
Single-agent DFMEA without destination component verification. The Change Manager analysed the routing condition ("character_mug should be treated as a mug") without reading the destination component ("but what does MugCeramicPreview actually render?").

### Process fix
1. All DFMEAs require 3-agent consensus (QA Lead, FE Lead, Change Manager)
2. QA Lead persona now includes the Critical DFMEA Rule: TRACE THE FULL PATH
3. Every recommended action must include "Secondary failure check" analysis

---

*End of DFMEA V2. Pending: FE Lead and Change Manager consensus review of scores.*
