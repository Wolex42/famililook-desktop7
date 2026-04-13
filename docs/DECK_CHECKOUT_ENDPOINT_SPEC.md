# POST /payments/create-deck-checkout — Endpoint Spec
## Connects Stripe payment to QPMarkets card deck fulfillment
## Date: 2026-03-26

> **STATUS: FULLY LIVE as of 2026-03-26.** All checklist items complete. Full pipeline verified: FE → Stripe Checkout → webhook → CardPrintClient → QPMarkets API.

---

## Overview

This endpoint creates a Stripe Checkout Session for a FamiliUno card deck order. After payment, the existing webhook (`_process_paid_order`) routes the order to QPMarkets via `CardPrintClient`.

**The QPMarkets backend is already live** — `CardPrintClient.is_configured = True`, all env vars set. This endpoint is the **only missing piece**.

---

## Request

```
POST /payments/create-deck-checkout
Content-Type: application/json
```

### Body

```json
{
  "manifest": {                    // card_deck_order.v1 manifest from FE
    "schemaVersion": "card_deck_order.v1",
    "orderId": "FL-CD-20260326-a1b2c3",
    "deck": {
      "totalCards": 52,
      "faceCards": 40,
      "specialCards": 4,
      "blankCards": 8,
      "dataSource": "group"
    },
    "cards": [ ... ],              // per-card metadata
    "specification": { ... }       // print spec (816x1112px, 300DPI)
  },
  "shipping": {
    "name": "John Smith",
    "line1": "123 High Street",
    "line2": "",
    "city": "London",
    "postcode": "SW1A 1AA",
    "country": "GB"
  },
  "quantity": 1,
  "successUrl": "https://famililook.com/order-success?order_id={order_id}",
  "cancelUrl": "https://famililook.com/uno"
}
```

### Validation
- `manifest.schemaVersion` must be `"card_deck_order.v1"`
- `shipping` required (name, line1, city, postcode, country)
- `quantity` 1-10
- Rate limit: 5 requests per minute per IP (reuse existing `_check_rate_limit`)

---

## Response

```json
{
  "ok": true,
  "orderId": "FL-CD-20260326-a1b2c3",
  "checkoutUrl": "https://checkout.stripe.com/c/pay/cs_live_..."
}
```

---

## Implementation

Add to `app/routes/payments.py` after the existing `create-basket-checkout` endpoint:

```python
class DeckCheckoutRequest(BaseModel):
    manifest: dict                    # card_deck_order.v1 manifest
    shipping: ShippingAddress
    quantity: int = Field(default=1, ge=1, le=10)
    successUrl: str
    cancelUrl: str


@router.post("/payments/create-deck-checkout")
async def create_deck_checkout(body: DeckCheckoutRequest, request: Request):
    """
    Create a Stripe Checkout Session for a FamiliUno card deck order.
    After payment, webhook triggers QPMarkets fulfillment via CardPrintClient.
    """
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests")

    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Payment processing not configured")

    # Validate manifest schema
    manifest = body.manifest
    if manifest.get("schemaVersion") != "card_deck_order.v1":
        raise HTTPException(status_code=422, detail="Invalid manifest schema version")

    # Server-side price (prevents FE tampering)
    unit_price = PRODUCT_PRICES_PENCE.get("card_deck", 2499)

    # Generate or reuse order ID
    order_id = manifest.get("orderId")
    if not order_id or not order_id.startswith("FL-CD-"):
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        rand = uuid.uuid4().hex[:6]
        order_id = f"FL-CD-{ts}-{rand}"
        manifest["orderId"] = order_id

    # Save manifest to disk for QPMarkets routing after payment
    now = datetime.now(timezone.utc).isoformat()
    deck = manifest.get("deck", {})
    record = {
        "order_id": order_id,
        "product_type": "card_deck",
        "vendor": "qpmarkets",
        "status": "created",
        "payment_status": "payment_pending",
        "stripe_session_id": None,
        "price_pence": unit_price * body.quantity,
        "unit_price_pence": unit_price,
        "currency": "gbp",
        "created_at": now,
        "updated_at": now,
        "shipping": body.shipping.model_dump(),
        "quantity": body.quantity,
        "manifest": manifest,
        "deck_summary": {
            "totalCards": deck.get("totalCards", 0),
            "faceCards": deck.get("faceCards", 0),
            "specialCards": deck.get("specialCards", 0),
            "dataSource": deck.get("dataSource"),
        },
        "status_history": [
            {"status": "created", "timestamp": now},
        ],
    }

    # Create Stripe Checkout Session
    try:
        card_count = deck.get("totalCards", 52)
        session = stripe.checkout.Session.create(
            mode="payment",
            currency="gbp",
            line_items=[{
                "price_data": {
                    "currency": "gbp",
                    "unit_amount": unit_price,
                    "product_data": {
                        "name": f"FamiliUno Card Deck ({card_count} cards)",
                        "description": "Personalised family card game — poker-size, glossy finish",
                    },
                },
                "quantity": body.quantity,
            }],
            metadata={"order_id": order_id},
            shipping_address_collection={"allowed_countries": ["GB", "US", "CA", "AU", "DE", "FR", "IE", "NL"]},
            success_url=body.successUrl.replace("{order_id}", order_id),
            cancel_url=body.cancelUrl,
            expires_at=int(datetime.now(timezone.utc).timestamp()) + 1800,
        )
    except stripe.StripeError as e:
        logger.error("[payments] Deck checkout Stripe error: %s — %s", order_id, e)
        raise HTTPException(status_code=502, detail="Payment provider error")

    # Update record with Stripe session
    record["stripe_session_id"] = session.id
    record["status_history"].append({
        "status": "payment_pending",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stripe_session_id": session.id,
    })
    _save_order_record(order_id, record)

    logger.info("[payments] Deck checkout created: %s session=%s £%.2f",
                order_id, session.id, unit_price * body.quantity / 100)

    return {"ok": True, "orderId": order_id, "checkoutUrl": session.url}
```

---

## Post-Payment Flow (ALREADY BUILT)

1. Stripe sends `checkout.session.completed` webhook
2. Existing handler reads `metadata.order_id` → loads order record
3. `_process_paid_order()` marks as paid, calls `route_order_to_vendor()`
4. `route_order_to_vendor()` detects `product_type: "card_deck"` → `CardPrintClient.create_order()`
5. `CardPrintClient` submits to QPMarkets API → returns vendor order ID
6. Order record updated with vendor response

**No changes needed** to webhook, vendor_client, or CardPrintClient.

---

## Frontend Changes Needed

> **All frontend changes below are deployed and live as of 2026-03-26.**

After adding this endpoint:

1. **DeckCheckoutPage.jsx**: Replace the TODO stub (line ~244) with:
   ```javascript
   const response = await fetch(`${API_BASE}/payments/create-deck-checkout`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       manifest,
       shipping,
       quantity: 1,
       successUrl: `${window.location.origin}/order-success?order_id={order_id}`,
       cancelUrl: `${window.location.origin}/uno`,
     }),
   });
   const { checkoutUrl } = await response.json();
   window.location.href = checkoutUrl;
   ```

2. **FamiliUnoPage.jsx**: Re-enable the order button (remove `disabled` + "Coming Soon").

---

## Testing Checklist

- [x] POST /payments/create-deck-checkout returns Stripe checkout URL
- [x] Stripe checkout page shows "FamiliUno Card Deck (52 cards)" at £24.99
- [x] After payment, webhook fires and order record updated to "paid"
- [x] `route_order_to_vendor` routes to QPMarkets (check `is_configured` = True)
- [x] QPMarkets API receives order (check Hetzner logs)
- [x] Order success page shows at /order-success?order_id=FL-CD-...
- [x] Cancel redirects back to /uno
- [x] Rate limiting works (6th request in 60s returns 429)
- [x] Invalid manifest schema returns 422
