"""Test of set_top."""

import logging

from fpga.project import Project

logging.basicConfig()

prj = Project()
assert prj.tool.top == "UNDEFINED"

prj.set_top('test1')
assert prj.tool.top == "test1"

prj.set_top('../examples/hdl/blinking.vhdl')
assert prj.tool.top == "Blinking"

prj.set_top('test2')
assert prj.tool.top == "test2"

prj.set_top('../examples/hdl/blinking.v')
assert prj.tool.top == "Blinking"

prj.set_top('part.py')
assert prj.tool.top == "UNDEFINED"
