# learn_library.py
# Purpose: Utility to learn any library from a set of documentation URLs using the agent

from main import agent  # Import the previously defined agent
from typing import Dict


def learn_library_from_urls(library_name: str, documentation_urls: list[str]) -> Dict:
    """Learn about any library from its documentation URLs."""

    try:
        library_info = agent.learn_from_urls(library_name, documentation_urls)

        print(f"\n🔍 Library Analysis Results for {library_name}:")
        print(f"Sources: {len(library_info['source_urls'])} successful fetches")
        print(f"Core Concepts: {library_info['core_concepts']}")
        print(f"Common Patterns: {library_info['patterns']}")
        print(f"Key Methods: {library_info['methods']}")
        print(f"Installation: {library_info['installation']}")
        print(f"Found {len(library_info['examples'])} code examples")

        return library_info

    except Exception as e:
        print(f"❌ Error learning library: {e}")
        raise


# Example 1: Learn FastAPI from official documentation
fastapi_urls = [
    "https://fastapi.tiangolo.com/",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "https://fastapi.tiangolo.com/tutorial/path-params/",
    "https://fastapi.tiangolo.com/tutorial/query-params/",
]

print("🚀 Learning FastAPI from official documentation...")
fastapi_info = learn_library_from_urls("FastAPI", fastapi_urls)

# Example 2: Learn a different library (you can replace with any library)
streamlit_urls = [
    "https://docs.streamlit.io/",
    "https://docs.streamlit.io/get-started",
    "https://docs.streamlit.io/develop/api-reference",
]

print("\n\n📊 Learning Streamlit from official documentation...")
streamlit_info = learn_library_from_urls("Streamlit", streamlit_urls)
