"""Generic Yosys generate example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('yosys', 'generic')

prj.set_outdir('../../build/yosys')

prj.add_files('../hdl/headers1/freq.vh', included=True)
prj.add_files('../hdl/headers2/secs.vh', included=True)
prj.add_files('../hdl/blinking.v')
prj.add_files('../hdl/top.v')
prj.set_top('Top')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
