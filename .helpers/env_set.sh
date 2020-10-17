# PATHs

ISE_DIR=/opt/Xilinx/ise
VIVADO_DIR=/opt/Xilinx/vivado
QUARTUS_DIR=/opt/Intel/quartus
LIBERO_DIR=/opt/Microsemi/libero

# Extra info

LIBERO_LIC_PORT=1702
LIBERO_LIC_HOST=localhost
LIBERO_LMGRD_DIR=/opt/Microsemi/Linux_Licensing_Daemon
LIBERO_LIC_FILE=/opt/Microsemi/License.dat
LIBERO_LIC_LOG=/tmp/libero-license.log

# Exports

TOOL=$1

if [ -z "$TOOL" ]; then
    TOOL=all
fi

## Xilinx

if [ $TOOL == "all" ] || [ $TOOL == "vivado" ]; then
    echo "Configuring Vivado"
    export PATH=$VIVADO_DIR/bin:$PATH
fi

if [ $TOOL == "all" ] || [ $TOOL == "ise" ]; then
    echo "Configuring ISE"
    export PATH=$ISE_DIR/ISE/bin/lin64:$PATH
fi

## Intel/Altera

if [ $TOOL == "all" ] || [ $TOOL == "quartus" ]; then
    echo "Configuring Quartus"
    export PATH=$PATH:$QUARTUS_DIR/quartus/bin
    # Platform Designer (Qsys) workaround
    export PERL5LIB=$QUARTUS_DIR/quartus/linux64/perl/lib/5.28.1
fi

# Microchip/Microsemi/Actel

if [ $TOOL == "all" ] || [ $TOOL == "libero" ]; then
    echo "Configuring Libero"
    export PATH=$PATH:$LIBERO_DIR/Libero/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu
    export LM_LICENSE_FILE=$LIBERO_LIC_PORT@$LIBERO_LIC_HOST
    if [ -z `pidof lmgrd` ]; then
        echo "Launcingh Microsemi License manager... "
        $LIBERO_LMGRD_DIR/lmgrd -c $LIBERO_LIC_FILE -l $LIBERO_LIC_LOG
    else
        echo "Microsemi License manager is already running... "
    fi
fi

if [ $TOOL == "stop" ]; then
    $LIBERO_LMGRD_DIR/lmutil lmdown -c $LIBERO_LIC_FILE -q
fi
