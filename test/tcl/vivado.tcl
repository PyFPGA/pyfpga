create_project -force example

set_property "part" xc7z010-1-clg400 [current_project]

add_files ../../examples/hdl/blinking.vhdl
add_files ../../examples/vivado/zybo.xdc

set_property top Blinking [current_fileset]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

launch_runs impl_1
wait_on_run impl_1

open_run impl_1
write_bitstream -force example

close_project
