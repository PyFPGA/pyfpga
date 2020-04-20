create_project -force example

set_property "part" xc7z010-1-clg400 [current_project]

# When specifying binary values for boolean or std_logic VHDL generic types,
# you must specify the value using the Verilog bit format, rather than
# standard VHDL format.

add_files ../../hdl/fakes/parameters.v
set_property top Params [current_fileset]
set_property "generic" "INT=1 REA=1.5 LOG=1'b1 VEC=8'b11001100 STR=\"WXYZ\"" -objects [get_filesets sources_1]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

# To avoid re-synthesis of the Verilog version
remove_files [get_files]

add_files ../../hdl/fakes/generics.vhdl
set_property top Params [current_fileset]
# TODO: fix it? (possible?)
#set_property "generic" "INT=1 REA=1.5 LOG=1'b1 VEC=8'b11001100 STR=\"WXYZ\"" -objects [get_filesets sources_1]
set_property "generic" "INT=1 LOG=1'b1 VEC=8'b11001100 STR=\"WXYZ\"" -objects [get_filesets sources_1]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

close_project
