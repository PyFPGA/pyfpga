#!/usr/bin/env python3
#
# Copyright (C) 2020 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to go from FPGA design files to a bitstream.
"""

import argparse
import logging
import sys

from fpga import __version__ as version
from fpga.project import Project, TOOLS
from fpga.tool import TASKS

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.INFO

EPILOGUE = """
Supported values of arguments with choices:
* TOOL = {}
* TASK = {}

Notes:
* PATH and FILE must be relative to the execution directory.
* The default PART name and how to specify it depends on the selected TOOL.
* More than one '--file', '--include' or '--param' arguments can be specified.
""".format(
    " | ".join(TOOLS),
    " | ".join(TASKS[1:len(TASKS)])
)


def main():
    """Solves the main functionality of this helper."""

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=EPILOGUE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='v{}'.format(version)
    )

    parser.add_argument(
        'top',
        metavar='TOPFILE',
        help='a top-level file'
    )

    parser.add_argument(
        '-t', '--tool',
        metavar='TOOL',
        default='vivado',
        choices=TOOLS,
        help='backend tool to be used [vivado]'
    )

    parser.add_argument(
        '-o', '--outdir',
        metavar='PATH',
        default='temp',
        help='where to generate files [temp]'
    )

    parser.add_argument(
        '-p', '--part',
        metavar='PART',
        help='the target device'
    )

    parser.add_argument(
        '-f', '--file',
        metavar='FILE[,PACKAGE]',
        action='append',
        help='add a design file (specifying an optional VHDL package)'
    )

    parser.add_argument(
        '-i', '--include',
        metavar='PATH',
        action='append',
        help='specify where to search Verilog included files'
    )

    parser.add_argument(
        '--param',
        metavar=('GENERIC/PARAMETER', 'VALUE'),
        action='append',
        nargs=2,
        help='set the value of a generic/parameter of the top-level'
    )

    parser.add_argument(
        '--run',
        metavar='TASK',
        choices=TASKS[1:len(TASKS)],
        default='bit',
        help='task to perform [{}]'.format('bit')
    )

    args = parser.parse_args()

    # Solving with PyFPGA

    prj = Project(args.tool, relative_to_script=False)
    prj.set_outdir(args.outdir)

    if args.part is not None:
        prj.set_part(args.part)

    if args.include is not None:
        for include in args.include:
            prj.add_vlog_include(include)

    if args.file is not None:
        for file in args.file:
            file = file.split(',')
            if len(file) > 1:
                prj.add_files(file[0], library=file[1])
            else:
                prj.add_files(file[0])

    if args.param is not None:
        for param in args.param:
            prj.add_param(param[0], param[1])

    prj.add_files(args.top)
    prj.set_top(args.top)

    try:
        prj.generate(args.run)
    except RuntimeError:
        logging.error('{} not found'.format(args.tool))
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
