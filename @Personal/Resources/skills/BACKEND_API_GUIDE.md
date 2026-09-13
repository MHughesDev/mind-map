---
name: backend-api-guide
description: Use when designing or building any backend service or API — choosing REST/GraphQL/tRPC/gRPC, structuring services, versioning, pagination, idempotency, rate limiting, error formats, webhooks, background jobs, or APIs consumed by LLM agents. Consult even if the user only says "build the server," "add an endpoint," or "connect the frontend to the backend."
version: 1.0.0
date: 2026-09-11
scope: Service architecture (monolith vs microservices), API style selection, versioning, pagination, idempotency, rate limiting, error design, webhooks, async jobs, event patterns, agent-consumable API design.
---

# BACKEND & API DESIGN GUIDE
### Drop-in rules file for coding agents building backend services and APIs

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Choose architecture (Part 1) and API style (Part 2) from the tables — do not debate beyond them without new evidence.
3. Implement the reliability primitives of Parts 3–5 (idempotency, pagination, errors, rate limiting) on every applicable endpoint — they are not optional polish.
4. Route all slow work through Part 6 (webhooks and jobs); nothing slow runs inline in a request.
5. If any LLM agent (yours or a customer's) will call the API, apply Part 7.
6. Walk the checklist (Part 9) before declaring done.

**Prime directive:** Build a modular monolith with boring, explicit, idempotent HTTP semantics. Extract services and add mechanisms only when a measured constraint demands it — the request/response contract is the product; keep it stable, typed, and honest.

---

## PART 0 — MENTAL MODEL

- Architecture follows organization: services exist to decouple teams and scaling domains, not to decorate diagrams. One team ≈ one deployable.
- A distributed system is a monolith plus network failures. Every service boundary adds latency, partial failure, and versioning burden — pay only when bought something.
- Mutations over a network are retried; therefore every mutating endpoint must be safe to call twice. Idempotency is a correctness requirement, not an optimization.
- Errors are part of the API contract. A machine-readable error is a feature; a stack trace is a leak.
- Webhooks and queues convert "slow and unreliable" into "eventually and reliably" — the request path stays fast because slow work never runs in it.
- APIs are now consumed by probabilistic callers (LLM agents). Explicitness, one-purpose endpoints, and actionable errors stop being style preferences and become reliability features.

**Never:**
1. Never start with microservices — extract from a modular monolith when a specific pain (independent scaling, release cadence, team bottleneck) is measured.
2. Never build a distributed monolith — services that must deploy together are the worst of both worlds.
3. Never expose tRPC as a public API — it couples clients to your TypeScript; public means REST + OpenAPI.
4. Never ship a mutating money/state endpoint without idempotency-key support.
5. Never store an idempotency record only on success — a crash then leaves no recovery path; persist the key before executing.
6. Never use offset pagination on large or live datasets — cost grows linearly and rows duplicate/skip under insert; use cursors.
7. Never return unbounded collections — every list endpoint has a default and max page size.
8. Never invent a bespoke error format — use RFC 9457 problem details (`application/problem+json`).
9. Never do slow work inline in a webhook handler — verify signature, enqueue, return 2xx immediately.
10. Never assume webhooks arrive ordered or exactly once — dedupe on event ID and reconcile against the source API.
11. Never version preemptively — `/v1` from day one, a second version only when a break is unavoidable.
12. Never build generic `/process` multiplexer endpoints — one endpoint, one purpose; both humans and agents misuse anything else.

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Architecture | Modular monolith, enforced module boundaries | A module needs independent scaling/release, or team coordination is the bottleneck → extract that service |
| Public API style | REST + OpenAPI spec | Complex multi-client data graph → GraphQL |
| Internal full-stack TS | tRPC | API goes public/polyglot → add REST |
| Service-to-service | Same-process calls | Extracted services with high throughput → gRPC |
| Versioning | URL path `/v1` | Large platform with many integrators → date-pinned versions |
| Pagination | Cursor; `limit` default 100, max 1000 | Small static/admin lists → offset acceptable |
| Idempotency | `Idempotency-Key` (UUID) on all mutating POSTs; server stores first response ~24h | Never remove |
| Errors | RFC 9457 problem+json everywhere | Never |
| Rate limiting | Per-user/tenant; 429 + `Retry-After` | Add sliding-window per-route tiers as abuse appears |
| Slow work | Background job queue | Never inline past ~1s of work |
| Webhook delivery (outbound) | Signed (HMAC on raw body), retried with backoff up to ~72h, at-least-once | Never |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Service architecture · Part 2 API style & versioning · Part 3 Idempotency · Part 4 Pagination, errors, rate limits · Part 5 Resource design · Part 6 Webhooks & async jobs · Part 7 APIs for LLM agents · Part 8 Build order · Part 9 Checklist

---

## PART 1 — SERVICE ARCHITECTURE

| Situation | Choice |
|---|---|
| New product, one team | Modular monolith: one deployable, internal modules with enforced boundaries (no cross-module imports except via module APIs) |
| One module measurably needs independent scaling or its own release cadence | Extract exactly that module as a service |
| Two-pizza-sized teams blocking each other on deploys | Split along team ownership lines |
| CPU/GPU-heavy or long-running work | Worker service consuming a queue — extract this early; it is the cheapest useful split |

Rules:
- Module boundaries inside the monolith mirror future service boundaries: separate schemas or table prefixes, explicit module APIs, no shared mutable internals — because extraction then becomes mechanical instead of a rewrite.
- Communicate between extracted services with explicit contracts (OpenAPI/protobuf), never shared database tables.
- Every extraction must name the constraint it relieves. "Cleaner" is not a constraint.

## PART 2 — API STYLE & VERSIONING

| Need | Choose |
|---|---|
| Public/third-party API, multiple client platforms | REST + OpenAPI (spec is source of truth; generate clients/docs from it) |
| Full-stack TypeScript monorepo, you control both ends | tRPC (end-to-end types, zero codegen) |
| Complex graph, many differing client views, large org | GraphQL (own the N+1 problem: dataloaders, depth/complexity limits) |
| Internal high-throughput service-to-service | gRPC |

Hybrids are normal: REST public + tRPC app-internal + gRPC service-to-service.

Versioning:
- `/v1` in the path from day one; additive changes (new optional fields, new endpoints) never bump versions.
- Breaking changes: additive-first (ship the new alongside the old), deprecation headers + dated sunset, then remove.
- Header-based versioning only for internal APIs, and send `Vary` on the version header or caching breaks.

## PART 3 — IDEMPOTENCY

- Client generates and persists an `Idempotency-Key` (UUID) BEFORE issuing any mutating POST, because generating it after the call defeats retry recovery.
- Server flow: (1) look up key — if a stored response exists, replay it verbatim; (2) if the key is mid-flight, return 409/425 rather than double-executing; (3) otherwise persist the key, execute, store status + body atomically with the business effect, return.
- Store records ~24h. Key + differing request body = reject (409), because silent divergence hides client bugs.
- After a 4xx, a client modifying the request must use a fresh key.
- Auth and rate-limit layers run before the idempotency layer — a 401/429 replayed later may legitimately produce a different result.
- Inbound webhook processing gets the same treatment via UNIQUE(event_id) in the same transaction as the business write (Part 6).

## PART 4 — PAGINATION, ERRORS, RATE LIMITS

Pagination:
- Cursor/keyset: return an opaque `next_cursor` + `has_more`; fetch `limit+1` rows to detect the next page cheaply.
- Params named `limit`, `after` (and `before` if bidirectional). Default 100, max 1000, enforced server-side.
- Cursors encode the sort key, so every paginated endpoint has a total, stable ordering (tiebreak on id).

Errors:
- RFC 9457 problem details on every error: `type` (stable URI you document), `title`, `status`, `detail`, `instance`, plus typed extensions (e.g., `errors[]` for field validation).
- `detail` must be actionable: what was wrong, what a valid value looks like. Never leak internals or stack traces.
- 400 malformed / 401 unauthenticated / 403 unauthorized / 404 absent-or-hidden / 409 conflict / 422 semantic validation / 429 rate limited / 5xx yours.

Rate limiting:
- Enforce per user AND per tenant (one tenant's burst must not starve others).
- Respond 429 with `Retry-After` (seconds). Standardized rate-limit headers are still in flux — verify current state before relying on any particular `RateLimit-*` scheme; `Retry-After` is the dependable signal.
- Give expensive AI/inference routes their own, tighter buckets (cross-reference SAAS_PRODUCT_GUIDE.md, Part 3 for spend-based quotas).

## PART 5 — RESOURCE DESIGN

- Nouns for resources, HTTP verbs for actions; explicit non-CRUD actions as sub-resources (`POST /invoices/{id}/finalize`), because "PATCH with magic status field" hides state machines.
- Consistent casing (pick snake_case or camelCase JSON once), consistent id fields (`user_id`, never bare ambiguous `id` in payload references), `timestamptz` ISO-8601 UTC everywhere.
- Requests validated at the edge against the schema; unknown fields rejected or explicitly ignored by policy, not by accident.
- Responses are stable contracts: additive evolution only; never repurpose a field's meaning.
- Long-running operations return `202` + an operation resource to poll (`GET /operations/{id}`), never a hanging request.

## PART 6 — WEBHOOKS & ASYNC JOBS

Inbound webhook handling (you receive):
- Verify the HMAC signature on the RAW request body before parsing, with a bounded timestamp tolerance (minutes, never disabled) — because parsed-then-reserialized bodies break signatures and replay protection.
- Thin handler: verify → enqueue → return 2xx fast (well under the sender's timeout). All business logic runs in the worker.
- Idempotent consumption: UNIQUE constraint on event id, inserted in the SAME transaction as the business effect.
- Never trust event ordering; on doubt, re-fetch the object from the sender's API — the API is the source of truth, the webhook is a hint.
- Separate secrets per environment (test/live).

Outbound webhooks (you send):
- Sign with HMAC over the raw body; include a timestamp; document verification.
- At-least-once delivery with exponential backoff over ~72h; expose delivery logs and a manual redrive to consumers.
- Include an event `id` and `type`; keep payloads thin (ids + summary) and let consumers fetch detail, because fat payloads fossilize your internal shapes.

Async jobs:
- Anything slower than ~1s of pure work (email, third-party syncs, LLM calls, media processing) goes to a queue with retries + dead-letter handling.
- Jobs are idempotent and parameterized by ids, not serialized objects, because payloads go stale in the queue.
- LLM calls are jobs par excellence: slow, failure-prone, cost-bearing — never inline them in a user request path without a streaming or 202-operation contract (see FRONTEND_UI_GUIDE.md, Part 6 for the streaming half).

## PART 7 — APIS FOR LLM AGENTS

When any LLM agent — your internal one or a customer's — will call the API:

- One clear purpose per endpoint/tool; explicit parameter names (`user_id`, not `id`); documented enums, ranges, defaults, and one example per operation.
- Descriptions written as operating instructions ("Use to … Requires … Returns … Side effects: …"), because the description is effectively a prompt.
- Provide consolidated, workflow-level operations for common multi-step flows (one `schedule_event` instead of three primitives), because each round-trip an agent must chain multiplies failure probability (see AGENT_HARNESS_GUIDE.md, Part 2, for the internal-tool version of this rule).
- Return high-signal fields (names alongside ids), support a `response_format`/verbosity option, and cap response sizes with pagination and truncation — agent context is scarce.
- Errors must state the fix in text ("`start_date` must be ISO-8601, e.g. 2026-09-11"), because agents recover from actionable errors and loop on opaque ones.
- Idempotency keys are mandatory here: agents retry aggressively.
- Publish machine-readable guidance (an `llms.txt`-style manifest and/or MCP tool definitions) stating preferred patterns and deprecated paths, because agent integrators propagate whatever the manifest says.
- Authenticate agents as first-class principals with scoped, revocable credentials — never a shared master key (see AUTH_SECURITY_GUIDE.md, Parts 3 and 6).

## PART 8 — BUILD ORDER

1. **Skeleton:** modular monolith, REST or tRPC per Part 2, OpenAPI spec, RFC 9457 errors, edge validation. *Exit bar: spec-driven; contract tests pass.*
2. **Reliability primitives:** idempotency keys on mutations, cursor pagination, per-tenant rate limits. *Exit bar: double-submitting any mutation is provably safe.*
3. **Async spine:** job queue + inbound/outbound webhooks per Part 6. *Exit bar: no request handler exceeds its latency budget doing slow work.*
4. **Agent surface (if applicable):** Part 7 applied; consolidated operations; manifest published. *Exit bar: an agent completes each core workflow in ≤2 tool calls.*
5. **Evolution:** deprecation policy, versioning playbook, first service extraction only when a Part 1 trigger fires.

## PART 9 — CHECKLIST

- [ ] Modular monolith with enforced module boundaries (or trigger-named extractions)
- [ ] API style matches Part 2 table; OpenAPI/contract is source of truth
- [ ] `/v1` path; additive evolution policy written down
- [ ] Idempotency keys on all mutating POSTs; keys persisted before execution; replay verbatim
- [ ] Cursor pagination with default 100 / max 1000 on every list
- [ ] RFC 9457 errors everywhere; details actionable; no internals leaked
- [ ] Per-user and per-tenant rate limits; 429 + Retry-After; tighter buckets on AI routes
- [ ] Webhook handlers: raw-body HMAC verify, thin enqueue-and-200, UNIQUE(event_id) dedupe, reconcile via API
- [ ] All slow work (including every LLM call) in the job queue with retries + DLQ
- [ ] Agent-facing surface follows Part 7; consolidated workflow operations exist
- [ ] Every service extraction names its measured trigger
