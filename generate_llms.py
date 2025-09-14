# generate_llms.py — add CLI + guard for empty repo URL (fixed)
from dotenv import load_dotenv
import argparse
import dspy
from repository_analyzer import RepositoryAnalyzer
from repo_helpers import gather_repository_info

load_dotenv()

def generate_llms_txt_for_dspy(repo_url: str):
    if not repo_url:
        raise ValueError("Missing --repo URL. Provide https://github.com/<owner>/<repo>")
    # Correct Ollama LM initialization
    lm = dspy.LM(
        "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
        api_base="http://localhost:11434",
        api_key="",
        streaming=False,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["name", "description"],
                        },
                        "key_concepts": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                        "architecture_overview": {"type": "string"},
                        "important_directories": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                        "entry_points": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                        "development_info": {
                            "type": "object",
                            "properties": {
                                "test_dependencies": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                                "linting_tools": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                                "optional_dependencies": {"type": "array", "items": {"type": "string"}},
                            },
                            "required": ["test_dependencies", "linting_tools"],
                        },
                        "usage_examples": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    },
                    "required": [
                        "project",
                        "key_concepts",
                        "architecture_overview",
                        "important_directories",
                        "entry_points",
                        "development_info",
                        "usage_examples",
                    ],
                }
            },
        },
    )
    dspy.configure(lm=lm)

    analyzer = RepositoryAnalyzer()
    file_tree, readme_content, package_files = gather_repository_info(repo_url)

    result = analyzer(
        repo_url=repo_url,
        file_tree=file_tree,
        readme_content=readme_content,
        package_files=package_files,
    )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate llms.txt for a GitHub repo")
    parser.add_argument("--repo", required=True, help="GitHub repo URL (https://github.com/<owner>/<repo>)")
    args = parser.parse_args()

    result = generate_llms_txt_for_dspy(repo_url=args.repo)
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(result.llms_txt_content)
    print("Generated llms.txt file!")
    print("\nPreview:")
    print(result.llms_txt_content[:500] + "...")
