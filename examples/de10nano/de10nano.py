"""DE10Nano example project."""

from fpga.project import Project

prj = Project('quartus', 'de10nano')
prj.set_part('5CSEBA6U23I7')

prj.set_outdir('../../build/de10nano')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../hdl/top.vhdl')
prj.add_files('de10nano.tcl')
prj.set_top('Top')

prj.generate()

#set fpga_pos 2
