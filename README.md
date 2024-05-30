# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-darkgreen?style=flat-square)](LICENSE)

![Vivado](https://img.shields.io/badge/Vivado-2019.2-blue.svg?style=flat-square)
![Quartus](https://img.shields.io/badge/Quartus--Prime-19.1-blue.svg?style=flat-square)
![Libero](https://img.shields.io/badge/Libero--Soc-12.2-blue.svg?style=flat-square)
![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg?style=flat-square)
![Openflow](https://img.shields.io/badge/Openflow-GHDL%20%7C%20Yosys%20%7C%20nextpnr%20%7C%20icestorm%20%7C%20prjtrellis-darkgreen.svg?style=flat-square)

> **WARNING:** (2024-05-20) PyFPGA is in the process of being strongly rewritten/simplified.
> Most changes are internal, but the API will also change.

PyFPGA is a **Python Package** for **vendor-agnostic** FPGA development.
It provides a **Class** which allows the programmatically execution of **synthesis**,
**place and route**, **bitstream generation** and/or **programming** of FPGA devices.
Additionally, a set of **command-line helpers** are provided for quick and simple runs.

Features:
* It's *Version Control Systems* and *Continuous Integration* friendly.
* Allows reproducibility and repeatability.
* Consumes fewer system resources than GUI based workflows.

With PyFPGA you can create your custom FPGA tool using a workflow tailored to your needs!

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
[HDL containers](https://hdl.github.io/containers) project, so
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
