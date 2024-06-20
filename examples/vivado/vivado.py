"""Vivado VHDL example project."""

import argparse

from pyfpga.vivado import Vivado

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
parser.add_argument(
    '--source', choices=['vhdl', 'vlog', 'design'], default='vhdl'
)
args = parser.parse_args()

prj = Vivado(odir=f'../build/vivado-{args.source}')
prj.set_part('xc7z010-1-clg400')

prj.add_param('FREQ', '125000000')
if args.source == 'vhdl':
    prj.add_vhdl('../resources/vhdl/blink.vhdl')
if args.source == 'vlog':
    prj.add_vlog('../resources/vlog/blink.v')
prj.add_constraint('../resources/constraints/zybo/timing.xdc', 'syn')
prj.add_constraint('../resources/constraints/zybo/clk.xdc', 'par')
prj.add_constraint('../resources/constraints/zybo/led.xdc', 'par')
prj.set_top('Blink')

if args.action in ['make', 'all']:
    prj.make()

if args.action in ['prog', 'all']:
    prj.prog()
