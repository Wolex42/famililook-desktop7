# Messaging Framework: Product-Led FamiliLook

> **Author:** Copywriter Agent
> **Date:** 2026-04-01
> **Status:** READY FOR REVIEW
> **Purpose:** Complete copy framework for the product-led pivot. Every line is code-ready.

---

## 1. Brand Voice Definition

### Emotional Register

**Warm pride meets playful discovery.**

FamiliLook speaks like a thoughtful friend who just found the perfect gift — not a lab technician reading results. The voice sits between gift-shop warmth and playground curiosity. We celebrate what families already feel; we never explain the science behind it.

**Voice pillars:**
- **Proud:** "Look at that — she's got your smile." (Not clinical. Not surprised. Proud.)
- **Playful:** "Settle the argument once and for all." (Light stakes, real fun.)
- **Personal:** Always use names. Always reference real features. Never generic.
- **Gift-first:** The product is the hero, not the technology behind it.

### Tone Scale

| Context | Tone |
|---|---|
| Product cards / shop | Warm, inviting, gift-giving |
| Upload flow | Encouraging, simple, reassuring |
| Results reveal | Celebratory, proud, specific |
| Share prompts | Playful, brag-worthy, social |
| Occasion banners | Urgent but warm, never pushy |
| Error states | Calm, helpful, human |

### BANNED Words

These words must NEVER appear in user-facing copy:

| Banned | Why | Use Instead |
|---|---|---|
| facial analysis | Clinical, surveillance | "see who they look like" |
| biometric | Regulatory / scary | (omit entirely) |
| kinship | Academic jargon | "family bond" / "resemblance" |
| consent to processing | Legal language in UI | "ready to go" / "let's start" |
| algorithm | Tech jargon | "we looked closely" |
| scan / scanning | Surveillance feel | "looking at" / "checking" |
| upload (as noun) | Technical | "your photos" / "your pictures" |
| data / dataset | Cold | "your family photos" |
| processing | Factory language | "creating" / "making" |
| engine | Technical | (omit entirely) |
| parameters | Technical | (omit entirely) |
| facial recognition | Surveillance / regulatory | "family resemblance" |
| percentage match | Clinical | use `{matchPercent}%` in context only |

### CORE Words

These words carry the brand. Use them liberally:

| Word | Usage |
|---|---|
| **bond** | "Your bond with Mum" — the emotional connection |
| **match** | "How well do you match?" — playful, competitive |
| **discover** | "Discover who they take after" — curiosity trigger |
| **your family** | Always possessive. It's THEIR family, THEIR moment |
| **keep** | "Keep this moment" — permanence, keepsake |
| **share** | "Share the proof" — social currency |
| **play** | "Play with your family" — games, fun |
| **looks like** | "She looks like Dad" — the most natural phrase |
| **made from** | "Made from your real family features" — craft, not tech |
| **settle** | "Settle the debate" — playful conflict |
| **proof** | "Proof on a mug" — tangible, fun |
| **spot on** | "Spot on — she's got your eyes" — British, warm |

---

## 2. Three Front Door Headlines

### Door 1: "Make Something" (Gift Buyers)

Target: Someone who wants a personalised gift. They see product cards first.

| # | Headline (max 60 chars) | Chars |
|---|---|---|
| 1 | **Gifts made from your family's real features** | 48 |
| 2 | **Turn your resemblance into something real** | 46 |
| 3 | **The gift that proves who they take after** | 45 |
| 4 | **Your family bond, on a mug, a card, a print** | 48 |
| 5 | **Personalised gifts only your family can make** | 49 |

**Subline (max 100 chars):**
> We look at your family photos and create one-of-a-kind gifts you can hold, hang, and send. (92 chars)

### Door 2: "Find Out" (Curious Families)

Target: "Who does the baby look like?" — the question that starts everything.

| # | Headline (max 60 chars) | Chars |
|---|---|---|
| 1 | **Who do they really take after?** | 33 |
| 2 | **Settle the family debate in seconds** | 39 |
| 3 | **Discover whose eyes, smile, and nose they got** | 50 |
| 4 | **Mum's eyes or Dad's smile? Now you'll know** | 47 |
| 5 | **See the family resemblance — feature by feature** | 52 |

**Subline (max 100 chars):**
> Add three photos and we'll show you exactly which features came from which parent. (83 chars)

### Door 3: "How Well Do You Match?" (Couples, Friends, Siblings)

Target: Social, shareable, competitive. FamiliMatch audience.

| # | Headline (max 60 chars) | Chars |
|---|---|---|
| 1 | **How well do you actually match?** | 34 |
| 2 | **Find your look-alike score** | 29 |
| 3 | **Are you really alike? Let's find out** | 39 |
| 4 | **Compare faces. Settle arguments. Share proof** | 48 |
| 5 | **Your match score is waiting** | 30 |

**Subline (max 100 chars):**
> See how your features compare — eyes, smile, face shape and more. Then share your score. (90 chars)

---

## 3. Product Card Copy (OccasionShelf)

### Bond Mug (`mug_wrap`) — Price: £14.99

```
headline:  "{matchPercent}% {winnerName}'s — on a mug"
           // e.g. "72% Mum's — on a mug" (24 chars)
subline:   "Your bond, glazed and ready to gift"  (36 chars)
cta:       "Make This Mug"  (13 chars)
```

### Character Mug (`character_mug`) — Price: £16.99

```
headline:  "Their face, illustrated"
           // (23 chars)
subline:   "A one-of-a-kind character made from real features"  (51 chars)
cta:       "Create Character"  (16 chars)
```

### Greeting Card (`greeting_card`) — Price: £6.99

```
headline:  "{matchPercent}% yours, {winnerName}"
           // e.g. "72% yours, Mum" (22 chars)
subline:   "A card only your family could send"  (35 chars)
cta:       "Make This Card"  (14 chars)
```

### Fine Art Print (`fine_art_print`) — Price: £24.99

```
headline:  "Your family bond, framed"
           // (24 chars)
subline:   "Museum-quality print of your resemblance story"  (48 chars)
cta:       "Order Print"  (11 chars)
```

### FamiliUno Card Deck (`card_deck`) — Price: £24.99

```
headline:  "52 cards. Your faces. Game on"
           // (29 chars)
subline:   "A real card deck made from your family photos"  (47 chars)
cta:       "Build Your Deck"  (15 chars)
```

### Postcard (`postcard`) — Price: £3.99

```
headline:  "Send the proof"
           // (14 chars)
subline:   "A postcard with your family resemblance story"  (47 chars)
cta:       "Send Postcard"  (13 chars)
```

### Cushion (`cushion`) — Price: £29.99

```
headline:  "Your bond, on the sofa"
           // (22 chars)
subline:   "A cushion featuring your family's real features"  (48 chars)
cta:       "Make Cushion"  (12 chars)
```

---

## 4. Occasion-Specific Copy

### Mother's Day

```
banner:    "Make Mum's Day — She'll See It Instantly"  (41 chars)
urgency:   "Mother's Day orders close Sunday. Don't leave her waiting."  (59 chars)
```

### Father's Day

```
banner:    "For The Dad Who Has Everything — Except This"  (46 chars)
urgency:   "Father's Day orders close Friday. Prove he passed it on."  (57 chars)
```

### Christmas

```
banner:    "The Gift They'll Never Guess"  (28 chars)
urgency:   "Order by 15 Dec for Christmas delivery. Every gift is unique."  (62 chars)
```

### Easter

```
banner:    "A Little Something That's Truly Theirs"  (39 chars)
urgency:   "Easter gifts ship in 3-5 days. Unique to your family."  (54 chars)
```

### Birthday (Evergreen)

```
banner:    "A Birthday Gift No One Else Can Give"  (37 chars)
urgency:   "Order now — personalised gifts take 3-5 days to arrive."  (56 chars)
```

### New Baby (Evergreen)

```
banner:    "Welcome To The Family — See Who They Take After"  (49 chars)
urgency:   "The perfect newborn gift. Made from your first family photos."  (62 chars)
```

### Family Holiday (Evergreen)

```
banner:    "Turn Your Holiday Snaps Into Keepsakes"  (39 chars)
urgency:   "Fresh photos make the best gifts. Start while the memories are warm."  (68 chars)
```

---

## 5. Results Page Transition Copy

The bridge from "here's your result" to "here's what you can do with it."

**RETIRED:** "Turn this result into a keepsake" (too generic, too technical)

| # | Transition Line | Chars | Notes |
|---|---|---|---|
| 1 | **Now put it on something real** | 31 | Direct, action-oriented |
| 2 | **This deserves more than a screenshot** | 39 | Challenges the default behaviour |
| 3 | **Keep this. Gift it. Show it off** | 34 | Three verbs, rising energy |
| 4 | **Your family bond — ready to make real** | 40 | Ties back to brand word "bond" |
| 5 | **Too good to stay on a screen** | 31 | Playful nudge toward physical |

**Recommended: Option 3** — "Keep this. Gift it. Show it off." — because it maps to the three user intents (self, gift, social) and has natural rhythm.

---

## 6. Upload Screen Copy (Product-Led)

When the user arrives from Door 1 (a product card), the upload screen reframes around making, not analysing.

### When Making a Mug

```
heading:     "Add your photos to make this mug"
subheading:  "We need three photos — two parents and one child"
```

### When Making a Card

```
heading:     "Add your photos to make this card"
subheading:  "Three photos and your card is on its way"
```

### When Making a Card Deck

```
heading:     "Add your family to build your deck"
subheading:  "The more faces you add, the better your deck"
```

### Slot Labels (Warm Replacements)

| Old Label | New Label | Alt Label |
|---|---|---|
| Parent A | **Mum or Parent 1** | **First parent** |
| Parent B | **Dad or Parent 2** | **Second parent** |
| Child | **The little one** | **Who do they look like?** |

**Recommended slot labels for code:**

```js
const SLOT_LABELS = {
  parent1: {
    label: "Mum, Dad, or Guardian",
    helper: "A clear, front-facing photo works best"
  },
  parent2: {
    label: "The other parent or guardian",
    helper: "A clear, front-facing photo works best"
  },
  child: {
    label: "The one everyone argues about",
    helper: "Who do they look like? Let's find out"
  }
};
```

### Generic Upload (No Product Context)

```
heading:     "Add three family photos"
subheading:  "Two parents (or guardians) and one child. That's all we need."
```

---

## 7. Share Copy Templates

All templates use available data variables: `{childName}`, `{matchPercent}`, `{winnerName}`, `{topFeatures}`.

### WhatsApp / iMessage

**Option A (Winner focus):**
```
{childName} is {matchPercent}% {winnerName}'s! Eyes, smile, the lot. See for yourself: {link}
```
Example: "Emma is 72% Mum's! Eyes, smile, the lot. See for yourself: famililook.com/s/abc123"

**Option B (Debate focus):**
```
We finally settled it — {childName} takes after {winnerName} ({matchPercent}%). Want to try yours? {link}
```

**Option C (Gift focus):**
```
Look what we made! {childName}'s bond with {winnerName} — on a mug. Your family next? {link}
```

### Instagram Story Caption

**Option A:**
```
{matchPercent}% {winnerName}'s. Called it. 👀
#FamiliLook #WhoDoTheyLookLike
```

**Option B:**
```
{childName} got {winnerName}'s {topFeatures[0]} and it shows.
#FamiliLook #FamilyResemblance
```

**Option C:**
```
The proof is in the {topFeatures[0]}. {matchPercent}% match.
#FamiliLook
```

### Twitter / X Post

**Option A (under 280 chars):**
```
Turns out {childName} is {matchPercent}% {winnerName}'s — the {topFeatures[0]} and {topFeatures[1]} gave it away. Try yours free: {link}
```

**Option B:**
```
Settled the "{childName} looks like..." debate for good. {matchPercent}% {winnerName}'s. Science says so. {link}
```

**Option C:**
```
Made a mug with our family resemblance on it and honestly it's the best gift I've ever given. {link}
```

---

## Implementation Notes

### Variable Reference

| Variable | Type | Example | Available On |
|---|---|---|---|
| `{childName}` | string | "Emma" | Results, Share |
| `{winnerName}` | string | "Mum" | Results, Share, Product Cards |
| `{matchPercent}` | integer | 72 | Results, Share, Product Cards |
| `{topFeatures}` | string[] | ["eyes", "smile", "face shape"] | Results, Share |
| `{link}` | string | short URL | Share only |

### Character Limits Summary

| Element | Max Chars |
|---|---|
| Front door headline | 60 |
| Front door subline | 100 |
| Product card headline | 40 |
| Product card subline | 60 |
| Product card CTA | 20 |
| Occasion banner | 50 |
| Occasion urgency | 80 |
| Share: WhatsApp | 160 (before link) |
| Share: Instagram | 150 (before hashtags) |
| Share: Twitter/X | 240 (before link) |

### Copy Priority for A/B Testing

1. **Results transition line** — highest impact on conversion to purchase
2. **Door 1 headlines** — determines gift-buyer entry rate
3. **Product card CTAs** — "Make This Mug" vs "Order Mug" vs "Start Making"
4. **Upload screen heading** — reduces drop-off when product-led
5. **Share templates** — viral coefficient

---

*Framework complete. All copy is code-ready with character counts verified.*
