#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Quartus.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

from pyfpga.project import Project


class Quartus(Project):
    """Class to support Quartus projects."""

    def _make_prepare(self, steps):
        context = {
            'PROJECT': self.name or 'quartus',
            'PART': self.data.get('part', '10M50SCE144I7G')
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
        self._create_file('quartus', 'tcl', context)
        return 'quartus_sh --script quartus.tcl'

    def _prog_prepare(self, bitstream, position):
        # sof: SRAM Object File
        # pof: Programming Object File
        if not bitstream:
            basename = self.name or 'quartus'
            bitstream = f'{basename}.sof'
        context = {'BITSTREAM': bitstream, 'POSITION': position}
        self._create_file('quartus-prog', 'tcl', context)
        return 'bash quartus-prog.sh'
