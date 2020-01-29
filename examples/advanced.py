"""PyFPGA advanced example."""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

PRJ = Project('vivado', 'advanced')
PRJ.set_outdir('../build/advanced')

PRJ.set_part('ExampleFPGA')
PRJ.add_files('hdl/*.vhdl')
PRJ.set_top('Top')

PRJ.add_prefile_opt('# PRE FILE OPTIONS 1')
PRJ.add_postprj_opt('# POST PRJ OPTIONS 1')
PRJ.add_preflow_opt('# PRE FLOW OPTIONS 1')
PRJ.add_postsyn_opt('# POST SYN OPTIONS 1')
PRJ.add_postimp_opt('# POST IMP OPTIONS 1')
PRJ.add_postbit_opt('# POST BIT OPTIONS 1')

PRJ.add_prefile_opt('# PRE FILE OPTIONS 2')
PRJ.add_postprj_opt('# POST PRJ OPTIONS 2')
PRJ.add_preflow_opt('# PRE FLOW OPTIONS 2')
PRJ.add_postsyn_opt('# POST SYN OPTIONS 2')
PRJ.add_postimp_opt('# POST IMP OPTIONS 2')
PRJ.add_postbit_opt('# POST BIT OPTIONS 2')

try:
    PRJ.generate('area', 'bit')
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
