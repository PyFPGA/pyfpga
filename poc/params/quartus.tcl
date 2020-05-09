package require ::quartus::flow

project_new example -overwrite

set_global_assignment -name DEVICE 5CSEBA6U23I7

set_global_assignment -name VERILOG_FILE ../../hdl/fakes/parameters.v
set_global_assignment -name TOP_LEVEL_ENTITY Params
set_parameter -name BOO 1
set_parameter -name INT 255
set_parameter -name LOG 1
set_parameter -name VEC 255
set_parameter -name STR WXYZ
set_parameter -name REA 1.1
execute_module -tool map

# To avoid re-synthesis of the Verilog version
set_global_assignment -name VERILOG_FILE -remove

set_global_assignment -name VHDL_FILE ../../hdl/fakes/generics.vhdl
set_global_assignment -name TOP_LEVEL_ENTITY Params
set_parameter -name BOO True
set_parameter -name INT 255
set_parameter -name LOG '1'
set_parameter -name VEC "11111111"
set_parameter -name STR WXYZ
set_parameter -name REA 1.1
execute_module -tool map

project_close
