"""Test for template.tcl."""

import sys

from fpga.project import Project

prj = Project('tclsh')
prj.set_outdir('../build/tclsh')

tasks = ['prj', 'syn', 'imp', 'bit']

for i in range(0, 4):
    for j in range(i, 4):
        try:
            print(
                "* Testing generate from task '{}' to '{}'"
                .format(tasks[i], tasks[j])
            )
            prj.generate(to_task=tasks[j], from_task=tasks[i])
        except Exception as e:
            print('{} ({})'.format(type(e).__name__, e))
            sys.exit(1)
