"""Zybo transfer example project."""

from fpga.project import Project

prj = Project('vivado', 'zybo')
prj.set_outdir('../../build/zybo')

try:
    prj.transfer('fpga')
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
