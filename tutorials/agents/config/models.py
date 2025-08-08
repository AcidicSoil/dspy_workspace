import dspy


def setup_models():
    """
    Initializes and configures the language models for the project.
    """
    # Student model - a small, fast model to be optimized
    llama3b = dspy.LM(
        "ollama_chat/hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:latest",
        api_base="http://localhost:11434",  # Local Ollama server URL
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

    # Teacher model - a larger, more capable model for generating demonstrations
    qwen3coder = dspy.LM(
        "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
        api_base="http://localhost:11434",  # Local Ollama server URL
        api_key="",
        streaming=False,
        temperature=0.7,
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

    # Configure the default language model for dspy
    dspy.configure(lm=llama3b)

    #Return a dictionary of models for easy access
    return {"student": llama3b, "teacher": qwen3coder}