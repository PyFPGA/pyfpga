#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t gowin -o results/gowin-vlog -p GW2AR-LV18QN88C8/I7 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/tangnano20k/timing.sdc -f ../sources/cons/tangnano20k/clk.cst \
    -f ../sources/cons/tangnano20k/led.cst \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 27000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t gowin -o results/gowin-vhdl -p GW2AR-LV18QN88C8/I7 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/tangnano20k/timing.sdc -f ../sources/cons/tangnano20k/clk.cst \
    -f ../sources/cons/tangnano20k/led.cst \
    --param FREQ 27000000 --param SECS 1 --last cfg Top
