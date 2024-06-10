#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Quartus.
"""

# import re

from pyfpga.project import Project


class Quartus(Project):
    """Class to support Quartus projects."""

    def __init__(self, name='quartus', odir='results'):
        super().__init__(name=name, odir=odir)
        self.set_part('10cl120zf780i8g')

    def _make_prepare(self, steps):
        self.tool['make-app'] = 'quartus_sh'
        self.tool['make-cmd'] = 'quartus_sh --script quartus.tcl'

    def _prog_prepare(self):
        # binaries = ['sof', 'pof']
        self.tool['prog-app'] = 'quartus_pgm'
        self.tool['prog-cmd'] = 'bash quartus-prog.sh'

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
