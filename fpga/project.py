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

import glob

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado


class Project:
    """Manage an FPGA project."""

    def __init__(self, tool='vivado', device=None, project=None):
        """Instantiate the Tool to use."""
        if tool == 'ise':
            self.tool = Ise(project, device)
        elif tool == 'libero':
            self.tool = Libero(project, device)
        elif tool == 'quartus':
            self.tool = Quartus(project, device)
        elif tool == 'vivado':
            self.tool = Vivado(project, device)
        else:
            raise NotImplementedError(tool)

    def add_files(self, pathname, lib):
        """Add files to the project.

        PATHNAME must be a string containing an absolute or relative path
        specification, and can contain shell-style wildcards.
        LIB is optional and only useful for VHDL files.
        """
        files = glob.glob(pathname)
        for file in files:
            self.tool.add_file(file, lib)

    def set_top(self, toplevel):
        """Set the TOP LEVEL of the project."""
        self.tool.set_top(toplevel)

    def set_project_opts(self, options):
        """Set project OPTIONS."""
        self.tool.set_options(options, 'project')

    def set_pre_flow_opts(self, options):
        """Set pre flow OPTIONS."""
        self.tool.set_options(options, 'pre_flow')

    def set_post_syn_opts(self, options):
        """Set post synthesis OPTIONS."""
        self.tool.set_options(options, 'post_syn')

    def set_post_imp_opts(self, options):
        """Set post implementation OPTIONS."""
        self.tool.set_options(options, 'post_imp')

    def set_post_bit_opts(self, options):
        """Set post bitstream generation OPTIONS."""
        self.tool.set_options(options, 'post_bit')

    def generate(self, strategy, task):
        """Run the FPGA tool."""
        self.tool.generate(strategy, task)

    def transfer(self, device, position, name, width):
        """Transfer the bitstream to a DEVICE."""
        self.tool.transfer(device, position, name, width)
