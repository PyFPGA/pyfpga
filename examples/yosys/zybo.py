"""Zybo with Yosys-Vivado example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

PART = 'xc7z010-1-clg400'
OUTDIR = '../../build/yosys-zybo'

prj = Project('yosys')
prj.set_outdir(OUTDIR)
prj.set_part(PART)

prj.add_files('../hdl/headers1/freq.vh', included=True)
prj.add_files('../hdl/headers2/secs.vh', included=True)
prj.add_files('../hdl/blinking.v')
prj.add_files('../hdl/top.v')
prj.set_top('Top')

try:
    prj.generate(to_task='syn')
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

prj = Project('vivado', 'zybo')
prj.set_outdir(OUTDIR)
prj.set_part(PART)

prj.add_files('zybo.xdc')
prj.add_files(OUTDIR + '/yosys.edif')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
