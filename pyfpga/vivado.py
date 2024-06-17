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
        #     if { $LIBRARY != "work" } {
        #         add_files $FILE
        #         set_property library $LIBRARY [get_files $FILE]
        #     } else {
        #         add_files $FILE
        if 'arch' in self.data:
            context['ARCH'] = self.data['arch']
        if 'defines' in self.data:
            defines = []
            for key, value in self.data['defines'].items():
                defines.append(f'{key}={value}')
            context['DEFINES'] = ' '.join(defines)
        if 'includes' in self.data:
            includes = []
            for include in self.data['includes']:
                includes.append(str(include))
            context['INCLUDES'] = ' '.join(includes)
        if 'params' in self.data:
            params = []
            for key, value in self.data['params'].items():
                params.append(f'{key}={value}')
            context['PARAMS'] = ' '.join(params)
        self._create_file('vivado', 'tcl', context)

    def _prog_prepare(self):
        # binaries = ['bit']
        self.tool['prog-app'] = 'vivado'
        self.tool['prog-cmd'] = (
            'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
        )
