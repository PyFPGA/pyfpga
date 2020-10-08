#
# Copyright (C) 2019-2020 INTI
# Copyright (C) 2019-2020 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""fpga.tool.vivado

Implements the support of Vivado (Xilinx).
"""

import os

from fpga.tool import Tool, run

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


class Vivado(Tool):
    """Implementation of the class to support Vivado."""

    _TOOL = 'vivado'
    _EXTENSION = 'xpr'
    _PART = 'xc7k160t-3-fbg484'

    _GEN_COMMAND = 'vivado -mode batch -notrace -quiet -source vivado.tcl'
    _TRF_COMMAND = 'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'

    _BIT_EXT = ['bit']
    _DEVTYPES = ['fpga', 'detect']

    _GENERATED = [
        # directories
        '*.cache', '*.hw', '*.ip_user_files', '*.runs', '*.sim', '.Xil',
        # files
        '*.bit', '*.jou', '*.log', '*.rpt', 'vivado_*.zip',
        'vivado.tcl'
    ]

    def __init__(self, project, frontend=None):
        super().__init__(project)
        # pylint: disable=import-outside-toplevel
        if frontend == 'yosys':
            from fpga.tool.yosys import Yosys
            self.tool = Yosys(self.project, 'vivado')
            self.presynth = True

    def set_param(self, name, value):
        if self.presynth:
            self.tool.set_param(name, value)
        else:
            super().set_param(name, value)

    def add_file(self, file, library=None, included=False, design=False):
        ext = os.path.splitext(file)[1]
        if self.presynth and ext in ['.v', '.sv', '.vh', '.vhd', '.vhdl']:
            self.tool.add_file(file, library, included, design)
        else:
            super().add_file(file, library, included, design)

    def generate(self, strategy, to_task, from_task, capture):
        if self.presynth and from_task in ['prj', 'syn']:
            self.tool.set_part(self.part)
            self.tool.set_top(self.top)
            output1 = self.tool.generate(strategy, 'syn', 'prj', capture)
            self.add_file('{}.edif'.format(self.project))
            self.set_top(self.project)
            output2 = super().generate(strategy, to_task, from_task, capture)
            return str(output1) + str(output2)
        return super().generate(strategy, to_task, from_task, capture)

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        temp = _TEMPLATES[devtype]
        if devtype != 'detect':
            temp = temp.replace('#BITSTREAM#', self.bitstream)
        open("vivado-prog.tcl", 'w').write(temp)
        return run(self._TRF_COMMAND, capture)
