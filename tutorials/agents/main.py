import dspy
from dspy.evaluate import Evaluate
from config.models import setup_models
from data.hover_loader import load_hover_data
from agent.react_agent import create_react_agent
from evaluation.metrics import top5_recall
import os
import mlflow

# --- Optional: MLflow Setup ---
# To enable MLflow, start the server (`mlflow ui`) and uncomment the following lines.
# This will automatically log traces and evaluation results.
# -----------------------------------
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("DSPy")
mlflow.dspy.autolog()
# MLFLOW_ENABLED = True
# -----------------------------------
MLFLOW_ENABLED = True  # Set to True after uncommenting the lines above


def safe_agent_call(agent, claim):
    """Wrapper to handle potential exceptions during agent execution."""
    try:
        return agent(claim=claim)
    except Exception as e:
        print(f"Error processing claim '{claim[:50]}...': {e}")
        return dspy.Prediction(titles=[])


def log_evaluation_results(evaluator, run_name):
    """Helper to log detailed evaluation results to MLflow."""
    if not MLFLOW_ENABLED:
        return

    # Log aggregated score
    mlflow.log_metric("avg_top5_recall", evaluator.average_score)

    # Log detailed results as a table
    results_table = {
        "claim": [r.inputs.claim for r in evaluator.results],
        "expected_titles": [r.gold.titles for r in evaluator.results],
        "predicted_titles": [r.pred.titles for r in evaluator.results],
        "recall_score": [r.score for r in evaluator.results],
        "correct": [r.correct for r in evaluator.results],
    }
    mlflow.log_table(data=results_table, artifact_file=f"{run_name}_results.json")

def main():
    """
    Main script to evaluate the ReAct agent before and after optimization.
    """
    print("--- Starting Agent Evaluation ---")

    # 1. Setup Models and Data
    setup_models()
    _, devset, _ = load_hover_data(train_size=0, dev_size=100, test_size=0)

    # 2. Setup Evaluator
    evaluator = Evaluate(
        devset=devset,
        metric=top5_recall,
        num_threads=16,
        display_progress=True,
        display_table=5,
    )

    # 3. Evaluate the un-optimized agent
    print("\n--- Evaluating base (un-optimized) agent ---")
    unoptimized_agent = create_react_agent()
    with (
        mlflow.start_run(run_name="unoptimized_agent_eval")
        if MLFLOW_ENABLED
        else dspy.util.null_context()
    ):
        evaluator(lambda example: safe_agent_call(unoptimized_agent, example.claim))
        log_evaluation_results(evaluator, "unoptimized")

    # 4. Evaluate the optimized agent
    save_path = "optimized_react.json"
    if os.path.exists(save_path) or MLFLOW_ENABLED:
        print("\n--- Evaluating optimized agent ---")
        optimized_agent = create_react_agent()
        # Load from MLflow if enabled, otherwise from local file
        if MLFLOW_ENABLED:
            try:
                # Find the latest run from the training experiment
                runs = mlflow.search_runs(
                    experiment_names=["DSPy"],
                    filter_string="tags.mlflow.runName = 'agent_optimization'",
                    order_by=["start_time DESC"],
                )
                if not runs.empty:
                    model_uri = f"runs:/{runs.iloc[0].run_id}/optimized_agent_model"
                    print(f"Loading optimized model from MLflow: {model_uri}")
                    optimized_agent = mlflow.dspy.load_model(model_uri)
                else:
                    raise FileNotFoundError("No training run found in MLflow.")
            except Exception as e:
                print(
                    f"Could not load model from MLflow ({e}), falling back to local file."
                )
                if os.path.exists(save_path):
                    optimized_agent.load(save_path)
                else:
                    print(
                        f"Local file '{save_path}' not found. Cannot evaluate optimized agent."
                    )
                    return
        elif os.path.exists(save_path):
            print(f"Loading optimized agent from local file: {save_path}")
            optimized_agent.load(save_path)

        with (
            mlflow.start_run(run_name="optimized_agent_eval")
            if MLFLOW_ENABLED
            else dspy.util.null_context()
        ):
            evaluator(lambda example: safe_agent_call(optimized_agent, example.claim))
            log_evaluation_results(evaluator, "optimized")
    else:
        print("Optimized agent file not found. Please run 'python train.py' first.")


if __name__ == "__main__":
    main()
