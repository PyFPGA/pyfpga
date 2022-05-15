# Changelog

## [v0.2.0] - 2022-05-15

NOTE: this log is probably outdated/incomplete, but PyFPGA will be strongly rewritten/simplified.

* Additional supported FPGA EDA Tools:
    - GHDL --synth: synthesizes VHDL sources.
    - ghdl-yosys-plugin: add VHDL support to Yosys.
    - Openflow: Yosys + nextpnr + icestrom/prjtrellis.
* Added CLI helper utilities:
    - hdl2bit: to go from FPGA design files to a bitstream.
    - prj2bit: to deal with a vendor FPGA Project file.
    - bitprog: to transfer a bitstream to a supported device
* Improves into the API classes:
    - Added relative_to_script to the Project class constructor.
    - Added the methods set_bitstream and clean.
    - Simplified code related to absolute and relative directories.
    - Exported some useful lists into the Tool class.
* Examples:
    - Improved examples with the addition of command-line arguments.
    - Added a GHDL example.
    - Added examples using VHDL with Yosys (through `ghdl-yosys-plugin`).
    - Added Openflow examples.
    - Fixed a small problem into examples/multi/vhdl.py.
* Testing:
    - Added some tests for the new CLI utilities.
    - Added vendor project files to test prj2bit.
    - Added a Makefile to run some examples as a test.

## [v0.1.0] - 2020-02-29

NOTE: originally released on 2020-02-29 at https://gitlab.com/rodrigomelo9/pyfpga

* FPGA Helpers switched to be a Python package which provides an API to manage projects
* Supported FPGA EDA Tools:
    - ISE and Vivado from Xilinx: bitstream generation and transfer to an FPGA (ISE also support
      SPI/BPI memories)
    - Quartus Prime from Intel/Altera: bitstream generation and transfer to an FPGA
    - Libero-SoC from Microchip/Microsemi: bitstream generation
    - Yosys: generic synthesizer or combined with ISE/Vivado (implementation and bitstream
      generation)
* The API implemented by the Project class provides:
    - A constructor where the TOOL must be specified and an optional PROJECT NAME can be specified
      (TOOL is used by default)
    - A method to set the target device PART (default values per TOOL are provided)
    - A method to add multiple HDL, Constraint and Tcl files to the project (in case of VHDL an
      optional PACKAGE NAME can be specified)
    - A method to specify the TOP-LEVEL (NAME or FILE)
    - A method to specify a different OUTPUT directory (build by default)
    - Methods to generate a bitstream and transfer it to a device (running the selected EDA Tool)
    - The capability of specifying an optimization strategy (area, power or speed) when the
      bitstream is generated
    - A method to add Verilog Included File directories
    - A method to specify generics/parameters values
    - Methods to add Tcl commands in up to six different parts of the Flow (workaround for not yet
      implemented features)
    - Optional logging capabilities which include the display of the Tool Execution Time
    - A method to get some project configurations for debug purposes
    - Methods to specify where to search an ip-repo, add a block design and export the hardware
      (Only supported for Xilinx Vivado)
* Documentation:
    - User Guide
    - API Reference
    - Development notes
    - Tools notes
* Examples:
    - General-purpose (boilerplate and capture)
    - Multi-purpose (memory, parameters, projects, strategies, verilog and vhdl)
    - Specific of each Tool where Constraint files are included (for the boards s6micro, mkr,
      de10nano and zybo)
* Testing:
    - Examples are used to test the correct Tool behaviour
    - The PART specification is particularly tested for ISE and Libero
    - The master Tcl is checked using Tclsh
    - The top-level specification is tested with different alternatives

## History

The roots of this project date back to 2015, where an internal project called fpga_tools, written
in Perl, was used to populate templates for the ISE tool.

In 2016 the project was renamed as fpga_helpers, changing Perl by Python, published as open-source
and adding support for Vivado, Quartus and time after for Libero-SoC.
The project evolved to a Makefile and two Tcl scripts, one for Synthesis and other for Programming,
all of them implementing multi-vendor support, with a few Python scripts to automate tasks.

At the end of 2019, a new project written from scratch, called PyFPGA, superseded the previous one,
where the use of the Makefile and the Tcl scripts were replaced by a Python class used to create
customized workflows.
