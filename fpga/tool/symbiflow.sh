#!/bin/bash
#
# Copyright (C) 2021 Rodrigo A. Melo
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
# Description: bash script to performs synthesis, implementation and bitstream
# generation, using SymbiFlow.
#

set -e

###############################################################################
# Things to tuneup
###############################################################################

PROJECT={project}
PART={part}
FAMILY={family}
DEVICE={device}
TOP={top}

XDC="{xdc}"
SDC="{sdc}"
PCF="{pcf}"

VERILOGS="{verilogs}"

# taks = prj syn imp bit
TASKS="{tasks}"

###############################################################################
# Support
###############################################################################

function print () {{
    tput setaf 6; echo ">>> PyFPGA ($1): $2"; tput sgr0;
}}

###############################################################################
# Pre-processing Constraints
###############################################################################

XDC_OPT=
SDC_OPT=
PCF_OPT=

if [[ ! -z $XDC ]]; then
    cat $XDC > pyfpga.xdc
    XDC_OPT="-x pyfpga.xdc"
fi

if [[ ! -z $SDC ]]; then
    cat $SDC > pyfpga.sdc
    SDC_OPT="-s pyfpga.sdc"
fi

if [[ ! -z $PCF ]]; then
    cat $PCF > pyfpga.pcf
    PCF_OPT="-p pyfpga.pcf"
fi

###############################################################################
# Synthesis
###############################################################################

if [[ $TASKS == *"syn"* ]]; then

print "running 'synthesis'"

symbiflow_synth -t $TOP -v $VERILOGS -d $FAMILY -p $PART $XDC_OPT

fi

###############################################################################
# Place and Route
###############################################################################

if [[ $TASKS == *"imp"* ]]; then

print "running 'implementation'"

symbiflow_pack -e $TOP.eblif -d $DEVICE $SDC_OPT
symbiflow_place -e $TOP.eblif -d $DEVICE $PCF_OPT -n $TOP.net -P $PART $SDC_OPT
symbiflow_route -e $TOP.eblif -d $DEVICE $SDC_OPT

fi

###############################################################################
# Bitstream generation
###############################################################################

if [[ $TASKS == *"bit"* ]]; then

print "running 'bitstream generation'"

symbiflow_write_fasm -e $TOP.eblif -d $DEVICE
symbiflow_write_bitstream -d $FAMILY -f $TOP.fasm -p $PART -b $PROJECT.bit

fi
