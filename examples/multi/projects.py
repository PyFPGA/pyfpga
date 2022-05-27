"""PyFPGA Multi Project example.

The main idea of a multi-project is to manage more than one project with the
same script.
"""

import logging

from fpga.project import Project

logging.basicConfig()

PROJECTS = {
    'prj1': Project(
        'vivado',
        'vivado-prj',
        meta={
            'outdir': '../../build/multi/projects/vivado',
            'part': 'xc7k70t-3-fbg484',
            'vhdl': [
                ['../../hdl/blinking.vhdl', 'examples'],
                ['../../hdl/examples_pkg.vhdl', 'examples'],
                '../../hdl/top.vhdl'
                ],
            'top': 'Top'
        }
    ),
    'prj2': Project(
        'ise',
        'ise-prj',
        meta={
            'outdir': '../../build/multi/projects/ise',
            'part': 'xc6slx9-2-csg324',
            'vhdl': [
                '../../hdl/blinking.vhdl'
                ],
            'top': 'Blinking'
        }
    ),
    'prj3': Project(
        'quartus',
        'qurtus-prj',
        meta={
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
    )
}

for prj in PROJECTS:
    PROJECTS[prj].generate('syn')
