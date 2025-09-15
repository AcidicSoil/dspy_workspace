# repo_helpers.py
# Contains functions for interacting with the GitHub API.

import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables from a .env file
load_dotenv()


def get_github_file_tree(repo_url):
    """Get repository file structure from the GitHub API."""
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    parts = repo_url.strip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    print(f"🌳 Fetching file tree for {owner}/{repo}...")
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        tree_data = response.json()
        # Filter for files (blobs) only
        file_paths = [
            item["path"] for item in tree_data.get("tree", []) if item["type"] == "blob"
        ]
        return "\n".join(sorted(file_paths))
    else:
        print(
            f"⚠️  Could not fetch repository tree (Status: {response.status_code}): {response.text}"
        )
        return "Could not fetch repository file tree."


def get_github_file_content(repo_url, file_path):
    """Get specific file content from a GitHub repository."""
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    parts = repo_url.strip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return content
    else:
        return f"Could not fetch {file_path}"


def gather_repository_info(repo_url):
    """
    Gathers the file tree, README, and example files from a repository.
    Focuses on README for overview and Python/Jupyter files for examples.
    """
    print(f"🔍 Gathering information from repository: {repo_url}")
    file_tree_str = get_github_file_tree(repo_url)

    if "Could not fetch" in file_tree_str:
        return "Could not access repository.", {}

    readme_content = get_github_file_content(repo_url, "README.md")

    # --- Find and fetch example files ---
    example_files = {}
    file_paths = file_tree_str.split("\n")

    # Look for common example directories or files
    example_keywords = ["examples", "example", "docs", "samples", "tutorial"]
    py_files = [p for p in file_paths if p.endswith(".py")]
    ipynb_files = [p for p in file_paths if p.endswith(".ipynb")]

    # Prioritize files in example-related directories
    potential_examples = [
        p
        for p in py_files + ipynb_files
        if any(keyword in p.lower() for keyword in example_keywords)
    ]

    # If not enough found, take a few from the root
    if len(potential_examples) < 5:
        potential_examples.extend(
            [p for p in py_files if "/" not in p][:5]
        )  # Top-level python files

    # Fetch content for a limited number of examples to avoid being overwhelming
    for i, file_path in enumerate(
        list(set(potential_examples))[:5]
    ):  # Limit to 5 unique examples
        print(f"📄 Fetching example file: {file_path}")
        content = get_github_file_content(repo_url, file_path)
        if "Could not fetch" not in content:
            example_files[file_path] = content

    # --- Combine all info into a single string for the LLM ---
    combined_content = f"# REPOSITORY OVERVIEW: {repo_url}\n\n"
    combined_content += "## README.md\n\n" + readme_content + "\n\n---\n\n"

    if example_files:
        combined_content += "## CODE EXAMPLES\n\n"
        for path, code in example_files.items():
            combined_content += f"### File: {path}\n\n```python\n{code}\n```\n\n"

    return combined_content, {"file_tree": file_tree_str, **example_files}
