#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

function msg () { tput setaf 6; echo "$1"; tput sgr0; }

###############################################################################

msg "* VHDL with GHDL --synth"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
ghdl --synth $FLAGS Top
"

rm -fr *.cf

#################################################################################

msg "* Verilog with Yosys"

$DOCKER ghdl/synth:beta yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_xilinx -top Blinking -family xc7;
write_edif -pvector bra yosys.edif
'

rm -fr *.edif

#################################################################################

msg "* VHDL with GHDL + ghdl-yosys-plugin + Yosys"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
yosys -Q -m ghdl -p '
ghdl $FLAGS Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
'"

rm -fr *.cf *.edif

#################################################################################

msg "* VHDL with ghdl-yosys-plugin + Yosys"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
ghdl $FLAGS --work=examples ../../hdl/blinking.vhdl ../../hdl/examples_pkg.vhdl ../../hdl/top.vhdl -e Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
'"

rm -fr *.edif

##################################################################################

msg "* Yosys + nextpnr + IceStorm"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_ice40 -top Blinking -json blinking.json
'"

$DOCKER ghdl/synth:nextpnr-ice40  /bin/bash -c "
nextpnr-ice40 --json blinking.json --hx8k --package tq144:4k --pcf ../../examples/yosys-nextpnr/edu-ciaa-fpga.pcf --asc blinking.asc
"

$DOCKER ghdl/synth:icestorm /bin/bash -c "
icepack blinking.asc blinking.bit
icetime -d hx8k -mtr blinking.rpt blinking.asc
"

# $DOCKER --device /dev/bus/usb ghdl/synth:prog iceprog blinking.bit

rm -fr *.asc *.bit *.json *.rpt

##################################################################################

msg "* Yosys + nextpnr + Trellis"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_ecp5 -top Blinking -json blinking.json
'"

$DOCKER ghdl/synth:nextpnr-ecp5 /bin/bash -c "
nextpnr-ecp5 --json blinking.json --25k --package CSFBGA285 --lpf ../../examples/yosys-nextpnr/orangecrab_r0.2.lpf --textcfg blinking.config
"

$DOCKER ghdl/synth:trellis /bin/bash -c "
ecppack --svf blinking.svf blinking.config blinking.bit
"

rm -fr *.bit *.config *.json *.svf

# $DOCKER --device /dev/bus/usb ghdl/synth:prog openocd -f ${TRELLIS}/misc/openocd/ecp5-evn.cfg -c "transport select jtag; init; svf blinking.svf; exit"
# tinyprog -p aux.bit
