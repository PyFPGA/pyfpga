#!/bin/bash

FLAGS="-fsynopsys -fexplicit -frelaxed --std=08"

ghdl -a $FLAGS ../../hdl/fakes/generics.vhdl
ghdl --synth $FLAGS -gBOO=true -gINT=255 -gLOG=\'1\' -gSTR="WXYZ" Params

ghdl --synth $FLAGS -gBOO=true -gINT=255 -gLOG=\'1\' -gSTR="WXYZ" -gVEC="11111111" Params
ghdl --synth $FLAGS -gBOO=true -gINT=255 -gLOG=\'1\' -gSTR="WXYZ" -gVEC=\"11111111\" Params
ghdl --synth $FLAGS -gBOO=true -gINT=255 -gLOG=\'1\' -gSTR="WXYZ" -gREA=1.1 Params

#ghdl --synth $FLAGS -gBOO=true -gINT=255 -gLOG=\'1\' -gVEC=\"11111111\" -gSTR="WXYZ" -gREA=1.1 Params
