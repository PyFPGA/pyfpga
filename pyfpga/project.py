#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Base class that implements agnostic methods to deal with FPGA projects.
"""

import glob
import logging
import os
import subprocess

from pathlib import Path
from time import time
from jinja2 import Environment, FileSystemLoader


class Project:
    """Base class to manage an FPGA project.

    :param name: project name (tool name when nothing specified)
    :type name: str, optional
    :param odir: output directory
    :type odir: str, optional
    """

    tool = {}

    def __init__(self, name=None, odir='results'):
        """Class constructor."""
        self.data = {}
        self.name = name
        self.odir = odir
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
        """Set the FPGA part name.

        :param name: FPGA part name
        :type name: str
        """
        self.logger.debug('Executing set_part')
        self.data['part'] = name

    def add_include(self, path):
        """Add an Include path.

        Specify where to search for Included Verilog Files, IP repos, etc.

        :param path: path of a directory
        :type name: str
        :raises NotADirectoryError: if path is not a directory
        """
        self.logger.debug('Executing add_include')
        path = Path(path).resolve()
        if not path.is_dir():
            raise NotADirectoryError(path)
        self.data.setdefault('includes', []).append(path)

    def _add_file(self, pathname, hdl=None, lib=None):
        files = glob.glob(pathname, recursive=True)
        if len(files) == 0:
            raise FileNotFoundError(pathname)
        for file in files:
            path = Path(file).resolve()
            attr = {}
            if hdl:
                attr['hdl'] = hdl
            if lib:
                attr['lib'] = lib
            self.data.setdefault('files', {})[path] = attr

    def add_slog(self, pathname):
        """Add System Verilog file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_slog')
        self._add_file(pathname, 'slog')

    def add_vhdl(self, pathname, lib=None):
        """Add VHDL file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :param lib: VHDL library name
        :type lib: str, optional
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_vhdl')
        self._add_file(pathname, 'vhdl', lib)

    def add_vlog(self, pathname):
        """Add Verilog file/s.

        :param pathname: path to a SV file (glob compliant)
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_vlog')
        self._add_file(pathname, 'vlog')

    def add_cons(self, path, when='all'):
        """Add a constraint file.

        :param pathname: path of a file
        :type pathname: str
        :param when: always ('all'), synthesis ('syn') or P&R ('par')
        :type only: str, optional
        :raises FileNotFoundError: if path is not found
        """
        self.logger.debug('Executing add_cons')
        path = Path(path).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        if when not in ['all', 'syn', 'par']:
            raise ValueError('Invalid only.')
        self.data.setdefault('constraints', {})[path] = when

    def add_param(self, name, value):
        """Add a Parameter/Generic Value.

        :param name: parameter/generic name
        :type name: str
        :param value: parameter/generic value
        :type name: str
        """
        self.logger.debug('Executing add_param')
        self.data.setdefault('params', {})[name] = value

    def add_define(self, name, value):
        """Add a Verilog Defile Value.

        :param name: define name
        :type name: str
        :param value: define value
        :type name: str
        """
        self.logger.debug('Executing add_define')
        self.data.setdefault('defines', {})[name] = value

    def add_fileset(self, pathname):
        """Add fileset file/s.

        :param pathname: path to a fileset file
        :type pathname: str
        :raises FileNotFoundError: when pathname is not found
        """
        self.logger.debug('Executing add_fileset')
        if not os.path.exists(pathname):
            raise FileNotFoundError(pathname)
        raise NotImplementedError()

    def set_top(self, name):
        """Set the name of the top level component.

        :param name: top-level name
        :type name: str
        """
        self.logger.debug('Executing set_top')
        self.data['top'] = name

    def add_hook(self, stage, hook):
        """Add a hook in the specific stage.

        A hook is a place that allows you to insert customized code.

        :param stage: where to insert the hook
        :type stage: str
        :param hook: a tool-specific command
        :type hook: str
        :raises ValueError: when stage is invalid
        """
        self.logger.debug('Executing add_hook')
        stages = [
            'precfg', 'postcfg', 'presyn', 'postsyn',
            'prepar', 'postpar', 'prebit', 'postbit'
        ]
        if stage not in stages:
            raise ValueError('Invalid stage.')
        self.data.setdefault('hooks', {}).setdefault(stage, []).append(hook)

    def make(self, first='cfg', last='bit'):
        """Run the underlying tool.

        :param first: first step
        :type first: str, optional
        :param last: last step
        :type last: str, optional
        :raises ValueError: for missing or wrong values
        :raises RuntimeError: error running the needed underlying tool

        .. note:: valid steps are ``cfg``, ``syn``, ``par`` and ``bit``.
        """
        self.logger.debug('Executing make')
        if 'part' not in self.data:
            self.logger.info('Using the default PART')
        steps = {
            'cfg': 'Project Creation',
            'syn': 'Synthesis',
            'par': 'Place and Route',
            'bit': 'Bitstream generation'
        }
        if last not in steps:
            raise ValueError('Invalid last step.')
        if first not in steps:
            raise ValueError('Invalid first step.')
        keys = list(steps.keys())
        index = [keys.index(first), keys.index(last)]
        if index[0] > index[1]:
            raise ValueError('Invalid steps combination.')
        message = f'from {steps[first]} to {steps[last]}'
        if first == last:
            message = steps[first]
        self.logger.info('Running %s', message)
        selected = [step.upper() for step in keys[index[0]:index[1]+1]]
        self._run(self._make_prepare(selected))

    def prog(self, bitstream=None, position=1):
        """Program the FPGA

        :param bitstream: bitstream to be programmed
        :type bitstream: str, optional
        :param position: position of the device in the JTAG chain
        :type position: str, optional
        :raises ValueError: for missing or wrong values
        :raises RuntimeError: error running the needed underlying tool
        """
        self.logger.debug('Executing prog')
        if position not in range(1, 9):
            raise ValueError('Invalid position.')
        self.logger.info('Programming')
        self._run(self._prog_prepare(bitstream, position))

    def _make_prepare(self, steps):
        raise NotImplementedError('Tool-dependent')

    def _prog_prepare(self, bitstream, position):
        raise NotImplementedError('Tool-dependent')

    def _create_file(self, basename, extension, context):
        tempdir = Path(__file__).parent.joinpath('templates')
        jinja_file_loader = FileSystemLoader(str(tempdir))
        jinja_env = Environment(loader=jinja_file_loader)
        jinja_template = jinja_env.get_template(f'{basename}.jinja')
        content = jinja_template.render(context)
        directory = Path(self.odir)
        directory.mkdir(parents=True, exist_ok=True)
        filename = f'{basename}.{extension}'
        with open(directory / filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def _run(self, command):
        num = 20
        error = 0
        old_dir = Path.cwd()
        new_dir = Path(self.odir)
        start = time()
        try:
            os.chdir(new_dir)
            with open('run.log', 'w', encoding='utf-8') as file:
                subprocess.run(
                    command, shell=True, check=True, text=True,
                    stdout=file, stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError:
            with open('run.log', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                last_lines = lines[-num:] if len(lines) >= num else lines
                for line in last_lines:
                    message = line.strip()
                    if len(message):
                        print(f'>> {message}')
            error = 1
        finally:
            os.chdir(old_dir)
            end = time()
            elapsed = end - start
            self.logger.info(
                'Elapsed time %dh %dm %.2fs',
                int(elapsed // 3600),
                int((elapsed % 3600) // 60),
                elapsed % 60
            )
            if error:
                raise RuntimeError('Problem with the underlying tool')
