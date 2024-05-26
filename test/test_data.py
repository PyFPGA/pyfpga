import os
import pytest

from pyfpga.project import Project, Tool

pattern = {
    'part': 'PARTNAME',
    'top': 'TOPNAME',
    'arch': 'ARCHNAME',
    'includes': ['INC1', 'INC2', 'INC3'],
    'params': {
        'PARAM1': 'VALUE1',
        'PARAM2': 'VALUE2',
        'PARAM3': 'VALUE3'
    },
    'defines': {
        'DEF1': 'VALUE1',
        'DEF2': 'VALUE2',
        'DEF3': 'VALUE3'
    },
}


def test_names():
    prj = Project(Tool.VIVADO)
    prj.set_part('PARTNAME')
    prj.set_top('TOPNAME')
    prj.set_arch('ARCHNAME')
    prj.add_include('INC1')
    prj.add_include('INC2')
    prj.add_include('INC3')
    prj.add_param('PARAM1', 'VALUE1')
    prj.add_param('PARAM2', 'VALUE2')
    prj.add_param('PARAM3', 'VALUE3')
    prj.add_define('DEF1', 'VALUE1')
    prj.add_define('DEF2', 'VALUE2')
    prj.add_define('DEF3', 'VALUE3')
    assert prj.data == pattern, 'ERROR: unexpected data'
