#
# Copyright (C) 2019-2020 INTI
# Copyright (C) 2019-2021 Rodrigo A. Melo
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

"""fpga.tool.ise

Implements the support of ISE (Xilinx).
"""

import re

from fpga.tool import Tool, run

_TEMPLATES = {
    'fpga': """setMode -bs
setCable -port auto
Identify -inferir
assignFile -p #POSITION# -file #BITSTREAM#
Program -p #POSITION#

quit
""",
    'spi': """setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffspi
addDesign -version 0 -name 0
addDeviceChain -index 0
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -spi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# -spionly -e -v -loadfpga

quit
""",
    'bpi': """setMode -pff
addConfigDevice -name #NAME# -path .
setSubmode -pffbpi
addDesign -version 0 -name 0
addDeviceChain -index 0
setAttribute -configdevice -attr flashDataWidth -value #WIDTH#
addDevice -p 1 -file #BITSTREAM#
generate -generic

setMode -bs
setCable -port auto
Identify
attachflash -position #POSITION# -bpi #NAME#
assignfiletoattachedflash -position #POSITION# -file ./#NAME#.mcs
Program -p #POSITION# -dataWidth #WIDTH# \
-rs1 NONE -rs0 NONE -bpionly -e -v -loadfpga

quit
""",
    'detect': """setMode -bs
setCable -port auto
Identify -inferir
quit
""",
    'unlock': """cleancablelock
quit
"""
}


class Ise(Tool):
    """Implementation of the class to support ISE."""

    _TOOL = 'ise'
    _EXTENSION = 'xise'
    _PART = 'xc7k160t-3-fbg484'
    _GEN_PROGRAM = 'xtclsh'
    _GEN_COMMAND = 'xtclsh ise.tcl'
    _TRF_PROGRAM = 'impact'
    _TRF_COMMAND = 'impact -batch ise-prog.impact'
    _BIT_EXT = ['bit']
    _DEVTYPES = ['fpga', 'spi', 'bpi', 'detect', 'unlock']
    _CLEAN = [
        # directories
        'iseconfig', '_ngo', 'xlnx_auto_0_xdb', '_xmsgs', 'xst',
        # files
        '*.bgn', '*.bld', '*.bit',
        '*.cmd_log', '*.csv',
        '*.drc',
        '*.gise',
        '*.html',
        '*.log', '*.lso',
        '*.map', '*.mrp',
        '*.ncd', '*.ngc', '*.ngd', '*.ngm', '*.ngr',
        '*.pad', '*.par', '*.pcf', '*.prj', '*.ptwx',
        '*.stx', '*.syr',
        '*.twr', '*.twx',
        '*.unroutes', '*.ut',
        '*.txt',
        '*.xml', '*.xpi', '*.xrpt', '*.xst', '*.xwbt',
        '_impact*',
        # pyfpga
        '*.impact', 'ise.tcl'
    ]

    def __init__(self, project, frontend=None):
        super().__init__(project)
        if frontend == 'yosys':
            from fpga.tool.openflow import Openflow
            self.tool = Openflow(
                self.project,
                frontend='yosys',
                backend='ise'
            )
            self.presynth = True

    def set_part(self, part):
        try:
            device, speed, package = re.findall(r'(\w+)-(\w+)-(\w+)', part)[0]
            if len(speed) > len(package):
                speed, package = package, speed
            part = f'{device}-{speed}-{package}'
        except IndexError:
            raise ValueError(
                'Part must be DEVICE-SPEED-PACKAGE or DEVICE-PACKAGE-SPEED'
            )
        self.part['name'] = part
        self.part['family'] = get_family(part)
        self.part['device'] = device
        self.part['package'] = package
        self.part['speed'] = '-' + speed

    def generate(self, to_task, from_task, capture):
        if self.presynth and from_task in ['prj', 'syn']:
            self.tool.set_part(self.part['name'])
            self.tool.set_top(self.top)
            self.tool.paths = self.paths
            self.tool.files['vhdl'] = self.files['vhdl']
            self.tool.files['verilog'] = self.files['verilog']
            self.tool.params = self.params
            output1 = self.tool.generate('syn', 'prj', capture)
            output2 = super().generate(to_task, from_task, capture)
            return str(output1) + str(output2)
        return super().generate(to_task, from_task, capture)

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        temp = _TEMPLATES[devtype]
        if devtype not in ['detect', 'unlock']:
            temp = temp.replace('#BITSTREAM#', self.bitstream)
            temp = temp.replace('#POSITION#', str(position))
            temp = temp.replace('#NAME#', part)
            temp = temp.replace('#WIDTH#', str(width))
        with open('ise-prog.impact', 'w', encoding='utf-8') as file:
            file.write(temp)
        return run(self._TRF_COMMAND, capture)


def get_family(part):
    """Get the Family name from the specified part name."""
    part = part.lower()
    families = {
        r'xc7a\d+l': 'artix7l',
        r'xc7a': 'artix7',
        r'xc7k\d+l': 'kintex7l',
        r'xc7k': 'kintex7',
        r'xc3sd\d+a': 'spartan3adsp',
        r'xc3s\d+a': 'spartan3a',
        r'xc3s\d+e': 'spartan3e',
        r'xc3s': 'spartan3',
        r'xc6s\d+l': 'spartan6l',
        r'xc6s': 'spartan6',
        r'xc4v': 'virtex4',
        r'xc5v': 'virtex5',
        r'xc6v\d+l': 'virtex6l',
        r'xc6v': 'virtex6',
        r'xc7v\d+l': 'virtex7l',
        r'xc7v': 'virtex7',
        r'xc7z': 'zynq'
    }
    for key, value in families.items():
        if re.match(key, part):
            return value
    return 'UNKNOWN'
