import dspy
from config.models import setup_models
from data.hover_loader import load_hover_data
from agent.react_agent import create_react_agent
from evaluation.metrics import top5_recall
import mlflow

# --- Optional: MLflow Setup ---
# To enable MLflow, start the server (`mlflow server`) and uncomment the following lines.
# This will automatically log traces and allow for model versioning.
# -----------------------------------
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("DSPy")
mlflow.dspy.autolog()
# MLFLOW_ENABLED = True
# -----------------------------------
MLFLOW_ENABLED = True  # Set to True after uncommenting the lines above


def main():
    """
    Main training script to optimize the ReAct agent.
    """
    print("--- Starting Agent Optimization ---")

    # 1. Setup Models and Data
    models = setup_models()
    try:
        teacher_model = dspy.LM(
            model="ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
            max_tokens=4000,
        )
    except ImportError:
        print("Warning: Qwen3 config failed. Using student model as teacher.")
        print("Optimization quality will be significantly lower.")
        teacher_model = models.get("student")

    # 2. Load Data
    trainset, _, _ = load_hover_data(train_size=100, dev_size=0, test_size=0)

    # 3. Create Agent
    react_agent = create_react_agent()

    # 4. Configure Optimizer (MIPROv2)
    # This optimizer uses a teacher model to generate high-quality demonstrations
    # and fine-tunes the prompts of the student model.
    optimizer_kwargs = dict(
        teacher_settings=dict(lm=teacher_model),
        prompt_model=teacher_model,
        max_errors=5,  # Setting a lower max_errors to avoid long hangs on difficult examples
    )

    optimizer = dspy.MIPROv2(
        metric=top5_recall,
        auto="medium",  # Automatically selects a moderate number of candidates
        num_threads=8,  # Adjust based on your machine's capability
        **optimizer_kwargs,
    )

    # Wrap compilation in an MLflow run
    with (
        mlflow.start_run(run_name="agent_optimization")
        if MLFLOW_ENABLED
        else dspy.util.null_context()
    ):
        print("Compiling the agent with MIPROv2... This may take a while.")
        optimized_agent = optimizer.compile(
            react_agent,
            trainset=trainset,
            max_bootstrapped_demos=3,
            max_labeled_demos=0,
        )

        # Save the Optimized Agent
        if MLFLOW_ENABLED:
            print("Logging optimized agent to MLflow...")
            mlflow.dspy.log_model(
                optimized_agent, artifact_path="optimized_agent_model"
            )
            mlflow.log_params({"optimizer": "MIPROv2", "demos": 3})
        else:
            save_path = "optimized_react.json"
            optimized_agent.save(save_path)
            print(f"--- Optimization complete. Agent saved to {save_path} ---")

    # 6. Save the Optimized Agent
    save_path = "optimized_react.json"
    optimized_agent.save(save_path)
    print(f"--- Optimization complete. Optimized agent saved to {save_path} ---")


if __name__ == "__main__":
    main()
