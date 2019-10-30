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
    raises a NotImplementedError exception and should be replaced by a tool
    implementation to provide the needed funcionality.
    """

    _TOOL = 'UNDEFINED'
    _EXTENSION = 'UNDEFINED'
    _DEVICE = 'UNDEFINED'

    def __init__(self, project, device):
        """Initializes the attributes of the class."""
        self.project = self._TOOL if project is None else project
        self.files = ''
        self.strategy = 'none'
        self.task = 'bit'
        self.device = {
            'name': self._DEVICE if device is None else device,
            'family': 'unused',
            'device': 'unused',
            'package': 'unused',
            'speed': 'unused'
        }
        self.options = {
            'project': '#empty',
            'pre-flow': '#empty',
            'post-syn': '#empty',
            'post-imp': '#empty',
            'post-bit': '#empty'
        }

    def get_config(self):
        """Get Configurations."""
        info = {
            "tool": self._TOOL,
            "project": self.project,
            "extension": self._EXTENSION,
            "device": self.device['name'],
            "strategy": self.strategy,
            "task": self.task
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

    _PHASES = ['project', 'pre-flow', 'post-syn', 'post-imp', 'post-bit']

    def set_options(self, options, phase):
        """Set the specified OPTIONS in the desired PHASE.

        The OPTIONs are specific for each tool (one or more Tcl lines). The
        valid PHASEs are project, pre-flow, post-syn, post-imp and post-bit.
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

    def get_tcl(self):
        """Get the Tcl to be used as input of the Tool."""
        template = os.path.join(os.path.dirname(__file__), 'template.tcl')
        tcl = open(template).read()
        tcl = tcl.replace("#TOOL#", self._TOOL)
        tcl = tcl.replace("#PROJECT#", self.project)
        tcl = tcl.replace("#STRATEGY#", self.strategy)
        tcl = tcl.replace("#TASK#", self.task)
        tcl = tcl.replace("#FPGA#", self.device['name'])
        tcl = tcl.replace("#FAMILY#", self.device['family'])
        tcl = tcl.replace("#DEVICE#", self.device['device'])
        tcl = tcl.replace("#PACKAGE#", self.device['package'])
        tcl = tcl.replace("#SPEED#", self.device['speed'])
        tcl = tcl.replace("#PROJECT_OPTS#", self.options['project'])
        tcl = tcl.replace("#PRE_FLOW_OPTS#", self.options['pre-flow'])
        tcl = tcl.replace("#POST_SYN_OPTS#", self.options['post-syn'])
        tcl = tcl.replace("#POST_IMP_OPTS#", self.options['post-imp'])
        tcl = tcl.replace("#POST_BIT_OPTS#", self.options['post-bit'])
        return tcl

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
