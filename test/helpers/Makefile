#!/usr/bin/make

all: hdl2bit-vhdl hdl2bit-verilog prj2bit

hdl2bit-vhdl:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-f ../../examples/hdl/*.vhdl,examples \
	--run syn \
	../../examples/hdl/top.vhdl

hdl2bit-verilog:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-i ../../examples/hdl/headers1 \
	-i ../../examples/hdl/headers2 \
	-f ../../examples/hdl/blinking.v \
	--run syn \
	../../examples/hdl/top.v

prj2bit:
	mkdir -p ../../build/helpers
	touch ../../build/helpers/test.xise
	../../venv/bin/python3 ../../fpga/helpers/prj2bit.py \
	--run syn \
	../../build/helpers/test.xise

clean:
	rm -fr ../../build/helpers
