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

"""fpga.project

Main Class of PyFPGA, which provides functionalities to create a project,
generate files and transfer to a Device.
"""

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado


class Project:
    """Manage an FPGA project."""

    def __init__(self, tool='vivado', device=None, project=None):
        """Instantiate the Tool to use."""
        if tool is 'ise':
            self.tool = Ise(project, device)
        elif tool is 'libero':
            self.tool = Libero(project, device)
        elif tool is 'quartus':
            self.tool = Quartus(project, device)
        elif tool is 'vivado':
            self.tool = Vivado(project, device)
        else:
            raise NotImplementedError(tool)
