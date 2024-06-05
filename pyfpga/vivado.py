#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

from pyfpga.project import Project

_TEMPLATES = {
    'fpga': """\
if { [ catch { open_hw_manager } ] } { open_hw }
connect_hw_server
open_hw_target
set obj [lindex [get_hw_devices [current_hw_device]] 0]
set_property PROGRAM.FILE #BITSTREAM# $obj
program_hw_devices $obj
""",
    'detect': """\
if { [ catch { open_hw_manager } ] } { open_hw }
connect_hw_server
open_hw_target
puts [get_hw_devices]
"""
}

# pylint: disable=too-few-public-methods


class Vivado(Project):
    """Class to support Vivado."""

    tool = {
        'program': 'vivado',
        'command': 'vivado -mode batch -notrace -quiet -source vivado.tcl',
    }

#     _TOOL = 'vivado'
#     _EXTENSION = 'xpr'
#     _PART = 'xc7k160t-3-fbg484'
#     _GEN_PROGRAM = 'vivado'
#     _GEN_COMMAND = 'vivado -mode batch -notrace -quiet -source vivado.tcl'
#     _TRF_PROGRAM = 'vivado'
#     _TRF_COMMAND =
#         'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
#     _BIT_EXT = ['bit']
#     _DEVTYPES = ['fpga', 'detect']
#     _CLEAN = [
#         # directories
#         '*.cache', '*.hw', '*.ip_user_files', '*.runs', '*.sim', '.Xil',
#         # files
#         '*.bit', '*.jou', '*.log', '*.rpt', 'vivado_*.zip',
#         # pyfpga
#         'vivado.tcl', 'vivado-prog.tcl'
#     ]

#     def __init__(self, project, frontend=None):
#         super().__init__(project)
#         if frontend == 'yosys':
#             from fpga.tool.openflow import Openflow
#             self.tool = Openflow(
#                 self.project,
#                 frontend='yosys',
#                 backend='vivado'
#             )
#             self.presynth = True

#     def generate(self, to_task, from_task, capture):
#         if self.presynth and from_task in ['prj', 'syn']:
#             self.tool.set_part(self.part['name'])
#             self.tool.set_top(self.top)
#             self.tool.paths = self.paths
#             self.tool.files['vhdl'] = self.files['vhdl']
#             self.tool.files['verilog'] = self.files['verilog']
#             self.tool.params = self.params
#             output1 = self.tool.generate('syn', 'prj', capture)
#             self.set_top(self.project)
#             output2 = super().generate(to_task, from_task, capture)
#             return str(output1) + str(output2)
#         return super().generate(to_task, from_task, capture)

#     def transfer(self, devtype, position, part, width, capture):
#         super().transfer(devtype, position, part, width, capture)
#         temp = _TEMPLATES[devtype]
#         if devtype != 'detect':
#             temp = temp.replace('#BITSTREAM#', self.bitstream)
#         with open('vivado-prog.tcl', 'w', encoding='utf-8') as file:
#             file.write(temp)
#         return run(self._TRF_COMMAND, capture)
