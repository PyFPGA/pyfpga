# Notes about the development of PyFPGA

PyFPGA try to be PEP8 compliant.

## fpga/tool/template.tcl

Many (all?) FPGA development Tools provides a Tcl (Tool Command Language)
interface for the Bitstream generation.
This multi-vendor master Tcl was developed, where the different commands to
solve the complete workflow were encapsulated into procedures
(using the `fpga_*` prefix to avoid namespace conflicts).

> To add a new Tool, a *case* in the *switch* of each `fpga_*` must be
> provided.

## fpga/tool/*.py

A base class (`__init__.py`) was developed to provides a uniform API to be implemented for each Tool to support.
Also, validation of values is performed here.

Classes to supports each Tool (`<TOOL>.py`) implements the base class, ideally
setting a few variables.

> Transfer of the bitstream to a device is not always performed by a Tcl
> script, so special methods must be developed, following the proposed API.

## fpga/project.py
