"""DE10Nano transfer example project."""

from fpga.project import Project

prj = Project('quartus', 'de10nano')
prj.set_outdir('../../build/de10nano')

try:
    prj.transfer('fpga', 2)
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
