#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR=$(dirname "$0")

# Change to the script directory (optional but recommended)
cd "$SCRIPT_DIR" || exit

# Discard any local changes
git reset --hard

# Fetch the latest changes from the remote repository
git fetch origin

# Reset the local main branch to match the remote main branch
git reset --hard origin/main

# Run the Python script
python3.11 "$SCRIPT_DIR/main.py"
