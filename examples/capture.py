"""PyFPGA capture example.

Example about how to capture the execution messages to be post-processed
or saved into a file.
"""

import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

PRJ = Project('ise', 'capture')
PRJ.set_outdir('../build/capture')

PRJ.add_files('hdl/*.vhdl', 'examples')
PRJ.set_top('Top')

try:
    output = PRJ.generate(to_task='syn', capture=True)
    print('### STDOUT:')
    print(output.stdout)
    print('### STDERR:')
    print(output.stderr)
except Exception as e:
    logging.warning('{} ({})'.format(type(e).__name__, e))
