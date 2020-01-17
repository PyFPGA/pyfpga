# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-orange)](LICENSE)

A Python Class and helper scripts to use FPGA development tools in a
vendor-independent way.

With PyFPGA you can create a project file, synthesizes, implements, generates
a bitstream and transfers to a supported device, all in a programmatic way.
You can create your own FPGA Tool using a workflow tailored to your needs.

Features:

* Provides a vendor-independent experience.
* Has the advantages to using Python as the programming language.
* The workflow is solved from the command-line, which have extra advantages:
    * Is friendly with *Version Control Systems* and *Continuous Integration*.
    * Provides reproducibility and repeatability.
    * Consumes fewer system resources.

## Support

PyFPGA was developed under a Debian GNU/Linux, but it must run in any other
POSIX compatible operating system and probably also with a Linux Bash under
Windows (or maybe PowerSheel? Please let me know if you try).

### Bitstream Generation

![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg)
![Libero](https://img.shields.io/badge/Libero--Soc-12.2-blue.svg)
![Quartus](https://img.shields.io/badge/Quartus--Prime-19.1-blue.svg)
![Vivado](https://img.shields.io/badge/Vivado-2019.2-blue.svg)
![Yosys](https://img.shields.io/badge/Yosys-0.9&nbsp;(*)-green.svg)

(*) Only performs synthesis.

### Transfer

![ISE](https://img.shields.io/badge/ISE-FPGA,&nbsp;SPI&nbsp;and&nbsp;BPI-blue.svg)
![Libero](https://img.shields.io/badge/Libero--Soc-Unsupported&nbsp;(*)-red.svg)
![Quartus](https://img.shields.io/badge/Quartus--Prime-FPGA-green.svg)
![Vivado](https://img.shields.io/badge/Vivado-FPGA-green.svg)

(*) No available kit to test.

## Installation

* From this repository: `pip3 install .`

> The FPGA tool to be used in the backend must be well installed, have the
> license configured and be available to run from a terminal.
