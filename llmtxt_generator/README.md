# LLM txt Generator Toolkit

This directory bundles multiple ways to build `llms.txt` reference files for GitHub repositories using DSPy. The scripts can analyze a single repository, iterate across many, or expose an interactive web UI backed by FastAPI. All paths share the same analyzer code and GitHub helpers so you can mix and match workflows.

## Prerequisites
- Python 3.11 or later
- Running [Ollama](https://ollama.ai/) server with the `hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS` model pulled locally  
  ```bash
  ollama pull hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS
  ```
- GitHub personal access token stored in `GITHUB_ACCESS_TOKEN` (read-only scope is enough). You can export it in the shell or place it inside a `.env` file at the project root—`python-dotenv` loads it automatically.

Install dependencies from the workspace root:

```bash
pip install -e .
```

### Key Modules
- `generate_llms.py` – utility for a single repository.
- `multiple-repo_llmstxt.py` – loop over a list of repositories, writing one `llms.txt` per repo.
- `web_interface.py` – FastAPI app + Jinja templates for browser-based generation and downloading.
- `repository_analyzer.py` / `signatures.py` – DSPy chains and signatures for the summarization pipeline.
- `repo_helpers.py` – GitHub API helpers to fetch directory trees and packaging metadata.

## CLI Usage

### Generate for a single repository
```bash
python llmtxt_generator/generate_llms.py
```
By default the script expects `repo_url` to be supplied by the caller. You can wrap `generate_llms_txt_for_dspy` in your own driver script or shell to set the target:

```python
from llmtxt_generator.generate_llms import generate_llms_txt_for_dspy

result = generate_llms_txt_for_dspy("https://github.com/owner/repo")
with open("llms.txt", "w") as f:
    f.write(result.llms_txt_content)
```

### Batch multiple repositories
```bash
python llmtxt_generator/multiple-repo_llmstxt.py
```
Edit `repo_list` near the bottom of the script to match your targets. Each repository writes an `<repo>_llms.txt` file in the current working directory.

### Launch the web interface
The FastAPI app serves a simple form you can open in a browser.

```bash
uvicorn llmtxt_generator.web_interface:app --reload
```

Navigate to `http://127.0.0.1:8000`, enter a GitHub URL, and click **Generate** to preview the output. Use **Save** to download the content with a filename derived from the repository owner and name.

## Customization Tips
- Swap the LM by editing the `dspy.LM` configuration in each script (model name, base URL, API key).
- The GitHub helpers default to the `main` branch; adjust `repo_helpers.py` if you need branch selection.
- Tweak the JSON schema in `generate_llms.py` to guide model output formats for your downstream use case.

## Troubleshooting
- `Failed to fetch repository tree`: confirm `GITHUB_ACCESS_TOKEN` is valid and has access to the repo.
- `Connection refused` errors: ensure the Ollama daemon is running and listening on `http://localhost:11434`.
- FastAPI posts returning 422 or form errors: verify `python-multipart` is installed (pulled in by the project dependencies).
