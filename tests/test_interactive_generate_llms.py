import importlib.util
import pathlib
import subprocess
import sys
import types

MODULE_PATH = (
    pathlib.Path(__file__).parent.parent
    / "tutorials"
    / "multi-llmtxt_generator"
    / "interactive_generate_llms.py"
)

# Stub out helper modules expected by the script so it imports cleanly.
dummymod = types.ModuleType("repo_helpers")
dummymod.gather_repository_info = lambda _: ([], "", [])
sys.modules["repo_helpers"] = dummymod
sys.modules["fixed_repo_helpers"] = dummymod

spec = importlib.util.spec_from_file_location("interactive_generate_llms", MODULE_PATH)
module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
assert spec and spec.loader
spec.loader.exec_module(module)  # type: ignore[attr-defined]
stop_ollama_model = module.stop_ollama_model


def test_stop_ollama_model_calls_subprocess_run(monkeypatch):
    called = {}

    def fake_run(cmd, check, capture_output):
        called["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    stop_ollama_model("test-model")
    assert called["cmd"] == ["ollama", "stop", "test-model"]


def test_stop_ollama_model_handles_error(monkeypatch, capsys):
    def fake_run(cmd, check, capture_output):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    stop_ollama_model("bad-model")
    out = capsys.readouterr().out
    assert "Failed to stop model bad-model" in out
