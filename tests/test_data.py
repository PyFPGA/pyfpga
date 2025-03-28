from pathlib import Path
from pyfpga.vivado import Vivado

tdir = Path(__file__).parent.resolve()


def prepare(path):
    return Path(tdir / path).as_posix()


pattern = {
    'project': 'EXAMPLE',
    'part': 'PARTNAME',
    'includes': [
        prepare('fakedata/dir1'),
        prepare('fakedata/dir2'),
        prepare('fakedata/dir3')
    ],
    'files': {
        prepare('fakedata/vhdl0.vhdl'): {'hdl': 'vhdl', 'lib': 'LIB'},
        prepare('fakedata/dir1/vhdl1.vhdl'): {'hdl': 'vhdl', 'lib': 'LIB'},
        prepare('fakedata/dir2/vhdl2.vhdl'): {'hdl': 'vhdl', 'lib': 'LIB'},
        prepare('fakedata/dir3/vhdl3.vhdl'): {'hdl': 'vhdl', 'lib': 'LIB'},
        prepare('fakedata/vlog0.v'): {'hdl': 'vlog'},
        prepare('fakedata/dir1/vlog1.v'): {'hdl': 'vlog'},
        prepare('fakedata/dir2/vlog2.v'): {'hdl': 'vlog'},
        prepare('fakedata/dir3/vlog3.v'): {'hdl': 'vlog'},
        prepare('fakedata/slog0.sv'): {'hdl': 'slog'},
        prepare('fakedata/dir1/slog1.sv'): {'hdl': 'slog'},
        prepare('fakedata/dir2/slog2.sv'): {'hdl': 'slog'},
        prepare('fakedata/dir3/slog3.sv'): {'hdl': 'slog'}
    },
    'top': 'TOPNAME',
    'constraints': {
        prepare('fakedata/cons/all.xdc'): {},
        prepare('fakedata/cons/syn.xdc'): {},
        prepare('fakedata/cons/par.xdc'): {}
    },
    'params': {
        'PAR1': 'VAL01',
        'PAR2': 'VAL02',
        'PAR3': 'VAL03'
    },
    'defines': {
        'DEF1': 'VAL01',
        'DEF2': 'VAL02',
        'DEF3': 'VAL03'
    },
    'hooks': {
        'precfg': ['CMD01', 'CMD02'],
        'postcfg': ['CMD03', 'CMD04'],
        'presyn': ['CMD05', 'CMD06'],
        'postsyn': ['CMD07', 'CMD08'],
        'prepar': ['CMD09', 'CMD10'],
        'postpar': ['CMD11', 'CMD12'],
        'prebit': ['CMD13', 'CMD14'],
        'postbit': ['CMD15', 'CMD16']
    }
}


def test_data():
    prj = Vivado('EXAMPLE')
    prj.set_part('PARTNAME')
    prj.set_top('TOPNAME')
    prj.add_include(str(tdir / 'fakedata/dir1'))
    prj.add_include(str(tdir / 'fakedata/dir2'))
    prj.add_include(str(tdir / 'fakedata/dir3'))
    prj.add_slog(str(tdir / 'fakedata/**/*.sv'))
    prj.add_vhdl(str(tdir / 'fakedata/**/*.vhdl'), 'LIB')
    prj.add_vlog(str(tdir / 'fakedata/**/*.v'))
    prj.add_cons(str(tdir / 'fakedata/cons/all.xdc'))
    prj.add_cons(str(tdir / 'fakedata/cons/syn.xdc'))
    prj.add_cons(str(tdir / 'fakedata/cons/par.xdc'))
    prj.add_param('PAR1', 'VAL01')
    prj.add_param('PAR2', 'VAL02')
    prj.add_param('PAR3', 'VAL03')
    prj.add_define('DEF1', 'VAL01')
    prj.add_define('DEF2', 'VAL02')
    prj.add_define('DEF3', 'VAL03')
    prj.add_hook('precfg', 'CMD01')
    prj.add_hook('precfg', 'CMD02')
    prj.add_hook('postcfg', 'CMD03')
    prj.add_hook('postcfg', 'CMD04')
    prj.add_hook('presyn', 'CMD05')
    prj.add_hook('presyn', 'CMD06')
    prj.add_hook('postsyn', 'CMD07')
    prj.add_hook('postsyn', 'CMD08')
    prj.add_hook('prepar', 'CMD09')
    prj.add_hook('prepar', 'CMD10')
    prj.add_hook('postpar', 'CMD11')
    prj.add_hook('postpar', 'CMD12')
    prj.add_hook('prebit', 'CMD13')
    prj.add_hook('prebit', 'CMD14')
    prj.add_hook('postbit', 'CMD15')
    prj.add_hook('postbit', 'CMD16')
    assert prj.data == pattern, 'ERROR: unexpected data'
    paths = prj.data['includes'] + list(prj.data['files'].keys())
    for path in paths:
        assert '\\' not in path, (
            f"'{path}' contains a '\\' character, which is not allowed."
        )
