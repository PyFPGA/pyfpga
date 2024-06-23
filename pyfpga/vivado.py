#
# Copyright (C) 2019-2024 Rodrigo A. Melo
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
        if 'includes' in self.data:
            includes = []
            for include in self.data['includes']:
                includes.append(str(include))
            context['INCLUDES'] = ' '.join(includes)
        files = []
        if 'files' in self.data:
            for file in self.data['files']:
                files.append(f'add_file {file}')
            for file in self.data['files']:
                if 'lib' in self.data['files'][file]:
                    lib = self.data['files'][file]['lib']
                    files.append(
                        f'set_property library {lib} [get_files {file}]'
                    )
        if 'constraints' in self.data:
            for file in self.data['constraints']:
                files.append(f'add_file -fileset constrs_1 {file}')
            for file in self.data['constraints']:
                if self.data['constraints'][file] == 'syn':
                    prop = 'USED_IN_IMPLEMENTATION FALSE'
                if self.data['constraints'][file] == 'syn':
                    prop = 'USED_IN_SYNTHESIS FALSE'
                if self.data['constraints'][file] != 'all':
                    files.append(f'set_property {prop} [get_files {file}]')
            first = next(iter(self.data['constraints']))
            prop = f'TARGET_CONSTRS_FILE {first}'
            files.append(f'set_property {prop} [current_fileset -constrset]')
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
        if 'arch' in self.data:
            context['ARCH'] = self.data['arch']
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        self._create_file('vivado', 'tcl', context)
        return 'vivado -mode batch -notrace -quiet -source vivado.tcl'

    def _prog_prepare(self):
        # binaries = ['bit']
        return 'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
