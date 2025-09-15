# llms_autofix.py — make a minimal spec‑compliant llms.txt from a loose draft
import re, sys
from pathlib import Path

LINK_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^\)]+)\)(?:: (?P<note>.*))?$")

def has_link_bullets(lines):
    return any(LINK_RE.match(l.strip()) for l in lines)

def prompt_repo():
    try:
        repo = input("Enter GitHub repo (https://github.com/<owner>/<repo>) for Docs links (or leave blank): ").strip()
    except KeyboardInterrupt:
        print("\nCanceled.")
        sys.exit(1)
    if not repo:
        return None
    repo = repo.rstrip("/").removesuffix(".git")
    return repo

def main():
    src = Path("llms.txt")
    if not src.exists():
        print("No llms.txt in current directory.")
        sys.exit(1)
    raw = src.read_text(encoding="utf-8", errors="replace")

    lines = raw.splitlines()
    out = []

    # 1) Ensure H1 on first non-empty line
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i == len(lines):
        print("Empty file.")
        sys.exit(1)

    first = lines[i].strip()
    if not first.startswith("# "):
        # Turn first line into title
        title = first.lstrip("# ").strip() or "Project"
        out.append(f"# {title}")
        i += 1
    else:
        out.append(first)
        i += 1

    # 2) Ensure a one-line blockquote summary (reuse next non-empty line)
    while i < len(lines) and not lines[i].strip():
        i += 1
    summary = ""
    if i < len(lines):
        summary = lines[i].strip().lstrip("> ").strip()
        i += 1
    out += ["", f"> {summary or 'Project overview.'}", ""]

    remember = []
    docs_section = []
    optional_section = []
    current_is_links = False

    # 3) Parse the rest; non-link sections become Remember bullets
    while i < len(lines):
        l = lines[i]
        i += 1
        s = l.strip()

        if s.startswith("## "):
            # entering a heading → check if the following bullets are links
            # lookahead a few lines
            block = []
            while i < len(lines) and not lines[i].strip().startswith("## "):
                block.append(lines[i]); i += 1
            if has_link_bullets(block):
                # treat as Docs (or Optional if header contains 'optional')
                target = optional_section if "optional" in s.lower() else docs_section
                for b in block:
                    bs = b.strip()
                    if bs and bs.startswith("- "):
                        if LINK_RE.match(bs):
                            target.append(bs)
                continue
            else:
                # demote to Remember bullets
                for b in block:
                    bs = b.strip()
                    if bs.startswith("- "):
                        remember.append(bs[2:])
                    elif bs:
                        remember.append(bs)

        else:
            # free text outside headings → remember bullet if looks like a list
            if s.startswith("- "):
                remember.append(s[2:])

    if remember:
        out += ["Remember:", ""] + [f"- {r}" for r in remember]

    # 4) Ensure at least one Docs link
    if not docs_section:
        repo = prompt_repo()
        if repo:
            docs_section = [
                f"- [README]({repo}#readme): Overview",
                f"- [Issues]({repo}/issues): Open issues",
            ]

    if docs_section:
        out += ["", "## Docs"] + docs_section

    if optional_section:
        out += ["", "## Optional"] + optional_section

    Path("llms_fixed.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("Wrote llms_fixed.txt (spec‑compliant). Now run:")
    print("  llms_txt2ctx llms_fixed.txt > llms-ctx.txt")
    print("  llms_txt2ctx --optional True llms_fixed.txt > llms-ctx-full.txt")

if __name__ == "__main__":
    main()
