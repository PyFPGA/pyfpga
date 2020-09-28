"""Yosys-ISE example project."""

import argparse
import logging

from fpga.project import Project

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog',
)
args = parser.parse_args()

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('yosys-ise')
prj.set_outdir('../../build/yosys-ise-{}'.format(args.lang))
prj.set_part('XC6SLX9-2-CSG324')

if args.lang == 'verilog':
    prj.add_include('../../hdl/headers1/freq.vh')
    prj.add_include('../../hdl/headers2/secs.vh')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', 'examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', 'examples')
    prj.add_files('../../hdl/top.vhdl')

prj.add_files('../ise/s6micro.ucf')
prj.set_top('Top')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))

if args.action in ['transfer', 'all']:
    try:
        prj.transfer()
    except Exception as e:
        logging.warning('ERROR: {} ({})'.format(type(e).__name__, e))
