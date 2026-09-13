---
name: frontend-ui-guide
description: Use when building or restructuring any web frontend — choosing rendering strategy (SSR/SSG/islands/server components), state management, component architecture, performance budgets, accessibility, or AI-native UI like chat, streaming, and generative interfaces. Consult even if the user only says "build the UI," "make a dashboard," "the page is slow," or "add a chat interface."
version: 1.0.0
date: 2026-09-11
scope: Rendering strategy, framework defaults, state management, component architecture, performance budgets (Core Web Vitals), accessibility, streaming/AI-native UI patterns.
---

# FRONTEND & UI ARCHITECTURE GUIDE
### Drop-in rules file for coding agents building web application frontends

---

## HOW TO APPLY THIS FILE

1. Read Part 0 and the Defaults table. Hold both while working.
2. Pick the rendering strategy per page type from Part 1 — pages differ; the app is not one strategy.
3. Enforce the server-state/client-state split of Part 2 on every piece of data — misfiled state is the root frontend defect.
4. Set the performance budget (Part 4) BEFORE building, and wire its enforcement into CI.
5. Apply accessibility (Part 5) as you build components, not as an audit later.
6. For AI features, implement Part 6's streaming-first patterns.
7. Walk the checklist (Part 8) before declaring done.

**Prime directive:** Render on the server by default, ship interactivity as small client islands, file every piece of state in exactly one home, and hold the interaction budget (responsiveness under 200ms) as a hard constraint — an AI app's UI is judged by how honest it is while the model is thinking.

---

## PART 0 — MENTAL MODEL

- The client is a hostile runtime: unknown device, unknown network, every kilobyte of JS taxes interactivity. Server-first is a performance and reliability posture, not a fashion.
- There are two kinds of state and they never mix: server state (someone else's truth, fetched and cached) and client state (your UI's truth, owned locally). Nearly every state-management mess is server data copied into a client store, which instantly forks the truth.
- Components split along the server/client boundary: server components for data and layout, client components as leaf islands for interaction — push `'use client'` down, not up.
- Performance is a budget, not an aspiration: field data from real users is the truth; lab scores are a debugging tool.
- Loading states are product surface. In AI apps especially, the wait IS the experience — stream, skeleton, and show progress honestly rather than blocking.
- Accessibility is architecture: semantic HTML and keyboard paths are cheap on day one and a rewrite later.

**Never:**
1. Never copy server data into Redux/Zustand/Context — the query cache is its single home; components read from it.
2. Never maintain both a fetch-cache and a global store for the same entity — one source of truth per entity.
3. Never mark a whole layout `'use client'` to fix one interactive widget — isolate the widget as a leaf island.
4. Never ship an element that loads without reserved dimensions (images, embeds, ads) — layout shift is a self-inflicted wound.
5. Never block the main thread >50ms in an interaction handler — chunk, defer, or move work off-thread.
6. Never judge performance by lab scores alone — budget and alert on field (real-user) data.
7. Never fetch client-side what the server could have rendered — client fetching is for post-load interactivity.
8. Never build interactive elements out of divs — buttons are buttons, links are links; keyboard and screen readers depend on it.
9. Never render LLM output as raw HTML — sanitize; model output is untrusted (see AUTH_SECURITY_GUIDE.md, Part 6).
10. Never leave an AI action without streamed or staged feedback — a frozen spinner on a 20-second model call reads as a crash.
11. Never optimize a metric already in its "good" band — spend the effort on the failing one.
12. Never adopt a state library because it's familiar — file the state first (Part 2), then pick the smallest tool that holds it.

---

## DEFAULTS AT A GLANCE

| Decision | Default | Change when (measured trigger) |
|---|---|---|
| Framework | Server-components-first React meta-framework (app-router style) | Content-first site with sparse interactivity → islands framework / SSG |
| Styling | Utility CSS or CSS Modules (server-component safe) | — |
| Server state | Query library (cache, revalidate, dedupe) | Never hand-roll fetch-into-store |
| Client state | Small store (e.g., Zustand-style) + Context for slow config | Very large org/devtools needs → Redux Toolkit defensible |
| Rendering | Per page type, Part 1 table | — |
| Performance budget | LCP < 2.5s · INP < 200ms · CLS < 0.1 at p75 field data; alert at 80% (2.0s / 160ms / 0.08) | Tighten for commerce/marketing landing paths |
| JS budget | Set an explicit per-route bundle cap and enforce in CI | — |
| Accessibility | Semantic HTML, full keyboard paths, visible focus, labeled controls | Never |
| AI responses | Token streaming + optimistic UI + staged progress | Batch-only for non-interactive jobs |

*These defaults are starting points; override only on measured evidence, and record the evidence.*

---

## CONTENTS
Part 1 Rendering strategy · Part 2 State management · Part 3 Component architecture · Part 4 Performance budgets · Part 5 Accessibility · Part 6 AI-native UI · Part 7 Build order · Part 8 Checklist

---

## PART 1 — RENDERING STRATEGY (per page type, not per app)

| Page type | Pattern |
|---|---|
| Marketing, blog, docs (content-first) | Static generation / islands; near-zero JS |
| Personalized dashboard, account pages | Server-render with streamed dynamic sections (Suspense holes) |
| Interactive SaaS working surface | Server components for shell + data; client islands for controls |
| Mostly-static page with pockets of interactivity | Static shell + islands |
| Real-time/chat/agent surface | Server shell + a client island owning the stream (Part 6) |

Rules:
- Server components fetch data and ship zero JS; client components exist only where there are event handlers, browser APIs, or local state.
- Stream the shell immediately and let slow data arrive into Suspense boundaries, because first paint and first interaction must not wait for the slowest query.
- Cache deliberately at each layer (request dedupe, data cache, route cache) and document per route what is static, revalidated, or dynamic — accidental caching of personalized data is a correctness bug.
- Treat experimental rendering modes as experimental: verify current stability before relying on them in production.

## PART 2 — STATE MANAGEMENT (file every piece of state)

| State | Home |
|---|---|
| Server data (anything fetched) | Query library cache — with revalidation, dedupe, retries |
| Client UI state (modals, selection, drafts, theme, cart) | Small client store or component state |
| Slow-changing config (locale, feature flags, current user shell) | Context |
| URL-worthy state (filters, tabs, pagination) | The URL — searchParams are state |
| Form state | Form library or uncontrolled inputs + action |

Rules:
- Mutations go through the query layer with invalidation (or optimistic update + rollback), because hand-synced caches drift.
- Derive, don't store: anything computable from existing state is computed, memoized if hot — stored derivations desynchronize.
- Keep the client store small enough to read in one sitting; growth there is a smell that server state is leaking in.

## PART 3 — COMPONENT ARCHITECTURE

- Structure by feature, not by kind: `features/billing/` containing its components, hooks, api, tests — because kind-folders (`components/`, `hooks/`) scale into junk drawers.
- Shared design-system primitives (Button, Input, Dialog) live in one `ui/` package with tokens (color, spacing, type) — components consume tokens, never raw values, so theming stays one-file.
- Props are the contract: typed, minimal, no reaching into children's internals; composition over configuration (pass children, not 14 booleans).
- Server/client boundary is explicit per feature: a `*.client.tsx` leaf convention keeps islands visible in review.
- Every async surface has designed loading, empty, and error states — they are states of the product, not afterthoughts.

## PART 4 — PERFORMANCE BUDGETS

Targets (75th percentile, field data from real users):
- LCP < 2.5s · INP < 200ms · CLS < 0.1. Internal alerts at 80% of each (2.0s / 160ms / 0.08) so drift is caught before failure.
- Interaction work >50ms on the main thread must be split, deferred, or moved to a worker — long tasks are what push INP over budget.
- Aim TTFB < 200ms on server-rendered routes; slow TTFB poisons every downstream metric.

Enforcement:
- Real-user monitoring wired from launch; budgets asserted in CI against lab proxies (bundle size per route, route-level Lighthouse) to catch regressions pre-merge — lab gates, field verdicts.
- Standing diet: explicit dimensions on all media; code-split by route; defer non-critical third-party scripts; preload the LCP asset; font-display swap with size-adjusted fallbacks.
- Fix the failing metric: responsiveness failures (INP) are usually oversized hydration and long tasks; loading failures (LCP) are usually server latency and unpreloaded hero assets; stability failures (CLS) are unreserved space.

## PART 5 — ACCESSIBILITY

- Semantic HTML first: native button/a/label/heading order — ARIA is the patch, not the plan.
- Every interactive path operable by keyboard alone: logical tab order, visible focus rings, Escape closes overlays, focus trapped in modals and returned on close.
- Every input labeled; every image alt-texted (empty alt for decorative); color contrast ≥ 4.5:1 for text; state conveyed by more than color.
- Streamed/AI content announced politely to assistive tech (aria-live="polite" on message regions), because screen-reader users otherwise get silence while sighted users watch tokens.
- Automated a11y checks in CI + a manual keyboard-and-screen-reader pass over each core flow before release.

## PART 6 — AI-NATIVE UI

Streaming is the default contract:
- Stream tokens into the transcript as they arrive; render markdown progressively; auto-scroll with a user-scroll override, because reading-while-generating is the core UX.
- Sanitize model output before render — untrusted (never `dangerouslySetInnerHTML` raw model text); code blocks rendered inert with copy affordances.
- Show the machinery honestly: staged progress ("searching → reading → drafting"), tool-call chips with status, cancel always available, retry on failure, partial results preserved on cancel/error.
- Optimistic UI on the user's side of the exchange: message appears instantly, send button disabled during flight, edit-and-resend supported.

Generative/structured UI:
- Prefer schema-constrained output rendered by YOUR components (model emits validated JSON → you map to a fixed component registry) over model-emitted markup, because a component allowlist is both safer and visually consistent.
- Validate structured output against the schema before render; on failure, fall back to text rendering, never to a blank.

Plumbing:
- Long generations run server-side against your API with streaming to the client; provider keys never reach the browser (AUTH_SECURITY_GUIDE.md, Part 6).
- Rate-limit and quota AI routes per user before inference; surface remaining quota in the UI so limits are never a surprise (SAAS_PRODUCT_GUIDE.md, Part 3).
- Long agent tasks (beyond a request timeout) become operations: kick off, show live status from the operation resource, notify on completion (BACKEND_API_GUIDE.md, Part 5; AGENT_HARNESS_GUIDE.md, Part 15).
- Persist transcripts server-side; hydrate on reload; a refresh must never eat a conversation.

## PART 7 — BUILD ORDER

1. **Skeleton:** framework per defaults, design tokens + ui/ primitives, feature-folder structure, typed API client. *Exit bar: one end-to-end page server-rendered with a client island.*
2. **State discipline:** query layer for all server data; client store only for filed client state; URL state in the URL. *Exit bar: zero server data in client stores.*
3. **Budget wiring:** RUM live; CI bundle + Lighthouse gates; media dimensions enforced. *Exit bar: budgets fail the build when exceeded.*
4. **Access + polish:** keyboard paths, focus management, loading/empty/error states designed for every async surface. *Exit bar: core flows pass a keyboard-only run.*
5. **AI surfaces (if applicable):** streaming transcript island, staged progress, sanitized rendering, quota surfacing, operation-backed long tasks. *Exit bar: a 30-second generation feels alive, cancellable, and survives a refresh.*

## PART 8 — CHECKLIST

- [ ] Rendering strategy chosen per page type from Part 1
- [ ] Server components default; `'use client'` only on leaf islands
- [ ] All server data in the query cache; none in client stores; URL state in the URL
- [ ] Feature-folder structure; tokenized ui/ primitives; typed props
- [ ] Budgets set (LCP/INP/CLS + JS per route) and enforced in CI; RUM live with 80% alerts
- [ ] Explicit dimensions on all media; route-level code splitting; LCP asset preloaded
- [ ] Semantic HTML; full keyboard operability; labels, contrast, focus management; aria-live on streams
- [ ] AI output streamed, sanitized, cancellable; partial results preserved
- [ ] Structured/generative UI schema-validated against a component allowlist
- [ ] Provider keys server-side; AI routes quota'd with quota visible in UI
- [ ] Transcripts persisted; reload-safe
