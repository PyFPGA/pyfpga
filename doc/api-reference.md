# Module fpga.project documentation

fpga.project

This module implements the main class of PyFPGA, which provides
functionalities to create a project, generate a bitstream and transfer it to a
Device.

## Class Project

Class to manage an FPGA project.

### `__init__(tool='vivado', project=None, relative_to_script=True)`

Class constructor.

* **tool:** FPGA tool to be used.
* **project:** project name (the tool name is used if none specified).
* **relative_to_script:** specifies if the files/directories are
relative to the script or the execution directory.

### `add_design(pathname)`

Adds a Block Design.

* **pathname:** a string containing a relative path to a file.

### `add_files(pathname, library=None)`

Adds files to the project (HDLs, TCLs, Constraints).

* **pathname:** a string containing a relative path specification,
and can contain shell-style wildcards (glob compliant).
* **library:** an optional VHDL library name.

### `add_hook(hook, phase='postprj')`

Adds a hook in the specified phase.

A hook is a place that allows you to insert customized programming.

The valid **phase** values are:
* *prefile* to add options needed to find files.
* *postprj* to add project related options.
* *preflow* to change options previous to run the flow.
* *postsyn* to perform an action between *syn* and *imp*.
* *postimp* to perform an action between *imp* and *bit*.
* *postbit* to perform an action after *bit*.

The *hook* is a string representing a tool specific command.

**WARNING:** using a hook, you will be probably broken the vendor
independence.

### `add_include(pathname)`

Adds a search path.

Useful to specify where to search Verilog Included Files or IP
repositories.

* **pathname:** a string containing a relative path to a directory
or a file.

**Note:** generally a directory must be specified, but Libero-SoC
also needs to add the file when is a Verilog Included File.

### `clean()`

Clean the generated project files.

### `export()`

Exports files for the development of a Processor System.

Useful when working with FPGA-SoCs to provide information for the
development of the Processor System side.

### `generate(strategy='default', to_task='bit', from_task='prj', capture=False)`

Run the FPGA tool.

* **strategy:** *default*, *area*, *speed* or *power*.
* **to_task:** last task.
* **from_task:** first task.
* **capture:** capture STDOUT and STDERR (returned values).

The valid tasks values, in order, are:
* *prj* to creates the project file.
* *syn* to performs the synthesis.
* *imp* to runs implementation.
* *bit* to generates the bitstream.

### `get_configs()`

Gets the Project Configurations.

It returns a dict which includes *tool* and *project* names, the
*extension* of a project file (according to the selected tool) and
the *part* to be used.

### `set_bitstream(path)`

Set the bitstream file to transfer.

* **path:** path to the bitstream file.

### `set_board(board)`

Sets a development board to have predefined values.

* **board:** board name.

**Note:** Not Yet Implemented.

### `set_outdir(outdir)`

Sets the OUTput DIRectory (where to put the resulting files).

* **outdir:** path to the output directory.

### `set_param(name, value)`

Set a Generic/Parameter Value.

### `set_part(part)`

Set the target FPGA part.

* **part:** the FPGA part as specified by the tool.

### `set_top(toplevel)`

Set the top level of the project.

* **toplevel:** name or file path of the top level entity/module.

### `transfer(devtype='fpga', position=1, part='', width=1, capture=False)`

Transfers the generated bitstream to a device.

* **devtype:** *fpga* or other valid option
(depending on the used tool, it could be *spi*, *bpi, etc).
* **position:** position of the device in the JTAG chain.
* **part:** name of the memory (when device is not *fpga*).
* **width:** bits width of the memory (when device is not *fpga*).
* **capture:** capture STDOUT and STDERR (returned values).

