import dspy
import os
from assistant.modules import DevAssistant
from data.trainset import get_trainset


def main():
    """
    Main function to configure DSPy, compile, and run the DevAssistant.
    """
    # --- 1. Configure DSPy ---
    # Set up the language model. Assumes OPENAI_API_KEY is set.
    # Replace with your preferred model.
    try:
        llm = dspy.OpenAI(model="gpt-4o-mini", max_tokens=4000)
        dspy.settings.configure(lm=llm)
        print("INFO: DSPy configured with OpenAI model.")
    except Exception as e:
        print(
            f"ERROR: Could not configure DSPy. Make sure your OPENAI_API_KEY is set. Details: {e}"
        )
        return

    # --- 2. Load Training Data ---
    trainset = get_trainset()
    print(f"INFO: Loaded {len(trainset)} training examples.")

    # --- 3. Compile the Assistant ---
    # The compiler will learn from the training examples to improve the assistant's reliability.
    compiler = dspy.BootstrapFewShot(metric=None)  # Using default metric for simplicity

    print("INFO: Compiling the DevAssistant... This may take a moment.")
    try:
        compiled_assistant = compiler.compile(DevAssistant(), trainset=trainset)
        print("INFO: Compilation complete.")
    except Exception as e:
        print(f"ERROR: Compilation failed. Details: {e}")
        return

    # --- 4. Run the Compiled Assistant ---
    print("\n--- Running Assistant ---")

    # This query is designed to trigger the correction learned from our training example.
    user_query = "Write a Python loop to iterate over a dictionary's items."

    final_code = compiled_assistant(user_query=user_query)

    print("\n--- Final Generated Code ---")
    print(final_code)
    print("--------------------------\n")


if __name__ == "__main__":
    main()
