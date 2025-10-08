# Full Stack Open (/en) Offline Markdown Mirror

This repo mirrors **<https://fullstackopen.com/en/>** to local Markdown for personal offline reference and programmatic reuse. It uses **crawl4ai** with strict safety guardrails.

## Motivation

The primary motivation for this project is to create a personal, offline-first copy of the excellent Full Stack Open curriculum. This allows for:

- **Offline Access:** Study the course material without an internet connection.
- **Local Search:** Use local search tools like `grep` or `ripgrep` to instantly find content across the entire course.
- **Programmatic Use:** Enables building other tools on top of the content, such as flashcard generators or concept extractors.
- **Long-Term Archive:** Preserves a personal copy of the course material.

## Features

- **Web Crawling:** Uses `crawl4ai` to efficiently crawl and download the course content.
- **Markdown Conversion:** Converts the HTML content to clean, readable Markdown.
- **Image Downloading:** Downloads and locally stores all images referenced in the course.
- **Link Fixing:** Rewrites all links to point to the local Markdown files, ensuring a seamless offline experience.
- **Link Validation:** A pre-commit hook is included to validate all internal links, preventing broken links.
- **Safety First:** The crawler is configured with strict guardrails to only crawl the `/en/` section of `fullstackopen.com`, honors `robots.txt`, and uses conservative concurrency settings.

## Install

This project uses `uv` for environment and dependency management.

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install dependencies in editable mode, including dev tools
uv pip install -e '.[dev]'

# Optional: Install Playwright browsers for JS-rendered pages
python -m playwright install chromium
```

## One-command runs

The `crawl` command is defined in `pyproject.toml`.

```bash
# Full fresh crawl + postprocess + linkcheck
uv run crawl --fresh

# Incremental since a date
uv run crawl --since 2025-01-01

# Dry run (no writes)
uv run crawl --dry-run

# Save raw HTML alongside Markdown
uv run crawl --save-html
```

## Code Quality

This project uses `ruff` for linting/formatting, `mypy` for type checking, and `bandit` for security scanning.

```bash
# Format code
ruff format .

# Lint for issues
ruff check .

# Type check
mypy .

# Run security scan
bandit -r .
```

## Project Structure

```
fullstackopen-en-repo/
├── .githooks/
│   └── pre-commit
├── assets/
│   └── .keep
├── data/
│   └── .keep
├── logs/
│   └── .keep
├── src/
│   └── fullstackopen_en_repo/
│       ├── crawl_fullstackopen.py
│       ├── linkcheck.py
│       ├── postprocess.py
│       └── utils_slug.py
├── .gitignore
├── crawl.config.yml
├── main.py
├── pyproject.toml
├── README.md
└── seeds.txt
```

## Refresh later

- Update `seeds.txt` if the course gains new parts.
- Re-run with `--since YYYY-MM-DD` to limit fetches.
- Deterministic queue: URLs sorted, stable slugging, normalized headings.

## Pre-commit hook

Enable the provided hook to block commits if linkcheck fails.

```bash
git config core.hooksPath .githooks
```

## License and use

Course content copyright to its owners. This mirror is **for personal use only**.
