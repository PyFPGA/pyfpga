#
# Copyright (C) 2020 INTI
# Copyright (C) 2020 Rodrigo A. Melo
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

"""fpga.tool.yosys

Implements the support for Yosys synthesizer.
"""

import re

from fpga.tool import Tool


class Yosys(Tool):
    """Implementation of the class to support Yosys."""

    _TOOL = 'yosys'

    _GEN_COMMAND = 'yosys -Q yosys.tcl'

    def __init__(self, project, backend=None):
        """Initializes the attributes of the class."""
        super().__init__(project)
        # pylint: disable=import-outside-toplevel
        if backend == 'ise':
            from fpga.tool.ise import Ise
            self.tool = Ise(project)
            self.sectool = 'ise'
        elif backend == 'vivado':
            from fpga.tool.vivado import Vivado
            self.tool = Vivado(project)
            self.sectool = 'vivado'
        else:
            self.tool = None

    def generate(self, strategy, to_task, from_task, capture):
        """Run the FPGA tool."""
        super().generate(strategy, 'syn', from_task, capture)
        # Configuring the backend tool
        self.tool.sectool = 'yosys'
        self.tool.part = self.part
        self.tool.options = self.options
        for file in self.files:
            if 'fpga_include' in file:
                continue
            if re.match(r'.*\.v$', file):
                continue
            self.tool.files.append(file)
        self.tool.add_file('yosys.edif')
        self.tool.set_top('Top')
        # Running the backend tool
        self.tool.generate(strategy, to_task, from_task, capture)

    def transfer(self, devtype, position, part, width, capture):
        """Transfer a bitstream."""
        self.tool.transfer(devtype, position, part, width, capture)
