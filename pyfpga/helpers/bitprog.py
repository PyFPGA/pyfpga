#!/usr/bin/env python3
#
# Copyright (C) 2020 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A CLI helper utility to transfer a bitstream to a supported device.
"""

import argparse
import logging
import sys

from fpga import __version__ as version
from fpga.project import Project, TOOLS
from fpga.tool import MEMWIDTHS

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.INFO

DEVS = ['fpga', 'spi', 'bpi']
POSITIONS = range(1, 10)
ACTIONS = ['program', 'detect', 'unlock']

EPILOGUE = """
Supported values of arguments with choices:
* TOOL = {}
* DEVTYPE = {}
* POSITIONS = {}
* MEMWIDTH = {}
* ACTION = {}
""".format(
    " | ".join(TOOLS),
    " | ".join(DEVS),
    " | ".join(str(x) for x in POSITIONS),
    " | ".join(str(x) for x in MEMWIDTHS),
    " | ".join(ACTIONS)
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
        'bit',
        metavar='BITFILE',
        nargs='?',
        help='a bitstream file'
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
        '-d', '--device',
        metavar='DEVTYPE',
        choices=DEVS,
        default=DEVS[0],
        help='the target device type [{}]'.format(DEVS[0])
    )

    parser.add_argument(
        '-p', '--position',
        metavar='POSITION',
        choices=POSITIONS,
        type=int,
        default=1,
        help='the device position into the JTAG chain [1]'
    )

    parser.add_argument(
        '-m', '--memname',
        metavar='MEMNAME',
        default='',
        help='memory name if spi or bpi selected'
    )

    parser.add_argument(
        '-w', '--width',
        metavar='MEMWIDTH',
        choices=MEMWIDTHS,
        type=int,
        default=1,
        help='memory width if spi or bpi selected [1]'
    )

    parser.add_argument(
        '--run',
        metavar='ACTION',
        choices=ACTIONS,
        default=ACTIONS[0],
        help='action to perform [{}]'.format(ACTIONS[0])
    )

    args = parser.parse_args()

    # Solving with PyFPGA

    prj = Project(args.tool, relative_to_script=False)
    prj.set_outdir(args.outdir)

    if args.run == 'program':
        devtype = args.device
        prj.set_bitstream(args.bit)
    elif args.run == 'detect':
        devtype = 'detect'
    else:  # args.run == 'unlock'
        devtype = 'unlock'

    try:
        prj.transfer(devtype, args.position, args.memname, args.width)
    except RuntimeError:
        logging.error('{} not found'.format(args.tool))
    except Exception as e:
        sys.exit('{} ({})'.format(type(e).__name__, e))


if __name__ == "__main__":
    main()
