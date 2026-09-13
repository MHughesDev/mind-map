---
name: deployment-operations-guide
description: Use when deploying an application, setting up CI/CD, choosing hosting (PaaS vs containers vs Kubernetes), designing environments, adding observability/logging/metrics/tracing, feature flags, rollback strategy, or managing infra cost — including operating apps with LLM inference. Consult even if the user only says "ship it," "set up the pipeline," "why did prod break," or "hosting."
version: 1.0.0
date: 2026-09-11
scope: Deployment targets, CI/CD, branching, environments, release strategies (rolling/blue-green/canary), rollback, feature flags, infrastructure-as-code, observability, cost management, LLM-app operations.
---

# DEPLOYMENT, DEVOPS & OPERATIONS GUIDE
### Drop-in rules file for coding agents shipping and operating applications

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Choose the deployment target from Part 1's ladder — enter at the lowest rung that fits; climb only on a named trigger.
3. Stand up the pipeline and environments of Part 2 before feature work accelerates — retrofitting CI onto momentum is costlier.
4. Every release follows Part 3 (strategy) and Part 4 (rollback): rollback criteria are written BEFORE deploying, never during the incident.
5. Instrument per Part 6 from the first deploy; an unobserved service is undebuggable by definition.
6. If the app calls LLMs, apply Part 7's cost-and-durability rules.
7. Walk the checklist (Part 9) before declaring done.

**Prime directive:** Deploy small changes continuously from trunk through an automated pipeline to a boring platform, with rollback criteria written in advance and telemetry that can answer "what changed and what broke" in one query. Operational sophistication is added by trigger, never by ambition.

---

## PART 0 — MENTAL MODEL

- Deployment frequency and failure recovery are the health metrics of engineering: small, frequent, reversible releases beat large, rare, careful ones because small diffs localize blame.
- The platform ladder is one-way and expensive to climb: every rung (PaaS → containers → orchestration) trades convenience for control. Take control only when a constraint demands it.
- A deploy is not done when the code is out; it is done when telemetry says the release is healthy against predefined criteria.
- Feature flags decouple deploy (moving code) from release (exposing behavior) — this separation is what makes trunk-based development and instant mitigation possible.
- An untested rollback is not a plan; it is a hope. Rollback is a rehearsed mechanism plus pre-written triggers.
- Observability is three joined views of one event stream — logs (what happened), traces (where time went), metrics (how much/how often) — correlated by trace id or they are three silos.

**Never:**
1. Never adopt Kubernetes before a named scale/control/compliance trigger and someone to operate it — the overhead is permanent.
2. Never keep long-lived feature branches — branches live under ~24 hours; integrate behind flags.
3. Never deploy manually or from a laptop — the pipeline is the only path to production.
4. Never deploy without predefined rollback criteria and a rehearsed rollback mechanism.
5. Never run a canary on traffic too thin for significance — a low-traffic service canary detects nothing; use blue-green or rolling instead.
6. Never roll back a release involving schema changes without the expand-contract discipline already in place (DATA_LAYER_GUIDE.md, Part 3) — data makes naive rollback destructive.
7. Never instrument with vendor-proprietary SDKs when open telemetry standards exist — portability of telemetry is leverage over vendors.
8. Never log unsampled everything — logs cost multiples of metrics; sample noise, keep errors and security events.
9. Never let flags rot — a flag's definition of done is its removal; review flags on a schedule.
10. Never share mutable infrastructure state by clicking in consoles — infrastructure is code, reviewed and versioned.
11. Never ship secrets in images or pipelines — inject at runtime from the secrets manager (AUTH_SECURITY_GUIDE.md, Part 4).
12. Never treat LLM spend as invisible COGS — token cost per feature per tenant is a first-class production metric.

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Hosting | PaaS (git-push deploys, managed DB) | Regional control/GPUs/custom runtime → containers platform; org-scale multi-team + platform team → Kubernetes |
| Branching | Trunk-based; branches < 24h; merge queue | Regulated release trains → release branches, still short-lived |
| Environments | dev → preview-per-PR → staging → prod | — |
| CI gates | Lint, typecheck, tests, build, secret scan, dependency scan | Add contract/e2e/a11y/perf gates as surfaces appear |
| Release strategy | Rolling (low traffic) / blue-green (atomic swap) | High traffic + good telemetry → canary 1→5→25→50→100%, 5–10 min bake per step |
| Rollback criteria | Written pre-deploy (e.g., 5xx > 2× baseline for 5 min, or p95 latency +25%) | Tune thresholds per service baseline |
| Feature flags | For every user-visible change; two-stage cleanup; quarterly sweep | — |
| IaC | All infra in code from the second environment onward | — |
| Telemetry | Structured JSON logs + traces + metrics, one trace id through all; collector-based export | — |
| On-call/incidents | Alert on symptoms (user-facing SLO breaches), runbook per alert | — |
| LLM ops | Token spend + latency + failure per feature/tenant as standard metrics; durable execution for long agent runs | — |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Platform ladder · Part 2 Pipeline, branching, environments · Part 3 Release strategies · Part 4 Rollback · Part 5 Feature flags & IaC · Part 6 Observability · Part 7 Operating LLM apps · Part 8 Build order · Part 9 Checklist

---

## PART 1 — PLATFORM LADDER (enter low, climb on trigger)

| Situation | Target |
|---|---|
| Frontend / meta-framework app | Frontend PaaS with preview deploys |
| Full-stack MVP (API + DB + workers + cron) | Full-stack PaaS (one project, managed Postgres/Redis) |
| Need regional placement, GPUs, custom runtimes, scale-to-zero containers | Container platform |
| Event-driven glue, spiky workloads | Serverless functions (mind timeout ceilings — Part 7) |
| Many teams, platform engineers on staff, compliance-driven control | Kubernetes |

Rules:
- The PaaS rung is not training wheels; it is the correct rung until a trigger fires. Name the trigger in writing when climbing.
- Whatever the rung: the app is containerizable, config comes from environment, state lives in managed services — because this keeps every higher rung reachable without rewrite.
- Prefer managed databases/queues/storage at every rung; self-operate stateful systems only with a dedicated reason and owner.

## PART 2 — PIPELINE, BRANCHING, ENVIRONMENTS

- Trunk-based development: small PRs off main, merged within a day, gated by a merge queue running the full pipeline — long-lived branches are where integration pain compounds silently.
- Pipeline stages, all automated: lint/typecheck → unit + integration tests → build artifact once → scan (secrets, dependencies) → deploy staging → smoke → deploy prod (per Part 3). The artifact promoted is the artifact tested — never rebuilt between environments.
- Preview environment per PR (app + isolated or branched data), because reviewing running behavior beats reviewing diffs.
- Staging mirrors production topology (same platform, same env-var shape, masked data) — a staging that differs structurally validates nothing.
- Configuration via environment; the same artifact runs everywhere.

## PART 3 — RELEASE STRATEGIES

| Situation | Strategy |
|---|---|
| Low traffic, tolerant of brief mixed versions | Rolling |
| Need atomic cutover/rollback, can afford double capacity briefly | Blue-green |
| High traffic + real-time telemetry + defined health metrics | Canary: 1% → 5% → 25% → 50% → 100%, bake 5–10 min per step against the rollback criteria |

Rules:
- Zero-downtime is a schema discipline first: only expand-contract-compatible releases (DATA_LAYER_GUIDE.md, Part 3) can roll safely in any strategy.
- Canary steps advance only on green criteria; any red halts and rolls back automatically where possible.
- A service without enough traffic to make a canary step statistically meaningful uses blue-green instead — a silent canary is false confidence.

## PART 4 — ROLLBACK

- Criteria are written before the deploy, mechanically checkable, and tied to the release: error-rate multiple over baseline, latency regression bound, key business transaction failure. Deciding thresholds mid-incident is how bad calls get made.
- The mechanism is rehearsed in staging on a schedule: redeploy previous artifact (rolling), swap back (blue-green), or kill the flag (fastest of all — prefer flag-off as first response when the change is flagged).
- Stateful rollbacks get a data plan: written-in-new-format data must be readable by the old version (expand-contract guarantees this) or the rollback includes a cleanup step.
- After any rollback: blameless incident note — trigger, detection time, mitigation time, and the gap it revealed.

## PART 5 — FEATURE FLAGS & IAC

Flags:
- Every user-visible change ships behind a flag; deploy dark, release by percentage/cohort/tenant.
- Naming carries metadata (`release_`, `experiment_`, `ops_` prefixes + owner + date); one behavior per flag — mega-flags make rollback ambiguous.
- Cleanup is two-stage (remove code references, then archive the flag) and scheduled — a quarterly sweep at minimum, because dead flags are live complexity.
- Flags gate behavior, never security: authorization stays in the auth layer (AUTH_SECURITY_GUIDE.md, Part 3).

Infrastructure as code:
- From the moment there are two environments, all infra (services, DNS, buckets, queues, alert rules) is declared in code, reviewed in PRs, applied by the pipeline — console clicks create unrecorded drift by definition.
- One stack definition parameterized per environment; state stored remotely and locked.

## PART 6 — OBSERVABILITY

- Instrument with the open telemetry standard (traces + metrics + logs through a collector), because vendor-neutral instrumentation makes backends swappable and negotiable.
- Structured JSON logs with `timestamp, level, service, trace_id, tenant_id` on every line; request-scoped context propagated — a log line without a trace id is an orphan.
- Trace every inbound request and outbound dependency call; span the expensive interior steps (DB, cache, queue, LLM calls — Part 7).
- Metrics: the golden four per service (traffic, errors, latency distribution, saturation) + business counters that matter (signups, jobs completed, tokens spent).
- Logs are the expensive pillar: sample verbose levels, always keep warnings/errors/security events; retention per class, not one blanket.
- Alert on user-facing symptoms against SLOs (availability, latency), not on every cause metric — cause-alerts page humans for machines' problems. Every alert links a runbook.
- Track the four delivery metrics (deploy frequency, lead time, change-failure rate, time-to-restore) monthly — they are the pipeline's own health check; verify current-year framing of any external benchmark before comparing.

## PART 7 — OPERATING LLM APPS

Cost:
- Token spend is a standard metric dimensioned by feature, model, and tenant, with budget alerts — because inference is the rare COGS a deploy can 10× silently.
- Per-tenant spend caps enforced in the app before inference (AUTH_SECURITY_GUIDE.md, Part 6; billing linkage in SAAS_PRODUCT_GUIDE.md, Part 3).
- Route through a gateway layer you control (yours or managed) for provider fallback, model pinning, and rate-limit smoothing — one provider incident must not be your incident.

Durability:
- Agent runs and long generations exceed serverless timeout ceilings; run them as durable jobs/workflows with checkpoint-resume, never as stretched HTTP requests (AGENT_HARNESS_GUIDE.md, Part 15; queue mechanics in BACKEND_API_GUIDE.md, Part 6).
- Every model and tool call is a traced span with tokens, latency, and outcome — an agent run must replay as a trace or it cannot be debugged.
- Pin model versions in config, not code; treat a model/prompt change as a release: flagged, canaried against eval metrics, rollback-able (evals per AGENT_HARNESS_GUIDE.md, Part 6).
- Degrade gracefully: on provider failure or budget exhaustion, fall back per the degradation ladder (AGENT_HARNESS_GUIDE.md, Part 7) and tell the user honestly.

## PART 8 — BUILD ORDER

1. **Ship path:** PaaS, git-based deploys, prod + staging, env-var config, secrets injected. *Exit bar: main deploys to prod through the pipeline only.*
2. **Pipeline depth:** full CI gates, preview envs per PR, trunk-based with merge queue. *Exit bar: no human-pushed artifacts; branch age p95 < 24h.*
3. **Release safety:** flags on user-visible changes, zero-downtime strategy per Part 3, rollback criteria template + rehearsal. *Exit bar: a rollback has been executed in staging on purpose.*
4. **Sight:** telemetry per Part 6 live; SLOs + symptom alerts + runbooks; delivery metrics visible. *Exit bar: one query answers "what changed and what broke."*
5. **Scale & spend:** IaC everywhere, canary where traffic supports it, cost dashboards (including tokens), incident review loop running.

## PART 9 — CHECKLIST

- [ ] Platform rung chosen from Part 1; any climb has a written trigger
- [ ] Trunk-based; branches <24h; merge queue; pipeline is the only deploy path
- [ ] Artifact built once, promoted unchanged; config from environment
- [ ] Preview env per PR; staging mirrors prod topology
- [ ] Release strategy per Part 3; canary only with sufficient traffic
- [ ] Rollback criteria written pre-deploy; mechanism rehearsed; flag-off preferred first response
- [ ] Flags named/owned; two-stage cleanup; quarterly sweep scheduled
- [ ] All infra in code, reviewed, pipeline-applied; no console drift
- [ ] Structured logs + traces + metrics correlated by trace id; collector-based export
- [ ] SLO symptom alerts with runbooks; log sampling + retention per class
- [ ] Delivery metrics tracked monthly
- [ ] LLM: token spend metered per feature/tenant with caps; gateway fallback; durable long runs; model changes released like code
