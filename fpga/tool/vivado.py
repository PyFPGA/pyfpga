#
# Copyright (C) 2019 INTI
# Copyright (C) 2019 Rodrigo A. Melo
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

from glob import glob
import subprocess

from fpga.tool import Tool

_TEMPLATES = {
    'fpga': """\
if { [ catch { open_hw_manager } ] } { open_hw }
connect_hw_server
open_hw_target
set obj [lindex [get_hw_devices [current_hw_device]] 0]
set_property PROGRAM.FILE #BITSTREAM# $obj
program_hw_devices $obj
""",
    'detect': """open_hw
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

    def transfer(self, devtype='fpga', position=1, part=None, width=None):
        super().transfer(devtype, position, part, width)
        temp = _TEMPLATES[devtype]
        if devtype != 'detect':
            bitstream = glob('**/*.bit', recursive=True)
            temp = temp.replace('#BITSTREAM#', bitstream[0])
        open("vivado-prog.tcl", 'w').write(temp)
        subprocess.run(self._TRF_COMMAND, shell=True, check=True)
