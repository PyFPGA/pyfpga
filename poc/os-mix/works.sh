#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

function msg () { tput setaf 6; echo "$1"; tput sgr0; }

msg "* Alternative 1: blinking.vhdl + top.v"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a blinking.vhdl
yosys -Q -m ghdl -p '
ghdl Blinking;
read_verilog top.v;
synth_ice40 -top Top -json blinking.json
'" > /dev/null

#rm -fr *.cf *.edif *.json

msg "* Alternative 2: blinking.v + top.vhdl"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
ghdl --std=08 top.vhdl -e ;
read_verilog blinking.v;
synth_ice40 -top Top -json blinking.json
'" > /dev/null

rm -fr *.cf *.edif *.json
