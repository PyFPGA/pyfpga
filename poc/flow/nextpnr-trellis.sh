#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

$DOCKER ghdl/synth:beta yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_ecp5 -top Blinking -json blinking.json
'

$DOCKER ghdl/synth:nextpnr-ecp5 nextpnr-ecp5 --json blinking.json --25k --package CSFBGA285 --lpf ../../examples/yosys-nextpnr/orangecrab_r0.2.pcf --textcfg blinking.config

$DOCKER ghdl/synth:trellis ecppack --svf blinking.svf blinking.config blinking.bit

# $DOCKER --device /dev/bus/usb ghdl/synth:prog openocd -f ${TRELLIS}/misc/openocd/ecp5-evn.cfg -c "transport select jtag; init; svf $<; exit"
