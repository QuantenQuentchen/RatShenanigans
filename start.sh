#!/bin/bash


SCRIPT_DIR=$(cd $(dirname $0))

git pull

python3.11 $SCRIPT_DIR/main.py