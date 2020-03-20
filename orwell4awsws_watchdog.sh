#!/bin/bash

# Add to crontab
#*/5 * * * * ~/orwell4awsws_watchdog.sh bocchibot 2>&1 | /usr/bin/logger -t hubotAlive

# Change to suit where you install your script and what you want to call it
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

