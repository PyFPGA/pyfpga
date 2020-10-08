#!/bin/bash
#
# PyFPGA Master Bash Script for the open-source flow
#
# Copyright (C) 2020 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Supported TOOLs: ghdl, ghdl-yosys-plugin, yosys, nextpnr, icestrom, trellis
#

###############################################################################
# Things to tuneup
###############################################################################

TOOL={tool}
BACKEND={backend}
PROJECT={project}
FAMILY={family}
DEVICE={device}
PACKAGE={package}
TOP={top}

PARAMS="{params}"
FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"
VHDLS="{vhdls}"
INCLUDES="{includes}"
VERILOGS="{verilogs}"

# taks = prj syn imp bit
TASKS="{tasks}"

###############################################################################
# Support
###############################################################################

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

MODULE=
[ -n "$VHDLS" ] && MODULE="-m ghdl"

###############################################################################
# Synthesis
###############################################################################

#######################################
# GHDL
#######################################

if [[ $TASKS == *"syn"* && $TOOL == "ghdl" ]]; then

$DOCKER ghdl/synth:beta /bin/bash -c "
$VHDLS
ghdl --synth $FLAGS $TOP
" > $PROJECT.vhdl

fi

#######################################
# Yosys (with ghdl-yosys-plugin)
#######################################

if [[ $TASKS == *"syn"* && $TOOL == "yosys" ]]; then

SYNTH=
WRITE=
if [[ $BACKEND == "vivado" ]]; then
    SYNTH="synth_xilinx -top $TOP -family $FAMILY"
    WRITE="write_edif -pvector bra $PROJECT.edif"
elif [[ $BACKEND == "ise" ]]; then
    SYNTH="synth_xilinx -top $TOP -family $FAMILY -ise"
    WRITE="write_edif -pvector bra $PROJECT.edif"
elif [[ $BACKEND == "nextpnr" ]]; then
    SYNTH="synth_$FAMILY -top $TOP -json $PROJECT.json"
elif [[ $BACKEND == "verilog-nosynth" ]]; then
    WRITE="write_verilog $PROJECT.v"
else
    SYNTH="synth -top $TOP"
    WRITE="write_verilog $PROJECT.v"
fi

$DOCKER ghdl/synth:beta /bin/bash -c "
$VHDLS
yosys -Q $MODULE -p '
$INCLUDES;
$VERILOGS;
$PARAMS;
$SYNTH;
$WRITE
'"

fi
