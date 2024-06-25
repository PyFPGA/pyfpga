#!/bin/bash

set -e

BOARDS=("zybo" "arty")
SOURCES=("vlog" "vhdl" "slog")
ACTIONS=("make" "prog" "all")

for BOARD in "${BOARDS[@]}"; do
  for SOURCE in "${SOURCES[@]}"; do
    for ACTION in "${ACTIONS[@]}"; do
      echo "> $BOARD - $SOURCE - $ACTION"
      python3 run.py --board $BOARD --source $SOURCE --action $ACTION
    done
  done
done
