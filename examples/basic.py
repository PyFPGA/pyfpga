"""PyFPGA basic example."""

from fpga.project import Project

PRJ = Project('vivado', 'basic')
PRJ.set_outdir('../build/basic')

PRJ.set_part('ExampleFPGA')
PRJ.add_files('hdl/*.vhdl')
PRJ.set_top('Top')

PRJ.generate()
