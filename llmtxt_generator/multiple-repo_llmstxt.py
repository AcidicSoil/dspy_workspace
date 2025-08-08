# generate_llms.py

from dotenv import load_dotenv
import dspy
from repository_analyzer import RepositoryAnalyzer
from repo_helpers import gather_repository_info

load_dotenv()

"""
def generate_llms_txt_for_dspy():
    # Existing single repo function (unchanged)
    lm = dspy.LM(
        "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
        api_base="http://localhost:11434",
        api_key="EMPTY",
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

    repo_url = "https://github.com/stanfordnlp/dspy"
    file_tree, readme_content, package_files = gather_repository_info(repo_url)

    result = analyzer(
        repo_url=repo_url,
        file_tree=file_tree,
        readme_content=readme_content,
        package_files=package_files,
    )

    return result
"""

def generate_llms_txt_for_multiple_repos(repo_urls):
    lm = dspy.LM(
        "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
        api_base="http://localhost:11434",
        api_key="EMPTY",
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
    """
    Analyze multiple repositories and generate llms.txt content for each.

    Args:
        repo_urls (list of str): List of GitHub repository URLs.

    Returns:
        dict: Mapping from repo_url to analysis result (dspy.Prediction)
    """
    analyzer = RepositoryAnalyzer()
    results = {}

    for repo_url in repo_urls:
        print(f"Processing repository: {repo_url}")
        try:
            file_tree, readme_content, package_files = gather_repository_info(repo_url)
            result = analyzer(
                repo_url=repo_url,
                file_tree=file_tree,
                readme_content=readme_content,
                package_files=package_files,
            )
            results[repo_url] = result
        except Exception as e:
            print(f"Error processing {repo_url}: {e}")
            results[repo_url] = None

    return results


if __name__ == "__main__":
    # Example usage with multiple repos
    repo_list = [
        "https://github.com/vllm-project/vllm",
        "https://github.com/BerriAI/litellm",  # example second repo
    ]

    multiple_results = generate_llms_txt_for_multiple_repos(repo_list)

    for repo_url, result in multiple_results.items():
        if result is None:
            print(f"Failed to analyze {repo_url}")
            continue
        filename = repo_url.split("/")[-1] + "_llms.txt"
        with open(filename, "w") as f:
            f.write(result.llms_txt_content)
        print(f"Generated {filename} for repository: {repo_url}")
