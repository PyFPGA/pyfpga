#!/usr/bin/make

VENV=venv

all: install-hooks venv-create

venv-create:
	virtualenv $(VENV) --python=python3
	$(VENV)/bin/python3 -m pip install -e .
	$(VENV)/bin/python3 -m pip install pyclean
	$(VENV)/bin/python3 -m pip install pycodestyle
	$(VENV)/bin/python3 -m pip install pylint
	@rm -fr pyfpga.egg-info

venv-remove:
	@rm -fr $(VENV)

HOOKS = $(notdir $(basename $(wildcard .helpers/*.sh)))

install-hooks:
	@$(foreach HOOK,$(HOOKS), echo "* Installing $(HOOK)";\
		ln -sf ../../.helpers/$(HOOK).sh .git/hooks/$(HOOK);\
	)

clean: venv-create
	$(VENV)/bin/py3clean .
	@rm -fr build
