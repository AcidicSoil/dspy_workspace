# path: fullstackopen-en-repo/scripts/postprocess.py
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Convert absolute links to local relative paths (best-effort)
for md_path in DATA.rglob("*.md"):
    md = md_path.read_text(encoding="utf-8")

    def repl(m):
        text, href = m.group(1), m.group(2)
        if href.startswith("https://fullstackopen.com/en/"):
            parts = href.replace("https://fullstackopen.com/", "").strip("/").split("/")
            if len(parts) >= 2:
                target = Path("..") / parts[1] / f"01-{parts[-1] or 'index'}.md"
                return f"[{text}]({target.as_posix()})"
        return m.group(0)

    md2 = re.sub(r"$([^$]+)$$([^)]+)$", repl, md)
    if md != md2:
        md_path.write_text(md2, encoding="utf-8")

# rebuild global index
index = {}
for p in DATA.rglob("*.md"):
    rel = p.relative_to(DATA).as_posix()
    try:
        content = p.read_text(encoding="utf-8")
        meta = json.loads(content.split("---", 2)[1])
    except Exception:
        meta = {}
    index[rel] = {"title": meta.get("title", p.stem), "path": rel}
(ROOT / "index.json").write_text(
    json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
)
