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


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations. By default, the
    methods raise a NotImplementedError exception and should be replaced by a
    tool implementation to provide the needed funcionality.
    """

    set_project(self, name):
        """Set the NAME of the project."""
        raise NotImplementedError(self.set_project.__name__)

    set_device(self, device):
        """Set the target DEVICE."""
        raise NotImplementedError(self.set_device.__name__)

    set_file(self, file, lib):
        """Set a FILE of the project belonging to LIB.

        LIB is only useful for VHDL files belonging to a library which is not
        Work.
        """
        raise NotImplementedError(self.set_file.__name__)

    set_top(self, toplevel):
        """Set the TOP LEVEL of the project."""
        raise NotImplementedError(self.set_top.__name__)

    set_strategy(self, strategy):
        """Set the Optimization STRATEGY.

        The valid options are none (default), area, speed and power.
        """
        raise NotImplementedError(self.set_strategy.__name__)

    set_options(self, options, phase):
        """Set the specified OPTIONS in the desired phase.

        The OPTIONs are specific for each tool (one or more Tcl lines).
        The valid PHASEs are pre_syn (default), post_syn, post_impl and
        post_bit.
        """
        raise NotImplementedError(self.set_options.__name__)

    set_flow(self, task):
        """Set the tasks of the workflow to perform.

        The valid options are syn for only Synthesis, imp for synthesis and
        implementation and bit (default) to add the bitstream generation.
        """
        raise NotImplementedError(self.set_flow.__name__)

    generate(self):
        """Creates the Project File and run the tool."""
        raise NotImplementedError(self.generate.__name__)

    transfer(self, device, position, name, width):
        """Transfer the bitstream to a DEVICE.

        Optionally, the POSITION in the Jtag chain (for FPGAs and some old
        memories), the NAME (for SPI/BPI memories) and the data WIDTH (for
        memories) can be specified.
        """
        raise NotImplementedError(self.transfer.__name__)
