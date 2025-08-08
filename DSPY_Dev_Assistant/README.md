# **DSPy Dev Assistant**

This project is a powerful, self-correcting developer tool built with the DSPy framework. It can generate, explain, and fix code while fact-checking its own output against documentation to ensure accuracy and reliability.

This codebase is a result of a collaborative design session, structuring various advanced DSPy features into a cohesive application.

## **Features**

* **Retrieval-Augmented Generation (RAG)**: The assistant can retrieve information from a knowledge base (like documentation) to answer questions and generate code.
* **Modular Architecture**: Built with composable dspy.Module classes, making it easy to extend and maintain.
* **Self-Correction & Verification**: Includes a custom VerificationModule that fact-checks generated code against documentation and corrects it if necessary.
* **Optimized with Compilation**: Uses DSPy's compilation (BootstrapFewShot) to learn from examples and improve its reliability, reducing hallucinations.

```
## **Project Structure**

dspy\_dev\_assistant/
│
├── main.py                 \# Main script to run the assistant
├── requirements.txt        \# Project dependencies
├── README.md               \# This file
│
├── assistant/
│   ├── \_\_init\_\_.py
│   ├── modules.py            \# All dspy.Module classes
│   └── signatures.py         \# All dspy.Signature classes
│
└── data/
    └── trainset.py           \# Training examples for compilation
```

## **How to Run**

1. **Install Dependencies:**
   pip install \-r requirements.txt

2. Configure Your Environment:
   Set your OPENAI\_API\_KEY environment variable. This project is configured to use an OpenAI model, but you can easily swap it out for any model supported by DSPy.
3. **Run the Assistant:**
   python main.py

   The main.py script will initialize the assistant, compile it with the training data, and run a sample query to demonstrate its capabilities.
