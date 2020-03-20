#!/bin/bash
# title             orwell4awsws_watchdog.sh
# description:      service init script for orwell4awsws
# author:           Rich Bocchinfuso
# email:            rbocchinfuso@gmail.com
# date:             20200319
# version:          0.2.0    
# usage:            bash orwell4awsws_watchdog.sh
    # add to crontab
    # */5 * * * * ~/orwell4awsws_watchdog.sh bocchibot 2>&1 | /usr/bin/logger -t hubotAlive
# default-start:    2 3 4 5
# default-stop:     0 1 6
#==============================================================================

# change to suit your install
DAEMON_USER="bocchrj"
USER_HOME="/home/$DAEMON_USER"
DAEMON_NAME="orwell4awsws"
ORWELL_ROOT="$USER_HOME/$DAEMON_NAME"
DAEMON="$ORWELL_ROOT/$DAEMON_NAME.py"

PID=$(ps -aux | grep -w python | grep -w ${DAEMON_NAME} | grep -v grep | awk '{print $2}')

echo "PID: ${PID}"

if [ -n "${PID// }" ] ; then
    echo "`date`: $DAEMON_NAME service running, everything is fine"
else
    echo "`date`: $DAEMON_NAME service NOT running, starting service."
    $DAEMON
fi

