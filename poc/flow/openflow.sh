#!/bin/bash

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

###############################################################################

echo "* VHDL with GHDL --synth"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
ghdl --synth $FLAGS Top
" > /dev/null

rm -fr *.cf

#################################################################################

echo "* Verilog with Yosys"

$DOCKER ghdl/synth:beta yosys -Q -p '
verilog_defaults -add -I../../hdl/headers1;
verilog_defaults -add -I../../hdl/headers2;
read_verilog -defer ../../hdl/blinking.v;
synth_xilinx -top Blinking -family xc7;
write_edif -pvector bra yosys.edif
' > /dev/null

rm -fr *.edif

#################################################################################

echo "* VHDL with GHDL + ghdl-yosys-plugin + Yosys"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
yosys -Q -m ghdl -p '
ghdl $FLAGS Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.cf *.edif

#################################################################################

echo "* VHDL with ghdl-yosys-plugin + Yosys"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
ghdl $FLAGS --work=examples ../../hdl/blinking.vhdl ../../hdl/examples_pkg.vhdl ../../hdl/top.vhdl -e Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.edif

##################################################################################

echo "* VHDL with GHDL + ghdl-yosys-plugin and Verilog with Yosys"

echo "  * Alternative 1"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
yosys -Q -m ghdl -p '
read_verilog -defer ../../hdl/top.v;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.cf *.edif

echo "  * Alternative 2"

$DOCKER ghdl/synth:beta /bin/bash -c "
ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
yosys -Q -m ghdl -p '
read_verilog -defer ../../hdl/top.v;
ghdl Top;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.cf *.edif

##################################################################################

echo "* VHDL with ghdl-yosys-plugin and Verilog with Yosys"

echo "  * Alternative 1"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
ghdl $FLAGS ../../hdl/blinking.vhdl;
read_verilog -defer ../../hdl/top.v;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.cf *.edif

echo "  * Alternative 2"

$DOCKER ghdl/synth:beta /bin/bash -c "
yosys -Q -m ghdl -p '
read_verilog -defer ../../hdl/top.v;
ghdl $FLAGS ../../hdl/blinking.vhdl -e Top;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
'" > /dev/null

rm -fr *.cf *.edif
