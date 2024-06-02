import os
import pytest

from pathlib import Path

from pyfpga.project import Project

pattern = {
    'part': 'PARTNAME',
    'includes': [
        Path('fakedata/dir1').resolve(),
        Path('fakedata/dir2').resolve(),
        Path('fakedata/dir3').resolve()
    ],
    'files': {
        Path('fakedata/dir1/slog1.sv').resolve():
            {'type': 'slog', 'options': None, 'library': None},
        Path('fakedata/dir2/slog2.sv').resolve():
            {'type': 'slog', 'options': None, 'library': None},
        Path('fakedata/dir3/slog3.sv').resolve():
            {'type': 'slog', 'options': None, 'library': None},
        Path('fakedata/dir1/vhdl1.vhdl').resolve():
            {'type': 'vhdl', 'options': None, 'library': None},
        Path('fakedata/dir2/vhdl2.vhdl').resolve():
            {'type': 'vhdl', 'options': None, 'library': None},
        Path('fakedata/dir3/vhdl3.vhdl').resolve():
            {'type': 'vhdl', 'options': None, 'library': None},
        Path('fakedata/dir1/vlog1.v').resolve():
            {'type': 'vlog', 'options': None, 'library': None},
        Path('fakedata/dir2/vlog2.v').resolve():
            {'type': 'vlog', 'options': None, 'library': None},
        Path('fakedata/dir3/vlog3.v').resolve():
            {'type': 'vlog', 'options': None, 'library': None}
    },
    'top': 'TOPNAME',
    'params': {
        'PAR1': 'VAL1',
        'PAR2': 'VAL2',
        'PAR3': 'VAL3'
    },
    'defines': {
        'DEF1': 'VAL1',
        'DEF2': 'VAL2',
        'DEF3': 'VAL3'
    },
    'arch': 'ARCHNAME',
    'hooks': {
        'precfg': ['CMD1', 'CMD2'],
        'postcfg': ['CMD1', 'CMD2'],
        'presyn': ['CMD1', 'CMD2'],
        'postsyn': ['CMD1', 'CMD2'],
        'prepar': ['CMD1', 'CMD2'],
        'postpar': ['CMD1', 'CMD2'],
        'prebit': ['CMD1', 'CMD2'],
        'postbit': ['CMD1', 'CMD2']
    }
}


def test_names():
    prj = Project()
    prj.set_part('PARTNAME')
    prj.set_top('TOPNAME')
    prj.set_arch('ARCHNAME')
    prj.add_include('fakedata/dir1')
    prj.add_include('fakedata/dir2')
    prj.add_include('fakedata/dir3')
    prj.add_slog('fakedata/**/*.sv')
    prj.add_vhdl('fakedata/**/*.vhdl')
    prj.add_vlog('fakedata/**/*.v')
    prj.add_param('PAR1', 'VAL1')
    prj.add_param('PAR2', 'VAL2')
    prj.add_param('PAR3', 'VAL3')
    prj.add_define('DEF1', 'VAL1')
    prj.add_define('DEF2', 'VAL2')
    prj.add_define('DEF3', 'VAL3')
    prj.add_hook('precfg', 'CMD1')
    prj.add_hook('precfg', 'CMD2')
    prj.add_hook('postcfg', 'CMD1')
    prj.add_hook('postcfg', 'CMD2')
    prj.add_hook('presyn', 'CMD1')
    prj.add_hook('presyn', 'CMD2')
    prj.add_hook('postsyn', 'CMD1')
    prj.add_hook('postsyn', 'CMD2')
    prj.add_hook('prepar', 'CMD1')
    prj.add_hook('prepar', 'CMD2')
    prj.add_hook('postpar', 'CMD1')
    prj.add_hook('postpar', 'CMD2')
    prj.add_hook('prebit', 'CMD1')
    prj.add_hook('prebit', 'CMD2')
    prj.add_hook('postbit', 'CMD1')
    prj.add_hook('postbit', 'CMD2')
    assert prj.data == pattern, 'ERROR: unexpected data'
