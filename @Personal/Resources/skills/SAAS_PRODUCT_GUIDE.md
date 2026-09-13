---
name: saas-product-guide
description: Use when building SaaS product mechanics — multi-tenancy, subscriptions, billing, usage-based/metered pricing, entitlements, quotas and free tiers, onboarding, admin panels, notifications, product analytics, or compliance basics. Consult even if the user only says "charge customers," "add plans," "workspaces/teams," "limit the free tier," or "meter AI usage."
version: 1.0.0
date: 2026-09-11
scope: Multi-tenancy models, billing and subscriptions, usage metering, entitlements and quota enforcement, AI-cost pricing, onboarding, admin surface, notifications, analytics, GDPR/SOC 2 awareness.
---

# SAAS PRODUCT PATTERNS GUIDE
### Drop-in rules file for coding agents building SaaS product mechanics

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Decide tenancy (Part 1) before the second table exists — it is the least retrofittable decision in SaaS.
3. Build billing per Part 2 with the webhook and reconciliation discipline intact — this is where revenue silently leaks.
4. If any feature has real marginal cost (LLM inference above all), implement Part 3's metering/entitlement/billing separation before exposing the feature.
5. Ship the product shell of Part 4 (onboarding, admin, notifications, analytics) deliberately, not accidentally.
6. Walk the checklist (Part 7) before declaring done.

**Prime directive:** Tenant isolation from the first migration, billing state reconciled from the provider as source of truth, and — for anything with real marginal cost — enforcement BEFORE the cost is incurred, not after the invoice. Meter, entitle, and bill as three separate concerns.

---

## PART 0 — MENTAL MODEL

- Tenancy is a spectrum you re-decide per tenant, not a one-time global choice: shared for the many, isolated for the few who pay for it. What must be global is the discipline (tenant_id everywhere) that makes per-tenant moves possible.
- Billing is distributed-systems programming with money: webhooks arrive late, duplicated, and unordered; your subscription state is a cache of the provider's truth and must be reconcilable at any time.
- Metering (what happened), entitlement (is this allowed now), and billing (what to charge) are three systems. Fusing them is why AI free tiers hemorrhage money: the invoice is later, the GPU bill is now.
- Usage events are financial records: append-only, immutable, idempotent — an editable usage table is an un-auditable one.
- Flat pricing and spiky AI usage are incompatible at the margin; expensive features trend toward metered/credit models with hard caps.
- The unsexy shell — onboarding, admin panel, emails, analytics — is where activation, support cost, and churn actually live.

**Never:**
1. Never launch without tenant_id on tenant-owned tables and row-level enforcement — retrofitting isolation costs multiples of building it in.
2. Never treat tenancy as settled once — design so one tenant can be moved to higher isolation without a rewrite.
3. Never run the shared tier without noisy-neighbor limits (per-tenant rate/connection/job caps).
4. Never bury data residency in infra config — region is a tenant attribute decided at tenant creation.
5. Never gate expensive usage on billing-cycle math — entitlement checks run synchronously in the request path, before cost is incurred.
6. Never write billing webhook handlers that aren't idempotent and signature-verified — duplicated events double-grant and double-charge.
7. Never trust your local subscription cache over the provider — reconcile on webhook and on schedule; the provider API is truth.
8. Never emit one metering event per action at high volume — accumulate and flush aggregates; per-action emission melts rate limits and budgets.
9. Never offer an uncapped free tier on a feature with real marginal cost — hard caps, then upgrade paths.
10. Never surprise customers with overage — usage visible in-app, alerts before caps, grace behavior defined.
11. Never hand-roll subscription proration/tax/dunning — the billing provider's job; yours is state mapping and entitlements.
12. Never defer deletion/export obligations — erasure and export paths are features built early, because retrofits touch every store (including embeddings — DATA_LAYER_GUIDE.md, Part 7).

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Tenancy | Shared schema + tenant_id + RLS | Compliance/residency/noisy-neighbor or big-ticket tenant → schema- or DB-per-tenant for that tenant |
| Tenant model | Org/workspace object owns membership, roles, billing | — |
| Billing provider | Hosted checkout + provider-managed subscription lifecycle | High-volume/complex usage pricing → dedicated metering/entitlement layer |
| Pricing shape | Flat tiers for capacity; metered/credits for real-marginal-cost features | AI margins break under flat → prepaid credits + caps |
| Usage pipeline | Append-only events → aggregate in fast store → flush to biller | — |
| Entitlement checks | Synchronous, cached (memory/Redis), in request path pre-cost | — |
| Free tier (AI features) | Hard-capped units + cheaper model + visible remaining quota | — |
| Webhooks (billing) | Signature-verified, idempotent by event id, reconciled against API | Never relax |
| Compliance floor | Audit log, access controls, deletion + export paths, DPAs with model providers | Enterprise motion → formal certification work |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Multi-tenancy · Part 2 Billing & subscriptions · Part 3 Metering, entitlements, AI cost · Part 4 Product shell · Part 5 Compliance basics · Part 6 Build order · Part 7 Checklist

---

## PART 1 — MULTI-TENANCY

| Need | Model |
|---|---|
| Early product, many small tenants, cost efficiency | Shared schema: tenant_id on every tenant-owned table + row-level security as backstop |
| Per-tenant customization, moderate isolation | Schema-per-tenant |
| Strict isolation, data residency, compliance, whale tenants | Database-per-tenant (region-pinned) |
| Real portfolio | Hybrid: shared default + promoted tenants — isolation is a per-tenant, revisitable decision |

Rules:
- Tenant context derives from the authenticated session server-side on every request — never from a client-supplied tenant id (enforcement partners: AUTH_SECURITY_GUIDE.md Part 3; DATA_LAYER_GUIDE.md Part 2).
- Application queries are tenant-scoped by construction (scoped repositories/middleware); RLS exists to catch the query someone forgets.
- Model tenants as organizations from day one — personal accounts are single-member orgs — because bolting teams onto user-rooted data is a schema rewrite.
- Noisy-neighbor controls on the shared tier: per-tenant rate limits, connection ceilings, queue fairness, storage quotas.
- Region is a first-class tenant field chosen at creation; residency promises are only keepable if data placement keys off it.
- Cross-tenant leakage is the reputation-ending bug class: isolation tests (user A provably cannot reach tenant B's objects by id) run in CI permanently.

## PART 2 — BILLING & SUBSCRIPTIONS

- Use the provider's hosted checkout and customer portal — card handling, tax, SCA, dunning are their liability and competence; you map state and enforce entitlements.
- Local mirror: `customer_id`, `subscription_id`, plan/price ids, status, current-period end — a cache of provider truth, refreshed by webhook and reconciled on schedule (nightly sweep), because missed webhooks otherwise fossilize wrong state.
- Webhook discipline in full (mechanics in BACKEND_API_GUIDE.md, Part 6): raw-body signature verification, UNIQUE(event_id) idempotency in the same transaction as the state change, no ordering assumptions — on conflict, re-fetch the subscription from the API and overwrite.
- Entitlement flips (upgrades, downgrades, cancellations, payment failure grace) are driven by subscription status transitions in one place — a single `sync_subscription(tenant)` function — not scattered event-specific hacks.
- Migrations of live pricing use versioned prices: grandfather existing subscriptions, sell new prices — never mutate a price in place.
- Test-mode and live-mode credentials, webhooks, and data never mix.

## PART 3 — METERING, ENTITLEMENTS & AI COST

Three separated concerns:
1. **Metering (record):** append-only usage events — tenant, user, feature, units (tokens/actions/seconds), timestamp, idempotency key. Immutable, because they are financial records and eval data at once.
2. **Entitlement (allow?):** synchronous check in the request path BEFORE incurring cost — cached limits (memory/Redis) so the check adds milliseconds, hard-failing closed on exhausted quota, honestly messaged in the UI.
3. **Billing (charge):** aggregates flushed to the provider's metering on an interval; invoices derive from provider aggregation; disputes resolve from your immutable event log.

Rules:
- High-volume paths accumulate usage in a fast store and flush aggregated events on interval — per-action emission to the biller fails at scale.
- For LLM features, prefer prepaid credits or hard-capped allowances over pure postpaid metering, because postpaid means you front the inference cost and eat it when the invoice fails. Deferred billing without caps is unbounded financial exposure.
- Meter what maps to customer value AND correlates with your cost (tokens, agent runs, documents processed); model-multiplier credits let one meter cover heterogeneous model costs.
- Free tier with real marginal cost: hard unit caps + automatic cheaper-model routing + visible remaining quota + clean upgrade path. Model downgrade beats service denial; denial beats silent overspend (degradation philosophy shared with AGENT_HARNESS_GUIDE.md, Part 7).
- Usage visibility is churn prevention: an in-app usage dashboard, threshold alerts (e.g., 80%), and defined at-cap behavior — block, degrade, or metered overage — stated before it happens.
- Spend guardrails stack with security-side caps (AUTH_SECURITY_GUIDE.md, Part 6) and ops-side token metrics (DEPLOYMENT_OPERATIONS_GUIDE.md, Part 7): three nets, one goal — no invisible inference spend.

## PART 4 — PRODUCT SHELL

Onboarding:
- Route every new user to one defined activation moment (the action after which retention jumps — define it, instrument it); collect only what that path needs, defer the rest.
- Invites/team-join flows handle the signed-out, signed-in-wrong-account, and existing-member cases explicitly — invite edge cases are a classic support sinkhole.

Admin surface:
- An internal admin panel from early: tenant lookup, subscription state, entitlement view, feature-flag overrides, usage view, impersonation with consent + audit trail — because support without it becomes engineering interrupts.
- Admin actions are privileged API calls through the same authorization layer, fully audit-logged — never raw DB edits.

Notifications:
- Transactional email via a provider from day one (verification, invites, receipts, resets); every notification idempotent (send-once keys) and event-driven off the job queue (BACKEND_API_GUIDE.md, Part 6).
- Notification preferences and unsubscribe honored per category from the start — retrofitting preference plumbing touches every send site.

Analytics:
- Instrument the handful of events that map the funnel (signup → activation → habitual use → conversion) with consistent naming and tenant/user dimensions; a few reliable events beat an ocean of unnamed ones.
- Product analytics and billing metering are separate pipelines — analytics may sample and drop; billing may not.

## PART 5 — COMPLIANCE BASICS (awareness floor)

- Data inventory: know what personal data lives where (including logs, backups, embeddings, model-provider retention) — every obligation below depends on this map.
- User deletion and export paths implemented as real features reaching all stores; data-processing agreements with subprocessors (model providers included); privacy policy reflecting actual AI data flows.
- Access controls + audit logging (AUTH_SECURITY_GUIDE.md, Part 5) double as certification groundwork; keep evidence-friendly habits (change control via PRs, access reviews) from the start so later formal audits are documentation, not archaeology.
- Enterprise deals will ask for SSO, audit logs, residency, and certifications — the architecture choices in Parts 1–2 of this guide and AUTH_SECURITY_GUIDE.md, Part 1 are what make "yes" cheap.

## PART 6 — BUILD ORDER

1. **Tenancy spine:** org model, tenant_id everywhere, RLS backstop, tenant-scoped queries, isolation tests in CI. *Exit bar: cross-tenant access provably fails.*
2. **Money loop:** hosted checkout, subscription mirror + `sync_subscription`, verified idempotent webhooks, nightly reconciliation, entitlement gating on plan. *Exit bar: replaying every webhook twice changes nothing; kill a webhook for a day and reconciliation heals it.*
3. **Shell:** activation-focused onboarding, transactional email, admin panel with audit-logged impersonation, funnel analytics. *Exit bar: support can resolve a billing question without engineering.*
4. **Metered value (AI features):** usage events → aggregation → flush; synchronous cached entitlement checks; credits/caps; usage dashboard + alerts. *Exit bar: quota exhaustion blocks BEFORE inference; usage never surprises the customer.*
5. **Scale & trust:** per-tenant isolation promotions, residency handling, deletion/export complete, evidence-friendly ops, noisy-neighbor tuning.

## PART 7 — CHECKLIST

- [ ] Org/workspace tenant model; tenant_id on all tenant-owned tables; RLS backstop
- [ ] Tenant context from session server-side; isolation tests in CI
- [ ] Noisy-neighbor limits on shared tier; region as tenant field
- [ ] Hosted checkout + portal; subscription mirror with single sync function
- [ ] Billing webhooks: signature-verified, idempotent, unordered-safe; nightly reconciliation
- [ ] Prices versioned; grandfathering strategy; test/live separation absolute
- [ ] Usage events append-only + idempotent; aggregation before flush
- [ ] Entitlement checks synchronous, cached, pre-cost, fail-closed, honestly messaged
- [ ] AI features: credits or hard caps; model-downgrade path; usage dashboard + 80% alerts
- [ ] Onboarding drives one instrumented activation moment; invite edge cases handled
- [ ] Admin panel with audited impersonation; no raw DB support edits
- [ ] Notifications idempotent, queued, preference-aware
- [ ] Deletion + export reach all stores including embeddings; DPAs cover model providers
