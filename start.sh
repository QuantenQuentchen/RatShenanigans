#!/bin/bash


SCRIPT_DIR=$(dirname "$0")

git pull

echo "$SCRIPT_DIR"

python3.11 $SCRIPT_DIR/main.py