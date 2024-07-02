#!/bin/bash

set -e

declare -A TOOLS

TOOLS["ise"]="s6micro nexys3"
TOOLS["libero"]="maker-board"
TOOLS["openflow"]="icestick edu-ciaa orangecrab ecp5evn"
TOOLS["quartus"]="de10nano"
TOOLS["vivado"]="zybo arty"

SOURCES=("vlog" "vhdl" "slog")

for TOOL in "${!TOOLS[@]}"; do
  BOARDS=${TOOLS[$TOOL]}
  for BOARD in $BOARDS; do
    for SOURCE in "${SOURCES[@]}"; do
      if [[ "$TOOL" == "ise" && "$SOURCE" == "slog" ]]; then
        continue
      fi
      if [[ "$TOOL" == "openflow" && "$SOURCE" != "vlog" ]]; then
        continue
      fi
      echo "> $TOOL - $BOARD - $SOURCE"
      python3 $TOOL.py --board $BOARD --source $SOURCE
    done
  done
done
