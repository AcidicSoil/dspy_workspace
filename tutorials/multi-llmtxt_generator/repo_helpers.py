# repo_helpers.py

import requests
from dotenv import load_dotenv
import os

# os.environ["GITHUB_ACCESS_TOKEN"] = "<your_access_token>"
# Load variables from .env file into environment
load_dotenv()

def get_github_file_tree(repo_url):
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    """Get repository file structure from GitHub API."""
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(
        api_url,
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code == 200:
        tree_data = response.json()
        file_paths = [
            item["path"] for item in tree_data["tree"] if item["type"] == "blob"
        ]
        return "\n".join(sorted(file_paths))
    else:
        raise Exception(f"Failed to fetch repository tree: {response.status_code}")


def get_github_file_content(repo_url, file_path):
    """Get specific file content from GitHub."""
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(
        api_url,
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code == 200:
        import base64

        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return content
    else:
        return f"Could not fetch {file_path}"


def gather_repository_info(repo_url):
    """Gather all necessary repository information."""
    file_tree = get_github_file_tree(repo_url)
    readme_content = get_github_file_content(repo_url, "README.md")

    package_files = []
    for file_path in ["pyproject.toml", "setup.py", "requirements.txt", "package.json"]:
        try:
            content = get_github_file_content(repo_url, file_path)
            if "Could not fetch" not in content:
                package_files.append(f"=== {file_path} ===\n{content}")
        except:
            continue

    package_files_content = "\n\n".join(package_files)

    return file_tree, readme_content, package_files_content


# --- helpers for raw GitHub URLs ---

def owner_repo_from_url(repo_url: str):
    """Extract (owner, repo) from https or SSH GitHub URLs."""
    repo_url = repo_url.strip()
    if repo_url.startswith("git@github.com:"):
        rest = repo_url.split("git@github.com:", 1)[1]
        owner, repo = rest.split("/", 1)
        repo = repo.replace(".git", "").strip("/")
        return owner, repo
    if repo_url.startswith(("https://", "http://")):
        from urllib.parse import urlparse
        p = urlparse(repo_url)
        parts = [x for x in p.path.strip("/").split("/") if x]
        if len(parts) >= 2:
            owner, repo = parts[0], parts[1].replace(".git", "")
            return owner, repo
    raise ValueError("Unrecognized GitHub URL")

def construct_raw_url(repo_url: str, path: str) -> str:
    """Build a raw.githubusercontent.com URL for a file on the repo’s default branch."""
    owner, repo = owner_repo_from_url(repo_url)
    # Uses your existing get_default_branch(repo_url); falls back to 'main' if missing
    ref = get_default_branch(repo_url) if "get_default_branch" in globals() else "main"
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
