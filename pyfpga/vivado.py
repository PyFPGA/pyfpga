#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

from pyfpga.project import Project


class Vivado(Project):
    """Class to support Vivado projects."""

    def _make_prepare(self, steps):
        self.tool['make-app'] = 'vivado'
        self.tool['make-cmd'] = (
            'vivado -mode batch -notrace -quiet -source vivado.tcl'
        )
        context = {
            'PROJECT': self.name or 'vivado',
            'PART': self.data.get('part', 'xc7k160t-3-fbg484'),
            'TOP': self.data.get('top', 'top')
        }
        for step in steps:
            context[step] = 1
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        # FILES
        # DEFINES
        # INCLUDES
        # PARAMS
        # ARCH
        self._create_file('vivado', 'tcl', context)

    def _prog_prepare(self):
        # binaries = ['bit']
        self.tool['prog-app'] = 'vivado'
        self.tool['prog-cmd'] = (
            'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
        )
