#
# Copyright (C) 2019 INTI
# Copyright (C) 2019 Rodrigo A. Melo
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

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado
from fpga.tool.tclsh import Tclsh


TOOLS = ['ise', 'libero', 'quartus', 'vivado']


class Project:
    """Class to manage an FPGA project."""

    def __init__(self, tool='vivado', project=None):
        """Class constructor.

        * **tool:** FPGA tool to be used.
        * **project:** project name (the tool name is used if none specified).
        """
        self._log = logging.getLogger(__name__)
        self._log.level = logging.INFO
        self._log.addHandler(logging.NullHandler())
        if tool == 'ise':
            self.tool = Ise(project)
        elif tool == 'libero':
            self.tool = Libero(project)
        elif tool == 'quartus':
            self.tool = Quartus(project)
        elif tool == 'vivado':
            self.tool = Vivado(project)
        elif tool == 'tclsh':
            self.tool = Tclsh(project)
        else:
            raise NotImplementedError(tool)
        self._rundir = os.getcwd()
        self._log.debug('RUNDIR = %s', self._rundir)
        self._reldir = os.path.dirname(inspect.stack()[-1].filename)
        self._log.debug('RELDIR = %s', self._reldir)
        self.set_outdir('build')

    def set_outdir(self, outdir):
        """Sets the OUTput DIRectory (where to put the resulting files).

        * **outdir:** path to the output directory.
        """
        auxdir = os.path.join(self._reldir, outdir)
        self.outdir = os.path.join(self._rundir, auxdir)
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

    def add_files(self, pathname, library=None, included=False):
        """Adds files to the project (HDLs, TCLs, Constraints).

        * **pathname:** a string containing a relative path specification,
        and can contain shell-style wildcards (glob compliant).
        * **library:** VHDL library name.
        * **included:** Verilog included file.

        Note: **library** and **included** are mutually exclusive.
        """
        pathname = os.path.join(self._reldir, pathname)
        self._log.debug('PATHNAME = %s', pathname)
        files = glob.glob(pathname)
        if len(files) == 0:
            self._log.warning('add_files: %s not found', pathname)
        for file in files:
            file_abs = os.path.join(self._rundir, file)
            self.tool.add_file(file_abs, library, included)

    def set_top(self, toplevel):
        """Set the top level of the project.

        * **toplevel:** name or file path of the top level entity/module.
        """
        if os.path.splitext(toplevel)[1]:
            toplevel = os.path.join(self._reldir, toplevel)
            if os.path.exists(toplevel):
                hdl = open(toplevel, 'r').read()
                top = re.findall(r'module\s+(\w+)', hdl)
                top.extend(re.findall(r'entity\s+(\w+)', hdl))
                if len(top) > 0:
                    self.tool.set_top(top[0])
                else:
                    self.tool.set_top('UNDEFINED')
            else:
                raise FileNotFoundError(toplevel)
        else:
            self.tool.set_top(toplevel)

    def add_prefile_opt(self, option):
        """Adds a prefile OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'prefile')

    def add_postprj_opt(self, option):
        """Adds a postprj OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'postprj')

    def add_preflow_opt(self, option):
        """Adds a pre flow OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'preflow')

    def add_postsyn_opt(self, option):
        """Adds a post synthesis OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'postsyn')

    def add_postimp_opt(self, option):
        """Adds a post implementation OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'postimp')

    def add_postbit_opt(self, option):
        """Adds a post bitstream generation OPTION.

        * **option:** a valid, commonly Tcl, tool option.
        """
        self.tool.add_option(option, 'postbit')

    def generate(self, strategy='none', to_task='bit', from_task='prj'):
        """Run the FPGA tool.

        * **strategy:** *none*, *area*, *speed* or *power*.
        * **to_task:** last task.
        * **from_task:** first task.

        The valid tasks values, in order, are:
        * *prj* to creates the project file.
        * *syn* to performs the synthesis.
        * *imp* to runs implementation.
        * *bit* to generates the bitstream.
        """
        with self._run_in_dir():
            self.tool.generate(strategy, to_task, from_task)

    def set_board(self, board):
        """Sets a development board to have predefined values.

        * **board:** board name.

        **Note:** Not Yet Implemented.
        """
        raise NotImplementedError('set_board')

    def transfer(self, devtype='fpga', position=1, part='', width=1):
        """Transfers the generated bitstream to a device.

        * **devtype:** *fpga* or other valid option
        (depending on the used tool, it could be *spi*, *bpi, etc).
        * **position:** position of the device in the JTAG chain.
        * **part:** name of the memory (when device is not *fpga*).
        * **width:** bits width of the memory (when device is not *fpga*).
        """
        with self._run_in_dir():
            self.tool.transfer(devtype, position, part, width)

    @contextlib.contextmanager
    def _run_in_dir(self):
        """Runs the tool in other directory."""
        try:
            start = time.time()
            if not os.path.exists(self.outdir):
                self._log.debug('the output directory did not exist, created.')
                os.makedirs(self.outdir)
            os.chdir(self.outdir)
            yield
        finally:
            os.chdir(self._rundir)
            end = time.time()
            self._log.info('executed in %.3f seconds.', end-start)
