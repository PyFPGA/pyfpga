#!/usr/bin/make

PYTHON = ../../venv/bin/python3
OUTDIR = ../../build/helpers
HLPDIR = ../../fpga/helpers
HDLDIR = ../../hdl

all: hdl2bit-vhdl hdl2bit-verilog prj2bit bitprog

hdl2bit-vhdl:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(OUTDIR) \
	--tool ise --run syn \
	-f $(HDLDIR)/*.vhdl,examples $(HDLDIR)/top.vhdl

hdl2bit-verilog:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(OUTDIR) \
	--tool ise --run syn \
	-i $(HDLDIR)/headers1 -i $(HDLDIR)/headers2 \
	-f $(HDLDIR)/blinking.v $(HDLDIR)/top.v

prj2bit:
	mkdir -p $(OUTDIR)
	cp ise.xise quartus.* vivado.xpr $(OUTDIR)
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(OUTDIR)/ise.xise
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(OUTDIR)/quartus.qpf
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(OUTDIR)/vivado.xpr

bitprog:
	$(PYTHON) $(HLPDIR)/bitprog.py \
	--outdir $(OUTDIR) \
	--tool ise \
	-d fpga -p 2 \
	../../README.md

clean:
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(OUTDIR)/ise.xise
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(OUTDIR)/quartus.qpf
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(OUTDIR)/vivado.xpr
