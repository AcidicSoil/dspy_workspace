# DSPy File Analyzer

This folder contains a small DSPy program that analyzes a single file and produces a structured report covering:

- an overview of the file and its major sections
- key teaching points, workflows, and pitfalls highlighted in the material
- a polished markdown brief suitable for sharing with learners

The implementation mirrors the multi-file tutorial (`tutorials/multi-llmtxt_generator`) but focuses on per-file inference. The program is split into:

- `dspy_file/signatures.py` – DSPy signatures that define inputs/outputs for each step
- `dspy_file/file_analyzer.py` – the main DSPy module that orchestrates overview, teaching extraction, and report composition
- `dspy_file/file_helpers.py` – utilities for loading files and rendering the markdown brief
- `dspy_file/analyze_file_cli.py` – command line entry point that configures the local model and prints results

## Requirements

- Python 3.10+
- DSPy installed in the environment
- Ollama running locally with the model `hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M` available
- (Optional) `.env` file for any additional DSPy configuration; `dotenv` is loaded automatically

Install the Python dependencies if you have not already:

```bash
uv pip install dspy dotenv
```

Ensure the Ollama server is running and the model is pulled:

```bash
ollama pull hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M
```

```bash
uv pip install -e .
```

## Usage

Run the CLI to extract a teaching brief from a file:

```bash
dspy-file-teaching path/to/your_file
```

Flags:

- `--raw` prints the raw DSPy prediction object instead of the formatted text report.

Example:

```bash
python -m dspy_file.analyze_file_cli ../some_project/app/main.py
```

Each run also saves the report under `dspy_file/data/` named after the analyzed file (e.g. `main.teaching.md`). If a file already exists, the CLI appends a numeric suffix to avoid overwriting previous runs.

The generated brief is markdown that mirrors the source material:

- Overview paragraphs for quick orientation
- Section-by-section bullets capturing the narrative
- Key concepts, workflows, pitfalls, and references learners should review

Behind the scenes the CLI:

1. Loads environment variables via `python-dotenv`.
2. Configures DSPy with the same local Ollama model used in the tutorial.
3. Reads the file contents, runs the DSPy `FileTeachingAnalyzer` module, and prints a human-friendly report.
4. Persists the report to the `dspy_file/data/` directory so results are easy to revisit.
5. Attempts to stop the Ollama model when finished, mirroring the fail-safe logic from the tutorial.

## Extending

- Adjust the `TeachingReport` signature or add new chains in `dspy_file/file_analyzer.py` to capture additional teaching metadata.
- Customize the render logic in `dspy_file.file_helpers.render_prediction` if you want richer CLI output or structured JSON.
- Add more signatures and module stages to capture additional metadata (e.g., security checks) and wire them into `FileAnalyzer`.

## Troubleshooting

- If the program cannot connect to Ollama, verify that the server is running on `http://localhost:11434` and the requested model has been pulled.
- When you see `ollama command not found`, ensure the `ollama` binary is on your `PATH`.
- For encoding errors, the helper already falls back to `latin-1`, but you can add more fallbacks in `file_helpers.read_file_content` if needed.
