#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Base class that implements agnostic methods to deal with FPGA projects.
"""

import logging
import os
import subprocess

from enum import Enum
from datetime import datetime
from pathlib import Path
from time import time


class Step(Enum):
    """Enumeration of supported Steps"""
    PRJ = 'prj'
    SYN = 'syn'
    PAR = 'par'
    BIT = 'bit'


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
        self.odir = odir
        # self.odir.mkdir(parents=True, exist_ok=True)
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
        self.logger.debug('Executing set_part')
        self.data['part'] = name

    def add_file(self, pathname, filetype=None, library=None, options=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_cons(self, pathname, options=None):
        """Temp placeholder"""
        self.logger.debug('Executing add_cons')
        self.add_file(pathname, filetype='cons', options=options)

    def add_slog(self, pathname, options=None):
        """Temp placeholder"""
        self.logger.debug('Executing add_slog')
        self.add_file(pathname, filetype='slog', options=options)

    def add_vhdl(self, pathname, library=None, options=None):
        """Temp placeholder"""
        self.logger.debug('Executing add_vhdl')
        self.add_file(
            pathname, filetype='vhdl',
            library=library, options=options
        )

    def add_vlog(self, pathname, options=None):
        """Temp placeholder"""
        self.logger.debug('Executing add_vlog')
        self.add_file(pathname, filetype='vlog', options=options)

    def add_include(self, path):
        """Temp placeholder"""
        self.logger.debug('Executing add_include')
        if 'includes' not in self.data:
            self.data['includes'] = []
        self.data['includes'].append(path)

    def add_param(self, name, value):
        """Temp placeholder"""
        self.logger.debug('Executing add_param')
        if 'params' not in self.data:
            self.data['params'] = {}
        self.data['params'][name] = value

    def add_define(self, name, value):
        """Temp placeholder"""
        self.logger.debug('Executing add_define')
        if 'defines' not in self.data:
            self.data['defines'] = {}
        self.data['defines'][name] = value

    def set_arch(self, name):
        """Temp placeholder"""
        self.logger.debug('Executing set_arch')
        self.data['arch'] = name

    def set_top(self, name):
        """Temp placeholder"""
        self.logger.debug('Executing set_top')
        self.data['top'] = name

    def add_precfg_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_postcfg_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_presyn_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_prepar_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_prebit_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def add_postbit_hook(self, content):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def make(self, end=Step.BIT, start=Step.PRJ, capture=False):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def prog(self, position=1, bitstream=None):
        """Temp placeholder"""
        raise NotImplementedError('Method is not implemented yet.')

    def _run(self, command):
        self.logger.info('Running the underlying tool (%s)', datetime.now())
        run_error = 0
        old_dir = Path.cwd()
        new_dir = Path(self.odir)
        start = time.time()
        try:
            os.chdir(new_dir)
            with open('run.log', 'w', encoding='utf-8') as logfile:
                subprocess.run(
                    command, shell=True, check=True, text=True,
                    stdout=logfile, stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError:
            with open('run.log', 'r', encoding='utf-8') as logfile:
                lines = logfile.readlines()
                last_lines = lines[-10:] if len(lines) >= 10 else lines
                for line in last_lines:
                    self.logger.error(line.strip())
            run_error = 1
        finally:
            os.chdir(old_dir)
            end = time.time()
            self.logger.info('Done (%s)', datetime.now())
            elapsed = end - start
            self.logger.info(
                'Elapsed time %dh %dm %.2fs',
                int(elapsed // 3600),
                int((elapsed % 3600) // 60),
                elapsed % 60
            )
            if run_error:
                raise RuntimeError('Error running the underlying tool')
