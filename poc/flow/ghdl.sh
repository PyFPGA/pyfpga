#!/bin/bash

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

ghdl -a $FLAGS --work=examples ../../hdl/blinking.vhdl
ghdl -a $FLAGS --work=examples ../../hdl/examples_pkg.vhdl
ghdl -a $FLAGS ../../hdl/top.vhdl
ghdl --synth $FLAGS Top
