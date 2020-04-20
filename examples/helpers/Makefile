#!/usr/bin/make

PYTHON = ../../venv/bin/python3
BLDDIR = ../../build/helpers
HLPDIR = ../../fpga/helpers
HDLDIR = ../../hdl

all: hdl2bit-vhdl hdl2bit-verilog prj2bit

hdl2bit-vhdl:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(BLDDIR) \
	--tool ise --run syn \
	-f $(HDLDIR)/*.vhdl,examples $(HDLDIR)/top.vhdl

hdl2bit-verilog:
	$(PYTHON) $(HLPDIR)/hdl2bit.py \
	--outdir $(BLDDIR) \
	--tool ise --run syn \
	-i $(HDLDIR)/headers1 -i $(HDLDIR)/headers2 \
	-f $(HDLDIR)/blinking.v $(HDLDIR)/top.v

prj2bit:
	mkdir -p $(BLDDIR)
	cp ise.xise quartus.qpf vivado.xpr $(BLDDIR)
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(BLDDIR)/ise.xise
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(BLDDIR)/quartus.qpf
	$(PYTHON) $(HLPDIR)/prj2bit.py --run syn $(BLDDIR)/vivado.xpr

clean:
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(BLDDIR)/ise.xise
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(BLDDIR)/quartus.qpf
	$(PYTHON) $(HLPDIR)/prj2bit.py --clean $(BLDDIR)/vivado.xpr
