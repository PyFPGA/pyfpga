# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-orange)](LICENSE)

A Python Class and helper scripts to use FPGA development tools in a vendor-independent way.

Features:

* Provides a vendor-independent experience.
* Has the advantages to using Python as the programming language.
* The workflow is solved from the command-line, which have extra advantages:
    * Is friendly with *Version Control Systems* and *Continuous Integration*.
    * Provides reproducibility and repeatability.
    * Consumes fewer system resources.

## Support

![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg)
![Libero](https://img.shields.io/badge/Libero&nbsp;Soc-12.2-blue.svg)
![Quartus](https://img.shields.io/badge/Quartus&nbsp;Prime-19.1-blue.svg)
![Vivado](https://img.shields.io/badge/Vivado-2019.1-blue.svg)

> PyFPGA was developed under a Debian GNU/Linux, but it must run in any other
> POSIX compatible operating system and probably also with a Linux Bash under
> Windows (or maybe PowerSheel? Please let me know if you try).

In all cases, it is implemented at least until the bitstream generation.
As for the transfer, the supported devices are:
* ISE: FPGA, SPI and BPI.
* Quartus, Vivado: FPGA.
* Libero-SoC: unsupported (I have not a kit were to test).

> ISE, Quartus and Vivado supports the auto-detection of the Jtag Chain.

## Installation

* From this repository: `pip3 install .`

> The FPGA tool to be used in the backend must be well installed, have the
> license configured and be available to run from the terminal.
