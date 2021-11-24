"""ISE example project."""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
parser.add_argument(
    '--board',
    choices=['nexys3', 's6micro'],
    default='nexys3'
)
args = parser.parse_args()

BOARDS = {
    'nexys3': ['XC6SLX16-3-CSG324', 'nexys3.ucf', 'nexys3.xcf'],
    's6micro': ['XC6SLX9-2-CSG324', 's6micro.ucf', 's6micro.xcf']
}

prj = Project('ise')
prj.set_part(BOARDS[args.board][0])

prj.set_outdir('../../build/ise-{}'.format(args.board))

prj.add_files('../../hdl/blinking.vhdl', library='examples')
prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
prj.add_files('../../hdl/top.vhdl')
prj.set_top('Top')

prj.add_files(BOARDS[args.board][1])
prj.add_files(BOARDS[args.board][2])

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except RuntimeError:
        print('ERROR:generate:ISE not found')

if args.action in ['transfer', 'all']:
    try:
        prj.transfer('fpga')
        #  prj.transfer('detect')
        #  prj.transfer('unlock')
        #  prj.transfer('spi', 1, 'N25Q128', 4)
    except RuntimeError:
        print('ERROR:transfer:ISE not found')
