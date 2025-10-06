# analyze_file_cli.py - command line entry point for DSPy file analyzer
from __future__ import annotations

import argparse
import sys
import subprocess
from pathlib import Path

import dspy
from dotenv import load_dotenv

from file_analyzer import FileTeachingAnalyzer
from file_helpers import read_file_content, render_prediction, resolve_file_path

MODEL_NAME = "hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M"
OLLAMA_BASE_URL = "http://localhost:11434"
DATA_DIR = Path(__file__).parent / "data"


def configure_local_model() -> None:
    """Configure DSPy to talk to the local Ollama model."""

    lm = dspy.LM(
        f"ollama_chat/{MODEL_NAME}",
        api_base=OLLAMA_BASE_URL,
        api_key="",
        streaming=False,
        cache=False,
    )
    dspy.configure(lm=lm)


def stop_ollama_model(model_name: str) -> None:
    """Stop the Ollama model to free server resources."""

    try:
        subprocess.run(
            ["ollama", "stop", model_name],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover - warn only
        print(f"Warning: Failed to stop model {model_name}: {exc}")
    except FileNotFoundError:
        print("Warning: ollama command not found while attempting to stop the model.")


def _write_output(original_name: str, content: str) -> Path:
    """Persist analyzer output under the data directory with de-duplicated file names."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(original_name).stem
    base_name = f"{stem}.teaching.md"
    output_path = DATA_DIR / base_name
    counter = 1
    while output_path.exists():
        output_path = DATA_DIR / f"{stem}.teaching-{counter}.md"
        counter += 1
    if not content.endswith('\n'):
        content = content + '\n'
    output_path.write_text(content, encoding='utf-8')
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a single file using DSPy signatures and modules",
    )
    parser.add_argument("path", help="Path to the file to analyze")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw DSPy prediction repr instead of formatted text",
    )
    return parser


def analyze_file(path: str, *, raw: bool) -> int:
    """Run the DSPy pipeline and render results to stdout."""

    resolved = resolve_file_path(path)
    content = read_file_content(resolved)

    analyzer = FileTeachingAnalyzer()
    prediction = analyzer(file_path=str(resolved), file_content=content)

    if raw:
        output_text = repr(prediction)
        print(output_text)
    else:
        output_text = render_prediction(prediction)
        print(output_text, end="")

    output_path = _write_output(resolved.name, output_text)
    print(f"Saved report to {output_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    configure_local_model()

    parser = build_parser()
    args = parser.parse_args(argv)

    exit_code = 0
    try:
        exit_code = analyze_file(args.path, raw=args.raw)
    except (FileNotFoundError, IsADirectoryError) as exc:
        parser.print_usage(sys.stderr)
        print(f"{parser.prog}: error: {exc}", file=sys.stderr)
        exit_code = 2
    except KeyboardInterrupt:
        exit_code = 1
    finally:
        stop_ollama_model(MODEL_NAME)

    return exit_code


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
