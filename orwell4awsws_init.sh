#!/bin/bash
# title             orwell4awsws_init.sh
# description:      service init script for orwell4awsws
# author:           Rich Bocchinfuso
# email:            rbocchinfuso@gmail.com
# date:             20200319
# version:          0.2.0    
# usage:            bash orwell4awsws_init.sh [start|stop|restart|status]
# default-start:    2 3 4 5
# default-stop:     0 1 6
#==============================================================================

# change to suit your install
USER="bocchrj"
USER_HOME="/home/$USER"
DAEMON_NAME="orwell4awsws"
ORWELL_ROOT="$USER_HOME/$DAEMON_NAME"
DAEMON="$ORWELL_ROOT/$DAEMON_NAME.py"

# the process ID of the script when it runs is stored here:
PIDFILE="$ORWELL_ROOT/$DAEMON_NAME.pid"

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    $DAEMON    
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc -p $PIDFILE "$DAEMON_NAME" $DAEMON_NAME && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0