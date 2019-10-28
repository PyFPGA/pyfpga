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

"""fpga.tool

Defines the interface to be inherited to support a tool.
"""

import os.path


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations. By default, most of
    the methods raises a NotImplementedError exception and should be replaced
    by a tool implementation to provide the needed funcionality.
    """

    def __init__(self, project, device):
        """Initializes the attributes of the class."""
        self.project = project
        self.device = device
        self.strategy = 'none'
        self.task = 'bit'
        self.files = ""
        self.phase = {
            'project': '',
            'pre_flow': '',
            'post_syn': '',
            'post_imp': '',
            'post_bit': ''
        }

    def add_file(self, file, lib):
        """Add a FILE to the project.

        LIB is optional and only useful for VHDL files.
        """
        raise NotImplementedError('add_file')

    def set_top(self, toplevel):
        """Set the TOP LEVEL of the project."""
        raise NotImplementedError('set_top')

    _STRATEGIES = ['none', 'area', 'speed', 'power']

    def set_strategy(self, strategy):
        """Set the Optimization STRATEGY.

        The valid options are none (default), area, speed and power.
        """
        raise NotImplementedError('set_strategy')

    _PHASES = ['project', 'pre_flow', 'post_syn', 'post_imp', 'post_bit']

    def set_options(self, options, phase):
        """Set the specified OPTIONS in the desired PHASE.

        The OPTIONs are specific for each tool (one or more Tcl lines). The
        valid PHASEs are project, pre_flow, post_syn, post_imp and post_bit.
        """
        raise NotImplementedError('set_options')

    def get_template(self):
        """Loads a template Tcl file."""
        file = os.path.join(os.path.dirname(__file__), 'template.tcl')
        self.template = open(file).read()

    def get_script(self):
        """Generates the script to be used as input of the Tool."""
        raise NotImplementedError('get_script')

    _TASKS = ['prj', 'syn', 'imp', 'bit']

    def generate(self, task):
        """Run the FPGA tool.

        The valid TASKs are prj to only create the project file, syn for also
        performs the synthesis, imp to add implementation and bit (default)
        to finish with the bitstream generation.
        """
        raise NotImplementedError('generate')

    DEVICES = ['fpga', 'spi', 'bpi', 'xcf']

    def transfer(self, device, position, name, width):
        """Transfer the bitstream to a DEVICE.

        Optionally, the POSITION in the Jtag chain (for FPGAs and some old
        memories), the NAME (for SPI/BPI memories) and the data WIDTH (for
        memories) can be specified.
        """
        raise NotImplementedError('transfer')
