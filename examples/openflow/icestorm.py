"""Icestorm example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate'
)
parser.add_argument(
    '--lang', choices=['verilog', 'vhdl'], default='verilog'
)
parser.add_argument(
    '--board',
    choices=['icestick', 'edu-ciaa-fpga'],
    default='icestick'
)
args = parser.parse_args()

BOARDS = {
    'icestick': ['hx1k-tq144', 'icestick.pcf'],
    'edu-ciaa-fpga': ['hx4k-tq144', 'edu-ciaa-fpga.pcf']
}

prj = Project('openflow')
prj.set_outdir('../../build/icestorm-{}-{}'.format(args.board, args.lang))
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
    prj.generate()

if args.action in ['transfer', 'all']:
    prj.transfer()
