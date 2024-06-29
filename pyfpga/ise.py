#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for ISE.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

import re

from pathlib import Path
from pyfpga.project import Project


class Ise(Project):
    """Class to support ISE projects."""

    def _make_prepare(self, steps):
        info = get_info(self.data.get('part', 'xc7k160t-3-fbg484'))
        context = {
            'PROJECT': self.name or 'ise',
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
            context['INCLUDES'] = '|'.join(includes)
        files = []
        if 'files' in self.data:
            for file in self.data['files']:
                if 'lib' in self.data['files']:
                    lib = self.data['files'][file]['lib']
                    files.append(f'lib_vhdl new {lib}')
                    files.append(f'xfile add {file} -lib_vhdl {lib}')
                else:
                    files.append(f'xfile add {file}')
        if 'constraints' in self.data:
            constraints = []
            for file in self.data['constraints']:
                files.append(f'xfile add {file}')
                if file.suffix == '.xcf':
                    constraints.append(str(file))
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
            context['DEFINES'] = ' | '.join(defines)
        if 'params' in self.data:
            params = []
            for key, value in self.data['params'].items():
                params.append(f'{key}={value}')
            context['PARAMS'] = ' '.join(params)
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        self._create_file('ise', 'tcl', context)
        return 'xtclsh ise.tcl'

    def _prog_prepare(self, bitstream, position):
        if not bitstream:
            basename = self.name or 'ise'
            bitstream = Path(self.odir).resolve() / f'{basename}.bit'
        context = {'BITSTREAM': bitstream, 'POSITION': position}
        self._create_file('vivado-prog', 'tcl', context)
        return 'impact -batch impact-prog'

    def add_slog(self, pathname):
        """Add System Verilog file/s."""
        raise NotImplementedError('ISE does not support SystemVerilog')

#     _DEVTYPES = ['fpga', 'spi', 'bpi', 'detect', 'unlock']

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


def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dictionary with the keys family, device, speed and package
    """
    part = part.lower()
    # Looking for the family
    family = None
    families = {
        r'xc7a\d+l': 'artix7l',
        r'xc7a': 'artix7',
        r'xc7k\d+l': 'kintex7l',
        r'xc7k': 'kintex7',
        r'xc3sd\d+a': 'spartan3adsp',
        r'xc3s\d+a': 'spartan3a',
        r'xc3s\d+e': 'spartan3e',
        r'xc3s': 'spartan3',
        r'xc6s\d+l': 'spartan6l',
        r'xc6s': 'spartan6',
        r'xc4v': 'virtex4',
        r'xc5v': 'virtex5',
        r'xc6v\d+l': 'virtex6l',
        r'xc6v': 'virtex6',
        r'xc7v\d+l': 'virtex7l',
        r'xc7v': 'virtex7',
        r'xc7z': 'zynq'
    }
    for key, value in families.items():
        if re.match(key, part):
            family = value
            break
    # Looking for the device, package and speed
    device = None
    speed = None
    package = None
    aux = part.split('-')
    if len(aux) == 3:
        device = aux[0]
        if len(aux[1]) < len(aux[2]):
            speed = aux[1]
            package = aux[2]
        else:
            speed = aux[2]
            package = aux[1]
    else:
        raise ValueError(
            'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE-SPEED'
        )
    # Finish
    return {
        'family': family, 'device': device, 'speed': speed, 'package': package
    }
