"""PyFPGA Multi Vendor example."""

from fpga.project import Project

tools = ['ise', 'libero', 'quartus', 'vivado']

for tool in tools:
    PRJ = Project(tool)
    PRJ.set_outdir('../build/multi/%s' % tool)
    PRJ.add_files('hdl/*.vhdl')
    PRJ.set_top('Top')
    try:
        PRJ.generate(task='imp')
    except:
        print('%s is not available' % tool)
