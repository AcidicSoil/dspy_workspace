# DSPy ReAct Agent for Multi-Hop Search

This project demonstrates how to build, optimize, and evaluate a `dspy.ReAct` agent for a complex multi-hop question-answering task using the HoVer dataset. It is structured into separate modules for configuration, data loading, tools, agent definition, training, and evaluation.

## ⚙️ Setup

1. **Clone the repository**:

    ```bash
    git clone <your-repo-url>
    cd dspy-agent-project
    ```

2. **Install dependencies**:
    Make sure you have Python 3.9+ installed.

    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

The project is split into two main scripts:

1. **`train.py`**: This script uses the `MIPROv2` optimizer to fine-tune the prompts of the ReAct agent. It requires a powerful "teacher" model (like GPT-4o) to generate high-quality examples for the smaller "student" model.

    ```bash
    python train.py
    ```

    This process can be lengthy and will produce an `optimized_react.json` file containing the optimized program, or save it as an MLflow model if configured.

2. **`main.py`**: This script evaluates both the original, un-optimized agent and the optimized agent to compare their performance on the development set.

    ```bash
    # Run this after train.py has completed
    python main.py
    ```

---

## 📈 MLflow Integration (Recommended)

<a href="https://mlflow.org/">**MLflow**</a> is an LLMOps tool that natively integrates with DSPy to offer powerful experiment tracking and explainability. You can use it to visualize prompts, trace agent behavior, and log evaluation results.

### **Initial Setup**

1. **Install MLflow** (included in `requirements.txt`):

    ```bash
    pip install mlflow>=2.20
    ```

2. **Start the MLflow UI**:
    Run this command in a separate terminal. It will host the tracking server locally.

    ```bash
    mlflow ui --port 5000
    ```

3. **Enable in Scripts**:
    To connect your scripts to the MLflow server, uncomment the MLflow setup block at the top of `train.py` and `main.py`. This enables automatic logging of all DSPy module executions as traces.

    ```python
    # In train.py and main.py
    import mlflow

    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("DSPy Multi-Hop Agent")
    mlflow.dspy.autolog()
    ```

### **Tracking Training & Evaluation**

The scripts are already configured to log artifacts and results to MLflow:

* **`train.py`**: Wraps the optimization process in an MLflow run and uses `mlflow.dspy.log_model()` to save the optimized agent. This is superior to a local file save as it versions the agent and its environment for reproducibility.

* **`main.py`**: Wraps each evaluation in a distinct MLflow run, logging the final recall score and a detailed table of predictions vs. ground truth for each example.

To learn more about the integration, visit the [MLflow DSPy Documentation](https://mlflow.org/docs/latest/llms/dspy/index.html).
