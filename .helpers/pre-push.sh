#!/bin/sh

exec venv/bin/python .helpers/pydoc-md.py fpga.project > doc/api-reference.md

git add docs/
git commit -m "Updated auto-generated documentation"
