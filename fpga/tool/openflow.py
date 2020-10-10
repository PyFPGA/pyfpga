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

"""fpga.tool.openflow

Implements the support of the open-source tools.
"""

import os

from fpga.tool import Tool


def get_family(part):
    """Get the Family name from the specified part name."""
    part = part.lower()
    families = [
        # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
        'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
        'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
    ]
    for family in families:
        if part.startswith(family):
            return family
    families = [
        # From <nextpnr>/ice40/main.cc
        'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
        'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
    ]
    if part.startswith(tuple(families)):
        return 'ice40'
    families = [
        # From <nextpnr>/ecp5/main.cc
        '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
        'um5g-25k', 'um5g-45k', 'um5g-85k'
    ]
    if part.startswith(tuple(families)):
        return 'ecp5'
    return 'UNKNOWN'


class Openflow(Tool):
    """Implementation of the class to support Yosys."""

    _TOOL = 'yosys'

    _GEN_COMMAND = 'bash yosys.sh'

    _GENERATED = ['*.cf', '*.edif', '*.json']

    def __init__(self, project, backend='nextpnr'):
        super().__init__(project)
        self.backend = backend
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
        # pylint: disable=too-many-locals
        # Verilog includes
        includes = []
        for include in self.includes:
            dirname = os.path.dirname(include)
            includes.append('verilog_defaults -add -I{}'.format(dirname))
        # Files
        constraints = []
        verilogs = []
        vhdls = []
        for file in self.files:
            ext = os.path.splitext(file[0])[1]
            # VHDL (GHDL)
            if ext in ['.vhd', '.vhdl']:
                lib = ''
                if file[1] is not None:
                    lib = '--work={}'.format(file[1])
                vhdls.append('ghdl -a $FLAGS {} {}'.format(lib, file[0]))
            # Verilog (Yosys)
            elif ext == '.sv':
                verilogs.append('read_verilog -sv -defer {}'.format(file[0]))
            elif ext == '.v':
                verilogs.append('read_verilog -defer {}'.format(file[0]))
            else:
                constraints.append(file[0])
        if len(vhdls) > 0:
            verilogs = ['ghdl $FLAGS {}'.format(self.top)]
        # Parameters
        params = []
        for param in self.params:
            params.append('chparam -set {} {} {}').format(
                param[0], param[1], self.top
            )
        # Device and Package
        device, package = self.part.split('-')
        if device.endswith('4k'):
            # See http://www.clifford.at/icestorm/
            device = device.replace('4', '8')
            package += ":4k"
        # Script creation
        template = os.path.join(os.path.dirname(__file__), 'template.sh')
        text = open(template).read()
        text = text.format(
            backend=self.backend,
            constraints='\\\n'+'\n'.join(constraints),
            device=device,
            includes='\\\n'+'\n'.join(includes),
            family=get_family(self.part),
            package=package,
            params='\\\n'+'\n'.join(params),
            project=self.project,
            tasks=tasks,
            tool=self._TOOL,
            top=self.top,
            verilogs='\\\n'+'\n'.join(verilogs),
            vhdls='\\\n'+'\n'.join(vhdls)
        )
        open("%s.sh" % self._TOOL, 'w').write(text)
