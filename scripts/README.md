# scripts – Purpose

## About
Helper shell scripts for managing local development environments and MLflow tracking.

## Contents
- `activate_env.sh` – activate the Python virtual environment for this workspace.
- `start_mlflow.sh` – launch an MLflow tracking server on port 5000.
- `push.sh` – convenience wrapper for committing and pushing changes.

## How to Use
Run the scripts directly from the repository root, e.g. `bash scripts/start_mlflow.sh` to start MLflow.

## Development Notes
Ensure executable permissions are preserved when modifying these files (`chmod +x`).

## Related Links
- [MLflow documentation](https://mlflow.org)

## Status/TODO
Scripts are minimal and may require adaptation for different environments.
