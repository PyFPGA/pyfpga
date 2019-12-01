#!/bin/sh

docfile=doc/api-reference.md
venv/bin/python .helpers/pydoc-md.py fpga.project > $docfile

exec git add $docfile
exec git commit -m "Updated auto-generated documentation"
