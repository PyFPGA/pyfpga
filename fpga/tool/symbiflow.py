#
# Copyright (C) 2021 Rodrigo A. Melo
# Copyright (C) 2021 INTI
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

"""fpga.tool.symbiflow

Implements the support of Symbiflow (FOSS).
"""

import os
from fpga.tool import Tool


class Symbiflow(Tool):
    """Implementation of the class to support Symbiflow."""

    _TOOL = 'symbiflow'
    _PART = 'xc7a35tcsg324-1'
    _GEN_PROGRAM = 'bash'
    _GEN_COMMAND = 'bash symbiflow.sh'
    _CLEAN = [
        # files
        '*.bit', '*.eblif', '*.fasm', '*.ilang', '*.ioplace', '*.json',
        '*.log', '*.net', '*.place', '*.post_routing', '*.route',
        '*_synth', '*.premap.v', '*.pcf', '*.sdc', '*.xdc',
        # pyfpga
        '*.sh'
    ]

    def set_part(self, part):
        part = part.lower()
        self.part['name'] = part
        # Family
        self.part['family'] = 'artix7'
        if part.startswith('xc7k'):
            self.part['family'] = 'kintex7'
        elif part.startswith('xc7v'):
            self.part['family'] = 'virtex7'
        elif part.startswith('xc7z'):
            self.part['family'] = 'zynq7'
        # Device
        self.part['device'] = 'xc7a50t_test'
        if part.startswith('xc7a35t'):
            self.part['device'] = 'xc7a50t_test'
        elif part.startswith('xc7a100t'):
            self.part['device'] = 'xc7a100t_test'
        elif part.startswith('xc7a200t'):
            self.part['device'] = 'xc7a200t_test'
        elif part.startswith('xc7z010'):
            self.part['device'] = 'xc7z010_test'

    def _create_gen_script(self, tasks):
        # Files
        verilogs = []
        for file in self.files['verilog']:
            verilogs.append(file[0])
        constraints = {'pcf': [], 'sdc': [], 'xdc': []}
        for file in self.files['constraint']:
            ext = os.path.splitext(file[0])[1].replace('.', '')
            constraints[ext].append(file[0])
        # Script creation
        template = os.path.join(
            os.path.dirname(__file__), '%s.sh' % self._TOOL
        )
        with open(template, 'r') as file:
            text = file.read()
        text = text.format(
            project=self.project,
            part=self.part['name'],
            family=self.part['family'],
            device=self.part['device'],
            top=self.top,
            xdc=' '.join(constraints['xdc']),
            sdc=' '.join(constraints['sdc']),
            pcf=' '.join(constraints['pcf']),
            verilogs=' '.join(verilogs),
            tasks=tasks
        )
        with open('%s.sh' % self._TOOL, 'w') as file:
            file.write(text)

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        raise NotImplementedError('transfer(symbiflow)')
