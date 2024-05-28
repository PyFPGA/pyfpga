#!/usr/bin/make

.PHONY: docs

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
	rm -fr build .pytest_cache

submodule:
	git submodule update --init
