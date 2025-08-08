import dspy
from signatures import CodeGenerator, VerificationSignature


class VerificationModule(dspy.Module):
    """A module to verify and correct generated code."""

    def __init__(self):
        super().__init__()
        # In a real application, you would configure this retriever
        # to point to your documentation (e.g., a Weaviate instance, a local FAISS index).
        # For this example, we'll use the default ColBERTv2 retriever.
        self.retriever = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
        self.verifier = dspy.Predict(VerificationSignature)

    def forward(self, question, generated_answer):
        """
        Verifies the generated_answer.

        Args:
            question (str): The original user query.
            generated_answer (str): The code or answer to be verified.

        Returns:
            dspy.Prediction: A prediction object with 'verdict' and 'corrected_answer'.
        """
        # 1. Retrieve context from documentation based on the original question.
        context = self.retriever(question, k=1).passages[0]

        # 2. Run the verification signature.
        result = self.verifier(
            context=context, question=question, generated_answer=generated_answer
        )

        return result


class DevAssistant(dspy.Module):
    """The main module for our self-correcting developer assistant."""

    def __init__(self):
        super().__init__()
        # The primary module for generating code.
        self.generate_code = dspy.Predict(CodeGenerator)

        # Our custom module for fact-checking and correcting the output.
        self.verifier = VerificationModule()

    def forward(self, user_query, task="generate"):
        """
        The main logic loop for the assistant.

        Args:
            user_query (str): The user's input prompt.
            task (str, optional): The task to perform. Defaults to "generate".

        Returns:
            str: The final, verified code or answer.
        """
        if task == "generate":
            # Step 1: Generate the initial code.
            print(f"INFO: Generating code for query: '{user_query}'")
            generated_output = self.generate_code(description=user_query)

            # Step 2: Verify the generated code against documentation.
            print("INFO: Verifying generated code...")
            verification_result = self.verifier(
                question=user_query, generated_answer=generated_output.code
            )

            # Step 3: Decide what to return based on the verdict.
            if "incorrect" in verification_result.verdict.lower():
                # If the code was wrong, log it and return the corrected version.
                print(
                    "INFO: Initial generation was incorrect. Returning verified version."
                )
                # You could add logging here to track incorrect verdicts.
                return verification_result.corrected_answer
            else:
                # If the code was correct, return the original.
                print("INFO: Generation was correct.")
                return generated_output.code

        # You can add more tasks like "fix_bug" or "explain_code" here.
        else:
            raise ValueError(f"Unknown task: {task}")
