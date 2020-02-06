# PyFPGA examples

## General purpose examples

* [advanced.py](advanced.py): logging capabilities, setting of options and
exception catch are used.
* [capture.py](capture.py): the execution messages are captured.

## Specific Tool examples

Examples for generate and transfer, where the Constraints files were also
specified. A led blinking is implemented over the specified board.

* [ise](ise): Spartan-6 FPGA LX9 MicroBoard (Avnet)
* [libero](libero): Digi-Key SmartFusion2 Maker Board (Digi-Key)
* [quartus](quartus): DE10Nano (Terasic)
* [vivado](vivado): Zybo (Digilent)

## Multi purpose examples

Examples where more than a project is solved in the same script.

* [multi_project.py](multi_project.py): it uses a dict with three project names
where different tools, part names, files and top-level names can be specified.
In this manner, you can manage alternatives or sub-products of your design in
a single place.
* [multi_tool_params.py](multi_tool_params.py): VHDL and Verilog files are
synthesized changing the value of its generics/parameters.
* [multi_tool_verilog.py](multi_tool_verilog.py): here the same set of Verilog
files are synthesised with all the available tools, which is useful to make
comparations and check portability.
* [multi_tool_vhdl.py](multi_tool_vhdl.py): the same concept that the previous
one, but using VHDL instead of Verilog files. The main difference is how to
deal with VHDL libraries.
* [multi_tool_strategy.py](multi_tool_strategy.py): based on the previous
examples, the strategy is changed, useful to make comparison with different
optimizations.
