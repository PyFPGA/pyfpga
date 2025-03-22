#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t openflow -o results/openflow-vlog -p hx1k-tq144 \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/icestick/clk.pcf -f ../sources/cons/icestick/led.pcf \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 100000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t openflow -o results/openflow-vhdl -p hx1k-tq144 --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/icestick/clk.pcf -f ../sources/cons/icestick/led.pcf \
    --param FREQ 125000000 --param SECS 1 --last syn Top

# OpenFlow doesn't have a project file, so it is not supported by prj2bit

python3 $HDIR/bitprog.py -t openflow results/openflow-vhdl/openflow.bit
