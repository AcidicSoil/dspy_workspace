# repository_analyzer.py — deterministic llms.txt builder (ctx-compatible)
import re
import dspy
from signatures import (
    AnalyzeRepository,
    AnalyzeCodeStructure,
    GenerateUsageExamples,
    GenerateLLMsTxt,
)
from typing import List, Tuple


def _nicify_title(name: str) -> str:
    base = name.rsplit("/", 1)[-1]
    base = re.sub(r"\.(md|rst|txt|py|ipynb|js|ts)$", "", base, flags=re.I)
    base = base.replace("-", " ").replace("_", " ")
    return base.strip().title() or name


def _select_paths(file_tree: str, patterns: List[str]) -> List[str]:
    paths = [p.strip() for p in file_tree.splitlines() if p.strip()]
    out = []
    for p in paths:
        for pat in patterns:
            if re.search(pat, p, flags=re.I):
                out.append(p)
                break
    # de-dup preserving order
    seen = set(); uniq = []
    for p in out:
        if p not in seen:
            uniq.append(p); seen.add(p)
    return uniq


def _build_links(repo_url: str, file_tree: str) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    from repo_helpers import construct_raw_url

    # Priority picks
    readme_first = _select_paths(file_tree, [r"(^|/)README\.md$"])
    docs_md = _select_paths(file_tree, [r"(^|/)(docs?|documentation)/.*\.md$"])
    root_md = _select_paths(file_tree, [r"^[^/]+\.md$"])

    examples = _select_paths(file_tree, [
        r"(^|/)(examples?|demos?|tutorials?)/.*\.(md|py|ipynb|js|ts)$"
    ])

    optional = _select_paths(file_tree, [
        r"(^|/)CONTRIBUTING\.md$",
        r"(^|/)CHANGELOG\.md$",
        r"(^|/)HISTORY\.md$",
        r"(^|/)BENCHMARKS?\.md$",
        r"(^|/)LICENSE(\.|$)",
        r"(^|/)SECURITY\.md$",
    ])

    # Build at most N links for each section
    def to_links(paths, note_hint):
        links = []
        for p in paths:
            url = construct_raw_url(repo_url, p)
            title = "README" if re.search(r"(^|/)README\.md$", p, flags=re.I) else _nicify_title(p)
            note = note_hint(p)
            links.append((title, url, note))
        return links

    docs_links = []
    docs_links += to_links(readme_first[:1], lambda p: "overview and usage.")
    # Prefer a handful of docs pages
    docs_links += to_links(docs_md[:6], lambda p: "docs page.")
    # Then a couple of root .mds (skipping README which we already added)
    root_md_filtered = [p for p in root_md if not re.search(r"(^|/)README\.md$", p, flags=re.I)]
    docs_links += to_links(root_md_filtered[:4], lambda p: "reference page.")
    docs_links = docs_links[:8]

    example_links = to_links(examples[:6], lambda p: "worked example.")

    optional_links = to_links(optional[:8], lambda p: "optional reading.")

    # If nothing found at all, at least link README (raw) as Docs
    if not docs_links and readme_first:
        p = readme_first[0]
        url = construct_raw_url(repo_url, p)
        docs_links.append(("README", url, "overview and usage."))

    return docs_links, example_links, optional_links


def _render_llms_markdown(project_name: str, project_purpose: str, remember_bullets: List[str], docs_links, example_links, optional_links) -> str:
    # constrain remember bullets 3–6 items
    rb = [str(b).strip().rstrip(".") for b in remember_bullets if str(b).strip()]
    rb = rb[:6] or ["Key concepts and usage patterns", "Common pitfalls and best practices", "Consult Docs and Examples links below"]
    if len(rb) < 3:
        rb += ["Follow the docs for setup", "Use examples as starting points"][: 3 - len(rb)]

    def fmt_links(links):
        return "\n".join([f"- [{title}]({url}): {note}" for (title, url, note) in links]) or "- [README](https://example.com): overview."

    md = f"""# {project_name}

> {project_purpose.strip().replace('\n', ' ')}

**Remember:**
""" + "\n".join([f"- {b}" for b in rb]) + """

## Docs
""" + fmt_links(docs_links) + """

## Examples
""" + fmt_links(example_links) + """

## Optional
""" + fmt_links(optional_links) + "\n"

    return md


class RepositoryAnalyzer(dspy.Module):
    def __init__(self, final_lm=None):
        super().__init__()
        self.analyze_repo = dspy.ChainOfThought(AnalyzeRepository)
        self.analyze_structure = dspy.ChainOfThought(AnalyzeCodeStructure)
        self.generate_examples = dspy.ChainOfThought(GenerateUsageExamples)
        self.generate_llms_txt = dspy.ChainOfThought(GenerateLLMsTxt)  # kept for compatibility if needed
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
        usage_examples = self.generate_examples(
            repo_info=(
                f"Purpose: {repo_analysis.project_purpose}\n\n"
                f"Concepts: {', '.join(repo_analysis.key_concepts or [])}\n\n"
                f"Entry points: {', '.join(structure_analysis.entry_points or [])}\n"
            )
        )

        # Derive a friendly project name
        try:
            from repo_helpers import owner_repo_from_url
            owner, repo = owner_repo_from_url(repo_url)
            project_name = repo.replace('-', ' ').replace('_', ' ').title()
        except Exception:
            project_name = "Project"

        docs_links, example_links, optional_links = _build_links(repo_url, file_tree)

        llms_txt_content = _render_llms_markdown(
            project_name=project_name,
            project_purpose=repo_analysis.project_purpose or "Project overview unavailable.",
            remember_bullets=repo_analysis.key_concepts or [],
            docs_links=docs_links,
            example_links=example_links,
            optional_links=optional_links,
        )

        return dspy.Prediction(
            llms_txt_content=llms_txt_content,
            analysis=repo_analysis,
            structure=structure_analysis,
        )
