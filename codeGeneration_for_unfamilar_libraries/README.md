# codeGeneration_for_unfamilar_libraries – Purpose

## About
Utilities for exploring and learning the APIs of unfamiliar Python libraries using DSPy-driven agents.  The tools scrape documentation and generate example code to accelerate onboarding.

## Contents
- `main.py` – orchestrates the learning workflow and produces summaries.
- `interactive_learning.py` – CLI for iteratively querying a library.
- `learn_library.py` – helper functions used during exploration.
- `generate_examples.py` – builds code snippets from discovered APIs.
- `repo_helpers.py` – common routines for gathering repository metadata.

## How to Use
Run `python main.py --library <name>` to generate a quick reference for a new package, or launch `interactive_learning.py` to engage in a question–answer session about the library.

## Development Notes
Requires network access for documentation scraping. Ensure environment variables required by `python-dotenv` are configured.

## Related Links
- [DSPy](https://dspy.ai)

## Status/TODO
Additional tests and error handling are planned.
