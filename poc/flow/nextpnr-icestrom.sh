#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

$DOCKER ghdl/synth:beta yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_ice40 -top Blinking -json blinking.json
'

$DOCKER ghdl/synth:nextpnr-ice40 nextpnr-ice40 --json blinking.json --hx8k --package tq144:4k --pcf ../../examples/yosys-nextpnr/edu-ciaa-fpga.pcf --asc blinking.asc

$DOCKER ghdl/synth:icestorm icepack blinking.asc blinking.bit
$DOCKER ghdl/synth:icestorm icetime -d hx8k -mtr blinking.rpt blinking.asc

# $DOCKER --device /dev/bus/usb ghdl/synth:prog iceprog blinking.bit
