#!/usr/bin/make

PYTHON = ../../venv/bin/python3
OUTDIR = ../../build/helpers
HLPDIR = ../../fpga/helpers

all: hdl2bit-vhdl hdl2bit-verilog prj2bit bitprog

hdl2bit-vhdl:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(OUTDIR) \
	--tool ise \
	-f ../../hdl/*.vhdl,examples \
	--run syn \
	../../hdl/top.vhdl

hdl2bit-verilog:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(OUTDIR) \
	--tool ise \
	-i ../../hdl/headers1 \
	-i ../../hdl/headers2 \
	-f ../../hdl/blinking.v \
	--run syn \
	../../hdl/top.v

prj2bit:
	mkdir -p $(OUTDIR)
	touch $(OUTDIR)/test.xise
	$(PYTHON) $(HLPDIR)/prj2bit.py \
	--run syn \
	$(OUTDIR)/test.xise

bitprog:
	$(PYTHON) $(HLPDIR)/bitprog.py \
	--outdir $(OUTDIR) \
	--tool ise \
	-d fpga -p 2 \
	../../README.md

clean:
	rm -fr $(OUTDIR)
