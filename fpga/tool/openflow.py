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

from fpga.tool import Tool, run


class Openflow(Tool):
    """Implementation of the class to support the open-source tools."""

    _TOOL = 'openflow'
    _PART = 'hx8k-ct256'
    _GEN_PROGRAM = 'docker'
    _GEN_COMMAND = 'bash openflow.sh'
    _TRF_PROGRAM = 'docker'
    _TRF_COMMAND = 'bash openprog.sh'
    _BIT_EXT = ['bit']
    _DEVTYPES = ['fpga']
    _CLEAN = [
        # files
        '*.asc', '*.bit', '*.cf', '*.config', '*.edif', '*.json', '*.rpt',
        '*.svf',
        # pyfpga
        '*.sh'
    ]

    def __init__(self, project, frontend='yosys', backend='nextpnr'):
        # The valid frontends are be ghdl and yosys
        # The valid backends are:
        # * For ghdl -> vhdl
        # * For yosys -> ise, nextpnr, verilog, verilog-nosynth and vivado
        super().__init__(project)
        self.backend = backend
        self.frontend = frontend

    def set_part(self, part):
        self.part['name'] = part
        self.part['family'] = get_family(part)
        if self.part['family'] in ['ice40', 'ecp5']:
            aux = part.split('-')
            if len(aux) == 2:
                self.part['device'] = aux[0]
                self.part['package'] = aux[1]
            elif len(aux) == 3:
                self.part['device'] = '{}-{}'.format(aux[0], aux[1])
                self.part['package'] = aux[2]
            else:
                raise ValueError('Part must be DEVICE-PACKAGE')
            if self.part['device'].endswith('4k'):
                # See http://www.clifford.at/icestorm/
                self.part['device'] = self.part['device'].replace('4', '8')
                self.part['package'] += ":4k"

    def _create_gen_script(self, tasks):
        # Verilog includes
        paths = []
        for path in self.paths:
            paths.append('verilog_defaults -add -I{}'.format(path))
        # Files
        constraints = []
        verilogs = []
        vhdls = []
        for file in self.filesets['vhdl']:
            lib = ''
            if file[1] is not None:
                lib = '--work={}'.format(file[1])
            vhdls.append('ghdl -a $FLAGS {} {}'.format(lib, file[0]))
        for file in self.filesets['verilog']:
            if file[0].endswith('.sv'):
                verilogs.append('read_verilog -sv -defer {}'.format(file[0]))
            else:
                verilogs.append('read_verilog -defer {}'.format(file[0]))
        for file in self.filesets['constraint']:
            constraints.append(file[0])
        if len(vhdls) > 0:
            verilogs = ['ghdl $FLAGS {}'.format(self.top)]
        # Parameters
        params = []
        for param in self.params:
            params.append('chparam -set {} {} {}'.format(
                param[0], param[1], self.top
            ))
        # Script creation
        template = os.path.join(os.path.dirname(__file__), 'template.sh')
        text = open(template).read()
        text = text.format(
            backend=self.backend,
            constraints='\\\n'+'\n'.join(constraints),
            device=self.part['device'],
            includes='\\\n'+'\n'.join(paths),
            family=self.part['family'],
            frontend=self.frontend,
            package=self.part['package'],
            params='\\\n'+'\n'.join(params),
            project=self.project,
            tasks=tasks,
            top=self.top,
            verilogs='\\\n'+'\n'.join(verilogs),
            vhdls='\\\n'+'\n'.join(vhdls)
        )
        open("%s.sh" % self._TOOL, 'w').write(text)

    def generate(self, to_task, from_task, capture):
        if self.frontend == 'ghdl' or 'verilog' in self.backend:
            to_task = 'syn'
            from_task = 'syn'
        return super().generate(to_task, from_task, capture)

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        template = os.path.join(os.path.dirname(__file__), 'openprog.sh')
        text = open(template).read()
        text = text.format(
            family=self.part['family'],
            project=self.project
        )
        open("openprog.sh", 'w').write(text)
        return run(self._TRF_COMMAND, capture)


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
