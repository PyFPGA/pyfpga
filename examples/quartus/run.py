"""Quartus examples."""

import argparse

from pyfpga.quartus import Quartus


parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['de10nano'], default='de10nano'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl', 'slog'], default='vlog'
)
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
args = parser.parse_args()

prj = Quartus(odir='../build/quartus')

if args.board == 'de10nano':
    prj.set_part('5CSEBA6U23I7')
    prj.add_param('FREQ', '125000000')
    prj.add_cons('../sources/de10nano/clk.sdc', 'syn')
    prj.add_cons('../sources/de10nano/clk.tcl', 'par')
    prj.add_cons('../sources/de10nano/led.tcl', 'par')
prj.add_param('SECS', '1')

if args.source == 'vhdl':
    prj.add_vhdl('../sources/vhdl/*.vhdl', 'blink_lib')
if args.source == 'vlog':
    prj.add_include('../sources/vlog/include1')
    prj.add_include('../sources/vlog/include2')
    prj.add_vlog('../sources/vlog/*.v')
if args.source == 'slog':
    prj.add_include('../sources/slog/include1')
    prj.add_include('../sources/slog/include2')
    prj.add_vlog('../sources/slog/*.sv')
if args.source in ['vlog', 'slog']:
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')

prj.set_top('Top')

if args.action in ['make', 'all']:
    prj.make()

if args.action in ['prog', 'all']:
    prj.prog()
