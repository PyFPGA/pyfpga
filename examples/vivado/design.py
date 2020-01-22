"""Zybo block design example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('vivado', 'zybo')
prj.set_part('xc7z010-1-clg400')

prj.set_outdir('../../build/zybo/block-design')

prj.add_files('../../../core_comblock/src/helpers/fifo_loop.vhdl')
prj.add_files('../../../core_comblock/src', included=True)
prj.add_files('../../../core_comblock/examples/test/zybo.tcl', design=True)

prj.add_postbit_opt(
    'write_hw_platform -fixed -force -include_bit -file design_1_wrapper.xsa'
)

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
