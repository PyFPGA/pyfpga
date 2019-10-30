#
# PyFPGA Master Tcl
#
# Copyright (C) 2015-2019 INTI
# Copyright (C) 2015-2019 Rodrigo A. Melo <rmelo@inti.gob.ar>
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
# Description: Tcl script to create a new project and performs synthesis,
# implementation and bitstream generation.
#
# Note: fpga_ is used to avoid name collisions.
#

set TOOL     @TOOL
set PROJECT  @PROJECT
set STRATEGY @STRATEGY
set TASK     @TASK

proc fpga_create {TOOL} {
    switch $TOOL {
        "ise"     { project new $PROJECT.xise }
        "libero"  {}
        "quartus" {}
        "vivado"  { create_project -force $PROJECT }
    }
}

proc fpga_open {TOOL} {
    switch $TOOL {
        "ise"     { project open $PROJECT.xise }
        "libero"  {}
        "quartus" {}
        "vivado"  { project open $PROJECT }
    }
}

proc fpga_close {TOOL} {
    switch $TOOL {
        "ise"     { project close }
        "libero"  {}
        "quartus" {}
        "vivado"  { close_project }
    }
}

proc fpga_device {} {
@DEVICE
}

proc fpga_files {} {
@FILES
}

proc fpga_area_opts {TOOL} {
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Area"
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
            set obj [get_runs synth_1]
            set_property strategy "Flow_AreaOptimized_high" $obj
            set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
            set_property "steps.synth_design.args.control_set_opt_threshold" "1" $obj
            set obj [get_runs impl_1]
            set_property strategy "Area_Explore" $obj
            set_property "steps.opt_design.args.directive" "ExploreArea" $obj
        }
    }
}

proc fpga_power_opts {TOOL} {
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Area"
            project set "Power Reduction" "true" -process "Synthesize - XST"
            project set "Power Reduction" "high" -process "Map"
            project set "Power Reduction" "true" -process "Place & Route"
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
            #enable power_opt_design and phys_opt_design
            set obj [get_runs synth_1]
            set_property strategy "Vivado Synthesis Defaults" $obj
            set obj [get_runs impl_1]
            set_property strategy "Power_DefaultOpt" $obj
            set_property "steps.power_opt_design.is_enabled" "1" $obj
            set_property "steps.phys_opt_design.is_enabled" "1" $obj
        }
    }
}

proc fpga_speed_opts {TOOL} {
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Speed"
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
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
            set_property "steps.route_design.args.directive" "Explore" $obj
        }
    }
}

proc fpga_run_syn {TOOL} {
    switch $TOOL {
        "ise"     {
            process run "Synthesize" -force rerun
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
            reset_run synth_1
            launch_runs synth_1
            wait_on_run synth_1
        }
    }
}

proc fpga_run_imp {TOOL} {
    switch $TOOL {
        "ise"     {
            process run "Translate" -force rerun
            process run "Map" -force rerun
            process run "Place & Route" -force rerun
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
            open_run synth_1
            launch_runs impl_1
            wait_on_run impl_1
        }
    }
}

proc fpga_run_bit {TOOL} {
    switch $TOOL {
        "ise"     {
            process run "Generate Programming File" -force rerun
        }
        "libero"  {}
        "quartus" {}
        "vivado"  {
            open_run impl_1
            launch_run impl_1 -to_step write_bitstream
            wait_on_run impl_1
        }
    }
}

proc fpga_options {} {
    if {[catch {
@OPTS_PROJECT
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your project options.\n"
        puts $ERRMSG
        exit 3
    }
}

proc fpga_pre_flow {} {
    if {[catch {
@OPTS_PRE_FLOW
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your pre-flow options.\n"
        puts $ERRMSG
        exit 4
    }
}

proc fpga_post_syn {} {
    if {[catch {
@OPTS_POST_SYN
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your post-syn options.\n"
        puts $ERRMSG
        exit 5
    }
}

proc fpga_post_imp {} {
    if {[catch {
@OPTS_POST_IMP
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your post-imp options.\n"
        puts $ERRMSG
        exit 6
    }
}

proc fpga_post_bit {} {
    if {[catch {
@OPTS_POST_BIT
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your post-bit options.\n"
        puts $ERRMSG
        exit 7
    }
}

#
# Project Creation
#

if {[catch {
    fpga_create $TOOL
    fpga_device
    fpga_files
    switch $STRATEGY {
        "area"  {fpga_area_opts  $TOOL}
        "power" {fpga_power_opts $TOOL}
        "speed" {fpga_speed_opts $TOOL}
    }
    fpga_options
    fpga_close $TOOL
} ERRMSG]} {
    puts "ERROR: there was a problem creating a new project.\n"
    puts $ERRMSG
    exit 1
}

#
# Flow
#

if {[catch {
    fpga_open $TOOL
    if { $TASK=="syn" || $TASK=="imp" || $TASK=="bit" } {
        fpga_pre_flow
        fpga_run_syn $TOOL
        fpga_post_syn
    }
    if { $TASK=="imp" || $TASK=="bit" } {
        fpga_run_imp $TOOL
        fpga_post_imp
    }
    if { $TASK=="bit" } {
        fpga_run_bit $TOOL
        fpga_post_bit
    }
    fpga_close $TOOL
} ERRMSG]} {
    puts "ERROR: there was a problem running the flow for $TASK.\n"
    puts $ERRMSG
    exit 2
}
