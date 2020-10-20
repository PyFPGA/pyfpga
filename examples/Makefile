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
	$(PYTHON) ise/ise.py
	$(PYTHON) libero/libero.py
	$(PYTHON) openflow/icestorm.py
	$(PYTHON) openflow/icestorm.py --lang vhdl
	$(PYTHON) openflow/prjtrellis.py --board ecp5evn
	$(PYTHON) openflow/prjtrellis.py --lang vhdl
	$(PYTHON) quartus/quartus.py
	$(PYTHON) vivado/design.py
	$(PYTHON) vivado/vivado.py
	$(PYTHON) yosys/yosys.py
	$(PYTHON) yosys/yosys.py --lang vhdl
	$(PYTHON) yosys/ise.py
	$(PYTHON) yosys/ise.py --lang vhdl
	$(PYTHON) yosys/vivado.py
	$(PYTHON) yosys/vivado.py --lang vhdl
