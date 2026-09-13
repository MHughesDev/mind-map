---
name: skills-vault-index
description: Read this file FIRST in any session with vault access. It routes to every guide in this skills folder. Open only the guide(s) whose trigger matches the current task.
version: 1.1.0
date: 2026-09-11
scope: Guide registry and routing for the skills vault.
---

# SKILLS VAULT INDEX

**Operating rule for agents:** Read this index, match the task against the trigger column, open only matching guides. Read a guide's head (frontmatter through its Defaults table) first; grep into numbered parts as needed. Guides cross-reference each other by filename + part number.

| Guide | Version | Trigger |
|---|---|---|
| GUIDE_AUTHORING_GUIDE.md | 1.0.0 | Use when creating, editing, splitting, or registering any guide in this vault — the constitution all guides conform to. |
| AGENT_HARNESS_GUIDE.md | 3.0.0 | Use when designing or building any application containing an internal AI agent — loops, tools, local model support, sub-agents, sandboxes, agent memory. |
| DATA_LAYER_GUIDE.md | 1.0.0 | Use when choosing databases, designing schemas, migrations, indexing, caching, vector/embedding storage, or backups. |
| BACKEND_API_GUIDE.md | 1.0.0 | Use when designing backend services or APIs — architecture, REST/GraphQL/tRPC, idempotency, pagination, errors, webhooks, jobs, agent-consumable APIs. |
| AUTH_SECURITY_GUIDE.md | 1.0.0 | Use when implementing authentication, sessions, authorization, secrets, API security, or securing LLM features and agents. |
| FRONTEND_UI_GUIDE.md | 1.0.0 | Use when building web frontends — rendering strategy, state management, components, performance budgets, accessibility, streaming/AI-native UI. |
| DEPLOYMENT_OPERATIONS_GUIDE.md | 1.0.0 | Use when deploying, setting up CI/CD, choosing hosting, releases and rollback, feature flags, observability, or operating LLM apps in production. |
| SAAS_PRODUCT_GUIDE.md | 1.0.0 | Use when building SaaS mechanics — multi-tenancy, billing, usage metering, entitlements, quotas and AI cost control, onboarding, admin, compliance basics. |

**Reading order for a full new application:** DATA_LAYER → BACKEND_API → AUTH_SECURITY → FRONTEND_UI → DEPLOYMENT_OPERATIONS → SAAS_PRODUCT, with AGENT_HARNESS alongside wherever an internal agent exists.

**Registration rule:** A guide not listed here does not exist. Update the row on every version bump (see GUIDE_AUTHORING_GUIDE.md, Part 5).
