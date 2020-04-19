"""PyFPGA Multi Vendor Verilog example.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices could be used.
"""

import logging

from fpga.project import Project, TOOLS

logging.basicConfig()

for tool in TOOLS:
    PRJ = Project(tool)
    PRJ.set_outdir('../../build/multi/verilog/%s' % tool)
    PRJ.add_include('../../hdl/headers1/freq.vh')
    PRJ.add_include('../../hdl/headers2/secs.vh')
    PRJ.add_files('../../hdl/blinking.v')
    PRJ.add_files('../../hdl/top.v')
    PRJ.set_top('Top')
    try:
        PRJ.generate(to_task='syn')
    except Exception as e:
        print('There was an error running %s' % tool)
        print('{} ({})'.format(type(e).__name__, e))
