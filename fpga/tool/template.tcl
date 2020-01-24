#
# PyFPGA Master Tcl
#
# Copyright (C) 2015-2020 INTI
# Copyright (C) 2015-2020 Rodrigo A. Melo <rmelo@inti.gob.ar>
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
# Supported TOOLs: ise, libero, quartus, vivado, yosys
#
# Notes:
# * fpga_ is used to avoid name collisions.
# * The 'in' operator was introduced by Tcl 8.5, but some Tools uses 8.4,
#   so 'lsearch' is used to test if a value is in a list.
#

#
# Things to tuneup (#SOMETHING#) for each project
#

global TOOL
set TOOL     #TOOL#
# To use with Yosys
set BACKEND  #BACKEND#
set PROJECT  #PROJECT#
set PART     #PART#
set TOP      #TOP#
# STRATEGY = none area power speed
set STRATEGY #STRATEGY#
# TASKS = prj syn imp bit
set TASKS    [list #TASKS#]

set PARAMS   [list #PARAMS#]

proc fpga_files {} {
#FILES#
}

proc fpga_options { PHASE } {
    fpga_print "setting options for the phase '$PHASE'"
    switch $PHASE {
        "prefile" {
#PREFILE_OPTS#
        }
        "postprj" {
#POSTPRJ_OPTS#
        }
        "preflow" {
#PREFLOW_OPTS#
        }
        "postsyn" {
#POSTSYN_OPTS#
        }
        "postimp" {
#POSTIMP_OPTS#
        }
        "postbit" {
#POSTBIT_OPTS#
        }
    }
}

#
# Procedures
#

proc fpga_print { MSG } {
    global TOOL
    puts ">>> PyFPGA ($TOOL): $MSG"
}

proc fpga_create { PROJECT } {
    global TOOL
    fpga_print "creating the project '$PROJECT'"
    switch $TOOL {
        "ise"     {
            if { [ file exists $PROJECT.xise ] } { file delete $PROJECT.xise }
            project new $PROJECT.xise
        }
        "libero"  {
            if { [ file exists $PROJECT ] } { file delete -force -- $PROJECT }
            new_project -name $PROJECT -location $PROJECT -hdl {VHDL} -family {SmartFusion2}
        }
        "quartus" {
            package require ::quartus::project
            project_new $PROJECT -overwrite
            set_global_assignment -name NUM_PARALLEL_PROCESSORS ALL
        }
        "vivado"  { create_project -force $PROJECT }
        "yosys"   { yosys -import }
    }
}

proc fpga_open { PROJECT } {
    global TOOL
    fpga_print "opening the project '$PROJECT'"
    switch $TOOL {
        "ise"     { project open $PROJECT.xise }
        "libero"  {
            open_project $PROJECT/$PROJECT.prjx
        }
        "quartus" {
            package require ::quartus::flow
            project_open -force $PROJECT.qpf
        }
        "vivado"  { open_project $PROJECT }
        "yosys"   { }
    }
}

proc fpga_close {} {
    global TOOL
    fpga_print "closing the project"
    switch $TOOL {
        "ise"     { project close }
        "libero"  { close_project }
        "quartus" { project_close }
        "vivado"  { close_project }
        "yosys"   { }
    }
}

proc fpga_part { PART } {
    global TOOL
    fpga_print "adding the part '$PART'"
    switch $TOOL {
        "ise"     {
            regexp -nocase {(.*)(-.*)-(.*)} $PART -> DEVICE SPEED PACKAGE
            set FAMILY "Unknown"
            if {[regexp -nocase {xc7a\d+l} $DEVICE]} {
                set FAMILY "artix7l"
            } elseif {[regexp -nocase {xc7a} $DEVICE]} {
                set FAMILY "artix7"
            } elseif {[regexp -nocase {xc7k\d+l} $DEVICE]} {
                set FAMILY "kintex7l"
            } elseif {[regexp -nocase {xc7k} $DEVICE]} {
                set FAMILY "kintex7"
            } elseif {[regexp -nocase {xc3sd\d+a} $DEVICE]} {
                set FAMILY "spartan3adsp"
            } elseif {[regexp -nocase {xc3s\d+a} $DEVICE]} {
                set FAMILY "spartan3a"
            } elseif {[regexp -nocase {xc3s\d+e} $DEVICE]} {
                set FAMILY "spartan3e"
            } elseif {[regexp -nocase {xc3s} $DEVICE]} {
                set FAMILY "spartan3"
            } elseif {[regexp -nocase {xc6s\d+l} $DEVICE]} {
                set FAMILY "spartan6l"
            } elseif {[regexp -nocase {xc6s} $DEVICE]} {
                set FAMILY "spartan6"
            } elseif {[regexp -nocase {xc4v} $DEVICE]} {
                set FAMILY "virtex4"
            } elseif {[regexp -nocase {xc5v} $DEVICE]} {
                set FAMILY "virtex5"
            } elseif {[regexp -nocase {xc6v\d+l} $DEVICE]} {
                set FAMILY "virtex6l"
            } elseif {[regexp -nocase {xc6v} $DEVICE]} {
                set FAMILY "virtex6"
            } elseif {[regexp -nocase {xc7v\d+l} $DEVICE]} {
                set FAMILY "virtex7l"
            } elseif {[regexp -nocase {xc7v} $DEVICE]} {
                set FAMILY "virtex7"
            } elseif {[regexp -nocase {xc7z} $DEVICE]} {
                set FAMILY "zynq"
            } else {
                puts "The family of the device $DEVICE is $FAMILY"
            }
            project set family  $FAMILY
            project set device  $DEVICE
            project set package $PACKAGE
            project set speed   $SPEED
        }
        "libero"  {
            regexp -nocase {(.*)(-.*)-(.*)} $PART -> DEVICE SPEED PACKAGE
            set FAMILY "Unknown"
            if {[regexp -nocase {m2s} $DEVICE]} {
                set FAMILY "SmartFusion2"
            } elseif {[regexp -nocase {m2gl} $DEVICE]} {
                set FAMILY "Igloo2"
            } elseif {[regexp -nocase {rt4g} $DEVICE]} {
                set FAMILY "RTG4"
            } elseif {[regexp -nocase {mpf} $DEVICE]} {
                set FAMILY "PolarFire"
            } elseif {[regexp -nocase {a2f} $DEVICE]} {
                set FAMILY "SmartFusion"
            } elseif {[regexp -nocase {afs} $DEVICE]} {
                set FAMILY "Fusion"
            } elseif {[regexp -nocase {aglp} $DEVICE]} {
                set FAMILY "IGLOO+"
            } elseif {[regexp -nocase {agle} $DEVICE]} {
                set FAMILY "IGLOOE"
            } elseif {[regexp -nocase {agl} $DEVICE]} {
                set FAMILY "IGLOO"
            } elseif {[regexp -nocase {a3p\d+l} $DEVICE]} {
                set FAMILY "ProAsic3L"
            } elseif {[regexp -nocase {a3pe} $DEVICE]} {
                set FAMILY "ProAsic3E"
            } elseif {[regexp -nocase {a3p} $DEVICE]} {
                set FAMILY "ProAsic3"
            } else {
                puts "The family of the device $DEVICE is $FAMILY"
            }
            if { $SPEED == "-STD" } { set SPEED "STD"}
            set_device -family $FAMILY -die $DEVICE -package $PACKAGE -speed $SPEED
        }
        "quartus" {
            set_global_assignment -name DEVICE $PART
        }
        "vivado"  {
            set_property "part" $PART [current_project]
        }
        "yosys"   {
            global FAMILY
            set FAMILY "Unknown"
            if {[regexp -nocase {xcup} $PART]} {
                set FAMILY "xcup"
            } elseif {[regexp -nocase {xcu} $PART]} {
                set FAMILY "xcu"
            } elseif {[regexp -nocase {xc7} $PART]} {
                set FAMILY "xc7"
            } elseif {[regexp -nocase {xc6v} $PART]} {
                set FAMILY "xc6v"
            } elseif {[regexp -nocase {xc6s} $PART]} {
                set FAMILY "xc6s"
            } elseif {[regexp -nocase {xc5v} $PART]} {
                set FAMILY "xc5v"
            } else {
                puts "The family of the part $PART is $FAMILY"
            }
        }
    }
}

proc fpga_params {} {
    global TOOL PARAMS
    if { [llength $PARAMS] == 0 } { return }
    fpga_print "setting generics/parameters"
    switch $TOOL {
        "ise"     {
            set assigns [list]
            foreach PARAM $PARAMS { lappend assigns [join $PARAM "="] }
            project set "Generics, Parameters" "[join $assigns]" -process "Synthesize - XST"
        }
        "libero"  {
            # They must be specified after set_root (see fpga_top)
        }
        "quartus" {
            foreach PARAM $PARAMS {
                eval "set_parameter -name $PARAM"
            }
        }
        "vivado"  {
            set assigns [list]
            foreach PARAM $PARAMS { lappend assigns [join $PARAM "="] }
            set obj [get_filesets sources_1]
            set_property "generic" "[join $assigns]" -objects $obj
        }
        "yosys"   { puts "Not yet implemented" }
    }
}

proc fpga_file {FILE {LIBRARY "work"}} {
    global TOOL TOP
    set message "adding the file '$FILE'"
    if { $LIBRARY != "work" } { append message " (into the VHDL library '$LIBRARY')" }
    fpga_print $message
    regexp -nocase {\.(\w*)$} $FILE -> ext
    if { $ext == "tcl" } {
        source $FILE
        return
    }
    switch $TOOL {
        "ise" {
            if {$ext == "xcf"} {
                project set "Synthesis Constraints File" $FILE -process "Synthesize - XST"
            } elseif { $LIBRARY != "work" } {
                lib_vhdl new $LIBRARY
                xfile add $FILE -lib_vhdl $LIBRARY
            } else {
                xfile add $FILE
            }
        }
        "libero" {
            global LIBERO_PLACE_CONSTRAINTS
            global LIBERO_OTHER_CONSTRAINTS
            if {$ext == "pdc"} {
                create_links -io_pdc $FILE
                append LIBERO_PLACE_CONSTRAINTS "-file $FILE "
            } elseif {$ext == "sdc"} {
                create_links -sdc $FILE
                append LIBERO_PLACE_CONSTRAINTS "-file $FILE "
                append LIBERO_OTHER_CONSTRAINTS "-file $FILE "
            } else {
                create_links -library $LIBRARY -hdl_source $FILE
                build_design_hierarchy
            }
            # Only the last organize_tool_files for a certain TOOL is taking
            # into account, and it needs to include all the related files.
            #
            # PDC is only used for PLACEROUTE.
            # SDC is used by ALL (SYNTHESIZE, PLACEROUTE and VERIFYTIMING).
            #
            # The strategy is to make a command string with the collected
            # -file parameters and using eval to execute it as Tcl command.
            if {$ext == "pdc" || $ext == "sdc"} {
                if { [info exists LIBERO_OTHER_CONSTRAINTS] } {
                    set cmd "organize_tool_files -tool {SYNTHESIZE} "
                    append cmd $LIBERO_OTHER_CONSTRAINTS
                    append cmd "-module $TOP -input_type {constraint}"
                    eval $cmd
                    set cmd "organize_tool_files -tool {VERIFYTIMING} "
                    append cmd $LIBERO_OTHER_CONSTRAINTS
                    append cmd "-module $TOP -input_type {constraint}"
                    eval $cmd
                }
                if { [info exists LIBERO_PLACE_CONSTRAINTS] } {
                    set cmd "organize_tool_files -tool {PLACEROUTE} "
                    append cmd $LIBERO_PLACE_CONSTRAINTS
                    append cmd "-module $TOP -input_type {constraint}"
                    eval $cmd
                }
            }
        }
        "quartus" {
            if {$ext == "v"} {
                set TYPE VERILOG_FILE
            } elseif {$ext == "sv"} {
                set TYPE SYSTEMVERILOG_FILE
            } elseif {$ext == "vhdl" || $ext == "vhd"} {
                set TYPE VHDL_FILE
            } elseif {$ext == "sdc"} {
                set TYPE SDC_FILE
            } else {
                set TYPE SOURCE_FILE
            }
            if { $LIBRARY != "work" } {
                set_global_assignment -name $TYPE $FILE -library $LIBRARY
            } else {
                set_global_assignment -name $TYPE $FILE
            }
        }
        "vivado" {
            if { $LIBRARY != "work" } {
                add_files $FILE
                set_property library $LIBRARY [get_files $FILE]
            } else {
                add_files $FILE
            }
        }
        "yosys"   {
            if {$ext == "v" || $ext == "sv"} {
                read_verilog $FILE
            }
        }
    }
}

proc fpga_include {FILE} {
    global TOOL INCLUDED
    if { [file isfile $FILE] } {
        set PATH [file dirname $FILE]
    } else {
        set PATH $FILE
    }
    lappend INCLUDED $PATH
    fpga_print "setting '$PATH' as a search location"
    switch $TOOL {
        "ise" {
            # Verilog Included Files are NOT added
            project set "Verilog Include Directories" \
            [join $INCLUDED "|"] -process "Synthesize - XST"
        }
        "libero" {
            # Verilog Included Files are ALSO added
            # They must be specified after set_root (see fpga_top)
            create_links -hdl_source $FILE
            build_design_hierarchy
        }
        "quartus" {
            # Verilog Included Files are NOT added
            foreach INCLUDE $INCLUDED {
                set_global_assignment -name SEARCH_PATH $INCLUDE
            }
        }
        "vivado" {
            # Verilog Included Files are NOT added
            set_property "include_dirs" $INCLUDED [current_fileset]
        }
        "yosys"   {
            # Verilog Included Files are NOT added
            verilog_defaults -add -I[file dirname $FILE]
        }
    }
}

proc fpga_design {FILE} {
    global TOOL TOP INCLUDED
    fpga_print "including the block design '$FILE'"
    switch $TOOL {
        "ise" {
            puts "UNSUPPORTED"
        }
        "libero" {
            puts "UNSUPPORTED"
        }
        "quartus" {
            puts "UNSUPPORTED"
        }
        "vivado" {
            if { [info exists INCLUDED] && [llength $INCLUDED] > 0 } {
                set_property "ip_repo_paths" $INCLUDED [get_filesets sources_1]
                update_ip_catalog -rebuild
            }
            source $FILE
            set design [get_bd_designs]
            make_wrapper -force -files [get_files $design.bd] -top -import
            if { $TOP == "UNDEFINED"} {
                set TOP ${design}_wrapper
            }
        }
        "yosys"   {
            puts "UNSUPPORTED"
        }
    }
}

proc fpga_top { TOP } {
    global TOOL
    fpga_print "specifying the top level '$TOP'"
    switch $TOOL {
        "ise"     {
            project set top $TOP
        }
        "libero"  {
            set_root $TOP
            # Verilog Included files
            global INCLUDED PARAMS
            set cmd "configure_tool -name {SYNTHESIZE} -params {SYNPLIFY_OPTIONS:"
            if { [info exists INCLUDED] && [llength $INCLUDED] > 0 } {
                set PATHS [join $INCLUDED ";"]
                append cmd "set_option -include_path \"$PATHS\""
                append cmd "\n"
            }
            foreach PARAM $PARAMS {
                set assign [join $PARAM]
                append cmd "set_option -hdl_param -set \"$assign\""
                append cmd "\n"
            }
            append cmd "}"
            eval $cmd
        }
        "quartus" {
            set_global_assignment -name TOP_LEVEL_ENTITY $TOP
        }
        "vivado"  {
            set_property top $TOP [current_fileset]
        }
        "yosys"   { }
    }
}

proc fpga_area_opts {} {
    global TOOL
    fpga_print "setting options for 'area' optimization"
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Area"
        }
        "libero"  {
            configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:true}
        }
        "quartus" {
            set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE AREA"
            set_global_assignment -name OPTIMIZATION_TECHNIQUE AREA
        }
        "vivado"  {
            set obj [get_runs synth_1]
            set_property strategy "Flow_AreaOptimized_high" $obj
            set_property "steps.synth_design.args.directive" "AreaOptimized_high" $obj
            set_property "steps.synth_design.args.control_set_opt_threshold" "1" $obj
            set obj [get_runs impl_1]
            set_property strategy "Area_Explore" $obj
            set_property "steps.opt_design.args.directive" "ExploreArea" $obj
        }
        "yosys"   { puts "Not yet implemented" }
    }
}

proc fpga_power_opts {} {
    global TOOL
    fpga_print "setting options for 'power' optimization"
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Area"
            project set "Power Reduction" "true" -process "Synthesize - XST"
            project set "Power Reduction" "high" -process "Map"
            project set "Power Reduction" "true" -process "Place & Route"
        }
        "libero"  {
            configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:true}
            configure_tool -name {PLACEROUTE} -params {PDPR:true}
        }
        "quartus" {
            set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE POWER"
            set_global_assignment -name OPTIMIZE_POWER_DURING_SYNTHESIS "EXTRA EFFORT"
            set_global_assignment -name OPTIMIZE_POWER_DURING_FITTING "EXTRA EFFORT"
        }
        "vivado"  {
            #enable power_opt_design and phys_opt_design
            set obj [get_runs synth_1]
            set_property strategy "Vivado Synthesis Defaults" $obj
            set obj [get_runs impl_1]
            set_property strategy "Power_DefaultOpt" $obj
            set_property "steps.power_opt_design.is_enabled" "1" $obj
            set_property "steps.phys_opt_design.is_enabled" "1" $obj
        }
        "yosys"   { puts "Not yet implemented" }
    }
}

proc fpga_speed_opts {} {
    global TOOL
    fpga_print "setting options for 'speed' optimization"
    switch $TOOL {
        "ise"     {
            project set "Optimization Goal" "Speed"
        }
        "libero"  {
            configure_tool -name {SYNTHESIZE} -params {RAM_OPTIMIZED_FOR_POWER:false}
            configure_tool -name {PLACEROUTE} -params {EFFORT_LEVEL:true}
        }
        "quartus" {
            set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"
            set_global_assignment -name OPTIMIZATION_TECHNIQUE SPEED
        }
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
        "yosys"   { puts "Not yet implemented" }
    }
}

proc fpga_run_syn {} {
    global TOOL
    fpga_print "running 'synthesis'"
    switch $TOOL {
        "ise"     {
            project clean
            process run "Synthesize" -force rerun
        }
        "libero"  {
            run_tool -name {SYNTHESIZE}
        }
        "quartus" {
            execute_module -tool map
        }
        "vivado"  {
            reset_run synth_1
            launch_runs synth_1
            wait_on_run synth_1
        }
        "yosys"   {
            global BACKEND FAMILY TOP
            if {$BACKEND == "vivado"} {
                synth_xilinx -top $TOP -family $FAMILY
                write_edif -pvector bra yosys.edif
                puts "Generated yosys.edif to be used with Vivado"
            } elseif {$BACKEND == "ise"} {
                synth_xilinx -top $TOP -family $FAMILY -ise
                write_edif -pvector bra yosys.edif
                puts "Generated yosys.edif to be used with ISE"
            } else {
                synth -top $TOP
                write_verilog yosys.v
                puts "Generated yosys.v as a generic synthesis"
            }
        }
    }
}

proc fpga_run_imp {} {
    global TOOL
    fpga_print "running 'implementation'"
    switch $TOOL {
        "ise"     {
            process run "Translate" -force rerun
            process run "Map" -force rerun
            process run "Place & Route" -force rerun
        }
        "libero"  {
            run_tool -name {PLACEROUTE}
            run_tool -name {VERIFYTIMING}
        }
        "quartus" {
            execute_module -tool fit
            execute_module -tool sta
        }
        "vivado"  {
            open_run synth_1
            launch_runs impl_1
            wait_on_run impl_1
        }
        "yosys"   { puts "UNSUPPORTED (Yosys only performs Synthesis)" }
    }
}

proc fpga_run_bit {} {
    global TOOL PROJECT TOP
    fpga_print "running 'bitstream generation'"
    switch $TOOL {
        "ise"     {
            process run "Generate Programming File" -force rerun
            file rename -force $TOP.bit $PROJECT.bit
        }
        "libero"  {
            run_tool -name {GENERATEPROGRAMMINGFILE}
        }
        "quartus" {
            execute_module -tool asm
        }
        "vivado"  {
            open_run impl_1
            write_bitstream -force $PROJECT
        }
        "yosys"   { puts "UNSUPPORTED (Yosys only performs Synthesis)" }
    }
}

proc fpga_export {} {
    global TOOL PROJECT
    fpga_print "exporting the design"
    switch $TOOL {
        "ise"     {
            puts "UNSUPPORTED"
        }
        "libero"  {
            puts "UNSUPPORTED"
        }
        "quartus" {
            puts "UNSUPPORTED"
        }
        "vivado"  {
            if { [ catch {
                # Vitis
                write_hw_platform -fixed -force -include_bit \
                    -file ${PROJECT}.xsa
                fpga_print "design exported to be used with Vitis"
            } ] } {
                # SDK
                write_hwdef -force -file ${PROJECT}.hwdef
                write_sysdef -force \
                    -hwdef [glob -nocomplain *.hwdef] \
                    -bitfile [glob -nocomplain *.bit] \
                    -file ${PROJECT}.hdf
                fpga_print "design exported to be used with the SDK"
            }
        }
        "yosys"   {
            puts "UNSUPPORTED (Yosys only performs Synthesis)"
        }
    }
}

#
# Start of the script
#

fpga_print "start of the Tcl script (interpreter $tcl_version)"

#
# Project Creation
#

if { [lsearch -exact $TASKS "prj"] >= 0 } {
    fpga_print "running the Project Creation"
    if { [catch {
        fpga_create $PROJECT
        fpga_part $PART
        fpga_options "prefile"
        fpga_params
        fpga_files
        fpga_top $TOP
        switch $STRATEGY {
            "area"  {fpga_area_opts}
            "power" {fpga_power_opts}
            "speed" {fpga_speed_opts}
        }
        fpga_options "postprj"
        fpga_close
    } ERRMSG]} {
        puts "ERROR: there was a problem creating a New Project.\n"
        puts $ERRMSG
        exit 1
    }
}

#
# Design Flow
#

if { [lsearch -regexp $TASKS "syn|imp|bit"] >= 0 } {
    fpga_print "running the Design Flow"
    if { [catch {
        fpga_open $PROJECT
        fpga_options "preflow"
        if { [lsearch -exact $TASKS "syn"] >= 0 } {
            fpga_run_syn
            fpga_options "postsyn"
        }
        if { [lsearch -exact $TASKS "imp"] >= 0 } {
            fpga_run_imp
            fpga_options "postimp"
        }
        if { [lsearch -exact $TASKS "bit"] >= 0 } {
            fpga_run_bit
            fpga_options "postbit"
        }
        fpga_close
    } ERRMSG]} {
        puts "ERROR: there was a problem running the Design Flow.\n"
        puts $ERRMSG
        exit 2
    }
}

#
# End of the script
#

fpga_print "end of the Tcl script"
