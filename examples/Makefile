#!/usr/bin/make


DIRS=$(wildcard */)

all:
	@$(foreach DIR, $(DIRS), make -C $(DIR);)
