#!/bin/bash

FLAGS="-fsynopsys -fexplicit -frelaxed --std=08"

ghdl -a $FLAGS ../../hdl/blinking.vhdl
ghdl --synth $FLAGS Blinking
