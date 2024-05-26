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

from enum import Enum
from pathlib import Path


class Tool(Enum):
    """Enumeration of supported FPGA tools."""
    GHDL = 'ghdl'
    ISE = 'ise'
    LIBERO = 'libero'
    OPENFLOW = 'openflow'
    QUARTUS = 'quartus'
    VIVADO = 'vivado'
    YOSYS = 'yosys'
    YOSYS_ISE = 'yosys-ise'
    YOSYS_VIVADO = 'yosys-vivado'


class Step(Enum):
    """Enumeration of supported Steps"""
    PRJ = 'prj'
    ELB = 'elb'
    SYN = 'syn'
    PAR = 'par'
    BIT = 'bit'


class Hook(Enum):
    """Enumeration of supported Hooks"""
    PREFILE = 'prefile'
    PROJECT = 'project'
    PREFLOW = 'preflow'
    POSTSYN = 'postsyn'
    POSTPAR = 'postpar'
    POSTBIT = 'postbit'


class Project:
    """Class to manage an FPGA project.

    :param tool: tool name
    :type tool: Tool
    :param name: project name (tool name by default)
    :type name: str, optional
    :param data: pre-populated data for the project
    :type data: dict, optional
    :param odir: output directory
    :type odir: str, optional
    :raises TypeError: when a value is not a valid enum
    :raises NotImplementedError: when a method is not implemented yet
    """

    def __init__(self, tool, name=None, data=None, odir='results'):
        """Class constructor."""
        if not isinstance(tool, Tool):
            raise TypeError('tool must be a Tool enum.')
        if data and not isinstance(data, dict):
            raise TypeError('data must be a dict.')
        self.tool = tool
        self.name = name or tool.value
        self.data = data or {}
        self.odir = Path(odir)
        self.odir.mkdir(parents=True, exist_ok=True)

    def set_part(self, name):
        """Temp placeholder"""
        self.data['part'] = name

    def add_file(self, pathname, filetype=None, library=None, options=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_vlog(self, pathname, options=None):
        """Temp placeholder"""
        self.add_file(pathname, filetype='vlog', options=options)

    def add_slog(self, pathname, options=None):
        """Temp placeholder"""
        self.add_file(pathname, filetype='slog', options=options)

    def add_vhdl(self, pathname, library=None, options=None):
        """Temp placeholder"""
        self.add_file(
            pathname, filetype='vhdl',
            library=library, options=options
        )

    def add_include(self, path):
        """Temp placeholder"""
        if 'includes' not in self.data:
            self.data['includes'] = []
        self.data['includes'].append(path)

    def add_param(self, name, value):
        """Temp placeholder"""
        if 'params' not in self.data:
            self.data['params'] = {}
        self.data['params'][name] = value

    def add_define(self, name, value):
        """Temp placeholder"""
        if 'defines' not in self.data:
            self.data['defines'] = {}
        self.data['defines'][name] = value

    def set_arch(self, name):
        """Temp placeholder"""
        self.data['arch'] = name

    def set_top(self, name):
        """Temp placeholder"""
        self.data['top'] = name

    def add_hook(self, hook, content):
        """Temp placeholder"""
        # if not isinstance(hook, Hook):
        #     raise TypeError('hook must be a Hook enum.')
        raise NotImplementedError('Method is not implemented yet.')

    def make(self, end=Step.BIT, start=Step.PRJ, capture=False):
        """Temp placeholder"""
        # if not isinstance(end, Step) or not isinstance(start, Step):
        #     raise TypeError('start and end must be a Step enum.')
        raise NotImplementedError('Method is not implemented yet.')

    def prog(self, position=1, bitstream=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')
