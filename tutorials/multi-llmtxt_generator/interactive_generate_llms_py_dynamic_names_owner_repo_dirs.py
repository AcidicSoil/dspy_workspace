# interactive_generate_llms.py — prompt user for a valid GitHub URL
# Timestamp comments are optional and added only if --stamp is passed.

import argparse
import os
import re
import subprocess
from datetime import datetime, timezone

import dspy
from dotenv import load_dotenv
from repository_analyzer import RepositoryAnalyzer
from repo_helpers import gather_repository_info

load_dotenv()

HTTPS_RE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", re.IGNORECASE
)
SSH_RE = re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", re.IGNORECASE)
MODEL_NAME = "hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M"


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


def split_owner_repo(normalized_https_url: str) -> tuple[str, str]:
    m = HTTPS_RE.match(normalized_https_url)
    if not m:
        raise ValueError("Unexpected URL format after normalization.")
    return m.group(1), m.group(2)


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


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def timestamp_comment(prefix: str = "# Generated", tzname: str | None = None) -> str:
    # Use UTC by default to avoid local ambiguity. User requested comment only.
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    tz_note = f" ({tzname})" if tzname else ""
    return f"{prefix}: {now} UTC{tz_note}"


def write_text(path: str, content: str, add_stamp: bool) -> None:
    if add_stamp:
        content = content.rstrip() + "\n\n" + timestamp_comment()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate llms.txt for a GitHub repo with organized owner/repo output"
        )
    )
    parser.add_argument(
        "--repo", help="GitHub repo URL (https://github.com/<owner>/<repo>)"
    )
    parser.add_argument(
        "--outdir",
        default="artifacts",
        help="Base directory to save outputs (default: ./artifacts)",
    )
    parser.add_argument(
        "--stamp",
        action="store_true",
        help="Append a timestamp as a trailing comment in each text file",
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

    owner, repo = split_owner_repo(repo_url)

    # Output directory: <outdir>/<owner>/<repo>
    repo_root = os.path.join(args.outdir, owner, repo)
    ensure_dir(repo_root)

    # Base names derived from repo for clarity; filenames avoid timestamps
    base = repo.lower()
    llms_path = os.path.join(repo_root, f"{base}-llms.txt")

    # Run analysis
    result = generate_llms_txt_for_dspy(repo_url=repo_url)

    # Keep a pristine in-memory copy for parsers (avoid stamping issues)
    txt = result.llms_txt_content

    # Write llms.txt-like artifact
    write_text(llms_path, result.llms_txt_content, add_stamp=args.stamp)

    # Prefer the canonical API, but fall back if needed
    try:
        from llms_txt import create_ctx
    except ImportError:
        from llm_ctx.core import create_ctx
    # Create contexts from the pristine in-memory text (no stamp inside parser input)

    ctx = create_ctx(txt, optional=False)
    ctx_full = create_ctx(txt, optional=True)

    ctx_path = os.path.join(repo_root, f"{base}-llms-ctx.txt")
    ctx_full_path = os.path.join(repo_root, f"{base}-llms-ctx-full.txt")

    write_text(ctx_path, ctx, add_stamp=args.stamp)
    write_text(ctx_full_path, ctx_full, add_stamp=args.stamp)

    print("Artifacts written:")
    print(f" - {llms_path}")
    print(f" - {ctx_path}")
    print(f" - {ctx_full_path}")

    # Show preview
    preview = (result.llms_txt_content or "").strip()
    head = preview[:500] + ("..." if len(preview) > 500 else "")
    print("\nPreview of llms content:\n")
    print(head)

    stop_ollama_model(MODEL_NAME)
