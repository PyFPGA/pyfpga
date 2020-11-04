#
# Copyright (C) 2019-2020 INTI
# Copyright (C) 2019-2020 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""fpga.project

This module implements the main class of PyFPGA, which provides
functionalities to create a project, generate a bitstream and transfer it to a
Device.
"""

import contextlib
import glob
import inspect
import logging
import os
import re
import time


TOOLS = [
    'ghdl', 'ise', 'libero', 'openflow', 'quartus', 'vivado', 'yosys',
    'yosys-ise', 'yosys-vivado'
]


_log = logging.getLogger(__name__)
_log.level = logging.INFO
_log.addHandler(logging.NullHandler())


class Project:
    """Class to manage an FPGA project."""

    def __init__(
            self, tool='vivado', project=None, init=None,
            relative_to_script=True):
        """Class constructor.

        * **tool:** FPGA tool to be used.
        * **project:** project name (the tool name is used if none specified).
        * **init:** a dict to initialize some parameters.
        * **relative_to_script:** specifies if the files/directories are
        relative to the script or the execution directory.
        """
        if tool == 'ghdl':
            from fpga.tool.openflow import Openflow
            self.tool = Openflow(project, frontend='ghdl', backend='vhdl')
        elif tool in ['ise', 'yosys-ise']:
            from fpga.tool.ise import Ise
            self.tool = Ise(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'libero':
            from fpga.tool.libero import Libero
            self.tool = Libero(project)
        elif tool == 'openflow':
            from fpga.tool.openflow import Openflow
            self.tool = Openflow(project)
        elif tool == 'quartus':
            from fpga.tool.quartus import Quartus
            self.tool = Quartus(project)
        elif tool in ['vivado', 'yosys-vivado']:
            from fpga.tool.vivado import Vivado
            self.tool = Vivado(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'yosys':
            from fpga.tool.openflow import Openflow
            self.tool = Openflow(project, frontend='yosys', backend='verilog')
        else:
            raise NotImplementedError(tool)
        self._rundir = os.getcwd()
        _log.debug('RUNDIR = %s', self._rundir)
        if relative_to_script:
            self._reldir = os.path.dirname(inspect.stack()[-1].filename)
        else:
            self._reldir = ''
        _log.debug('RELDIR = %s', self._reldir)
        self._absdir = os.path.join(self._rundir, self._reldir)
        _log.debug('ABSDIR = %s', self._absdir)
        self.set_outdir('build')
        self._initialize(init)

    def _initialize(self, init):
        """Set some of the most used internal parameters."""
        if init is None:
            return
        if 'outdir' in init:
            _log.debug('OUTDIR = %s', init['outdir'])
            self.set_outdir(init['outdir'])
        if 'part' in init:
            _log.debug('PART = %s', init['part'])
            self.set_part(init['part'])
        if 'paths' in init:
            for path in init['paths']:
                _log.debug('PATH = %s', path)
                self.add_path(path)
        for filetype in ['vhdl', 'verilog', 'constraint']:
            if filetype in init:
                for file in init[filetype]:
                    if isinstance(file, list):
                        filename = file[0]
                        library = file[1]
                    else:
                        filename = file
                        library = None
                    _log.debug(
                        'FILE = %s %s %s', filename, filetype, library
                    )
                    self.add_files(filename, filetype, library)
        if 'params' in init:
            for parname, parvalue in init['params'].items():
                _log.debug('PARAM = %s %s', parname, parvalue)
                self.set_param(parname, parvalue)
        if 'top' in init:
            _log.debug('TOP = %s', init['top'])
            self.set_top(init['top'])

    def set_outdir(self, outdir):
        """Sets the OUTput DIRectory (where to put the resulting files).

        * **outdir:** path to the output directory.
        """
        self.outdir = os.path.normpath(os.path.join(self._absdir, outdir))
        _log.debug('OUTDIR = %s', self.outdir)

    def get_configs(self):
        """Gets the Project Configurations.

        It returns a dict which includes *tool* and *project* names, the
        *extension* of a project file (according to the selected tool) and
        the *part* to be used.
        """
        return self.tool.get_configs()

    def set_part(self, part):
        """Set the target FPGA part.

        * **part:** the FPGA part as specified by the tool.
        """
        self.tool.set_part(part)

    def set_param(self, name, value):
        """Set a Generic/Parameter Value."""
        self.tool.set_param(name, value)

    def add_files(self, pathname, filetype=None, library=None, options=None):
        """Adds files to the project.

        * **pathname:** a relative path to a file, which can contain
        shell-style wildcards (glob compliant).
        * **filetype:** the valid values are *verilog* or *vhdl*, *constraint*
        and *design* (for a graphical block design). It is automatically
        discovered (based on the extension) if None provided (except for
        *design*). The default (autodiscovery failed) is *constraint*.
        * **library:** an optional VHDL library name.
        * **options:** to be provided to the underlying tool.
        """
        pathname = os.path.join(self._absdir, pathname)
        pathname = os.path.normpath(pathname)
        _log.debug('PATHNAME = %s', pathname)
        files = glob.glob(pathname)
        if len(files) == 0:
            raise FileNotFoundError(pathname)
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(file)
            if filetype is None:
                ext = os.path.splitext(file)[1]
                if ext in ['.vhd', '.vhdl']:
                    filetype = 'vhdl'
                elif ext in ['.v', '.sv']:
                    filetype = 'verilog'
                else:
                    filetype = 'constraint'
                _log.debug('add_files: %s filetype detected', filetype)
            file = os.path.relpath(file, self.outdir)
            self.tool.add_file(file, filetype, library, options)

    def get_files(self):
        """Get the files of the project."""
        return self.tool.get_files()

    def add_path(self, path):
        """Add a search path.

        Useful to specify where to search Verilog Included Files or IP
        repositories.

        * **path:** a relative path to a directory.
        """
        path = os.path.join(self._absdir, path)
        path = os.path.normpath(path)
        if os.path.isdir(path):
            path = os.path.relpath(path, self.outdir)
            self.tool.add_path(path)
        else:
            raise NotADirectoryError(path)

    def set_top(self, toplevel):
        """Set the top level of the project.

        * **toplevel:** name or file path of the top level entity/module.
        """
        if os.path.splitext(toplevel)[1]:
            toplevel = os.path.join(self._absdir, toplevel)
            toplevel = os.path.normpath(toplevel)
            if os.path.exists(toplevel):
                with open(toplevel, 'r') as file:
                    hdl = file.read()
                # Removing comments, newlines and carriage-returns
                hdl = re.sub(r'--.*[$\n]|\/\/.*[$\n]', '', hdl)
                hdl = hdl.replace('\n', '').replace('\r', '')
                hdl = re.sub(r'\/\*.*\*\/', '', hdl)
                # Finding modules/entities
                top = re.findall(r'module\s+(\w+)\s*[#(;]', hdl)
                top.extend(re.findall(r'entity\s+(\w+)\s+is', hdl))
                if len(top) > 0:
                    self.tool.set_top(top[-1])
                    if len(top) > 1:
                        _log.warning(
                            'set_top: more than one Top found (last selected)'
                        )
                else:
                    self.tool.set_top('UNDEFINED')
            else:
                raise FileNotFoundError(toplevel)
        else:
            self.tool.set_top(toplevel)

    def add_hook(self, hook, phase='project'):
        """Adds a hook in the specified phase.

        A hook is a place that allows you to insert customized programming.

        The valid **phase** values are:
        * *prefile* to add options needed to find files.
        * *project* to add project related options.
        * *preflow* to change options previous to run the flow.
        * *postsyn* to perform an action between *syn* and *imp*.
        * *postimp* to perform an action between *imp* and *bit*.
        * *postbit* to perform an action after *bit*.

        The *hook* is a string representing a tool specific command.

        **WARNING:** using a hook, you will be probably broken the vendor
        independence.
        """
        self.tool.add_hook(hook, phase)

    def generate(self, to_task='bit', from_task='prj', capture=False):
        """Run the FPGA tool.

        * **to_task:** last task.
        * **from_task:** first task.
        * **capture:** capture STDOUT and STDERR (returned values).

        The valid tasks values, in order, are:
        * *prj* to creates the project file.
        * *syn* to performs the synthesis.
        * *imp* to runs implementation.
        * *bit* to generates the bitstream.
        """
        _log.info(
            'generating "%s" project using "%s" tool into "%s" directory',
            self.tool.project, self.tool.get_configs()['tool'], self.outdir
        )
        with self._run_in_dir():
            if capture:
                _log.info('the execution messages are being captured')
            return self.tool.generate(to_task, from_task, capture)

    def set_bitstream(self, path):
        """Set the bitstream file to transfer.

        * **path:** path to the bitstream file.
        """
        path = os.path.join(self._absdir, path)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.tool.set_bitstream(path)

    def transfer(
            self, devtype='fpga', position=1, part='', width=1,
            capture=False):
        """Transfers the generated bitstream to a device.

        * **devtype:** *fpga* or other valid option
        (depending on the used tool, it could be *spi*, *bpi, etc).
        * **position:** position of the device in the JTAG chain.
        * **part:** name of the memory (when device is not *fpga*).
        * **width:** bits width of the memory (when device is not *fpga*).
        * **capture:** capture STDOUT and STDERR (returned values).
        """
        _log.info(
            'transfering "%s" project using "%s" tool from "%s" directory',
            self.tool.project, self.tool.get_configs()['tool'], self.outdir
        )
        with self._run_in_dir():
            if capture:
                _log.info('the execution messages are being captured')
            return self.tool.transfer(devtype, position, part, width, capture)

    def clean(self):
        """Clean the generated project files."""
        _log.info(
            'cleaning the generated project files into "%s"', self.outdir
        )
        with self._run_in_dir():
            self.tool.clean()

    @contextlib.contextmanager
    def _run_in_dir(self):
        """Runs the tool in other directory."""
        try:
            if not os.path.exists(self.outdir):
                _log.debug('the output directory did not exist (created)')
                os.makedirs(self.outdir)
            os.chdir(self.outdir)
            start = time.time()
            yield
        finally:
            end = time.time()
            os.chdir(self._rundir)
            _log.info('executed in %.3f seconds', end-start)
