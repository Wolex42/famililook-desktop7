# Cross-Repository Audit — FML Platform
**Date:** 2026-04-09 | **Author:** COO Agent (read-only audit) | **Scope:** 7 repositories

## Summary Table

| Repo | Product | Source Files | Test Files | Framework | Last Commit | CI |
|------|---------|-------------|------------|-----------|-------------|-----|
| desktop2 | FamiliLook+Uno FE | 186 JSX, 97 JS, 7 CSS, 1 TS | 73 (1,346 tests) | Vitest+Playwright | 2026-04-09 | verify+security |
| desktop3 | ML Backend (all) | 35 app, 4 root, 2 scripts, 1 utils .py | 13 (173 tests) | pytest | 2026-04-09 | ci+security |
| desktop4 | FamiliPoker FE | 84 JSX, 64 JS, 1 TSX, 8 CSS | 47 | Vitest+Playwright | 2026-04-05 | verify+security |
| desktop5 | FamiliPoker BE | 5 app .py | 3 | pytest | 2026-02-27 | NONE |
| desktop6 | FamiliMatch FE | 19 JSX, 9 JS, 1 CSS | 6 | Vitest | 2026-04-03 | verify only |
| desktop7 | FamiliMatch BE | 7 app .py | 5 | pytest+asyncio | 2026-03-25 | NONE |
| FML root | Docs/agents/contracts | 24 docs MD, 158 Agent1 MD, 4 PY, 3 JSON | 0 | N/A | 2026-04-01 | NONE |

---

## 1. famililook-desktop2 (FamiliLook + FamiliUno FE)

### Directory structure (src/)
App.jsx, AppRouter.jsx, arcface.js, main.jsx. 20+ subdirs in components/ (analysis, animations, cardgame, cards, creation, debug, detection, keepsakes, merchandise, modals, navigation, results, trail, transitions, ui, uno, upload, vault, visualization). hooks/ (13 files), layout/ (5 files), pages/ (19 files), state/ (6 files), services/, styles/, test/, theme/, tools/, utils/, validation/.

### File counts
- JSX: 186
- JS: 97
- CSS: 7
- TS: 1

### Tests
- 73 test files, 1,346 tests
- Framework: Vitest + Playwright (E2E)

### Dependencies (13 production)
react ^18.3.1, react-dom ^18.3.1, react-router-dom ^7.9.5, framer-motion ^12.34.3, @tensorflow/tfjs-* ^4.22.0, @vladmandic/face-api ^1.7.15, pixi.js ^7.4.3, lucide-react ^0.473.0, html-to-image ^1.11.13, html2canvas ^1.4.1, web-vitals ^5.1.0.

DevDeps: vite ^5.4.10, vitest ^2.1.9, @playwright/test ^1.58.0, tailwindcss ^3.4.14, eslint ^9.13.0.

### Routes (19)
/, /hub, /app, /uno, /plans, /privacy, /terms, /dashboard, /order-success, /icon-preview, /mockup-preview, /character-preview, /mothers-day, /trail, /vault, /occasion/:occasionId, /create/:productId (conditional). Maintenance mode overrides all.

### Feature flags (9)
VITE_MAINTENANCE_MODE, VITE_PRODUCT_LED_HOMEPAGE, VITE_TRAIL_DEFAULT_LANDING, VITE_PRODUCT_CREATION_FLOW, VITE_FAMILY_PROFILES, VITE_SMART_PHOTO_PHASE1, VITE_SMART_PHOTO_PHASE2, VITE_FACE_NAMING_SHEET, VITE_OCCASION_SHELF.

### Environment variables (11)
VITE_API_BASE, VITE_API_KEY, VITE_API_URL, VITE_FAMILIMATCH_URL, VITE_FAMILIPOKER_URL, VITE_STRIPE_PLUS_MONTHLY_PRICE_ID, VITE_STRIPE_PLUS_ANNUAL_PRICE_ID, VITE_STRIPE_PRO_MONTHLY_PRICE_ID, VITE_STRIPE_PRO_ANNUAL_PRICE_ID, VITE_APP_MODE, import.meta.env.DEV.

### Last commit
2026-04-09 — `feat: add legal safeguards to maintenance page`

### Docs
README.md exists.

### Open issues
AppErrorBus NOT BUILT (23 silent catches), AppStorage NOT BUILT (35+ localStorage risks), resultsContract.js NOT BUILT. Platform audit: 5 CRITICAL, 18 HIGH findings. Multiple CRs UNVERIFIED on mobile device.

---

## 2. famililook-desktop3 (Python ML Backend)

### Directory structure
app/ has 35 .py files (including keepsake/ submodule with 4 files, routes/ with 13 files). Root: server.py, gunicorn.conf.py, collect_calibration_data.py, export_adaface_onnx.py. Also: contracts/, data/, docs/, models/, scripts/ (2), tests/ (13), traceability/, utils/ (1).

### File counts
- Python (app/): 35
- Python (root): 4
- Python (scripts): 2
- Python (utils): 1
- Tests: 13

### Tests
- 13 test files, 173 tests
- Framework: pytest

### Dependencies (16)
fastapi==0.115.0, uvicorn==0.30.6, gunicorn==22.0.0, python-multipart==0.0.20, opencv-contrib-python==4.11.0.86, numpy==1.26.4, mediapipe==0.10.14, protobuf>=4.25.3, insightface==0.7.3, onnxruntime==1.21.1, pillow==11.3.0, stripe==14.4.0, anthropic>=0.43.0, httpx==0.28.1, pytest==9.0.2, jsonschema==4.23.0.

### Endpoints (55+)
main.py legacy routes (22 endpoints) + routes/ module (33+ endpoints spanning ambassador, analytics, currency, detection, generation, explain, keepsake, payments, kinship, orders).

### Environment variables (25)
SECRET_KEY, FAMILILOOK_API_KEY, ENVIRONMENT, ADMIN_KEY_HASH, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, PRODIGI_WEBHOOK_SECRET, RATE_LIMIT_MAX, CORS_ORIGINS, PRODIGI_API_KEY, PRODIGI_SANDBOX, PRODIGI_CALLBACK_URL, QPMARKETS_STORE_TOKEN, QPMARKETS_UNO_PRODUCT_ID, QPMARKETS_VAULT_PRODUCT_ID, QPMARKETS_MATERIAL_PATH, QPMARKETS_UNIT_PRICE, DOMAIN, RATE_LIMIT_LEDGER, RATE_LIMIT_WINDOW_DAYS, ADAFACE_MODEL_PATH, DATA_DIR, ANTHROPIC_API_KEY, LLM_MODEL, INTERNAL_API_TOKEN.

### Last commit
2026-04-09 — `feat: maintenance feedback endpoints with IP geolocation`

### Docs
DEPLOYMENT_GUIDE.md, docs/traceability_matrix_PRD_v2.0.csv. No README.

### Open issues
Duplicate route definitions in main.py and routes/ (migration in progress).

---

## 3. famililook-desktop4 (FamiliPoker FE)

### Directory structure
src/ mirrors desktop2 layout (components with 18 subdirs, contracts, game, hooks, layout, lib, pages (4), services, state, styles, test, theme, tools, utils). 84 JSX, 64 JS, 1 TSX, 8 CSS.

### File counts
- JSX: 84
- JS: 64
- TSX: 1
- CSS: 8

### Tests
- 47 test files
- Framework: Vitest + Playwright

### Dependencies
Same TensorFlow/face-api stack as desktop2. framer-motion ^11.0.0 (divergent from desktop2's ^12.34.3). react-router-dom ^7.9.5.

### Routes (5)
/ (redirect to /app), /app, /plans, /privacy, /terms. Age gate blocks all until confirmed.

### Feature flags (1)
VITE_MULTIPLAYER_ENABLED.

### Environment variables (6)
VITE_API_BASE, VITE_API_KEY, VITE_GAME_SERVER_URL, VITE_BRAND_HUB_URL, VITE_APP_MODE, DEV.

### Last commit
2026-04-05 — `feat: PlanGate -- FamiliPoker requires Plus subscription`

### Docs
README.md exists. No open issues.

---

## 4. famililook-desktop5 (FamiliPoker BE)

### Directory structure
Minimal. app/ (5 files: __init__, game_state, main, protocol, rooms). tests/ (3 files). docs/MULTIPLAYER_ARCHITECTURE.md.

### File counts
- Python (app/): 5
- Tests: 3

### Tests
- 3 test files
- Framework: pytest

### Dependencies (3)
fastapi==0.115.0, uvicorn==0.30.6, pydantic>=2.0.

### Endpoints (2)
GET /health, WebSocket /ws/game.

### Environment variables (6)
ALLOWED_ORIGINS, PORT (8020), ROOM_IDLE_TIMEOUT_SECONDS (1800), MAX_PLAYERS_PER_ROOM (4), MAX_ROOMS (10000), MAX_CONNECTIONS_PER_IP (10).

### Last commit
2026-02-27 — `fix: per-IP WebSocket connection limit (max 10 concurrent)`. **41 days inactive.**

### Docs
docs/MULTIPLAYER_ARCHITECTURE.md. No CI. No README.

---

## 5. famililook-desktop6 (FamiliMatch FE)

### Directory structure
Compact. src/ has 19 JSX, 9 JS, 1 CSS. components/ (9 files), pages/ (6), hooks/, state/, test/, utils/.

### File counts
- JSX: 19
- JS: 9
- CSS: 1

### Tests
- 6 test files
- Framework: Vitest (no Playwright E2E)

### Dependencies (6 production)
framer-motion ^11.0.0, html2canvas ^1.4.1, lucide-react ^0.473.0, react ^18.3.1, react-dom ^18.3.1, react-router-dom ^7.1.1 (divergent — others on ^7.9.5).

### Routes (6)
/, /solo, /room, /results, /privacy, /terms.

### Environment variables (6)
VITE_API_BASE, VITE_API_KEY, VITE_MATCH_SERVER_URL, VITE_BRAND_HUB_URL, VITE_SHARE_URL, DEV.

### Last commit
2026-04-03 — `ci: optimise workflows to reduce Actions usage`

### Docs
No README. No docs/. CI: verify.yml only (no security scanning). No Playwright E2E.

### Open issues
Duo/Group modes gated behind Plus tier.

---

## 6. famililook-desktop7 (FamiliMatch BE)

### Directory structure
app/ (7 files: __init__, comparison, consent, desktop3_client, main, protocol, rooms). tests/ (5 files + conftest).

### File counts
- Python (app/): 7
- Tests: 5

### Tests
- 5 test files
- Framework: pytest + pytest-asyncio

### Dependencies (6)
fastapi==0.115.0, uvicorn==0.30.6, pydantic>=2.0, httpx>=0.27.0, pytest>=8.0, pytest-asyncio>=0.23.0.

### Endpoints (2)
GET /health, WebSocket /ws/match.

### Environment variables (5)
DESKTOP3_URL, DESKTOP3_TIMEOUT, MATCH_TIER_SECRET, ALLOWED_ORIGINS, MAX_CONNECTIONS_PER_IP.

### Last commit
2026-03-25 — `fix: desktop7 -- add X-Biometric-Consent header to desktop3 calls`. **15 days inactive.**

### Docs
No CI. No README.

### Open issues
BIPA server-side validation not yet complete.

---

## 7. FML Root Repository

### Directory structure
CLAUDE.md, PRD_GOVERNANCE_CONSOLIDATED.md, Dockerfile, requirements.txt. Agent_1/ (158 .md files across agents/workflows/output + 4 .py files). contracts/ (3 frozen JSON schemas). docs/ (24 .md files). .claude/ (governance layer).

### File counts
- MD (docs/): 24
- MD (Agent_1/): 158
- Python: 4
- JSON (contracts/): 3

### Tests
None.

### Dependencies
fastapi==0.115.0, uvicorn==0.30.6, pydantic>=2.0, httpx>=0.27.0, pytest>=8.0, pytest-asyncio>=0.23.0.

### Last commit
2026-04-01 — `docs: keepsake mobile redesign + product quality fixes + stale chunk prevention`

### Key docs
PLATFORM_ARCHITECTURE.md, MASTER_REGRESSION_MATRIX.md, FMEA_comprehensive.md, FULL_PLATFORM_AUDIT_2026-03-26.md, SWOT_ANALYSIS_2026-03-26.md, DPIA_FAMILILOOK.md, INCIDENT_RESPONSE_PLAN.md, UXD_all_products.md. 3 frozen API contract schemas. 9 agent personas. 5 workflows. 95+ crew output deliverables.

### Open issues
AppErrorBus/AppStorage/resultsContract.js NOT BUILT. VITE_API_KEY rotation (operational). Cyber insurance pending.

---

## Cross-Cutting Facts

**Dependency divergence:**
- react-router-dom: desktop6 ^7.1.1 vs others ^7.9.5
- framer-motion: desktop2 ^12.34.3 vs desktop4/6 ^11.0.0

**CI gaps:**
- desktop5 and desktop7: zero CI
- desktop6: verify only (no security scanning)

**Test density:**
- desktop2: 73 test files (1,346 tests)
- desktop6: 6 test files
- desktop5: 3 test files

**Activity:**
- desktop5 last touched 41 days ago (2026-02-27)
- desktop7 last touched 15 days ago (2026-03-25)
- Active repos: desktop2 and desktop3 (both today)
