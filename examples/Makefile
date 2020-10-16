#!/usr/bin/make

PYTHON = ../venv/bin/python3

.PHONY: multi helpers

all: general specific multi helpers

general:
	$(PYTHON) capture.py

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

multi:
	$(PYTHON) multi/memory.py
	$(PYTHON) multi/parameters.py
	$(PYTHON) multi/projects.py
	$(PYTHON) multi/verilog.py
	$(PYTHON) multi/vhdl.py

helpers:
	make -C helpers
