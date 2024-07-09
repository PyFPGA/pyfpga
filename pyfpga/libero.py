#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Libero.
"""

import re

from pyfpga.project import Project


class Libero(Project):
    """Class to support Libero."""

    def _configure(self):
        tool = 'libero'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'{tool} SCRIPT:{tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = None
        self.conf['prog_cmd'] = None
        self.conf['prog_ext'] = None

    def _make_custom(self):
        info = get_info(self.data.get('part', 'mpf100t-1-fcg484'))
        self.data['family'] = info['family']
        self.data['device'] = info['device']
        self.data['speed'] = info['speed']
        self.data['package'] = info['package']

    def _prog_custom(self):
        raise NotImplementedError('Libero programming not supported')


# pylint: disable=duplicate-code

def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dictionary with the keys family, device, speed and package
    """
    part = part.lower()
    # Looking for the family
    family = None
    families = {
        r'm2s': 'SmartFusion2',
        r'm2gl': 'Igloo2',
        r'rt4g': 'RTG4',
        r'mpf': 'PolarFire',
        r'a2f': 'SmartFusion',
        r'afs': 'Fusion',
        r'aglp': 'IGLOO+',
        r'agle': 'IGLOOE',
        r'agl': 'IGLOO',
        r'a3p\d+l': 'ProAsic3L',
        r'a3pe': 'ProAsic3E',
        r'a3p': 'ProAsic3'
    }
    for key, value in families.items():
        if re.match(key, part):
            family = value
            break
    # Looking for the device and package
    device = None
    speed = None
    package = None
    aux = part.split('-')
    if len(aux) == 2:
        device = aux[0]
        speed = 'STD'
        package = aux[1]
    elif len(aux) == 3:
        device = aux[0]
        if len(aux[1]) < len(aux[2]):
            speed = f'-{aux[1]}'
            package = aux[2]
        else:
            speed = f'-{aux[2]}'
            package = aux[1]
    else:
        raise ValueError(
            'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE'
        )
    # Finish
    return {
        'family': family, 'device': device, 'speed': speed, 'package': package
    }
