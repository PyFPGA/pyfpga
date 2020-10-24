"""PyFPGA Multi Project example.

The main idea of a multi-project is to manage more than one project with the
same script.

Typically, you would want to change some files and the top-level, sometimes
the part (if different boards are used) and, less probable, maybe the tool.
"""

import logging

from fpga.project import Project

logging.basicConfig()

PROJECTS = {
    'vivado-prj': {
        'tool': 'vivado',
        'part': 'xc7k70t-3-fbg484',
        'files': [
            ('../../hdl/blinking.vhdl', 'vhdl', 'examples'),
            ('../../hdl/examples_pkg.vhdl', 'vhdl', 'examples'),
            '../../hdl/top.vhdl'
        ],
        'top': 'Top'
    },
    'ise-prj': {
        'tool': 'ise',
        'part': 'xc6slx9-2-csg324',
        'files': ['../../hdl/blinking.vhdl'],
        'top': 'Blinking'
    },
    'quartus-prj': {
        'tool': 'quartus',
        'part': '5CEBA2F17A7',
        'paths': [
            '../../hdl/headers1',
            '../../hdl/headers2'
        ],
        'files': ['../../hdl/blinking.v', '../../hdl/top.v'],
        'top': 'Top'
    },
}

for project in sorted(PROJECTS.keys()):
    PRJ = Project(PROJECTS[project]['tool'], project)
    PRJ.set_outdir('../../build/multi/projects/%s' % project)
    PRJ.set_part(PROJECTS[project]['part'])
    # Only if there are Verilog Included Files
    if 'paths' in PROJECTS[project]:
        for path in PROJECTS[project]['paths']:
            PRJ.add_path(path)
    # A VHDL into a PACKAGE were specified as a tuple
    for file in PROJECTS[project]['files']:
        if type(file) is tuple:
            PRJ.add_files(file[0], file[1], file[2])
        else:
            PRJ.add_files(file)
    # Specifying the Top-level
    PRJ.set_top(PROJECTS[project]['top'])
    # Running implementation
    try:
        PRJ.generate(to_task='imp')
    except RuntimeError:
        print('ERROR:generate:{} not found'.format(PROJECTS[project]['tool']))
