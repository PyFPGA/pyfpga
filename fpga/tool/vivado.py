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

"""fpga.tool.vivado

Implements the support of Vivado (Xilinx).
"""

from fpga.tool import Tool


class Vivado(Tool):
    """Implementation of the class to support Vivado."""

    _TOOL = 'vivado'
    _EXTENSION = 'xpr'
    _DEVICE = 'xc7z010-1-clg400'

    _TCL = {
        'create': """\
    create_project -force $project""",
        'open': """\
    project open $project""",
        'close': """\
    close_project""",
        'area': """\
    set obj [get_runs synth_1]
    set_property strategy "Flow_AreaOptimized_high" $obj
    set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
    set_property "steps.synth_design.args.control_set_opt_threshold" "1" $obj
    set obj [get_runs impl_1]
    set_property strategy "Area_Explore" $obj
    set_property "steps.opt_design.args.directive" "ExploreArea" $obj""",
        'power': """\
    #enable power_opt_design and phys_opt_design
    set obj [get_runs synth_1]
    set_property strategy "Vivado Synthesis Defaults" $obj
    set obj [get_runs impl_1]
    set_property strategy "Power_DefaultOpt" $obj
    set_property "steps.power_opt_design.is_enabled" "1" $obj
    set_property "steps.phys_opt_design.is_enabled" "1" $obj""",
        'speed': """\
    #enable phys_opt_design
    set obj [get_runs synth_1]
    set_property strategy "Flow_PerfOptimized_high" $obj
    set_property "steps.synth_design.args.fanout_limit" "400" $obj
    set_property "steps.synth_design.args.keep_equivalent_registers" "1" $obj
    set_property "steps.synth_design.args.resource_sharing" "off" $obj
    set_property "steps.synth_design.args.no_lc" "1" $obj
    set_property "steps.synth_design.args.shreg_min_size" "5" $obj
    set obj [get_runs impl_1]
    set_property strategy "Performance_Explore" $obj
    set_property "steps.opt_design.args.directive" "Explore" $obj
    set_property "steps.place_design.args.directive" "Explore" $obj
    set_property "steps.phys_opt_design.is_enabled" "1" $obj
    set_property "steps.phys_opt_design.args.directive" "Explore" $obj
    set_property "steps.route_design.args.directive" "Explore" $obj""",
        'syn': """\
    reset_run synth_1
    launch_runs synth_1
    wait_on_run synth_1""",
        'imp': """\
    open_run synth_1
    launch_runs impl_1
    wait_on_run impl_1""",
        'bit': """\
    open_run impl_1
    launch_run impl_1 -to_step write_bitstream
    wait_on_run impl_1"""
    }

    def generate(self):
        print(self.get_tcl())
#        open("%s.tcl" % self._TOOL, 'w').write(tcl)
