#!/usr/bin/make

VENV=venv

all: install-hooks venv-create

venv-create:
	virtualenv $(VENV) --python=python3
	$(VENV)/bin/python3 -m pip install -e .
	$(VENV)/bin/python3 -m pip install pyclean
	$(VENV)/bin/python3 -m pip install pycodestyle
	$(VENV)/bin/python3 -m pip install pylint
	$(VENV)/bin/python3 -m pip install pytest
	@rm -fr pyfpga.egg-info

venv-remove:
	@rm -fr $(VENV)

clean:
	@$(VENV)/bin/py3clean .
	@rm -fr build .pytest_cache

clean-all: clean venv-remove
