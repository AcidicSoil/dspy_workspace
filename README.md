# DSPy Workspace – Purpose

## About
This repository collects experiments, utilities, and tutorials built around the [DSPy](https://github.com/stanfordnlp/dspy) framework.  It bundles small applications, configuration examples for different LLM backends, and educational notebooks demonstrating how to compose DSPy programs.

## Contents
- `DSPY_Dev_Assistant/` – self-correcting developer assistant prototype.
- `llmtxt_generator/` – scripts and web UI to generate `llms.txt` descriptors for GitHub projects.
- `codeGeneration_for_unfamilar_libraries/` – interactive helper for exploring new Python libraries.
- `ollama-llm_config/` & `vllm-llm_config/` – configuration templates for different serving stacks.
- `tutorials/` – example agents and utilities showing DSPy usage.
- `scripts/` – helper shell scripts for environment setup and MLflow.

## How to Use
Each module is largely self-contained. Install dependencies with `pip install -e .[dev,web]` and run the scripts directly, e.g. `python generate_llms.py --repo <URL>`.  The `llmtxt_generator/web_interface.py` script can be started with `uvicorn llmtxt_generator.web_interface:app` for a simple UI.

## Development Notes
- Requires Python 3.9+.
- Linting is configured with [Ruff](https://ruff.rs/).
- Tests are executed via `pytest` (no tests are currently included).

## Related Links
- [DSPy documentation](https://dspy.ai)

## Status/TODO
This workspace is experimental and lacks packaging metadata such as license, author and project URLs.  Contributions are welcome.
