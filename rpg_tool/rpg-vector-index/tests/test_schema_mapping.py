# path: tests/test_schema_mapping.py
import json
from pathlib import Path

from scripts.build_pgvector import FeatureNode


def test_l1_category():
    n = FeatureNode(
        id="X",
        name="X",
        path="ml/algorithms/regression",
        level=3,
        ancestors=["ml", "algorithms"],
        description=None,
        tags=[],
        aliases=[],
    )
    assert n.l1_category == "ml"


def test_seed_loads_dim_matches():
    seed = Path(__file__).parents[1] / "feature_tree_seed.json"
    data = json.loads(seed.read_text())
    dim = int(data["retrieval"]["dims"])  # fails if missing
    assert dim > 0
