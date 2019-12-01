#!/bin/sh

docfile=doc/api-reference.md
exec venv/bin/python .helpers/pydoc-md.py fpga.project > $docfile

git add $docfile
git commit -m "Updated auto-generated documentation"
