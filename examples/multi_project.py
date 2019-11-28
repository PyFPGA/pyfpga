"""PyFPGA Multi Project example.

The main idea of a multi-project is to manage more than one project with the
same script.

Typically, you would want to change some files and the top level, sometimes
the part (if different boards are used) and less probable, maybe the tool.
"""

from fpga.project import Project

PROJECTS = {
    'example1': {
        'tool': 'vivado',
        'part': 'xc7s6cpga196-2',
        'files': [
            ['hdl/blinking.vhdl', 'examples'],
            ['hdl/examples_pkg.vhdl', 'examples'],
            ['hdl/top.vhdl']
        ],
        'top': 'Top'
    },
    'example2': {
        'tool': 'vivado',
        'part': 'xc7k70t-3-fbg484',
        'files': [
            ['hdl/*.vhdl', 'examples']
        ],
        'top': 'Top'
    },
    'example3': {
        'tool': 'quartus',
        'part': '5CEBA2F17A7',
        'files': [
            ['hdl/blinking.vhdl', 'examples'],
            ['hdl/examples_pkg.vhdl', 'examples'],
            ['hdl/top.vhdl', 'examples']
        ],
        'top': 'Top'
    },
}

for project in sorted(PROJECTS.keys()):
    PRJ = Project(PROJECTS[project]['tool'], project)
    PRJ.set_outdir('../build/multi-project/%s' % project)
    PRJ.set_part(PROJECTS[project]['part'])
    for file in PROJECTS[project]['files']:
        if len(file) > 1:
            PRJ.add_files(file[0], file[1])
        else:
            PRJ.add_files(file[0])
    PRJ.set_top(PROJECTS[project]['top'])
    try:
        PRJ.generate(to_task='imp')
    except Exception as e:
        print('There was an error with the project %s' % project)
        print('{} ({})'.format(type(e).__name__, e))
