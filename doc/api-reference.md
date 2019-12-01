# Module fpga.project documentation

fpga.project

Main Class of PyFPGA, which provides functionalities to create a project,
generate files and transfer to a Device.

## Class Project

Manage an FPGA project.

### `add_files(self, pathname, lib=None)`

Add files to the project.

PATHNAME must be a string containing an absolute or relative path
specification, and can contain shell-style wildcards.
LIB is optional and only useful for VHDL files.

### `add_postbit_opt(self, option)`

Add a post bitstream generation OPTION.

### `add_postimp_opt(self, option)`

Add a post implementation OPTION.

### `add_postsyn_opt(self, option)`

Add a post synthesis OPTION.

### `add_preflow_opt(self, option)`

Add a pre flow OPTION.

### `add_project_opt(self, option)`

Add a project OPTION.

### `generate(self, strategy='none', to_task='bit', from_task='prj')`

Run the FPGA tool.

The valid STRATEGIES are none (default), area, speed and power.
The valid TASKS are prj to only create the project file, syn for also
performs the synthesis, imp to add implementation and bit (default)
to finish with the bitstream generation.

### `get_configs(self)`

Get the Project Configurations.

### `set_board(self, board)`

Set the board to use.

A BOARD is a dictionary with predefined devices.

### `set_outdir(self, outdir)`

Set the OUTput DIRectory.

### `set_part(self, part)`

Set the target PART.

### `set_top(self, toplevel)`

Set the TOP LEVEL of the project.

### `transfer(self, devtype='fpga', position=1, part='', width=1)`

Transfer a bitstream.

