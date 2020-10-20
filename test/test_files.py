import os
import pytest

from fpga.project import Project, TOOLS


def get_path(file):
    return os.path.join(os.path.dirname(__file__), file)


@pytest.mark.parametrize('tool', TOOLS)
def test_files(tool):
    prj = Project(tool)
    prj.add_files(get_path('../hdl/*.vhdl'))
    prj.add_files(get_path('../hdl/*.v'))
    assert len(prj.get_fileset('verilog')) == 3
    assert len(prj.get_fileset('vhdl')) == 4
    assert len(prj.get_fileset('constraint')) == 0
