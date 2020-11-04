"""Libero example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
args = parser.parse_args()

prj = Project('libero')
prj.set_part('m2s010-1-tq144')

prj.set_outdir('../../build/libero')

prj.add_files('../../hdl/blinking.vhdl', library='examples')
prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
prj.add_files('../../hdl/top.vhdl')
prj.set_top('Top')
prj.add_files('mkr.pdc')
prj.add_files('mkr.sdc')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except RuntimeError:
        print('ERROR:generate:Libero not found')

if args.action in ['transfer', 'all']:
    print('ERROR:transfer:Not yet implemented')
