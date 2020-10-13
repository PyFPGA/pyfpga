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

"""fpga.tool.ghdl

Implements the support for GHDL synthesizer.
"""

from fpga.tool.openflow import Openflow


class Ghdl(Openflow):
    """Implementation of the class to support GHDL."""

    _TOOL = 'ghdl'

    _GEN_COMMAND = 'bash {}.sh'.format(_TOOL)

    _GENERATED = ['*.cf']

    def __init__(self, project):
        super().__init__(project)
        self.frontend = 'ghdl'

    def generate(self, strategy, to_task, from_task, capture):
        return super().generate(strategy, 'syn', 'syn', capture)
