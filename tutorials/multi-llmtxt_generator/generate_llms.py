# generate_llms.py

from dotenv import load_dotenv
import dspy
from repository_analyzer import RepositoryAnalyzer
from repo_helpers import gather_repository_info

load_dotenv()

def generate_llms_txt_for_dspy(
    repo_url="https://github.com/openai/openai-agents-python",
):
    # Correct Ollama LM initialization
    lm = dspy.LM(
        "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
        api_base="http://localhost:11434",  # Local Ollama server URL
        api_key="",  # Usually empty for local Ollama; remove if you do not have a key
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
                        "key_concepts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                        "architecture_overview": {"type": "string"},
                        "important_directories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                        "entry_points": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                        "development_info": {
                            "type": "object",
                            "properties": {
                                "test_dependencies": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "minItems": 1,
                                },
                                "linting_tools": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "minItems": 1,
                                },
                                "optional_dependencies": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                            "required": ["test_dependencies", "linting_tools"],
                        },
                        "usage_examples": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
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

#    repo_url = "https://github.com/stanfordnlp/dspy"
    file_tree, readme_content, package_files = gather_repository_info(repo_url)

    result = analyzer(
        repo_url=repo_url,
        file_tree=file_tree,
        readme_content=readme_content,
        package_files=package_files,
    )

    return result


if __name__ == "__main__":
    result = generate_llms_txt_for_dspy()
    with open("llms.txt", "w") as f:
        f.write(result.llms_txt_content)
    print("Generated llms.txt file!")
    print("\nPreview:")
    print(result.llms_txt_content[:500] + "...")
