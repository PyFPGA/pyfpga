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

"""fpga.tool.yosys

Implements the support for Yosys synthesizer.
"""

import os

from fpga.tool import Tool


def get_family(part):
    """Get the Family name from the specified part name."""
    families = [
        # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
        'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
        'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
    ]
    for family in families:
        if part.lower().startswith(family):
            return family
    return 'UNKNOWN'


_TEMPLATE = """\
#!/bin/bash

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

{vhdls}

yosys -Q {module} -p '
{includes};
{verilogs};
{params};
{actions}
'
"""


class Yosys(Tool):
    """Implementation of the class to support Yosys."""

    _TOOL = 'yosys'

    _DOCKER = "docker run --rm -v $HOME:$HOME -w $PWD ghdl/synth:beta"
    _GEN_COMMAND = '{} bash yosys.sh'.format(_DOCKER)

    _GENERATED = ['*.cf']

    def __init__(self, project, output='verilog'):
        super().__init__(project)
        self.output = output
        self.includes = []

    def set_param(self, name, value):
        """Set a Generic/Parameter Value."""
        self.params.append([name, value])

    def add_file(self, file, library=None, included=False, design=False):
        if included:
            self.includes.append(file)
        elif not design:
            self.files.append([file, library])

    def _create_gen_script(self, strategy, tasks):
        # Verilog includes
        includes = []
        for include in self.includes:
            dirname = os.path.dirname(include)
            includes.append('verilog_defaults -add -I{}'.format(dirname))
        # Files
        verilogs = []
        vhdls = []
        for file in self.files:
            # VHDL (GHDL)
            if os.path.splitext(file[0])[1] in ['.vhd', '.vhdl']:
                lib = ''
                if file[1] is not None:
                    lib = '--work={}'.format(file[1])
                vhdls.append('ghdl -a $FLAGS {} {}'.format(lib, file[0]))
            # Verilog (Yosys)
            if os.path.splitext(file[0])[1] == 'sv':
                verilogs.append('read_verilog -sv -defer {}'.format(file[0]))
            else:
                verilogs.append('read_verilog -defer {}'.format(file[0]))
        if len(vhdls) > 0:
            verilogs = ['ghdl \'"$FLAGS"\' {}'.format(self.top)]
        # Parameters
        params = []
        for param in self.params:
            params.append('chparam -set {} {} {}').format(
                param[0], param[1], self.top
            )
        # synth and write
        actions = []
        if self.output in ['edif-vivado', 'edif-ise']:
            actions.append('synth_xilinx -top {} -family {} {}'.format(
                self.top,
                get_family(self.part),
                '-ise' if self.output == 'edif-ise' else ''
            ))
            actions.append('write_edif -pvector bra {}.edif'.format(
                self.project
            ))
        elif self.output == 'verilog-nosynth':
            actions.append('write_verilog {}.v'.format(self.project))
        else:
            actions.append('synth -top {}'.format(self.top))
            actions.append('write_verilog {}.v'.format(self.project))
        # Write script
        text = _TEMPLATE.format(
            vhdls='\n'.join(vhdls),
            module='-m ghdl' if len(vhdls) > 0 else '',
            includes=';\n'.join(includes),
            verilogs=';\n'.join(verilogs),
            params=';\n'.join(params),
            actions=';\n'.join(actions)
        )
        open("%s.sh" % self._TOOL, 'w').write(text)
