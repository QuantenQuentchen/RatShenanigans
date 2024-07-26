#!/bin/bash


SCRIPT_DIR=$(dirname "$0")


rm -rf $SCRIPT_DIR/data/

git pull

python3.11 $SCRIPT_DIR/main.py