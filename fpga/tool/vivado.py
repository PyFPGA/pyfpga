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

from fpga.tool import Tool


class Vivado(Tool):
    """Implementation of the class to support Vivado."""

    _TOOL = 'vivado'
    _EXTENSION = 'xpr'
    _DEVICE = 'xc7z010-1-clg400'

    def generate(self):
        tcl = self._TEMPLATE
        open("%s.tcl" % self._TOOL, 'w').write(tcl)
