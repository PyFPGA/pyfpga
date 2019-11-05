"""Zybo example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('vivado', 'zybo')
prj.set_part('xc7z010-1-clg400')

prj.set_outdir('../../build/zybo')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('zybo.vhdl')
prj.add_files('zybo.xdc')
prj.set_top('Top')

prj.generate()
