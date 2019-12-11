# Changelog

## [v0.1.0] - 2019-12-??

* A class provides a Python API to work with FPGA Tools.
* The supported FPGA Tools are Ise and Vivado from Xilinx, Quartus Prime from
Intel/Altera and Libero-SoC from Microsemi.
* Documentation in the form of a User Guide and an API reference are provided.
* Examples for:
    * Basic and advanced projects.
    * Multi Project/Tool/Strategy.
    * Boards: s6micro, mkr, de10nano, zybo.

## History

The roots of this project date back to 2015, where a project called fpga_tools had Perl scripts to populate templates for the ISE tool.

In 2016 the project was renamed as fpga_helpers, changing Perl by Python and adding support for Vivado, Quartus and time after for Libero-SoC. The project evolved to a Makefile and two Tcl scripts, one for Synthesis and other for Programming, and a bunch of scripts to automate tasks.

At the end of 2019, a new project called pyfpga, superseded the previous one, where the Makefile and the Tcl scripts were replaced by a class to be used in Python scripts.

