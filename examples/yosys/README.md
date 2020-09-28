# Yosys examples

## Yosys synthesis

* Verilog project: `python3 yosys.py`
* VHDL project: `python3 yosys.py --lang vhdl`

## Yosys using ISE as backend

Bitstream generation:
* Verilog project: `python3 ise.py`
* VHDL project: `python3 ise.py --lang vhdl`

Spartan-6 FPGA LX9 MicroBoard programming:
* Verilog project: `python3 ise.py --action transfer`
* VHDL project: `python3 ise.py --lang vhdl --action transfer`

## Yosys using Vivado as backend

Bitstream generation:
* Verilog project: `python3 vivado.py`
* VHDL project: `python3 vivado.py --lang vhdl`

Zybo programming:
* Verilog project: `python3 vivado.py --action transfer`
* VHDL project: `python3 vivado.py --lang vhdl --action transfer`
