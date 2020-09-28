# PyFPGA examples

## General-purpose examples

The general-purpose examples present some features, regardless of the selected
tool or device.

* [boilerplate.py](boilerplate.py): an example where almost all the
capabilities of the Project class are used, to be employed as starting point.
* [capture.py](capture.py): it shows how to capture the execution messages.

## Tool-specific examples

Led blinking examples where a Bitstream is generated and transfer to a
supported board. It shows the inclusion of Constraints files.

* [ghdl](ghdl): VHDL synthesis with GDHL (`--synth`)
* [ise](ise): Spartan-6 FPGA LX9 MicroBoard (Avnet)
* [libero](libero): Digi-Key SmartFusion2 Maker Board (Digi-Key)
* [quartus](quartus): DE10Nano (Terasic)
* [vivado](vivado): Zybo (Digilent)
* [yosys](yosys):
  * Verilog synthesis with Yosys (using `ghdl-yosys-plugin` for VHDL)
  * Spartan-6 FPGA LX9 MicroBoard (`ise.py`)
  * Zybo (`vivado.py`)

## Multi-project examples

Examples where more than a project is solved in the same script.

* [multi/projects.py](multi/projects.py): it uses a dict with three project
names where different tools, part names, files and top-level names can be
specified. In this manner, you can manage alternatives or sub-products of your
design in a single place.
* [multi/verilog.py](multi/verilog.py): here the same set of Verilog files are
synthesised with all the available tools, which is useful to make comparations
and check portability.
* [multi/vhdl.py](multi/vhdl.py): the same concept that the previous one, but
using VHDL instead of Verilog files. The main difference is how to deal with
VHDL libraries.
* [multi/strategies.py](multi/strategies.py): based on the previous examples,
the strategy is changed, useful to make comparison with different
optimizations.
* [multi/parameters.py](multi/parameters.py): VHDL and Verilog files are
synthesized changing the value of its generics/parameters.
* [multi/memory.py](multi/memory.py): it tests the Memory Content Files
inclusion capability of the supported tools.
