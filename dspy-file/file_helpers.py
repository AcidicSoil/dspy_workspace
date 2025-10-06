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


def read_file_content(path: Path) -> str:
    """Read file contents using utf-8 and fall back to latin-1 if needed."""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def render_prediction(result: dspy.Prediction) -> str:
    """Return the generated teaching brief markdown."""

    try:
        report = result.report.report_markdown  # type: ignore[attr-defined]
    except AttributeError:
        report = "# Teaching Brief\n\nThe DSPy pipeline did not produce a report."
    return report if report.endswith("\n") else report + "\n"
