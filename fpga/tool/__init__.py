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

    It is the basic interface for tool implementations.
    """

    _TOOL = 'UNDEFINED'
    _EXTENSION = 'UNDEFINED'
    _PART = 'UNDEFINED'

    _GEN_COMMAND = 'UNDEFINED'
    _TRF_COMMAND = 'UNDEFINED'

    _DEVTYPES = []

    def __init__(self, project):
        """Initializes the attributes of the class."""
        self.project = self._TOOL if project is None else project
        self.set_part(self._PART)
        self.options = {
            'prefile': [],
            'postprj': [],
            'preflow': [],
            'postsyn': [],
            'postimp': [],
            'postbit': []
        }
        self.params = []
        self.files = []
        self.set_top('UNDEFINED')

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

    def set_param(self, name, value):
        """Set a Generic/Parameter Value."""
        self.params.append('{ %s %s }' % (name, value))

    def add_file(self, file, library, included):
        """Add a FILE to the project."""
        if library is not None and included:
            raise ValueError(
                'library and included are mutually exclusive arguments'
            )
        command = '    '  # indentation
        if included:
            command += 'fpga_include %s' % file
        else:
            command += 'fpga_file %s' % file
            if library is not None:
                command += ' %s' % library
        self.files.append(command)

    def set_top(self, top):
        """Set the TOP LEVEL of the project."""
        self.top = top

    _PHASES = [
        'prefile', 'postprj',
        'preflow', 'postsyn', 'postimp', 'postbit'
    ]

    def add_option(self, option, phase):
        """Add the specified OPTION in the desired PHASE."""
        check_value(phase, self._PHASES)
        self.options[phase].append(option)

    def _create_gen_script(self, strategy, tasks):
        """Create the script for generate execution."""
        template = os.path.join(os.path.dirname(__file__), 'template.tcl')
        tcl = open(template).read()
        tcl = tcl.replace('#TOOL#', self._TOOL)
        tcl = tcl.replace('#PROJECT#', self.project)
        tcl = tcl.replace('#PART#', self.part)
        tcl = tcl.replace('#PARAMS#', ' '.join(self.params))
        tcl = tcl.replace('#FILES#', '\n'.join(self.files))
        tcl = tcl.replace('#TOP#', self.top)
        tcl = tcl.replace('#STRATEGY#', strategy)
        tcl = tcl.replace('#TASKS#', tasks)
        tcl = tcl.replace('#PREFILE_OPTS#', '\n'.join(self.options['prefile']))
        tcl = tcl.replace('#POSTPRJ_OPTS#', '\n'.join(self.options['postprj']))
        tcl = tcl.replace('#PREFLOW_OPTS#', '\n'.join(self.options['preflow']))
        tcl = tcl.replace('#POSTSYN_OPTS#', '\n'.join(self.options['postsyn']))
        tcl = tcl.replace('#POSTIMP_OPTS#', '\n'.join(self.options['postimp']))
        tcl = tcl.replace('#POSTBIT_OPTS#', '\n'.join(self.options['postbit']))
        open("%s.tcl" % self._TOOL, 'w').write(tcl)

    _STRATEGIES = ['none', 'area', 'speed', 'power']
    _TASKS = ['prj', 'syn', 'imp', 'bit']

    def generate(self, strategy, to_task, from_task, capture):
        """Run the FPGA tool."""
        check_value(strategy, self._STRATEGIES)
        check_value(to_task, self._TASKS)
        check_value(from_task, self._TASKS)
        capture = subprocess.PIPE if capture else None
        to_index = self._TASKS.index(to_task)
        from_index = self._TASKS.index(from_task)
        if from_index > to_index:
            raise ValueError(
                'initial task ({}) cannot be later than the last task ({})'
                .format(from_task, to_task)
            )
        tasks = " ".join(self._TASKS[from_index:to_index+1])
        self._create_gen_script(strategy, tasks)
        return subprocess.run(
            self._GEN_COMMAND, shell=True, check=True,
            universal_newlines=True, stdout=capture, stderr=capture
        )

    def transfer(self, devtype, position, part, width, capture):
        """Transfer a bitstream."""
        # pylint: disable-msg=too-many-arguments
        check_value(devtype, self._DEVTYPES)
        check_value(position, range(10))
        isinstance(part, str)
        check_value(width, [1, 2, 4, 8, 16, 32])
        return subprocess.PIPE if capture else None
