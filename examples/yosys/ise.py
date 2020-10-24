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
    prj.add_path('../../hdl/headers1')
    prj.add_path('../../hdl/headers2')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', library='examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
    prj.add_files('../../hdl/top.vhdl')

prj.add_files('../ise/s6micro.ucf')
prj.set_top('Top')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except RuntimeError:
        print('ERROR:generate:Docker or ISE not found')

if args.action in ['transfer', 'all']:
    try:
        prj.transfer()
    except RuntimeError:
        print('ERROR:transfer:ISE not found')
