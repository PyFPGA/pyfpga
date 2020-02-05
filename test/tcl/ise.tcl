project new $PROJECT.xise

project set family  $FAMILY
project set device  $DEVICE
project set package $PACKAGE
project set speed   $SPEED

xfile add $FILE

project set top $TOP

process run "Synthesize" -force rerun

process run "Translate" -force rerun
process run "Map" -force rerun
process run "Place & Route" -force rerun

process run "Generate Programming File" -force rerun

project close
