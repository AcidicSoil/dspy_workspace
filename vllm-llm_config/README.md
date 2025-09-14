# vllm-llm_config – Purpose

## About
Example scripts and settings for running the library-learning workflow against [vLLM](https://github.com/vllm-project/vllm) servers.  The layout mirrors the Ollama configuration but targets the vLLM API.

## Contents
- `main.py` – drives the learning and summarization process.
- `interactive_learning.py` & `learn_library.py` – support scripts for conversational exploration.
- `generate_examples.py` – generate code samples from inferred APIs.
- `repo_helpers.py` – shared repository utilities.
- `litellm_learning.json` – sample model configuration.

## How to Use
Deploy a vLLM server and run `python main.py --library <name>` to explore a library.  Modify the JSON config to select different models or endpoints.

## Development Notes
Assumes the same Python dependencies as the base library-learning utilities (`requests`, `bs4`, `html2text`, etc.).

## Related Links
- [vLLM project](https://github.com/vllm-project/vllm)

## Status/TODO
Currently provided as a template; extend with real model settings as needed.
