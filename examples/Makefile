#!/usr/bin/make

PYTHON = ../venv/bin/python3

all: general specific multi

general:
	$(PYTHON) capture.py

specific:
	$(PYTHON) ise/generate.py
	$(PYTHON) ise/transfer.py
	$(PYTHON) libero/generate.py
	$(PYTHON) quartus/generate.py
	$(PYTHON) quartus/transfer.py
	$(PYTHON) vivado/design.py
	$(PYTHON) vivado/generate.py
	$(PYTHON) vivado/transfer.py
	$(PYTHON) yosys/generic.py

multi:
	$(PYTHON) multi/memory.py
	$(PYTHON) multi/parameters.py
	$(PYTHON) multi/projects.py
	$(PYTHON) multi/strategies.py
	$(PYTHON) multi/verilog.py
	$(PYTHON) multi/vhdl.py
