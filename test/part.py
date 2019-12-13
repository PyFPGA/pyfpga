"""Test of set_part.

For Ise and Libero.
"""

from fpga.project import Project

prj = Project('ise')
print(prj.get_configs()['part'])
prj.set_part('XC6SLX9-2-CSG324')
print(prj.get_configs()['part'])
prj.set_part('XC6SLX9-2L-CSG324')
print(prj.get_configs()['part'])
prj.set_part('XC6SLX9-CSG324-3')
print(prj.get_configs()['part'])

prj = Project('libero')
print(prj.get_configs()['part'])
prj.set_part('m2s010-3-tq144')
print(prj.get_configs()['part'])
prj.set_part('m2s010-tq144-2')
print(prj.get_configs()['part'])
prj.set_part('m2s010-tq144')
print(prj.get_configs()['part'])
