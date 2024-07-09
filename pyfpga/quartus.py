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
            'project': self.name or 'quartus',
            'part': self.data.get('part', '10M50SCE144I7G')
        }
        for step in steps:
            context[step] = 1
        context['includes'] = self.data.get('includes', None)
        context['files'] = self.data.get('files', None)
        context['constraints'] = self.data.get('constraints', None)
        context['top'] = self.data.get('top', None)
        context['defines'] = self.data.get('defines', None)
        context['params'] = self.data.get('params', None)
        if 'hooks' in self.data:
            context['precfg'] = self.data['hooks'].get('precfg', None)
            context['postcfg'] = self.data['hooks'].get('postcfg', None)
            context['presyn'] = self.data['hooks'].get('presyn', None)
            context['postsyn'] = self.data['hooks'].get('postsyn', None)
            context['prepar'] = self.data['hooks'].get('prepar', None)
            context['postpar'] = self.data['hooks'].get('postpar', None)
            context['presbit'] = self.data['hooks'].get('prebit', None)
            context['postbit'] = self.data['hooks'].get('postbit', None)
        self._create_file('quartus', 'tcl', context)
        return 'quartus_sh --script quartus.tcl'

    def _prog_prepare(self, bitstream, position):
        # sof: SRAM Object File
        # pof: Programming Object File
        if not bitstream:
            basename = self.name or 'quartus'
            bitstream = f'{basename}.sof'
        context = {'bitstream': bitstream, 'position': position}
        self._create_file('quartus-prog', 'tcl', context)
        return 'bash quartus-prog.sh'
