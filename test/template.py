"""Test for template.tcl."""

import sys

from fpga.project import Project

prj = Project('tclsh')
prj.set_outdir('../build/tclsh')

try:
    prj.generate()
except Exception as e:
    print('{} ({})'.format(type(e).__name__, e))
    sys.exit(1)
