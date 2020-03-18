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

from fpga.tool import Tool, find_bitstream, run

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

    _DEVTYPES = ['fpga', 'detect']

    _GENERATED = [
        # directories
        '*.cache', '*.hw', '*.ip_user_files', '*.runs', '*.sim', '.Xil',
        # files
        '*.bit', '*.jou', '*.log', '*.rpt', 'vivado_*.zip',
        'vivado.tcl'
    ]

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        temp = _TEMPLATES[devtype]
        if devtype != 'detect':
            bitstream = find_bitstream('bit')
            temp = temp.replace('#BITSTREAM#', bitstream)
        open("vivado-prog.tcl", 'w').write(temp)
        return run(self._TRF_COMMAND, capture)
