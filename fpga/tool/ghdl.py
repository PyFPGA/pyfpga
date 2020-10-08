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

import os
from fpga.tool import Tool


class Ghdl(Tool):
    """Implementation of the class to support GHDL."""

    _TOOL = 'ghdl'

    _GEN_COMMAND = 'bash ghdl.sh'

    _GENERATED = ['*.cf']

    def add_file(self, file, library=None, included=False, design=False):
        if not included and not design:
            self.files.append([file, library])

    def _create_gen_script(self, strategy, tasks):
        files = []
        for file in self.files:
            lib = '--work={}'.format(file[1]) if file[1] is not None else ''
            files.append('ghdl -a $FLAGS {} {}'.format(lib, file[0]))
        # Script creation
        template = os.path.join(os.path.dirname(__file__), 'template.sh')
        text = open(template).read()
        text = text.format(
            backend='',
            device='',
            includes='',
            family='',
            package='',
            params='',
            project=self.project,
            tasks='syn',
            tool=self._TOOL,
            top=self.top,
            verilogs='',
            vhdls='\\\n'+'\n'.join(files)
        )
        open("%s.sh" % self._TOOL, 'w').write(text)
