"""Yosys example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog',
)
args = parser.parse_args()

prj = Project('yosys')
prj.set_outdir('../../build/yosys-{}'.format(args.lang))

if args.lang == 'verilog':
    prj.add_path('../../hdl/headers1')
    prj.add_path('../../hdl/headers2')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', library='examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
    prj.add_files('../../hdl/top.vhdl')

prj.set_top('Top')

try:
    prj.generate()
except RuntimeError:
    print('ERROR:generate:Docker not found')
