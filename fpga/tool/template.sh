#!/bin/bash
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
# This file implements an open-source flow based on ghdl, ghdl-yosys-plugin,
# yosys, nextpnr, icestorm and prjtrellis.
#

set -e

###############################################################################
# Things to tuneup
###############################################################################

FRONTEND={frontend}
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
CONSTRAINTS="{constraints}"

# taks = prj syn imp bit
TASKS="{tasks}"

OCI_RUN="{oci_run}"
OCI_GHDL={oci_syn_ghdl}
OCI_YOSYS={oci_syn_yosys}
OCI_IMP_ICE40={oci_imp_ice40}
OCI_IMP_ECP5={oci_imp_ecp5}
OCI_BIT_ICE40={oci_bit_ice40}
OCI_BIT_ECP5={oci_bit_ecp5}

###############################################################################
# Support
###############################################################################

MODULE=
[ -n "$VHDLS" ] && MODULE="-m ghdl"

function print () {{
    tput setaf 6; echo ">>> PyFPGA ($1): $2"; tput sgr0;
}}

###############################################################################
# Synthesis
###############################################################################

#######################################
# GHDL
#######################################

if [[ $TASKS == *"syn"* && $FRONTEND == "ghdl" ]]; then

print "ghdl" "running 'synthesis'"

$OCI_RUN $OCI_GHDL /bin/bash -c "
$VHDLS
ghdl --synth $FLAGS $TOP
" > $PROJECT.vhdl

fi

#######################################
# Yosys (with ghdl-yosys-plugin)
#######################################

if [[ $TASKS == *"syn"* && $FRONTEND == "yosys" ]]; then

print "yosys" "running 'synthesis'"

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

$OCI_RUN $OCI_YOSYS /bin/bash -c "
$VHDLS
yosys -Q $MODULE -p '
$INCLUDES;
$VERILOGS;
$PARAMS;
$SYNTH;
$WRITE
'"

fi

###############################################################################
# Place and Route
###############################################################################

if [[ $TASKS == *"imp"* ]]; then

print "nextpnr-$FAMILY" "running 'implementation'"

INPUT="--json $PROJECT.json"
if [[ $FAMILY == "ice40" ]]; then
    CONSTRAINT="--pcf $CONSTRAINTS"
    OUTPUT="--asc $PROJECT.asc"
    $OCI_RUN $OCI_IMP_ICE40 \
        nextpnr-ice40 --$DEVICE --package $PACKAGE $CONSTRAINT $INPUT $OUTPUT
    $OCI_RUN $OCI_BIT_ICE40 \
        icetime -d $DEVICE -mtr $PROJECT.rpt $PROJECT.asc
else
    CONSTRAINT="--lpf $CONSTRAINTS"
    OUTPUT="--textcfg $PROJECT.config"
    $OCI_RUN $OCI_IMP_ECP5 \
        nextpnr-ecp5 --$DEVICE --package $PACKAGE $CONSTRAINT $INPUT $OUTPUT
fi

fi

###############################################################################
# Bitstream generation
###############################################################################

if [[ $TASKS == *"bit"* ]]; then

if [[ $FAMILY == "ice40" ]]; then
    print "icepack" "running 'bitstream generation'"
    $OCI_RUN $OCI_BIT_ICE40 icepack $PROJECT.asc $PROJECT.bit
else
    print "eccpack" "running 'bitstream generation'"
    $OCI_RUN $OCI_BIT_ECP5 \
      ecppack --svf $PROJECT.svf $PROJECT.config $PROJECT.bit
fi

fi
