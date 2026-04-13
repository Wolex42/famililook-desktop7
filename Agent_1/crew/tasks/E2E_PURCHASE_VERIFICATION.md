# Task: End-to-End Purchase Verification — Every Product

> **Date**: 2026-04-04
> **Priority**: P0 — Revenue-critical. No product ships until verified.
> **Status**: SPEC_READY
> **Reporter**: CEO

---

## Mandate

Every purchasable product must be tested end-to-end:
1. Select product in keepsake flow
2. Customise (style, age, recipient)
3. Preview renders correctly
4. PNG exports successfully
5. Add to basket
6. Fill shipping + email
7. Pay via Stripe (test mode)
8. Webhook fires, marks order paid
9. Vendor receives order with complete artwork + manifest
10. Vendor accepts order (no validation errors)

If ANY step fails for ANY product, that product must be fixed or hidden until fixed.

---

## Products to Test

### Prodigi Products (mug, print, canvas, cushion, t-shirt, puzzle, bodysuit)

| Product ID | Label | Prodigi SKU | Needs |
|-----------|-------|-------------|-------|
| `mug_wrap` | Ceramic Mug (11oz) | GLOBAL-MUG-W | PNG wrap image |
| `character_mug` | Character Mug (11oz) | GLOBAL-MUG-W | PNG wrap image + character art |
| `fine_art_print` | Fine Art Print (16×20") | GLOBAL-FAP-16x20 | PNG image |
| `framed_canvas` | Framed Canvas (12×16") | GLOBAL-CAN-12x16 | PNG image |
| `cushion` | Canvas Cushion (45×45cm) | GLOBAL-CSH-45x45 | PNG image |
| `tshirt_print` | T-Shirt Print (12×15") | GLOBAL-TEE-* | PNG image |
| `jigsaw_puzzle` | Jigsaw Puzzle (252pc) | GLOBAL-JPZ-* | PNG image |
| `baby_bodysuit` | Baby Bodysuit | GLOBAL-BBS-* | PNG image |
| `pet_family_report` | Pet Family Report (16×20") | GLOBAL-FAP-16x20 | PNG image |
| `family_mug_set` | Family Mug Set (pair) | GLOBAL-MUG-W × 2 | 2 PNG wrap images |

### QPMarkets Products (cards, decks)

| Product ID | Label | Needs |
|-----------|-------|-------|
| `greeting_card` | Greeting Card (5×7") | PNG image + email |
| `postcard` | Postcard (6×4") | PNG image + email |
| `card_deck` | FamiliUno Deck (52 cards) | Full manifest with 52 card PNGs + email |

---

## Test Protocol Per Product

### Step 1: Frontend Flow
- [ ] Product appears in catalogue (not hidden)
- [ ] Select product → customise screen loads
- [ ] Style options render correctly
- [ ] Preview renders with actual analysis data (not placeholder)
- [ ] PNG export succeeds (no "Could not generate print image")
- [ ] "Add to Basket" works
- [ ] Basket shows correct product, price, thumbnail

### Step 2: Checkout
- [ ] Email field present and validated
- [ ] Shipping address fields present
- [ ] "Pay with Stripe" button enabled when form valid
- [ ] Stripe session created (no 422/500)
- [ ] Redirect to Stripe checkout works

### Step 3: Payment & Webhook
- [ ] Stripe payment succeeds (use test card 4242 4242 4242 4242)
- [ ] Webhook fires (`POST /webhooks/stripe` returns 200)
- [ ] Order marked as `paid` in orders_data/
- [ ] PNG file saved to orders_data/ (persistent volume)

### Step 4: Vendor Submission
- [ ] Order auto-routed to correct vendor (Prodigi or QPMarkets)
- [ ] For Prodigi: PNG URL accessible, order accepted ("Created" or "AlreadyExists")
- [ ] For QPMarkets: email included, manifest valid, order accepted
- [ ] vendor_order_id populated
- [ ] No "pending_manual" status

### Step 5: Vendor Dashboard Verification
- [ ] Order visible in Prodigi/QPMarkets dashboard
- [ ] Artwork downloaded successfully (no "Error" in thumbnail)
- [ ] Production status: InProgress or better

---

## Known Issues to Fix Before Testing

1. **Card deck manifest**: empty manifest sent when ordering from results page. Need to verify deck builder generates and includes full manifest with 52 card images.

2. **Family mug set**: requires 2 separate PNG renders (Mum mug + Dad mug). Verify both are generated and submitted.

3. **Character mug**: requires character illustration overlay. Verify character art system works.

4. **Pet family report**: requires pet analysis data. Verify pet flow generates correct data.

---

## Agent Assignments

| Step | Agent | Task |
|------|-------|------|
| 1 | qa_lead | Audit each product's frontend flow — can it be selected, customised, previewed, exported? |
| 2 | qa_lead | Audit each product's backend flow — does the vendor submission include all required data? |
| 3 | fe_lead (BE) | Fix any vendor submission gaps (missing manifest, missing artwork, missing fields) |
| 4 | fe_lead (FE) | Fix any frontend gaps (broken preview, failed export, missing styles) |
| 5 | qa_lead | Write E2E test for each product: select → export → add to basket → verify payload |
