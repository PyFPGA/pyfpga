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

from glob import glob
import os
import subprocess
from shutil import rmtree, which


FILESETS = ['verilog', 'vhdl', 'constraint', 'simulation', 'design']
MEMWIDTHS = [1, 2, 4, 8, 16, 32]
PHASES = ['prefile', 'project', 'preflow', 'postsyn', 'postimp', 'postbit']
TASKS = ['prj', 'syn', 'imp', 'bit']


def check_value(value, values):
    """Check if VALUE is included in VALUES."""
    if value not in values:
        raise ValueError(
            '{} is not a valid value [{}]'
            .format(value, ", ".join(values))
        )


def run(command, capture):
    """Run a command."""
    output = subprocess.PIPE if capture else None
    check = not capture
    result = subprocess.run(
        command, shell=True, check=check, universal_newlines=True,
        stdout=output, stderr=subprocess.STDOUT
    )
    return result.stdout


class Tool:
    """Tool interface.

    It is the basic interface for tool implementations.
    """

    # Following variables are set in each inheritance (if employed)
    _TOOL = None         # tool name
    _EXTENSION = None    # project file extension
    _PART = None         # default device part name
    _GEN_PROGRAM = None  # program used when generate is executed
    _GEN_COMMAND = None  # command to run when generate is executed
    _TRF_PROGRAM = None  # program used when transfer is executed
    _TRF_COMMAND = None  # command to run when transfer is executed
    _BIT_EXT = []        # Supported BITstream EXTensions
    _DEVTYPES = []       # Supported DEVice TYPES
    _CLEAN = []          # Files to be CLEAN

    def __init__(self, project):
        """Initializes the attributes of the class."""
        self.bitstream = None
        self.cmds = {
            'prefile': [],
            'project': [],
            'preflow': [],
            'postsyn': [],
            'postimp': [],
            'postbit': []
        }
        self.filesets = {
            'vhdl': [],
            'verilog': [],
            'constraint': [],
            'simulation': [],
            'design': []
        }
        self.params = []
        self.part = {
            'name': 'UNSET',
            'family': 'UNSET',
            'device': 'UNSET',
            'package': 'UNSET',
            'speed': 'UNSET'
        }
        self.paths = []
        self.presynth = False
        self.project = self._TOOL if project is None else project
        self.set_part(self._PART)
        self.set_top('UNDEFINED')

    def get_configs(self):
        """Get Configurations."""
        return {
            'tool': self._TOOL,
            'project': self.project,
            'extension': self._EXTENSION,
            'part': self.part['name']
        }

    def set_part(self, part):
        """Set the target PART."""
        self.part['name'] = part

    def set_param(self, name, value):
        """Set a Generic/Parameter Value."""
        self.params.append([name, value])

    def add_file(self, file, fileset, library, options):
        """Add a file to the project in the specified **fileset**."""
        check_value(fileset, FILESETS)
        self.filesets[fileset].append([file, library, options])

    def get_fileset(self, fileset):
        """Get the list of files in the specified **fileset**."""
        check_value(fileset, FILESETS)
        files = []
        for file in self.filesets[fileset]:
            files.append(file[0])
        return files

    def add_path(self, path):
        """Add a search path."""
        self.paths.append(path)

    def set_top(self, top):
        """Set the TOP LEVEL of the project."""
        self.top = top

    def add_hook(self, hook, phase):
        """Add the specified *hook* in the desired *phase*."""
        check_value(phase, PHASES)
        self.cmds[phase].append(hook)

    def _create_gen_script(self, tasks):
        """Create the script for generate execution."""
        # Paths and files
        files = []
        if self.presynth:
            files.append('    fpga_file {}.edif'.format(self.project))
        else:
            for path in self.paths:
                files.append('    fpga_include {}'.format(path))
            for file in self.filesets['verilog']:
                files.append('    fpga_file {}'.format(file[0]))
            for file in self.filesets['vhdl']:
                if file[1] is None:
                    files.append('    fpga_file {}'.format(file[0]))
                else:
                    files.append(
                        '    fpga_file {} {}'.format(file[0], file[1])
                    )
        for file in self.filesets['design']:
            files.append('    fpga_design {}'.format(file[0]))
        for file in self.filesets['constraint']:
            files.append('    fpga_file {}'.format(file[0]))
        # Parameters
        params = []
        for param in self.params:
            params.append('{{ {} {} }}'.format(param[0], param[1]))
        # Script creation
        template = os.path.join(os.path.dirname(__file__), 'template.tcl')
        tcl = open(template).read()
        tcl = tcl.replace('#TOOL#', self._TOOL)
        tcl = tcl.replace('#PRESYNTH#', "True" if self.presynth else "False")
        tcl = tcl.replace('#PROJECT#', self.project)
        tcl = tcl.replace('#PART#', self.part['name'])
        tcl = tcl.replace('#FAMILY#', self.part['family'])
        tcl = tcl.replace('#DEVICE#', self.part['device'])
        tcl = tcl.replace('#PACKAGE#', self.part['package'])
        tcl = tcl.replace('#SPEED#', self.part['speed'])
        tcl = tcl.replace('#PARAMS#', ' '.join(params))
        tcl = tcl.replace('#FILES#', '\n'.join(files))
        tcl = tcl.replace('#TOP#', self.top)
        tcl = tcl.replace('#TASKS#', tasks)
        tcl = tcl.replace('#PREFILE_CMDS#', '\n'.join(self.cmds['prefile']))
        tcl = tcl.replace('#PROJECT_CMDS#', '\n'.join(self.cmds['project']))
        tcl = tcl.replace('#PREFLOW_CMDS#', '\n'.join(self.cmds['preflow']))
        tcl = tcl.replace('#POSTSYN_CMDS#', '\n'.join(self.cmds['postsyn']))
        tcl = tcl.replace('#POSTIMP_CMDS#', '\n'.join(self.cmds['postimp']))
        tcl = tcl.replace('#POSTBIT_CMDS#', '\n'.join(self.cmds['postbit']))
        open("%s.tcl" % self._TOOL, 'w').write(tcl)

    def generate(self, to_task, from_task, capture):
        """Run the FPGA tool."""
        if not which(self._GEN_PROGRAM):
            raise RuntimeError(
                'program "{}" not found'.format(self._GEN_PROGRAM)
            )
        check_value(to_task, TASKS)
        check_value(from_task, TASKS)
        to_index = TASKS.index(to_task)
        from_index = TASKS.index(from_task)
        if from_index > to_index:
            raise ValueError(
                'initial task "{}" cannot be later than the last task "{}"'
                .format(from_task, to_task)
            )
        tasks = " ".join(TASKS[from_index:to_index+1])
        self._create_gen_script(tasks)
        return run(self._GEN_COMMAND, capture)

    def set_bitstream(self, path):
        """Set the bitstream file to transfer."""
        self.bitstream = path

    def transfer(self, devtype, position, part, width, capture):
        """Transfer a bitstream."""
        if not which(self._TRF_PROGRAM):
            raise RuntimeError(
                'program "{}" not found'.format(self._TRF_PROGRAM)
            )
        check_value(devtype, self._DEVTYPES)
        check_value(position, range(10))
        isinstance(part, str)
        check_value(width, MEMWIDTHS)
        isinstance(capture, bool)
        # Bitstream autodiscovery
        if not self.bitstream and devtype not in ['detect', 'unlock']:
            bitstream = []
            for ext in self._BIT_EXT:
                bitstream.extend(glob('**/*.{}'.format(ext), recursive=True))
            if len(bitstream) == 0:
                raise FileNotFoundError('bitStream not found')
            self.bitstream = bitstream[0]

    def clean(self):
        """Clean the generated project files."""
        for path in self._CLEAN:
            elements = glob(path)
            for element in elements:
                if os.path.isfile(element):
                    os.remove(element)
                else:
                    rmtree(element)
