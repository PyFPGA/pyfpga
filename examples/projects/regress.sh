#!/bin/bash

set -e

declare -A TOOLS

TOOLS["diamond"]="brevia2"
TOOLS["ise"]="s6micro nexys3"
TOOLS["libero"]="maker"
TOOLS["openflow"]="icestick edu-ciaa orangecrab ecp5evn"
TOOLS["quartus"]="de10nano"
TOOLS["vivado"]="zybo arty"

SOURCES=("vlog" "vhdl" "slog")

SPECIFIED_TOOL=$1

for TOOL in "${!TOOLS[@]}"; do
  if [[ -n "$SPECIFIED_TOOL" && "$TOOL" != "$SPECIFIED_TOOL" ]]; then
    continue
  fi
  BOARDS=${TOOLS[$TOOL]}
  for BOARD in $BOARDS; do
    for SOURCE in "${SOURCES[@]}"; do
      if [[ "$TOOL" == "ise" && "$SOURCE" == "slog" ]]; then
        continue
      fi
      if [[ "$TOOL" == "openflow" && "$SOURCE" == "vhdl" ]]; then
        continue
      fi
      echo "> $TOOL - $BOARD - $SOURCE"
      python3 $TOOL.py --board $BOARD --source $SOURCE
    done
  done
done
