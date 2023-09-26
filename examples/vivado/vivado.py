"""Vivado example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
args = parser.parse_args()

prj = Project('vivado')
prj.set_part('xc7z010-1-clg400')

prj.set_outdir('../../build/vivado')

prj.add_param('FREQ', '125000000')
prj.add_files('../../hdl/blinking.vhdl')
prj.add_files('zybo.xdc')
prj.set_top('Blinking')

if args.action in ['generate', 'all']:
    prj.generate()

if args.action in ['transfer', 'all']:
    prj.transfer('fpga')
