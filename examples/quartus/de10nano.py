"""DE10Nano example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('quartus', 'de10nano')
prj.set_part('5CSEBA6U23I7')

prj.set_outdir('../../build/de10nano')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../hdl/top.vhdl')
prj.set_top('Top')
prj.add_files('de10nano.sdc')
prj.add_files('de10nano.tcl')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))

#try:
#    prj.transfer('fpga', 2)
#except Exception as e:
#    logging.warning('{} ({})'.format(type(e).__name__, e))
