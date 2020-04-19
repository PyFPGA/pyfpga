project new example.xise

project set family  spartan6
project set device  xc6slx9
project set package csg324
project set speed   -2

xfile add ../hdl/blinking.vhdl
xfile add ../examples/ise/s6micro.ucf

project set top Blinking

process run "Synthesize" -force rerun

process run "Translate" -force rerun
process run "Map" -force rerun
process run "Place & Route" -force rerun

process run "Generate Programming File" -force rerun

project close
