#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Vivado.
"""

from pyfpga.project import Project

_TEMPLATES = {
    'fpga': """\
if { [ catch { open_hw_manager } ] } { open_hw }
connect_hw_server
open_hw_target
set obj [lindex [get_hw_devices [current_hw_device]] 0]
set_property PROGRAM.FILE #BITSTREAM# $obj
program_hw_devices $obj
""",
    'detect': """\
if { [ catch { open_hw_manager } ] } { open_hw }
connect_hw_server
open_hw_target
puts [get_hw_devices]
"""
}

# pylint: disable=too-few-public-methods


class Vivado(Project):
    """Class to support Vivado."""

    tool = {
        'def-part': 'xc7k160t-3-fbg484',
        'proj-ext': 'xpr',
        'make-app': 'vivado',
        'make-opt': '-mode batch -notrace -quiet -source vivado.tcl',
        'prog-app': 'vivado',
        'prog-opt': '-mode batch -notrace -quiet -source vivado-prog.tcl',
        'binaries': ['bit']
    }
