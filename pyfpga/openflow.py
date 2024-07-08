#
# Copyright (C) 2020-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for an Open Source development flow.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

from pyfpga.project import Project


class Openflow(Project):
    """Class to support Open Source tools."""

    def _make_prepare(self, steps):
        info = get_info(self.data.get('part', 'hx8k-ct256'))
        context = {
            'PROJECT': self.name or 'openflow',
            'FAMILY': info['family'],
            'DEVICE': info['device'],
            'PACKAGE': info['package']
        }
        for step in steps:
            context[step] = 1
        context['INCLUDES'] = self.data.get('includes', None)
        context['FILES'] = self.data.get('files', None)
        context['CONSTRAINTS'] = self.data.get('constraints', None)
        context['TOP'] = self.data.get('top', None)
        context['DEFINES'] = self.data.get('defines', None)
        context['PARAMS'] = self.data.get('params', None)
        if 'hooks' in self.data:
            context['PRECFG'] = self.data['hooks'].get('precfg', None)
            context['POSTCFG'] = self.data['hooks'].get('postcfg', None)
            context['PRESYN'] = self.data['hooks'].get('presyn', None)
            context['POSTSYN'] = self.data['hooks'].get('postsyn', None)
            context['PREPAR'] = self.data['hooks'].get('prepar', None)
            context['POSTPAR'] = self.data['hooks'].get('postpar', None)
            context['PRESBIT'] = self.data['hooks'].get('prebit', None)
            context['POSTBIT'] = self.data['hooks'].get('postbit', None)
        self._create_file('openflow', 'sh', context)
        return 'bash openflow.sh'

    def _prog_prepare(self, bitstream, position):
        _ = position  # Not needed
        if not bitstream:
            basename = self.name or 'openflow'
            bitstream = f'{basename}.bit'
        context = {'BITSTREAM': bitstream}
        self._create_file('openflow-prog', 'sh', context)
        return 'bash openflow-prog.sh'


def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dictionary with the keys family, device and package
    """
    part = part.lower()
    # Looking for the family
    family = None
    families = [
        # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
        'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
        'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
    ]
    for item in families:
        if part.startswith(item):
            family = item
            break
    families = [
        # From <nextpnr>/ice40/main.cc
        'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
        'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
    ]
    if part.startswith(tuple(families)):
        family = 'ice40'
    families = [
        # From <nextpnr>/ecp5/main.cc
        '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
        'um5g-25k', 'um5g-45k', 'um5g-85k'
    ]
    if part.startswith(tuple(families)):
        family = 'ecp5'
    # Looking for the device and package
    device = None
    package = None
    aux = part.split('-')
    if len(aux) == 2:
        device = aux[0]
        package = aux[1]
    elif len(aux) == 3:
        device = f'{aux[0]}-{aux[1]}'
        package = aux[2]
    else:
        raise ValueError('Part must be DEVICE-PACKAGE')
    if family in ['lp4k', 'hx4k']:  # See http://www.clifford.at/icestorm
        device = device.replace('4', '8')
        package += ":4k"
    if family == 'ecp5':
        package = package.upper()
    # Finish
    return {'family': family, 'device': device, 'package': package}
