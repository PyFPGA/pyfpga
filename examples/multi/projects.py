"""PyFPGA Multi Project example.

The main idea of a multi-project is to manage more than one project with the
same script.
"""

import logging

from fpga.multi import Multi

logging.basicConfig()

PROJECTS = {
    'vivado-prj': {
        'tool': 'vivado',
        'outdir': '../../build/multi/projects/vivado',
        'part': 'xc7k70t-3-fbg484',
        'vhdl': [
            ['../../hdl/blinking.vhdl', 'examples'],
            ['../../hdl/examples_pkg.vhdl', 'examples'],
            '../../hdl/top.vhdl'
        ],
        'top': 'Top'
    },
    'ise-prj': {
        'tool': 'ise',
        'outdir': '../../build/multi/projects/ise',
        'part': 'xc6slx9-2-csg324',
        'vhdl': [
            '../../hdl/blinking.vhdl'
        ],
        'top': 'Blinking'
    },
    'quartus-prj': {
        'tool': 'quartus',
        'outdir': '../../build/multi/projects/quartus',
        'part': '5CEBA2F17A7',
        'paths': [
            '../../hdl/headers1',
            '../../hdl/headers2'
        ],
        'verilog': [
            '../../hdl/blinking.v',
            '../../hdl/top.v'
        ],
        'top': 'Top'
    }
}

Multi(PROJECTS).generate('syn')
