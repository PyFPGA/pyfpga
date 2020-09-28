#!/usr/bin/make

PYTHON = ../venv/bin/python3

.PHONY: multi

all: general specific multi

general:
	$(PYTHON) capture.py

specific:
	$(PYTHON) ghdl/ghdl.py
	$(PYTHON) ise/ise.py --action all
	$(PYTHON) libero/libero.py --action all
	$(PYTHON) quartus/quartus.py --action all
	$(PYTHON) vivado/design.py
	$(PYTHON) vivado/vivado.py --action all
	$(PYTHON) yosys/yosys.py
	$(PYTHON) yosys/yosys.py --lang vhdl
	$(PYTHON) yosys/ise.py --action all
	$(PYTHON) yosys/ise.py --lang vhdl --action all
	$(PYTHON) yosys/vivado.py --action all
	$(PYTHON) yosys/vivado.py --lang vhdl --action all

multi:
	$(PYTHON) multi/memory.py
	$(PYTHON) multi/parameters.py
	$(PYTHON) multi/projects.py
	$(PYTHON) multi/strategies.py
	$(PYTHON) multi/verilog.py
	$(PYTHON) multi/vhdl.py
