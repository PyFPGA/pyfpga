"""PyFPGA advanced example."""

import logging

from fpga.project import Project

logging.basicConfig()

PRJ = Project('vivado', 'advanced')
PRJ.set_outdir('../build/advanced')

PRJ.set_part('ExampleFPGA')
PRJ.add_files('hdl/*.vhdl')
PRJ.set_top('Top')

PRJ.add_project_opt('# PROJECT OPTIONS 1')
PRJ.add_project_opt('# PROJECT OPTIONS 2')
PRJ.add_preflow_opt('# PRE FLOW OPTIONS')
PRJ.add_postsyn_opt('# POST SYN OPTIONS')
PRJ.add_postimp_opt('# POST IMP OPTIONS')
PRJ.add_postbit_opt('# POST BIT OPTIONS')

try:
    PRJ.generate('area', 'bit')
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
