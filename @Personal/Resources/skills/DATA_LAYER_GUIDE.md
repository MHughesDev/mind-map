---
name: data-layer-guide
description: Use when choosing a database, designing schemas, writing migrations, adding indexes, adding caching, storing embeddings or vectors, or planning backups for any application. Consult even if the user only mentions "storing data," "adding search," or "the app is slow on queries."
version: 1.0.0
date: 2026-09-11
scope: Database selection, schema design, primary keys, migrations, indexing, caching, ORMs vs SQL, vector/embedding storage, retention, backup and recovery.
---

# DATA LAYER DESIGN GUIDE
### Drop-in rules file for coding agents building the data layer of any application

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Select the database with Part 1's table — default to Postgres unless a listed trigger applies.
3. Design the schema under Part 2's rules before writing any application code against it.
4. Adopt the migration discipline of Part 3 from the first migration, not later.
5. Add indexes, caching, and vector storage only per Parts 4–6 triggers.
6. Walk the checklist (Part 9) before declaring done.

**Prime directive:** One boring, well-typed Postgres carries the entire application until a measured constraint proves otherwise. Every additional data system (Redis, vector DB, NoSQL, queue-as-database) is an operational liability you must justify with evidence, not anticipation.

---

## PART 0 — MENTAL MODEL

- The database outlives every framework choice in the app. Schema quality compounds; schema debt compounds faster.
- Constraints in the database (types, FKs, NOT NULL, UNIQUE) are the only validations that hold when a second code path — including an LLM agent — writes data.
- Reads are cheap to fix later (indexes, caches, replicas). Wrong writes are forever. Optimize for write correctness first.
- The fault line between SQLite and Postgres is concurrency and operations, not data size.
- Retrofitting tenancy or isolation after launch costs 3–5x building it in from the first table. Decide tenancy now (see SAAS_PRODUCT_GUIDE.md, Part 1).
- Every index accelerates one read and taxes every write. Indexes are driven by observed query plans, not guesses.

**Never:**
1. Never `SELECT *` — it breaks index-only scans and multiplies I/O; select explicit columns.
2. Never use random UUIDv4 primary keys on large tables — random inserts scatter index pages; use BIGINT identity, or time-ordered UUIDs if external opacity is required.
3. Never store dates/times as text — use `timestamptz`.
4. Never index low-selectivity columns (booleans, small enums) alone.
5. Never run a destructive one-shot migration — always expand → backfill → switch → contract.
6. Never `count(*)` a huge table in a request path — use the planner's row estimate or a maintained counter.
7. Never add a dedicated vector DB before measuring pgvector against your actual corpus.
8. Never add a second data system (Redis, NoSQL) without a measured hot path it fixes.
9. Never let the ORM hide the SQL on anything beyond CRUD — read the generated queries.
10. Never skip foreign keys "for performance" at design time — remove them only with evidence.
11. Never treat backups as done until a restore has been rehearsed.
12. Never let an LLM agent write to tables without the same constraints and parameterized statements as any other client.

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Database | PostgreSQL | Single-server/local/edge app → SQLite |
| Primary keys | BIGINT generated identity | Need non-guessable external IDs → time-ordered UUID |
| Timestamps | `timestamptz`, UTC | Never |
| Foreign keys + constraints | On, everywhere | Proven write bottleneck on a specific hot table |
| Migrations | Expand-and-contract, small, reversible | Never |
| Connection pooling | On from day one | Never |
| Vector storage | pgvector in the same Postgres | >~10M vectors, >~10K vectors/sec ingest, GPU search needed |
| Cache | None | A measured read-heavy hot path → Redis |
| ORM use | Fine for CRUD; raw SQL for analytics/reports | Never fully abandon SQL literacy |
| Backups | Automated + point-in-time recovery, restore rehearsed | Never |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Database selection · Part 2 Schema rules · Part 3 Migrations · Part 4 Indexing · Part 5 Caching · Part 6 Vectors & search for AI apps · Part 7 Retention & backups · Part 8 Build order · Part 9 Checklist

---

## PART 1 — DATABASE SELECTION

| Situation | Choice |
|---|---|
| Default app backend: concurrent writers, a team, a server | PostgreSQL |
| Single-process app, desktop/mobile/edge, embedded, prototypes | SQLite |
| Serverless platform needing per-branch databases | Serverless Postgres (branching provider) |
| Heavy analytical/columnar aggregation as the core workload | Columnar store (e.g., ClickHouse) alongside Postgres |
| Embeddings/RAG within the triggers above | pgvector inside the same Postgres (Part 6) |

Rules:
- Choose one primary store. Additional stores are added by trigger, never by architecture diagram aesthetics.
- Use Postgres-native features before adding systems: JSONB before a document DB, `tsvector` full-text before a search engine, `LISTEN/NOTIFY` or a jobs table before a message broker at small scale.
- Use JSONB for genuinely variable payloads only; promote any JSONB field you query or index regularly into a real typed column, because typed columns get statistics, constraints, and cheap indexes.

## PART 2 — SCHEMA RULES

- Correct types always: `timestamptz`, `numeric` for money, `text` (not arbitrary `varchar(n)` limits), real enums or lookup tables for closed sets.
- `NOT NULL` by default; nullability is an explicit, justified decision per column.
- Foreign keys on every relationship; `ON DELETE` behavior chosen deliberately (RESTRICT default; CASCADE only where child data is meaningless without the parent).
- UNIQUE constraints encode business rules (one email per account, one event ID per webhook receipt) — these are correctness features other layers depend on.
- Soft-delete (`deleted_at timestamptz`) only where the product needs undelete or audit; otherwise delete rows and rely on backups.
- Naming: `snake_case`, singular or plural chosen once and applied everywhere, `<table>_id` for FKs.
- Multi-tenant apps: `tenant_id` on every tenant-owned table from the first migration, with row-level security as the enforcement backstop (details owned by SAAS_PRODUCT_GUIDE.md, Part 1).

## PART 3 — MIGRATIONS

- Use a migration tool from the first table; every schema change is a committed, ordered migration file. No console surgery.
- **Expand-and-contract for every breaking change:** (1) expand — add the new column/table alongside the old; (2) backfill in batches; (3) switch — deploy code reading/writing the new shape; (4) contract — remove the old shape in a later release. Because each step is independently deployable and reversible, this is what makes zero-downtime deploys possible (see DEPLOYMENT_OPERATIONS_GUIDE.md, Part 4).
- Keep migrations small and single-purpose; batch backfills (e.g., 1,000–10,000 rows per transaction) to avoid long locks.
- Test migrations against a realistic data volume before production — a migration that is instant on 1K rows can lock a 100M-row table for minutes.
- Additive migrations may auto-run on deploy; destructive contract steps require an explicit, separate release.

## PART 4 — INDEXING

- Start with what constraints give you (PKs, UNIQUEs, FK columns you join on), then add indexes only from observed query plans (`EXPLAIN ANALYZE`), because guessed indexes tax writes without proof of benefit.
- Composite index column order: equality filters first, then range filters, then sort columns.
- Partial indexes for hot subsets (`WHERE status = 'active'`); expression indexes for computed lookups (`lower(email)`).
- Periodically drop unused indexes — the database tracks index usage; act on it.
- Every added index is a write tax; on write-heavy tables demand a measured read win before adding.

## PART 5 — CACHING

- Add Redis only when a specific read path is measured hot, because a cache adds an invalidation problem and an operational dependency.
- Cache-aside pattern with TTLs as the default; explicit invalidation only where staleness is unacceptable.
- Legitimate Redis roles besides caching: sessions, rate-limit counters, usage/metering accumulation (see SAAS_PRODUCT_GUIDE.md, Part 3), short-lived locks and queues.
- Never cache what a missing index would fix — check the query plan first.

## PART 6 — VECTORS & SEARCH FOR AI APPS

- Default: pgvector in the primary Postgres. One system to back up, replicate, monitor; SQL pre-filtering (tenant, permissions, metadata) composes with similarity search in one query.
- Graduate to a dedicated vector DB only past a measured trigger: ~10M+ vectors, sustained ingest beyond ~10K vectors/sec, GPU-accelerated search, or on-device/edge constraints (use an embedded vector option there).
- Always pre-filter with SQL (tenant_id, ACLs) before similarity ranking — this is a correctness and security requirement in multi-tenant AI apps, not an optimization.
- Index metadata columns used in those filters like any other hot predicate.
- Treat retrieval quality empirically: benchmark full-text (`tsvector`) and hybrid (keyword + vector) against pure vector on your actual corpus — keyword search often wins on known-vocabulary domains.
- Store raw source documents and their chunk/embedding provenance (source ID, chunk index, embedding model + version), because re-embedding on model change is otherwise impossible.
- Keep usage/token events append-only and immutable if they feed billing (cross-reference SAAS_PRODUCT_GUIDE.md, Part 3).
- Agent-facing data access goes through the same parameterized queries and row-level constraints as user-facing code — an agent-authored query is untrusted input (see AGENT_HARNESS_GUIDE.md, Part 14).

## PART 7 — RETENTION & BACKUPS

- Automated daily backups + WAL/point-in-time recovery on from day one.
- A backup is unverified until restored: rehearse a full restore before launch and on a recurring schedule; record restore time.
- Define retention per data class (user content, logs, usage events, PII) and enforce with scheduled jobs; deletion obligations (user-requested erasure) must actually delete or anonymize, including from derived stores and embeddings.
- Environment separation is absolute: production data never flows into dev/staging unmasked.

## PART 8 — BUILD ORDER

1. **Foundation:** Postgres + migration tool + typed schema with FKs/constraints + pooling. *Exit bar: schema reviewed against Part 2; first migration committed.*
2. **Discipline:** expand-and-contract workflow proven on one real change; restore rehearsed. *Exit bar: a backfill migration has run in staging against realistic volume.*
3. **Performance:** indexes from real `EXPLAIN` output on observed slow queries. *Exit bar: no request-path query without an intentional plan.*
4. **AI layer (if applicable):** pgvector + provenance columns + hybrid-search benchmark. *Exit bar: retrieval quality measured on your corpus, tenant pre-filtering enforced.*
5. **Hardening:** retention jobs, PITR verified, unused-index sweep scheduled, Redis only if a trigger fired.

## PART 9 — CHECKLIST

- [ ] Postgres (or trigger-justified alternative) with pooling
- [ ] All columns correctly typed; NOT NULL default; FKs + UNIQUEs encode business rules
- [ ] tenant_id + RLS on tenant-owned tables (multi-tenant apps)
- [ ] Migration tool in place; expand-and-contract followed; backfills batched
- [ ] No `SELECT *` in application code; explicit columns everywhere
- [ ] Indexes justified by query plans; unused-index sweep scheduled
- [ ] Cache added only against a measured hot path
- [ ] pgvector before dedicated vector DB; SQL pre-filtering enforced; embedding provenance stored
- [ ] Backups + PITR on; restore rehearsed and timed
- [ ] Retention policy per data class; erasure reaches derived stores and embeddings
- [ ] Agent data access parameterized and constraint-bound like any client
