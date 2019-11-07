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

"""fpga.tool

Defines the interface to be inherited to support a tool.
"""

import os.path
import subprocess


def check_value(value, values):
    """Check if VALUE is included in VALUES."""
    if value not in values:
        raise ValueError(
            '{} is not a valid value ({})'
            .format(value, " ,".join(values))
        )


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations. There are methods that
    raises a NotImplementedError exception and should be replaced by a tool
    implementation to provide the needed funcionality.
    """

    _TOOL = 'UNDEFINED'
    _EXTENSION = 'UNDEFINED'
    _PART = 'UNDEFINED'

    _GEN_COMMAND = 'UNDEFINED'
    _TRF_COMMAND = 'UNDEFINED'

    _DEVTYPES = []

    def __init__(self, project=None):
        """Initializes the attributes of the class."""
        self.project = self._TOOL if project is None else project
        self.set_part(self._PART)
        self.options = {
            'project': [],
            'preflow': [],
            'postsyn': [],
            'postimp': [],
            'postbit': []
        }
        self.files = []
        self.set_top('undefined')

    def get_configs(self):
        """Get Configurations."""
        return {
            'tool': self._TOOL,
            'project': self.project,
            'extension': self._EXTENSION,
            'part': self.part
        }

    def set_part(self, part):
        """Set the target PART."""
        self.part = part

    def add_file(self, file, lib=None):
        """Add a FILE to the project."""
        command = '    '  # indentation
        command += 'fpga_file %s' % file
        if lib is not None:
            command += ' %s' % lib
        self.files.append(command)

    def set_top(self, top):
        """Set the TOP LEVEL of the project."""
        self.top = top

    _PHASES = ['project', 'preflow', 'postsyn', 'postimp', 'postbit']

    def add_option(self, option, phase):
        """Add the specified OPTION in the desired PHASE."""
        check_value(phase, self._PHASES)
        self.options[phase].append(option)

    def _create_gen_script(self, strategy, task):
        """Create the script for generate execution."""
        template = os.path.join(os.path.dirname(__file__), 'template.tcl')
        tcl = open(template).read()
        tcl = tcl.replace('#TOOL#', self._TOOL)
        tcl = tcl.replace('#PROJECT#', self.project)
        tcl = tcl.replace('#PART#', self.part)
        tcl = tcl.replace('#FILES#', "\n".join(self.files))
        tcl = tcl.replace('#TOP#', self.top)
        tcl = tcl.replace('#STRATEGY#', strategy)
        tcl = tcl.replace('#TASK#', task)
        tcl = tcl.replace('#PROJECT_OPTS#', "\n".join(self.options['project']))
        tcl = tcl.replace('#PREFLOW_OPTS#', "\n".join(self.options['preflow']))
        tcl = tcl.replace('#POSTSYN_OPTS#', "\n".join(self.options['postsyn']))
        tcl = tcl.replace('#POSTIMP_OPTS#', "\n".join(self.options['postimp']))
        tcl = tcl.replace('#POSTBIT_OPTS#', "\n".join(self.options['postbit']))
        open("%s.tcl" % self._TOOL, 'w').write(tcl)

    _STRATEGIES = ['none', 'area', 'speed', 'power']
    _TASKS = ['prj', 'syn', 'imp', 'bit']

    def generate(self, strategy='none', task='bit'):
        """Run the FPGA tool."""
        check_value(strategy, self._STRATEGIES)
        check_value(task, self._TASKS)
        self._create_gen_script(strategy, task)
        subprocess.run(self._GEN_COMMAND, shell=True, check=True)

    def _create_trf_script(self, devtype, position, part, width):
        """Create the script for transfer execution."""
        raise NotImplementedError('_create_trf_script')

    def transfer(self, devtype='fpga', position=1, part=None, width=None):
        """Transfer a bitstream."""
        check_value(devtype, self._DEVTYPES)
        self._create_trf_script(devtype, position, part, width)
        subprocess.run(self._TRF_COMMAND, shell=True, check=True)
