#
# Copyright (C) 2019-2024 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches

from pyfpga.project import Project


class Vivado(Project):
    """Class to support Vivado projects."""

    def _make_prepare(self, steps):
        context = {
            'PROJECT': self.name or 'vivado',
            'PART': self.data.get('part', 'xc7k160t-3-fbg484')
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
        self._create_file('vivado', 'tcl', context)
        return 'vivado -mode batch -notrace -quiet -source vivado.tcl'

    def _prog_prepare(self, bitstream, position):
        _ = position  # Not needed
        if not bitstream:
            basename = self.name or 'vivado'
            bitstream = f'{basename}.bit'
        context = {'BITSTREAM': bitstream}
        self._create_file('vivado-prog', 'tcl', context)
        return 'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
