#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Libero.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

import re

from pyfpga.project import Project


class Libero(Project):
    """Class to support Libero."""

    def _make_prepare(self, steps):
        info = get_info(self.data.get('part', 'mpf100t-1-fcg484'))
        context = {
            'PROJECT': self.name or 'libero',
            'FAMILY': info['family'],
            'DEVICE': info['device'],
            'SPEED': info['speed'],
            'PACKAGE': info['package']
        }
        for step in steps:
            context[step] = 1
        if 'includes' in self.data:
            includes = []
            for include in self.data['includes']:
                includes.append(str(include))
            context['INCLUDES'] = ';'.join(includes)
        files = []
        if 'files' in self.data:
            for file in self.data['files']:
                if 'lib' in self.data['files'][file]:
                    lib = self.data['files'][file]['lib']
                    files.append(
                        f'create_links -library {lib} -hdl_source {file}'
                    )
                else:
                    files.append(f'create_links -hdl_source {file}')
        if 'constraints' in self.data:
            constraints = []
            for file in self.data['constraints']:
                if file.suffix == '.sdc':
                    constraints.append(f'create_links -sdc {file}')
                else:
                    constraints.append(f'create_links -io_pdc {file}')
            if constraints:
                context['CONSTRAINTS'] = " ".join(constraints)
        if files:
            context['FILES'] = '\n'.join(files)
        if 'top' in self.data:
            context['TOP'] = self.data['top']
        if 'defines' in self.data:
            defines = []
            for key, value in self.data['defines'].items():
                defines.append(f'{key}={value}')
            context['DEFINES'] = ' '.join(defines)
        if 'params' in self.data:
            params = []
            for key, value in self.data['params'].items():
                params.append(f'{key}={value}')
            context['PARAMS'] = ' '.join(params)
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        self._create_file('libero', 'tcl', context)
        return 'libero SCRIPT:libero.tcl'

    def _prog_prepare(self, bitstream, position):
        raise NotImplementedError('Libero programming not supported')


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
            speed = aux[1]
            package = aux[2]
        else:
            speed = aux[2]
            package = aux[1]
    else:
        raise ValueError(
            'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE'
        )
    # Finish
    return {
        'family': family, 'device': device, 'speed': speed, 'package': package
    }
