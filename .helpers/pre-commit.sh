#!/bin/sh

verify() {
    if [ $? -ne 0 ]; then
        echo "Fix the errors to proceed the commit."
        exit 1
    fi
}

echo "Validating PEP8 compliance ..."
venv/bin/pycodestyle fpga/ examples/ test/
verify

echo "Running PyLint ..."
venv/bin/pylint -j 0 --score no fpga -d R0913
verify

echo "Updating documentation ..."
venv/bin/python .helpers/pydoc-md.py fpga.project > doc/api-reference.md
verify
git add doc

echo "Checking trailing whitespaces ..."
git diff --check --cached
verify

echo "The commit can proceed"
