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
        if tool == 'ghdl':
            continue
        if hdl == 'vhdl':
            if tool in ['openflow', 'yosys', 'yosys-ise', 'yosys-vivado']:
                continue
        PRJ = Project(tool)
        PRJ.set_param('FREQ', '50000000')
        PRJ.set_param('SECS', '2')
        PRJ.set_outdir('../../build/multi/params/%s/%s' % (tool, hdl))
        if hdl == 'vhdl':
            PRJ.add_files('../../hdl/blinking.vhdl')
        else:
            PRJ.add_path('../../hdl/headers1')
            PRJ.add_path('../../hdl/headers2')
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
        PRJ.generate(to_task='syn')
