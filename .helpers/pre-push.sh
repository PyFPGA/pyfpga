#!/bin/sh

venv/bin/python .helpers/pydoc-md.py fpga.project > doc/api-reference.md

git add doc
git commit -m "Updated auto-generated documentation"
