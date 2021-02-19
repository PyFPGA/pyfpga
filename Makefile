#!/usr/bin/make

check:
	pycodestyle fpga examples test
	pylint -s n fpga
	git diff --check --cached
	pytest test

clean:
	py3clean .
	rm -fr build .pytest_cache
