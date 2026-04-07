# Vault + MATH Graph Architecture (Implementation-Oriented)

## Objective

Build a personal vault system that supports:

- fast semantic retrieval over **all `.md` and other text-like files**
- multi-resolution context (chunk/file/folder vectors)
- compatibility with autonomous research/paper agents

## Implemented vector architecture

The current implementation adds a local vector pipeline (`vault_pipeline`) using ChromaDB:

1. `vault_chunks`
   - Granularity: chunk
   - Purpose: exact evidence retrieval
   - Metadata: `path`, `chunk_index`, `start_char`, `end_char`, `ext`, `folder`

2. `vault_files`
   - Granularity: file
   - Purpose: document-level relevance scoring and reranking
   - Metadata: `path`, `chunk_count`, `ext`, `folder`

3. `vault_folders`
   - Granularity: folder (including root `.`)
   - Purpose: route queries to the right domain subtrees
   - Metadata: `path`, `file_count_hint`

## End-to-end indexing flow

1. Traverse vault root recursively.
2. Select indexable files by extension and max byte size.
3. Read content with UTF-8 fallback.
4. Normalize whitespace and chunk text with overlap.
5. Generate chunk vectors and upsert into `vault_chunks`.
6. Build file summaries from leading chunks and upsert into `vault_files`.
7. Aggregate folder summaries from child content and upsert into `vault_folders`.

## Retrieval flow for agents

For autonomous agents (paper ideation, drafting, verification):

1. Folder routing:
   - Query `vault_folders` with user/task intent.
   - Select top domain folders.
2. File shortlist:
   - Query `vault_files` and filter/rerank by folder/path.
3. Evidence grounding:
   - Query `vault_chunks` for citation-grade snippets.
4. Return provenance:
   - include `path`, `chunk_index`, `start_char`, `end_char`.

## MATH Vault integration plan (next layer)

Use the current vector layer as a semantic substrate and add a symbolic graph:

- Graph nodes:
  - `Axiom`, `Definition`, `Lemma`, `Theorem`, `ProofTechnique`, `Conjecture`, `Counterexample`, `DomainTopic`
- Graph edges:
  - `depends_on`, `implies`, `generalizes`, `special_case_of`, `analog_of`, `contradicted_by`, `proved_by`

The vector layer supports semantic recall; the graph layer supports logical traversals and novelty synthesis.

## Why this shape is robust

- Chunk vectors maximize precision.
- File vectors preserve narrative/document context.
- Folder vectors preserve domain-level context.
- Local-first Chroma persistence supports repeatable agent runs.
- Fallback embedder keeps pipeline functional in constrained/offline environments.

## Recommended production hardening

1. Add metadata filters to query API (`where` by folder/ext/path).
2. Add incremental indexing by file hash + mtime cache.
3. Add multilingual/math token normalization for better equation retrieval.
4. Add hybrid search fusion (BM25 + vector).
5. Add cross-encoder reranking for top-k chunks.
