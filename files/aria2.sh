#!/bin/bash
### BEGIN INIT INFO
# Provides:          aria2
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remofe_fs
# Short-Description: Start aria2 download manager
# Description:       Start aria2 download manager
### END INIT INFO

. /etc/default/aria2
ARIA_DAEMON=/usr/bin/aria2c
PIDFILE=/var/run/aria2.pid

test -f $ARIA_DAEMON || exit 0

start() {
    echo "Starting aria2"
    nohup start-stop-daemon --start --quiet --chuid $ARIA_USER --cdir=$ARIA_HOME \
                            --exec $ARIA_DAEMON -- $ARIA_PARAMS
}
stop() {
    echo "Stopping aria2"
    start-stop-daemon --oknodo --chuid $ARIA_USER --stop \
                      --user $ARIA_USER --exec $ARIA_DAEMON
}
status() {
    dbpid=`pgrep -fu $USER $DAEMON`
    if [ -z "$dbpid" ]; then
        echo "aria2 daemon not running"
    else
        echo "aria2 daemon running"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart|reload|force-reload)
        stop
        start
        ;;
    *)
        echo "Usage: /etc/init.d/aria2c {start|stop|restart|reload|force-reload|status}"
        exit 2
esac
exit 0
