"""PyFPGA example about Memory Content Files inclusion.

This example is mainly used as a test of this feature through the different
tools.
"""

import logging

from fpga.project import Project, TOOLS

logging.basicConfig()

for hdl in ['vhdl', 'verilog']:
    for tool in TOOLS:
        if tool == 'yosys' and hdl == 'vhdl':
            continue
        if tool == 'ghdl' and hdl == 'verilog':
            continue
        PRJ = Project(tool)
        PRJ.set_outdir('../../build/multi/memory/%s/%s' % (tool, hdl))
        if hdl == 'vhdl':
            PRJ.add_files('../../hdl/ram.vhdl')
        else:
            PRJ.add_files('../../hdl/ram.v')
        PRJ.set_top('ram')
        try:
            PRJ.generate(to_task='syn')
        except Exception as e:
            print('There was an error running %s with %s files' % (tool, hdl))
            print('{} ({})'.format(type(e).__name__, e))
