"""Quartus example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
args = parser.parse_args()

prj = Project('quartus')
prj.set_part('5CSEBA6U23I7')

prj.set_outdir('../../build/quartus')

prj.add_files('../../hdl/blinking.vhdl', library='examples')
prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
prj.add_files('../../hdl/top.vhdl')
prj.set_top('Top')
prj.add_files('de10nano.sdc')
prj.add_files('de10nano.tcl')

if args.action in ['generate', 'all']:
    prj.generate()

if args.action in ['transfer', 'all']:
    prj.transfer('fpga', 2)
