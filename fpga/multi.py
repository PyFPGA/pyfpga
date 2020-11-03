#
# Copyright (C) 2020 Rodrigo A. Melo
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

"""fpga.multi

This module implements a class to deal with multiple projects at once, based
on a dictionary with METADATA.
"""

from fpga.project import Project


class Multi:
    """Class to deal with multiple projects."""

    def __init__(self, meta):
        """Class constructor."""
        self.meta = meta

    def generate(self, task='bit'):
        """Generates the provided projects."""
        for project, data in self.meta.items():
            print('>>> %s' % project)
            if 'tool' in data:
                tool = data['tool']
            else:
                tool = 'openflow'
            print('* TOOL = %s' % tool)
            prj = Project(tool, project)
            if 'outdir' in data:
                print('* OUTDIR = %s' % data['outdir'])
                prj.set_outdir(data['outdir'])
            if 'part' in data:
                print('* PART = %s' % data['part'])
                prj.set_part(data['part'])
            if 'paths' in data:
                print('* PATHS')
                for path in data['paths']:
                    print('  * %s' % path)
                    prj.add_path(path)
            if 'files' in data:
                for filetype in data['files']:
                    print('* %s files' % filetype)
                    for file in data['files'][filetype]:
                        filename = file[0]
                        library = file[1] if len(file) > 1 else ''
                        print('  * %s (%s)' % (filename, library))
                        prj.add_files(filename, filetype, library)
            if 'params' in data:
                for param, value in data['params'].items():
                    print('* PARAM %s = %s' % (param, value))
                    prj.set_param(param, value)
            if 'top' in data:
                prj.set_top(data['top'])
            try:
                prj.generate(task)
            except RuntimeError:
                print('ERROR: tool not found')

    def dump(self):
        """Fake function to avoid PyLint errors."""
        print(self.meta)
