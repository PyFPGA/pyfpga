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


def check_value(value, values):
    """Check if VALUE is included in VALUES."""
    if value not in values:
        raise ValueError(
            '{} is not a valid value ({})'
            .format(value, " ,".join(values))
        )


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations. There are methods that
    by default raises a NotImplementedError exception and should be replaced
    by a tool implementation to provide the needed funcionality.
    """

    _TOOL = 'UNDEFINED'
    _EXTENSION = 'UNDEFINED'
    _DEVICE = 'UNDEFINED'

    def __init__(self, project, device):
        """Initializes the attributes of the class."""
        if project is None:
            self.project = self._TOOL
        else:
            self.project = project
        if device is None:
            self.device = self._DEVICE
        else:
            self.device = device
        self.files = ''
        self.strategy = 'none'
        self.task = 'bit'
        self.options = {
            'project': '',
            'pre_flow': '',
            'post_syn': '',
            'post_imp': '',
            'post_bit': ''
        }

    def get_config(self):
        """Get Configurations."""
        info = {
            "tool" : self._TOOL,
            "project" : self.project,
            "extension" : self._EXTENSION,
            "device" : self.device,
            "strategy" : self.strategy,
            "task" : self.task
        }
        return info

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
        check_value(strategy, self._STRATEGIES)
        self.strategy = strategy

    _PHASES = ['project', 'pre_flow', 'post_syn', 'post_imp', 'post_bit']

    def set_options(self, options, phase):
        """Set the specified OPTIONS in the desired PHASE.

        The OPTIONs are specific for each tool (one or more Tcl lines). The
        valid PHASEs are project, pre_flow, post_syn, post_imp and post_bit.
        """
        check_value(phase, self._PHASES)
        self.options[phase] = options

    _TASKS = ['prj', 'syn', 'imp', 'bit']

    def set_task(self, task):
        """Set the TASK to reach when the Tool is executed.

        The valid TASKs are prj to only create the project file, syn for also
        performs the synthesis, imp to add implementation and bit (default)
        to finish with the bitstream generation.
        """
        check_value(task, self._TASKS)
        self.task = task

    _TCL_PATH = os.path.join(os.path.dirname(__file__), '/template.tcl')
    _TEMPLATE = open(_TCL_PATH).read()

    def generate(self):
        """Run the FPGA tool."""
        raise NotImplementedError('generate')

    _DEVICES = ['fpga', 'spi', 'bpi', 'xcf']

    def transfer(self, device, position, name, width):
        """Transfer the bitstream to a DEVICE.

        Optionally, the POSITION in the Jtag chain (for FPGAs and some old
        memories), the NAME (for SPI/BPI memories) and the data WIDTH (for
        memories) can be specified.
        """
        raise NotImplementedError('transfer')
