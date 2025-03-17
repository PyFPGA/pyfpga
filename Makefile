#!/usr/bin/make

.PHONY: docs

ifeq ($(OS),Windows_NT)
  PATH_SEP := ;
else
  PATH_SEP := :
endif
export PATH := $(CURDIR)/tests/mocks$(PATH_SEP)$(PATH)

all: docs lint test

docs:
	cd docs; make html

lint:
	pycodestyle pyfpga examples tests
	pylint -s n pyfpga
	git diff --check --cached

test:
	pytest
	cd tests && bash regress.sh

clean:
	py3clean .
	rm -fr docs/build
	rm -fr .pytest_cache
	rm -fr `find . -name results`
	rm -fr `find . -name __pycache__`
