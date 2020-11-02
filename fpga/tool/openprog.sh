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

set -e

###############################################################################
# Things to tuneup
###############################################################################

FAMILY={family}
PROJECT={project}

#
# Tools configuration
#

OCI_ENGINE="{oci_engine}"

CONT_ICEPROG="{cont_iceprog}"
CONT_OPENOCD="{cont_openocd}"

TOOL_ICEPROG="{tool_iceprog}"
TOOL_OPENOCD="{tool_openocd}"

###############################################################################
# Programming
###############################################################################

if [[ $FAMILY == "ice40" ]]; then
    $OCI_ENGINE $CONT_ICEPROG $TOOL_ICEPROG $PROJECT.bit
elif [[ $FAMILY == "ecp5" ]]; then
    $OCI_ENGINE $CONT_OPENOCD $TOOL_OPENOCD \
        -f /usr/share/trellis/misc/openocd/ecp5-evn.cfg \
        -c "transport select jtag; init; svf $PROJECT.svf; exit"
else
    echo "ERROR: unsuported tool" && exit 1
fi
