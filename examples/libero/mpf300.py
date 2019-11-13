"""MPF300 example project."""

from fpga.project import Project

prj = Project('libero', 'mpf300')
prj.set_part('mpf300ts-1-fcg1152')

prj.set_outdir('../../build/mpf300')

prj.add_files('../hdl/blinking.vhdl', 'examples')
prj.add_files('../hdl/examples_pkg.vhdl', 'examples')
prj.add_files('../hdl/top.vhdl')
prj.add_files('mpf300.pdc')
prj.set_top('Top')

prj.generate()
