---
name: auth-security-guide
description: Use when implementing login, authentication, sessions, tokens, OAuth, SSO, permissions, roles, authorization, secrets handling, or securing an app that contains LLM features or agents. Consult even if the user only says "add users," "protect this route," "API keys," or "is this safe."
version: 1.0.0
date: 2026-09-11
scope: Authentication methods (passkeys, magic links, OAuth 2.1, SSO), sessions vs JWT, authorization models (RBAC/ABAC/ReBAC), secrets management, API security, LLM/agent security (prompt injection, excessive agency, provider keys, spend abuse).
---

# AUTH & SECURITY GUIDE
### Drop-in rules file for coding agents implementing authentication, authorization, and app security

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Choose authentication per Part 1 and session mechanics per Part 2 — from the tables, not from habit.
3. Enforce Part 3 on every endpoint: authorization is per-resource, per-request, no exceptions.
4. Apply Part 4 (secrets) and Part 5 (API security) as build-time requirements, not launch-week patches.
5. If the app contains any LLM feature or agent, Part 6 is mandatory, not optional.
6. Walk the checklist (Part 8) before declaring done.

**Prime directive:** Authenticate with passwordless-first via a managed provider; authorize every single resource access server-side; treat all LLM input as attacker-controllable and all LLM output as untrusted. Security is enforced where the data lives, never where the UI suggests.

---

## PART 0 — MENTAL MODEL

- Authentication answers "who is this"; authorization answers "may they do this to THIS object." Most real breaches are authorization failures on individual objects, not exotic crypto breaks.
- Auth is undifferentiated heavy lifting: a managed identity provider gives passkeys, SSO, MFA, and audit logs on day one. Build your own only if identity IS the product.
- Sessions you can revoke beat tokens you must wait out. Statelessness is a scaling tool, not a default virtue.
- Secrets follow gravity: anything in client code, repos, or logs is public. Design as if it already leaked.
- An LLM processes instructions and data in one channel; nothing fully separates them. Therefore prompt injection is not solvable by filtering — only survivable by limiting what an injected model can do.
- The agent security budget goes to blast-radius reduction: least-privilege tools, gates on irreversible actions, spend caps.

**Never:**
1. Never launch password-only auth on a new system — passkeys primary, magic-link fallback.
2. Never store tokens in localStorage or expose sessions to JS — HTTP-only, Secure, SameSite cookies.
3. Never trust the JWT `alg` header or accept `none` — pin the algorithm server-side.
4. Never issue long-lived access tokens without rotation and a revocation strategy.
5. Never skip the per-object ownership check (the classic broken-object-level-authorization hole): every request verifies the caller may act on that specific resource id.
6. Never model per-object sharing as roles — role explosion; use relationships (Part 3).
7. Never commit secrets to source or ship them in env files to clients — secrets manager only.
8. Never execute, render as HTML, or SQL-interpolate LLM output — it is untrusted input from a possibly-injected model.
9. Never give an agent broader permissions than the current task needs, and never let an autonomous agent hold wider standing permissions than an interactive one.
10. Never let untrusted content (web pages, emails, uploaded docs, retrieved chunks) enter a prompt unlabeled — wrap and mark it as data.
11. Never expose model-provider API keys client-side; all inference calls go through your server.
12. Never deploy an LLM feature without per-user/tenant spend and rate caps — unbounded consumption is an attack class of its own.

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Auth methods | Passkeys (WebAuthn) primary + email magic-link fallback; password optional | High-assurance tenants → require user verification on passkeys |
| Provider | Managed identity provider | Identity is your product → build |
| First-party web sessions | Server-side session (Redis/DB) + HTTP-only cookie | Edge/serverless hot path → short-lived JWT |
| API/mobile/third-party | JWT access 15–60 min + refresh-token rotation | Never lengthen without revocation plan |
| Third-party & agent authorization | OAuth 2.1 with PKCE (S256) | Never downgrade |
| Enterprise SSO | OIDC + SAML both supported (buy, don't build) | — |
| Authorization model | RBAC + mandatory per-object ownership checks | Sharing/hierarchies → add ReBAC; contextual rules → add ABAC; cross-service policy → policy engine |
| Secrets | Secrets manager, short-lived creds, rotation | Never |
| Password storage (if kept) | argon2id (or bcrypt), breach-checked, no composition rules | Never |
| LLM output handling | Untrusted: sanitize before render, never execute | Never |
| Agent permissions | Per-task least privilege + human gate on irreversible/expensive actions | Never widen without a risk review |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Authentication · Part 2 Sessions & tokens · Part 3 Authorization · Part 4 Secrets · Part 5 API security · Part 6 LLM & agent security · Part 7 Build order · Part 8 Checklist

---

## PART 1 — AUTHENTICATION

| Situation | Choice |
|---|---|
| New consumer/B2B app | Passkeys primary, magic-link fallback, via managed provider |
| Enterprise customers | Add OIDC + SAML SSO (procurement asks for SAML by name), SCIM if they ask for user provisioning |
| CLI/device flows | OAuth device authorization flow |
| Machine/agent clients | OAuth 2.1 client credentials with narrow scopes (Part 6) |

Rules:
- OAuth 2.1 posture everywhere: authorization-code + PKCE (S256) mandatory, no implicit flow, no password grant, exact redirect-URI matching.
- If passwords exist at all: argon2id hashing, breach-list checking, length over composition rules, rate-limited attempts with progressive delays.
- MFA available from day one (the provider gives it free); step-up authentication for dangerous actions (payout changes, key generation, data export).
- Email flows (magic link, reset): single-use, short-expiry tokens, constant-time comparison, no account-existence oracle in responses.

## PART 2 — SESSIONS & TOKENS

| Situation | Choice |
|---|---|
| First-party web app | Server session in Redis/DB; HTTP-only, Secure, SameSite=Lax cookie |
| Mobile / third-party API / service-to-service | JWT access token 15–60 min + rotating refresh token |
| Serverless/edge hot path where a session lookup is too slow | Short-lived JWT; accept the revocation lag consciously |

Rules:
- Server sessions are the default because instant revocation, session listing, and "log out everywhere" are product requirements sooner than horizontal statelessness is.
- JWTs: pin algorithm, validate `iss`/`aud`/`exp` always, keep claims minimal (no PII), key rotation via JWKS.
- Refresh-token rotation with reuse detection: a replayed old refresh token revokes the whole family, because replay means theft.
- CSRF: SameSite cookies + framework CSRF tokens on state-changing form posts; CORS allowlist exact origins, never `*` with credentials.

## PART 3 — AUTHORIZATION

Layered model — start coarse, add precision where the product demands it:

| Access depends on | Model |
|---|---|
| User's static role in the org/tenant | RBAC (roles: e.g., owner/admin/member/viewer) |
| Attributes and context (department, resource state, time, amount) | ABAC conditions layered on RBAC |
| Relationships: sharing, folders, hierarchies, cross-tenant grants | ReBAC (relationship tuples, graph checks) |
| Many services needing one policy source | Externalized policy engine, policy-as-code |

Rules:
- The non-negotiable core is object-level authorization: every request that touches a resource verifies the caller's right to THAT id (ownership or explicit grant), server-side, after authentication. This is the single most common real-world API hole.
- Deny by default; authorization decisions live in one module/service, not scattered inline, because scattered checks drift and diverge.
- Roles for coarse grants + relationships/attributes for fine conditions is the stable end-state pattern; migrate toward it, don't leap.
- Multi-tenant: tenant_id scoping enforced in the data layer (RLS as backstop — see DATA_LAYER_GUIDE.md, Part 2) AND checked in the authorization layer; two independent nets.
- Log authorization denials with actor, object, and reason — they are your intrusion smoke detector.

## PART 4 — SECRETS

- All secrets in a secrets manager; injected at runtime; never in code, client bundles, images, or tickets.
- Short-lived, auto-rotated credentials preferred over static keys; per-environment isolation (dev secrets never open prod doors).
- Scan repos and CI for committed secrets continuously; a leaked secret is rotated immediately, not assessed.
- Model-provider keys are crown jewels: server-side only, one key per environment, usage-monitored, spend-alerted (Part 6).

## PART 5 — API SECURITY

- Validate every input at the edge against a schema (types, ranges, lengths); parameterized queries only — string-built SQL is prohibited even for "internal" values.
- Encode output per context (HTML, attribute, URL, JS) — applies doubly to LLM-generated text (Part 6).
- Rate limiting per user and per tenant with 429 + Retry-After (mechanics in BACKEND_API_GUIDE.md, Part 4); stricter buckets on auth endpoints and AI routes.
- Security headers as baseline: CSP, HSTS, X-Content-Type-Options, frame-ancestors.
- Audit log for security-relevant events (logins, permission changes, key operations, exports): append-only, actor + object + timestamp + origin.
- Dependency and image scanning in CI; patch cadence defined; fail builds on known-critical vulnerabilities.

## PART 6 — LLM & AGENT SECURITY

Threat model in one line: anyone who can get text in front of your model can try to steer it; anything the model can do, an attacker can attempt through it; anything it can see, an attacker can attempt to exfiltrate.

Prompt injection (direct and indirect):
- Assume any retrieved/uploaded/scraped content contains adversarial instructions. Wrap untrusted content in explicit data delimiters, tag provenance, and instruct the model that content inside is data, not commands — this lowers, never eliminates, risk.
- Because prevention is partial, put the real defense downstream: what can an injected model actually do? Minimize that.

Least privilege and blast radius:
- Tools scoped per task: read-only variants preferred; write/delete/spend tools gated; per-tenant data boundaries enforced in the tool implementation, never by trusting model-supplied filters (the harness-side twin of this rule lives in AGENT_HARNESS_GUIDE.md, Part 14).
- Never combine, ungated, in one agent: access to private data + exposure to untrusted content + an outbound channel (web, email, code execution). Cut or human-gate one leg.
- Human approval for irreversible or expensive actions (sends, deletes, payments, deploys, bulk writes); approvals are logged with the exact proposed action.
- Autonomous/background agents get NARROWER standing permissions than interactive ones, because no human is watching in the moment.

Output handling:
- LLM output is untrusted input to every downstream system: sanitize before HTML render (XSS via model), parameterize before DB, never eval/exec outside a sandbox, validate against schema before acting on structured output.
- Filter/moderate output surfaces that reach other users, because a prompt-injected model is an attacker's printing press into your UI.

Sensitive data and system prompts:
- Minimize secrets and PII entering prompts; assume anything in context can be extracted by a determined user. System prompts are configuration, not secrets — nothing confidential goes in them.
- Redact/limit PII into third-party model APIs per your data agreements; log prompts/completions with the same protection class as the data they contain.

Consumption abuse:
- Per-user and per-tenant rate + token + spend caps enforced BEFORE inference runs; hard monthly caps with alerts (billing mechanics in SAAS_PRODUCT_GUIDE.md, Part 3).
- Cap agent loop steps, tool calls, and recursion in the harness (AGENT_HARNESS_GUIDE.md, Parts 5 and 15), because runaway loops are both a cost and a DoS vector.

Supply chain:
- Third-party tools, MCP servers, skills, and prompts are code: review before enabling, pin versions, restrict their permissions like any dependency.

## PART 7 — BUILD ORDER

1. **Identity:** managed provider; passkeys + magic link; HTTP-only cookie sessions; CSRF/CORS set. *Exit bar: no password-only path; logout-everywhere works.*
2. **Authorization core:** RBAC roles + per-object ownership checks on every endpoint; deny-by-default middleware; denial logging. *Exit bar: an authenticated user provably cannot read another tenant's object by id.*
3. **Hygiene:** secrets manager, input validation everywhere, security headers, dependency scanning, audit log. *Exit bar: repo secret-scan clean; headers verified.*
4. **Third-party & agent access:** OAuth 2.1 + PKCE, scoped machine credentials, refresh rotation with reuse detection. *Exit bar: every credential is revocable and scoped.*
5. **LLM hardening (if applicable):** Part 6 in full — provenance wrapping, least-privilege tools, human gates, output sanitization, spend caps, adversarial test cases in CI. *Exit bar: injection test suite passes; trifecta audit done per agent.*

## PART 8 — CHECKLIST

- [ ] Passkeys + magic link via managed provider; MFA available; step-up on dangerous actions
- [ ] Sessions: HTTP-only Secure SameSite cookies; revocation + logout-everywhere
- [ ] JWTs (where used): pinned alg, 15–60 min, refresh rotation with reuse detection
- [ ] OAuth 2.1 + PKCE for all third-party/agent flows; no implicit/password grants
- [ ] Per-object authorization on every resource endpoint; deny by default; denials logged
- [ ] RBAC now; ReBAC/ABAC added only against product need; checks centralized
- [ ] Tenant isolation enforced in both data layer and authorization layer
- [ ] Secrets in manager only; repos scanned; provider keys server-side with spend alerts
- [ ] Inputs schema-validated; queries parameterized; output encoded per context
- [ ] Untrusted content wrapped + provenance-tagged before any prompt
- [ ] Agent trifecta audited; irreversible actions human-gated; autonomous agents narrower
- [ ] LLM output sanitized/validated before render, storage, or execution
- [ ] Per-user/tenant rate + token + spend caps enforced pre-inference
- [ ] Injection/abuse test cases run in CI
