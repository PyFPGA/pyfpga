"""Trellis example project."""

import argparse
import logging

from fpga.project import Project

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate'
)
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog'
)
parser.add_argument(
    '--board',
    choices=['orangecrab', 'ecp5evn'],
    default='orangecrab'
)
args = parser.parse_args()

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

BOARDS = {
    'orangecrab': ['25k-CSFBGA285', 'orangecrab_r0.2.lpf'],
    'ecp5evn': ['um5g-85k-CABGA381', 'ecp5evn.lpf']
}

prj = Project('openflow')
prj.set_outdir('../../build/prjtrellis-{}-{}'.format(args.board, args.lang))
prj.set_part(BOARDS[args.board][0])

if args.lang == 'verilog':
    prj.add_path('../../hdl/headers1')
    prj.add_path('../../hdl/headers2')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', library='examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
    prj.add_files('../../hdl/top.vhdl')

prj.add_files(BOARDS[args.board][1])
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
