#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""pyfpga.project
This module implements the entry-point of PyFPGA, which provides
functionalities to create a project, generate a bitstream and
program a device.
"""

from pathlib import Path

TASKS = ['prj', 'elb', 'syn', 'par', 'bit']

TOOLS = [
    'ghdl',
    'ise',
    'libero',
    'openflow',
    'quartus',
    'vivado',
    'yosys',
    'yosys-ise',
    'yosys-vivado'
]


class Project:
    """Class to manage an FPGA project.

    :param tool: tool name
    :type tool: str
    :param name: project name (tool name by default)
    :type name: str, optional
    :param data: pre-populated data for the project
    :type data: dict, optional
    :param odir: output directory
    :type odir: str, optional
    :raises NotImplementedError: unsupported tool

    .. note::
     Supported tool names are:
     ``ghdl``
     ``ise``
     ``libero``
     ``openflow``
     ``quartus``
     ``vivado``
     ``yosys``
     ``yosys-ise``
     ``yosys-vivado``
    """

    def __init__(self, tool, name=None, data=None, odir='results'):
        """Class constructor."""
        if tool not in TOOLS:
            raise NotImplementedError(f'unsupported tool ({tool}).')
        self.tool = tool
        self.name = name or tool
        self.data = data or {}
        self.odir = Path(odir)
        self.odir.mkdir(parents=True, exist_ok=True)

    def set_part(self, name):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_file(self, pathname, filetype=None, library=None, options=None):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_vlog(self, pathname, options=None):
        """Templ placeholder"""
        self.add_file(pathname, filetype='vlog', options=options)

    def add_slog(self, pathname, options=None):
        """Templ placeholder"""
        self.add_file(pathname, filetype='slog', options=options)

    def add_vhdl(self, pathname, library=None, options=None):
        """Templ placeholder"""
        self.add_file(
            pathname, filetype='vhdl',
            library=library, options=options
        )

    def add_param(self, name, value):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_include(self, path):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_define(self, name, value):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def set_arch(self, name):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def set_top(self, name):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_hook(self, stage, hook):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def make(self, last='bit', first='prj', capture=False):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def prog(self, position=1, bitstream=None):
        """Templ placeholder"""
        raise NotImplementedError('Method is not implemented yet.')
