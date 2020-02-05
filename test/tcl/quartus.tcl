package require ::quartus::project
project_new $PROJECT -overwrite

set_global_assignment -name DEVICE $PART

set_global_assignment -name VERILOG_FILE $FILE

set_global_assignment -name TOP_LEVEL_ENTITY $TOP

execute_module -tool map

execute_module -tool fit
execute_module -tool sta

execute_module -tool asm

project_close
