#!/usr/bin/make

PYTHON = ../venv/bin/python3

.PHONY: helpers misc multi

all: helpers misc multi specific

helpers:
	make -C $@

misc:
	$(PYTHON) $@/capture.py

multi:
	$(PYTHON) $@/memory.py
	$(PYTHON) $@/parameters.py
	$(PYTHON) $@/projects.py
	$(PYTHON) $@/verilog.py
	$(PYTHON) $@/vhdl.py

specific:
	$(PYTHON) ghdl/ghdl.py
	$(PYTHON) ise/ise.py --action all
	$(PYTHON) libero/libero.py --action all
	$(PYTHON) openflow/icestorm.py --action all
	$(PYTHON) openflow/icestorm.py --action all --lang vhdl
	$(PYTHON) openflow/prjtrellis.py --action all
	$(PYTHON) openflow/prjtrellis.py --action all --lang vhdl
	$(PYTHON) quartus/quartus.py --action all
	$(PYTHON) vivado/design.py
	$(PYTHON) vivado/vivado.py --action all
	$(PYTHON) yosys/yosys.py
	$(PYTHON) yosys/yosys.py --lang vhdl
	$(PYTHON) yosys/ise.py --action all
	$(PYTHON) yosys/ise.py --action all --lang vhdl
	$(PYTHON) yosys/vivado.py --action all
	$(PYTHON) yosys/vivado.py --action all --lang vhdl
