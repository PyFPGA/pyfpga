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

from fpga.tool import Tool

_TEMPLATE = """\
#!/bin/bash

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

{vhdls}

ghdl --synth $FLAGS {top} > {project}.vhdl
"""


class Ghdl(Tool):
    """Implementation of the class to support GHDL."""

    _TOOL = 'ghdl'

    _DOCKER = "docker run --rm -v $HOME:$HOME -w $PWD ghdl/synth:beta"
    _GEN_COMMAND = '{} bash ghdl.sh'.format(_DOCKER)

    _GENERATED = ['*.cf']

    def add_file(self, file, library=None, included=False, design=False):
        if not included and not design:
            self.files.append([file, library])

    def _create_gen_script(self, strategy, tasks):
        files = []
        for file in self.files:
            lib = '--work={}'.format(file[1]) if file[1] is not None else ''
            files.append('ghdl -a $FLAGS {} {}'.format(lib, file[0]))
        text = _TEMPLATE.format(
            vhdls='\n'.join(files),
            top=self.top,
            project=self.project
        )
        open("%s.sh" % self._TOOL, 'w').write(text)
