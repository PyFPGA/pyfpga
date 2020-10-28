new_project -name example -location libero -hdl {VHDL} -family {SmartFusion2}

set_device -family SmartFusion2 -die M2S010 -package tq144 -speed -1

create_links -hdl_source ../../hdl/headers1/freq.vh
create_links -hdl_source ../../hdl/headers2/secs.vh

create_links -hdl_source ../../hdl/blinking.v

build_design_hierarchy

set_root Blinking

# The Tcl for synplify is generated under "libero/synthesis", so an extra "../../" is needed
configure_tool -name {SYNTHESIZE} -params {SYNPLIFY_OPTIONS:set_option -include_path "../../../../hdl/headers1;../../../../hdl/headers2"}

run_tool -name {SYNTHESIZE}

close_project
