# Xilinx Design Constraints
#
# Are based on the standard Synopsys Design Constraints (SDC) format.

create_clock -name clk_i -period 8 [get_ports clk_i]

set_property PACKAGE_PIN L16 [get_ports clk_i]
set_property IOSTANDARD LVCMOS33 [get_ports clk_i]
set_property PACKAGE_PIN M14 [get_ports led_o]
set_property IOSTANDARD LVCMOS33 [get_ports led_o]
