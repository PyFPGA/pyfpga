#!/bin/sh

exec venv/bin/pycodestyle fpga examples test
exec venv/bin/pylint fpga

# Check of trailing whitespaces
exec git diff --check --cached
