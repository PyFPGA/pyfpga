#!/bin/sh

set -e

for TEST in test/*.py; do
    echo "* Running $TEST"
    venv/bin/python3 $TEST
done

echo "The push can proceed"
