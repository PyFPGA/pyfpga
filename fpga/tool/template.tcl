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

set tool     @TOOL
set project  @PROJECT
set strategy @STRATEGY
set task     @TASK

proc fpga_create {} {
@CREATE
}

proc fpga_open {} {
@OPEN
}

proc fpga_close {} {
@CLOSE
}

proc fpga_device {} {
@DEVICE
}

proc fpga_files {} {
@FILES
}

proc fpga_area_opts {} {
@OPTS_AREA
}

proc fpga_power_opts {} {
@OPTS_POWER
}

proc fpga_speed_opts {} {
@OPTS_SPEED
}

proc fpga_run_syn {} {
@SYNTHESIS
}

proc fpga_run_imp {} {
@IMPLEMENTATION
}

proc fpga_run_bit {} {
@BITSTREAM
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
    fpga_create
    fpga_device
    fpga_files
    switch $strategy {
        "area"  {fpga_area_opts}
        "power" {fpga_power_opts}
        "speed" {fpga_speed_opts}
    }
    fpga_options
    fpga_close
} ERRMSG]} {
    puts "ERROR: there was a problem creating a new project.\n"
    puts $ERRMSG
    exit 1
}

#
# Flow
#

if {[catch {
    fpga_open
    if { $TASK=="syn" || $TASK=="imp" || $TASK=="bit" } {
        fpga_pre_flow
        fpga_run_syn
        fpga_post_syn
    }
    if { $TASK=="imp" || $TASK=="bit" } {
        fpga_run_imp
        fpga_post_imp
    }
    if { $TASK=="bit" } {
        fpga_run_bit
        fpga_post_bit
    }
    fpga_close
} ERRMSG]} {
    puts "ERROR: there was a problem running the flow for $TASK.\n"
    puts $ERRMSG
    exit 2
}
