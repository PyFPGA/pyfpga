create_project -force example

set_property "part" xc7z010-1-clg400 [current_project]

# When specifying binary values for boolean or std_logic VHDL generic types,
# you must specify the value using the Verilog bit format, rather than
# standard VHDL format.

add_files ../../hdl/fakes/parameters.v
set_property top Params [current_fileset]
set_property "generic" "BOO=1 INT=255 LOG=1'b1 VEC=8'b11111111 STR=WXYZ REA=1.1" -objects [get_filesets sources_1]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

# To avoid re-synthesis of the Verilog version
remove_files [get_files]

add_files ../../hdl/fakes/generics.vhdl
set_property top Params [current_fileset]
# TODO: add REA=1.1 (possible?)
set_property "generic" "BOO=true INT=255 LOG=1'b1 VEC=8'b11111111 STR=WXYZ" -objects [get_filesets sources_1]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

close_project
