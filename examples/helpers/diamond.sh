#!/bin/bash

set -e

HDIR=../../pyfpga/helpers

python3 $HDIR/hdl2bit.py -t diamond -o results/diamond-vlog -p lfxp2-5e-5tn144c \
    -i ../sources/vlog/include1 -i ../sources/vlog/include2 \
    -f ../sources/vlog/blink.v -f ../sources/vlog/top.v \
    -f ../sources/cons/brevia2/clk.lpf -f ../sources/cons/brevia2/led.lpf \
    --define DEFINE1 1 --define DEFINE2 1 --param FREQ 125000000 --param SECS 1 Top

python3 $HDIR/hdl2bit.py -t diamond -o results/diamond-vhdl -p lfxp2-5e-5tn144c --project example \
    -f ../sources/vhdl/blink.vhdl,blink_lib -f ../sources/vhdl/blink_pkg.vhdl,blink_lib -f ../sources/vhdl/top.vhdl \
    -f ../sources/cons/brevia2/clk.lpf -f ../sources/cons/brevia2/led.lpf \
    --param FREQ 125000000 --param SECS 1 --last cfg Top

python3 $HDIR/prj2bit.py results/diamond-vhdl/example.ldf
