#!/bin/sh

verify() {
    if [ $? -ne 0 ]; then
        echo "Fix the errors to proceed the push."
        exit 1
    fi
}

for TEST in test/*.py; do
    echo "* Running $TEST"
    venv/bin/python3 $TEST
    verify
done

echo "The push can proceed"
