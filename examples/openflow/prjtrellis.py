"""Trellis example project."""

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
    choices=['orangecrab', 'ecp5evn'],
    default='orangecrab'
)
args = parser.parse_args()

BOARDS = {
    'orangecrab': ['25k-CSFBGA285', 'orangecrab_r0.2.lpf'],
    'ecp5evn': ['um5g-85k-CABGA381', 'ecp5evn.lpf']
}

prj = Project('openflow')
prj.set_outdir('../../build/prjtrellis-{}-{}'.format(args.board, args.lang))
prj.set_part(BOARDS[args.board][0])

if args.lang == 'verilog':
    prj.add_vlog_include('../../hdl/headers1')
    prj.add_vlog_include('../../hdl/headers2')
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
