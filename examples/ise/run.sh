#!/bin/bash

set -e

BOARDS=("s6micro" "nexys3")
SOURCES=("vlog" "vhdl")

for BOARD in "${BOARDS[@]}"; do
  for SOURCE in "${SOURCES[@]}"; do
    echo "> $BOARD - $SOURCE"
    python3 run.py --board $BOARD --source $SOURCE
  done
done
