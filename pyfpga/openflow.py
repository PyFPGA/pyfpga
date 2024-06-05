#
# Copyright (C) 2020-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

    def _configure(self):
        super()._configure()
        # OCI ENGINE
        engine = self.configs.get('oci', {}).get('engine', {})
        command = engine.get('command', 'docker') + ' run --rm'
        volumes = '-v ' + ('-v ').join(engine.get('volumes', ['$HOME:$HOME']))
        work = '-w ' + engine.get('work', '$PWD')
        self.oci_engine = f'{command} {volumes} {work}'
        # Containers
        defaults = {
            'ghdl': 'ghdl/synth:beta',
            'yosys': 'ghdl/synth:beta',
            'nextpnr-ice40': 'ghdl/synth:nextpnr-ice40',
            'icetime': 'ghdl/synth:icestorm',
            'icepack': 'ghdl/synth:icestorm',
            'iceprog': '--device /dev/bus/usb ghdl/synth:prog',
            'nextpnr-ecp5': 'ghdl/synth:nextpnr-ecp5',
            'ecppack': 'ghdl/synth:trellis',
            'openocd': '--device /dev/bus/usb ghdl/synth:prog'
        }
        self.tools = {}
        self.conts = {}
        tools = self.configs.get('tools', {})
        containers = self.configs.get('oci', {}).get('containers', {})
        for tool, container in defaults.items():
            self.tools[tool] = tools.get(tool, tool)
            self.conts[tool] = containers.get(tool, container)

    def set_part(self, part):
        self.part['name'] = part
        self.part['family'] = get_family(part)
        if self.part['family'] in ['ice40', 'ecp5']:
            aux = part.split('-')
            if len(aux) == 2:
                self.part['device'] = aux[0]
                self.part['package'] = aux[1]
            elif len(aux) == 3:
                self.part['device'] = f'{aux[0]}-{aux[1]}'
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
            paths.append(f'verilog_defaults -add -I{path}')
        # Files
        constraints = []
        verilogs = []
        vhdls = []
        for file in self.files['vhdl']:
            lib = ''
            if file[1] is not None:
                lib = f'--work={file[1]}'
            vhdls.append(f'{self.tools["ghdl"]} -a $FLAGS {lib} {file[0]}')
        for file in self.files['verilog']:
            if file[0].endswith('.sv'):
                verilogs.append(f'read_verilog -sv -defer {file[0]}')
            else:
                verilogs.append(f'read_verilog -defer {file[0]}')
        for file in self.files['constraint']:
            constraints.append(file[0])
        if len(vhdls) > 0:
            verilogs = [f'ghdl $FLAGS {self.top}']
        # Parameters
        params = []
        for param in self.params:
            params.append(f'chparam -set {param[0]} {param[1]} {self.top}')
        # Script creation
        template = os.path.join(os.path.dirname(__file__), 'template.sh')
        with open(template, 'r', encoding='utf-8') as file:
            text = file.read()
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
            vhdls='\\\n'+'\n'.join(vhdls),
            #
            oci_engine=self.oci_engine,
            cont_ghdl=self.conts['ghdl'],
            cont_yosys=self.conts['yosys'],
            cont_nextpnr_ice40=self.conts['nextpnr-ice40'],
            cont_icetime=self.conts['icetime'],
            cont_icepack=self.conts['icepack'],
            cont_nextpnr_ecp5=self.conts['nextpnr-ecp5'],
            cont_ecppack=self.conts['ecppack'],
            tool_ghdl=self.tools['ghdl'],
            tool_yosys=self.tools['yosys'],
            tool_nextpnr_ice40=self.tools['nextpnr-ice40'],
            tool_icetime=self.tools['icetime'],
            tool_icepack=self.tools['icepack'],
            tool_nextpnr_ecp5=self.tools['nextpnr-ecp5'],
            tool_ecppack=self.tools['ecppack']
        )
        with open(f'{self._TOOL}.sh', 'w', encoding='utf-8') as file:
            file.write(text)

    def generate(self, to_task, from_task, capture):
        if self.frontend == 'ghdl' or 'verilog' in self.backend:
            to_task = 'syn'
            from_task = 'syn'
        return super().generate(to_task, from_task, capture)

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        template = os.path.join(os.path.dirname(__file__), 'openprog.sh')
        with open(template, 'r', encoding='utf-8') as file:
            text = file.read()
        text = text.format(
            family=self.part['family'],
            project=self.project,
            #
            oci_engine=self.oci_engine,
            cont_iceprog=self.conts['iceprog'],
            cont_openocd=self.conts['openocd'],
            tool_iceprog=self.tools['iceprog'],
            tool_openocd=self.tools['openocd']
        )
        with open('openprog.sh', 'w', encoding='utf-8') as file:
            file.write(text)
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
