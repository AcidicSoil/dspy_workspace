# path: repo_full_builder.py
import base64, os, re, textwrap
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple
import requests

# --- GitHub helper -----------------------------------------------------------


@dataclass
class GhRef:
    owner: str
    repo: str
    path: str
    ref: Optional[str] = None  # branch/sha


_GH_LINK = re.compile(
    r"https?://(?:raw\.githubusercontent\.com|github\.com)/(?P<owner>[^/]+)/(?P<repo>[^/]+)/"
    r"(?:(?:blob|tree)/)?(?P<ref>[^/]+)/(?P<path>.+)$",
    re.I,
)


def parse_github_link(url: str) -> Optional[GhRef]:
    m = _GH_LINK.match(url)
    if not m:
        return None
    d = m.groupdict()
    return GhRef(d["owner"], d["repo"], d["path"], d.get("ref"))


def gh_get_file(
    owner: str,
    repo: str,
    path: str,
    ref: Optional[str] = None,
    token: Optional[str] = None,
) -> Tuple[str, bytes]:
    """
    Fetch a file body via the GitHub Contents API, returning (mime_hint, content_bytes).
    Uses base64 decoding per API docs. Auth increases rate limit.
    """
    # GitHub "Get repository content" endpoint returns base64 for files.
    # https://docs.github.com/en/rest/repos/contents  (Contents API)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": ref} if ref else {}
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, params=params, headers=headers, timeout=30)
    if r.status_code == 404:
        raise FileNotFoundError(
            f"GitHub 404 for {owner}/{repo}/{path}@{ref or 'default'}"
        )
    r.raise_for_status()
    js = r.json()
    if js.get("encoding") == "base64":
        raw = base64.b64decode(js["content"])
    else:
        # Some media types may be returned raw if a different Accept is used.
        raw = js.get("content", "").encode("utf-8", "ignore")
    mime_hint = js.get("type", "file")
    return mime_hint, raw


# --- llms-full builder -------------------------------------------------------

_PAGE_LINK = re.compile(
    r"^\s*-\s*\[(?P<title>.+?)\]\((?P<url>https?://[^\s)]+)\)", re.M
)


def iter_llms_links(curated_text: str) -> Iterable[Tuple[str, str]]:
    """
    Yields (title, url) for bullets like: - [Title](URL): note.
    """
    for m in _PAGE_LINK.finditer(curated_text):
        yield m.group("title").strip(), m.group("url").strip()


def sanitize_path_for_block(title: str, url: str, gh: Optional[GhRef]) -> str:
    if gh:
        p = gh.path
    else:
        p = title.lower().strip().replace(" ", "-")
    # ensure no leading slash to keep blocks consistent
    return p.lstrip("/")


def build_llms_full_from_repo(
    curated_llms_text: str,
    max_bytes_per_file: int = 800_000,  # keep blocks manageable
    max_files: int = 100,  # cap to avoid huge contexts
) -> str:
    """
    Builds a LangGraph-style llms-full: concatenated blocks delimited with:
        --- path/to/file.md ---
        <file content>
    For GitHub links, fetch via Contents API with GITHUB_TOKEN for private repos.
    Non-GitHub links are skipped (or you may add custom fetchers).
    """
    token = os.getenv("GITHUB_ACCESS_TOKEN") or os.getenv("GH_TOKEN")
    blocks = []
    seen = set()
    count = 0

    for title, url in iter_llms_links(curated_llms_text):
        if count >= max_files:
            break
        gh = parse_github_link(url)
        if not gh:
            # Skip off-domain for now; keep curated and predictable.
            continue

        key = (gh.owner, gh.repo, gh.path, gh.ref or "")
        if key in seen:
            continue
        seen.add(key)

        try:
            _, body = gh_get_file(gh.owner, gh.repo, gh.path, gh.ref, token)
        except Exception as e:
            # Insert a clear diagnostic instead of a raw 404 page.
            err = f"[fetch-error] {gh.owner}/{gh.repo}/{gh.path}@{gh.ref or 'default'} :: {e}"
            body = err.encode("utf-8")

        if len(body) > max_bytes_per_file:
            body = body[:max_bytes_per_file] + b"\n[truncated]\n"

        path_for_block = sanitize_path_for_block(title, url, gh)
        blocks.append(f"--- {path_for_block} ---\n{body.decode('utf-8', 'replace')}\n")
        count += 1

    disclaimer = textwrap.dedent(
        """\
        # llms-full (private-aware)
        > Built by authenticated GitHub API fetches. Large files may be truncated.
        """
    )
    return disclaimer + "\n" + "\n".join(blocks)
