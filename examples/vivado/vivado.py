"""Vivado example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
args = parser.parse_args()

prj = Project('vivado')
prj.set_part('xc7z010-1-clg400')

prj.set_outdir('../../build/vivado')

prj.set_param('FREQ', '125000000')
prj.add_files('../../hdl/blinking.vhdl')
prj.add_files('zybo.xdc')
prj.set_top('Blinking')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except RuntimeError:
        print('ERROR:generate:Vivado not found')

if args.action in ['transfer', 'all']:
    try:
        prj.transfer('fpga')
    except RuntimeError:
        print('ERROR:transfer:Vivado not found')
