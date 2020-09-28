"""Yosys example project."""

import argparse
import logging

from fpga.project import Project

parser = argparse.ArgumentParser()
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog',
)
args = parser.parse_args()

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('yosys')
prj.set_outdir('../../build/yosys-{}'.format(args.lang))

if args.lang == 'verilog':
    prj.add_include('../../hdl/headers1/freq.vh')
    prj.add_include('../../hdl/headers2/secs.vh')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', 'examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', 'examples')
    prj.add_files('../../hdl/top.vhdl')

prj.set_top('Top')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
