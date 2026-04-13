# Spec: IP-Based Analysis Rate Limiting

> **Author**: CPO Agent
> **Date**: 2026-04-02
> **Product**: FamiliLook (desktop3 BE + desktop2 FE)
> **Priority**: P1 — prevents unlimited free usage
> **Status**: SPEC_READY

---

## 1. Problem

Free tier users get 5 analyses per 14 days. Currently tracked in `localStorage` (`fl:analysis-count`). This is trivially bypassed by clearing storage or using incognito. Any user can run unlimited free analyses forever.

## 2. Solution

Dual-layer enforcement: frontend tracks count locally for instant UX, backend enforces by IP so it can't be bypassed.

---

## 3. Backend Changes (desktop3)

### 3.1 New Storage: IP Analysis Ledger

Create a lightweight JSON file or SQLite table (consistent with existing `analytics_data/`, `feedback_data/`, `orders_data/` pattern):

```
analysis_data/ip_ledger.json
```

Structure:
```json
{
  "192.168.1.100": {
    "count": 3,
    "first_at": "2026-04-02T10:30:00Z",
    "last_at": "2026-04-02T14:15:00Z",
    "plan": "free"
  },
  "82.45.12.34": {
    "count": 5,
    "first_at": "2026-03-28T09:00:00Z",
    "last_at": "2026-04-01T16:00:00Z",
    "plan": "free"
  }
}
```

### 3.2 Rate Check on `/kinship/analyze`

In `app/main.py`, before running analysis:

```python
# Rate limiting — Free tier IP enforcement
client_ip = request.client.host
plan = request.headers.get("X-Plan", "free")

if plan == "free":
    allowed, remaining, resets_at = check_ip_limit(client_ip, max_attempts=7, window_days=14)
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "ok": False,
                "error": "rate_limited",
                "message": "You've reached the free analysis limit. Upgrade for unlimited analyses.",
                "remaining": 0,
                "resets_at": resets_at,
                "upgrade_url": "/plans"
            }
        )
```

### 3.3 `check_ip_limit()` Function

```python
def check_ip_limit(ip: str, max_attempts: int = 7, window_days: int = 14) -> tuple:
    """
    Check if IP has exceeded free analysis limit.
    Returns: (allowed: bool, remaining: int, resets_at: str|None)
    
    Uses 7 per IP (not 5) because households share IPs.
    Frontend shows 5 as the user-facing limit.
    Backend allows 7 to handle family members on same network.
    """
    ledger = load_ledger()
    entry = ledger.get(ip)
    
    if not entry:
        # First analysis from this IP
        ledger[ip] = {"count": 1, "first_at": now_iso(), "last_at": now_iso(), "plan": "free"}
        save_ledger(ledger)
        return (True, max_attempts - 1, None)
    
    # Check if window has expired
    first_at = parse_iso(entry["first_at"])
    window_end = first_at + timedelta(days=window_days)
    
    if datetime.utcnow() > window_end:
        # Window expired — reset counter
        ledger[ip] = {"count": 1, "first_at": now_iso(), "last_at": now_iso(), "plan": "free"}
        save_ledger(ledger)
        return (True, max_attempts - 1, None)
    
    if entry["count"] >= max_attempts:
        # Limit reached
        return (False, 0, window_end.isoformat())
    
    # Increment
    entry["count"] += 1
    entry["last_at"] = now_iso()
    save_ledger(ledger)
    return (True, max_attempts - entry["count"], window_end.isoformat())
```

### 3.4 Rate Info Endpoint

New endpoint so frontend can check remaining without running an analysis:

```python
@router.get("/rate-limit/status")
async def rate_limit_status(request: Request):
    """Return current rate limit status for the requesting IP."""
    client_ip = request.client.host
    plan = request.headers.get("X-Plan", "free")
    
    if plan != "free":
        return {"limited": False, "remaining": -1, "plan": plan}
    
    ledger = load_ledger()
    entry = ledger.get(client_ip)
    
    if not entry:
        return {"limited": False, "remaining": 7, "resets_at": None, "plan": "free"}
    
    first_at = parse_iso(entry["first_at"])
    window_end = first_at + timedelta(days=14)
    
    if datetime.utcnow() > window_end:
        return {"limited": False, "remaining": 7, "resets_at": None, "plan": "free"}
    
    remaining = max(0, 7 - entry["count"])
    return {
        "limited": remaining == 0,
        "remaining": remaining,
        "resets_at": window_end.isoformat(),
        "plan": "free"
    }
```

### 3.5 Include Remaining in Analysis Response

Add to the successful analysis response in `kinship_analyze()`:

```python
# After successful analysis, include rate info
if plan == "free":
    _, remaining, resets_at = check_ip_limit(client_ip, max_attempts=7, window_days=14)
    report["rate_limit"] = {
        "remaining": remaining,
        "resets_at": resets_at
    }
```

### 3.6 Bypass for Paid Plans

Paid users (Plus/Pro) skip rate limiting entirely. Identified by:
- `X-Plan` header sent by frontend (set from `usePlanFeatures`)
- Backend can verify against Stripe subscription status if needed (future hardening)

### 3.7 IP Behind Proxy (Caddy)

The backend runs behind Caddy reverse proxy. Ensure `request.client.host` returns the real client IP, not Caddy's 127.0.0.1.

Check Caddy config — it should set `X-Forwarded-For` or `X-Real-IP`. FastAPI can read this:

```python
client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.client.host
```

---

## 4. Frontend Changes (desktop2)

### 4.1 Show Remaining Count

After each analysis, the response includes `rate_limit.remaining`. Display in the results area:

```
"4 of 5 free analyses remaining" (subtle, below results)
```

When 0 remaining:
```
┌─────────────────────────────────────────────┐
│  You've used all 5 free analyses             │
│  Resets in 12 days — or upgrade now          │
│  [Upgrade to Plus — £3.99/mo →]              │
└─────────────────────────────────────────────┘
```

### 4.2 Check Rate Limit on App Load

On mount of UploadSection or AppLayout, call `/rate-limit/status`:

```javascript
useEffect(() => {
  if (currentPlan === "free") {
    fetch(`${API_BASE}/rate-limit/status`, { headers: { "X-Plan": "free" } })
      .then(r => r.json())
      .then(data => {
        if (data.limited) {
          setRateLimited(true);
          setResetsAt(data.resets_at);
        } else {
          setRemainingAnalyses(data.remaining);
        }
      })
      .catch(() => { /* fail open — allow analysis, backend will enforce */ });
  }
}, [currentPlan]);
```

### 4.3 Block Upload When Rate Limited

If `rateLimited === true`, disable the "Analyze Family" button and show:

```
"Free limit reached. Resets {timeUntilReset}. Upgrade for unlimited."
```

### 4.4 Handle 429 Response

If `/kinship/analyze` returns 429:

```javascript
if (res.status === 429) {
  const data = await res.json();
  setRateLimited(true);
  setResetsAt(data.resets_at);
  setError("You've reached the free analysis limit. Upgrade for unlimited analyses.");
  return;
}
```

### 4.5 Send Plan Header

Add `X-Plan` header to all API calls so backend knows the tier:

```javascript
headers: {
  ...getBiometricHeaders(),
  "X-Plan": currentPlan || "free"
}
```

### 4.6 Keep localStorage as Soft Limit

Keep `fl:analysis-count` in localStorage for instant UX (no API call needed to show "3 of 5 remaining"). Backend is the hard enforcement — localStorage is just a courtesy display.

---

## 5. Numbers

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **User-facing limit** | 5 | CEO decision |
| **Backend IP limit** | 7 | Buffer for shared household IPs |
| **Window** | 14 days | CEO decision |
| **Bypass** | Plus/Pro plans | Paid users unlimited |
| **Storage** | JSON file | Consistent with existing data patterns (analytics_data/, etc.) |

The 2-number gap (5 shown vs 7 enforced) handles the case where Mum and Dad both try on the same WiFi. Frontend says "limit reached" at 5, but if a second family member tries, the backend still allows 2 more.

---

## 6. GDPR Considerations

- IP addresses are personal data under GDPR
- The ledger stores IP + timestamps + count only (no analysis results)
- Auto-purge entries older than 30 days (window is 14 days, so 30 gives buffer)
- Document in privacy policy: "We temporarily store your IP address to manage service usage limits. This data is automatically deleted after 30 days."
- Add to `public/cookie-policy.html` under "Server-side storage"

---

## 7. Files to Change

### Backend (desktop3)
| File | Change |
|------|--------|
| `app/main.py` | Add rate check before `kinship_analyze()`, include remaining in response |
| `app/rate_limit.py` | **NEW** — `check_ip_limit()`, `load_ledger()`, `save_ledger()`, auto-purge |
| `app/routes/detection.py` or new route file | **NEW** — `/rate-limit/status` endpoint |

### Frontend (desktop2)
| File | Change |
|------|--------|
| `src/layout/MobileResultsSection.jsx` | Show remaining count after analysis |
| `src/layout/UploadSection.jsx` | Check rate limit on mount, block when limited |
| `src/hooks/useKinshipAnalysis.jsx` | Handle 429 response, send X-Plan header |
| `src/layout/AppLayout.jsx` | Rate limit check on app load |
| `public/cookie-policy.html` | Document IP storage |

---

## 8. Agent Assignments

| Step | Agent | Task |
|------|-------|------|
| 1 | fe_lead (BE) | Create `app/rate_limit.py` with ledger functions + auto-purge |
| 2 | fe_lead (BE) | Add rate check to `kinship_analyze()` + `/rate-limit/status` endpoint |
| 3 | fe_lead (FE) | Send X-Plan header, handle 429, check rate on mount |
| 4 | fe_lead (FE) | Show remaining count + upgrade prompt when limited |
| 5 | qa_lead | Tests: rate limit enforcement, 429 handling, window reset, IP extraction |
| 6 | coo | Update privacy policy + cookie policy with IP storage disclosure |

---

## 9. Acceptance Criteria

- [ ] Free user on fresh IP gets 5 analyses (frontend shows 5, backend allows 7)
- [ ] After 5 analyses, frontend shows "limit reached" with upgrade CTA
- [ ] After 7 analyses from same IP, backend returns 429
- [ ] After 14 days, counter resets automatically
- [ ] Plus/Pro users are never rate limited
- [ ] Clearing localStorage does NOT reset the limit (backend enforces)
- [ ] Incognito mode does NOT reset the limit (same IP)
- [ ] Two people on same household WiFi get 7 total (not 5 each)
- [ ] IP ledger auto-purges entries older than 30 days
- [ ] Privacy policy updated with IP storage disclosure
- [ ] `/rate-limit/status` returns correct remaining count
- [ ] "Analyze Family" button disabled when rate limited
