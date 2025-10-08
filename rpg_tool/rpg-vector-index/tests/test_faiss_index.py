# path: tests/test_faiss_index.py
import json
from pathlib import Path

import numpy as np
import faiss


def test_faiss_roundtrip(tmp_path: Path):
    seed = Path(__file__).parents[1] / "feature_tree_seed.json"
    data = json.loads(seed.read_text())
    dim = int(data["retrieval"]["dims"])  # strict
    vecs = data["retrieval"]["vectors"]
    ids = sorted(vecs.keys())
    mat = np.vstack([np.array(vecs[i], dtype="float32") for i in ids])

    faiss.normalize_L2(mat)
    index = faiss.IndexHNSWFlat(dim, 16, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efSearch = 32
    index.add(mat)

    # nearest neighbor is itself
    D, I = index.search(mat[:1], 1)
    assert I[0][0] == 0

    # save/load
    p = tmp_path / "idx.faiss"
    faiss.write_index(index, str(p))
    idx2 = faiss.read_index(str(p))
    D2, I2 = idx2.search(mat[:1], 1)
    assert I2[0][0] == 0
