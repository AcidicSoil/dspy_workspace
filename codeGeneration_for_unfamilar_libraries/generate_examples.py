# generate_examples.py
# Purpose: Generate code examples for any learned library

from learn_library import fastapi_info, streamlit_info, agent


def generate_examples_for_library(library_info: dict, library_name: str):
    """Generate code examples for any library based on its documentation."""

    # Define generic use cases that can apply to most libraries
    use_cases = [
        {
            "name": "Basic Setup and Hello World",
            "description": f"Create a minimal working example with {library_name}",
            "requirements": "Include installation, imports, and basic usage",
        },
        {
            "name": "Common Operations",
            "description": f"Demonstrate the most common {library_name} operations",
            "requirements": "Show typical workflow and best practices",
        },
        {
            "name": "Advanced Usage",
            "description": f"Create a more complex example showcasing {library_name} capabilities",
            "requirements": "Include error handling and optimization",
        },
    ]

    generated_examples = []

    print(f"\n🔧 Generating examples for {library_name}...")

    for use_case in use_cases:
        print(f"\n📝 {use_case['name']}")
        print(f"Description: {use_case['description']}")

        example = agent.generate_example(
            library_info=library_info,
            use_case=use_case["description"],
            requirements=use_case["requirements"],
        )

        print("\n💻 Generated Code:")
        print("```python")
        print(example["code"])
        print("```")

        print("\n📦 Required Imports:")
        for imp in example["imports"]:
            print(f"  • {imp}")

        print("\n📝 Explanation:")
        print(example["explanation"])

        print("\n✅ Best Practices:")
        for practice in example["best_practices"]:
            print(f"  • {practice}")

        generated_examples.append(
            {
                "use_case": use_case["name"],
                "code": example["code"],
                "imports": example["imports"],
                "explanation": example["explanation"],
                "best_practices": example["best_practices"],
            }
        )

        print("-" * 80)

    return generated_examples


# Generate examples for both libraries
print("🎯 Generating FastAPI Examples:")
fastapi_examples = generate_examples_for_library(fastapi_info, "FastAPI")

print("\n\n🎯 Generating Streamlit Examples:")
streamlit_examples = generate_examples_for_library(streamlit_info, "Streamlit")
