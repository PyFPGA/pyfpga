project new example.xise

project set family  spartan6
project set device  xc6slx9
project set package csg324
project set speed   -2

xfile add ../../hdl/fakes/parameters.v
project set top Params
project set "Generics, Parameters" "BOO=True INT=92 LOG=1 VEC=204 STR=\"WXYZ\" REA=1.0" -process "Synthesize - XST"
process run "Synthesize" -force rerun

xfile add ../../hdl/fakes/generics.vhdl
project set top Params
project set "Generics, Parameters" "BOO=True INT=92 LOG='1' VEC=\"11001100\" STR=\"WXYZ\" REA=1.0" -process "Synthesize - XST"
process run "Synthesize" -force rerun

project close
