#!/bin/bash

yosys -Q -p 'verilog_defaults -add -I../../hdl/headers1; verilog_defaults -add -I../../hdl/headers2; read_verilog -defer ../../hdl/blinking.v; synth_xilinx -top Blinking -family xc7; write_edif -pvector bra yosys.edif'
