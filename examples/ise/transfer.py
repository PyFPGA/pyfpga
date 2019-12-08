"""S6micro transfer example project."""

from fpga.project import Project

prj = Project('ise', 's6micro')
prj.set_outdir('../../build/s6micro')

try:
    prj.transfer('fpga')
#    prj.transfer('detect')
#    prj.transfer('unlock')
#    prj.transfer('spi', 1, 'N25Q128', 4)
except Exception as e:
    print('ERROR: {} ({})'.format(type(e).__name__, e))
