# tutorials – Purpose

## About
Sample projects demonstrating DSPy concepts, including agent construction, conversation history management, and automatic `llms.txt` generation for multiple repositories.

## Contents
- `agents/` – full ReAct agent example with training and evaluation scripts.
- `conversation_history/` – minimal demo showing how to persist dialogue state.
- `multi-llmtxt_generator/` – batch utility for creating `llms.txt` files across repositories.

## How to Use
Enter a subdirectory and follow its README for environment setup and execution commands. Each tutorial is independent.

## Development Notes
Tutorial code depends on optional packages such as `mlflow` and `datasets`; install extras with `pip install -e .[dev]` if needed.

## Related Links
- [DSPy tutorial documentation](https://dspy.ai)

## Status/TODO
Additional tutorials and comprehensive tests may be added in the future.
