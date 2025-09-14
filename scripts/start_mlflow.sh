#!/bin/bash

# Idempotent MLflow local server startup script
# Assumes script is in scripts/ directory under project root

set -e

MLFLOW_DB="mlflow.db"
ARTIFACT_DIR="mlruns"
MLFLOW_PORT=5000

# Resolve project root directory (parent of this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Project root resolved to: $PROJECT_ROOT"

# Paths resolved relative to project root
MLFLOW_DB_PATH="$PROJECT_ROOT/$MLFLOW_DB"
ARTIFACT_DIR_PATH="$PROJECT_ROOT/$ARTIFACT_DIR"

# Create artifact directory if it doesn't exist
if [ ! -d "$ARTIFACT_DIR_PATH" ]; then
  echo "Creating artifact directory: $ARTIFACT_DIR_PATH"
  mkdir -p "$ARTIFACT_DIR_PATH"
else
  echo "Artifact directory '$ARTIFACT_DIR_PATH' already exists."
fi

# Create empty SQLite DB file if not exists (optional)
if [ ! -f "$MLFLOW_DB_PATH" ]; then
  echo "Creating empty MLflow backend DB file: $MLFLOW_DB_PATH"
  touch "$MLFLOW_DB_PATH"
else
  echo "MLflow backend DB '$MLFLOW_DB_PATH' already exists."
fi

# Check if MLflow server is already running on port $MLFLOW_PORT
if lsof -i tcp:$MLFLOW_PORT >/dev/null 2>&1; then
  echo "MLflow server already running on port $MLFLOW_PORT. Skipping server start."
else
  echo "Starting MLflow server on port $MLFLOW_PORT..."

  # Run mlflow server in background
  mlflow server \
    --backend-store-uri sqlite:///$MLFLOW_DB_PATH \
    --default-artifact-root "$ARTIFACT_DIR_PATH" \
    --host 0.0.0.0 \
    --port $MLFLOW_PORT &

  echo "MLflow server started."
fi
