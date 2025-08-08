import dspy
from pydantic import BaseModel, Field

# --- Signatures for Core Generation Tasks ---


class CodeGenerator(dspy.Signature):
    """Generate Python code based on a detailed description."""

    description = dspy.InputField(
        desc="A detailed description of the desired code's functionality."
    )
    code = dspy.OutputField(desc="The generated Python code.")


class CodeQuestionAnswering(dspy.Signature):
    """Answer a question about the given code context."""

    context = dspy.InputField(desc="Relevant code snippets from the user's codebase.")
    question = dspy.InputField(desc="The user's question about the code.")
    answer = dspy.OutputField(desc="A detailed answer to the question.")


# --- Signature for the Verification Module ---


class VerificationSignature(dspy.Signature):
    """Verify a generated answer against the provided documentation context. If the answer is incorrect, correct it."""

    context = dspy.InputField(desc="Relevant documentation for fact-checking.")
    question = dspy.InputField(desc="The original user question or programming task.")
    generated_answer = dspy.InputField(
        desc="The answer produced by the assistant that needs to be checked."
    )

    verdict = dspy.OutputField(
        desc="A simple 'Correct' or 'Incorrect' verdict based on the context."
    )
    corrected_answer = dspy.OutputField(
        desc="The corrected answer. If the verdict is 'Correct', this should be the same as the generated_answer."
    )
