#
# Copyright (C) 2026 PyFPGA Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
Implements support for Gowin.
"""

from pathlib import Path
from pyfpga.project import Project


class Gowin(Project):
    """Class to support Gowin projects."""

    def _configure(self):
        tool = 'gowin'
        command = 'gw_sh'
        self.conf['tool'] = tool
        self.conf['make_cmd'] = f'{command} {tool}.tcl'
        self.conf['make_ext'] = 'tcl'
        self.conf['prog_bit'] = ['fs', 'bin']
        self.conf['prog_cmd'] = f'bash {tool}-prog.sh'
        self.conf['prog_ext'] = 'sh'

    def _make_custom(self):
        if 'part' not in self.data:
            self.data['part'] = 'GW2AR-LV18QN88C8/I7'

    # pylint: disable=duplicate-code

    def _get_bitstream(self, bitstream=None):
        if not bitstream:
            project = self.data['project']
            pnr_dir = Path(self.odir) / project / 'impl' / 'pnr'

            for ext in self.conf['prog_bit']:
                candidate = pnr_dir / f'{project}.{ext}'
                if candidate.is_file():
                    bitstream = candidate
                    break
        else:
            bitstream = Path(bitstream)

        if not bitstream or not bitstream.is_file():
            raise FileNotFoundError(bitstream)

        abs_path = self._get_absolute(bitstream, self.conf['prog_ext'])
        return Path(abs_path).as_posix()
