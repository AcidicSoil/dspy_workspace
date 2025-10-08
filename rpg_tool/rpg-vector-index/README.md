<!-- path: README.md -->
# RPG Vector Index Upgrade (FAISS / pgvector)

This package upgrades the Feature Tree seed to a **real vector index** using **FAISS** (local) and **pgvector** (PostgreSQL). It preserves the **exact JSON schema** of your existing seed (nodes, hierarchy_edges, retrieval.vectors) and treats the JSON as the **single source of truth**.

## What this provides

- **pgvector** schema + indexes (HNSW + optional IVFFlat) and a loader that upserts features + embeddings.
- **FAISS** HNSW index builder that writes `feature_index.faiss` and a sidecar metadata CSV.
- **Query examples** for both backends returning **full hierarchical paths**.

## Inputs

- A JSON Feature Tree in the same schema as your `Feature Tree Seed` (top-level keys: `metadata`, `schema`, `nodes`, `hierarchy_edges`, `retrieval`).

## Quick start (local)

### 1) Create FAISS index from the seed

```bash
uv run python scripts/build_faiss.py feature_tree_seed.json --out-dir ./.artefacts
```

```md
# 1) ensure Postgres has pgvector installed; then:
psql "$PG_DSN" -f sql/pgvector_schema.sql

# 2) load data (will upsert nodes & vectors)
uv run python scripts/build_pgvector.py feature_tree_seed.json --dsn "$PG_DSN" --distance cosine

uv run python scripts/search_examples.py --faiss ./.artefacts/feature_index.faiss \
  --meta ./.artefacts/feature_meta.csv --query "logistic regression" --topk 5

uv run python scripts/search_examples.py --pgvector --dsn "$PG_DSN" \
  --query-vec "[0.8,0.2,0.1,0.1,0.4,0.0,0.1,0.1]" --topk 5
```

```md
Tip: Replace FAISS vectors/pgvector column dimension with your production embedding size (e.g., 1536 or 3072). The loader auto-detects dimension from retrieval.dims in the JSON.

Configuration
PG_DSN: Postgres connection string (e.g., postgresql://user:pass@localhost:5432/db).
--distance: one of l2, cosine, or ip for pgvector operator and FAISS metric.
Files
sql/pgvector_schema.sql – DDL for the table and indexes.
scripts/build_pgvector.py – parses JSON and upserts into Postgres/pgvector.
scripts/build_faiss.py – builds an HNSW FAISS index + metadata.
scripts/search_examples.py – thin examples to query either backend.
```
