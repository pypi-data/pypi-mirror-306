#! /bin/bash

# This script is used to build the release version of the project.
set -e
set -x

# Install build dependencies
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

# Build the project
python3 -m build

# Upload the project to PyPI (Make sure the TWINE_PASSWORD environment variable is set)
export TWINE_NON_INTERACTIVE=1
python3 -m twine upload dist/*
