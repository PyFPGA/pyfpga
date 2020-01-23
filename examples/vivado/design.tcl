################################################################
# START
################################################################

# CHANGE DESIGN NAME HERE
variable design_name
set design_name design_1

# If you do not already have an existing IP Integrator design open,
# you can create a design using the following command:
#    create_bd_design $design_name

# Creating design if needed
set errMsg ""
set nRet 0

set cur_design [current_bd_design -quiet]
set list_cells [get_bd_cells -quiet]

if { ${design_name} eq "" } {
   # USE CASES:
   #    1) Design_name not set

   set errMsg "Please set the variable <design_name> to a non-empty value."
   set nRet 1

} elseif { ${cur_design} ne "" && ${list_cells} eq "" } {
   # USE CASES:
   #    2): Current design opened AND is empty AND names same.
   #    3): Current design opened AND is empty AND names diff; design_name NOT in project.
   #    4): Current design opened AND is empty AND names diff; design_name exists in project.

   if { $cur_design ne $design_name } {
      common::send_msg_id "BD_TCL-001" "INFO" "Changing value of <design_name> from <$design_name> to <$cur_design> since current design is empty."
      set design_name [get_property NAME $cur_design]
   }
   common::send_msg_id "BD_TCL-002" "INFO" "Constructing design in IPI design <$cur_design>..."

} elseif { ${cur_design} ne "" && $list_cells ne "" && $cur_design eq $design_name } {
   # USE CASES:
   #    5) Current design opened AND has components AND same names.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 1
} elseif { [get_files -quiet ${design_name}.bd] ne "" } {
   # USE CASES:
   #    6) Current opened design, has components, but diff names, design_name exists in project.
   #    7) No opened design, design_name exists in project.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 2

} else {
   # USE CASES:
   #    8) No opened design, design_name not in project.
   #    9) Current opened design, has components, but diff names, design_name not in project.

   common::send_msg_id "BD_TCL-003" "INFO" "Currently there is no design <$design_name> in project, so creating one..."

   create_bd_design $design_name

   common::send_msg_id "BD_TCL-004" "INFO" "Making design <$design_name> as current_bd_design."
   current_bd_design $design_name

}

common::send_msg_id "BD_TCL-005" "INFO" "Currently the variable <design_name> is equal to \"$design_name\"."

if { $nRet != 0 } {
   catch {common::send_msg_id "BD_TCL-114" "ERROR" $errMsg}
   return $nRet
}

set bCheckIPsPassed 1
##################################################################
# CHECK IPs
##################################################################
set bCheckIPs 1
if { $bCheckIPs == 1 } {
   set list_check_ips "\
xilinx.com:ip:processing_system7:5.5\
"

   set list_ips_missing ""
   common::send_msg_id "BD_TCL-006" "INFO" "Checking if the following IPs exist in the project's IP catalog: $list_check_ips ."

   foreach ip_vlnv $list_check_ips {
      set ip_obj [get_ipdefs -all $ip_vlnv]
      if { $ip_obj eq "" } {
         lappend list_ips_missing $ip_vlnv
      }
   }

   if { $list_ips_missing ne "" } {
      catch {common::send_msg_id "BD_TCL-115" "ERROR" "The following IPs are not found in the IP Catalog:\n  $list_ips_missing\n\nResolution: Please add the repository containing the IP(s) to the project." }
      set bCheckIPsPassed 0
   }

}

##################################################################
# CHECK Modules
##################################################################
set bCheckModules 1
if { $bCheckModules == 1 } {
   set list_check_mods "\
Blinking\
"

   set list_mods_missing ""
   common::send_msg_id "BD_TCL-006" "INFO" "Checking if the following modules exist in the project's sources: $list_check_mods ."

   foreach mod_vlnv $list_check_mods {
      if { [can_resolve_reference $mod_vlnv] == 0 } {
         lappend list_mods_missing $mod_vlnv
      }
   }

   if { $list_mods_missing ne "" } {
      catch {common::send_msg_id "BD_TCL-115" "ERROR" "The following module(s) are not found in the project: $list_mods_missing" }
      common::send_msg_id "BD_TCL-008" "INFO" "Please add source files for the missing module(s) above."
      set bCheckIPsPassed 0
   }
}

if { $bCheckIPsPassed != 1 } {
  common::send_msg_id "BD_TCL-1003" "WARNING" "Will not continue with creation of design due to the error(s) above."
  return 3
}

##################################################################
# DESIGN PROCs
##################################################################



# Procedure to create entire design; Provide argument to make
# procedure reusable. If parentCell is "", will use root.
proc create_root_design { parentCell } {

  variable design_name

  if { $parentCell eq "" } {
     set parentCell [get_bd_cells /]
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_msg_id "BD_TCL-100" "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_msg_id "BD_TCL-101" "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj


  # Create interface ports
  set DDR [ create_bd_intf_port -mode Master -vlnv xilinx.com:interface:ddrx_rtl:1.0 DDR ]

  set FIXED_IO [ create_bd_intf_port -mode Master -vlnv xilinx.com:display_processing_system7:fixedio_rtl:1.0 FIXED_IO ]


  # Create ports
  set clk_i [ create_bd_port -dir I clk_i ]
  set led_o [ create_bd_port -dir O led_o ]

  # Create instance: Blinking_0, and set properties
  set block_name Blinking
  set block_cell_name Blinking_0
  if { [catch {set Blinking_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_msg_id "BD_TCL-105" "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $Blinking_0 eq "" } {
     catch {common::send_msg_id "BD_TCL-106" "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.FREQ {125000000} \
 ] $Blinking_0

  # Create instance: processing_system7_0, and set properties
  set processing_system7_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0 ]
  set_property -dict [ list \
   CONFIG.PCW_ACT_APU_PERIPHERAL_FREQMHZ {650} \
   CONFIG.PCW_ACT_CAN_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_DCI_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_ENET0_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_ENET1_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_FPGA0_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_FPGA1_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_FPGA2_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_FPGA3_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_PCAP_PERIPHERAL_FREQMHZ {200} \
   CONFIG.PCW_ACT_QSPI_PERIPHERAL_FREQMHZ {200} \
   CONFIG.PCW_ACT_SDIO_PERIPHERAL_FREQMHZ {50} \
   CONFIG.PCW_ACT_SMC_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_SPI_PERIPHERAL_FREQMHZ {10} \
   CONFIG.PCW_ACT_TPIU_PERIPHERAL_FREQMHZ {200} \
   CONFIG.PCW_ACT_TTC0_CLK0_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_TTC0_CLK1_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_TTC0_CLK2_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_TTC1_CLK0_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_TTC1_CLK1_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_TTC1_CLK2_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_ACT_UART_PERIPHERAL_FREQMHZ {100} \
   CONFIG.PCW_ACT_WDT_PERIPHERAL_FREQMHZ {108} \
   CONFIG.PCW_APU_PERIPHERAL_FREQMHZ {650} \
   CONFIG.PCW_ARMPLL_CTRL_FBDIV {26} \
   CONFIG.PCW_CAN_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_CAN_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_CLK0_FREQ {10000000} \
   CONFIG.PCW_CLK1_FREQ {10000000} \
   CONFIG.PCW_CLK2_FREQ {10000000} \
   CONFIG.PCW_CLK3_FREQ {10000000} \
   CONFIG.PCW_CPU_CPU_PLL_FREQMHZ {1300} \
   CONFIG.PCW_CPU_PERIPHERAL_DIVISOR0 {2} \
   CONFIG.PCW_CRYSTAL_PERIPHERAL_FREQMHZ {50.000000} \
   CONFIG.PCW_DCI_PERIPHERAL_DIVISOR0 {15} \
   CONFIG.PCW_DCI_PERIPHERAL_DIVISOR1 {7} \
   CONFIG.PCW_DDRPLL_CTRL_FBDIV {21} \
   CONFIG.PCW_DDR_DDR_PLL_FREQMHZ {1050} \
   CONFIG.PCW_DDR_PERIPHERAL_DIVISOR0 {2} \
   CONFIG.PCW_DDR_RAM_HIGHADDR {0x1FFFFFFF} \
   CONFIG.PCW_ENET0_ENET0_IO {<Select>} \
   CONFIG.PCW_ENET0_GRP_MDIO_ENABLE {0} \
   CONFIG.PCW_ENET0_GRP_MDIO_IO {<Select>} \
   CONFIG.PCW_ENET0_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_ENET0_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_ENET0_PERIPHERAL_ENABLE {0} \
   CONFIG.PCW_ENET0_PERIPHERAL_FREQMHZ {1000 Mbps} \
   CONFIG.PCW_ENET0_RESET_ENABLE {0} \
   CONFIG.PCW_ENET1_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_ENET1_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_ENET1_RESET_ENABLE {0} \
   CONFIG.PCW_ENET_RESET_ENABLE {0} \
   CONFIG.PCW_ENET_RESET_SELECT {<Select>} \
   CONFIG.PCW_EN_CLK0_PORT {0} \
   CONFIG.PCW_EN_EMIO_TTC0 {0} \
   CONFIG.PCW_EN_EMIO_WP_SDIO0 {1} \
   CONFIG.PCW_EN_ENET0 {0} \
   CONFIG.PCW_EN_GPIO {0} \
   CONFIG.PCW_EN_QSPI {1} \
   CONFIG.PCW_EN_RST0_PORT {0} \
   CONFIG.PCW_EN_SDIO0 {1} \
   CONFIG.PCW_EN_TTC0 {0} \
   CONFIG.PCW_EN_UART1 {1} \
   CONFIG.PCW_EN_USB0 {0} \
   CONFIG.PCW_FCLK0_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_FCLK0_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_FCLK1_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_FCLK1_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_FCLK2_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_FCLK2_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_FCLK3_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_FCLK3_PERIPHERAL_DIVISOR1 {1} \
   CONFIG.PCW_FCLK_CLK0_BUF {FALSE} \
   CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100} \
   CONFIG.PCW_FPGA_FCLK0_ENABLE {0} \
   CONFIG.PCW_FPGA_FCLK1_ENABLE {0} \
   CONFIG.PCW_FPGA_FCLK2_ENABLE {0} \
   CONFIG.PCW_FPGA_FCLK3_ENABLE {0} \
   CONFIG.PCW_GPIO_MIO_GPIO_ENABLE {0} \
   CONFIG.PCW_GPIO_MIO_GPIO_IO {<Select>} \
   CONFIG.PCW_I2C0_RESET_ENABLE {0} \
   CONFIG.PCW_I2C1_RESET_ENABLE {0} \
   CONFIG.PCW_I2C_PERIPHERAL_FREQMHZ {25} \
   CONFIG.PCW_I2C_RESET_ENABLE {0} \
   CONFIG.PCW_IOPLL_CTRL_FBDIV {32} \
   CONFIG.PCW_IO_IO_PLL_FREQMHZ {1600} \
   CONFIG.PCW_MIO_0_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_0_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_0_PULLUP {<Select>} \
   CONFIG.PCW_MIO_0_SLEW {<Select>} \
   CONFIG.PCW_MIO_10_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_10_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_10_PULLUP {<Select>} \
   CONFIG.PCW_MIO_10_SLEW {<Select>} \
   CONFIG.PCW_MIO_11_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_11_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_11_PULLUP {<Select>} \
   CONFIG.PCW_MIO_11_SLEW {<Select>} \
   CONFIG.PCW_MIO_12_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_12_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_12_PULLUP {<Select>} \
   CONFIG.PCW_MIO_12_SLEW {<Select>} \
   CONFIG.PCW_MIO_13_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_13_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_13_PULLUP {<Select>} \
   CONFIG.PCW_MIO_13_SLEW {<Select>} \
   CONFIG.PCW_MIO_14_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_14_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_14_PULLUP {<Select>} \
   CONFIG.PCW_MIO_14_SLEW {<Select>} \
   CONFIG.PCW_MIO_15_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_15_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_15_PULLUP {<Select>} \
   CONFIG.PCW_MIO_15_SLEW {<Select>} \
   CONFIG.PCW_MIO_16_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_16_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_16_PULLUP {<Select>} \
   CONFIG.PCW_MIO_16_SLEW {<Select>} \
   CONFIG.PCW_MIO_17_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_17_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_17_PULLUP {<Select>} \
   CONFIG.PCW_MIO_17_SLEW {<Select>} \
   CONFIG.PCW_MIO_18_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_18_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_18_PULLUP {<Select>} \
   CONFIG.PCW_MIO_18_SLEW {<Select>} \
   CONFIG.PCW_MIO_19_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_19_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_19_PULLUP {<Select>} \
   CONFIG.PCW_MIO_19_SLEW {<Select>} \
   CONFIG.PCW_MIO_1_DIRECTION {out} \
   CONFIG.PCW_MIO_1_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_1_PULLUP {disabled} \
   CONFIG.PCW_MIO_1_SLEW {fast} \
   CONFIG.PCW_MIO_20_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_20_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_20_PULLUP {<Select>} \
   CONFIG.PCW_MIO_20_SLEW {<Select>} \
   CONFIG.PCW_MIO_21_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_21_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_21_PULLUP {<Select>} \
   CONFIG.PCW_MIO_21_SLEW {<Select>} \
   CONFIG.PCW_MIO_22_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_22_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_22_PULLUP {<Select>} \
   CONFIG.PCW_MIO_22_SLEW {<Select>} \
   CONFIG.PCW_MIO_23_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_23_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_23_PULLUP {<Select>} \
   CONFIG.PCW_MIO_23_SLEW {<Select>} \
   CONFIG.PCW_MIO_24_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_24_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_24_PULLUP {<Select>} \
   CONFIG.PCW_MIO_24_SLEW {<Select>} \
   CONFIG.PCW_MIO_25_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_25_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_25_PULLUP {<Select>} \
   CONFIG.PCW_MIO_25_SLEW {<Select>} \
   CONFIG.PCW_MIO_26_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_26_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_26_PULLUP {<Select>} \
   CONFIG.PCW_MIO_26_SLEW {<Select>} \
   CONFIG.PCW_MIO_27_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_27_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_27_PULLUP {<Select>} \
   CONFIG.PCW_MIO_27_SLEW {<Select>} \
   CONFIG.PCW_MIO_28_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_28_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_28_PULLUP {<Select>} \
   CONFIG.PCW_MIO_28_SLEW {<Select>} \
   CONFIG.PCW_MIO_29_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_29_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_29_PULLUP {<Select>} \
   CONFIG.PCW_MIO_29_SLEW {<Select>} \
   CONFIG.PCW_MIO_2_DIRECTION {inout} \
   CONFIG.PCW_MIO_2_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_2_PULLUP {disabled} \
   CONFIG.PCW_MIO_2_SLEW {fast} \
   CONFIG.PCW_MIO_30_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_30_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_30_PULLUP {<Select>} \
   CONFIG.PCW_MIO_30_SLEW {<Select>} \
   CONFIG.PCW_MIO_31_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_31_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_31_PULLUP {<Select>} \
   CONFIG.PCW_MIO_31_SLEW {<Select>} \
   CONFIG.PCW_MIO_32_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_32_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_32_PULLUP {<Select>} \
   CONFIG.PCW_MIO_32_SLEW {<Select>} \
   CONFIG.PCW_MIO_33_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_33_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_33_PULLUP {<Select>} \
   CONFIG.PCW_MIO_33_SLEW {<Select>} \
   CONFIG.PCW_MIO_34_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_34_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_34_PULLUP {<Select>} \
   CONFIG.PCW_MIO_34_SLEW {<Select>} \
   CONFIG.PCW_MIO_35_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_35_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_35_PULLUP {<Select>} \
   CONFIG.PCW_MIO_35_SLEW {<Select>} \
   CONFIG.PCW_MIO_36_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_36_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_36_PULLUP {<Select>} \
   CONFIG.PCW_MIO_36_SLEW {<Select>} \
   CONFIG.PCW_MIO_37_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_37_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_37_PULLUP {<Select>} \
   CONFIG.PCW_MIO_37_SLEW {<Select>} \
   CONFIG.PCW_MIO_38_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_38_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_38_PULLUP {<Select>} \
   CONFIG.PCW_MIO_38_SLEW {<Select>} \
   CONFIG.PCW_MIO_39_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_39_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_39_PULLUP {<Select>} \
   CONFIG.PCW_MIO_39_SLEW {<Select>} \
   CONFIG.PCW_MIO_3_DIRECTION {inout} \
   CONFIG.PCW_MIO_3_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_3_PULLUP {disabled} \
   CONFIG.PCW_MIO_3_SLEW {fast} \
   CONFIG.PCW_MIO_40_DIRECTION {inout} \
   CONFIG.PCW_MIO_40_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_40_PULLUP {disabled} \
   CONFIG.PCW_MIO_40_SLEW {fast} \
   CONFIG.PCW_MIO_41_DIRECTION {inout} \
   CONFIG.PCW_MIO_41_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_41_PULLUP {disabled} \
   CONFIG.PCW_MIO_41_SLEW {fast} \
   CONFIG.PCW_MIO_42_DIRECTION {inout} \
   CONFIG.PCW_MIO_42_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_42_PULLUP {disabled} \
   CONFIG.PCW_MIO_42_SLEW {fast} \
   CONFIG.PCW_MIO_43_DIRECTION {inout} \
   CONFIG.PCW_MIO_43_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_43_PULLUP {disabled} \
   CONFIG.PCW_MIO_43_SLEW {fast} \
   CONFIG.PCW_MIO_44_DIRECTION {inout} \
   CONFIG.PCW_MIO_44_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_44_PULLUP {disabled} \
   CONFIG.PCW_MIO_44_SLEW {fast} \
   CONFIG.PCW_MIO_45_DIRECTION {inout} \
   CONFIG.PCW_MIO_45_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_45_PULLUP {disabled} \
   CONFIG.PCW_MIO_45_SLEW {fast} \
   CONFIG.PCW_MIO_46_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_46_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_46_PULLUP {<Select>} \
   CONFIG.PCW_MIO_46_SLEW {<Select>} \
   CONFIG.PCW_MIO_47_DIRECTION {in} \
   CONFIG.PCW_MIO_47_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_47_PULLUP {disabled} \
   CONFIG.PCW_MIO_47_SLEW {slow} \
   CONFIG.PCW_MIO_48_DIRECTION {out} \
   CONFIG.PCW_MIO_48_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_48_PULLUP {disabled} \
   CONFIG.PCW_MIO_48_SLEW {slow} \
   CONFIG.PCW_MIO_49_DIRECTION {in} \
   CONFIG.PCW_MIO_49_IOTYPE {LVCMOS 1.8V} \
   CONFIG.PCW_MIO_49_PULLUP {disabled} \
   CONFIG.PCW_MIO_49_SLEW {slow} \
   CONFIG.PCW_MIO_4_DIRECTION {inout} \
   CONFIG.PCW_MIO_4_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_4_PULLUP {disabled} \
   CONFIG.PCW_MIO_4_SLEW {fast} \
   CONFIG.PCW_MIO_50_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_50_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_50_PULLUP {<Select>} \
   CONFIG.PCW_MIO_50_SLEW {<Select>} \
   CONFIG.PCW_MIO_51_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_51_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_51_PULLUP {<Select>} \
   CONFIG.PCW_MIO_51_SLEW {<Select>} \
   CONFIG.PCW_MIO_52_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_52_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_52_PULLUP {<Select>} \
   CONFIG.PCW_MIO_52_SLEW {<Select>} \
   CONFIG.PCW_MIO_53_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_53_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_53_PULLUP {<Select>} \
   CONFIG.PCW_MIO_53_SLEW {<Select>} \
   CONFIG.PCW_MIO_5_DIRECTION {inout} \
   CONFIG.PCW_MIO_5_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_5_PULLUP {disabled} \
   CONFIG.PCW_MIO_5_SLEW {fast} \
   CONFIG.PCW_MIO_6_DIRECTION {out} \
   CONFIG.PCW_MIO_6_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_6_PULLUP {disabled} \
   CONFIG.PCW_MIO_6_SLEW {fast} \
   CONFIG.PCW_MIO_7_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_7_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_7_PULLUP {<Select>} \
   CONFIG.PCW_MIO_7_SLEW {<Select>} \
   CONFIG.PCW_MIO_8_DIRECTION {out} \
   CONFIG.PCW_MIO_8_IOTYPE {LVCMOS 3.3V} \
   CONFIG.PCW_MIO_8_PULLUP {disabled} \
   CONFIG.PCW_MIO_8_SLEW {fast} \
   CONFIG.PCW_MIO_9_DIRECTION {<Select>} \
   CONFIG.PCW_MIO_9_IOTYPE {<Select>} \
   CONFIG.PCW_MIO_9_PULLUP {<Select>} \
   CONFIG.PCW_MIO_9_SLEW {<Select>} \
   CONFIG.PCW_MIO_TREE_PERIPHERALS {unassigned#Quad SPI Flash#Quad SPI Flash#Quad SPI Flash#Quad SPI Flash#Quad SPI Flash#Quad SPI Flash#unassigned#Quad SPI Flash#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#SD 0#SD 0#SD 0#SD 0#SD 0#SD 0#unassigned#SD 0#UART 1#UART 1#unassigned#unassigned#unassigned#unassigned} \
   CONFIG.PCW_MIO_TREE_SIGNALS {unassigned#qspi0_ss_b#qspi0_io[0]#qspi0_io[1]#qspi0_io[2]#qspi0_io[3]/HOLD_B#qspi0_sclk#unassigned#qspi_fbclk#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#unassigned#clk#cmd#data[0]#data[1]#data[2]#data[3]#unassigned#cd#tx#rx#unassigned#unassigned#unassigned#unassigned} \
   CONFIG.PCW_NAND_GRP_D8_ENABLE {0} \
   CONFIG.PCW_NAND_PERIPHERAL_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_A25_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_CS0_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_CS1_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_SRAM_CS0_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_SRAM_CS1_ENABLE {0} \
   CONFIG.PCW_NOR_GRP_SRAM_INT_ENABLE {0} \
   CONFIG.PCW_NOR_PERIPHERAL_ENABLE {0} \
   CONFIG.PCW_PCAP_PERIPHERAL_DIVISOR0 {8} \
   CONFIG.PCW_PRESET_BANK1_VOLTAGE {LVCMOS 1.8V} \
   CONFIG.PCW_QSPI_GRP_FBCLK_ENABLE {1} \
   CONFIG.PCW_QSPI_GRP_FBCLK_IO {MIO 8} \
   CONFIG.PCW_QSPI_GRP_IO1_ENABLE {0} \
   CONFIG.PCW_QSPI_GRP_SINGLE_SS_ENABLE {1} \
   CONFIG.PCW_QSPI_GRP_SINGLE_SS_IO {MIO 1 .. 6} \
   CONFIG.PCW_QSPI_GRP_SS1_ENABLE {0} \
   CONFIG.PCW_QSPI_PERIPHERAL_DIVISOR0 {8} \
   CONFIG.PCW_QSPI_PERIPHERAL_ENABLE {1} \
   CONFIG.PCW_QSPI_PERIPHERAL_FREQMHZ {200} \
   CONFIG.PCW_QSPI_QSPI_IO {MIO 1 .. 6} \
   CONFIG.PCW_SD0_GRP_CD_ENABLE {1} \
   CONFIG.PCW_SD0_GRP_CD_IO {MIO 47} \
   CONFIG.PCW_SD0_GRP_POW_ENABLE {0} \
   CONFIG.PCW_SD0_GRP_WP_ENABLE {1} \
   CONFIG.PCW_SD0_GRP_WP_IO {EMIO} \
   CONFIG.PCW_SD0_PERIPHERAL_ENABLE {1} \
   CONFIG.PCW_SD0_SD0_IO {MIO 40 .. 45} \
   CONFIG.PCW_SDIO_PERIPHERAL_DIVISOR0 {32} \
   CONFIG.PCW_SDIO_PERIPHERAL_FREQMHZ {50} \
   CONFIG.PCW_SDIO_PERIPHERAL_VALID {1} \
   CONFIG.PCW_SINGLE_QSPI_DATA_MODE {x4} \
   CONFIG.PCW_SMC_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_SPI_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_TPIU_PERIPHERAL_DIVISOR0 {1} \
   CONFIG.PCW_TTC0_CLK0_PERIPHERAL_FREQMHZ {133.333333} \
   CONFIG.PCW_TTC0_CLK1_PERIPHERAL_FREQMHZ {133.333333} \
   CONFIG.PCW_TTC0_CLK2_PERIPHERAL_FREQMHZ {133.333333} \
   CONFIG.PCW_TTC0_PERIPHERAL_ENABLE {0} \
   CONFIG.PCW_TTC0_TTC0_IO {<Select>} \
   CONFIG.PCW_TTC_PERIPHERAL_FREQMHZ {50} \
   CONFIG.PCW_UART1_GRP_FULL_ENABLE {0} \
   CONFIG.PCW_UART1_PERIPHERAL_ENABLE {1} \
   CONFIG.PCW_UART1_UART1_IO {MIO 48 .. 49} \
   CONFIG.PCW_UART_PERIPHERAL_DIVISOR0 {16} \
   CONFIG.PCW_UART_PERIPHERAL_FREQMHZ {100} \
   CONFIG.PCW_UART_PERIPHERAL_VALID {1} \
   CONFIG.PCW_UIPARAM_ACT_DDR_FREQ_MHZ {525} \
   CONFIG.PCW_UIPARAM_DDR_BANK_ADDR_COUNT {3} \
   CONFIG.PCW_UIPARAM_DDR_BOARD_DELAY0 {0.176} \
   CONFIG.PCW_UIPARAM_DDR_BOARD_DELAY1 {0.159} \
   CONFIG.PCW_UIPARAM_DDR_BOARD_DELAY2 {0.162} \
   CONFIG.PCW_UIPARAM_DDR_BOARD_DELAY3 {0.187} \
   CONFIG.PCW_UIPARAM_DDR_CL {7} \
   CONFIG.PCW_UIPARAM_DDR_COL_ADDR_COUNT {10} \
   CONFIG.PCW_UIPARAM_DDR_CWL {6} \
   CONFIG.PCW_UIPARAM_DDR_DEVICE_CAPACITY {2048 MBits} \
   CONFIG.PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_0 {-0.073} \
   CONFIG.PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_1 {-0.034} \
   CONFIG.PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_2 {-0.03} \
   CONFIG.PCW_UIPARAM_DDR_DQS_TO_CLK_DELAY_3 {-0.082} \
   CONFIG.PCW_UIPARAM_DDR_DRAM_WIDTH {16 Bits} \
   CONFIG.PCW_UIPARAM_DDR_FREQ_MHZ {525} \
   CONFIG.PCW_UIPARAM_DDR_PARTNO {MT41K128M16 JT-125} \
   CONFIG.PCW_UIPARAM_DDR_ROW_ADDR_COUNT {14} \
   CONFIG.PCW_UIPARAM_DDR_SPEED_BIN {DDR3_1066F} \
   CONFIG.PCW_UIPARAM_DDR_TRAIN_DATA_EYE {1} \
   CONFIG.PCW_UIPARAM_DDR_TRAIN_READ_GATE {1} \
   CONFIG.PCW_UIPARAM_DDR_TRAIN_WRITE_LEVEL {1} \
   CONFIG.PCW_UIPARAM_DDR_T_FAW {40.0} \
   CONFIG.PCW_UIPARAM_DDR_T_RAS_MIN {35.0} \
   CONFIG.PCW_UIPARAM_DDR_T_RC {48.75} \
   CONFIG.PCW_UIPARAM_DDR_T_RCD {7} \
   CONFIG.PCW_UIPARAM_DDR_T_RP {7} \
   CONFIG.PCW_USB0_PERIPHERAL_ENABLE {0} \
   CONFIG.PCW_USB0_PERIPHERAL_FREQMHZ {60} \
   CONFIG.PCW_USB0_RESET_ENABLE {0} \
   CONFIG.PCW_USB0_RESET_IO {<Select>} \
   CONFIG.PCW_USB0_USB0_IO {<Select>} \
   CONFIG.PCW_USB1_RESET_ENABLE {0} \
   CONFIG.PCW_USB_RESET_ENABLE {0} \
   CONFIG.PCW_USB_RESET_SELECT {<Select>} \
   CONFIG.PCW_USE_M_AXI_GP0 {0} \
 ] $processing_system7_0

  # Create interface connections
  connect_bd_intf_net -intf_net processing_system7_0_DDR [get_bd_intf_ports DDR] [get_bd_intf_pins processing_system7_0/DDR]
  connect_bd_intf_net -intf_net processing_system7_0_FIXED_IO [get_bd_intf_ports FIXED_IO] [get_bd_intf_pins processing_system7_0/FIXED_IO]

  # Create port connections
  connect_bd_net -net Blinking_0_led_o [get_bd_ports led_o] [get_bd_pins Blinking_0/led_o]
  connect_bd_net -net clk_i_1 [get_bd_ports clk_i] [get_bd_pins Blinking_0/clk_i]

  # Create address segments


  # Restore current instance
  current_bd_instance $oldCurInst

  validate_bd_design
  save_bd_design
}
# End of create_root_design()


##################################################################
# MAIN FLOW
##################################################################

create_root_design ""
