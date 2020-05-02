project new example.xise

project set family  spartan6
project set device  xc6slx9
project set package csg324
project set speed   -2

xfile add ../../hdl/fakes/parameters.v
project set top Params
# BOO can be 1 or true
project set "Generics, Parameters" "BOO=true INT=255 LOG=1 VEC=255 STR=\"WXYZ\" REA=1.1" -process "Synthesize - XST"
process run "Synthesize" -force rerun

xfile add ../../hdl/fakes/generics.vhdl
project set top Params
# BOO can be 1 or true
project set "Generics, Parameters" "BOO=true INT=255 LOG='1' VEC=\"11111111\" STR=\"WXYZ\" REA=1.1" -process "Synthesize - XST"
process run "Synthesize" -force rerun

project close
