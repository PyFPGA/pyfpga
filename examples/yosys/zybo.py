"""Zybo with Yosys-Vivado example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('yosys-vivado', 'zybo')
prj.set_outdir('../../build/yosys-zybo')
prj.set_part('xc7z010-1-clg400')

prj.add_include('../hdl/headers1/freq.vh')
prj.add_include('../hdl/headers2/secs.vh')
prj.add_files('../hdl/blinking.v')
prj.add_files('../hdl/top.v')
prj.add_files('../vivado/zybo.xdc')
prj.set_top('Top')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

try:
    prj.transfer()
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
