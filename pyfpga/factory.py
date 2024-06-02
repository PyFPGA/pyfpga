#
# Copyright (C) 2019-2024 Rodrigo A. Melo
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
A factory class to create FPGA projects.
"""

import inspect
import logging
import os

from fpga.tool.ise import Ise
from fpga.tool.libero import Libero
from fpga.tool.openflow import Openflow
from fpga.tool.quartus import Quartus
from fpga.tool.vivado import Vivado


TOOLS = [
    'ghdl', 'ise', 'libero', 'openflow', 'quartus', 'vivado', 'yosys',
    'yosys-ise', 'yosys-vivado'
]


_log = logging.getLogger(__name__)
_log.level = logging.INFO
_log.addHandler(logging.NullHandler())


class Project:
    """Class to manage an FPGA project.

    :param tool: FPGA tool to be used
    :param project: project name (the tool name is used if none specified)
    :param meta: a dict with metadata about the project
    :param relative_to_script: specifies if the files/directories are relative
     to the script or the execution directory
    :raises NotImplementedError: when tool is unsupported

    .. note:: Valid values for **tool** are ``ghdl``, ``ise``, ``libero``,
     ``openflow``, ``quartus``, ``vivado``, ``yosys``, ``yosys-ise`` and
     ``yosys-vivado``
    """

    def __init__(
            self, tool='vivado', project=None,
            relative_to_script=True):
        """Class constructor."""
        if tool == 'ghdl':
            self.tool = Openflow(project, frontend='ghdl', backend='vhdl')
        elif tool in ['ise', 'yosys-ise']:
            self.tool = Ise(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'libero':
            self.tool = Libero(project)
        elif tool == 'openflow':
            self.tool = Openflow(project)
        elif tool == 'quartus':
            self.tool = Quartus(project)
        elif tool in ['vivado', 'yosys-vivado']:
            self.tool = Vivado(project, 'yosys' if 'yosys' in tool else '')
        elif tool == 'yosys':
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

    def add_hook(self, hook, phase='project'):
        """Adds a hook in the specified phase.

        A hook is a place that allows you to insert customized programming.

        :param hook: is a string representing a tool specific command
        :param phase: the phase where to insert a hook
        :raises ValueError: when phase is unsupported

        .. note:: Valid values for *phase* are
         ``prefile`` (to add options needed to find files),
         ``project`` (to add project related options),
         ``preflow`` (to change options previous to run the flow),
         ``postsyn`` (to perform an action between *syn* and *par*),
         ``postpar`` (to perform an action between *par* and *bit*) and
         ``postbit`` (to perform an action after *bit*)

        .. warning:: Using a hook, you will be probably broken the vendor
         independence
        """
        self.tool.add_hook(hook, phase)

    def generate(self, to_task='bit', from_task='prj', capture=False):
        """Run the FPGA tool.

        :param to_task: last task
        :param from_task: first task
        :param capture: capture STDOUT and STDERR
        :returns: STDOUT and STDERR messages
        :raises ValueError: when from_task is later than to_task
        :raises ValueError: when to_task or from_task are unsupported
        :raises RuntimeError: when the tool to be used is not found

        .. note:: Valid values for **tasks** are
         ``prj`` (to creates the project file),
         ``syn`` (to performs the synthesis),
         ``imp`` (to runs implementation) and
         ``bit`` (to generates the bitstream)
        """
        # _log.info(
        #     'generating "%s" project using "%s" tool into "%s" directory',
        #     self.tool.project, self.tool.get_configs()['tool'], self.outdir
        # )
        if capture:
            _log.info('the execution messages are being captured')
        return self.tool.generate(to_task, from_task, capture)

    def set_bitstream(self, path):
        """Set the bitstream file to transfer.

        :param path: path to the bitstream file
        """
        path = os.path.join(self._absdir, path)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.tool.set_bitstream(path)

    def transfer(
            self, devtype='fpga', position=1, part='', width=1):
        """Transfers the generated bitstream to a device.

        :param devtype: *fpga* or other valid option
         (depending on the used tool, it could be *spi*, *bpi*, etc)
        :param position: position of the device in the JTAG chain
        :param part: name of the memory (when device is not *fpga*)
        :param width: bits width of the memory (when device is not *fpga*)
        :returns: STDOUT and STDERR messages
        :raises FileNotFoundError: when the bitstream is not found
        :raises ValueError: when devtype, position or width are unsupported
        :raises RuntimeError: when the tool to be used is not found
        """
        # _log.info(
        #     'transfering "%s" project using "%s" tool from "%s" directory',
        #     self.tool.project, self.tool.get_configs()['tool'], self.outdir
        # )
        return self.tool.transfer(devtype, position, part, width, True)
