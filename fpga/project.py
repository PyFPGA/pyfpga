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


class Project:
    """Manage an FPGA project."""

    __init__(self, tool, device=None, name=None):
        """Instantiate the Tool to use.

        If a DEVICE is not specified, the default of the selected TOOL is
        used. The default project NAME is the same as the TOOL but another
        one can be specified.
        """
