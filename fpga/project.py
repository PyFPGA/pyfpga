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


TOOLS = ['ghdl', 'ise', 'libero', 'quartus', 'vivado', 'yosys']

COMBINED_TOOLS = ['yosys-ise', 'yosys-vivado']


class Project:
    """Class to manage an FPGA project."""

    def __init__(self, tool='vivado', project=None, relative_to_script=True):
        """Class constructor.

        * **tool:** FPGA tool to be used.
        * **project:** project name (the tool name is used if none specified).
        * **relative_to_script:** specifies if the files/directories are
        relative to the script or the execution directory.
        """
        self._log = logging.getLogger(__name__)
        self._log.level = logging.INFO
        self._log.addHandler(logging.NullHandler())
        # pylint: disable=import-outside-toplevel
        if tool == 'ghdl':
            from fpga.tool.ghdl import Ghdl
            self.tool = Ghdl(project)
        elif tool == 'ise':
            from fpga.tool.ise import Ise
            self.tool = Ise(project)
        elif tool == 'libero':
            from fpga.tool.libero import Libero
            self.tool = Libero(project)
        elif tool == 'quartus':
            from fpga.tool.quartus import Quartus
            self.tool = Quartus(project)
        elif tool == 'tclsh':
            from fpga.tool.tclsh import Tclsh
            self.tool = Tclsh(project)
        elif tool == 'vivado':
            from fpga.tool.vivado import Vivado
            self.tool = Vivado(project)
        elif tool in ['yosys', 'yosys-ise', 'yosys-vivado']:
            from fpga.tool.yosys import Yosys
            args = tool.split('-')
            if len(args) > 1:
                self.tool = Yosys(project, backend=args[1])
            else:
                self.tool = Yosys(project)
        else:
            raise NotImplementedError(tool)
        self._rundir = os.getcwd()
        self._log.debug('RUNDIR = %s', self._rundir)
        if relative_to_script:
            self._reldir = os.path.dirname(inspect.stack()[-1].filename)
        else:
            self._reldir = ''
        self._log.debug('RELDIR = %s', self._reldir)
        self._absdir = os.path.join(self._rundir, self._reldir)
        self._log.debug('ABSDIR = %s', self._absdir)
        self.set_outdir('build')

    def set_outdir(self, outdir):
        """Sets the OUTput DIRectory (where to put the resulting files).

        * **outdir:** path to the output directory.
        """
        self.outdir = os.path.join(self._absdir, outdir)
        self._log.debug('OUTDIR = %s', self.outdir)

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

    def add_design(self, pathname):
        """Adds a Block Design.

        * **pathname:** a string containing a relative path to a file.
        """
        pathname = os.path.join(self._absdir, pathname)
        if os.path.isfile(pathname):
            self.tool.add_file(pathname, None, False, True)
        else:
            self._log.warning('add_design: %s not found.', pathname)

    def add_files(self, pathname, library=None):
        """Adds files to the project (HDLs, TCLs, Constraints).

        * **pathname:** a string containing a relative path specification,
        and can contain shell-style wildcards (glob compliant).
        * **library:** an optional VHDL library name.
        """
        pathname = os.path.join(self._absdir, pathname)
        self._log.debug('PATHNAME = %s', pathname)
        files = glob.glob(pathname)
        if len(files) == 0:
            self._log.warning('add_files: %s not found.', pathname)
        for file in files:
            self.tool.add_file(file, library, False, False)

    def add_include(self, pathname):
        """Adds a search path.

        Useful to specify where to search Verilog Included Files or IP
        repositories.

        * **pathname:** a string containing a relative path to a directory
        or a file.

        **Note:** generally a directory must be specified, but Libero-SoC
        also needs to add the file when is a Verilog Included File.
        """
        pathname = os.path.join(self._absdir, pathname)
        if os.path.exists(pathname):
            self.tool.add_file(pathname, None, True, False)
        else:
            self._log.warning('add_include: %s not found.', pathname)

    def set_top(self, toplevel):
        """Set the top level of the project.

        * **toplevel:** name or file path of the top level entity/module.
        """
        if os.path.splitext(toplevel)[1]:
            toplevel = os.path.join(self._absdir, toplevel)
            if os.path.exists(toplevel):
                hdl = open(toplevel, 'r').read()
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
                        self._log.warning(
                            'set_top: more than one Top found, last selected.'
                        )
                else:
                    self.tool.set_top('UNDEFINED')
            else:
                raise FileNotFoundError(toplevel)
        else:
            self.tool.set_top(toplevel)

    def add_prefile_cmd(self, command):
        """Adds a prefile COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'prefile')

    def add_postprj_cmd(self, command):
        """Adds a postprj COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'postprj')

    def add_preflow_cmd(self, command):
        """Adds a pre flow COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'preflow')

    def add_postsyn_cmd(self, command):
        """Adds a post synthesis COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'postsyn')

    def add_postimp_cmd(self, command):
        """Adds a post implementation COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'postimp')

    def add_postbit_cmd(self, command):
        """Adds a post bitstream generation COMMAND.

        * **command:** a valid, commonly Tcl, tool command.
        """
        self.tool.add_command(command, 'postbit')

    def generate(
            self, strategy='default', to_task='bit', from_task='prj',
            capture=False):
        """Run the FPGA tool.

        * **strategy:** *default*, *area*, *speed* or *power*.
        * **to_task:** last task.
        * **from_task:** first task.
        * **capture:** capture STDOUT and STDERR (returned values).

        The valid tasks values, in order, are:
        * *prj* to creates the project file.
        * *syn* to performs the synthesis.
        * *imp* to runs implementation.
        * *bit* to generates the bitstream.
        """
        with self._run_in_dir():
            if capture:
                self._log.info('The execution messages are being captured.')
            return self.tool.generate(strategy, to_task, from_task, capture)

    def export_hardware(self):
        """Exports files for the development of a Processor System.

        Useful when working with FPGA-SoCs to provide information for the
        development of the Processor System side.
        """
        self.tool.export_hardware()

    def set_board(self, board):
        """Sets a development board to have predefined values.

        * **board:** board name.

        **Note:** Not Yet Implemented.
        """
        raise NotImplementedError('set_board')

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
        with self._run_in_dir():
            if capture:
                self._log.info('The execution messages are being captured.')
            return self.tool.transfer(devtype, position, part, width, capture)

    def clean(self):
        """Clean the generated project files."""
        self._log.info('Cleaning the generated project files.')
        with self._run_in_dir():
            self.tool.clean()

    @contextlib.contextmanager
    def _run_in_dir(self):
        """Runs the tool in other directory."""
        try:
            if not os.path.exists(self.outdir):
                self._log.debug('the output directory did not exist, created.')
                os.makedirs(self.outdir)
            os.chdir(self.outdir)
            start = time.time()
            yield
        finally:
            end = time.time()
            os.chdir(self._rundir)
            self._log.info('executed in %.3f seconds.', end-start)
