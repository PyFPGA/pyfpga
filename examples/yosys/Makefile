#!/usr/bin/make

SCRIPTS = $(wildcard *.py)

all:
	@$(foreach SCRIPT, $(SCRIPTS), python3 $(SCRIPT) || exit; python3 $(SCRIPT) --lang vhdl || exit; )
