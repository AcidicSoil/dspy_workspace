
\\ inferred\sql\pgvector_schema.sql
```sql
-- path: sql/pgvector_schema.sql
-- Requires: CREATE EXTENSION vector; (once per DB)
-- Dimension is auto-detected by the loader, but this DDL uses a safe default of 8
-- matching the seed. Change VECTOR(8) to your real embedding size when upgrading.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS features (
  id           TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  path_str     TEXT NOT NULL,
  level        INT  NOT NULL,
  l1_category  TEXT,
  ancestors    TEXT[] NOT NULL,
  description  TEXT,
  tags         TEXT[] DEFAULT '{}',
  aliases      TEXT[] DEFAULT '{}',
  embedding    VECTOR(8)  -- set to your true dimension (e.g., 1536 or 3072)
);

-- Helpful metadata indexes
CREATE INDEX IF NOT EXISTS idx_features_path        ON features (path_str);
CREATE INDEX IF NOT EXISTS idx_features_level       ON features (level);
CREATE INDEX IF NOT EXISTS idx_features_l1_category ON features (l1_category);
CREATE INDEX IF NOT EXISTS idx_features_tags        ON features USING GIN (tags);

-- Vector indexes (choose based on distance). HNSW prioritized; IVFFlat optional.
-- HNSW: better speed/recall trade-off, slower to build, higher memory.
CREATE INDEX IF NOT EXISTS features_embedding_hnsw_l2
  ON features USING hnsw (embedding vector_l2_ops) WITH (m = 16, ef_construction = 64);
-- Cosine
-- CREATE INDEX IF NOT EXISTS features_embedding_hnsw_cos
--   ON features USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
-- Inner product
-- CREATE INDEX IF NOT EXISTS features_embedding_hnsw_ip
--   ON features USING hnsw (embedding vector_ip_ops) WITH (m = 16, ef_construction = 64);

-- Optional: IVFFlat (requires data present and a training step; tune lists accordingly)
-- CREATE INDEX IF NOT EXISTS features_embedding_ivfflat_l2
--   ON features USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
