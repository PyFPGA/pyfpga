"""Icestorm example project."""

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

oci_configs = {
    'cmd': 'docker run --rm -v $HOME:$HOME -w $PWD',
    'syn': 'ghdl/synth:beta',
    'imp': 'ghdl/synth:nextpnr-ice40',
    'bit': 'ghdl/synth:icestorm',
    'prg': '--device /dev/bus/usb ghdl/synth:prog'
}

prj = Project('openflow')
prj.set_outdir('../../build/icestorm-{}'.format(args.lang))
prj.set_part('hx4k-tq144')
prj.set_oci(oci_configs)

if args.lang == 'verilog':
    prj.add_path('../../hdl/headers1')
    prj.add_path('../../hdl/headers2')
    prj.add_files('../../hdl/blinking.v')
    prj.add_files('../../hdl/top.v')
else:  # args.lang == 'vhdl'
    prj.add_files('../../hdl/blinking.vhdl', library='examples')
    prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
    prj.add_files('../../hdl/top.vhdl')

prj.add_files('*.pcf')
prj.set_top('Top')

if args.action in ['generate', 'all']:
    try:
        prj.generate()
    except RuntimeError:
        print('ERROR:generate:Docker not found')

if args.action in ['transfer', 'all']:
    try:
        prj.transfer()
    except RuntimeError:
        print('ERROR:transfer:Docker not found')
