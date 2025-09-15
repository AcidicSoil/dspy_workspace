# multi-llmtxt_generator – Purpose

## About

Batch-processing utility for generating `llms.txt` descriptors for multiple GitHub repositories at once.  Extends the single-repo generator with iteration and optional interactive mode.

## Contents

- `generate_llms.py` – core batch generation script.
- `interactive_generate_llms.py` – interactive CLI for reviewing each repo.
- `repository_analyzer.py` & `repo_helpers.py` – helper modules for repository analysis.
- `signatures.py` – DSPy signature definitions used by the analyzer.

## How to Use

Provide a list of repository URLs to `generate_llms.py` or use the interactive script to step through one at a time. Results are written to per-repo `llms.txt` files.

## Development Notes

Requires network connectivity and a configured language model backend accessible via DSPy.

## Related Links

- [Single-repo generator](../../llmtxt_generator)

## Status/TODO

Support for parallel processing and richer error reporting is a future enhancement.
