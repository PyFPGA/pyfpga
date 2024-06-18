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
        Path('fakedata/vhdl0.vhdl').resolve(): ['vhdl', 'LIB'],
        Path('fakedata/dir1/vhdl1.vhdl').resolve(): ['vhdl', 'LIB'],
        Path('fakedata/dir2/vhdl2.vhdl').resolve(): ['vhdl', 'LIB'],
        Path('fakedata/dir3/vhdl3.vhdl').resolve(): ['vhdl', 'LIB'],
        Path('fakedata/vlog0.v').resolve(): ['vlog'],
        Path('fakedata/dir1/vlog1.v').resolve(): ['vlog'],
        Path('fakedata/dir2/vlog2.v').resolve(): ['vlog'],
        Path('fakedata/dir3/vlog3.v').resolve(): ['vlog'],
        Path('fakedata/slog0.sv').resolve(): ['slog'],
        Path('fakedata/dir1/slog1.sv').resolve(): ['slog'],
        Path('fakedata/dir2/slog2.sv').resolve(): ['slog'],
        Path('fakedata/dir3/slog3.sv').resolve(): ['slog']
    },
    'constraints': {
        Path('fakedata/cons/all.xdc').resolve(): ['syn', 'par'],
        Path('fakedata/cons/syn.xdc').resolve(): ['syn'],
        Path('fakedata/cons/par.xdc').resolve(): ['par']
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


def test_data():
    prj = Project()
    prj.set_part('PARTNAME')
    prj.set_top('TOPNAME')
    prj.set_arch('ARCHNAME')
    prj.add_include('fakedata/dir1')
    prj.add_include('fakedata/dir2')
    prj.add_include('fakedata/dir3')
    prj.add_slog('fakedata/**/*.sv')
    prj.add_vhdl('fakedata/**/*.vhdl', 'LIB')
    prj.add_vlog('fakedata/**/*.v')
    prj.add_constraint('fakedata/cons/all.xdc')
    prj.add_constraint('fakedata/cons/syn.xdc', True, False)
    prj.add_constraint('fakedata/cons/par.xdc', False, True)
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
