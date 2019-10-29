#!/usr/bin/make

all: pep8 pylint

pep8:
	@pycodestyle fpga

pylint:
	@pylint --errors-only fpga

pylint-full:
	@pylint fpga

venv:
	virtualenv $@ --python=python3
	$@/bin/python3 -m pip install -e .
	@rm -fr pyfpga.egg-info

clean:
	@rm -fr venv
