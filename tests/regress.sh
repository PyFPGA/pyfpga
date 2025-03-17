#!/bin/bash

#
# Copyright (C) 2024-2025 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

set -e

declare -A TOOLS

TOOLS["diamond"]="brevia2"
TOOLS["ise"]="s6micro nexys3"
TOOLS["libero"]="maker"
TOOLS["openflow"]="icestick edu-ciaa orangecrab ecp5evn"
TOOLS["quartus"]="de10nano"
TOOLS["vivado"]="zybo arty"

SOURCES=("vlog" "vhdl" "slog")

SDIR=$PWD
TDIR=../examples/projects

SPECIFIED_TOOL=""
NOTOOL=false
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --tool)
      SPECIFIED_TOOL="$2"
      shift 2
      ;;
    *)
      echo "Invalid option: $1"
      exit 1
      ;;
  esac
done

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
      echo "> $TOOL - $BOARD - $SOURCE"
      cd $TDIR;
      python3 $TOOL.py --board $BOARD --source $SOURCE --action all;
      cd $SDIR;
    done
  done
done
