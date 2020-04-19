#!/usr/bin/make

all: hdl2bit-vhdl hdl2bit-verilog prj2bit

hdl2bit-vhdl:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-f ../../hdl/*.vhdl,examples \
	--run syn \
	../../hdl/top.vhdl

hdl2bit-verilog:
	../../venv/bin/python3 ../../fpga/helpers/hdl2bit.py \
	--outdir ../../build/helpers \
	--tool ise \
	-i ../../hdl/headers1 \
	-i ../../hdl/headers2 \
	-f ../../hdl/blinking.v \
	--run syn \
	../../hdl/top.v

prj2bit:
	mkdir -p ../../build/helpers
	touch ../../build/helpers/test.xise
	../../venv/bin/python3 ../../fpga/helpers/prj2bit.py \
	--run syn \
	../../build/helpers/test.xise

clean:
	rm -fr ../../build/helpers
