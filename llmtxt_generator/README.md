# llmtxt_generator – Purpose

## About
Tools for generating `llms.txt` metadata files describing repositories for LLM context ingestion. Includes both command-line utilities and a small web interface built with FastAPI.

## Contents
- `generate_llms.py` – single-repo generator script.
- `multiple-repo_llmstxt.py` – process many repositories sequentially.
- `repository_analyzer.py` & `repo_helpers.py` – analyze repository structure and README content.
- `signatures.py` – DSPy signature definitions for the analyzer.
- `web_interface.py` – FastAPI app providing a simple form-based UI.
- `templates/` – Jinja2 templates used by the web app.

## How to Use
Run `python generate_llms.py --repo <URL>` for a single project or `python multiple-repo_llmstxt.py --file list.txt` to batch process. Launch the web interface with `uvicorn llmtxt_generator.web_interface:app`.

## Development Notes
Requires DSPy, `requests`, `python-dotenv`, and `fastapi` with `uvicorn` for the web UI.

## Related Links
- [DSPy documentation](https://dspy.ai)

## Status/TODO
Error handling and unit tests are minimal and should be expanded.
