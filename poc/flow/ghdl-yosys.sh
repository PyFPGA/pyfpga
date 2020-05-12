#!/bin/bash

yosys -m ghdl -p 'ghdl -fsynopsys -fexplicit -frelaxed --std=08 ../../hdl/blinking.vhdl -e blinking; synth_xilinx -family xc7; write_edif -pvector bra yosys.edif'
