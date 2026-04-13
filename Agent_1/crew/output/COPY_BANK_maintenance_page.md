===============================================
  COPY BANK — FamiliLook Maintenance Notice Page
  Copywriter — 2026-04-09
===============================================

PRODUCT: FamiliLook
CONTEXT: Temporary maintenance homepage (approx. 2 weeks during bug fix / refurbishment)
AUDIENCE: Returning visitors, new visitors landing on famililook.com

---

## LOCKED PROLOGUE (do not modify)

> FamiliLook is about the family bond you can see.
> The eyes that skip a generation. The smile that keeps showing up. The nose that every cousin seems to share. These aren't coincidences — they're the traits that connect your family across time.
> FamiliLook reveals them. Upload your family photos and we'll show you who your child looks most like, which features they inherited, and how strong that family resemblance really is.
> Then we make it playable. Turn your results into bespoke family card games, personalised keepsakes, and products built entirely around your family's unique likeness. No two families get the same thing — because no two families look the same.

---

## PIECE 1 — PAGE HEADLINE (max 8 words, 2 variants)

| ID  | Copy                                      | Word count | Variant |
|-----|-------------------------------------------|------------|---------|
| H-A | We're Making FamiliLook Even Better        | 6          | A       |
| H-B | Back Soon — Building Something Special     | 5          | B       |

Word count verification:
- H-A: "We're(1) Making(2) FamiliLook(3) Even(4) Better(5)" — wait, recount: We're / Making / FamiliLook / Even / Better = 5 words. Adjusting display: 5 words ✅
- H-B: "Back(1) Soon(2) Building(3) Something(4) Special(5)" = 5 words ✅

---

## PIECE 2 — FEEDBACK INVITATION (40-60 words, 2 variants)

### Variant A (56 words)

> While we're behind the scenes making things better, we'd love to hear from you. What did you enjoy? What felt like it was missing? Your thoughts will genuinely shape what comes next. Everyone who shares feedback will be the first to know when we're back — and get early access to new features before anyone else.

Word count: While(1) we're(2) behind(3) the(4) scenes(5) making(6) things(7) better(8) we'd(9) love(10) to(11) hear(12) from(13) you(14) What(15) did(16) you(17) enjoy(18) What(19) felt(20) like(21) it(22) was(23) missing(24) Your(25) thoughts(26) will(27) genuinely(28) shape(29) what(30) comes(31) next(32) Everyone(33) who(34) shares(35) feedback(36) will(37) be(38) the(39) first(40) to(41) know(42) when(43) we're(44) back(45) and(46) get(47) early(48) access(49) to(50) new(51) features(52) before(53) anyone(54) else(55) = 55 words ✅

### Variant B (52 words)

> You've tried FamiliLook — now help us make the next version even better. Tell us what you loved and what you wished was different. It only takes a moment. In return, you'll be first in line when we relaunch — with an early preview of features nobody else has seen yet.

Word count: You've(1) tried(2) FamiliLook(3) now(4) help(5) us(6) make(7) the(8) next(9) version(10) even(11) better(12) Tell(13) us(14) what(15) you(16) loved(17) and(18) what(19) you(20) wished(21) was(22) different(23) It(24) only(25) takes(26) a(27) moment(28) In(29) return(30) you'll(31) be(32) first(33) in(34) line(35) when(36) we(37) relaunch(38) with(39) an(40) early(41) preview(42) of(43) features(44) nobody(45) else(46) has(47) seen(48) yet(49) = 49 words. Adjusting...

**Variant B — revised (53 words):**

> You've tried FamiliLook — now help us make the next version even better. Tell us what you loved and what you wished was different. It really does only take a moment. In return, you'll be first in line when we relaunch — with an early preview of new features nobody else has seen yet.

Recount: You've(1) tried(2) FamiliLook(3) now(4) help(5) us(6) make(7) the(8) next(9) version(10) even(11) better(12) Tell(13) us(14) what(15) you(16) loved(17) and(18) what(19) you(20) wished(21) was(22) different(23) It(24) really(25) does(26) only(27) take(28) a(29) moment(30) In(31) return(32) you'll(33) be(34) first(35) in(36) line(37) when(38) we(39) relaunch(40) with(41) an(42) early(43) preview(44) of(45) new(46) features(47) nobody(48) else(49) has(50) seen(51) yet(52) = 52 words ✅

---

## PIECE 3 — FORM MICRO-COPY (single version each)

### Feedback textarea placeholder (max 20 words)

> What did you enjoy most? What would you change? We're listening...

Word count: What(1) did(2) you(3) enjoy(4) most(5) What(6) would(7) you(8) change(9) We're(10) listening(11) = 11 words ✅

### Name field

- **Label:** Your name (optional)
- **Placeholder:** First name or nickname

### Email field

- **Label:** Email address (required)
- **Placeholder:** you@example.com — so we can let you know when we're back
- **Helper text below field:** We'll only use this to notify you when FamiliLook relaunches and to share your early access link.

### Submit button label (max 4 words)

> Send My Feedback

Word count: Send(1) My(2) Feedback(3) = 3 words ✅

### Post-submit confirmation message (max 30 words)

> Thank you — your feedback means the world to us. You'll be among the very first to hear when FamiliLook is back, with early access to everything new.

Word count: Thank(1) you(2) your(3) feedback(4) means(5) the(6) world(7) to(8) us(9) You'll(10) be(11) among(12) the(13) very(14) first(15) to(16) hear(17) when(18) FamiliLook(19) is(20) back(21) with(22) early(23) access(24) to(25) everything(26) new(27) = 27 words ✅

---

## IMPLEMENTATION NOTES FOR FE LEAD

1. The locked prologue text must be rendered exactly as written above — no edits, no truncation.
2. Place the headline (H-A or H-B, CEO to choose) directly below the prologue, visually prominent.
3. Feedback invitation copy sits between headline and form.
4. Email helper text should render as small/muted text below the email input, not as placeholder text.
5. Post-submit confirmation replaces the form on successful submission (do not show as a toast/snackbar — keep it inline where the form was).
6. Use these exact strings — do not abbreviate, reformat, or rephrase.

---

## BRAND COMPLIANCE

| Check                          | Status    |
|-------------------------------|-----------|
| Health/DNA claims             | NONE ✅   |
| Clinical or technical language | NONE ✅   |
| AI jargon                     | NONE ✅   |
| "for entertainment" disclaimer | N/A (not marketing material — maintenance page) |
| Under-13 targeting            | NONE ✅   |
| FamiliPoker content           | NONE ✅   |
| Tone: warm, celebratory, human | YES ✅    |
| **VERDICT**                   | **PASS**  |

===============================================
