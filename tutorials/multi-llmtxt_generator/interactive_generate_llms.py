# interactive_generate_llms.py — prompt user for a valid GitHub URL
import argparse
import re
import subprocess

import dspy
from dotenv import load_dotenv

# Prefer the user's local helpers if present; fall back to fixed helpers.
try:
    from repo_helpers import gather_repository_info  # type: ignore
except Exception:
    from fixed_repo_helpers import gather_repository_info  # type: ignore

load_dotenv()

HTTPS_RE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", re.IGNORECASE
)
SSH_RE = re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", re.IGNORECASE)
MODEL_NAME = "hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS"


def normalize_repo_url(url: str) -> str:
    """Accept common GitHub URL forms and normalize to https form.
    Valid examples:
      - https://github.com/owner/repo
      - https://github.com/owner/repo.git
      - git@github.com:owner/repo.git
    Returns: https://github.com/<owner>/<repo>
    Raises: ValueError if not a recognizable GitHub URL.
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL cannot be empty.")
    url = url.strip()
    m = HTTPS_RE.match(url)
    if m:
        owner, repo = m.group(1), m.group(2)
        return f"https://github.com/{owner}/{repo}"
    m = SSH_RE.match(url)
    if m:
        owner, repo = m.group(1), m.group(2)
        return f"https://github.com/{owner}/{repo}"
    raise ValueError(
        "Invalid GitHub URL. Expected https://github.com/<owner>/<repo> "
        "or git@github.com:owner/repo.git"
    )


def prompt_for_repo_url() -> str:
    while True:
        try:
            raw = input(
                "Enter GitHub repo URL (e.g., https://github.com/<owner>/<repo>): "
            ).strip()
            normalized = normalize_repo_url(raw)
            return normalized
        except ValueError as e:
            print(f"\n{e}\nPlease try again.\n")
        except KeyboardInterrupt:
            print("\nCanceled by user.")
            raise SystemExit(1) from None


def generate_llms_txt_for_dspy(repo_url: str):
    # Correct Ollama LM initialization
    lm = dspy.LM(
        f"ollama_chat/{MODEL_NAME}",
        api_base="http://localhost:11434",
        api_key="",
        streaming=False,
        cache=False,
    )
    dspy.configure(lm=lm)

    file_tree, readme_content, package_files = gather_repository_info(repo_url)
    from repository_analyzer import (
        # Local import so script still works without analyzer until used
        RepositoryAnalyzer,
    )

    analyzer = RepositoryAnalyzer()
    result = analyzer(
        repo_url=repo_url,
        file_tree=file_tree,
        readme_content=readme_content,
        package_files=package_files,
    )
    return result


def stop_ollama_model(model_name: str) -> None:
    """Stop the specified Ollama model to free server resources."""
    try:
        subprocess.run(
            ["ollama", "stop", model_name],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover - log warning only
        print(f"Warning: Failed to stop model {model_name}: {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate llms.txt for a GitHub repo (interactive-friendly)"
    )
    parser.add_argument(
        "--repo", help="GitHub repo URL (https://github.com/<owner>/<repo>)"
    )
    args = parser.parse_args()

    repo_url = None
    if args.repo:
        try:
            repo_url = normalize_repo_url(args.repo)
        except ValueError as e:
            print(f"{e}\nFalling back to interactive prompt...\n")

    if not repo_url:
        repo_url = prompt_for_repo_url()

    result = generate_llms_txt_for_dspy(repo_url=repo_url)
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(result.llms_txt_content)
    print("Generated llms.txt file!\nPreview:\n")
    print(result.llms_txt_content[:500] + "...")
    stop_ollama_model(MODEL_NAME)
