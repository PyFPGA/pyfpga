#!/usr/bin/make

all: pep8 pylint

pep8: venv
	$</bin/pycodestyle fpga examples

pylint: venv
	$</bin/pylint --errors-only fpga examples

pylint-full: venv
	$</bin/pylint fpga examples

test: venv
	$</bin/python3 examples/test.py

venv:
	virtualenv $@ --python=python3
	$@/bin/python3 -m pip install -e .
	$@/bin/python3 -m pip install pyclean
	$@/bin/python3 -m pip install pycodestyle
	$@/bin/python3 -m pip install pylint
	@rm -fr pyfpga.egg-info

venv-remove:
	@rm -fr venv

clean: venv
	$</bin/py3clean fpga
	@rm -fr build
