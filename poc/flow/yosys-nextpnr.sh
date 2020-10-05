#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

#
# Yosys + nextpnr + IceStorm
#

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

#
# Yosys + nextpnr + Trellis
#

$DOCKER ghdl/synth:beta yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_ecp5 -top Blinking -json blinking.json
'

$DOCKER ghdl/synth:nextpnr-ecp5 nextpnr-ecp5 --json blinking.json --25k --package CSFBGA285 --lpf ../../examples/yosys-nextpnr/orangecrab_r0.2.lpf --textcfg blinking.config

$DOCKER ghdl/synth:trellis ecppack --svf blinking.svf blinking.config blinking.bit

# $DOCKER --device /dev/bus/usb ghdl/synth:prog openocd -f ${TRELLIS}/misc/openocd/ecp5-evn.cfg -c "transport select jtag; init; svf blinking.svf; exit"
# tinyprog -p aux.bit
