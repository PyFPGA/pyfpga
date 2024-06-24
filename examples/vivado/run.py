"""Vivado VHDL example project."""

import argparse

from pyfpga.vivado import Vivado

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl', 'slog', 'design'], default='vlog'
)
args = parser.parse_args()

prj = Vivado(odir=f'../build/vivado-{args.source}')
prj.set_part('xc7z010-1-clg400')

prj.add_param('FREQ', '125000000')
if args.source == 'vhdl':
    prj.add_vhdl('../sources/vhdl/*.vhdl', 'blink_lib')
if args.source == 'vlog':
    prj.add_include('../sources/vlog/include')
    prj.add_vlog('../sources/vlog/*.v')
if args.source == 'slog':
    prj.add_include('../sources/slog/include')
    prj.add_vlog('../sources/slog/*.sv')
if args.source in ['vlog', 'slog']:
    prj.add_define('DEFINE', '1')
prj.add_cons('../sources/zybo/timing.xdc', 'syn')
prj.add_cons('../sources/zybo/clk.xdc', 'par')
prj.add_cons('../sources/zybo/led.xdc', 'par')
prj.set_top('Top')

if args.action in ['make', 'all']:
    prj.make()

if args.action in ['prog', 'all']:
    prj.prog()
