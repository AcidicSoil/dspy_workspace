#!/bin/bash

# Exit on any error
set -e

# Optional: Ask for commit message if not passed as argument
if [ -z "$1" ]; then
  echo "Usage: ./git-push.sh \"your commit message\""
  exit 1
fi

COMMIT_MSG="$1"

# Add all changes
git add .

# Commit
git commit -m "$COMMIT_MSG"

# Push to origin (default branch is 'main', change if using something else)
git push origin main
