#!/bin/bash

# Idempotent MLflow local server startup script

set -e

MLFLOW_DB="mlflow.db"
ARTIFACT_DIR="mlruns"
MLFLOW_PORT=5000

# Create artifact directory if it doesn't exist
if [ ! -d "$ARTIFACT_DIR" ]; then
  echo "Creating artifact directory: $ARTIFACT_DIR"
  mkdir -p "$ARTIFACT_DIR"
else
  echo "Artifact directory '$ARTIFACT_DIR' already exists."
fi

# Create empty SQLite DB file if not exists (SQLite will create on demand, so optional)
if [ ! -f "$MLFLOW_DB" ]; then
  echo "Creating empty MLflow backend DB file: $MLFLOW_DB"
  touch "$MLFLOW_DB"
else
  echo "MLflow backend DB '$MLFLOW_DB' already exists."
fi

# Check if MLflow server is already running on port $MLFLOW_PORT
if lsof -i tcp:$MLFLOW_PORT >/dev/null 2>&1; then
  echo "MLflow server already running on port $MLFLOW_PORT. Skipping server start."
else
  echo "Starting MLflow server on port $MLFLOW_PORT..."

  # Run mlflow server in background (you can remove & if you want to keep in foreground)
  mlflow server \
    --backend-store-uri sqlite:///$PWD/$MLFLOW_DB \
    --default-artifact-root "$PWD/$ARTIFACT_DIR" \
    --host 0.0.0.0 \
    --port $MLFLOW_PORT &

  echo "MLflow server started."
fi
