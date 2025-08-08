#!/bin/bash
set -e

# Define the workspace path relative to home
WORKSPACE_PATH="$HOME/projects/dspy_workspace"

# Get current directory
CURRENT_DIR="$(pwd)"

# Check if we are already inside dspy_workspace or any of its subdirectories
if [[ "$CURRENT_DIR" == "$WORKSPACE_PATH"* ]]; then
  # Already inside dspy_workspace, activate directly
  source .venv/bin/activate
else
  # Not inside dspy_workspace, change directory and activate
  cd "$WORKSPACE_PATH"
  source .venv/bin/activate
fi
