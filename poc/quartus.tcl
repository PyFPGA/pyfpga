package require ::quartus::flow

project_new example -overwrite

set_global_assignment -name DEVICE 5CSEBA6U23I7

set_global_assignment -name VHDL_FILE ../hdl/blinking.vhdl
source ../examples/quartus/de10nano.tcl

set_global_assignment -name TOP_LEVEL_ENTITY Blinking

execute_module -tool map

execute_module -tool fit
execute_module -tool sta

execute_module -tool asm

project_close
