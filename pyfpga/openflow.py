#
# Copyright (C) 2020-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for an Open Source development flow.
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code

from pathlib import Path
from pyfpga.project import Project


class Openflow(Project):
    """Class to support Open Source tools."""

    def _make_prepare(self, steps):
        context = {
            'PROJECT': self.name or 'openflow',
            'PART': self.data.get('part', 'hx8k-ct256'),
            'FAMILY': 'ice40',
            'DEVICE': 'hx8k',
            'PACKAGE': 'tq144:4k'
        }
        for step in steps:
            context[step] = 1
        if 'includes' in self.data:
            includes = []
            for include in self.data['includes']:
                includes.append(f'-I{str(include)}')
            context['INCLUDES'] = ' '.join(includes)
        files = []
        if 'files' in self.data:
            for file in self.data['files']:
                files.append(f'read_verilog -defer {file}')
        if files:
            context['VLOGS'] = '\n'.join(files)
#            for file in self.data['files']:
#                if 'lib' in self.data['files'][file]:
#                    lib = self.data['files'][file]['lib']
#                    files.append(
#                        f'set_property library {lib} [get_files {file}]'
#                    )
        if 'constraints' in self.data:
            constraints = []
            for constraint in self.data['constraints']:
                constraints.append(str(constraint))
            context['CONSTRAINTS'] = ' '.join(constraints)
        if 'top' in self.data:
            context['TOP'] = self.data['top']
        if 'defines' in self.data:
            defines = []
            for key, value in self.data['defines'].items():
                defines.append(f'-D{key}={value}')
            context['DEFINES'] = ' '.join(defines)
        if 'params' in self.data:
            params = []
            for key, value in self.data['params'].items():
                params.append(f'-set {key} {value}')
            context['PARAMS'] = ' '.join(params)
        if 'hooks' in self.data:
            for stage in self.data['hooks']:
                context[stage.upper()] = '\n'.join(self.data['hooks'][stage])
        self._create_file('openflow', 'sh', context)
        return 'bash openflow.sh'

    def _prog_prepare(self, bitstream, position):
        _ = position
        if not bitstream:
            basename = self.name or 'openflow'
            bitstream = Path(self.odir).resolve() / f'{basename}.bit'
        context = {'BITSTREAM': bitstream}
        self._create_file('openflow-prog', 'sh', context)
        return 'bash openflow-prog.sh'

#     def set_part(self, part):
#         self.part['name'] = part
#         self.part['family'] = get_family(part)
#         if self.part['family'] in ['ice40', 'ecp5']:
#             aux = part.split('-')
#             if len(aux) == 2:
#                 self.part['device'] = aux[0]
#                 self.part['package'] = aux[1]
#             elif len(aux) == 3:
#                 self.part['device'] = f'{aux[0]}-{aux[1]}'
#                 self.part['package'] = aux[2]
#             else:
#                 raise ValueError('Part must be DEVICE-PACKAGE')
#             if self.part['device'].endswith('4k'):
#                 # See http://www.clifford.at/icestorm/
#                 self.part['device'] = self.part['device'].replace('4', '8')
#                 self.part['package'] += ":4k"

#     def _create_gen_script(self, tasks):
#         # Verilog includes
#         paths = []
#         for path in self.paths:
#             paths.append(f'verilog_defaults -add -I{path}')
#         # Files
#         constraints = []
#         verilogs = []
#         vhdls = []
#         for file in self.files['vhdl']:
#             lib = ''
#             if file[1] is not None:
#                 lib = f'--work={file[1]}'
#             vhdls.append(f'{self.tools["ghdl"]} -a $FLAGS {lib} {file[0]}')
#         for file in self.files['verilog']:
#             if file[0].endswith('.sv'):
#                 verilogs.append(f'read_verilog -sv -defer {file[0]}')
#             else:
#                 verilogs.append(f'read_verilog -defer {file[0]}')
#         for file in self.files['constraint']:
#             constraints.append(file[0])
#         if len(vhdls) > 0:
#             verilogs = [f'ghdl $FLAGS {self.top}']
#         # Parameters
#         params = []
#         for param in self.params:
#             params.append(f'chparam -set {param[0]} {param[1]} {self.top}')

#     def generate(self, to_task, from_task, capture):
#         if self.frontend == 'ghdl' or 'verilog' in self.backend:
#             to_task = 'syn'
#             from_task = 'syn'
#         return super().generate(to_task, from_task, capture)

#     def transfer(self, devtype, position, part, width, capture):
#         super().transfer(devtype, position, part, width, capture)
#         template = os.path.join(os.path.dirname(__file__), 'openprog.sh')
#         with open(template, 'r', encoding='utf-8') as file:
#             text = file.read()
#         text = text.format(
#             family=self.part['family'],
#             project=self.project,
#             #
#             oci_engine=self.oci_engine,
#             cont_iceprog=self.conts['iceprog'],
#             cont_openocd=self.conts['openocd'],
#             tool_iceprog=self.tools['iceprog'],
#             tool_openocd=self.tools['openocd']
#         )
#         with open('openprog.sh', 'w', encoding='utf-8') as file:
#             file.write(text)
#         return run(self._TRF_COMMAND, capture)

# def get_family(part):
#     """Get the Family name from the specified part name."""
#     part = part.lower()
#     families = [
#         # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
#         'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
#         'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
#     ]
#     for family in families:
#         if part.startswith(family):
#             return family
#     families = [
#         # From <nextpnr>/ice40/main.cc
#         'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
#         'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
#     ]
#     if part.startswith(tuple(families)):
#         return 'ice40'
#     families = [
#         # From <nextpnr>/ecp5/main.cc
#         '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
#         'um5g-25k', 'um5g-45k', 'um5g-85k'
#     ]
#     if part.startswith(tuple(families)):
#         return 'ecp5'
#     return 'UNKNOWN'
