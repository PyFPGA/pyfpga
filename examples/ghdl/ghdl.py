"""Generic GHDL example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('ghdl')
prj.set_outdir('../../build/ghdl')

prj.add_files('../../hdl/blinking.vhdl', 'examples')
prj.add_files('../../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../../hdl/top.vhdl')
prj.set_top('Top')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
