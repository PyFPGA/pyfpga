#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Base class that implements agnostic methods to deal with FPGA projects.
"""

import logging

from enum import Enum
from pathlib import Path


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
    """Base class to manage an FPGA project.

    :param name: project name (tool name by default)
    :type name: str, optional
    :param odir: output directory
    :type odir: str, optional
    :raises NotImplementedError: when a method is not implemented yet
    """

    def __init__(self, name=None, odir='results'):
        """Class constructor."""
        self.data = {}
        self.name = name
        self.odir = Path(odir)
        self.odir.mkdir(parents=True, exist_ok=True)
        # logging config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_part(self, name):
        """Temp placeholder"""
        self.data['part'] = name

    def add_file(self, pathname, filetype=None, library=None, options=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_cons(self, pathname, options=None):
        """Temp placeholder"""
        self.add_file(pathname, filetype='cons', options=options)

    def add_slog(self, pathname, options=None):
        """Temp placeholder"""
        self.add_file(pathname, filetype='slog', options=options)

    def add_vhdl(self, pathname, library=None, options=None):
        """Temp placeholder"""
        self.add_file(
            pathname, filetype='vhdl',
            library=library, options=options
        )

    def add_vlog(self, pathname, options=None):
        """Temp placeholder"""
        self.add_file(pathname, filetype='vlog', options=options)

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
        raise NotImplementedError('Method is not implemented yet.')

    def make(self, end=Step.BIT, start=Step.PRJ, capture=False):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def prog(self, position=1, bitstream=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def _test_logging(self):
        self.logger.info('It is an INFO message')
        self.logger.debug('It is anDEBUG message')
