#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Quartus.
"""

# import re
# import subprocess

from pyfpga.project import Project


class Quartus(Project):
    """Class to support Quartus."""

    tool = {
        'program': 'quartus_sh',
        'command': 'quartus_sh --script quartus.tcl',
    }

    tool = {
        'def-part': '10cl120zf780i8g',
        'proj-ext': 'qpf',
        'make-app': 'quartus_sh',
        'make-opt': '--script quartus.tcl',
        'prog-app': 'quartus_pgm',
        'prog-opt': '-c %s --mode jtag -o "p;%s@%s"',
        'binaries': ['sof', 'pof']
    }

#     def transfer(self, devtype, position, part, width, capture):
#         super().transfer(devtype, position, part, width, capture)
#         result = subprocess.run(
#             'jtagconfig', shell=True, check=True,
#             stdout=subprocess.PIPE, universal_newlines=True
#         )
#         result = result.stdout
#         if devtype == 'detect':
#             print(result)
#         else:
#             cable = re.match(r"1\) (.*) \[", result).groups()[0]
#             cmd = self._TRF_COMMAND % (cable, self.bitstream, position)
#             result = run(cmd, capture)
#         return result
