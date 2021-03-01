"""Symbiflow example project."""

import logging

from fpga.project import Project

logging.basicConfig()

prj = Project('symbiflow')
prj.set_outdir('../../build/symbiflow')
prj.set_part('xc7a35tcsg324-1')

prj.add_files('../../resources/verilog/blink.v')

prj.add_files('../../resources/constraints/arty-a7-35t/*.xdc')
prj.set_top('Blink')

try:
    prj.generate()
except RuntimeError:
    print('ERROR:generate:Symbiflow not found')
