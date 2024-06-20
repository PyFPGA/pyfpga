#!/usr/bin/make

.PHONY: docs

docs:
	cd docs; make html

lint:
	pycodestyle pyfpga examples tests
	pylint -s n pyfpga
	git diff --check --cached

test:
	cd tests; pytest

clean:
	py3clean .
	cd docs; make clean
	rm -fr build .pytest_cache

submodule-init:
	git submodule update --init --recursive

submodule-update:
	cd examples/resources; git checkout main; git pull
