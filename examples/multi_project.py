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
        'part': 'FPGA1',
        'files': ['path1_1/*.vhdl', 'path1_2/*.vhdl'],
        'top': 'top1'
     },
    'example2': {
        'tool': 'vivado',
        'part': 'FPGA2',
        'files': ['path2_1/*.vhdl', 'path2_2/*.vhdl'],
        'top': 'top2'
     },
    'example3': {
        'tool': 'quartus',
        'part': 'FPGA3',
        'files': ['path3/*.v'],
        'top': 'top3'
     },
}

for project in sorted(PROJECTS.keys()):
    PRJ = Project(PROJECTS[project]['tool'], project)
    PRJ.set_outdir('../build/projects/%s' % project)
    PRJ.set_part(PROJECTS[project]['part'])
    for files in PROJECTS[project]['files']:
        PRJ.add_files(files)
    PRJ.set_part(PROJECTS[project]['top'])
    try:
        PRJ.generate()
    except:
        print('There was an error with the project %s' % project)
