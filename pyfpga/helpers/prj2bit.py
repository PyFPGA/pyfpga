#!/usr/bin/env python3
#
# Copyright (C) 2020 INTI
# Copyright (C) 2020 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
A CLI helper utility to deal with a vendor FPGA Project file.
"""

import argparse
import logging
import os
import sys

from fpga import __version__ as version
from fpga.project import Project
from fpga.tool import TASKS

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.INFO


def main():
    """Solves the main functionality of this helper."""

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='v{}'.format(version)
    )

    parser.add_argument(
        'project',
        metavar='PRJFILE',
        help='a vendor project file'
    )

    parser.add_argument(
        '--run',
        metavar='TASK',
        choices=TASKS[1:len(TASKS)],
        default='bit',
        help='task to perform [{}] ({})'.format(
            'bit', " | ".join(TASKS[1:len(TASKS)])
        )
    )

    parser.add_argument(
        '--clean',
        action='store_true',
        help='clean the generated project files'
    )

    args = parser.parse_args()

    # Detecting a Project file

    tool_per_ext = {
        '.xise': 'ise',
        '.prjx': 'libero',
        '.qpf': 'quartus',
        '.xpr': 'vivado'
    }

    if not os.path.exists(args.project):
        sys.exit('Project file not found')

    outdir = os.path.dirname(args.project)
    project, extension = os.path.splitext(args.project)
    project = os.path.basename(project)

    tool = ''
    if extension in tool_per_ext:
        tool = tool_per_ext[extension]
        print('{} Project file found.'.format(tool))
    else:
        sys.exit('Unknown Project file extension')

    # Solving with PyFPGA

    prj = Project(tool, project=project, relative_to_script=False)
    prj.set_outdir(outdir)

    prj.set_top(project)

    try:
        if args.clean:
            prj.clean()
        else:
            prj.generate(args.run, 'syn')
    except RuntimeError:
        logging.error('{} not found'.format(tool))
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
