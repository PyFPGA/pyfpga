#!/usr/bin/make

all: pep8 pylint

pep8:
	@pycodestyle fpga

pylint:
	@pylint --errors-only fpga

pylint-full:
	@pylint fpga
