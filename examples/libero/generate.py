"""Digi-Key SmartFusion2 Maker Board generate example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('libero', 'mkr')
prj.set_part('m2s010-1-tq144')

prj.set_outdir('../../build/libero')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../hdl/top.vhdl')
prj.set_top('Top')
prj.add_files('mkr.pdc')
prj.add_files('mkr.sdc')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
