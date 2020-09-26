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

from fpga.tool import Tool, run


class Ghdl(Tool):
    """Implementation of the class to support GHDL."""

    _TOOL = 'ghdl'

    _GENERATED = ['*.cf']

    _FLAGS = '--std=08 -fsynopsys -fexplicit -frelaxed'

    def add_file(self, file, library=None, included=False, design=False):
        command = 'ghdl -a {} '.format(self._FLAGS)
        if library is not None:
            command += '--work={} '.format(library)
        command += file
        self.files.append(command)

    def generate(self, strategy, to_task, from_task, capture):
        # GHDL flow is based on commands only
        if len(self.files) > 0:
            command = ';'.join(self.files) + ';'
        command += 'ghdl --synth {} {} > {}.vhdl'.format(
            self._FLAGS, self.top, self.project
        )
        # print(command)
        return run(command, capture)
