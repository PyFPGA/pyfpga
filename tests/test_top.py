import os
import pytest

from fpga.project import Project


def get_pathfile(file):
    return os.path.join(os.path.dirname(__file__), file)


def test_default():
    prj = Project()
    assert prj.tool.top == "UNDEFINED"


def test_names():
    prj = Project()
    prj.set_top('test1')
    assert prj.tool.top == "test1"
    prj.set_top('test2')
    assert prj.tool.top == "test2"


def test_files():
    prj = Project()
    prj.set_top(get_pathfile('../hdl/fakes/top.vhdl'))
    assert prj.tool.top == "Top1"
    prj.set_top(get_pathfile('../hdl/fakes/top.v'))
    assert prj.tool.top == "Top1"
    prj.set_top(get_pathfile('../README.md'))
    assert prj.tool.top == "UNDEFINED"
