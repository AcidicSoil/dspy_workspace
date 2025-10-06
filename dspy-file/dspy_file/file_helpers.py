# file_helpers.py - utilities for loading files and presenting DSPy results
from __future__ import annotations

from pathlib import Path

import dspy


def resolve_file_path(raw_path: str) -> Path:
    """Expand user shortcuts and validate that the target file exists."""

    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Expected a file path but received: {path}")
    return path


def _strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end_idx = text.find("\n---", 3)
    if end_idx == -1:
        return text
    return text[end_idx + 4 :]


def _trim_to_first_heading(text: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            return "\n".join(lines[idx:])
    return text


def read_file_content(path: Path) -> str:
    """Read file contents using utf-8 and fall back to latin-1 if needed."""

    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="latin-1")

    cleaned = _strip_front_matter(raw)
    cleaned = _trim_to_first_heading(cleaned)
    return cleaned


def render_prediction(result: dspy.Prediction) -> str:
    """Return the generated teaching brief markdown."""

    try:
        report = result.report.report_markdown  # type: ignore[attr-defined]
    except AttributeError:
        report = "# Teaching Brief\n\nThe DSPy pipeline did not produce a report."
    return report if report.endswith("\n") else report + "\n"
