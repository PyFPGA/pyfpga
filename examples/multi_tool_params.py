"""PyFPGA Multi Vendor example where parameters are changed.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices could be used. In this example, VHDL and Verilog
files are synthesized changing the value of its generics/parameters.
"""

import logging

from fpga.project import Project, TOOLS

logging.basicConfig()

for hdl in ['vhdl', 'verilog']:
    for tool in TOOLS:
        PRJ = Project(tool)
        PRJ.set_param('FREQ', '50000000')
        PRJ.set_param('SECS', '2')
        PRJ.set_outdir('../build/multi-tool-params/%s/%s' % (tool, hdl))
        if hdl == 'vhdl':
            PRJ.add_files('hdl/blinking.vhdl')
        else:
            PRJ.add_include('hdl/headers1/freq.vh')
            PRJ.add_include('hdl/headers2/secs.vh')
            PRJ.add_files('hdl/blinking.v')
        PRJ.set_top('Blinking')
        try:
            PRJ.generate(to_task='syn')
        except Exception as e:
            print('There was an error running %s with %s files' % (tool, hdl))
            print('{} ({})'.format(type(e).__name__, e))
