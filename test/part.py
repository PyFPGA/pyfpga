"""Test of set_part.

For Ise and Libero.
"""

import logging

from fpga.project import Project

logging.basicConfig()


def get_part(prj):
    return prj.get_configs()['part'].lower()


prj = Project('ise')
assert get_part(prj) == "xc7k160t-3-fbg484"
prj.set_part('XC6SLX9-2-CSG324')
assert get_part(prj) == "xc6slx9-2-csg324"
prj.set_part('XC6SLX9-2L-CSG324')
assert get_part(prj) == "xc6slx9-2l-csg324"
prj.set_part('XC6SLX9-CSG324-3')
assert get_part(prj) == "xc6slx9-3-csg324"

prj = Project('libero')
assert get_part(prj) == "mpf100t-1-fcg484"
prj.set_part('m2s010-3-tq144')
assert get_part(prj) == "m2s010-3-tq144"
prj.set_part('m2s010-tq144-2')
assert get_part(prj) == "m2s010-2-tq144"
prj.set_part('m2s010-tq144')
assert get_part(prj) == "m2s010-std-tq144"
