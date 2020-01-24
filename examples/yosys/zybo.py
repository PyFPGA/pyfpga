"""Zybo with Yosys-Vivado example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

PART = 'xc7z010-1-clg400'
OUTDIR = '../../build/yosys-zybo'
TOP = 'Top'

prj = Project('yosys')
prj.set_outdir(OUTDIR)
prj.set_part(PART)

prj.add_include('../hdl/headers1/freq.vh')
prj.add_include('../hdl/headers2/secs.vh')
prj.add_files('../hdl/blinking.v')
prj.add_files('../hdl/top.v')
prj.set_top(TOP)

try:
    prj.generate(to_task='syn')
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

prj = Project('vivado', 'zybo')
prj.set_outdir(OUTDIR)
prj.set_part(PART)

prj.add_files('../vivado/zybo.xdc')
prj.add_files(OUTDIR + '/yosys.edif')
prj.set_top('yosys')

try:
    prj.generate(to_task='prj')
    # Synthesis performed by Yosys
    prj.generate(to_task='bit', from_task='imp')
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

try:
    prj.transfer('fpga')
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
