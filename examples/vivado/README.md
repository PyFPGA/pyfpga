# Vivado examples

The Zybo related things are the FPGA part and the constraints file.
Modify them to make this example compatible with another board.

* `generat.py` generates a bitstream based on VHDL files.
* `transfer.py` points to the same output directory than `generate.py` and allows to transfer the bitstream to the board.
* `design.py` generates the bitstream based on a Vivado Block design.

## How to get a compatible Vivado Block Design

* In the *Flow Navigator* panel, under *IP INTEGRATOR*, click on *Create Block Design*.
* Work on your design.
* *File* -> *Export* -> *Export Block Design* to create a Tcl file to re-generate your design.

> Tip: open the generated Tcl file and remove the following code (which is generally a problem instead of help):

```tcl
################################################################
# Check if script is running in correct Vivado version.
################################################################
set scripts_vivado_version 2019.2
set current_vivado_version [version -short]

if { [string first $scripts_vivado_version $current_vivado_version] == -1 } {
   puts ""
   catch {common::send_msg_id "BD_TCL-109" "ERROR" "This script was generated using Vivado <$scripts_vivado_version> and is being run in <$current_vivado_version> of Vivado. Please run the script in Vivado <$scripts_vivado_version> then open the design in Vivado <$current_vivado_version>. Upgrade the design by running \"Tools => Report => Report IP Status...\", then run write_bd_tcl to create an updated script."}

   return 1
}
```
