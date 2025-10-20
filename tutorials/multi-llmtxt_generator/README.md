# Multi LLM txt Generator Tutorial

This tutorial shows how to create `llms.txt` context files for any public GitHub repository by combining DSPy prompting with repository metadata pulled from the GitHub API. It includes an automated batch script and an interactive CLI helper so you can experiment with different repositories quickly.

## Prerequisites

- Python 3.11 or later (matches the workspace requirement in `pyproject.toml`)
- A working [Ollama](https://ollama.ai/) instance with the `Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS` model pulled locally

  ```bash
  ollama pull hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS
  ```

- GitHub personal access token stored in the environment variable `GITHUB_ACCESS_TOKEN` (read-only scopes are sufficient)
- `.env` file (optional) for convenient storage of `GITHUB_ACCESS_TOKEN`

Install the Python dependencies from the project root:

```bash
pip install -e .
```

## Scripts

- `generate_llms.py` – pulls repository data and writes `llms.txt` for a fixed or programmatically supplied repository URL.
- `interactive_generate_llms.py` – prompts for a GitHub URL (or accepts `--repo`) before running the same analysis flow.
- `repo_helpers.py` – lightweight GitHub API helpers for file trees and raw file content.
- `repository_analyzer.py` – orchestrates DSPy chains to turn repository metadata into readable summaries.
- `signatures.py` – DSPy signature declarations that describe the subtasks handled by the analyzer.

## Usage

### 1. Prepare environment

1. Start your Ollama server (defaults to `http://localhost:11434`).
2. Export the GitHub token so API calls succeed without heavy rate limiting:

   ```bash
   export GITHUB_ACCESS_TOKEN=ghp_example_token
   ```

   Alternatively place the token in a local `.env` file; `python-dotenv` loads it automatically.

### 2. Generate `llms.txt` for a known repository

```bash
python tutorials/multi-llmtxt_generator/generate_llms.py
```

The script defaults to `https://github.com/openai/openai-agents-python`. To target a different project, pass a new URL when calling `generate_llms_txt_for_dspy` from your own driver script:

```python
from tutorials.multi_llmtxt_generator.generate_llms import generate_llms_txt_for_dspy

generate_llms_txt_for_dspy("https://github.com/stanfordnlp/dspy")
```

### 3. Use the interactive helper

```bash
python tutorials/multi-llmtxt_generator/interactive_generate_llms.py --repo https://github.com/owner/repo
```

If `--repo` is omitted the script prompts until it receives a valid GitHub URL. The resulting `llms.txt` file is written to the current working directory and the first 500 characters are echoed to the console.

## Customizing the LM

- Change the Ollama model by editing the `dspy.LM` configuration in either script.
- Set `api_key` if your LM endpoint requires authentication.
- Adjust `response_format` in `generate_llms.py` to tailor the JSON schema returned by the model.

## Troubleshooting

- `Failed to fetch repository tree`: verify `GITHUB_ACCESS_TOKEN` is set and has access to the repository.
- `Connection refused` from Ollama: ensure the Ollama daemon is running and reachable at the `api_base` configured in the scripts.

With these pieces in place you can iterate on your own repository analyzers or plug the generated `llms.txt` files into other tutorials in this workspace.
