import os
import pytest

from pyfpga.project import Project

pattern = {
    'part': 'PARTNAME',
    'includes': ['INC1', 'INC2', 'INC3'],
    'files': {
        'path1': {'type': 'vhdl', 'options': 'OPT1', 'library': 'LIB1'},
        'path2': {'type': 'vlog', 'options': 'OPT2', 'library': None},
        'path3': {'type': 'slog', 'options': 'OPT3', 'library': None},
        'path4': {'type': 'cons', 'options': 'OPT4', 'library': None}
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
        'precfg': ['HOOK1', 'HOOK2'],
        'postcfg': ['HOOK1', 'HOOK2'],
        'presyn': ['HOOK1', 'HOOK2'],
        'postsyn': ['HOOK1', 'HOOK2'],
        'prepar': ['HOOK1', 'HOOK2'],
        'postpar': ['HOOK1', 'HOOK2'],
        'prebit': ['HOOK1', 'HOOK2'],
        'postbit': ['HOOK1', 'HOOK2']
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
    prj.add_vhdl('path1', 'LIB1', 'OPT1')
    prj.add_vlog('path2', 'OPT2')
    prj.add_slog('path3', 'OPT3')
    prj.add_cons('path4', 'OPT4')
    prj.add_hook('precfg', 'HOOK1')
    prj.add_hook('precfg', 'HOOK2')
    prj.add_hook('postcfg', 'HOOK1')
    prj.add_hook('postcfg', 'HOOK2')
    prj.add_hook('presyn', 'HOOK1')
    prj.add_hook('presyn', 'HOOK2')
    prj.add_hook('postsyn', 'HOOK1')
    prj.add_hook('postsyn', 'HOOK2')
    prj.add_hook('prepar', 'HOOK1')
    prj.add_hook('prepar', 'HOOK2')
    prj.add_hook('postpar', 'HOOK1')
    prj.add_hook('postpar', 'HOOK2')
    prj.add_hook('prebit', 'HOOK1')
    prj.add_hook('prebit', 'HOOK2')
    prj.add_hook('postbit', 'HOOK1')
    prj.add_hook('postbit', 'HOOK2')
    assert prj.data == pattern, 'ERROR: unexpected data'
