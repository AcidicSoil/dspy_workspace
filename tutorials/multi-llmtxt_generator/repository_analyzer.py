# path: repository_analyzer.py
# repository_analyzer.py — dynamic llms.txt builder (canonical + ad-hoc sections)

import re
from collections import defaultdict
from typing import List, Tuple, Dict, Iterable

import dspy
from signatures import (
    AnalyzeRepository,
    AnalyzeCodeStructure,
    GenerateUsageExamples,
    GenerateLLMsTxt,
)

# --- Title helpers -----------------------------------------------------------


def _nicify_title(name: str) -> str:
    base = name.rsplit("/", 1)[-1]
    base = re.sub(r"\.(md|rst|txt|py|ipynb|js|ts|html|mdx)$", "", base, flags=re.I)
    base = base.replace("-", " ").replace("_", " ")
    t = base.strip().title() or name
    # Treat index pages as their parent folder (Docs, Api, etc.)
    if re.search(r"(^|/)index(\.mdx?|\.html?)?$", name, flags=re.I):
        parts = name.strip("/").split("/")
        if len(parts) > 1:
            t = parts[-2].replace("-", " ").replace("_", " ").title()
    return t


# --- Path selection ----------------------------------------------------------


def _select_paths(file_tree: str, patterns: List[str]) -> List[str]:
    """Pick paths matching any regex in patterns, de-duped in tree order."""
    paths = [p.strip() for p in file_tree.splitlines() if p.strip()]
    out: List[str] = []
    for p in paths:
        for pat in patterns:
            if re.search(pat, p, flags=re.I):
                out.append(p)
                break
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            uniq.append(p)
            seen.add(p)
    return uniq


# --- Legacy link builder (kept for compatibility) ---------------------------


def _build_links(
    repo_url: str, file_tree: str
) -> Tuple[
    List[Tuple[str, str, str]], List[Tuple[str, str, str]], List[Tuple[str, str, str]]
]:
    """Return (Docs, Examples, Optional) for the legacy renderer."""
    from repo_helpers import construct_raw_url

    readme_first = _select_paths(file_tree, [r"(^|/)README\.md$"])
    docs_md = _select_paths(file_tree, [r"(^|/)(docs?|documentation)/.*\.(md|mdx)$"])
    root_md = _select_paths(file_tree, [r"^[^/]+\.mdx?$"])

    examples = _select_paths(
        file_tree, [r"(^|/)(examples?|demos?|tutorials?)/.*\.(md|mdx|py|ipynb|js|ts)$"]
    )

    optional = _select_paths(
        file_tree,
        [
            r"(^|/)CONTRIBUTING\.md$",
            r"(^|/)CHANGELOG\.md$",
            r"(^|/)HISTORY\.md$",
            r"(^|/)BENCHMARKS?\.md$",
            r"(^|/)LICENSE(\.|$)",
            r"(^|/)SECURITY\.md$",
        ],
    )

    def to_links(paths, note_hint):
        links = []
        for p in paths:
            url = construct_raw_url(repo_url, p)
            title = (
                "README"
                if re.search(r"(^|/)README\.md$", p, flags=re.I)
                else _nicify_title(p)
            )
            note = note_hint(p)
            links.append((title, url, note))
        return links

    docs_links = []
    docs_links += to_links(readme_first[:1], lambda p: "overview and usage.")
    docs_links += to_links(docs_md[:6], lambda p: "docs page.")
    root_md_filtered = [
        p for p in root_md if not re.search(r"(^|/)README\.md$", p, flags=re.I)
    ]
    docs_links += to_links(root_md_filtered[:4], lambda p: "reference page.")
    docs_links = docs_links[:8]

    example_links = to_links(examples[:6], lambda p: "worked example.")
    optional_links = to_links(optional[:8], lambda p: "optional reading.")

    if not docs_links and readme_first:
        p = readme_first[0]
        from repo_helpers import construct_raw_url

        url = construct_raw_url(repo_url, p)
        docs_links.append(("README", url, "overview and usage."))

    return docs_links, example_links, optional_links


# --- Dynamic bucketizer (LangGraph-style) -----------------------------------

# Canonical sections first; everything else becomes an ad-hoc section based
# on the top-level directory name (Plugins, Cloud, Cookbook, etc.).
TAXONOMY: List[Tuple[str, re.Pattern]] = [
    (
        "Docs",
        re.compile(
            r"(docs|guide|getting[-_ ]?started|quickstart|install|overview)", re.I
        ),
    ),
    ("Tutorials", re.compile(r"(tutorial|example|how[-_ ]?to|cookbook|demos?)", re.I)),
    ("API", re.compile(r"(api|reference|sdk|class|module)", re.I)),
    ("Concepts", re.compile(r"(concept|architecture|design|faq)", re.I)),
    (
        "Optional",
        re.compile(
            r"(contributing|changelog|release|security|license|benchmark)", re.I
        ),
    ),
]


def _short_note(path: str) -> str:
    p = path.lower()
    if any(
        k in p
        for k in ["getting-started", "quickstart", "install", "overview", "/readme"]
    ):
        return "install & quickstart"
    if any(k in p for k in ["reference", "/api"]):
        return "API reference"
    if any(k in p for k in ["tutorial", "example", "how-to", "demo"]):
        return "worked example"
    if any(k in p for k in ["concept", "architecture", "faq"]):
        return "core concept"
    if "changelog" in p or "release" in p:
        return "version history"
    if "license" in p:
        return "usage terms"
    if "security" in p:
        return "security policy"
    return "docs page"


def _score(path: str) -> float:
    s = 0.0
    p = path.lower()
    if any(
        k in p
        for k in ["quickstart", "getting-started", "install", "overview", "/readme"]
    ):
        s += 5
    if any(k in p for k in ["tutorial", "example", "how-to", "demo"]):
        s += 3
    if re.search(r"(^|/)index(\.mdx?|\.html?)?$", p):
        s += 2
    s -= p.count("/") * 0.1
    return s


def _docs_url_or_raw(repo_url: str, path: str) -> str:
    """Prefer rendered docs URLs if the repo is publishing GitHub Pages (heuristic)."""
    # You can enhance this to map /docs/*.md -> https://<site>/docs/... if you have a site base.
    from repo_helpers import construct_raw_url

    return construct_raw_url(repo_url, path)


def _build_dynamic_buckets(
    repo_url: str, file_tree: str
) -> List[Tuple[str, List[Tuple[str, str, str]]]]:
    """Return ordered [(SectionName, [(title, url, note), ...]), ...]."""
    paths = [p.strip() for p in file_tree.splitlines() if p.strip()]

    # 1) Prepare page records
    pages = []
    for p in paths:
        if not re.search(r"\.(md|mdx|py|ipynb|js|ts|rst|txt|html)$", p, flags=re.I):
            continue
        url = _docs_url_or_raw(repo_url, p)
        title = (
            "README"
            if re.search(r"(^|/)README\.md$", p, flags=re.I)
            else _nicify_title(p)
        )
        note = _short_note(p)
        score = _score(p)
        pages.append({
            "path": p,
            "url": url,
            "title": title,
            "note": note,
            "score": score,
        })

    # 2) Assign to canonical buckets; otherwise ad-hoc based on top-level dir
    buckets: Dict[str, List[dict]] = defaultdict(list)

    for pg in pages:
        matched = False
        for name, rx in TAXONOMY:
            if rx.search(pg["path"]) or rx.search(pg["title"]):
                buckets[name].append(pg)
                matched = True
                break
        if not matched:
            top = pg["path"].strip("/").split("/")[0] or "Misc"
            buckets[top.replace("-", " ").replace("_", " ").title()].append(pg)

    # 3) Curate: sort & cap each section to 10 items
    for name, items in list(buckets.items()):
        items.sort(key=lambda x: (-x["score"], x["title"]))
        buckets[name] = items[:10]
        if not buckets[name]:
            del buckets[name]

    # 4) Collapse singletons of ad-hoc sections into Optional (except reserved)
    reserved = {n for n, _ in TAXONOMY}
    for name in list(buckets.keys()):
        if name not in reserved and len(buckets[name]) <= 1:
            buckets["Optional"].extend(buckets.pop(name))

    # 5) Final ordering: reserved order first, then alphabetical of ad-hoc
    ordered: List[Tuple[str, List[Tuple[str, str, str]]]] = []
    seen = set()
    for n, _ in TAXONOMY:
        if n in buckets:
            ordered.append((
                n,
                [(pg["title"], pg["url"], pg["note"]) for pg in buckets[n]],
            ))
            seen.add(n)
    for n in sorted(k for k in buckets.keys() if k not in seen):
        ordered.append((n, [(pg["title"], pg["url"], pg["note"]) for pg in buckets[n]]))
    return ordered


# --- Renderers ---------------------------------------------------------------


def _render_llms_markdown(
    project_name: str,
    project_purpose: str,
    remember_bullets: List[str],
    docs_links,
    example_links,
    optional_links,
) -> str:
    # Legacy renderer (unchanged) — keeps compatibility with existing callers.
    rb = [str(b).strip().rstrip(".") for b in remember_bullets if str(b).strip()]
    rb = rb[:6] or [
        "Key concepts and usage patterns",
        "Common pitfalls and best practices",
        "Consult Docs and Examples links below",
    ]
    if len(rb) < 3:
        rb += ["Follow the docs for setup", "Use examples as starting points"][
            : 3 - len(rb)
        ]

    def fmt_links(links):
        return (
            "\n".join([f"- [{title}]({url}): {note}" for (title, url, note) in links])
            or "- [README](https://example.com): overview."
        )

    purpose_one_line = (project_purpose or "").strip().replace("\n", " ")

    md = (
        f"# {project_name}\n\n"
        f"> {purpose_one_line}\n\n"
        "**Remember:**\n" + "\n".join([f"- {b}" for b in rb]) + "\n\n"
        "## Docs\n" + fmt_links(docs_links) + "\n\n"
        "## Examples\n" + fmt_links(example_links) + "\n\n"
        "## Optional\n" + fmt_links(optional_links) + "\n"
    )
    return md


def _render_llms_markdown_v2(
    project_name: str,
    project_purpose: str,
    remember_bullets: List[str],
    buckets: List[Tuple[str, List[Tuple[str, str, str]]]],
) -> str:
    """Dynamic renderer: only prints sections that exist, in canonical order."""
    rb = [str(b).strip().rstrip(".") for b in remember_bullets if str(b).strip()]
    rb = rb[:6] or [
        "Install + Quickstart first",
        "Core concepts & API surface",
        "Use Tutorials for worked examples",
    ]
    if len(rb) < 3:
        rb += ["Review API reference", "See Optional for meta docs"][: 3 - len(rb)]
    purpose_one_line = (project_purpose or "").strip().replace("\n", " ")

    def fmt_section_items(items: Iterable[Tuple[str, str, str]]) -> str:
        return "\n".join([f"- [{t}]({u}): {n}." for (t, u, n) in items])

    out = [
        f"# {project_name}",
        "",
        f"> {purpose_one_line}",
        "",
        "**Remember:**",
        *[f"- {b}" for b in rb],
        "",
    ]
    for name, items in buckets:
        if not items:
            continue
        out.append(f"## {name}")
        out.append(fmt_section_items(items) or "- _No curated links yet_.")
        out.append("")
    return "\n".join(out).strip()


# --- Analyzer module ---------------------------------------------------------


class RepositoryAnalyzer(dspy.Module):
    def __init__(self, final_lm=None):
        super().__init__()
        self.analyze_repo = dspy.ChainOfThought(AnalyzeRepository)
        self.analyze_structure = dspy.ChainOfThought(AnalyzeCodeStructure)
        self.generate_examples = dspy.ChainOfThought(GenerateUsageExamples)
        self.generate_llms_txt = dspy.ChainOfThought(GenerateLLMsTxt)  # compatibility
        self.final_lm = final_lm  # set to a plain-text LM

    def forward(self, repo_url, file_tree, readme_content, package_files):
        repo_analysis = self.analyze_repo(
            repo_url=repo_url,
            file_tree=file_tree,
            readme_content=readme_content,
        )
        structure_analysis = self.analyze_structure(
            file_tree=file_tree,
            package_files=package_files,
        )
        _ = self.generate_examples(  # not rendered in llms.txt yet, but keep the signal
            repo_info=(
                f"Purpose: {repo_analysis.project_purpose}\n\n"
                f"Concepts: {', '.join(repo_analysis.key_concepts or [])}\n\n"
                f"Entry points: {', '.join(structure_analysis.entry_points or [])}\n"
            )
        )

        # Friendly project name from repo URL
        try:
            from repo_helpers import owner_repo_from_url

            owner, repo = owner_repo_from_url(repo_url)
            project_name = repo.replace("-", " ").replace("_", " ").title()
        except Exception:
            project_name = "Project"

        # --- NEW: dynamic buckets (LangGraph-style) ---
        dynamic_buckets = _build_dynamic_buckets(repo_url, file_tree)

        llms_txt_content = _render_llms_markdown_v2(
            project_name=project_name,
            project_purpose=repo_analysis.project_purpose
            or "Project overview unavailable.",
            remember_bullets=repo_analysis.key_concepts or [],
            buckets=dynamic_buckets,
        )

        # If needed elsewhere, we still return the legacy analysis objects
        return dspy.Prediction(
            llms_txt_content=llms_txt_content,
            analysis=repo_analysis,
            structure=structure_analysis,
        )
