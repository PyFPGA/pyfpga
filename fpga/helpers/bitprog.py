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
A CLI helper utility to transfer a bitstream to a supported device.
"""

import argparse
import logging

from fpga import __version__ as version
from fpga.project import Project, TOOLS, COMBINED_TOOLS
from fpga.tool import MEMWIDTHS


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
    " | ".join(TOOLS + COMBINED_TOOLS),
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
        choices=TOOLS+COMBINED_TOOLS,
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
    elif args.run == 'detect':
        devtype = 'detect'
    else:  # args.run == 'unlock'
        devtype = 'unlock'

    # pylint: disable=broad-except
    # pylint: disable=invalid-name
    try:
        prj.transfer(devtype, args.position, args.memname, args.width)
    except Exception as e:
        logging.warning('%s (%s)', type(e).__name__, e)


if __name__ == "__main__":
    main()
