#!/bin/sh

set -e

echo "Validating PEP8 compliance ..."
venv/bin/pycodestyle fpga/ examples/ test/

echo "Running PyLint ..."
venv/bin/pylint fpga

echo "Checking trailing whitespaces ..."
git diff --check --cached

echo "The commit can proceed"
