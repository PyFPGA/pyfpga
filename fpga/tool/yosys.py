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

_TEMPLATE = """\
#!/bin/bash

FLAGS="--std=08 -fsynopsys -fexplicit -frelaxed"

{vhdls}

yosys -Q {module} -p '
{verilogs};
{params};
{synth};
{write}
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
        verilogs = []
        for include in self.includes:
            dirname = os.path.dirname(include)
            verilogs.append('verilog_defaults -add -I{}'.format(dirname))
        vhdls = []
        # Files
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
        # synth and write command
#            global FAMILY
#            set FAMILY "Unknown"
#            if {[regexp -nocase {xcup} $PART]} {
#                set FAMILY "xcup"
#            } elseif {[regexp -nocase {xcu} $PART]} {
#                set FAMILY "xcu"
#            } elseif {[regexp -nocase {xc7} $PART]} {
#                set FAMILY "xc7"
#            } elseif {[regexp -nocase {xc6v} $PART]} {
#                set FAMILY "xc6v"
#            } elseif {[regexp -nocase {xc6s} $PART]} {
#                set FAMILY "xc6s"
#            } elseif {[regexp -nocase {xc5v} $PART]} {
#                set FAMILY "xc5v"
#            } else {
#                puts "The family of the part $PART is $FAMILY"
#            }
        family = 'xc7'
        if self.output == 'edif-vivado':
            synth = 'synth_xilinx -top {} -family {}'.format(
                self.top, family
            )
            write = 'write_edif -pvector bra {}.edif'.format(self.project)
        elif self.output == 'edif-ise':
            synth = 'synth_xilinx -top {} -family {} --ise'.format(
                self.top, family
            )
            write = 'write_edif -pvector bra {}.edif'.format(self.project)
        else:
            synth = 'synth -top {}'.format(self.top)
            write = 'write_verilog {}.v'.format(self.project)
        # Write script
        text = _TEMPLATE.format(
            vhdls='\n'.join(vhdls),
            module='-m ghdl' if len(vhdls) > 0 else '',
            verilogs=';\n'.join(verilogs),
            params=';\n'.join(params),
            synth=synth,
            write=write
        )
        open("%s.sh" % self._TOOL, 'w').write(text)
