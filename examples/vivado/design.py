"""Zybo block design example project."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

prj = Project('vivado', 'zybo-design')
prj.set_part('xc7z010-1-clg400')

prj.set_outdir('../../build/zybo-design')

prj.add_files('../../hdl/blinking.vhdl')
prj.add_files('zybo.xdc')
prj.add_files('design.tcl', filetype='design')

export = """
set PROJECT %s
if { [ catch {
    # Vitis
    write_hw_platform -fixed -force -include_bit -file ${PROJECT}.xsa
} ] } {
    # SDK
    write_hwdef -force -file ${PROJECT}.hwdef
    write_sysdef -force -hwdef [glob -nocomplain *.hwdef] \\
       -bitfile [glob -nocomplain *.bit] -file ${PROJECT}.hdf
}
""" % ('zybo-design')

prj.add_hook(export, 'postbit')

try:
    prj.generate()
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
