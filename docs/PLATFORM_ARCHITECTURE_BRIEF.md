# FamiliLook — Platform Architecture Brief

## What it is

A consumer AI platform that uses computer vision to analyse family facial resemblance across **4 products** — all served by a single shared ML engine.

| Product | What It Does | Status |
|---------|-------------|--------|
| **FamiliLook** | "Who does baby look like?" — 8-feature kinship analysis + keepsake prints | LIVE |
| **FamiliUno** | Custom card game printed from your family's faces | FULLY LIVE (FE + deck ordering via QPMarkets) |
| **FamiliPoker** | Casino-style card games using facial features as suits | DEPLOYED |
| **FamiliMatch** | "Who's your face twin?" — compatibility scoring between any two faces | DEPLOYED |

---

## The ML Engine (Single Shared Backend)

**Pipeline:** Photo → Face detection → 512-dim embedding → 468-landmark mesh → 8-feature extraction → Percentile calibration

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Detection | InsightFace buffalo_l | Face bounding box + alignment |
| Embedding | AdaFace IR50 (ONNX) | 512-dim quality-adaptive face vector |
| Landmarks | MediaPipe FaceMesh | 468 2D normalised landmark coordinates |
| Features | Custom dense attributes | 8 features: eyes, eyebrows, smile, nose, face shape, skin, hair, ears |
| Calibration | Percentile reference (654 faces) | 5-tier labels per feature (e.g. "High-arch Brows", "Balanced Eyes") |

Two analysis modes with **frozen API contracts**:
- **Kinship** (`/kinship/analyze`) — feature voting with 5-3 winner rule
- **Compatibility** (`/compare/faces`) — `0.6 × embedding_sim + 0.4 × feature_sim`

---

## The Agentic Layer — What Makes This Interesting

### 9 Autonomous ML Modules (Zero External API Cost)

All run within the existing Python process. No new dependencies. No LLM calls. Pure Python stdlib + numpy.

| Module | Autonomy Level | What It Does |
|--------|---------------|-------------|
| **Circuit Breaker** | ACTIVE | CLOSED→OPEN→HALF_OPEN state machine. Fallback chain: InsightFace → MediaPipe → graceful empty. Auto-recovery probing after 30s. |
| **Maintenance Scheduler** | ACTIVE | Daily log rotation + compression. Weekly ONNX model SHA-256 integrity verification. 30-day analytics archival. Background daemon thread. |
| **Drift Monitor** | OBSERVE | Tracks AdaFace embedding distribution via Population Stability Index (PSI). Stores only aggregate statistics — never raw embeddings. Severity bands: LOW ≥0.10, MEDIUM ≥0.20, HIGH ≥0.25. |
| **Margin Tuner** | AUTO-TUNE | Per-feature dynamic vote margins. Hard bounds: 0.005–0.050, max 0.005 step, 100+ sample minimum. Optimises unknown rate toward 10–35% target band. Every adjustment logged. |
| **Feedback Loop** | OBSERVE+FLAG | Correlates user satisfaction ratings with disputed features. Flags features with >20% dispute rate. Ingests historical feedback for bootstrapping. |
| **Calibration Pipeline** | AUTO-COLLECT | Accumulates high-confidence (≥0.90) feature measurements. Triggers percentile recalculation at 200+ new samples. Rate-limited (100/hr), SHA-256 deduplicated. Privacy-preserving — stores statistics, not images. |
| **Metric-Gated Deploy** | ACTIVE | Submit → Validate → Compare → Deploy pipeline for calibration updates. Built-in validators (monotonic percentiles, margin bounds). 5-deep rollback stack. Rejects updates that fail validation. |
| **Usage Intelligence** | OBSERVE | 5 rules-based anomaly detectors: burst abuse (>20/hr/IP), quality gaming (same image re-uploaded), high engagement (conversion signal), session anomaly, error spike. Per-identifier cooldowns. |
| **A/B Testing** | ACTIVE | Canary-tests new calibrations against current. Configurable traffic split (default 90/10). Chi-squared significance testing (self-contained, no scipy). Auto-promote winner to metric-gated deploy. |

### Key Design Principle: Bounded Autonomy

Each module has a defined **autonomy zone** — it can act freely within hard limits but cannot:
- Break frozen API contracts (8 features, percentage formula, no 50/50)
- Modify existing source files
- Add dependencies
- Make external API calls
- Store raw biometric data

The margin tuner illustrates this best: it auto-adjusts vote margins per feature, but within bounds (0.005–0.050) with a max step of 0.005 per cycle. If it has no data yet, it falls back to the static default. The system self-improves without human intervention, but can never drift outside its safety envelope.

---

### 30 Native Agent Personas (Zero API Cost)

All agents run as Claude Code personas — no external LLM calls, no per-invocation cost.

| Team | Count | Schedule | Key Agents |
|------|-------|----------|-----------|
| **Product** | 4 | Daily / On-demand | CPO, PM, Design Lead, UX Researcher |
| **Engineering** | 7 | Daily / Weekly / On-commit | CTO, FE Lead, BE Lead, QA Lead, DevOps, Security, **ML Monitor** |
| **Operations** | 5 | Daily / Weekly | COO, Change Manager, Commerce Lead, Fulfillment, Compliance |
| **Marketing** | 9 | Daily / Weekly / Campaign | Brand Strategist, Copywriter, Visual Director, Social Media, Conversion, Influencer, PR, SEO, Campaign Manager |
| **Patch Cycle** | 6 | On-commit / On-demand | Spec Owner, Developer, Feature Builder, Test Engineer, DFMEA Maintainer, QA Gatekeeper |

A unified orchestrator schedules all 30 agents across 6 cadences (daily, weekly, on-commit, on-demand, on-deploy, campaign). Health dashboard at `localhost:9200/status`. Git polling triggers on-commit agents automatically.

---

## Infrastructure

| Component | Technology | Cost |
|-----------|-----------|------|
| Frontend (×3) | React 18.3 / Vite / Tailwind on Vercel | Free tier |
| Backend | Python 3.10 / FastAPI on Hetzner CPX22 | ~£15/mo |
| ML Models | InsightFace + AdaFace (ONNX) + MediaPipe | Bundled |
| Container | Docker Compose + Caddy (auto-HTTPS) | Included |
| Agents (30) | Claude Code native personas | $0/day |
| Agentic ML (9) | Python stdlib + numpy | $0/day |
| **Total operational cost** | | **~£15/month** |

---

## The Numbers

- **4** products, all sharing one ML engine
- **9** autonomous ML modules (self-monitoring, self-tuning, self-healing)
- **30** agent personas across 5 departments
- **2,063** automated tests (FE + BE)
- **3** frozen API contracts (schema-validated, immutable)
- **654**-face calibration dataset with auto-expanding pipeline
- **$0/day** external API cost for all agent and ML automation
- **~£15/month** total infrastructure

---

## What's Novel

1. **Bounded autonomy over observe-only** — most MLOps systems either auto-pilot everything or just log metrics. This system has per-module autonomy zones with hard limits. The margin tuner self-improves, but can never produce a margin outside 0.005–0.050 or step by more than 0.005 per cycle. The circuit breaker intervenes on failure but is invisible when healthy.

2. **Self-improving calibration without retraining** — the calibration pipeline continuously accumulates high-confidence measurements and recalculates percentiles. New percentiles go through metric-gated deployment (validation + rollback) and can be A/B tested with chi-squared significance before full rollout. The model stays frozen; the calibration evolves.

3. **Zero-cost agent organisation** — 30 agents with org structure, reporting lines, and scheduled workflows, all running within a single Claude Code subscription. No per-agent API cost. A full marketing department, engineering team, and patch cycle — all persona-driven.

4. **Statistical rigour in the deployment pipeline** — A/B testing with chi-squared significance feeds into metric-gated deployment with rollback. New calibrations are canary-tested on 10% of traffic, not yolo-deployed.

5. **Privacy-by-design monitoring** — the drift monitor tracks embedding distributions without storing embeddings. The calibration pipeline collects measurement statistics, not images. Usage intelligence flags patterns without storing PII. Biometric data flows through the system and out — it's never retained for monitoring purposes.
