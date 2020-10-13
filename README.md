# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-darkgreen)](LICENSE)

![GDHL](https://img.shields.io/badge/GHDL-last-brightgreen.svg)
![icestorm](https://img.shields.io/badge/icestorm-last-brightgreen.svg)
![nextpnr](https://img.shields.io/badge/nextpnr-last-brightgreen.svg)
![prjtrellis](https://img.shields.io/badge/prjtrellis-last-brightgreen.svg)
![Yosys](https://img.shields.io/badge/Yosys-last-brightgreen.svg)

![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg)
![Libero](https://img.shields.io/badge/Libero--Soc-12.2-blue.svg)
![Quartus](https://img.shields.io/badge/Quartus--Prime-19.1-blue.svg)
![Vivado](https://img.shields.io/badge/Vivado-2019.2-blue.svg)

A Python Class to use FPGA development tools in a vendor-independent way.

With PyFPGA you can create a project file, synthesizes, implements, generates a bitstream and
transfers it to a supported device, all in a programmatic way. You can create your own FPGA Tool
using a workflow tailored to your needs, with the following advantages:

* Provides a vendor-independent experience.
* Uses Python as the programming language.
* The workflow is solved from the command-line, which:
    - Is friendly with *Version Control Systems* and *Continuous Integration*.
    - Provides reproducibility and repeatability.
    - Consumes fewer system resources.

A simple example of how to use PyFPGA:

```py
from fpga.project import Project

# Specify the backend tool and an optional project name
prj = Project('vivado', 'example')

# Set the FPGA, the project files and the top-level name
prj.set_part('xc7z010-1-clg400')
prj.add_files('location1/*.v')
prj.add_files('location2/top.v')
prj.add_files('location3/example.xdc')  # Vivado implementation constraints
prj.set_top('Top')

# Generate the bitstream running the tool
prj.generate()
```

> More examples into the [User Guide](doc/user_guide.md) and under the [examples](examples)
> directory.

The API implemented by the `Project class` provides:
* A constructor where the TOOL must be specified and an optional PROJECT NAME can be indicated
* Methods to set the target device PART, to add multiple HDL, Constraint and Tcl files to the
  project (in case of VHDL an optional PACKAGE NAME can be specified) and to specify the TOP-LEVEL
* Methods to specify a different OUTPUT directory or get some project configurations
* Methods to generate a bitstream and transfer it to a device (running the selected EDA Tool)
* The capability of specifying an optimization strategy (area, power or speed) when the bitstream
  is generated
* A method to add Verilog Included File directories
* A method to specify generics/parameters values
* Methods to add Tcl commands in up to six different parts of the Flow (workaround for not yet
  implemented features)
* Optional logging capabilities which include the display of the Tool Execution Time
* Methods to specify where to search an ip-repo, add a block design and export the hardware
  (only supported for Vivado)

## Support

PyFPGA is a Python 3 package, which was developed under a Debian GNU/Linux.
It must run in any other POSIX compatible Operating System and probably also in a different OS
(the problem could be how the backends tools are called, please let me know any SUCCESS or FAIL
using the [issues](https://gitlab.com/rodrigomelo9/pyfpga/issues) tracker).

* The whole development flow, from reading HDL and constraint sources to produce a bitstream, can
be performed with ISE and Vivado (Xilinx), Quarts Prime (Intel), Libero-SoC (Microsemi) and
open-source tools.
* ISE (Impact) can be used to programming FPGAs, BPIs and SPIs memories. Vivado, Quartus and
iceprog (IceStorm, for ice40 devices) can be used to programming FPGAs. Libero-SoC and
prjtrellis programming is not yet supported.
* GDHL (`--synth`) can be used to convert VHDL sources into a synthesized VHDL.
* Yosys cab be used to convert Verilog and VHDL (using `ghdl-yosys-plugin`) sources into a
synthetized Verilog. Also, ISE and Vivado are supported as backend tools to generate a bitstream.

**Notes:**
* The open-source tools are supported trough Docker images from the
[ghdl/docker](https://github.com/ghdl/docker) project, so Docker must be
[installed](https://docs.docker.com/install).
* ISE, Libero-Soc, Quartus Prime and Vivado, must be ready to be executed from the terminal
(installed and well configured).

## Installation

PyFPGA Python 3.5+ and can be installed from the online repository with:

```
pip install 'git+https://gitlab.com/rodrigomelo9/pyfpga#egg=pyfpga'
```
