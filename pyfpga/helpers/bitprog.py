#!/usr/bin/env python3
#
# Copyright (C) 2020-2025 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to transfer a bitstream to a supported device.
"""

import argparse
import sys

from pathlib import Path
from pyfpga import __version__ as version
from pyfpga.factory import Factory, TOOLS
from pyfpga.project import STEPS

tools = list(TOOLS.keys())
positions = range(1, 10)

EPILOGUE = f"""
Supported values of arguments with choices:
* TOOL = {'|'.join(tools)}
* POSITION = {'|'.join(map(str, positions))}
"""


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
        version=f'v{version}'
    )

    parser.add_argument(
        '-t', '--tool',
        metavar='TOOL',
        default='vivado',
        choices=tools,
        help='backend tool to be used [vivado]'
    )

    parser.add_argument(
        '-p', '--position',
        metavar='POSITION',
        choices=positions,
        type=int,
        default=1,
        help='the device position into the JTAG chain [1]'
    )

    parser.add_argument(
        '-o', '--odir',
        metavar='PATH',
        default='results',
        help='where to generate files [results]'
    )

    parser.add_argument(
        'bit',
        metavar='BITFILE',
        help='a bitstream file'
    )

    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # Solving with PyFPGA
    # -------------------------------------------------------------------------

    prj = Factory(args.tool, odir=args.odir)

    try:
        prj.prog(args.bit, args.position)
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
