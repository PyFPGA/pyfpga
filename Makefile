#!/usr/bin/make

lint:
	pycodestyle pyfpga examples test
	pylint -s n pyfpga
	git diff --check --cached

test:
	pytest test

clean:
	py3clean .
	rm -fr build .pytest_cache

submodule:
	 git submodule update --init
