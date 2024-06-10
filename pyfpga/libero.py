#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Libero.
"""

# import re

from pyfpga.project import Project


class Libero(Project):
    """Class to support Libero."""

    def __init__(self, name='libero', odir='results'):
        super().__init__(name=name, odir=odir)
        self.set_part('mpf100t-1-fcg484')

    def _make_prepare(self, steps):
        self.tool['make-app'] = 'libero'
        self.tool['make-cmd'] = 'libero SCRIPT:libero.tcl'

    def _prog_prepare(self):
        # binaries = ['bit']
        self.tool['prog-app'] = ''
        self.tool['prog-cmd'] = ''

#     def set_part(self, part):
#         try:
#             device, speed, package =
#                 re.findall(r'(\w+)-(\w+)-*(\w*)', part)[0]
#             if len(speed) > len(package):
#                 speed, package = package, speed
#             if speed == '':
#                 speed = 'STD'
#             part = f'{device}-{speed}-{package}'
#         except IndexError:
#             raise ValueError(
#                 'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE'
#             )
#         self.part['name'] = part
#         self.part['family'] = get_family(part)
#         self.part['device'] = device
#         self.part['package'] = package
#         self.part['speed'] = 'STD' if speed == 'STD' else '-' + speed

#     def transfer(self, devtype, position, part, width, capture):
#         super().transfer(devtype, position, part, width, capture)
#         raise NotImplementedError('transfer(libero)')

# def get_family(part):
#     """Get the Family name from the specified part name."""
#     part = part.lower()
#     families = {
#         r'm2s': 'SmartFusion2',
#         r'm2gl': 'Igloo2',
#         r'rt4g': 'RTG4',
#         r'mpf': 'PolarFire',
#         r'a2f': 'SmartFusion',
#         r'afs': 'Fusion',
#         r'aglp': 'IGLOO+',
#         r'agle': 'IGLOOE',
#         r'agl': 'IGLOO',
#         r'a3p\d+l': 'ProAsic3L',
#         r'a3pe': 'ProAsic3E',
#         r'a3p': 'ProAsic3'
#     }
#     for key, value in families.items():
#         if re.match(key, part):
#             return value
#     return 'UNKNOWN'
