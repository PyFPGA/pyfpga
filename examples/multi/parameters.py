"""PyFPGA Multi Vendor example where parameters are changed.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices are used. In this example, VHDL and Verilog
files are synthesized changing the value of its generics/parameters.
"""

import logging

from fpga.project import Project, TOOLS

logging.basicConfig()

for hdl in ['vhdl', 'verilog']:
    for tool in TOOLS:
        if tool == 'ghdl' and hdl == 'verilog':
            continue
        PRJ = Project(tool)
        PRJ.set_param('FREQ', '50000000')
        PRJ.set_param('SECS', '2')
        PRJ.set_outdir('../../build/multi/params/%s/%s' % (tool, hdl))
        if hdl == 'vhdl':
            PRJ.add_files('../../hdl/blinking.vhdl')
        else:
            PRJ.add_include('../../hdl/headers1/freq.vh')
            PRJ.add_include('../../hdl/headers2/secs.vh')
            PRJ.add_files('../../hdl/blinking.v')
        PRJ.set_top('Blinking')
        # PRJ.set_param('INT', '15')
        # PRJ.set_param('REA', '1.5')
        # PRJ.set_param('LOG', "'1'")
        # PRJ.set_param('VEC', '"10101010"')
        # PRJ.set_param('STR', '"WXYZ"')
        # PRJ.set_outdir('../../build/multi/params/%s/%s' % (tool, hdl))
        # if hdl == 'vhdl':
        #     PRJ.add_files('../../hdl/fakes/generics.vhdl')
        # else:
        #     PRJ.add_files('../../hdl/fakes/parameters.v')
        # PRJ.set_top('Params')
        try:
            PRJ.generate(to_task='syn')
        except Exception as e:
            print('There was an error running %s with %s files' % (tool, hdl))
            print('{} ({})'.format(type(e).__name__, e))
