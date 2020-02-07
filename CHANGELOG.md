# Changelog

## [v0.1.0] - 2020-02-??

* FPGA Helpers switched to be a Python package which provides an API to manage projects
* Supported FPGA EDA Tools:
    - Ise and Vivado from Xilinx
    - Quartus Prime from Intel/Altera
    - Libero-SoC from Microsemi
    - Yosys (as a generic synthesizer or combined with ISE and Vivado)
* The API provides:
    - A constructor where the TOOL must be specified and an optional PROJECT NAME can be provided
      (TOOL is used as default)
    - A method to set the target device PART (default values per TOOL are provided)
    - A method to add multiple HDL, Constraint and Tcl files to the project (in case of VHDL an
      optional PACKAGE NAME can be specified)
    - A method to specify the TOP-LEVEL (NAME or FILE)
    - A method to specify the OUTPUT directory (build by default)
    - Methods to generate a bitstream and transfer it to a device (running the selected EDA Tool)
    - A method to add Verilog Included File directories
    - Methods to add Tcl options in six different parts of the Flow (workaround for not yet
      implemented features)
    - Optional logging capabilities which include the display of the Tool Execution Time
    - A method to get some project configurations for debug purposes
    - Methods to specify where to search an ip-repo, add a block design and export the hardware
      (Only supported for Xilinx Vivado)
* Documentation:
    - User Guide
    - API Reference
    - Development Notes
* Examples:
    - General-purpose (advanced and capture)
    - Multi-purpose (memory, parameters, projects, strategies, verilog and vhdl)
    - Specific of each Tool where Constraint files are included (for the boards s6micro, mkr,
      de10nano and zybo respectively)
* Testing:
    - Examples are used to test the correct Tool behaviour
    - The PART specification is particularly tested for ISE and Libero
    - The master Tcl is checked using tclsh
    - The top-level specification is tested with different alternatives

## History

The roots of this project date back to 2015, where an internal project called
fpga_tools, written in Perl, was used to populate templates for the ISE tool.

In 2016 the project was renamed as fpga_helpers, changing Perl by Python,
published as open-source and adding support for Vivado, Quartus and time after
for Libero-SoC.
The project evolved to a Makefile and two Tcl scripts, one for Synthesis and
other for Programming, all of them implementing multi-vendor support, with a
few Python scripts to automate tasks.

At the end of 2019, a new project written from scratch, called PyFPGA,
superseded the previous one, where the use of the Makefile and the Tcl scripts
were replaced by a Python class used to create customized workflows.
