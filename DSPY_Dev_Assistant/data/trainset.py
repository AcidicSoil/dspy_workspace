import dspy


def get_trainset():
    """Returns a list of training examples for compiling the DevAssistant."""

    # Example 1: Teaches the verifier to correct outdated Python 2 syntax.
    train_example_1 = dspy.Example(
        question="Write a Python loop to iterate over a dictionary's items.",
        generated_answer="""
for key, value in my_dict.iteritems():
    print(f"{key}: {value}")
""",
        context="In Python 3, the `iteritems()` method was removed. You should use the `items()` method instead, which returns a view object displaying a list of a given dictionary's key-value tuple pairs.",
        verdict="Incorrect",
        corrected_answer="""
for key, value in my_dict.items():
    print(f"{key}: {value}")
""",
    ).with_inputs("question", "generated_answer", "context")

    # Example 2: Teaches the verifier to confirm a correct, modern answer.
    train_example_2 = dspy.Example(
        question="How do I open a file in Python?",
        generated_answer="""
with open('my_file.txt', 'r') as f:
    content = f.read()
""",
        context="The recommended way to open a file in Python is using the `with` statement. This ensures the file is automatically closed even if errors occur.",
        verdict="Correct",
        corrected_answer="""
with open('my_file.txt', 'r') as f:
    content = f.read()
""",
    ).with_inputs("question", "generated_answer", "context")

    # In a real project, you would add many more diverse examples.
    return [train_example_1, train_example_2]
