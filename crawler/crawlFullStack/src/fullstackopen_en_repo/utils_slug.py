from __future__ import annotations
import re
from slugify import slugify

SAFE_CHARS = "-abcdefghijklmnopqrstuvwxyz0123456789"

def slug(s: str) -> str:
    base = slugify(s, lowercase=True)
    base = re.sub(r"-+", "-", base).strip("-")
    return base or "untitled"


def numbered(name: str, index: int) -> str:
    return f"{index:02d}-{slug(name)}"


def path_from_parts(parts: list[str]) -> str:
    parts = [slug(p) for p in parts if p]
    return "/".join(parts)
