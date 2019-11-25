"""PyFPGA Multi Vendor example.

The main idea of a multi-vendor project is to implements the same HDL code
with different tools, to make comparisons. The project name is not important
and the default devices could be used.
"""

from fpga.project import Project, TOOLS

for tool in TOOLS:
    PRJ = Project(tool)
    PRJ.set_outdir('../build/multi-tool/%s' % tool)
    PRJ.add_files('hdl/*.vhdl', 'examples')
    PRJ.set_top('Top')
    try:
        PRJ.generate(task='imp')
    except:
        print('There was an error running %s' % tool)
