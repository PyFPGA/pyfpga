#!/bin/sh

docfile=doc/api-reference.md
venv/bin/python .helpers/pydoc-md.py fpga.project > $docfile

git add doc
git commit -m "Updated auto-generated documentation"
