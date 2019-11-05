"""S6Micro example project."""

from fpga.project import Project

prj = Project('ise', 's6micro')
prj.set_part('XC6SLX9-2-CSG324')

prj.set_outdir('../../build/s6micro')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../hdl/top.vhdl')
prj.add_files('s6micro.ucf')
prj.set_top('Top')

prj.generate()

#set fpga_pos  1
#set spi_width 1
#set spi_name  W25Q64BV
#set bpi_width 8
#set bpi_name  28F128J3D
