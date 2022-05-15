# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-darkgreen?style=flat-square)](LICENSE)

![GDHL](https://img.shields.io/badge/GHDL-last-brightgreen.svg?style=flat-square)
![icestorm](https://img.shields.io/badge/icestorm-last-brightgreen.svg?style=flat-square)
![nextpnr](https://img.shields.io/badge/nextpnr-last-brightgreen.svg?style=flat-square)
![prjtrellis](https://img.shields.io/badge/prjtrellis-last-brightgreen.svg?style=flat-square)
![Yosys](https://img.shields.io/badge/Yosys-last-brightgreen.svg?style=flat-square)

![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg?style=flat-square)
![Libero](https://img.shields.io/badge/Libero--Soc-12.2-blue.svg?style=flat-square)
![Quartus](https://img.shields.io/badge/Quartus--Prime-19.1-blue.svg?style=flat-square)
![Vivado](https://img.shields.io/badge/Vivado-2019.2-blue.svg?style=flat-square)

PyFPGA is a **Python** Class for **vendor-independent FPGA development**.
It allows using **a single project file** and **programmatically** executing
**synthesis**, **implementation**, generation of **bitstream** and/or
**transference** to supported boards.

- The workflow is command-line centric.
- It's friendly with *Version Control Systems* and *Continuous Integration* (CI).
- Allows reproducibility and repeatability.
- Consumes fewer system resources than GUI based workflows.

Create your custom FPGA Tool using a workflow tailored to your needs!

> **WARNING:** (2022-05-15) PyFPGA is in the process of being strongly rewritten/simplified.
> Most changes are internal, but the API (`Project` class) will change.

## Usage

A minimal example of how to use PyFPGA:

```py
from fpga import Project

# Specify the backend tool and an optional project name
prj = Project('vivado', 'example')

# Set the device/part
prj.set_part('xc7z010-1-clg400')

# Add HDL sources to the project
prj.add_files('location1/*.v')
prj.add_files('location2/top.v')

# Optionally add constraint files to the project
prj.add_files('location3/example.xdc')

# Set the top-level unit name
prj.set_top('Top')

# Generate the bitstream running the tool
prj.generate()
```

Now, you can read the [docs](https://pyfpga.github.io/pyfpga/) or find
more examples in subdir [examples](examples).

The API implemented by the `Project class` provides:

- A constructor where the TOOL must be specified and an optional PROJECT NAME can be indicated
- Methods to set the target device PART, to add multiple HDL, Constraint and Tcl files to the
 project (in case of VHDL an optional PACKAGE NAME can be specified) and to specify the TOP-LEVEL
- Methods to specify a different OUTPUT directory or get some project configurations
- Methods to generate a bitstream and transfer it to a device (running the selected EDA Tool)
- The capability of specifying an optimization strategy (area, power or speed) when the bitstream
 is generated
- A method to add Verilog Included File directories
- A method to specify generics/parameters values
- Methods to add Tcl commands in up to six different parts of the Flow (workaround for not yet
 implemented features)
- Optional logging capabilities which include the display of the Tool Execution Time

## Support

PyFPGA is a Python 3 package, which is developed on Debian GNU/Linux.
It should run on any other POSIX compatible OS and probably also on different OS.
Should you achieve either success of failure on non-POSIX systems, please let us know through the
[issue](https://github.com/PyFPGA/pyfpga/issues) tracker.

- The whole development flow (from reading HDL and constraint sources to producing a bitstream)
 can be performed with ISE (Xilinx), Vivado (Xilinx), Quarts Prime (Intel/Altera), Libero-SoC
 (Microsemi) and/or with open-source tools.
- GDHL (`--synth`) allows converting VHDL sources into a VHDL 1993 netlist.
- Yosys allows synthesising Verilog and VHDL (using `ghdl-yosys-plugin`) and supports multiple
 output formats: JSON, Verilog, EDIF, etc.
  - nextpnr can be used for implementation of JSON netlists.
  - Also, ISE and Vivado are supported for implementation of Verilog netlists.
- Transferring bitstreams and programming devices:
  - ISE (Impact) can be used for programming FPGAs and/or memories (BPI and SPI) through JTAG.
  - Vivado, Quartus and iceprog (IceStorm, for ice40 devices) can be used to programming FPGAs.
  - Programming with Libero-SoC and programming ECP5 devices (prjtrellis, openocd) is not yet
   supported.

**Notes:**

- The open-source tools are supported trough container images from the
[ghdl/docker](https://github.com/ghdl/docker) project, so
[Docker](https://www.docker.com/) ~~or [Podman](https://podman.io/)~~ must be
installed. The same workflow can be used in CI services.
- ISE, Libero-Soc, Quartus Prime and Vivado, must be ready to be executed from
the terminal (installed and well configured).

## Installation

PyFPGA requires Python `>=3.6`. For now, it's only available as a git repository
hosted on GitHub. It can be installed with pip:

```
pip install 'git+https://github.com/PyFPGA/pyfpga#egg=pyfpga'
```

> On GNU/Linux, installing pip packages on the system requires `sudo`.
> Alternatively, use `--local` for installing PyFPGA in your HOME.

You can get a copy of the repository either through git clone or downloading a
tarball/zipfile:

```
git clone https://github.com/PyFPGA/pyfpga.git
cd pyfpga
```

Then, use pip from the root of the repo:

```
pip install -e .
```

> With `-e` (`--editable`) your application is installed into site-packages via
> a kind of symlink. That allows pulling changes through git or changing the
> branch, without the need to reinstall the package.
