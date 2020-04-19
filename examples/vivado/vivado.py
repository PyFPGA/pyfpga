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

prj.add_files('../../hdl/blinking.vhdl', 'examples')
prj.add_files('../../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('zybo.vhdl')
prj.add_files('zybo.xdc')
prj.set_top('Top')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))

if args.action in ['transfer', 'all']:
    try:
        prj.transfer('fpga')
    except Exception as e:
        logging.warning('ERROR: {} ({})'.format(type(e).__name__, e))
