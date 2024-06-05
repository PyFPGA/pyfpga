#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""fpga.tool.quartus

Implements the support of Quartus (Intel/Altera).
"""

import re
import subprocess

from fpga.tool import Tool, run


class Quartus(Tool):
    """Implementation of the class to support Quartus."""

    _TOOL = 'quartus'
    _EXTENSION = 'qpf'
    _PART = '10cl120zf780i8g'
    _GEN_PROGRAM = 'quartus_sh'
    _GEN_COMMAND = 'quartus_sh --script quartus.tcl'
    _TRF_PROGRAM = 'quartus_pgm'
    _TRF_COMMAND = 'quartus_pgm -c %s --mode jtag -o "p;%s@%s"'
    _BIT_EXT = ['sof', 'pof']
    _DEVTYPES = ['fpga', 'detect']
    _CLEAN = [
        # directories
        'db', 'incremental_db', 'output_files',
        # files
        '*.done', '*.jdi', '*.log', '*.pin', '*.pof', '*.qws', '*.rpt',
        '*.smsg', '*.sld', '*.sof', '*.sop', '*.summary', '*.txt',
        # pyfpga
        'quartus.tcl'
    ]

    def transfer(self, devtype, position, part, width, capture):
        super().transfer(devtype, position, part, width, capture)
        result = subprocess.run(
            'jtagconfig', shell=True, check=True,
            stdout=subprocess.PIPE, universal_newlines=True
        )
        result = result.stdout
        if devtype == 'detect':
            print(result)
        else:
            cable = re.match(r"1\) (.*) \[", result).groups()[0]
            cmd = self._TRF_COMMAND % (cable, self.bitstream, position)
            result = run(cmd, capture)
        return result
