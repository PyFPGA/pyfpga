# PyFPGA examples

## Generic examples

* [basic.py](basic.py): almost a minimal example.
* [advanced.py](advanced.py): logging capabilities, setting of options and
exception catch are used.

## Multipurpose examples

Examples where more than a project is solved in the same script.

* [multi_project.py](multi_project.py): use of a Python dict to change the
tool, the part, the HDL files and the top level.
* [multi_tool_verilog.py](multi_tool_verilog.py): use of a Python list
to synthesize the same Verilog files with the different available Tools.
* [multi_tool_vhdl.py](multi_tool_vhdl.py): use of a Python list
to synthesize the same VHDL files with the different available Tools.
* [multi_tool_strategy.py](multi_tool_strategy.py): based on the previous
example, here also the strategy is changed.

## Specific Tool examples

Examples for generate and transfer, where the Constraints files were also
specified. They works for the specified board (led blinking).

* [ise](ise): Spartan-6 FPGA LX9 MicroBoard (Avnet)
* [libero](libero): PolarFire FPGA Evaluation Kit (Microsemi)
* [quartus](quartus): DE10Nano (Terasic)
* [vivado](vivado): Zybo (Digilent)
