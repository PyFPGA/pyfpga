#!/bin/bash

set -e

BOARDS=("icestick" "edu-ciaa" "orangecrab" "ecp5evn")
SOURCES=("vlog" "vhdl" "slog")

for BOARD in "${BOARDS[@]}"; do
  for SOURCE in "${SOURCES[@]}"; do
    echo "> $BOARD - $SOURCE"
    python3 run.py --board $BOARD --source $SOURCE
  done
done
