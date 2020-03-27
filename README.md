# PyFPGA [![License](https://img.shields.io/badge/License-GPL--3.0-darkgreen)](LICENSE)

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
prj.add_files('location3/example.xdc')
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

### Bitstream Generation

![ISE](https://img.shields.io/badge/ISE-14.7-blue.svg)
![Libero](https://img.shields.io/badge/Libero--Soc-12.2-blue.svg)
![Quartus](https://img.shields.io/badge/Quartus--Prime-19.1-blue.svg)
![Vivado](https://img.shields.io/badge/Vivado-2019.2&nbsp;(*)-blue.svg)
![Yosys](https://img.shields.io/badge/Yosys-0.9&nbsp;dev&nbsp;(**)-orange.svg)

(*) Also supports Block Designs and export of hardware info to be used from SDK/Vitis.
(**) Yosys only performs synthesis. Can be used with ISE/Vivado to run implementation and
bitstream generation.

### Transfer

![ISE](https://img.shields.io/badge/ISE-FPGA,&nbsp;SPI&nbsp;and&nbsp;BPI-blue.svg)
![Libero](https://img.shields.io/badge/Libero--Soc-Unsupported&nbsp;(*)-red.svg)
![Quartus](https://img.shields.io/badge/Quartus--Prime-FPGA-green.svg)
![Vivado](https://img.shields.io/badge/Vivado-FPGA-green.svg)

(*) No available kit to test.

## Installation

To install a local clone of the repository:

```
git clone https://gitlab.com/rodrigomelo9/pyfpga.git
cd pyfpga
sudo pip install -e .
```

> With `-e` (`--editable`) your application is installed into site-packages via a kind of symlink,
> so you do not need to reinstall it after making, for example, a `git pull`.

To install from the online repository:

```
pip install -e 'git+https://gitlab.com/rodrigomelo9/pyfpga#egg=pyfpga'
```