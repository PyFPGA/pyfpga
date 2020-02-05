create_project -force $PROJECT

set_property "part" $PART [current_project]

add_files $FILE

set_property top $TOP [current_fileset]

reset_run synth_1
launch_runs synth_1
wait_on_run synth_1

launch_runs impl_1
wait_on_run impl_1

open_run impl_1
write_bitstream -force $PROJECT

close_project
