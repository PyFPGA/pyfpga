#!/bin/sh

# Check of code
exec venv/bin/pycodestyle fpga examples test
exec venv/bin/pylint fpga

# Check of trailing whitespaces
exec git diff --check --cached

# Dod generation
venv/bin/python .helpers/pydoc-md.py fpga.project > doc/api-reference.md
git add doc
git commit -m "Updated auto-generated documentation"
