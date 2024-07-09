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
            'project': self.name or 'vivado',
            'part': self.data.get('part', 'xc7k160t-3-fbg484')
        }
        context['steps'] = steps
        context['includes'] = self.data.get('includes', None)
        context['files'] = self.data.get('files', None)
        context['constraints'] = self.data.get('constraints', None)
        context['top'] = self.data.get('top', None)
        context['defines'] = self.data.get('defines', None)
        context['params'] = self.data.get('params', None)
        context['hooks'] = self.data.get('hooks', None)
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
