#!/bin/bash

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

###############################################################################

echo "GHDL analysis and Yosys synthesis of pure VHDL"

ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
yosys -Q -m ghdl -p '
ghdl '"$FLAGS"' Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
' > /dev/null || echo "ERROR: it failed, seems not supported."

# Clean-all
rm -fr *.cf *.edif

###############################################################################

echo "Yosys analysis and synthesis of pure VHDL"

yosys -Q -m ghdl -p '
ghdl '"$FLAGS"' --work=examples ../../hdl/blinking.vhdl ../../hdl/examples_pkg.vhdl ../../hdl/top.vhdl -e Top;
synth_xilinx -family xc7;
write_edif -pvector bra yosys.edif
' > /dev/null || echo "ERROR: it failed, seems not supported."

# Clean-all
rm -fr *.cf *.edif

###############################################################################

echo "GHDL analysis of VHDL and Yosys synthesis of Verilog (mix)"

ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl

yosys -Q -m ghdl -p '
read_verilog -defer ../../hdl/top.v;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
' > /dev/null || echo "ERROR: it failed, seems not supported."

# Clean-all
rm -fr *.cf *.edif

###############################################################################

echo " Yosys analysis and synthesis of VHDL and Verilog (mix)"

yosys -Q -m ghdl -p '
ghdl '"$FLAGS"' ../../hdl/blinking.vhdl;
read_verilog -defer ../../hdl/top.v;
synth_xilinx -top Top -family xc7;
write_edif -pvector bra yosys.edif
' > /dev/null || echo "ERROR: it failed, seems not supported."

# Clean-all
rm -fr *.cf *.edif
