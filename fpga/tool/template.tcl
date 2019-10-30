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

#
# Things to tuneup (#SOMETHING#) for each project
#

set TOOL     #TOOL#
set PROJECT  #PROJECT#
set STRATEGY #STRATEGY#
set TASK     #TASK#

set FPGA     #FPGA#
set FAMILY   #FAMILY#
set DEVICE   #DEVICE#
set PACKAGE  #PACKAGE#
set SPEED    #SPEED#

proc fpga_files {} {
#FILES#
}

proc fpga_options { PHASE } {
    if {[catch {
        switch $PHASE {
            "project" {
#PROJECT_OPTS#
            }
            "pre-flow" {
#PRE_FLOW_OPTS#
            }
            "post-syn" {
#POST_SYN_OPTS#
            }
            "post-imp" {
#POST_IMP_OPTS#
            }
            "post-bit" {
#POST_BIT_OPTS#
            }
        }
    } ERRMSG]} {
        puts "ERROR: there was a problem applying your $PHASE options.\n"
        puts $ERRMSG
        exit $ERR_PHASE
    }
}

#
# Constants
#

set ERR_PROJECT 1
set ERR_FLOW    2
set ERR_PHASE   3

#
# Procedures for multi vendor support
#

proc fpga_create { TOOL } {
    switch $TOOL {
        "ise"     { project new $PROJECT.xise }
        "libero"  {}
        "quartus" {}
        "vivado"  { create_project -force $PROJECT }
    }
}

proc fpga_open { TOOL } {
    switch $TOOL {
        "ise"     { project open $PROJECT.xise }
        "libero"  {}
        "quartus" {}
        "vivado"  { project open $PROJECT }
    }
}

proc fpga_close { TOOL } {
    switch $TOOL {
        "ise"     { project close }
        "libero"  {}
        "quartus" {}
        "vivado"  { close_project }
    }
}

proc fpga_device { TOOL } {
    switch $TOOL {
        "ise"     {
            project set family  $FAMILY
            project set device  $DEVICE
            project set package $PACKAGE
            project set speed   $SPEED
        }
        "libero"  {
            set_device -family $FAMILY -die $DEVICE -package $PACKAGE -speed $SPEED
        }
        "quartus" {
            set_global_assignment -name DEVICE $FPGA
        }
        "vivado"  {
            set_property "part" $FPGA [current_project]
        }
    }
}

proc fpga_area_opts { TOOL } {
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

proc fpga_power_opts { TOOL } {
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

proc fpga_speed_opts { TOOL } {
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

proc fpga_run_syn { TOOL } {
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

proc fpga_run_imp { TOOL } {
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

proc fpga_run_bit { TOOL } {
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
    fpga_options "project"
    fpga_close $TOOL
} ERRMSG]} {
    puts "ERROR: there was a problem creating a new project.\n"
    puts $ERRMSG
    exit $ERR_PROJECT
}

#
# Flow
#

if {[catch {
    fpga_open $TOOL
    if { $TASK=="syn" || $TASK=="imp" || $TASK=="bit" } {
        fpga_options "pre-flow"
        fpga_run_syn $TOOL
        fpga_options "post-syn"
    }
    if { $TASK=="imp" || $TASK=="bit" } {
        fpga_run_imp $TOOL
        fpga_options "post-imp"
    }
    if { $TASK=="bit" } {
        fpga_run_bit $TOOL
        fpga_options "post-bit"
    }
    fpga_close $TOOL
} ERRMSG]} {
    puts "ERROR: there was a problem running the flow ($TASK).\n"
    puts $ERRMSG
    exit $ERR_FLOW
}
