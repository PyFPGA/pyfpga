#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

from pyfpga.project import Project


class Vivado(Project):
    """Class to support Vivado projects."""

    def __init__(self, name='vivado', odir='results'):
        super().__init__(name=name, odir=odir)
        self.set_part('xc7k160t-3-fbg484')

    def _make_prepare(self):
        self.tool['make-app'] = 'vivado'
        self.tool['make-cmd'] = (
            'vivado -mode batch -notrace -quiet -source vivado.tcl'
        )

    def _prog_prepare(self):
        # binaries = ['bit']
        self.tool['prog-app'] = 'vivado'
        self.tool['prog-cmd'] = (
            'vivado -mode batch -notrace -quiet -source vivado-prog.tcl'
        )
