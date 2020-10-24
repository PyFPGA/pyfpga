"""PyFPGA Multi Vendor Verilog example.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices could be used.
"""

import logging

from fpga.project import Project, TOOLS

logging.basicConfig()

for tool in TOOLS:
    if tool == 'ghdl':
        continue
    PRJ = Project(tool)
    PRJ.set_outdir('../../build/multi/verilog/%s' % tool)
    PRJ.add_path('../../hdl/headers1')
    PRJ.add_path('../../hdl/headers2')
    PRJ.add_files('../../hdl/blinking.v')
    PRJ.add_files('../../hdl/top.v')
    PRJ.set_top('Top')
    try:
        PRJ.generate(to_task='syn')
    except RuntimeError:
        print('ERROR:generate:{} not found'.format(tool))
