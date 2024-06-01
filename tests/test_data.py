import os
import pytest

from pyfpga.project import Project

pattern = {
    'part': 'PARTNAME',
    'includes': ['INC1', 'INC2', 'INC3'],
    'files': {
        'path1': {'type': 'TYPE1', 'options': 'OPTION1', 'library': 'LIBRARY1'},
        'path2': {'type': 'TYPE2', 'options': 'OPTION2', 'library': 'LIBRARY2'},
        'path3': {'type': 'TYPE3', 'options': 'OPTION3', 'library': 'LIBRARY3'}
    },
    'top': 'TOPNAME',
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
    'arch': 'ARCHNAME',
    'hooks': {
        'precfg': ['HOOK1', 'HOOK2', 'HOOKn'],
        'postcfg': ['HOOK1', 'HOOK2', 'HOOKn'],
        'presyn': ['HOOK1', 'HOOK2', 'HOOKn'],
        'postsyn': ['HOOK1', 'HOOK2', 'HOOKn'],
        'prepar': ['HOOK1', 'HOOK2', 'HOOKn'],
        'postpar': ['HOOK1', 'HOOK2', 'HOOKn'],
        'prebit': ['HOOK1', 'HOOK2', 'HOOKn'],
        'postbit': ['HOOK1', 'HOOK2', 'HOOKn']
    }
}


def test_names():
    prj = Project()
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
