#!/bin/sh

set -e

echo "Validating PEP8 compliance ..."
venv/bin/pycodestyle fpga/ examples/ test/

echo "Running PyLint ..."
venv/bin/pylint -j 0 --score no fpga -d too-many-arguments

echo "Updating documentation ..."
venv/bin/python .helpers/pydoc-md.py fpga.project > doc/api-reference.md
git add doc

echo "Checking trailing whitespaces ..."
git diff --check --cached

echo "The commit can proceed"
