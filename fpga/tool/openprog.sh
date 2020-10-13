#!/bin/bash
#
# Copyright (C) 2020 Rodrigo A. Melo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

###############################################################################
# Things to tuneup
###############################################################################

FAMILY={family}
PROJECT={project}

###############################################################################
# Support
###############################################################################

set -e

DOCKER="docker run --rm -v $HOME:$HOME -w $PWD"
DOCKER="$DOCKER --device /dev/bus/usb ghdl/synth:prog"

###############################################################################
# Programming
###############################################################################

if [[ $FAMILY == "ice40" ]]; then

$DOCKER iceprog $PROJECT.bit

#elif [[ $FAMILY == "ecp5" ]]; then

#$DOCKER openocd -f /usr/share/trellis/misc/openocd/ecp5-evn.cfg \
#-c "transport select jtag; init; svf $PROJECT.svf; exit"

else

echo "ERROR: unsuported tool" && exit 1

fi
