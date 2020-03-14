#!/usr/bin/make

all: general specific multi

general:
	../../venv/bin/python3 ../../examples/capture.py

specific:
	../../venv/bin/python3 ../../examples/ise/generate.py
	../../venv/bin/python3 ../../examples/ise/transfer.py
	../../venv/bin/python3 ../../examples/libero/generate.py
	../../venv/bin/python3 ../../examples/quartus/generate.py
	../../venv/bin/python3 ../../examples/quartus/transfer.py
	../../venv/bin/python3 ../../examples/vivado/design.py
	../../venv/bin/python3 ../../examples/vivado/generate.py
	../../venv/bin/python3 ../../examples/vivado/transfer.py

multi:
	../../venv/bin/python3 ../../examples/multi/memory.py
	../../venv/bin/python3 ../../examples/multi/parameters.py
	../../venv/bin/python3 ../../examples/multi/projects.py
	../../venv/bin/python3 ../../examples/multi/strategies.py
	../../venv/bin/python3 ../../examples/multi/verilog.py
	../../venv/bin/python3 ../../examples/multi/vhdl.py
