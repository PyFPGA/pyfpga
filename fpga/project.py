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

Main Class of PyFPGA, which provides functionalities to create a project,
generate files and transfer to a Device.
"""

import contextlib
import glob
import inspect
import logging
import os

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado


log = logging.getLogger(__name__)
log.level = logging.INFO
log.addHandler(logging.NullHandler())

class Project:
    """Manage an FPGA project."""

    def __init__(self, tool='vivado', project=None):
        """Instantiate the Tool to use."""
        if tool == 'ise':
            self.tool = Ise(project)
        elif tool == 'libero':
            self.tool = Libero(project)
        elif tool == 'quartus':
            self.tool = Quartus(project)
        elif tool == 'vivado':
            self.tool = Vivado(project)
        else:
            raise NotImplementedError(tool)
        self.rundir = os.getcwd()
        log.debug('RUNDIR = {}'.format(self.rundir))
        self.reldir = os.path.dirname(inspect.stack()[-1].filename)
        log.debug('RELDIR = {}'.format(self.reldir))
        self.set_outdir('build')

    def set_outdir(self, outdir):
        """Set the OUTput DIRectory."""
        auxdir = os.path.join(self.reldir, outdir)
        self.outdir = os.path.join(self.rundir, auxdir)
        log.debug('OUTDIR = {}'.format(self.outdir))

    def get_configs(self):
        """Get the Project Configurations."""
        return self.tool.get_configs()

    def set_part(self, part):
        """Set the target PART."""
        self.tool.set_part(part)

    def add_files(self, pathname, lib=None):
        """Add files to the project.

        PATHNAME must be a string containing an absolute or relative path
        specification, and can contain shell-style wildcards.
        LIB is optional and only useful for VHDL files.
        """
        files = glob.glob(os.path.join(self.reldir, pathname))
        for file in files:
            file_abs = os.path.join(self.rundir, file)
            self.tool.add_file(file_abs, lib)

    def set_top(self, toplevel):
        """Set the TOP LEVEL of the project."""
        self.tool.set_top(toplevel)

    def add_project_opt(self, option):
        """Add a project OPTION."""
        self.tool.add_option(option, 'project')

    def add_preflow_opt(self, option):
        """Add a pre flow OPTION."""
        self.tool.add_option(option, 'preflow')

    def add_postsyn_opt(self, option):
        """Add a post synthesis OPTION."""
        self.tool.add_option(option, 'postsyn')

    def add_postimp_opt(self, option):
        """Add a post implementation OPTION."""
        self.tool.add_option(option, 'postimp')

    def add_postbit_opt(self, option):
        """Add a post bitstream generation OPTION."""
        self.tool.add_option(option, 'postbit')

    def set_strategy(self, strategy):
        """Set the STRATEGY to use.

        The valid STRATEGIES are none (default), area, speed and power.
        """
        self.tool.set_strategy(strategy)

    def set_task(self, task):
        """Set the TASK to perform.

        The valid TASKS are prj to only create the project file, syn for also
        performs the synthesis, imp to add implementation and bit (default)
        to finish with the bitstream generation.
        """
        self.tool.set_task(task)

    def generate(self, strategy=None, task=None):
        """Run the FPGA tool."""
        with self._run_in_dir():
            self.tool.generate(strategy, task)

    def set_device(self, devtype, position=1, part='UNDEFINED', width='1'):
        """Set a device.

        The valid DEVice TYPEs are fpga, spi, bpi and xcf.
        An integer specify the POSITION in the Jtag chain.
        PART is the name of the device.
        WIDTH is used for memories
        """
        self.tool.set_device(devtype, position, part, width)

    def set_board(self, board):
        """Set the board to use.

        A BOARD is a dictionary with predefined devices.
        """
        self.tool.set_board(board)

    def transfer(self, devtype='fpga'):
        """Transfer a bitstream."""
        with self._run_in_dir():
            self.tool.transfer(devtype)

    @contextlib.contextmanager
    def _run_in_dir(self):
        """Run a function in the specified DIRECTORY."""
        try:
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
            os.chdir(self.outdir)
            yield
        finally:
            os.chdir(self.rundir)
