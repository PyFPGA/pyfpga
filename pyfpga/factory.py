#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A factory class to create FPGA projects.
"""

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.openflow import Openflow
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado

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
            return Openflow(project, frontend='ghdl', backend='vhdl')
        elif tool in ['ise', 'yosys-ise']:
            return Ise(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'libero':
            return Libero(project)
        elif tool == 'openflow':
            return Openflow(project)
        elif tool == 'quartus':
            return Quartus(project)
        elif tool in ['vivado', 'yosys-vivado']:
            return Vivado(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'yosys':
            return Openflow(project, frontend='yosys', backend='verilog')
        else:
            raise NotImplementedError(tool)
