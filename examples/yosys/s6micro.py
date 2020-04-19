"""S6micro with Yosys-ISE example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('yosys-ise', 's6micro')
prj.set_outdir('../../build/yosys-s6micro')
prj.set_part('XC6SLX9-2-CSG324')

prj.add_include('../../hdl/headers1/freq.vh')
prj.add_include('../../hdl/headers2/secs.vh')
prj.add_files('../../hdl/blinking.v')
prj.add_files('../../hdl/top.v')
prj.add_files('../ise/s6micro.ucf')
prj.set_top('Top')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

try:
    prj.transfer()
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
