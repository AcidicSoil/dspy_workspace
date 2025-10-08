# path: fullstackopen-en-repo/scripts/linkcheck.py
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FAILS = 0

link_re = re.compile(r"$([^$]+)$$([^)]+)$")

for md_path in DATA.rglob("*.md"):
    rel_dir = md_path.parent
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    for m in link_re.finditer(text):
        href = m.group(2)
        if href.startswith("http"):
            continue
        target = (rel_dir / href).resolve()
        if not target.exists():
            print(f"BROKEN: {md_path.relative_to(ROOT)} -> {href}")
            FAILS += 1

if FAILS:
    print(f"broken links: {FAILS}")
    sys.exit(1)
print("linkcheck ok")
