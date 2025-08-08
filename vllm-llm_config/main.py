# main.py
# Purpose: Automated documentation-powered code generation pipeline using DSPy.
# Now with integrated GitHub repository analysis.

import dspy
import requests
from bs4 import BeautifulSoup
import html2text
from typing import List, Dict, Any
import json
import time

# Import the GitHub helper functions
from repo_helpers import gather_repository_info

# --- DSPy Configuration ---
# Replace with your actual LM provider if not using a local one
    # For models like Llama
lm = dspy.LM(
    "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q3_K_XL_XXS",
    api_base="http://localhost:11434",  # Local Ollama server URL
    api_key="EMPTY",  # Usually empty for local Ollama; remove if you do not have a key
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


# --- Data Fetching Classes ---


class DocumentationFetcher:
    """
    Fetches and processes documentation from both standard URLs and GitHub repositories.
    """

    def __init__(self, max_retries=3, delay=1):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        self.max_retries = max_retries
        self.delay = delay
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True

    def fetch_website_url(self, url: str) -> dict:
        """Fetches and cleans content from a standard website URL."""
        for attempt in range(self.max_retries):
            try:
                print(f"📡 Fetching Website: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                markdown_content = self.html_converter.handle(str(soup))
                return {
                    "url": url,
                    "title": soup.title.string if soup.title else "No title",
                    "content": markdown_content,
                    "success": True,
                }
            except Exception as e:
                print(f"❌ Error fetching {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay)
        return {"url": url, "title": "Failed to fetch", "content": "", "success": False}

    def fetch_github_repo(self, url: str) -> dict:
        """Fetches and consolidates content from a GitHub repository."""
        print(f"📦 Fetching GitHub Repo: {url}")
        try:
            # Use the helper function to get README and example files
            combined_content, details = gather_repository_info(url)
            if "Could not access" in combined_content:
                return {
                    "url": url,
                    "title": "Failed to fetch repo",
                    "content": "",
                    "success": False,
                }

            return {
                "url": url,
                "title": f"GitHub Repo: {url.split('/')[-1]}",
                "content": combined_content,
                "success": True,
                "details": details,
            }
        except Exception as e:
            print(f"❌ Error fetching GitHub repo {url}: {e}")
            return {
                "url": url,
                "title": "Failed to fetch repo",
                "content": f"Error: {e}",
                "success": False,
            }

    def fetch_documentation(self, urls: list[str]) -> list[dict]:
        """
        Fetches documentation from a list of URLs, routing to the correct
        fetcher (website or GitHub) based on the URL.
        """
        results = []
        for url in urls:
            if "github.com" in url:
                result = self.fetch_github_repo(url)
            else:
                result = self.fetch_website_url(url)

            results.append(result)
            time.sleep(self.delay)  # Be respectful to servers
        return results


# --- DSPy Signatures and Modules ---


class LibraryAnalyzer(dspy.Signature):
    """Analyze library documentation to understand core concepts, patterns, and examples."""

    library_name: str = dspy.InputField(desc="Name of the library to analyze")
    documentation_content: str = dspy.InputField(
        desc="Combined documentation from websites, READMEs, and code examples"
    )

    core_concepts: list[str] = dspy.OutputField(
        desc="Main concepts, classes, and components of the library."
    )
    common_patterns: list[str] = dspy.OutputField(
        desc="Common usage patterns or workflows."
    )
    key_methods: list[str] = dspy.OutputField(
        desc="List of important methods or functions and their purpose."
    )
    installation_info: str = dspy.OutputField(
        desc="How to install the library (e.g., 'pip install ...')."
    )
    code_examples: list[str] = dspy.OutputField(
        desc="Key code snippets found in the documentation."
    )


class CodeGenerator(dspy.Signature):
    """Generate a complete, working code example for a specific use case."""

    library_info: str = dspy.InputField(
        desc="Summary of the library's concepts, patterns, and methods."
    )
    use_case: str = dspy.InputField(
        desc="The specific task to accomplish with the code."
    )
    requirements: str = dspy.InputField(
        desc="Additional requirements or constraints for the code."
    )

    code_example: str = dspy.OutputField(
        desc="A single, complete, and runnable code block."
    )
    explanation: str = dspy.OutputField(
        desc="A step-by-step explanation of the generated code."
    )
    best_practices: list[str] = dspy.OutputField(
        desc="Tips and best practices for using the library."
    )
    imports_needed: list[str] = dspy.OutputField(
        desc="A list of necessary import statements."
    )


class DocumentationLearningAgent(dspy.Module):
    """Agent that learns from documentation and generates code."""

    def __init__(self):
        super().__init__()
        self.fetcher = DocumentationFetcher()
        self.analyze_docs = dspy.ChainOfThought(LibraryAnalyzer)
        self.generate_code = dspy.ChainOfThought(CodeGenerator)

    def learn_from_urls(self, library_name: str, doc_urls: list[str]) -> Dict:
        """Learns about a library from documentation URLs and GitHub repos."""
        print(f"📚 Learning about {library_name} from {len(doc_urls)} sources...")
        docs = self.fetcher.fetch_documentation(doc_urls)

        combined_content = "\n\n---\n\n".join(
            [
                f"SOURCE: {doc['url']}\n\n{doc['content']}"
                for doc in docs
                if doc["success"]
            ]
        )

        if not combined_content:
            raise ValueError("No documentation could be fetched successfully.")

        analysis = self.analyze_docs(
            library_name=library_name, documentation_content=combined_content
        )

        return {
            "library": library_name,
            "source_urls": [doc["url"] for doc in docs if doc["success"]],
            "core_concepts": analysis.core_concepts,
            "patterns": analysis.common_patterns,
            "methods": analysis.key_methods,
            "installation": analysis.installation_info,
            "examples": analysis.code_examples,
        }

    def generate_example(
        self, library_info: Dict, use_case: str, requirements: str = ""
    ) -> Dict:
        """Generates a code example for a specific use case."""
        info_text = f"""
        Library: {library_info["library"]}
        Core Concepts: {", ".join(library_info["core_concepts"])}
        Common Patterns: {", ".join(library_info["patterns"])}
        Key Methods: {", ".join(library_info["methods"])}
        Installation: {library_info["installation"]}
        """

        code_result = self.generate_code(
            library_info=info_text, use_case=use_case, requirements=requirements
        )

        return {
            "code": code_result.code_example,
            "explanation": code_result.explanation,
            "best_practices": code_result.best_practices,
            "imports": code_result.imports_needed,
        }


# --- Interactive Session Logic ---


def interactive_learning_session():
    """Main interactive session for the library learning system."""
    print("🎯 Welcome to the Interactive Library Learning System!")
    print("This system now supports learning from websites AND GitHub repositories.\n")

    agent = DocumentationLearningAgent()
    learned_libraries = {}

    while True:
        print("\n" + "=" * 60)
        library_name = input(
            "\n📚 Enter the library name (or 'quit' to exit): "
        ).strip()
        if library_name.lower() in ["quit", "exit", "q"]:
            break

        print(
            f"\n🔗 Enter documentation URLs or a GitHub repo URL for {library_name} (one per line, empty line to finish):"
        )
        urls = []
        while True:
            url = input("  URL: ").strip()
            if not url:
                break
            urls.append(url)

        if not urls:
            continue

        try:
            # Step 1: Learn about the library from the provided sources
            library_info = agent.learn_from_urls(library_name, urls)
            print(f"\n✅ Successfully learned {library_name}!")
            print(f"   - Core Concepts: {library_info.get('core_concepts', 'N/A')}")
            print(f"   - Installation: {library_info.get('installation', 'N/A')}")

            # Step 2: Get all use cases from the user upfront
            print(
                f"\n🎯 Define use cases for {library_name} (one per line, empty line to finish):"
            )
            use_cases = []
            while True:
                use_case = input("     Use case: ").strip()
                if not use_case:
                    break
                use_cases.append(use_case)

            if not use_cases:
                print("No use cases provided. Moving on.")
                continue

            # Step 3: Generate and display all examples
            print(f"\n🔧 Generating {len(use_cases)} examples for {library_name}...")
            all_examples = []
            for i, use_case in enumerate(use_cases, 1):
                print(f"\n--- EXAMPLE {i}/{len(use_cases)}: {use_case} ---")

                example = agent.generate_example(library_info, use_case)
                all_examples.append({"use_case": use_case, **example})

                print("\n💻 Code Example:")
                print(f"```python\n{example['code']}\n```")

                print("\n📦 Required Imports:")
                print("\n".join([f"  • {imp}" for imp in example["imports"]]))

                print("\n📝 Explanation:")
                print(example["explanation"])

                print("\n✅ Best Practices:")
                print("\n".join([f"  • {bp}" for bp in example["best_practices"]]))
                print("--- END OF EXAMPLE ---")

            # Store the complete results
            learned_libraries[library_name] = {
                "library_info": library_info,
                "examples": all_examples,
            }

            # Step 4: Offer to save the results to a file
            save_results = (
                input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
                .strip()
                .lower()
            )
            if save_results in ["y", "yes"]:
                filename = input(
                    f"   Enter filename (default: {library_name.lower()}_learning.json): "
                ).strip()
                if not filename:
                    filename = f"{library_name.lower()}_learning.json"

                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(
                            learned_libraries[library_name], f, indent=2, default=str
                        )
                    print(f"   ✅ Results saved to {filename}")
                except Exception as e:
                    print(f"   ❌ Error saving file: {e}")

        except Exception as e:
            print(f"❌ An error occurred while learning {library_name}: {e}")

    print("\n👋 Thanks for using the Interactive Library Learning System!")
    if learned_libraries:
        print(f"\n🎉 Session Summary:")
        print(
            f"Successfully learned {len(learned_libraries)} libraries: {list(learned_libraries.keys())}"
        )


if __name__ == "__main__":
    interactive_learning_session()
