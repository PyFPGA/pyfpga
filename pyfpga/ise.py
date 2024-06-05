#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for ISE.
"""

# import re

from pyfpga.project import Project

_TEMPLATES = {
    'fpga': """setMode -bs
setCable -port auto
Identify -inferir
assignFile -p #POSITION# -file #BITSTREAM#
Program -p #POSITION#

quit
""",
    'spi': """setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffspi
addDesign -version 0 -name 0
addDeviceChain -index 0
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -spi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# -spionly -e -v -loadfpga

quit
""",
    'bpi': """setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffbpi
addDesign -version 0 -name 0
addDeviceChain -index 0
setAttribute -configdevice -attr flashDataWidth -value #WIDTH#
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -bpi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# \
-rs1 NONE -rs0 NONE -bpionly -e -v -loadfpga

quit
""",
    'detect': """setMode -bs
setCable -port auto
Identify -inferir
quit
""",
    'unlock': """cleancablelock
quit
"""
}

# pylint: disable=too-few-public-methods


class Ise(Project):
    """Class to support ISE projects."""

    tool = {
        'program': 'xtclsh',
        'command': 'xtclsh ise.tcl',
    }

    tool = {
        'def-part': 'xc7k160t-3-fbg484',
        'proj-ext': 'xise',
        'make-app': 'xtclsh',
        'make-opt': 'ise.tcl',
        'prog-app': 'impact',
        'prog-opt': '-batch ise-prog.impact',
        'binaries': ['bit']
    }

#     _DEVTYPES = ['fpga', 'spi', 'bpi', 'detect', 'unlock']

#     def set_part(self, part):
#         try:
#             device, speed, package =
#                 re.findall(r'(\w+)-(\w+)-(\w+)', part)[0]
#             if len(speed) > len(package):
#                 speed, package = package, speed
#             part = f'{device}-{speed}-{package}'
#         except IndexError:
#             raise ValueError(
#                 'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE-SPEED'
#             )
#         self.part['name'] = part
#         self.part['family'] = get_family(part)
#         self.part['device'] = device
#         self.part['package'] = package
#         self.part['speed'] = '-' + speed

#     def transfer(self, devtype, position, part, width, capture):
#         super().transfer(devtype, position, part, width, capture)
#         temp = _TEMPLATES[devtype]
#         if devtype not in ['detect', 'unlock']:
#             temp = temp.replace('#BITSTREAM#', self.bitstream)
#             temp = temp.replace('#POSITION#', str(position))
#             temp = temp.replace('#NAME#', part)
#             temp = temp.replace('#WIDTH#', str(width))
#         with open('ise-prog.impact', 'w', encoding='utf-8') as file:
#             file.write(temp)
#         return run(self._TRF_COMMAND, capture)


# def get_family(part):
#     """Get the Family name from the specified part name."""
#     part = part.lower()
#     families = {
#         r'xc7a\d+l': 'artix7l',
#         r'xc7a': 'artix7',
#         r'xc7k\d+l': 'kintex7l',
#         r'xc7k': 'kintex7',
#         r'xc3sd\d+a': 'spartan3adsp',
#         r'xc3s\d+a': 'spartan3a',
#         r'xc3s\d+e': 'spartan3e',
#         r'xc3s': 'spartan3',
#         r'xc6s\d+l': 'spartan6l',
#         r'xc6s': 'spartan6',
#         r'xc4v': 'virtex4',
#         r'xc5v': 'virtex5',
#         r'xc6v\d+l': 'virtex6l',
#         r'xc6v': 'virtex6',
#         r'xc7v\d+l': 'virtex7l',
#         r'xc7v': 'virtex7',
#         r'xc7z': 'zynq'
#     }
#     for key, value in families.items():
#         if re.match(key, part):
#             return value
#     return 'UNKNOWN'
