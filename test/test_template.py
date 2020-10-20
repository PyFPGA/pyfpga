import os
import pytest

from fpga.project import Project


def get_path(file):
    return os.path.join(os.path.dirname(__file__), file)


def test_min():
    prj = Project('tclsh')
    prj.set_outdir(get_path('../build/test'))
    output = prj.generate(to_task='prj', capture=True)
    assert output.count('PyFPGA') == 9


def test_max():
    prj = Project('tclsh')
    prj.set_outdir(get_path('../build/test'))
    output = prj.generate(capture=True)
    prj.add_path(get_path('../hdl/headers1'))
    prj.add_path(get_path('../hdl/headers2'))
    prj.add_files(get_path('../hdl/blinking.v'))
    prj.add_files(get_path('../hdl/top.v'))
    prj.set_top(get_path('../hdl/top.v'))
    assert output.count('PyFPGA') == 19
