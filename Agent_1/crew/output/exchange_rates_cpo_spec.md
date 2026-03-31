## CPO Spec: Live Exchange Rates API (H1)

**Agent**: CPO
**Date**: 2026-03-24
**Severity**: HIGH — hardcoded rates drift from reality. Customers see one price, Stripe charges another.

---

### Problem

CurrencyContext.jsx has hardcoded approximate rates:
```js
GB: 1.0, US: 1.27, CA: 1.72, AU: 1.95, DE: 1.17, FR: 1.17, IE: 1.17, NL: 1.17
```
These were set weeks ago. GBP/USD alone drifts ~2-5% monthly. A customer sees "£14.99" but Stripe charges at the real rate — causing confusion and refund requests at scale.

### Solution

Backend endpoint that fetches live rates daily and caches them. Frontend calls on load instead of using hardcoded values.

### Backend (desktop3)

- New endpoint: `GET /currency/rates`
- Returns: `{ base: "GBP", rates: { USD: 1.27, EUR: 1.17, ... }, updated_at: "2026-03-24T..." }`
- Source: Free API — exchangerate.host or open.er-api.com (no key required for basic use)
- Cache: fetch once per day, store in memory. Return cached on subsequent requests.
- Fallback: if API fails, return hardcoded rates (same as current) with `{ stale: true }`

### Frontend (desktop2)

- CurrencyContext.jsx: on mount, call `GET /currency/rates`
- Replace hardcoded RATES with live data
- If API fails: fall back to hardcoded (current behaviour)
- Show subtle indicator if rates are stale (>24h old)

### Acceptance Criteria

- [ ] Backend: `GET /currency/rates` returns live rates for GBP→USD/EUR/CAD/AUD
- [ ] Backend: rates cached for 24h, refreshed on first request after cache expires
- [ ] Backend: fallback to hardcoded if external API unreachable
- [ ] Frontend: CurrencyContext loads rates from backend on mount
- [ ] Frontend: falls back to hardcoded if backend unavailable
- [ ] Existing tests still pass

### Scope
- desktop3: new route `app/routes/currency.py`
- desktop2: update `src/state/CurrencyContext.jsx`
- **Both are approved for modification**

**Effort**: M
