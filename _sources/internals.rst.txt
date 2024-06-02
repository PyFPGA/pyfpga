Internals
=========

Underlying tool steps
---------------------

.. code-block::

    create project
    config project
    part
    precfg hook
    params
    defines
    includes
    files
    arch
    top
    postcfg hook
    close project

    open project
    presyn hook
    synthesis
    postsyn hook
    prepar hook
    place_and_route
    postpar hook
    prebit hook
    bitstream
    postbit hook
    close project

Internal data structure
-----------------------

.. code-block::

    data = {
        'part': 'PARTNAME',
        'includes': ['DIR1', 'DIR2', 'DIR3'],
        'files': {
            'file1': {'type': 'vhdl', 'options': 'OPT1', 'library': 'LIB1'},
            'file2': {'type': 'vlog', 'options': 'OPT2', 'library': None},
            'file3': {'type': 'slog', 'options': 'OPT3', 'library': None},
            'file4': {'type': 'cons', 'options': 'OPT4', 'library': None}
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
