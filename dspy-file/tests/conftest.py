from __future__ import annotations

import os
from pathlib import Path


_CACHE_DIR = Path(__file__).parent / ".dspy-cache"
_CACHE_DIR.mkdir(exist_ok=True)

os.environ.setdefault("DISKCACHE_DEFAULT_DIRECTORY", str(_CACHE_DIR))
os.environ.setdefault("DSPY_CACHE_DIR", str(_CACHE_DIR))
os.environ.setdefault("DSPY_CACHEDIR", str(_CACHE_DIR))
