#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

function msg () { tput setaf 6; echo "$1"; tput sgr0; }

msg "* Alternative 1: blinking.vhdl + top.v"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a blinking.vhdl
yosys -Q -m ghdl -p '
read_verilog top.v;
synth_ice40 -top Top -json blinking.json
'"

rm -fr *.cf *.edif *.json

msg "* Alternative 2: blinking.vhdl + top.v"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a blinking.vhdl
yosys -Q -m ghdl -p '
read_verilog top.v;
ghdl Top
'"

rm -fr *.cf *.edif

msg "* Alternative 3: blinking.vhdl + top.v"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
ghdl blinking.vhdl;
read_verilog top.v
'"

rm -fr *.cf *.edif

msg "* Alternative 4: blinking.vhdl + top.v"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
read_verilog top.v;
ghdl blinking.vhdl -e Top
'"

rm -fr *.cf *.edif

msg "* Alternative 5: blinking.v + top.vhdl"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
read_verilog blinking.v;
ghdl top.vhdl -e Top
'"

rm -fr *.cf *.edif
