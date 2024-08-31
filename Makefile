#!/usr/bin/make

.PHONY: docs

all: docs lint test

docs:
	cd docs; make html

lint:
	pycodestyle pyfpga examples tests
	pylint -s n pyfpga
	git diff --check --cached

test:
	pytest

clean:
	py3clean .
	cd docs; make clean
	rm -fr .pytest_cache
	rm -fr `find . -name results`
	rm -fr `find . -name __pycache__`
