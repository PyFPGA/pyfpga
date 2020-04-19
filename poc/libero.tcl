new_project -name example -location libero -hdl {VHDL} -family {SmartFusion2}

set_device -family SmartFusion2 -die M2S010 -package tq144 -speed -1

create_links -hdl_source ../hdl/blinking.vhdl
create_links -io_pdc ../examples/libero/mkr.pdc
build_design_hierarchy

set_root Blinking

organize_tool_files -tool {PLACEROUTE} -file ../examples/libero/mkr.pdc -module Blinking -input_type {constraint}

run_tool -name {SYNTHESIZE}

run_tool -name {PLACEROUTE}
run_tool -name {VERIFYTIMING}

run_tool -name {GENERATEPROGRAMMINGFILE}

close_project
