#!/usr/bin/make

ifdef MOCKS
export PATH := $(PATH):$(PWD)/../test/mocks
$(info INFO: using MOCKS for the vendor EDA tools)
endif

DIRS=$(wildcard */)

all:
	@$(foreach DIR, $(DIRS), make -C $(DIR) || exit;)
