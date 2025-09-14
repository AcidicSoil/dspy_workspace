# ollama-llm_config – Purpose

## About
Configuration files and scripts for experimenting with DSPy using the [Ollama](https://ollama.com/) local LLM server.  They mirror the generic library-learning utilities with settings tailored for the Ollama backend.

## Contents
- `main.py` – entry point for generating library summaries.
- `interactive_learning.py` & `learn_library.py` – interactive exploration helpers.
- `generate_examples.py` – produce sample code from learned APIs.
- `repo_helpers.py` – common repository utilities.
- `litellm_learning.json` / `vllm_learning.json` – example model configurations.

## How to Use
Ensure an Ollama server is running, then execute `python main.py --library <name>` to query a library using the configured models.  Adjust the JSON configs to swap models or parameters.

## Development Notes
Relies on `requests`, `html2text`, and `python-dotenv` for HTTP access and environment management.

## Related Links
- [Ollama project](https://ollama.com)

## Status/TODO
Configuration files are samples; adapt them for your environment.
