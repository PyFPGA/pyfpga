"""Generic GHDL example project."""

import logging

from fpga.project import Project

logging.basicConfig()

prj = Project('ghdl')
prj.set_outdir('../../build/ghdl')

prj.add_files('../../hdl/blinking.vhdl', library='examples')
prj.add_files('../../hdl/examples_pkg.vhdl', library='examples')
prj.add_files('../../hdl/top.vhdl')
prj.set_top('Top')

prj.generate()
