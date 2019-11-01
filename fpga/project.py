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
import os

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado


@contextlib.contextmanager
def _run_in_dir(directory):
    """Run a function in the specified DIRECTORY."""
    rundir = os.getcwd()
    outdir = os.path.join(rundir, directory)
    try:
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        os.chdir(outdir)
        yield
    finally:
        os.chdir(rundir)


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
        self.set_outdir('build')

    def get_config(self):
        """Get the Project Configurations."""
        return self.tool.get_config()

    def set_outdir(self, outdir):
        """Set the OUTput DIRectory."""
        self.outdir = outdir

    def set_part(self, part):
        """Set the target PART."""
        self.tool.set_part(part)

    def add_files(self, pathname, lib=None):
        """Add files to the project.

        PATHNAME must be a string containing an absolute or relative path
        specification, and can contain shell-style wildcards.
        LIB is optional and only useful for VHDL files.
        """
        path = os.getcwd()
        files = glob.glob(pathname)
        for file in files:
            file_abs = os.path.join(path, file)
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

    def generate(self, strategy='none', task='bit'):
        """Run the FPGA tool."""
        with _run_in_dir(self.outdir):
            self.tool.generate(strategy, task)

    def set_hard(self, devtype, position, name, width):
        """Set hardware configurations for the programmer."""
        self.tool.set_hard(devtype, position, name, width)

    def transfer(self):
        """Transfer a bitstream."""
        with _run_in_dir(self.outdir):
            self.tool.transfer()
