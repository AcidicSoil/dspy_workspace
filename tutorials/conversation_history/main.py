# Import necessary libraries and configure DSPy
import dspy


# Replace default LM configuration with local Ollama-compatible configuration
lm = dspy.LM(
    # "ollama_chat/acidic/Qwen3-Coder-IQ2_XXS:latest",
    # "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
    "ollama_chat/hf.co/mradermacher/Qwen3-Coder-42B-A3B-Instruct-TOTAL-RECALL-MASTER-CODER-M-1million-ctx-i1-GGUF:IQ2_XXS",
    # api_base="http://localhost:11434",  # Local Ollama server URL
    api_key="EMPTY",  # Usually empty for local Ollama; remove if you do not have a key
    streaming=False,
    response_format={},
)
dspy.configure(lm=lm)


# Define the signature for question answering with conversation history
class QA(dspy.Signature):
    question: str = dspy.InputField()
    history: dspy.History = dspy.InputField()
    answer: str = dspy.OutputField()

"""
# Create a prediction module and initialize empty history
predict = dspy.Predict(QA)
history = dspy.History(messages=[])

predict.demos.append(
    dspy.Example(
        question="What is the capital of France?",
        history=dspy.History(
            messages=[
                {
                    "question": "What is the capital of Germany?",
                    "answer": "The capital of Germany is Berlin.",
                }
            ]
        ),
        answer="The capital of France is Paris.",
    )
)

predict(question="What is the capital of America?", history=dspy.History(messages=[]))
"""

# Loop to accept user input and maintain conversation history
while True:
    question = input("Type your question, end conversation by typing 'finish': ")
    if question == "finish":
        break
    outputs = predict(question=question, history=history)
    print(f"\n{outputs.answer}\n")
    history.messages.append({"question": question, **outputs})

# Inspect the conversation history after interaction
dspy.inspect_history()
