# repo_helpers.py — robust GitHub helpers (fixed)
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def _build_headers():
    """Build GitHub API headers. Token is optional but recommended."""
    token = os.getenv("GITHUB_ACCESS_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "llms-txt-generator/1.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def _parse_owner_repo(repo_url: str):
    """Return (owner, repo) from a GitHub URL like:
    https://github.com/<owner>/<repo>[.git][/...]
    """
    if not repo_url or not isinstance(repo_url, str):
        raise ValueError("repo_url is empty. Provide https://github.com/<owner>/<repo>")
    url = repo_url.strip().rstrip("/").removesuffix(".git")
    parts = url.split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid repo URL: {repo_url!r}")
    owner, repo = parts[-2], parts[-1]
    if not owner or not repo or owner == "github.com":
        # handle accidental formats like 'github.com/owner/repo'
        try:
            idx = parts.index("github.com")
            owner, repo = parts[idx+1], parts[idx+2]
        except Exception:
            raise ValueError(f"Invalid GitHub repo URL: {repo_url!r}. Expected https://github.com/<owner>/<repo>")
    return owner, repo

def _get_default_branch(owner: str, repo: str):
    res = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=_build_headers())
    if res.status_code == 200:
        return res.json().get("default_branch", "main")
    # Fallback if repo lookup fails for any reason
    return "main"

def get_github_file_tree(repo_url: str) -> str:
    """Get repository file structure from GitHub API."""
    owner, repo = _parse_owner_repo(repo_url)
    branch = _get_default_branch(owner, repo)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(api_url, headers=_build_headers())
    if res.status_code == 200:
        data = res.json()
        file_paths = [item["path"] for item in data.get("tree", []) if item.get("type") == "blob"]
        return "\n".join(sorted(file_paths))
    raise Exception(f"Failed to fetch repository tree ({res.status_code}): {res.text}")

def get_github_file_content(repo_url: str, file_path: str, ref: str | None = None) -> str:
    """Get specific file content from GitHub."""
    owner, repo = _parse_owner_repo(repo_url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    params = {"ref": ref} if ref else None
    res = requests.get(api_url, headers=_build_headers(), params=params)
    if res.status_code == 200:
        try:
            return base64.b64decode(res.json().get("content", "")).decode("utf-8", errors="replace")
        except Exception:
            return f"Could not decode {file_path}"
    return f"Could not fetch {file_path}"

def gather_repository_info(repo_url: str):
    """Gather all necessary repository information."""
    owner, repo = _parse_owner_repo(repo_url)
    branch = _get_default_branch(owner, repo)

    file_tree = get_github_file_tree(repo_url)
    readme_content = get_github_file_content(repo_url, "README.md", ref=branch)

    package_files = []
    for file_path in ["pyproject.toml", "setup.py", "requirements.txt", "package.json"]:
        content = get_github_file_content(repo_url, file_path, ref=branch)
        if content and not content.startswith("Could not fetch"):
            package_files.append(f"=== {file_path} ===\n{content}")

    package_files_content = "\n\n".join(package_files)
    return file_tree, readme_content, package_files_content
