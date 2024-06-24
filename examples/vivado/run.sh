#!/bin/bash

ACTIONS=("make" "prog" "all")
SOURCES=("vlog" "vhdl" "slog" "design")

for ACTION in "${ACTIONS[@]}"; do
  for SOURCE in "${SOURCES[@]}"; do
    python3 run.py --action $ACTION --source $SOURCE
  done
done
