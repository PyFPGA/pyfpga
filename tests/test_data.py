from pathlib import Path

from pyfpga.vivado import Vivado

tdir = Path(__file__).parent.resolve()

pattern = {
    'project': 'EXAMPLE',
    'part': 'PARTNAME',
    'includes': [
        Path(tdir / 'fakedata/dir1').resolve().as_posix(),
        Path(tdir / 'fakedata/dir2').resolve().as_posix(),
        Path(tdir / 'fakedata/dir3').resolve().as_posix()
    ],
    'files': {
        Path(tdir / 'fakedata/vhdl0.vhdl').resolve().as_posix(): {
            'hdl': 'vhdl', 'lib': 'LIB'
        },
        Path(tdir / 'fakedata/dir1/vhdl1.vhdl').resolve().as_posix(): {
            'hdl': 'vhdl', 'lib': 'LIB'
        },
        Path(tdir / 'fakedata/dir2/vhdl2.vhdl').resolve().as_posix(): {
            'hdl': 'vhdl', 'lib': 'LIB'
        },
        Path(tdir / 'fakedata/dir3/vhdl3.vhdl').resolve().as_posix(): {
            'hdl': 'vhdl', 'lib': 'LIB'
        },
        Path(tdir / 'fakedata/vlog0.v').resolve().as_posix(): {
            'hdl': 'vlog'
        },
        Path(tdir / 'fakedata/dir1/vlog1.v').resolve().as_posix(): {
            'hdl': 'vlog'
        },
        Path(tdir / 'fakedata/dir2/vlog2.v').resolve().as_posix(): {
            'hdl': 'vlog'
        },
        Path(tdir / 'fakedata/dir3/vlog3.v').resolve().as_posix(): {
            'hdl': 'vlog'
        },
        Path(tdir / 'fakedata/slog0.sv').resolve().as_posix(): {
            'hdl': 'slog'
        },
        Path(tdir / 'fakedata/dir1/slog1.sv').resolve().as_posix(): {
            'hdl': 'slog'
        },
        Path(tdir / 'fakedata/dir2/slog2.sv').resolve().as_posix(): {
            'hdl': 'slog'
        },
        Path(tdir / 'fakedata/dir3/slog3.sv').resolve().as_posix(): {
            'hdl': 'slog'
        }
    },
    'top': 'TOPNAME',
    'constraints': {
        Path(tdir / 'fakedata/cons/all.xdc').resolve().as_posix(): 'all',
        Path(tdir / 'fakedata/cons/syn.xdc').resolve().as_posix(): 'syn',
        Path(tdir / 'fakedata/cons/par.xdc').resolve().as_posix(): 'par'
    },
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
    prj.add_cons(str(tdir / 'fakedata/cons/syn.xdc'), 'syn')
    prj.add_cons(str(tdir / 'fakedata/cons/par.xdc'), 'par')
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
