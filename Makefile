#!/usr/bin/make

.PHONY: docs test

docs:
	cd docs; make html

lint:
	pycodestyle pyfpga examples test
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
