#
# Copyright (C) 2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A factory class to create FPGA projects.
"""

from pyfpga.ise import Ise
from pyfpga.libero import Libero
from pyfpga.openflow import Openflow
from pyfpga.quartus import Quartus
from pyfpga.vivado import Vivado

# pylint: disable=return-in-init
# pylint: disable=no-else-return
# pylint: disable=too-many-return-statements
# pylint: disable=too-few-public-methods


class Factory:
    """A factory class to create FPGA projects."""

    def __init__(
            self, tool='vivado', project=None):
        """Class constructor."""
        if tool == 'ghdl':
            return Openflow(project)  # , frontend='ghdl', backend='vhdl')
        elif tool == 'ise':
            return Ise(project)
        elif tool == 'libero':
            return Libero(project)
        elif tool == 'openflow':
            return Openflow(project)
        elif tool == 'quartus':
            return Quartus(project)
        elif tool == 'vivado':
            return Vivado(project)
        elif tool == 'yosys':
            return Openflow(project)  # , frontend='yosys', backend='verilog')
        else:
            raise NotImplementedError(tool)
