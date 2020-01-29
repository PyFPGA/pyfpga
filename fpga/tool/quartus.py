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

"""fpga.tool.quartus

Implements the support of Quartus (Intel/Altera).
"""

import re

from fpga.tool import Tool, find_bitstream, run


class Quartus(Tool):
    """Implementation of the class to support Quartus."""

    _TOOL = 'quartus'
    _EXTENSION = 'qpf'
    _PART = '10cl120zf780i8g'

    _GEN_COMMAND = 'quartus_sh --script quartus.tcl'
    _TRF_COMMAND = 'quartus_pgm -c %s --mode jtag -o "p;%s@%s"'

    _DEVTYPES = ['fpga', 'detect']

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        result = run('jtagconfig', capture)
        if devtype == 'detect':
            print(result)
        else:
            bitstream = find_bitstream('sof')
            if len(bitstream) == 0:
                bitstream = find_bitstream('pof')
            cable = re.match(r"1\) (.*) \[", result.stdout).groups()[0]
            cmd = self._TRF_COMMAND % (cable, bitstream, position)
            result = run(cmd, capture)
        return result
