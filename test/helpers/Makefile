#!/usr/bin/make

all: vhdl verilog

vhdl:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-f ../../examples/hdl/*.vhdl,examples \
	--task syn \
	../../examples/hdl/top.vhdl

verilog:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-i ../../examples/hdl/headers1 \
	-i ../../examples/hdl/headers2 \
	-f ../../examples/hdl/blinking.v \
	--task syn \
	../../examples/hdl/top.v

clean:
	rm -fr ../../build/helpers
