#!/bin/bash

# Copyright (C) 2010 Embecosm Limited

# Contributor Jeremy Bennett <jeremy.bennett@embecosm.com>
# Contributor Simon Cook <simon.cook@embecosm.com>

# A script to get the IP of the next available GDB Server

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.          

# ------------------------------------------------------------------------------

# Usage

# ./get-ip.sh [--rotate] [--delete <ip_address>]

# Get the top IP address from a file of addresses, rotating it to the bottom
# of the file if --rotate is specified. Delete the given IP address if
# --delete is specified.
 
ipfile=`dirname ${DEJAGNU}`/ip-avail.txt
tmp=/tmp/get-ip-$$
lockfile=`dirname ${DEJAGNU}`/get-ip-lockfile
arg1=$1
arg2=$2
ip=""

# Lock all the file manipulation.
(
    flock -e 200

while [ "x${ip}" == "x" ]; do
    # Check we have an IP address available
    if [ ! -s ${ipfile} ]
    then
	echo "No IP addresses available" >&2
	exit 255
    fi

    # Get the top IP address
    ip=`head -1 ${ipfile}`

    # Optionally move it to the bottom of the IP file or delete it
    if [ "x--rotate" == "x${arg1}" ]
    then
	tail -n +2 ${ipfile} > ${tmp}
	echo ${ip} >> ${tmp}
	mv ${tmp} ${ipfile}
    fi

    if [ "x--delete" == "x${arg1}" ]
    then
	sed -i ${ipfile} -e "/${arg2}/d"
    fi

    # Because we cycle IPs that may be in use, check with telnet
    if [ "x--delete" != "x${arg1}" ]
    then
        ipaddr=`echo ${ip} | cut -d ':' -f 1`
        ipport=`echo ${ip} | cut -d ':' -f 2`
	echo '' | telnet ${ipaddr} ${ipport} 2>&1 | \
            grep "Connection closed by foreign host." > /dev/null 2>&1
        if [ $? -eq 0 ]; then
	    echo -n ${ip}
	else
 	    ip=''
	fi
    fi
done

) 200> ${lockfile}
