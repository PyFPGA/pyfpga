#!/usr/bin/make

ise:
	xtclsh ise.tcl

vivado:
	vivado -mode batch -notrace -quiet -source vivado.tcl

quartus:
	quartus_sh --script quartus.tcl

libero:
	libero SCRIPT:libero.tcl
