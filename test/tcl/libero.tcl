new_project -name $PROJECT -location $PROJECT -hdl {VHDL} -family {SmartFusion2}

set_device -family $FAMILY -die $DEVICE -package $PACKAGE -speed $SPEED

create_links -library $LIBRARY -hdl_source $FILE
build_design_hierarchy

set_root $TOP

run_tool -name {SYNTHESIZE}

run_tool -name {PLACEROUTE}
run_tool -name {VERIFYTIMING}

run_tool -name {GENERATEPROGRAMMINGFILE}

close_project
